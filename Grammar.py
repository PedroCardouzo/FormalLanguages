from collections import namedtuple

# Rule = 2-uple (String, [String]) | each char from String belongs to terminals or variables
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
        terminals_string = ', '.join(self.terminals)  # ['X', 'Y', 'Z'] -> 'X, Y, Z'
        variables_string = ', '.join(self.variables)  # ['a', 'b', 'c'] -> 'a, b, c'
        rules_string = self.__str_rules__()
        return 'G = ({' + terminals_string + '}, {' + variables_string + '}, P, ' + self.initial + ')\nP = {\n' + rules_string + '}'

    def __str_rules__(self):
        str_buffer = ''
        for variable in self.variables:
            rules_for_variable = filter(lambda x: x.head == variable, self.rules)  # filter for only one variable
            rules_for_variable = map(lambda x: x.tail, rules_for_variable)  # extract only the rules

            rules_for_variable = [' '.join(single_rule) for single_rule in rules_for_variable]

            str_buffer += '\t' + variable + ' -> ' + ' | '.join(
                rules_for_variable) + '\n'  # return the formatted rule generation
        return str_buffer

    def read_grammar_from_file(self, filepath):
        buffer = []  # buffer slots
        buffer_pos = (a for a in range(0, 4))  # there are 4 elements that define a grammar
        with open(filepath, 'r', encoding='UTF-8-sig') as file:  # this removes special UTF-8 encoding "ï»¿"
            for line in file:
                if line[0] == '#':
                    i = next(buffer_pos)
                    buffer.append([])  # new buffer slot
                else:
                    line = clean_line(line, ']')
                    if line != '':
                        buffer[i].append(line)

        self.generate_terminals(buffer[0])
        self.generate_variables(buffer[1])
        self.generate_initial(buffer[2])
        self.generate_rules(buffer[3])

        self.sort_grammar()

    def sort_grammar(self):
        self.sort_variables()  # so we can print in a more organized way
        self.terminals.sort()

    def sort_variables(self):  # sort but let initial variable @ position 1 in variables list
        self.variables.remove(self.initial)
        self.variables.sort()
        self.variables = [self.initial] + self.variables

    def generate_terminals(self, buffer):
        for encoded_symbol in buffer:
            self.terminals.append(extract_symbol(encoded_symbol))

    def generate_variables(self, buffer):
        for encoded_symbol in buffer:
            self.variables.append(extract_symbol(encoded_symbol))

    def generate_initial(self, encoded_symbol):
        self.initial = extract_symbol(encoded_symbol[0])

    def generate_rules(self, buffer):
        for rule in buffer:
            head, tail = rule.split(' > ')

            tail = tail.split('] [')
            generated_symbols = [extract_symbol(x) for x in tail]

            new_rule = Rule(extract_symbol(head), generated_symbols)
            self.rules.append(new_rule)

    def is_empty_rule(self, rule_tail):
        for symbol in rule_tail:
            if symbol != self.empty_symbol:
                return False

        return True

    def minimize(self):
        # check if it would generate empty symbol then add it at the end
        self.remove_empty_productions()
        # self.remove_ nome que nao sei ainda A -> B or A -> C or A -> A
        self.remove_useless_symbols()

    def remove_empty_productions(self):
        loop_again = True
        variables_that_generate_empty = self.get_variables_that_gen_empty()

        if self.initial in variables_that_generate_empty:
            add_empty_rule = True

        self.rules = [rule for rule in self.rules if not self.is_empty_rule(rule.tail)]
        new_rules = []
        while(loop_again):
            loop_again = False
            for variable in variables_that_generate_empty:
                for rule in self.rules:
                    new_tail = [symbol for symbol in rule.tail if symbol != variable]
                    # if combination must be made, self.generate_all_new_rules(rule, variable) -> returns multiple rules
                    # XaX -> [aX, Xa, a]

                    if new_tail != []:
                        new_rules.append(Rule(rule.head, new_tail))
                        loop_again = True

            self.rules = new_rules

        # add empty string if it belonged to the grammar before
        if add_empty_rule:
            self.rules.apend(Rule(self.initial, [self.empty_symbol]))

## checar se as regras sao removidas na etapa 2 1 por 1 (XaX -> aX e Xa -> aX, Xa, a


    def get_variables_that_gen_empty(self, variables_gen_empty=[]):
        recursive_call = False

        if variables_gen_empty == []:
            variables_gen_empty = [rule.head for rule in self.rules if self.empty_symbol in rule.tail]

        buffer = []
        # dont check rules from variables that are already confirmed to generate empty string
        rules_to_check = [rule for rule in self.rules if rule.head not in variables_gen_empty]

        for (head, tail) in rules_to_check:
            if len(tail) == 1 and tail[0] in variables_gen_empty:  # tail must contain only 1 variable
                buffer.append(head)
                recursive_call = True

        if recursive_call:
            return self.get_variables_that_gen_empty(variables_gen_empty + buffer)
        else:
            return variables_gen_empty + buffer

    def remove_useless_symbols(self):

        # clear variables that don't achieve a terminal
        # have to send a copy otherwise the terminals themselves will be altered
        self.variables = self._achieve_terminals(self.terminals.copy())

        # clear symbols that can't be achieved through the initial variable
        achievable_symbols = self._filter_achievable_symbols([])

        self.variables = [x for x in achievable_symbols if x in self.variables]
        self.terminals = [x for x in achievable_symbols if x in self.terminals]

        # remove rules that became useless
        self.rules = [rule for rule in self.rules if rule.head in self.variables and self.is_useful_rule(rule)]

    # clear variables that don't achieve a terminal
    def _achieve_terminals(self, target_symbols):
        recursive_call = False
        for (generator, rule) in self.rules:
            add = True
            for symbol in rule:
                if symbol not in target_symbols or generator in target_symbols:
                    add = False
                    break  # if add is set as False we know that this rule will not be added so we can stop the loop

            if add:
                target_symbols.append(generator)
                recursive_call = True

        if recursive_call:
            return self._achieve_terminals(target_symbols)
        else:
            return [x for x in target_symbols if x not in self.terminals]
            # up until now the terminals were in the target_symbols, but this function must return
            # variables only, therefore we must filter them out here

    def _filter_achievable_symbols(self, achieved_symbols, new_achievable_symbols=[]):

        if not new_achievable_symbols:  # the only symbol achievable by default is the initial
            new_achievable_symbols = [self.initial]

        recursive_call = False
        new_symbols_buffer = []  # just a buffer for the soon to be new symbols

        # new_achievable_symbols is only separated so that we don't go over the symbols we have already gone through
        # however, they are already symbols that have been achieved so we can add them to achieved_symbols
        achieved_symbols += new_achievable_symbols
        for generator in new_achievable_symbols:
            rules_for_generator = [rule.tail for rule in self.rules if rule.head == generator]
            for rule_tail in rules_for_generator:
                for symbol in rule_tail:
                    # new symbols are separated into another variable for efficiency purposes
                    if symbol not in new_symbols_buffer and symbol not in achieved_symbols:
                        new_symbols_buffer.append(symbol)
                        recursive_call = True

        if recursive_call:  # loop only over the newly achieved symbols
            return self._filter_achievable_symbols(achieved_symbols, new_symbols_buffer)
        else:
            return achieved_symbols

    def is_useful_rule(self, rule):

        for symbol in rule.tail:
            if symbol not in self.variables and symbol not in self.terminals:
                return False

        return True


def extract_symbol(encoded_symbol):
    return ''.join([c for c in encoded_symbol if c not in ' []'])  # pick every char except if char is ' ' or '[' or ']'
    # join function is used to join the characters form the generated list to a single string (list of char -> String)


def clean_line(string, stop_char):
    pos = len(string) - 1
    cut_pos = 0
    stop_char_found = False

    while stop_char_found is False and pos >= 0:

        if string[pos] == stop_char:
            cut_pos = pos + 1
            stop_char_found = True

        pos -= 1

    return string[:cut_pos]


# cleanLine('addpowadwapkdwadda$ fhsoiejfsoi fsofjsojf es', '$') -> addpowadwapkdwadda$
# cleanLine('#acawdowa', '$') -> ''


def main():
    filename = 'test.txt'  # input()
    grammar = Grammar()
    grammar.read_grammar_from_file(filename)
    grammar.minimize()
    print(grammar)


if __name__ == '__main__':
    main()
