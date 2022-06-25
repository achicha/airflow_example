from typing import List


def read_file(file_path: str) -> List[str]:
    """
        Open and read a file by given path
    :param file_path: path to file
    :return: list with string lines
    """

    with open(file_path, 'r') as f:
        lines = [i.strip() for i in f.readlines()]

    return lines
