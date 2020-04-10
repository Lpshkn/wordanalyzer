import sys
from arguments_parser import arguments_parser
from load_data import load_words


def main():
    args = arguments_parser().parse_args(sys.argv[1:])
    words = load_words(args.source, args.count, args.encoding)
    frequency_words = load_words(args.frequency)


if __name__ == '__main__':
    main()
