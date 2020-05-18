import sys
from analyzer.lib.configurator import Configurator
from analyzer.lib.word_analyzer import WordAnalyzer


def main():
    configurator = Configurator(sys.argv[1:])
    analyzer = WordAnalyzer.build(configurator)
    analyzer.analyze()


if __name__ == '__main__':
    main()
