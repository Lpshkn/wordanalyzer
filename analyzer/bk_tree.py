"""
This module implements an interface between the BKTree class and operations with it
"""

import pickle
from pybktree import BKTree
from similarity.damerau import Damerau


class BuildBKTree(BKTree):
    @staticmethod
    def build_tree(words):
        if not words:
            raise WordsBKTreeError("The passed list of words is empty")

        tree = BuildBKTree(Damerau().distance, words)
        return tree

    @staticmethod
    def save_tree(filename, tree):
        if not filename:
            raise FileBKTreeError("The file where you're going to save the bk-tree has the incorrect name")

        with open(filename, 'wb') as file:
            pickle.dump(tree, file)
        return tree

    @staticmethod
    def load_tree(filename):
        tree = pickle.load(filename)
        return tree


class WordsBKTreeError(Exception):
    def __init__(self, text):
        self.text = text


class FileBKTreeError(Exception):
    def __init__(self, text):
        self.text = text
