import src.Grammar
from src.ChomskyNormalForm import ChomskyNormalForm
from copy import deepcopy

#from pprint import pprint

class CYKTable:
    def __init__(self, grammar, word):
        self.word = word
        self.grammar = self.prepare_grammar(grammar)
        self.table = None
        accepts = self.build_table()

    def prepare_grammar(self, grammar):
        '''
            Returns a version of the grammar parameter that is
            first minimized, and then converted to Chomsky normal form.
        '''
        minimized_grammar = deepcopy(grammar)
        minimized_grammar.minimize()
        cnf_grammar = ChomskyNormalForm(minimized_grammar, log=False)
        return cnf_grammar

    def init_table(self):
        self.table = dict()
        for r in range(len(self.word)):
            for s in range(len(self.word) - r):
                self.table[(r, s)] = set()
    
    def print_cell_label(self, r, s):
        print('V'+'('+'r='+ str(r) +','+'s='+ str(s)+')')

    def print_table(self):
        for s in reversed(range(len(self.word))):
            row = [self.table[(r, s)] for r in range(len(self.word)- s)]
            print('Row', s,':',row)

    def build_table(self):
        # If word has spaces within it, we consider it to be a "sentence".
        # As such, we separate the sentence into a list of terminal "words"
        if ' ' in self.word:
            self.word = self.word.split(' ')
            word_or_sentence = 'sentence'
        else:
            word_or_sentence = 'word'

        print('\nParsing',word_or_sentence,':', self.word)

        self.init_table()

        # The algorithm works inductively on the table's len(self.word) rows
        # The table is a dict from pairs of integers to sets of variables
        # s is a row index in the table, starting at 0
        # r is a column index in the table, starting at 0
        # As such, any cell in the table may be addressed as self.table[(r, s)]

        # ------------ basis (s = 0) ------------
        for r in range(len(self.word)):
            self.table[(r, 0)] = { rule.head for rule in \
                                  self.grammar.rules if \
                                  len(rule.tail) == 1 and \
                                  self.word[r] in self.grammar.terminals and \
                                  self.word[r] in rule.tail }


        # ------------ induction (s > 0) ------------
        for s in range(1, len(self.word)):
            for r in range(len(self.word) - s):
                for k in range(s):
                    possible_Bs = { symbol for symbol in \
                                    self.table[(r,k)] }
                    possible_Cs = { symbol for symbol in \
                                    self.table[(r+k+1, s-k-1)] }

                    possible_tails = {(B, C) for B in possible_Bs for \
                                      C in possible_Cs}

                    self.table[(r, s)].update( {rule.head for rule in \
                                                self.grammar.rules \
                                                for tail in possible_tails if \
                                                rule.tail == tail} )
                    

        print('Expected table size:', len(self.word) * (len(self.word)+1) / 2)
        print('Actual table size:', len(self.table))
        print('Table state after parse:')
        self.print_table()

        if self.grammar.initial in self.table[(0, len(self.word)-1)]:
            print('Grammar generates',word_or_sentence,self.word)
            return True
        else:
            print('Grammar doesn\'t generate',word_or_sentence,self.word)
            return False

class Parser:
    
    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, word):
        cyk_table = CYKTable(self.grammar, word)


    

