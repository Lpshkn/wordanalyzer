"""
Tests for analyzer/methods.py module
"""
import unittest
import analyzer.methods as methods


class LeetTransformTest(unittest.TestCase):
    """
    Tests for leet_transform function
    """
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


class GetIndicesIncorrectSymbolsTest(unittest.TestCase):
    """
    Tests for get_indices_incorrect_symbols function
    """

    def test_correct_input(self):
        self.assertEqual(methods.get_indices_incorrect_symbols('!i@n#c$o%r^r&e*c(t)'),
                         [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])

        # The are no incorrect characters
        self.assertEqual(methods.get_indices_incorrect_symbols('correctword'), [])
        self.assertEqual(methods.get_indices_incorrect_symbols(''), [])

        # The are all symbols are incorrect
        self.assertEqual(methods.get_indices_incorrect_symbols('1234567890_'), list(range(10)))
        self.assertEqual(methods.get_indices_incorrect_symbols('`~!@#$%^&*()-+="№;%:?'), list(range(21)))

    def test_incorrect_input(self):
        with self.assertRaises(TypeError):
            methods.get_indices_incorrect_symbols(None)
        with self.assertRaises(TypeError):
            methods.get_indices_incorrect_symbols(42)
        with self.assertRaises(TypeError):
            methods.get_indices_incorrect_symbols([])


class GetAllCombinationsTest(unittest.TestCase):
    """
    Tests for get_all_combinations function
    """
    def test_correct_input(self):
        self.assertEqual(methods.get_all_combinations([]), [])
        self.assertEqual(methods.get_all_combinations([1, 2, 3]),
                         [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)])
        self.assertEqual(methods.get_all_combinations([1]), [(1,)])

    def test_incorrect_input(self):
        with self.assertRaises(TypeError):
            methods.get_all_combinations(None)
        with self.assertRaises(TypeError):
            methods.get_all_combinations([1, 'str'])
        with self.assertRaises(TypeError):
            methods.get_all_combinations(1)
