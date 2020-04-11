"""
Tests for analyzer/word_analyzer.py module
"""
import unittest
import wordninja
from word_analyzer import WordAnalyzer
from math import log


class WordAnalyzerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.words = ['one', 'two', 'three', 'four', 'five', 'six']
        self.frequency_words = ['three', 'two', 'five', 'one', 'four']

        self.word_cost = dict((k, log((i + 1) * log(len(self.words)))) for i, k in enumerate(self.words))
        self.word_analyzer = WordAnalyzer(self.words, self.frequency_words)

    def test_correct_constructor(self):
        self.assertEqual(self.frequency_words, self.word_analyzer.frequency_words)
        self.assertEqual(self.words, self.word_analyzer.words)
        self.assertEqual(self.word_cost, self.word_analyzer.word_cost)

    def test_incorrect_constructor(self):
        with self.assertRaises(ValueError):
            WordAnalyzer([], self.frequency_words)

        with self.assertRaises(ValueError):
            WordAnalyzer(self.words, [])

        with self.assertRaises(TypeError):
            WordAnalyzer(None, None)

        with self.assertRaises(TypeError):
            WordAnalyzer(1, self.frequency_words)

        with self.assertRaises(TypeError):
            WordAnalyzer(self.words, 'string')

    def test_correct_total_cost(self):
        text = 'onetwothreefour'
        sum_cost = sum([self.word_cost.get(word, self.word_analyzer.default_cost) for word in wordninja.split(text)])

        self.assertEqual(self.word_analyzer.get_total_cost(text), sum_cost)
        # 'six' will be split to 3 letters
        self.assertEqual(self.word_analyzer.get_total_cost('six'), self.word_analyzer.default_cost * 3)
        self.assertNotEqual(self.word_analyzer.get_total_cost('two'), self.word_analyzer.default_cost)
        self.assertEqual(self.word_analyzer.get_total_cost(''), 0)

    def test_incorrect_total_cost(self):
        with self.assertRaises(TypeError):
            self.word_analyzer.get_total_cost([])
        with self.assertRaises(TypeError):
            self.word_analyzer.get_total_cost(None)
        with self.assertRaises(TypeError):
            self.word_analyzer.get_total_cost(42)