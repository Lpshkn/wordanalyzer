"""
Tests for analyzer/word_analyzer.py module
"""
import unittest
import os
from analyzer.word_analyzer import WordAnalyzer
from math import log


class WordAnalyzerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.words = ['one', 'two', 'three', 'four', 'five', 'six']
        self.frequency_words = ['three', 'two', 'five', 'one', 'four']

        self.word_cost = dict((k, log((i + 1) * log(len(self.frequency_words)))) for i, k in enumerate(self.frequency_words))
        self.word_analyzer = WordAnalyzer(self.words, self.frequency_words)

    def test_correct_constructor(self):
        self.assertEqual(self.frequency_words, self.word_analyzer.frequency_words)
        self.assertEqual(self.words, self.word_analyzer.words)
        self.assertEqual(self.word_cost, self.word_analyzer.splitter.word_cost)

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
        sum_cost = sum([self.word_cost.get(word, self.word_analyzer.default_cost) for word in
                        self.word_analyzer.splitter.split(text)])

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

    def test_correct_clear_word(self):
        # self.frequency_words used as a dictionary
        # Remove incorrect symbols
        self.assertEqual(self.word_analyzer.get_clear_word('one$two123'), 'onetwo')

        # Replace leet symbols and remove incorrect
        self.assertEqual(self.word_analyzer.get_clear_word('0n3f1v3@#$%'), 'onefive')
        self.assertEqual(self.word_analyzer.get_clear_word(''), '')
        self.assertEqual(self.word_analyzer.get_clear_word(' '), '')
        self.assertEqual(self.word_analyzer.get_clear_word('12345'), '')
        self.assertEqual(self.word_analyzer.get_clear_word('onetwothreefour'), 'onetwothreefour')
        self.assertEqual(self.word_analyzer.get_clear_word('0one1two3th@re@ef$o^ur'), 'onetwothreefour')

    def test_incorrect_clear_word(self):
        with self.assertRaises(TypeError):
            self.word_analyzer.get_clear_word(None)
        with self.assertRaises(TypeError):
            self.word_analyzer.get_clear_word([])
        with self.assertRaises(TypeError):
            self.word_analyzer.get_clear_word(42)

    def test_build_bk_tree(self):
        # test is empty file
        with open('test', 'w'):
            with self.assertRaises(ValueError):
                self.word_analyzer.build_bk_tree('test')
        os.remove('test')

        # Check that the tree will be saved, i.e. file 'test' will be create
        tree = self.word_analyzer.build_bk_tree('test')
        self.assertTrue(os.path.isfile('test'))

        # Now load the bk-tree from existed file 'test' and compare original tree and loaded tree
        tree2 = self.word_analyzer.build_bk_tree('test')
        self.assertEqual(tree.tree, tree2.tree)
        os.remove('test')

    def test_correct_similar_words(self):
        self.assertEqual(self.word_analyzer.get_similar_words('one', distance=0), ['one'])
        self.assertEqual(self.word_analyzer.get_similar_words('one', number_similar_words=5, distance=3),
                         ['two', 'five', 'one', 'four'])
        self.assertEqual(self.word_analyzer.get_similar_words('one', number_similar_words=5, distance=4),
                         self.frequency_words)

        self.assertEqual(self.word_analyzer.get_similar_words(''), None)

    def test_incorrect_similar_words(self):
        with self.assertRaises(TypeError):
            self.word_analyzer.get_similar_words(None)
