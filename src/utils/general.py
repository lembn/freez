import stat
import shutil
import os

from . import platform


def delete(path: str) -> None:
    if os.path.exists(path):
        remove = os.remove if os.path.isfile(path) else shutil.rmtree
        os.chmod(path, stat.S_IWUSR)
        remove(path)


def dirname(path: str, levels: int = 1) -> str:
    for i in range(levels):
        path = os.path.dirname(path)
    return path


def app_path(*paths: str) -> str:
    path = os.path.join(dirname(__file__, 3), "apps", platform.PLATFORM)

    for p in paths:
        path = os.path.join(path, p)

    return path
