# coding: utf-8

_package_data = dict(
    full_package_name='ruamel.std.pathlib',
    version_info=(0, 9, 2),
    __version__='0.9.2',
    version_timestamp='2022-02-19 08:36:38',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    since=2013,
    description='improvements over the standard pathlib module',
    entry_points=None,
    license='MIT License',
    tox=dict(env='*',),
    python_requires='>=3',  # 3.7
    print_allowed=True,
)

version_info = _package_data['version_info']
__version__ = _package_data['__version__']

###########

import os  # NOQA
import sys  # NOQA
import inspect  # NOQA
import pathlib  # NOQA

from pathlib import *  # NOQA

from typing import Any, Union, Optional, Dict, Generator, Tuple, List  # NOQA


# https://bugs.python.org/issue24132#msg401946
# without this you cannot subclass or assign data attributes (methods always worked fine)
class Path(type(pathlib.Path())):  # type: ignore
    def utime_ns(self, atime_ns: int, mtime_ns: int) -> None:
        os.utime(self, ns=(atime_ns, mtime_ns), follow_symlinks=False)

    def read_bytes_atime_preserve(self, *arg: Any, **kw: Any) -> bytes:
        stat = os.stat(self)
        res: bytes = self.read_bytes(*arg, **kw)
        os.utime(self, ns=(stat.st_atime_ns, stat.st_mtime_ns), follow_symlinks=False)
        return res

    def read_text_atime_preserve(self, *arg: Any, **kw: Any) -> str:
        stat = os.stat(self)
        res: str = self.read_text(*arg, **kw)
        os.utime(self, ns=(stat.st_atime_ns, stat.st_mtime_ns), follow_symlinks=False)
        return res


if sys.version_info < (3, 9):

    def _is_relative_to(self, other):
        try:
            self.relative_to(other)
            return True
        except ValueError:
            return False

    Path.is_relative_to = _is_relative_to


class DirStack(object):
    def __init__(self) -> None:
        self._dir_stack: list[str] = []

    def pushd(self, d: Union[str, Path]) -> None:
        self._dir_stack.insert(0, os.getcwd())
        os.chdir(str(d))

    def popd(self) -> None:
        os.chdir(self._dir_stack.pop())


# global stack, always there
_dir_stack = DirStack()


def pushd(d: Union[str, Path]) -> None:
    _dir_stack.pushd(d)


def popd() -> None:
    _dir_stack.popd()


# just for some sanity
pathlib.Path.remove = pathlib.Path.unlink  # type: ignore


def _rmtree(self: Path) -> None:
    import shutil

    assert self.is_dir()
    shutil.rmtree(str(self))


Path.rmtree = _rmtree  # type: ignore


def _chdir(self: Path) -> None:
    assert self.is_dir()
    os.chdir(str(self))


Path.chdir = _chdir  # type: ignore


def _hash(self: Path, typ: Optional[str] = None, size: int = -1) -> Any:
    """hash of the contents, typ can be any of the hashlib.new() acceptable strings
    if size is provided and non-negative only read that amount of bytes from the start
    of the file
    """
    import hashlib

    if typ is None:
        typ = 'sha224'
    with self.open(mode='rb') as f:
        data = f.read(size)
    h = hashlib.new(typ, data=data)
    return h


pathlib.Path.hash = _hash  # type: ignore


def _copy(self: Path, target: Union[str, Path]) -> None:
    import shutil

    assert self.is_file()
    shutil.copy(str(self), str(target))


pathlib.Path.copy = _copy  # type: ignore


# this is the times parameter of os.utime, taking int/float seconds (and not nanoseconds)
if sys.version_info < (3, 6):

    def _utime(self: Path, atime: int, mtime: int) -> None:
        os.utime(str(self), (atime, mtime), follow_symlinks=False)


else:

    def _utime(self: Path, atime: int, mtime: int) -> None:
        os.utime(self, (atime, mtime), follow_symlinks=False)


pathlib.Path.utime = _utime  # type: ignore


# #
# # - If the check level is set at 1, any calls that are issued with strings that
# #     could be changed are logged (to the console), those are the positions where
# #     arguments should still be converted from string to Path.
# # - If check level is set at 2, all call to pl methods are logged, those
# #     are the areas where the calls can be replaced by methods on the Path instance,
# #     check level 3 is the same as level 1, but any remaining string isntances throw
# #         an error.


class PathLibConversionHelper(object):
    """
    if you are changing to use the standard pathlib library, it is cumbersome
    to change everything at once, and also to change all the arguments to calls to
    os.path.join, os.rename, os.path.dirname to be made encapsulated in str()

    by making an instance of PathLibConversionHelper named pl you can change
    os.path.join() to pl.path.join(), etc., and then start passing in Path instances
    instead of strings.

    if the check level is set at 1 any calls that are issued with strings that
    could be changed are logged (to the console), those are the positions where
    arguments should still be converted from string to Path
    if check level is set at 2, all calls to pl methods are logged, those
    are the areas where the calls can be replaced by methods on the Path instance,
    check level 3 is the same as level 1, but any remaining string instances throw
    an error.

    maybe look at https://github.com/mikeorr/Unipath#comparision-with-osospathshutil-and-pathpy
    and incorporate
    """

    def __init__(self, check: int = 0) -> None:
        class Container(object):
            pass

        self._check = check
        self._usage: Dict[Any, list[int]] = {}
        path = self.path = Container()
        for m in dir(self):
            if not m.startswith('_path_'):
                continue
            attr = m.split('_', 2)[2]
            setattr(path, attr, getattr(self, m))

    def add_usage(self, vars: Any, comment: str) -> None:
        if isinstance(vars, (list, tuple)):
            vt = tuple([isinstance(x, Path) for x in vars])
        else:
            vt = tuple([isinstance(vars, Path)])
        if self._check < 1:
            return
        caller = inspect.stack()[2]
        t = caller[1], caller[2], comment, vt
        count = self._usage.setdefault(t, [0])
        count[0] += 1
        if self._check > 1 and count[0] == 1:
            print('{2} [{0}:{1} / Path {3}]'.format(*t))

    def dump(self, stream: Any = None, show_all: bool = False) -> None:
        """dump unique invocations of methods

        unless show_all is True, invocations that uniquely use Path arguments
        are not shown
        """
        if stream is None:
            stream = sys.stdout
        for t in self._usage:
            if show_all or not all(t[3]):
                print(
                    '{t[2]} [{t[0]}:{t[1]} / {count} / Path {t[3]}]'.format(
                        count=self._usage[t][0], t=t
                    )
                )

    def rename(self, old_name: Union[str, Path], new_name: Union[str, Path]) -> None:
        """os.rename replacement that can handle Path argument"""
        self.add_usage([old_name, new_name], 'update .rename')
        if isinstance(old_name, Path):
            old_name.rename(new_name)  # rename works with strings and Path
        else:
            os.rename(old_name, str(new_name))

    # os.rename
    # os.getcwd
    # os.path.expanduser

    def walk(
        self, top: Union[str, Path], *args: Any, **kw: Any
    ) -> Generator[Tuple[Path, List[str], List[str]], None, None]:
        for r, d, f in os.walk(str(top), *args, **kw):
            yield Path(r), d, f

    def _path_join(self, base: Union[str, Path], *args: str) -> Union[str, Path]:
        self.add_usage([base] + list(args), 'update .path.join to use "/"')
        # os.path.join
        if isinstance(base, Path):
            return base.joinpath(*args)
        else:
            return os.path.join(base, *args)

    def _path_exists(self, path: Union[str, Path]) -> bool:
        self.add_usage(path, 'update .exists to use Path.exists()')
        if isinstance(path, Path):
            return path.exists()
        else:
            return os.path.exists(path)

    def _path_dirname(self, file_name: Union[str, Path]) -> Union[str, Path]:
        self.add_usage(file_name, 'update .path.dirname to use Path.parent')
        if isinstance(file_name, Path):
            return file_name.parent
        else:
            return os.path.dirname(file_name)

    def _path_getmtime(self, file_name: Union[str, Path]) -> float:
        self.add_usage(file_name, 'update .path.getmtime to use Path.stat().st_mtime')
        if isinstance(file_name, Path):
            return file_name.stat().st_mtime
        else:
            return os.path.getmtime(file_name)

    def _path_expanduser(self, path: Union[str, Path]) -> Union[str, Path]:
        self.add_usage(path, 'update .path.expanduser to use Path.expanduser')
        if isinstance(path, Path):
            return path.expanduser()
        else:
            return os.path.expanduser(path)

    def _path_basename(self, path: Union[str, Path]) -> str:
        self.add_usage(path, 'update .path.basename to use Path.basename')
        if isinstance(path, Path):
            return path.name
        else:
            return os.path.basename(path)

    def _path_isdir(self, path: Union[str, Path]) -> bool:
        self.add_usage(path, 'update .path.isdir to use Path.isdir')
        if isinstance(path, Path):
            return path.is_dir()
        else:
            return os.path.isdir(path)

    def _path_splitext(self, path: Union[str, Path]) -> Any:
        self.add_usage(
            path, 'update .path.splitext to use Path.parent / Path.stem + Path.suffix'
        )
        if isinstance(path, Path):
            return path.parent / path.stem, path.suffix
        else:
            return os.path.splitext(path)

    def chdir(self, path: Union[str, Path]) -> Any:
        """replaces: os.chdir()"""
        self.add_usage(path, 'update .chdir to use Path.chdir() or os.chdir(str(Path))')
        if isinstance(path, Path):
            return path.chdir()  # type: ignore
        else:
            return os.chdir(path)

    # os.mkdir

    def rmdir(self, path: Union[str, Path]) -> bool:
        """replaces: os.rmdir()"""
        self.add_usage(path, 'update .rmdir to use Path.rmdir() or os.rmdir(str(Path))')
        if isinstance(path, Path):
            return path.rmdir()  # type: ignore
        else:
            return os.rmdir(path)  # type: ignore

    def makedirs(self, path: Union[str, Path], *args: Any, **kw: Any) -> None:
        """replaces: os.makedirs()"""
        self.add_usage(path, 'update .makedirs to use Path.mkdir()')
        os.makedirs(str(path), *args, **kw)

    def remove(self, path: Union[str, Path]) -> Any:
        """replaces: os.remove()"""
        self.add_usage(path, 'update .remove to use Path.remove() or os.remove(str(Path))')
        if isinstance(path, Path):
            return path.remove()  # type: ignore
        else:
            return os.remove(path)

    def listdir(self, path: Union[str, Path] = '.') -> Any:
        """replaces: os.listdir()"""
        return os.listdir(str(path))

    def glob(self, pattern: str) -> Union[List[str], List[Path]]:
        """replaces: glob.glob()"""
        import glob

        self.add_usage(pattern, 'update .glob to use Path.glob()')
        if isinstance(pattern, Path):
            return [Path(fn) for fn in glob.glob(str(pattern))]
        else:
            return glob.glob(pattern)

    # shutil.rmtree
    def rmtree(self, path: Union[str, Path]) -> Any:
        """replaces: shutil.rmtree()"""
        import shutil

        self.add_usage(path, 'update .rmtree to use Path.rmtree() or shutil.rmtree(str(Path))')
        if isinstance(path, Path):
            return path.rmtree()  # type: ignore
        else:
            return shutil.rmtree(path)

    # shutil.copy
    def copy(self, src: Union[str, Path], dst: Union[str, Path]) -> Any:
        """replaces: shutil.copy()"""
        import shutil

        self.add_usage(
            src, 'update .copy to use Path.copy() or shutil.copy(str(src), str(dst))'
        )
        if isinstance(src, Path):
            return src.copy(dst)  # type: ignore
        else:
            return shutil.copy(str(str), str(dst))

    # built-in open
    def open(self, path: Union[str, Path], mode: str = 'r', buffering: int = 1) -> Any:
        """replaces: built-in open()"""
        self.add_usage(path, 'update .open to use Path.open()')
        if isinstance(path, Path):
            return path.open(mode, buffering)
        else:
            return open(path, mode, buffering)

    def mkstemp(
        self,
        suffix: Any = "",
        prefix: Optional[str] = None,
        dir: Optional[Union[str, Path]] = None,
        text: bool = False,
    ) -> Any:
        """replaces: tempfile.mkstemp()"""
        import tempfile

        if prefix is None:
            prefix = tempfile.template
        self.add_usage(dir, 'update .mkstemp to use Path.mkstemp()')
        if isinstance(dir, Path):
            dir = str(dir)
        return tempfile.mkstemp(suffix, prefix, dir, text)
