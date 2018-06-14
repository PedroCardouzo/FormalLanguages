import sys
from src.Grammar import *
from src.ChomskyNormalForm import ChomskyNormalForm
from src.CYKTable import *

def main():

    # filename handling stuff
    file_folder = './grammars/'  # folder is test_grammars
    filename = ''  # input('name of grammar file inside grammars (default = test.txt): ')
    if filename == '':
        filename = 't.txt'

    grammar = Grammar(log=False)  # True is sent to 'log' as we want to log each step of minimization
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
    print('CYK DUDE')
    cyk_parser = Parser(cnf, False)
    cyk_parser.parse('abaab')
    cyk_parser.cyk_table.print_table()

    cyk_parser.cyk_table.extract_all_parse_trees(pretty_print=True)

    #for c in tree.children:
     #   print('*'*30)
      #  print(c[0].__str__() + '\n' + c[1].__str__())
       # print('*'*30)



if __name__ == '__main__':
    main()
