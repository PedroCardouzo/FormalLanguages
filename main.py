import sys
from src.Grammar import *
import src.Parser

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
    '''
    print('Grammar before minimization:')
    print(grammar)

    grammar.minimize()
    print('Grammar after minimization')
    print(grammar)
    '''

    print(grammar)
    cyk_parser = src.Parser.CYK(grammar)

    # word for Hopcroft example grammar
    #cyk_parser.parse('baaba')

    # word for Blauth example grammar
    #cyk_parser.parse('abaab')

    # word for Wikipedia example grammar
    cyk_parser.parse('she eats a fish with a fork')

if __name__ == '__main__':
    main()
