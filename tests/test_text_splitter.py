"""
Tests for analyzer/text_splitter.py module
"""
import unittest
from text_splitter import TextSplitter
from math import log


class TextSplitterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.words = ['first', 'second', 'third']
        self.splitter = TextSplitter(self.words)

    def test_correct_input(self):
        max_len = max(len(word) for word in self.words)
        cost = dict((word, log((number + 1) * log(len(self.words)))) for number, word in enumerate(self.words))

        self.assertEqual(max_len, self.splitter.max_len)
        self.assertEqual(cost, self.splitter.word_cost)

    def test_incorrect_input(self):
        # Words can't be empty or None
        with self.assertRaises(ValueError):
            TextSplitter([])
        with self.assertRaises(ValueError):
            TextSplitter(None)

        # Words can't contain non str type elements
        words_int = ['first', 1, 'second']
        with self.assertRaises(TypeError):
            TextSplitter(words_int)

    def test_correct_split(self):
        # Words isn't contained in the list will be split by letters
        self.assertEqual(['first', 'second', 'third', 'a', 'b', 'c'], self.splitter.split('firstsecondthirdabc'))
        self.assertEqual([], self.splitter.split(''))
        
    def test_incorrect_split(self):
        # Split function can't receive non str type argument
        with self.assertRaises(TypeError):
            self.splitter.split(None)

        with self.assertRaises(TypeError):
            self.splitter.split(['string'])

        with self.assertRaises(TypeError):
            self.splitter.split(1)
        



