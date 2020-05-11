import unittest
import os
from analyzer.bk_tree import BuildBKTree, BKTree, WordsBKTreeError, FileBKTreeError, WrongTreeError
from similarity.damerau import Damerau


class BuildBKTreeTest(unittest.TestCase):
    def setUp(self):
        self.words = ['first', 'second']
        self.distance = Damerau().distance

    def tearDown(self):
        if os.path.isfile('test'):
            os.remove('test')

    def test_build_tree_correct(self):
        self.assertEqual(BuildBKTree.build_tree(self.words).tree, BKTree(self.distance, self.words).tree)
        self.assertNotEqual(BuildBKTree.build_tree(['5555']).tree, BKTree(self.distance, self.words).tree)

    def test_build_tree_incorrect_words(self):
        with self.assertRaises(WordsBKTreeError):
            BuildBKTree.build_tree([])
        with self.assertRaises(WordsBKTreeError):
            BuildBKTree.build_tree(None)

    def test_save_tree_incorrect_filename(self):
        with self.assertRaises(FileBKTreeError):
            BuildBKTree.save_tree(None, BuildBKTree.build_tree(['123']))
        with self.assertRaises(FileBKTreeError):
            BuildBKTree.save_tree("", BuildBKTree.build_tree(['123']))

    def test_save_tree_correct_filename(self):
        filename = 'test'
        BuildBKTree.save_tree(filename, BuildBKTree.build_tree(['123']))

        self.assertTrue(os.path.isfile(filename))
        self.assertTrue(os.stat(filename).st_size != 0)

    def test_save_tree_incorrect_tree(self):
        filename = 'test'

        with self.assertRaises(WrongTreeError):
            BuildBKTree.save_tree(filename, '123')
        with self.assertRaises(WrongTreeError):
            BuildBKTree.save_tree(filename, [])
        with self.assertRaises(WrongTreeError):
            BuildBKTree.save_tree(filename, None)
