from os.path import join, dirname, abspath


def absolute(relative_path):
    relative_path_string = join(*relative_path)
    return absolute_from_string(relative_path_string)

def absolute_from_string(relative_path):
    root_dir = dirname(dirname(dirname(abspath(__file__))))
    return join(root_dir, relative_path)