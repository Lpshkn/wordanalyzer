"""
Tests for analyzer/methods.py module
"""
import unittest
import analyzer.methods as methods


class LeetTransformTest(unittest.TestCase):
    def test_correct_input(self):
        # Replace all leet characters
        self.assertEqual(methods.leet_transform('Th1$is0nmyl3@p', [2, 3, 6, 11, 12]), 'Thisisonmyleap')

        # Replace only one character, delete the rest
        self.assertEqual(methods.leet_transform("on3tw0th@$w12", [2]), 'onetwthw')

        # Delete all incorrect characters
        self.assertEqual(methods.leet_transform('1@$03_/?#$%@!%^&*()_+={}', []), '')

        # There are no any symbols
        self.assertEqual(methods.leet_transform('', []), '')

        # There are no incorrect characters and leet symbols too
        self.assertEqual(methods.leet_transform('string', [4]), 'string')

    def test_incorrect_input(self):
        # The list can't be None
        with self.assertRaises(TypeError):
            methods.leet_transform("string", None)

        # Incorrect type instead of string
        with self.assertRaises(TypeError):
            methods.leet_transform(1, [])

        with self.assertRaises(TypeError):
            methods.leet_transform(None, [])

        # The symbol with index 3 doesn't exist
        with self.assertRaises(IndexError):
            methods.leet_transform('str', [3])
