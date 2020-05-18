"""
This module implements loading words from the file
"""

import codecs
import sys
import os
from random import sample
from os import stat


def load_words(words_filename: str, count: int = None, encoding: str = 'utf-8') -> list:
    """
    :param encoding: encoding of the file
    :param words_filename: str - filename
    :param count: int - count of words which will be processed
    :return: list(str) - list of loaded words
    """

    if not isinstance(words_filename, str):
        raise TypeError("That type isn't string!")

    if not os.path.isfile(words_filename):
        raise FileNotFoundError(f"Error: this file: \"{words_filename}\" doesn't exist!")

    if stat(words_filename).st_size == 0:
        raise EmptyFileError(f"Error: The specified file: \"{words_filename}\" is empty!")

    if count is not None and count <= 0:
        raise ValueError("Error: The number of words that you want to load can't be 0 and less")

    with codecs.open(words_filename, 'r', encoding) as f:
        data = f.read().splitlines()

    return sample(data, count) if count else data


class EmptyFileError(Exception):
    """
    The error will be raised when empty file is passed to input
    """
    def __init__(self, text):
        self.text = text
