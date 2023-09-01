import os
import shutil

current_path = os.path.dirname(os.path.abspath(__file__))

root_dir = os.path.dirname(current_path)


def get_abs_path(*paths: str):
    return os.path.join(root_dir, *paths)


def rm_abs_dir(*paths: str):
    dirname = get_abs_path(*paths)
    if os.path.exists(dirname):
        shutil.rmtree(dirname)


def rm_abs_file(*paths: str):
    filepath = get_abs_path(*paths)
    if os.path.exists(filepath):
        os.remove(filepath)


def mkdir_ifnot_exist(path: str):
    if not os.path.exists(path):
        os.mkdir(path)
