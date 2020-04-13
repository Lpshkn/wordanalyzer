"""
This module provides WordAnalyzer class that is a wrapper for words dictionary and any functions for
working with them.
"""

import pickle
import os
import pybktree as bk
from .text_splitter import TextSplitter
from .methods import (get_all_combinations, get_indices_incorrect_symbols, leet_transform)
from similarity.damerau import Damerau


class WordAnalyzer:
    def __init__(self, words: list, frequency_words: list, filename_tree: str = None):
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

        # Build BK-tree for correcting words
        self.tree = self.build_bk_tree(filename_tree)

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

    def build_bk_tree(self, filename: str = None) -> bk.BKTree:
        """
        This function builds the BK-tree based on frequency words. If bk-tree is already saved in the file,
        it will be loaded and returned, if filename was passed. BK-tree builds based on Damerau's distance.

        :param filename: the file where the tree will be saved or from will be loaded
        :return: built BK-tree
        """

        # If filename was passed, then the tree will either be loaded or will be built and saved.
        # Else the tree will be build and just returned without saving
        if filename:
            if os.path.isfile(filename):
                with open(filename, 'rb') as file:
                    if os.stat(filename).st_size == 0:
                        raise ValueError("File is empty")

                    tree = pickle.load(file)

                    if not isinstance(tree, bk.BKTree):
                        raise TypeError("Was loaded not bk-tree")

                    return tree
            else:
                tree = bk.BKTree(Damerau().distance, self.frequency_words)
                with open(filename, 'wb') as file:
                    pickle.dump(tree, file)

                return tree
        else:
            return bk.BKTree(Damerau().distance, self.frequency_words)

    def get_similar_words(self, word: str, number_similar_words=4, distance=1) -> list:
        """
        This function finds all similar words to passed word depending on the Damerau's distance. Function returns
        only first number_similar_words (by default, 4) words of the most similar words.

        :param word: function will find similar words to this word
        :param number_similar_words: how many words will be returned
        :param distance: Damerau's distance
        :return: list of the most similar words
        """
        found_words = self.tree.find(word, distance)

        arr = [[self.get_total_cost(it[1]), it[1]] for it in found_words]
        if arr:
            arr = sorted(arr)[:number_similar_words]
            return [it[1] for it in arr]
        else:
            return None
