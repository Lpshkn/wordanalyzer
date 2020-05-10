"""
The tests for the analyzer/arguments_parser.py module
"""
import unittest
import analyzer.arguments_parser as ap


class ArgumentsParserTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        A parser is an instance of the ArgumentParser class containing handled arguments
        """
        self.parser = ap.arguments_parser()

    def test_default_values(self):
        # Pass an empty list
        parsed = self.parser.parse_args([])

        # These parameters have no default value
        self.assertIsNone(parsed.count)
        self.assertIsNone(parsed.tree)
        self.assertIsNone(parsed.source)
        self.assertIsNone(parsed.frequency)
        self.assertIsNone(parsed.words)

        # These parameters are flags and are false by default
        self.assertFalse(parsed.clear_word)
        self.assertFalse(parsed.total_cost)
        self.assertFalse(parsed.verbose)

        # These parameters have a default value
        self.assertEqual(parsed.encoding, 'utf-8')
        self.assertEqual(parsed.destination, 'output.txt')
        self.assertEqual(parsed.number_corrected, 2)
        self.assertEqual(parsed.threshold, 2)
        self.assertEqual(parsed.distance, 1)
        self.assertEqual(parsed.similar_words, 4)

    def test_correct_input(self):
        parsed = self.parser.parse_args(['-s', 'source.txt', '--destination', 'destination.txt',
                                         '--frequency', 'frequency', '-c', '100'])

        # Count is int
        self.assertEqual(parsed.count, 100)
        self.assertEqual(parsed.destination, 'destination.txt')
        self.assertEqual(parsed.source, 'source.txt')
        self.assertEqual(parsed.frequency, 'frequency')
