import sys
from src.Grammar import *

def main():

    if len(sys.argv) == 2:
        # If shell input is used,
        # it is assumed that the folder is 
        # included in input.
        file_folder = ''
        filename = sys.argv[1]

    else: 
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

    print('Grammar before minimization:')
    print(grammar)

    grammar.minimize()
    print('Grammar after minimization')
    print(grammar)

if __name__ == '__main__':
    main()
