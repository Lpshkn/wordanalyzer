import sys
from analyzer.arguments_parser import arguments_parser
from analyzer.load_data import load_words
from analyzer.word_analyzer import WordAnalyzer


def main():
    parser = arguments_parser()
    args = parser.parse_args(sys.argv[1:])
    if not (args.source or args.words):
        parser.error('No action requested, add -s/--source or -w/--words')
    if not args.frequency:
        parser.error('To process the words, you must specify a file containing a list of frequency words')

    if args.words:
        words = args.words
    else:
        words = load_words(args.source, args.count, args.encoding)
    frequency_words = load_words(args.frequency)

    word_analyzer = WordAnalyzer(frequency_words, args.tree, number_similar_words=args.similar_words,
                                 distance=args.distance, threshold=args.threshold,
                                 number_of_corrected_words=args.number_corrected)

    if args.clear_word:
        print("Clearing words is beginning...")
        for word in words:
            new_word = word_analyzer.get_clear_word(word)
            print('ORIGINAL: ', word, ' CLEARED: ', new_word)

    elif args.total_cost:
        print("Counting total cost is beginning...")
        for word in words:
            total_cost = word_analyzer.get_total_cost(word)
            print('WORD: ', word, ' TOTAL COST: ', total_cost)

    else:
        with open(args.destination, 'w') as file:
            print("Correcting words is beginning...")
            for word in words:
                new_words = word_analyzer.get_correct_words(word)
                if args.verbose:
                    print('ORIGINAL: ', word, ' CORRECTED: ', new_words)
                if new_words:
                    file.writelines('\n'.join(new_words))
                    file.write('\n')

        # Remove duplicates and make all words lower
        with open(args.destination, 'r+') as file:
            words = set(word.lower() for word in file.readlines())
            file.truncate(0)
            file.writelines(words)

        print("New corrected words were saved successfully")


if __name__ == '__main__':
    main()
