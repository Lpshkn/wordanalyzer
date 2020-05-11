"""
This module implements an interface between the BKTree class and operations with it
"""

import os
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
        if not isinstance(tree, BKTree):
            raise WrongTreeError("You're trying to save into the file not a BK-tree object")
        if os.path.isfile(filename) and os.stat(filename).st_size != 0:
            raise FileBKTreeError("The file what you specified is not empty. It's unable to write into that file")

        with open(filename, 'wb') as file:
            pickle.dump(tree, file)
        return tree

    @staticmethod
    def load_tree(filename):
        if not filename or not os.path.isfile(filename):
            raise FileBKTreeError("This file of the bk-tree structure doesn't exist")

        try:
            with open(filename, 'rb') as file:
                tree = pickle.load(file)
                if not isinstance(tree, BKTree):
                    raise WrongTreeError("You're trying to load from the file not a BK-tree object")

        except pickle.UnpicklingError:
            raise FileBKTreeError("This file of the bk-tree structure doesn't contain any bk-tree structure actually")
        except EOFError:
            raise FileBKTreeError("The bk-tree file you specified is empty and can't be loaded")

        return tree


class WordsBKTreeError(Exception):
    def __init__(self, text):
        self.text = text


class FileBKTreeError(Exception):
    def __init__(self, text):
        self.text = text


class WrongTreeError(Exception):
    def __init__(self, text):
        self.text = text
