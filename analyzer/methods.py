"""
This module contains functions for processing string, clearing from incorrect symbols or another actions with it
"""

import re
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


def process_words(function, words: list, destination: str = None, prefix: str = None, postfix: str = None,
                  verbose_pattern: str = None, file_pattern: str = None, duplicate: bool = False):
    """
    This function applies the passed function to the list of words, then processes these words and prints all results
    in the command line or/and saves to the file if necessary. All preferences are set by the passed arguments.

    :param function: a function will be used to a list of words
    :param words: a list of words that you need to process
    :param destination: specify the filename, if you need to save results to the file
    :param prefix: this message will be printed before processing
    :param postfix: this message will be printed after successful processing
    :param verbose_pattern: words will be inserted into this pattern and this string will be passed into stdout.
            If it isn't specified, the string won't be printed
    :param file_pattern: words will be inserted into this pattern and this string will be saved into the file.
            If it isn't specified, only processed words will be saved.
    :param duplicate: if it's specified and it's True, duplicates won't be deleted
    """
    if prefix:
        print(prefix)

    file = open(destination, 'w') if destination else None
    for word in words:
        processed = function(word)

        # Convert to one form
        if not isinstance(processed, Iterable):
            processed = [processed]

        for processed_word in processed:
            if verbose_pattern:
                print(verbose_pattern.format(word, processed_word))
            if file:
                if file_pattern:
                    file.write(file_pattern.format(word, processed_word))
                else:
                    file.write(processed_word)
                file.write('\n')
                file.flush()

    # Delete duplicates
    if file:
        file.close()
        if not duplicate and destination:
            with open(destination, 'r+') as file:
                words = set(word.lower() for word in file.readlines())
                file.truncate(0)
                file.writelines(words)

    if postfix:
        print(postfix)