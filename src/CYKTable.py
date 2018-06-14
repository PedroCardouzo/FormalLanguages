import src.Grammar
from src.ChomskyNormalForm import ChomskyNormalForm
from copy import deepcopy


class CYKTable:
    def __init__(self, grammar, word):
        self.word = word
        self.grammar = grammar
        self.table = None
        self.accepts = self.build_table()

    def init_table(self):
        self.table = dict()
        for r in range(len(self.word)):
            for s in range(len(self.word) - r):
                self.table[(r, s)] = set()

    def print_table(self):
        rows = []
        for s in reversed(range(len(self.word))):
            rows.append([self.table[(r, s)] for r in range(len(self.word) - s)])
            # print('Row', s,':',row)

        for row in rows:
            print(row)

    def build_table(self):
        # If word has spaces within it, we consider it to be a "sentence".
        # As such, we separate the sentence into a list of terminal "words"
        if ' ' in self.word:
            self.word = self.word.split(' ')
            word_or_sentence = 'sentence'
        else:
            word_or_sentence = 'word'

        print('\nParsing', word_or_sentence, ':', self.word)

        self.init_table()

        # The algorithm works inductively on the table's len(self.word) rows
        # The table is a dict from pairs of integers to sets of variables
        # s is a row index in the table, starting at 0
        # r is a column index in the table, starting at 0
        # As such, any cell in the table may be addressed as self.table[(r, s)]

        # ------------ basis (s = 0) ------------
        for r in range(len(self.word)):
            self.table[(r, 0)] = {rule.head for rule in \
                                  self.grammar.rules if \
                                  len(rule.tail) == 1 and \
                                  self.word[r] in self.grammar.terminals and \
                                  self.word[r] in rule.tail}

        # ------------ induction (s > 0) ------------
        for s in range(1, len(self.word)):
            for r in range(len(self.word) - s):
                for k in range(s):
                    possible_Bs = {symbol for symbol in \
                                   self.table[(r, k)]}
                    possible_Cs = {symbol for symbol in \
                                   self.table[(r + k + 1, s - k - 1)]}

                    possible_tails = {(B, C) for B in possible_Bs for \
                                      C in possible_Cs}

                    self.table[(r, s)].update({rule.head for rule in \
                                               self.grammar.rules \
                                               for tail in possible_tails if \
                                               rule.tail == tail})

        print('Expected table size:', len(self.word) * (len(self.word) + 1) / 2)
        print('Actual table size:', len(self.table))
        print('Table state after parse:')
        self.print_table()

        if self.grammar.initial in self.table[(0, len(self.word) - 1)]:
            print('Grammar generates', word_or_sentence, self.word)
            return True
        else:
            print('Grammar doesn\'t generate', word_or_sentence, self.word)
            return False

    def gen_iterator(self, c, l):
        for i in range(0, l):
            yield ((c, i), (c+i+1, l-i-1))
        raise StopIteration

    def gen_tree(self, var, pos):
        if pos[1] == 0:
            return Node(var, Node(self.word[pos[0]]))
        else:
            var = Node(var)
            rules_tails = set(rule.tail for rule in self.grammar.rules if rule.head == var.value)
            for a, b in self.gen_iterator(pos[0], pos[1]):
                combs = self.combinations(self.table[a], self.table[b])
                for comb in combs:
                    if comb in rules_tails:
                        var.add(
                            self.gen_tree(comb[0], a),
                            self.gen_tree(comb[1], b)
                        )
            return var

    @staticmethod
    def combinations(iter1, iter2):
        acc = []
        for i in iter1:
            for j in iter2:
                acc.append((i, j))
        return acc

    # extract_all :: TreeNode -> [String]
    # if is a leaf, returns a list containing only the node value of the leaf.
    # else appends itself in front of every element in the list returned by calling this function recursively on its children
    @classmethod
    def extract_all(cls, node):
        acc = []
        for child in node.children:
            if type(child) is tuple:
                aux1 = cls.extract_all(child[0])
                aux2 = cls.extract_all(child[1])
                acc += [node.value + ' -> ' + str(x) for x in cls.combinations(aux1, aux2)]
            else:
                acc.append(node.value + ' -> ' + child.value)
        return acc

    def extract_all_parse_trees(self, pretty_print=False):
        tree = self.gen_tree('S', (0, len(self.word)-1))
        data = self.extract_all(tree)

        if pretty_print:
            print(data)  # do something better
        return data

class Node:
    def __init__(self, value, terminal=None):
        self.value = value  # str
        self.children = []  # [(Node, Node)] | [Node] if Node.value is terminal
        if terminal is not None:
            # if terminal in self.grammar.terminals: provide some way to check terminals
            self.children.append(terminal)

    def __str__(self, deepness=0):
        s = deepness*'\t' + self.value + '\n'
        for c in self.children:
            if type(c) is tuple:
                s += c[0].__str__(deepness+1) + '\n' + c[1].__str__(deepness+1) + '\n'
            else:
                s += (deepness+1)*'\t' + c.value
        return s
        #if self.children != []:
        #    return 'value = ' + str(self.value) + '\nchildren = ' + str([c[0].__str__() + '\n' + c[1].__str__() for c in self.children])
        #else:
        #    return 'value = ' + str(self.value)

    def add(self, var1, var2):
        self.children.append((var1, var2))

    def get_value(self):
        return self.value


class Parser:
    def __init__(self, grammar, log_grammar_preparation=False):
        self.grammar = grammar
        self.prepare_grammar_for_cyk(log_grammar_preparation)
        self.cyk_table = None

    def parse(self, word):
        self.cyk_table = CYKTable(self.grammar, word)

        return self.cyk_table.accepts

    def prepare_grammar_for_cyk(self, log):
        '''
        Converts grammar to Chomsky normal form.
        '''
        # grammar_copy = deepcopy(self.grammar)
        # cnf_grammar = ChomskyNormalForm(grammar_copy, log)
        # print('Grammar in Chomsky normal form')
        # print(cnf_grammar)
        #
        # self.grammar = cnf_grammar
