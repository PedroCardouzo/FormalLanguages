import sys
from src.Grammar import *
from src.ChomskyNormalForm import ChomskyNormalForm
from src.CYKTable import *

def get_grammar_filename():
    file_folder = './grammars/'  
    if len(sys.argv) >= 2:
        file_folder = ''
        filename = sys.argv[1]

    else:
        filename = input('Enter the name of a grammar from within the ./grammars/ directory: ')
    if filename == '':
        print('No filename given, assuming t.txt')
        filename = 't.txt'

    return file_folder + filename

def get_input_word_from_command_line():
    if len(sys.argv) == 3:
        return sys.argv[2]
    elif len(sys.argv) > 3:
        print('\nSentences (i.e., words with spaces in them) should be entered between "quote marks". \nIgnoring command-line input.')
        return ''





def main():

    grammar = Grammar(log=True)  # True is sent to 'log' as we want to log each step of minimization
    try:
        grammar.read_grammar_from_file(get_grammar_filename())
    except FileNotFoundError:
        print('File ' + filename + ' could not be found inside grammars folder. Please check if name is correct.')
        sys.exit(1)

    cyk_parser = Parser(grammar, log_grammar_preparation=True)

    command_line_word = get_input_word_from_command_line()
    if command_line_word:
        cyk_parser.parse(command_line_word)

    else:
        word = ' '
        while word:
            word = input('Enter an input word or sentence (or just press Enter to exit): ')
            if word:
                cyk_parser.parse(word)
            else:
                print('No word entered this time.')

    print('\nSEE YOU SPACE COWBOY...\n')

    #for c in tree.children:
     #   print('*'*30)
      #  print(c[0].__str__() + '\n' + c[1].__str__())
       # print('*'*30)



if __name__ == '__main__':
    main()
