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
        self.assertEqual(parsed.count, None)
        self.assertEqual(parsed.words_dictionary, None)

        # These parameters have default value
        self.assertEqual(parsed.destination, ap.DESTINATION_FILE)
        self.assertEqual(parsed.source, ap.PASSWORDS_FILE)
        self.assertEqual(parsed.frequency, ap.FREQUENCY_FILE)

    def test_correct_input(self):
        parsed = self.parser.parse_args(['-s', 'source.txt', '--destination', 'destination.txt',
                                         '--frequency', 'frequency', '-c', '100'])

        # Count is int
        self.assertEqual(parsed.count, 100)
        self.assertEqual(parsed.destination, 'destination.txt')
        self.assertEqual(parsed.source, 'source.txt')
        self.assertEqual(parsed.frequency, 'frequency')

        # Dictionary isn't specified
        self.assertEqual(parsed.words_dictionary, None)

    def test_incorrect_input(self):
        # One argument is expected
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['-s'])

        # Type error because the destination is string
        with self.assertRaises(TypeError):
            self.parser.parse_args(['-d', 1234])

        # This parameter is unknown
        with self.assertRaises(SystemExit) :
            self.parser.parse_args(['-q', 'txt'])
