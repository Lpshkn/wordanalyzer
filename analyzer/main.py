import sys
from analyzer.configurator import Configurator
from analyzer.word_analyzer import WordAnalyzer


def main():
    configurator = Configurator(sys.argv[1:])
    analyzer = WordAnalyzer.build(configurator)
    analyzer.analyze()


if __name__ == '__main__':
    main()
