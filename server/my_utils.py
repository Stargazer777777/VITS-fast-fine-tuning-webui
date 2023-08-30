from os import path, getcwd

current_path = path.dirname(path.abspath(__file__))

root_dir = path.dirname(current_path)


def get_abs_path(*paths: str):
    return path.join(root_dir, *paths)
