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

    if postfix:
        print(postfix)

    return processed_words


def identify_basics(words: list, splitter: TextSplitter, destination: str = None) -> list:
    """
    This function identifies the base parts of a word, applies the stemming to them and returns a list of base words.
    If the destination is specified, then saves the list into this file.

    :param words: a list of words which will be processed
    :param splitter: an instance of the TextSplitter to split a word to parts
    :param destination:  a filename that you want to save a list to
    :return: a list of base words
    """
    stemmer = SnowballStemmer('english')
    file = open(destination, 'a') if destination else None
    basics = set()

    for word in words:
        for part in splitter.split(word):
            part = part.lower()
            cost = splitter.word_cost.get(part)
            if cost:
                basics.add(stemmer.stem(part))

    if file:
        file.writelines(list(basics))

    return list(basics)


def convert_flags(flags: int) -> list:
    """
    This method receives a decimal number means flags which a user chose and selects from this number all flags.

    :param flags: a number meaning flags that a user chose
    :return: a list of flags
    """
    convert = []
    while flags:
        flag = flags & (~flags + 1)
        convert.append(flag)
        flags ^= flag

    return convert
