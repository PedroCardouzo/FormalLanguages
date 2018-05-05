from collections import namedtuple

# Rule = 2-uple (Char, String) | each char from String belongs to terminals or variables
Rule = namedtuple('Rule', ['head', 'tail'])


class Grammar:

    def __init__(self, empty_symbol='V'):
        self.terminals = []
        self.variables = []
        self.initial = None
        self.rules = []
        self.empty_symbol = empty_symbol  # 'V' is default for empty symbol

    def __str__(self):
        # will print formal grammar definition in this style:
        # G = ({S, A, B, C}, {a, b}, P, S)
        # P = {
        #     rules
        # }
        terminals_string = ', '.join(self.terminals) # ['X', 'Y', 'Z'] -> 'X, Y, Z'
        variables_string = ', '.join(self.variables) # ['a', 'b', 'c'] -> 'a, b, c'
        rules_string = self.__str_rules__()
        return 'G = ({' + variables_string + '}, {' + terminals_string + '}, P, ' + self.initial + ')\nP = {\n' + rules_string + '}'

    def __str_rules__(self):
        str_buffer = ''
        buffer = []
        for variable in self.variables:
            rules_for_variable = filter(lambda x: x.head == variable, self.rules)  # filter for only one variable
            rules_for_variable = map(lambda x: x.tail, rules_for_variable)  # extract only the rules

            rules_for_variable = [' '.join(single_rule) for single_rule in rules_for_variable]

            str_buffer += '\t' + variable + ' -> ' + ' | '.join(rules_for_variable) + '\n'  # return the formatted rule generation
        return str_buffer

    def read_grammar_from_file(self, filepath):
        buffer = []  # the 4 buffer slots
        buffer_pos = (a for a in range(0, 4))  # there are 4 elements that define a grammar
        with open(filepath, 'r') as file:
            for line in file:
                if line[0] == '#':
                    i = next(buffer_pos)
                    buffer.append([])  # new buffer slot
                else:
                    line = cleanLine(line, ']')
                    if line != '':
                        buffer[i].append(line)

        self.generate_terminals(buffer[0])
        self.generate_variables(buffer[1])
        self.generate_initial(buffer[2])
        self.generate_rules(buffer[3])

        self.sort_variables() # so we can print in a more organized way
        self.terminals.sort()

    def sort_variables(self):
        self.variables.remove(self.initial)
        self.variables.sort()
        self.variables = [self.initial] + self.variables

    def generate_terminals(self, buffer):
        for encoded_symbol in buffer:
            self.terminals.append(extractSymbol(encoded_symbol))

    def generate_variables(self, buffer):
        for encoded_symbol in buffer:
            self.variables.append(extractSymbol(encoded_symbol))

    def generate_initial(self, encoded_symbol):
        self.initial = extractSymbol(encoded_symbol[0])

    def generate_rules(self, buffer):
        for rule in buffer:
            head, tail = rule.split(' > ')

            tail = tail.split('] [')
            generated_symbols = [extractSymbol(x) for x in tail]

            new_rule = Rule(extractSymbol(head), generated_symbols)
            self.rules.append(new_rule)


def extractSymbol(encoded_symbol):
    return ''.join([c for c in encoded_symbol if c not in ' []']) # pick every char except if char is ' ' or '[' or ']'
    # join function is used to join the characters form the generated list to a single string (list of char -> String)


def cleanLine(string, stop_char):
    pos = len(string)-1
    cut_pos = 0
    stop_char_found = False

    while stop_char_found is False and pos >= 0:

        if string[pos] == stop_char:
            cut_pos = pos+1
            stop_char_found = True

        pos -= 1

    return string[:cut_pos]

# cleanLine('addpowadwapkdwadda$ fhsoiejfsoi fsofjsojf es', '$') -> addpowadwapkdwadda$
# cleanLine('#acawdowa', '$') -> ''


def main():
    filename = 'test.txt' #input()
    grammar = Grammar()
    grammar.read_grammar_from_file(filename)
    print(grammar)

if __name__ == '__main__':
    main()