import sys
from src.Grammar import *
from src.ChomskyNormalForm import ChomskyNormalForm

def main():

    # filename handling stuff
    file_folder = './grammars/'  # folder is test_grammars
    filename = ''  # input('name of grammar file inside grammars (default = test.txt): ')
    if filename == '':
        filename = '4_d.txt'

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


if __name__ == '__main__':
    main()
