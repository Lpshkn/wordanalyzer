"""
This module implements loading words from the file
"""

import codecs
from random import sample


def load_words(words_filename, count=None):
    """
    :param words_filename: str - filename
    :param count: int - count of words which will be processed
    :return: list(str) - list of loaded words
    """

    with codecs.open(words_filename, 'r', 'ANSI') as f:
        data = f.read().splitlines()

    return sample(data, count) if count else data
