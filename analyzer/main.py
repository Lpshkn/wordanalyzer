import sys
from analyzer.arguments_parser import arguments_parser
from analyzer.load_data import load_words
from analyzer.word_analyzer import WordAnalyzer


def main():
    args = arguments_parser().parse_args(sys.argv[1:])
    words = load_words(args.source, args.count, args.encoding)
    frequency_words = load_words(args.frequency)

    word_analyzer = WordAnalyzer(frequency_words, args.tree, number_similar_words=args.similar_words,
                                 distance=args.distance, threshold=args.threshold,
                                 number_of_corrected_words=args.number_corrected)

    if args.verbose:
        with open(args.destination, 'w') as file:
            print("Correcting words is beginning...")
            for word in words:
                new_words = word_analyzer.get_correct_words(word)
                print('ORIGINAL: ', word, ' CORRECTED: ', new_words)
                if new_words:
                    file.writelines('\n'.join(new_words))
                    file.write('\n')
        print("New corrected words were saved successfully")

    else:
        with open(args.destination, 'w') as file:
            print("Correcting words is beginning...")
            for word in words:
                new_words = word_analyzer.get_correct_words(word)
                if new_words:
                    file.writelines('\n'.join(new_words))
                    file.write('\n')
        print("New corrected words were saved successfully")


if __name__ == '__main__':
    main()
