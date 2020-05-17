"""
Tests for analyzer/load_data.py module
"""

import unittest
from analyzer.load_data import load_words, EmptyFileError
import os


class LoadDataTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setup 2 files - empty file and file with numbers.
        They will be processed in the future.
        """
        self.filename = 'test_file.txt'
        self.empty_file = 'empty_file.txt'
        self.count = 10

        with open(self.filename, 'w') as file:
            for i in range(self.count):
                file.write(str(i) + '\n')

        file = open(self.empty_file, 'w')
        file.close()

    def test_incorrect_filename(self):
        # If file doesn't exist
        with self.assertRaises(FileNotFoundError):
            load_words('1234incorrect')

        # If type is incorrect
        with self.assertRaises(TypeError):
            load_words(words_filename=None)

    def test_empty_file(self):
        with self.assertRaises(EmptyFileError):
            load_words(self.empty_file)

    def test_incorrect_count(self):
        # If count is incorrect (1 <= count <= n)
        with self.assertRaises(ValueError):
            load_words(self.filename, self.count + 1)
        with self.assertRaises(ValueError):
            load_words(self.filename, -1)

        # Count can't be 0
        with self.assertRaises(ValueError):
            load_words(self.filename, 0)

    def test_correct_data(self):
        # data - list of numbers from 0 to 9
        data = load_words(self.filename)

        self.assertEqual(data, [str(i) for i in range(self.count)])

    def test_correct_count(self):
        self.assertEqual(5, len(load_words(self.filename, 5)))

    def tearDown(self) -> None:
        os.remove(self.filename)
        os.remove(self.empty_file)
