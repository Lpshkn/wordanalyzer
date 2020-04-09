import sys
from analyzer.arguments_parser import arguments_parser


def main():
    args = arguments_parser().parse_args(sys.argv[1:])


if __name__ == '__main__':
    main()
