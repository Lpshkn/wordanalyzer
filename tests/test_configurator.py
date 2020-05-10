"""
The tests for the analyzer/arguments_parser.py module
"""
import io
import os
import unittest.mock
from analyzer.configurator import Configurator


class ArgumentsParserTest(unittest.TestCase):
    def setUp(self):
        args = ['-s', 'source', '-f', 'frequency']
        self.configurator = Configurator(args)

    @unittest.mock.patch("sys.stderr", new_callable=io.StringIO)
    def test_empty_input_words(self, error):
        args = []
        with self.assertRaises(SystemExit):
            configurator = Configurator(args)

        # Check that this error is what we expected
        self.assertTrue("No action requested, add -s/--source or -w/--words" in error.getvalue())

    @unittest.mock.patch("sys.stderr", new_callable=io.StringIO)
    def test_empty_frequency_words(self, error):
        args = ['-w' 'word']
        with self.assertRaises(SystemExit):
            configurator = Configurator(args)

        # Check that this error is what we expected
        self.assertTrue("you must specify a file containing a list of frequency words" in error.getvalue())

    def test_default_values(self):
        args = ['-w', 'first', 'second', '-f', 'frequency']
        configurator = Configurator(args)
        parameters = configurator._get_parameters(args)

        # These parameters have no default value
        self.assertIsNone(parameters.count)
        self.assertIsNone(parameters.tree)
        self.assertIsNone(parameters.source)

        # These parameters are flags and are false by default
        self.assertFalse(parameters.clear_word)
        self.assertFalse(parameters.total_cost)
        self.assertFalse(parameters.verbose)

        # These parameters have a default value
        self.assertEqual(parameters.encoding, 'utf-8')
        self.assertEqual(parameters.destination, 'output.txt')
        self.assertEqual(parameters.number_corrected, 2)
        self.assertEqual(parameters.threshold, 2)
        self.assertEqual(parameters.distance, 1)
        self.assertEqual(parameters.similar_words, 4)

    def test_input_words(self):
        args = ['-w', 'first', 'second', '-f', 'frequency']
        parameters = Configurator(args)._parameters

        self.assertEqual(parameters.words, ['first', 'second'])
        self.assertEqual(parameters.frequency, 'frequency')

    def test_get_correct_words(self):
        args = ['-w', 'first', 'second', '-f', 'frequency', '-s', 'source']
        configurator = Configurator(args)

        # -w flag should cover the -s flag
        self.assertEqual(configurator.get_words(), ['first', 'second'])

    def test_get_destination(self):
        args = ['-w', 'first', 'second', '-f', 'frequency', '-d', 'new_file.txt']
        configurator = Configurator(args)

        self.assertEqual(configurator.get_destination(), 'new_file.txt')

    def test_get_frequency_words_wrong(self):
        with self.assertRaises(FileNotFoundError):
            self.configurator.get_frequency_words()

    @unittest.mock.patch('sys.stdout', open(os.devnull, 'w'))
    def test_get_frequency_words_correct(self):
        with open('frequency', 'w') as file:
            file.write('teststring')

        self.assertEqual(self.configurator.get_frequency_words(), ['teststring'])
        os.remove('frequency')

    def test_get_words_sourcefile_wrong(self):
        with self.assertRaises(FileNotFoundError):
            self.configurator.get_words()

    @unittest.mock.patch('sys.stdout', open(os.devnull, 'w'))
    def test_get_words_sourcefile_correct(self):
        with open('source', 'w') as file:
            file.write('teststring')

        self.assertEqual(self.configurator.get_words(), ['teststring'])
        os.remove('source')
