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
    def __init__(self, frequency_words: list, filename_tree: str = None,
                 number_similar_words: int = 4, distance: int = 1, threshold: int = 2,
                 number_of_corrected_words: int = 4):
        """
        :param frequency_words: list of words ordered by frequency usage
        """

        if not isinstance(frequency_words, (list, tuple)):
            raise TypeError("List must be list type")

        # Lists can't be empty or None
        if not frequency_words:
            raise ValueError("The list of words is empty")

        # It's necessary the each element is str type in the list
        if not all(isinstance(word, str) for word in frequency_words):
            raise TypeError("The list of words has a non string type element")

        self.frequency_words = frequency_words

        self.splitter = TextSplitter(frequency_words)

        # Build BK-tree for correcting words
        self.tree = self.build_bk_tree(filename_tree)

        # If the word isn't in the dictionary, then its cost is default_cost
        self.default_cost = 100

        # How many similar words will be returned by get_similar_words method
        self.number_similar_words = number_similar_words
        # What distance will be used to search for similar words
        self.distance = distance
        # How many parts will be spliced in the get_correct_words method
        self.threshold = threshold
        # How many words will be returned by get_correct_words method
        self.number_of_corrected_words = number_of_corrected_words

    def get_total_cost(self, text: str) -> int:
        """
        Calculate total cost of the text based on cost of the each word
        :param text: the text without spaces
        :return: total sum of costs
        """

        return sum([self.splitter.word_cost.get(word, self.default_cost) for word in self.splitter.split(text)])

    def get_clear_word(self, word: str):
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

                    print("The bk-tree is loading from {}...".format(filename))
                    tree = pickle.load(file)

                    if not isinstance(tree, bk.BKTree):
                        raise TypeError("Was loaded not bk-tree")

                    print("The bk-tree loaded successfully")

                    return tree
            else:
                print("The bk-tree is building...")
                tree = bk.BKTree(Damerau().distance, self.frequency_words)
                print("The bk-tree is saving to {}...".format(filename))
                with open(filename, 'wb') as file:
                    pickle.dump(tree, file)

                print("The bk-tree built and saved successfully")
                return tree
        else:
            print("The bk-tree is building...")
            tree = bk.BKTree(Damerau().distance, self.frequency_words)
            print("The bk-tree built successfully")
            return tree

    def get_similar_words(self, word: str) -> list:
        """
        This function finds all similar words to passed word depending on the Damerau's distance. Function returns
        only first number_similar_words (by default, 4) words of the most similar words.

        :param word: function will find similar words to this word
        :return: list of the most similar words
        """

        number_similar_words = self.number_similar_words
        distance = self.distance

        found_words = self.tree.find(word, distance)

        arr = [[self.get_total_cost(it[1]), it[1]] for it in found_words]
        if arr:
            arr = sorted(arr)[:number_similar_words]
            return [it[1] for it in arr]
        else:
            return None

    def get_correct_words(self, word: str) -> set:
        """
        This function clears passed word, then splits it to some parts and in turn splice these parts into one word,
        trying to find the cheapest for each. How many parts will be spliced is determined by the threshold argument.
        By changing threshold parameter, you can reach at an optimal correcting. After correcting many corrected
        words will be returned. How many determined by number_of_corrected_words. You can change that parameter
        in order to build optimal list of corrected words.

        :param word: word that will be corrected
        :return: list of corrected words
        """

        minimum_parts = 2
        threshold = self.threshold
        number_of_corrected_words = self.number_of_corrected_words

        word = self.get_clear_word(word)
        parts = self.splitter.split(word)
        evaluated_words = []

        def replace_correcting_parts(parts: list, similar_words: list, indices: list) -> list:
            """
            This function receives parts - list of parts of a word. Some of these parts whose indices are passed as
            third argument splice into one word and similar words to that word pass to this function.
            Indices - indices of those parts of a word that were spliced into one. So, this function pastes
            one of the similar words to the places indicated by indices, then that all splices with the rest
            parts of a word and then it will be evaluated. The cost of the full spliced word with this word will be
            appended into the list. The list containing all these similar spliced words with their cost
            will be returned.

            :param parts: list of parts of a word
            :param similar_words: list of similar to a word which will be replaced
            :param indices: indices of those parts of a word that were spliced into one
            :return: list of (cost of full spliced word, this word)
            """

            i, j = indices
            full_words_with_cost = []
            for similar_word in similar_words:
                full_word = ''.join(parts[:i] + [similar_word] + parts[j:])
                cost = self.get_total_cost(full_word)
                full_words_with_cost.append([cost, full_word])

            return full_words_with_cost

        # If after splitting the count of parts isn't enough
        if len(parts) < minimum_parts:
            arr = []
            for part in parts:
                similar = self.get_similar_words(part)
                if similar:
                    arr.extend(similar)

            arr = sorted(evaluated_words)[:number_of_corrected_words]
            if word:
                arr.append(word)
            return set(arr)

        for i in range(len(parts)):
            # That value will decrease
            max_range = threshold if threshold <= len(parts) - i else len(parts) - i

            for j in range(i + minimum_parts, max_range + i + 1):
                spliced_word = ''.join(parts[i:j])
                similar_words = self.get_similar_words(spliced_word)

                if similar_words:
                    full_words = replace_correcting_parts(parts, similar_words, (i, j - 1))
                    evaluated_words.extend(full_words)

        arr = sorted(evaluated_words)[:number_of_corrected_words]
        if word:
            arr.append([0, word])

        return set(it[1] for it in arr)

    def set_number_similar_words(self, number: int):
        if not isinstance(number, int):
            raise TypeError("Number is not int")

        self.number_similar_words = number
        return self

    def set_distance(self, distance: int):
        if not isinstance(distance, int):
            raise TypeError("distance is not int")

        self.distance = distance
        return self

    def set_threshold(self, threshold: int):
        if not isinstance(threshold, int):
            raise TypeError("threshold is not int")

        self.threshold = threshold
        return self

    def set_number_of_corrected_words(self, number_of_corrected_words: int):
        if not isinstance(number_of_corrected_words, int):
            raise TypeError("number_of_corrected_words is not int")

        self.number_of_corrected_words = number_of_corrected_words
        return self
