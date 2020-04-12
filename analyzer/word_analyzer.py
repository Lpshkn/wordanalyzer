"""
This module provides WordAnalyzer class that is a wrapper for words dictionary and any functions for
working with them.
"""

from math import log
from .text_splitter import TextSplitter
from .methods import (get_all_combinations, get_indices_incorrect_symbols, leet_transform)


class WordAnalyzer:
    def __init__(self, words: list, frequency_words: list):
        """
        :param words: list of words which you need to analyze
        :param frequency_words: list of words ordered by frequency usage
        """

        if not isinstance(words, (list, tuple)) or not isinstance(frequency_words, (list, tuple)):
            raise TypeError("Lists must be list type")

        # Lists can't be empty or None
        if words == [] or frequency_words == []:
            raise ValueError("The list of words is empty")

        # It's necessary the each element is str type in the list
        if not all(isinstance(word, str) for word in words) or not \
                all(isinstance(word, str) for word in frequency_words):

            raise TypeError("The list of words has a non string type element")

        self.words = words
        self.frequency_words = frequency_words

        self.splitter = TextSplitter(frequency_words)

        # If the word isn't in the dictionary, then its cost is default_cost
        self.default_cost = 100

    def get_total_cost(self, text: str) -> int:
        """
        Calculate total cost of the text based on cost of the each word
        :param text: the text without spaces
        :return: total sum of costs
        """

        if not isinstance(text, str):
            raise TypeError("Text must be str type")

        return sum([self.splitter.word_cost.get(word, self.default_cost) for word in self.splitter.split(text)])

    def get_clear_word(self, word):
        """
        This function iterates through all possible combinations of indices, which were obtained from
        get_indices_incorrect_symbols and the call to the get_all_combinations function.
        Function returns the cheapest found word among all these combinations.

        :param word: word that will be cleared
        :return: the cheapest cleared word
        """

        # Get all indices of incorrect symbols
        indices = get_indices_incorrect_symbols(word)
        # Define the word which will be override
        cleared_word = [9e999, '']
        # Get all combinations of indices
        all_combinations = get_all_combinations(indices)

        # Define an empty combination. It's important in order to check the cost of the word without changes
        all_combinations.append([])

        # Find the cheapest cleared word among all the possible combinations of indices,
        # which will be used to clear the word
        for combinations in all_combinations:
            prepared_str = leet_transform(word, combinations)

            total_cost = self.get_total_cost(prepared_str.lower())
            if total_cost < cleared_word[0]:
                cleared_word = [total_cost, prepared_str]

        return cleared_word[1]
