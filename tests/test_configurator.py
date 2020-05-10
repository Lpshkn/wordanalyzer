"""
The tests for the analyzer/arguments_parser.py module
"""
import io
import unittest.mock
from analyzer.configurator import Configurator


class ArgumentsParserTest(unittest.TestCase):
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

    def test_correct_input(self):
        parsed = self.parser.parse_args(['-s', 'source.txt', '--destination', 'destination.txt',
                                         '--frequency', 'frequency', '-c', '100'])

        # Count is int
        self.assertEqual(parsed.count, 100)
        self.assertEqual(parsed.destination, 'destination.txt')
        self.assertEqual(parsed.source, 'source.txt')
        self.assertEqual(parsed.frequency, 'frequency')
