"""
Tests for analyzer/arguments_parser.py module
"""
import unittest
import analyzer.arguments_parser as ap


class ArgumentsParserTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Parser is instance of ArgumentParser class, contains handled arguments
        """
        self.parser = ap.arguments_parser()

    def test_default_values(self):
        parsed = self.parser.parse_args([])

        # These parameters haven't default value
        self.assertIsNone(parsed.count)
        self.assertIsNone(parsed.tree)

        self.assertFalse(parsed.verbose)

        # These parameters have default value
        self.assertEqual(parsed.encoding, 'utf-8')
        self.assertEqual(parsed.destination, ap.DESTINATION_FILE)
        self.assertEqual(parsed.source, ap.PASSWORDS_FILE)
        self.assertEqual(parsed.frequency, ap.FREQUENCY_FILE)
        self.assertEqual(parsed.number_corrected, 4)
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

    def test_incorrect_input(self):
        # Type error because the destination is string
        with self.assertRaises(TypeError):
            self.parser.parse_args(['-d', 1234])
