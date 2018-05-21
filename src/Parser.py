import src.Grammar

#from pprint import pprint

class CYK:
    
    def __init__(self, grammar):
        self.grammar = grammar
        self.table = None
        #self.grammar.convert_cnf()

    def create_table(self, size):
        self.table = dict()
        for r in range(size):
            for s in range(size - r):
                self.table[(r, s)] = set()

    def print_cell_label(self, r, s):
        print('V'+'('+'r='+ str(r) +','+'s='+ str(s)+')')

    def print_table(self, word_length):
        for s in reversed(range(word_length)):
            row = [self.table[(r, s)] for r in range(word_length - s)]
            print('Row', s,':',row)

    
    def parse(self, word):
        # If word has spaces within it, we consider it to be a "sentence".
        # As such, we separate the sentence into a list of terminal "words"
        if ' ' in word:
            word = word.split(' ')
            word_or_sentence = 'sentence'
        else:
            word_or_sentence = 'word'

        print('\nParsing',word_or_sentence,':', word)

        self.create_table(len(word))

        # The algorithm works inductively on the table's len(word) rows
        # The table is a dict from pairs of integers to sets of variables
        # s is a row index in the table, starting at 0
        # r is a column index in the table, starting at 0
        # As such, any cell in the table may be addressed as self.table[(r, s)]

        # ------------ basis (s = 0) ------------
        for r in range(len(word)):
            self.table[(r, 0)] = { rule.head for rule in \
                                  self.grammar.rules if \
                                  len(rule.tail) == 1 and \
                                  word[r] in self.grammar.terminals and \
                                  word[r] in rule.tail }


        # ------------ induction (s > 0) ------------
        for s in range(1, len(word)):
            for r in range(len(word) - s):
                for k in range(s):
                    possible_Bs = { symbol for symbol in self.table[(r,k)] }
                    possible_Cs = { symbol for symbol in self.table[(r+k+1, s-k-1)] }

                    possible_tails = {(B, C) for B in possible_Bs for C in possible_Cs}

                    self.table[(r, s)].update( {rule.head for rule in self.grammar.rules \
                                                for tail in possible_tails if \
                                                rule.tail == tail} )
                    

        print('Table size:', len(self.table))
        print('Table state after parse:')
        self.print_table(len(word))

        if self.grammar.initial in self.table[(0, len(word)-1)]:
            print('Grammar generates',word_or_sentence,word)
            return True
        else:
            print('Grammar doesn\'t generate',word_or_sentence,word)
            return False

