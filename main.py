import sys
from src.Grammar import *
from src.ChomskyNormalForm import ChomskyNormalForm

def main():

    # filename handling stuff
    file_folder = './grammars/'  # folder is test_grammars
    filename = ''  # input('name of grammar file inside grammars (default = test.txt): ')
    if filename == '':
        filename = '4_d.txt'

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

    print('Grammar in Chomsky Normal Form')
    cnf = ChomskyNormalForm(grammar)
    print(cnf)


if __name__ == '__main__':
    main()
