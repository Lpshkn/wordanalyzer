"""
This module provides WordAnalyzer class that is a wrapper for words dictionary and any functions for
working with them.
"""

from math import log
from text_splitter import TextSplitter


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

        # Words' cost calculated by Zipf's law
        self.word_cost = dict((k, log((i + 1) * log(len(words)))) for i, k in enumerate(words))

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

        return sum([self.word_cost.get(word, self.default_cost) for word in self.splitter.split(text)])
