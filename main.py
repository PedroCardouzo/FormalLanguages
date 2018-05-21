import sys
from src.Grammar import *
from src.ChomskyNormalForm import ChomskyNormalForm
from src.Parser import CYK

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

    grammar = Grammar(log=True)  # True is sent to 'log' as we want to log each step of minimization

    try:
        grammar.read_grammar_from_file(file_folder + filename)
    except FileNotFoundError:
        print('File ' + filename + ' could not be found inside grammars folder. Please check if name is correct.')
        sys.exit(1)

    grammar.minimize()

    print('Grammar in Chomsky Normal Form')
    # False is sent to 'log' parameter as we won't be logging CNF minimization
    cnf = ChomskyNormalForm(grammar, log=False)
    print(cnf)

    cyk_parser = CYK(cnf)

    # word for Hopcroft example grammar
    #cyk_parser.parse('baaba')

    # word for Blauth example grammar
    #cyk_parser.parse('abaab')
    # word for Wikipedia example grammar
    #cyk_parser.parse('she eats a fish with a fork')

    # word for regular expression grammar
    #cyk_parser.parse('(x+x)*')
    cyk_parser.parse('a')

if __name__ == '__main__':
    main()
