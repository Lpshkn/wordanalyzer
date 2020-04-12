"""
This module contains functions for processing string, clearing from incorrect symbols or another actions with it
"""

import re


def leet_transform(word: str, indices: list) -> str:
    """
    This functions clears the passed word from digits, service symbols or any incorrect characters.
    Also it corrects "leet" characters if their indices were passed
    :param word: the word you need to correct
    :param indices: indices of incorrect characters that will be corrected
    :return: corrected word
    """

    # "Leet" characters that need to be replaced
    comparison = {
        '$': 's',
        '1': 'i',
        '0': 'o',
        '3': 'e',
        '@': 'a'
    }

    for index in indices:
        # Get corrected symbol
        symbol = comparison.get(word[index])

        if not symbol:
            continue

        # Build corrected word
        word = word[:index] + symbol + word[index + 1:]

    # Remove all incorrect symbols
    return re.sub(r'[\W\d\s_]+', r'', word)


def get_indices_incorrect_symbols(word: str) -> list:
    """
    Function returns the list of all indices incorrect characters in the passed word
    :param word: the passed word in which you need to find indices
    :return: list of found indices
    """

    arr = []
    index = 0
    for char in re.findall(r'[\W\d\s]', word):
        index = word.index(char, __start=index)
        arr.append(index)
        index += 1

    return arr
