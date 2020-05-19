import sys
from analyzer.lib.configurator import Configurator
from analyzer.lib.word_analyzer import WordAnalyzer
from datetime import datetime


def main():
    configurator = Configurator(sys.argv[1:])
    analyzer = WordAnalyzer.build(configurator)
    time = datetime.now()
    analyzer.analyze()
    print("Working time: ", datetime.now() - time)


if __name__ == '__main__':
    main()
