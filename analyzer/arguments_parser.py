"""
This module implements reading arguments from the command line. Also this module specifies default paths to files
located in the root directory.
"""

from argparse import ArgumentParser
from os.path import dirname, join

PROJECT_ROOT = dirname(dirname(__file__))
DATA_DIRECTORY = join(PROJECT_ROOT, 'data')
PASSWORDS_FILE = join(DATA_DIRECTORY, 'rockyou.txt')
FREQUENCY_FILE = join(DATA_DIRECTORY, 'frequency_words.txt')
DESTINATION_FILE = join(PROJECT_ROOT, 'new_words.txt')


def arguments_parser() -> ArgumentParser:
    """
    Define command line arguments which will be received by the program

    :return: instance of ArgumentParser()
    """
    parser = ArgumentParser(prog='wordanalyzer',
                            description='This program analyzes the source set of words was obtained from the file '
                                        '(-s parameter), clear this set from incorrect symbols, split cleared words '
                                        'to lexemes, then correct them by replacing assumed incorrect words to right '
                                        'words and then will create new set of words and save it to the '
                                        'destination file (-d parameter)',
                            epilog='Lpshkn, 2020')

    parser.add_argument('-s', '--source',
                        help='the source file containing the set of words you need to analyze',
                        default=PASSWORDS_FILE,
                        type=str)

    parser.add_argument('-f', '--frequency',
                        help="the dictionary ordered by frequency of word usage, which will be used to perform the "
                             "splitting text and correcting incorrect words (if the dictionary parameter -w isn't "
                             "override)",
                        default=FREQUENCY_FILE,
                        type=str)

    parser.add_argument('-d', '--destination',
                        help="the destination file where the processed set of source words will be saved",
                        default=DESTINATION_FILE,
                        type=str)

    parser.add_argument('-w', '--words-dictionary',
                        help="the dictionary which will be used to perform correcting incorrect words (by default, "
                             "the same file as in -f parameter)",
                        type=str)

    parser.add_argument('-c', '--count',
                        help="count of words which will be processed (set of words will be selected randomly)",
                        type=int)

    parser.add_argument('-e', '--encoding',
                        help='encoding of the file',
                        default='utf-8',
                        type=str)

    parser.add_argument('-t', '--tree',
                        help="filename, where the bk-tree will be saved or from will be loaded. If it specified and "
                             "this file exists, then tree will be loaded from this file. Else if it specified, but "
                             "doesn't exist, it will be built and saved to this file",
                        type=str)

    return parser
