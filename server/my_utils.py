from os import path, getcwd, remove
import shutil

current_path = path.dirname(path.abspath(__file__))

root_dir = path.dirname(current_path)


def get_abs_path(*paths: str):
    return path.join(root_dir, *paths)


def rm_abs_dir(*paths: str):
    dirname = get_abs_path(*paths)
    if path.exists(dirname):
        shutil.rmtree(dirname)


def rm_abs_file(*paths: str):
    filepath = get_abs_path(*paths)
    if path.exists(filepath):
        remove(filepath)
