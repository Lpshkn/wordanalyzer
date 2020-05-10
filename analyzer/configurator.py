"""
This module represents a configurator which will set any configurations,
get and process the parameters received from the command line
"""
from argparse import ArgumentParser


class Configurator:
    def __init__(self, args):
        # Set descriptions of the program
        self.description = "This program analyzes the source set of words was obtained from the file (-s parameter), " \
                           "clear this set from incorrect symbols, split cleared words to lexemes, then correct " \
                           "them by replacing assumed incorrect words to right words and then will create new set of " \
                           "words and save it to the destination file (-d parameter)."
        self.program_name = "wordanalyzer"
        self.epilog = "Lpshkn, 2020"
        self.parser = self.get_parser()

        # Get parameters from the arguments received from the command line
        self.args = args
        self.parameters = self.get_parameters(self.args)

    def get_parser(self):
        parser = ArgumentParser(prog=self.program_name, description=self.description, epilog=self.epilog)

        parser.add_argument('-s', '--source',
                            help='The source file containing the set of words you need to analyze.',
                            type=str)

        parser.add_argument('-f', '--frequency',
                            help="The dictionary ordered by frequency of word usage, which will be used to perform the "
                                 "splitting text and correcting incorrect words (if the dictionary parameter -w isn't "
                                 "override).",
                            type=str)

        parser.add_argument('-d', '--destination',
                            help="The destination file where the processed set of source words will be saved.",
                            default='output.txt',
                            type=str)

        parser.add_argument('-c', '--count',
                            help="Count of words which will be processed (set of words will be selected randomly).",
                            type=int)

        parser.add_argument('-e', '--encoding',
                            help="Encoding of the file.",
                            default='utf-8',
                            type=str)

        parser.add_argument('-t', '--tree',
                            help="Filename, where the bk-tree will be saved or from will be loaded. If it specified and"
                                 " this file exists, then tree will be loaded from this file. Else if it specified, but"
                                 " doesn't exist, it will be built and saved to this file.",
                            type=str)

        parser.add_argument('-similar', '--similar-words',
                            help="How many similar words will be returned by get_similar_words method. It provides more "
                                 "thorough search for correcting word, but slows down the speed.",
                            default=4,
                            type=int)

        parser.add_argument('-dist', '--distance',
                            help="What Damerau's distance will be used to search for similar words. You must select the "
                                 "lowest optimal value, else the word may be corrected wrongly.",
                            default=1,
                            type=int)

        parser.add_argument('-tres', '--threshold',
                            help="How many parts will be spliced when processing and searching for a correct word. "
                                 "It will influence to searching correct word. You can try to change this value, "
                                 "but it's undesirable.",
                            default=2,
                            type=int)

        parser.add_argument('-n', '--number-corrected',
                            help="How many corrected words will be returned after processing and correcting a word. "
                                 "You should keep in mind that one cleared word (without any incorrect symbols) will be "
                                 "added to the new corrected words.",
                            default=2,
                            type=int)

        parser.add_argument('-cost', '--total-cost',
                            help="Return summary cost for each word passed to input. If it's specified, another methods "
                                 "will not work.",
                            action='store_true')

        parser.add_argument('-clr', '--clear-word',
                            help="Return cleared words from the incorrect symbols depending on the total sum of the word. "
                                 "If it's specified, another methods will not work. This method replaces -sum option.",
                            action='store_true')

        parser.add_argument('-w', '--words',
                            nargs='+',
                            help="Input list of words which you need to process.",
                            type=str)

        parser.add_argument('-v', '--verbose',
                            help="If it specified, then the process of correcting words will be printed",
                            action='store_true')

        return parser

    def get_parameters(self):
        pass
