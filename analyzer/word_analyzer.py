"""
This module provides WordAnalyzer class that is a wrapper for words dictionary and any functions for
working with them.
"""

from math import log
import wordninja


class WordAnalyzer:
    def __init__(self, words: list, frequency_words: list):
        """
        :param words: list of words which you need to analyze
        :param frequency_words: list of words ordered by frequency usage
        """

        # Words' cost calculated by Zipf's law
        self.word_cost = dict((k, log((i + 1) * log(len(words)))) for i, k in enumerate(words))

        self.words = words
        self.frequency_words = frequency_words

        # If the word isn't in the dictionary, then its cost is default_cost
        self.default_cost = 100

    def get_total_cost(self, text: str) -> int:
        """
        Calculate total cost of the text based on cost of the each word
        :param text: the text without spaces
        :return: total sum of costs
        """
        return sum([self.word_cost.get(word, self.default_cost) for word in wordninja.split(text)])
