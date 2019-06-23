import os


def load_file(file_path):
    """
    Loads and returns content into file.
    :param file_path: Path to the file.
    :return: Content of the file.
    """
    try:
        with open(file_path, 'r') as file:
            data = file.read()
    except IsADirectoryError:
        raise Exception("Reading file '{0}' not possible, because it's a directory.".format(file_path))
    except IOError:
        raise Exception("IOError while reading the '{0}' file.".format(file_path))
    return data


def save_file(file_path, data):
    """
    Saves content into file.
    :param file_path: Path to the file.
    :param data: Content which will be saved.
    :return: Boolean value if the write was successful.
    """
    try:
        f = open(file_path, 'w')
        f.write(data)
        f.close()
    except IOError:
        raise Exception("IOError while writing into the '{0}' file.".format(file_path))


def dir_content(dir_path, ends_with=""):
    """
    Reads content of the directory and returns list of files and directories.
    :param dir_path: Path to the directory.
    :param ends_with: Suffix which files have to contain to be returned.
    :return: List of files which match the suffix filter.
    """
    files = []
    try:
        for file in os.listdir(dir_path):
            if file.endswith(ends_with):
                files.append(file)
    except FileNotFoundError:
        raise Exception("Unable to get content of the directory '{0}', because it doesn't exist.".format(dir_path))
    return files


def get_list_of_files(path, ends_with=""):
    """
    Checks path and returns all files under that path (doesn't use folder recursion).
    :param path: Path to the file or folder.
    :param ends_with: Suffix which files have to contain to be returned.
    :return: List of files which match the suffix filter.
    """
    if os.path.isdir(path):
        files = []
        dir_files = dir_content(path, ends_with)
        for dir_file in dir_files:
            file = os.path.join(path, dir_file)
            files.append(file)
    else:  # file
        if path.endswith(ends_with):
            files = [path]
        else:
            files = []
    return files
