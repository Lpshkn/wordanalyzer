"""
Tests for analyzer/methods.py module
"""
import unittest
import os
import analyzer.methods as methods
import analyzer.configurator as cfg


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


class FactorizeTest(unittest.TestCase):
    """
    Tests for get_all_combinations function
    """

    def test_correct_input(self):
        self.assertEqual(methods.factorize(-100), [])
        self.assertEqual(methods.factorize(0), [])
        self.assertEqual(methods.factorize(1), [])
        self.assertEqual(methods.factorize(2), [1])
        self.assertEqual(methods.factorize(10), [1, 2, 5])
        self.assertEqual(methods.factorize(3453), [1, 3, 1151])
        self.assertEqual(methods.factorize(4354), [1, 2, 7, 14, 311, 622, 2177])

    def test_incorrect_input(self):
        self.assertEqual(methods.factorize(None), [])


class PrintResultsTest(unittest.TestCase):
    def setUp(self):
        self.filename = 'test.txt'

    def tearDown(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)

    def test_correct_input_with_verbose(self):
        word = "word"
        args = ['arg1', 'arg2']
        pattern = '{}, {}, {}'
        with open(self.filename, 'w') as file:
            methods.print_results(word, pattern, args, file, verbose=True)
        with open(self.filename, 'r') as file:
            self.assertEqual(file.read(), "word, arg1, arg2")

    def test_correct_input_without_verbose(self):
        word = "word"
        args = ['arg1', 'arg2']
        pattern1 = '{}, {}'
        pattern2 = '{}, {}, {}, {}'
        with open(self.filename, 'w') as file:
            methods.print_results(word, pattern1, args, file)
        with open(self.filename, 'r') as file:
            self.assertEqual(file.read(), "arg1, arg2")

        with open(self.filename, 'w') as file:
            methods.print_results(word, pattern2, args, file)
        with open(self.filename, 'r') as file:
            self.assertEqual(file.read(), "arg1, arg2, NONE, NONE")

    def test_incorrect_pattern(self):
        args = ['arg1', 'arg2']
        pattern1 = "{}, {}, {"
        pattern2 = "{4}, {6}"
        pattern3 = "{gdfg}"
        pattern4 = ""
        pattern5 = "{}, {}, {fdgdf}"
        with open(self.filename, 'w') as file:
            with self.assertRaises(ValueError):
                methods.print_results('word', pattern1, args, file)
            with self.assertRaises(IndexError):
                methods.print_results('word', pattern2, args, file)
            with self.assertRaises(ValueError):
                methods.print_results('word', pattern3, args, file)
            with self.assertRaises(ValueError):
                methods.print_results('word', pattern4, args, file)
            with self.assertRaises(KeyError):
                methods.print_results('word', pattern5, args, file)

    def test_incorrect_args(self):
        args = []
        pattern1 = "{}, {}"
        with open(self.filename, 'w') as file:
            methods.print_results('word', pattern1, args, file)
        with open(self.filename, 'r') as file:
            self.assertEqual(file.read(), "NONE, NONE")

    def test_args_list(self):
        args = [[1, 2, 3]]
        pattern1 = "{}\n"
        with open(self.filename, 'w') as file:
            methods.print_results('word', pattern1, args, file)
        with open(self.filename, 'r') as file:
            self.assertEqual(file.read(), "1\n2\n3\n")

        args = [[1, [2], 3]]
        with open(self.filename, 'w') as file:
            methods.print_results('word', pattern1, args, file)
        with open(self.filename, 'r') as file:
            self.assertEqual(file.read(), "1\n[2]\n3\n")

        args = [[1, 2], [3, 4]]
        pattern2 = '{}, {}, {}'
        with open(self.filename, 'w') as file:
            methods.print_results('word', pattern2, args, file, True)
        with open(self.filename, 'r') as file:
            self.assertEqual(file.read(), "word, [1, 2], [3, 4]")

    def test_non_word(self):
        args = ['test']
        pattern = "{}, {}"
        with open(self.filename, 'w') as file:
            methods.print_results('', pattern, args, file, True)
        with open(self.filename, 'r') as file:
            self.assertEqual(file.read(), "NONE, test")

    def test_incorrect_file(self):
        args = ['test']
        pattern = "{}, {}"
        with self.assertRaises(TypeError):
            methods.print_results('', pattern, args, "test", True)


class DeleteDuplicatesTest(unittest.TestCase):
    def setUp(self):
        self.filename = 'test.txt'

    def tearDown(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)

    def test_correct_input(self):
        words = ['test', 'test', 'first', 'second', 'first']
        with open(self.filename, 'w') as file:
            for word in words:
                file.write(word + '\n')

        methods.delete_duplicates(self.filename)
        with open(self.filename, 'r') as file:
            self.assertEqual(file.readlines(), ['first\n', 'second\n', 'test\n'])


class GetPatternsTest(unittest.TestCase):
    def setUp(self):
        self.filename = 'test.txt'

    def tearDown(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)

    def test_correct_input(self):
        mode = {cfg.MODE_CORRECT: 'correct', cfg.MODE_BASIC: 'STDOUT', cfg.MODE_CLEAR: 'STDOUT'}
        patterns = methods.get_patterns(mode)
        self.assertEqual(patterns['correct'], '{}\n')
        self.assertEqual(patterns['STDOUT'], '{}, {}\n')

        mode = {cfg.MODE_CORRECT: 'STDOUT', cfg.MODE_BASIC: 'STDOUT', cfg.MODE_CLEAR: 'STDOUT', cfg.MODE_COST: 'STDOUT'}
        patterns = methods.get_patterns(mode, verbose=True)
        self.assertEqual(patterns['STDOUT'], 'word: {}, cost: {}, cleared: {}, corrected: {}, base words: {}\n')

    def test_incorrect_input(self):
        mode = {0: 'STDOUT', cfg.MODE_COST: 'STDOUT'}
        patterns = methods.get_patterns(mode)
        self.assertEqual(patterns['STDOUT'], '{}\n')

    def test_empty_input(self):
        mode = {}
        patterns = methods.get_patterns(mode)
        self.assertEqual(patterns, '')