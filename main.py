import sys
from src.Grammar import *


def main():

    # filename handling stuff
    file_folder = './grammars/'  # folder is test_grammars
    filename = input('name of grammar file inside grammars (default = test.txt): ')
    if filename == '':
        filename = 'test.txt'

    grammar = Grammar()
    try:
        grammar.read_grammar_from_file(file_folder + filename)
    except FileNotFoundError:
        print('File ' + filename + ' could not be found inside grammars folder. Please check if name is correct.')
        sys.exit(1)

    print(grammar)

    # print('Grammar before minimization:')

    # grammar.minimize()
    # print('Grammar after minimization')
    # print(grammar)


if __name__ == '__main__':
    main()
