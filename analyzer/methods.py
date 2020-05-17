"""
This module contains functions for processing string, clearing from incorrect symbols or another actions with it
"""

import re
import collections
import analyzer.configurator as cfg
from collections.abc import Iterable


def leet_transform(word: str, indices: tuple) -> str:
    """
    This functions clears the passed word from digits, service symbols or any incorrect characters.
    Also it corrects "leet" characters if their indices were passed
    :param word: the word you need to correctТак
    :param indices: indices of incorrect characters that will be corrected
    :return: corrected word
    """

    # "Leet" characters that need to be replaced
    comparison = {
        '$': 's',
        '1': 'i',
        '0': 'o',
        '3': 'e',
        '@': 'a',
        '4': 'a',
        '7': 't',
        '6': 'g',
        '5': 's'
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
        index = word.index(char, index)
        arr.append(index)
        index += 1

    return arr


def factorize(number: int) -> list:
    """
    This function calculates all divisors of the number, begin from 1 (except for itself)

    :param number: the number for which you want to find divisors
    :return: list of divisors
    """
    divisors = []
    divisor = 1
    if number:
        while divisor < number:
            if number % divisor == 0:
                divisors.append(divisor)
            divisor += 1
    return divisors


def process_words(word: str, pattern: str, args: list, file, verbose: bool = False):
    """
    This function applies the passed function to the list of words, then processes these words and prints all results
    in the command line or/and saves to the file if necessary. All preferences are set by the passed arguments.
    """
    if verbose:
        if len(args) == 1:
            for arg in args:
                if isinstance(arg, Iterable) and not isinstance(arg, str):
                    for arg_word in arg:
                        file.write(pattern.format(word, arg_word))
                else:
                    file.write(pattern.format(word, arg))
        else:
            args = [arg if arg else 'NONE' for arg in args]
            file.write(pattern.format(word, *args))
    else:
        if len(args) == 1:
            for arg in args:
                if not arg:
                    break

                if isinstance(arg, Iterable) and not isinstance(arg, str):
                    for arg_word in arg:
                        file.write(pattern.format(arg_word))
                else:
                    file.write(pattern.format(arg))
        else:
            args = [arg if arg else 'NONE' for arg in args]
            file.write(pattern.format(*args))
    file.flush()


def delete_duplicates(filename: str):
    if filename:
        with open(filename, 'r+') as file:
            words = set(word.lower() for word in file.readlines())
            file.truncate(0)
            file.writelines(words)


def get_patterns(mode: dict, verbose: bool = False):
    patterns = {filename: ["word: {}"] if verbose else [] for filename in set(mode.values())}

    filename_modes = collections.defaultdict(list)
    for _mode, filename in mode.items():
        filename_modes[filename].append(_mode)

    for filename, _mode in filename_modes.items():
        if cfg.MODE_COST in _mode:
            patterns[filename].append("cost: {}" if verbose else "{}")
        if cfg.MODE_CLEAR in _mode:
            patterns[filename].append("cleared: {}" if verbose else "{}")
        if cfg.MODE_CORRECT in _mode:
            patterns[filename].append("corrected: {}" if verbose else "{}")
        if cfg.MODE_BASIC in _mode:
            patterns[filename].append("base words: {}" if verbose else "{}")

    patterns = {filename: ", ".join(pattern) + '\n' for filename, pattern in patterns.items()}
    return patterns
