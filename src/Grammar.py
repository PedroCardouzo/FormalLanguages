from collections import namedtuple
from collections import deque # used for BFS in Grammar.remove_unit_productions
import sys # for command-line arguments

# Rule = 2-uple (String, (String,)) | each String belongs to terminals or variables
Rule = namedtuple('Rule', ['head', 'tail'])


class Grammar:

    def __init__(self, empty_symbol='V'):
        """
            # __init__ ::
            Initilizes variables
        """
        self.terminals = set()
        self.variables = set()
        self.initial = None
        self.rules = set()
        self.empty_symbol = empty_symbol  # 'V' is default for empty symbol

    def __str__(self):
        """
            # __str__ ::  --> 
            Uses self to access state
            


        """
        
        
        # will print formal grammar definition in this style:
        # G = ({S, A, B, C}, {a, b}, P, S)
        # P = {
        #     rules
        # }
        terminals = list(self.terminals)
        variables = list(self.variables)
        terminals.sort()
        variables.sort()
        # places the initial variable first
        variables = [self.initial] + [var for var in variables if var != self.initial]

        terminals_string = ', '.join(terminals)  # ['a', 'b', 'c'] -> 'a, b, c'
        variables_string = ', '.join(variables)  # ['X', 'Y', 'Z'] -> 'X, Y, Z'
        rules_string = self.__str_rules__(variables)
        return 'G = ({' + variables_string + '}, {' + terminals_string + '}, P, '\
               + self.initial + ')\nP = {\n' + rules_string + '}'

    def __str_rules__(self, variables):
        """
            # __str_rules__ ::  -->
            Used for rules printing in the screen in an easier way for future reading

        """
        str_buffer = ''
        for variable in variables:
            rules_for_variable = [x.tail for x in self.rules if x.head == variable]
            rules_for_variable = [' '.join(single_rule) for single_rule in rules_for_variable]

            if rules_for_variable != []:
                str_buffer += '\t' + variable + ' -> ' + ' | '.join(rules_for_variable) + '\n'

        # return the formatted rule generation
        return str_buffer

    def read_grammar_from_file(self, filepath):
        """
                # read_grammar_from_file :: String ->
                Receives the filepath with its folder and puts each part of the input text on its own slot of the
                buffer so that afterwards we generate variables, terminals and rules.
        """
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

    def sort_variables(self):  # sort but let initial variable @ position 1 in variables list
        """
                # Sort variables ::
                Sorts variables set so that when we print them they are ordenated
        """
        self.variables.remove(self.initial)
        self.variables.sort()
        self.variables = {self.initial} + self.variables

    def generate_terminals(self, buffer):
        """
                # generate_terminals ::  [chars] -->
                Reads information from buffer and puts them in self.terminals
        """
        for encoded_symbol in buffer:
            self.terminals.add(extract_symbol(encoded_symbol))

    def generate_variables(self, buffer):
        """
                # generate_variables ::  [chars] -->
                Reads information from buffer and puts them in self.variables
        """
        for encoded_symbol in buffer:
            self.variables.add(extract_symbol(encoded_symbol))

    def generate_initial(self, encoded_symbol):
        """
                # generate_initial ::  char -->
                Reads char from buffer and sets as initial variable
        """
        self.initial = extract_symbol(encoded_symbol[0])

    def generate_rules(self, buffer):
        """
                # generate_rules ::  [chars] -->
                Reads information from buffer and puts them in 'self.rules' as a tuple
        """
        for rule in buffer:
            head, tail = rule.split(' > ')

            tail = tail.split('] [')
            generated_symbols = tuple([extract_symbol(x) for x in tail])

            new_rule = Rule(extract_symbol(head), generated_symbols)
            self.rules.add(new_rule)

    def is_empty_rule(self, rule_tail):
        """
                # is_empty_rule ::  {chars} -->
                Checks if a rule tail is an empty symbol (pattern: V)
        """
        for symbol in rule_tail:
            if symbol != self.empty_symbol:
                return False

        return True

    def minimize(self):
        """
            Minimizes
        """
        # check if it would generate empty symbol then add it at the end

        self.remove_empty_productions()
        self.remove_unit_productions()
        self.remove_useless_symbols()

    def remove_empty_productions(self):
        """
                # remove_empty_productions ::
                Removes empty productions from 'self.rules'
        """
        variables_that_generate_empty = self.get_variables_that_gen_empty()

        add_empty_rule = self.initial in variables_that_generate_empty

        self.rules = {rule for rule in self.rules if not self.is_empty_rule(rule.tail)}

        # in each loop the rules will include more and more newly generated rules
        for variable in variables_that_generate_empty:
            self.rules = self._derivate_rules(variable)

        # add empty string if it belonged to the grammar before
        if add_empty_rule:
            self.rules.add(Rule(self.initial, tuple(self.empty_symbol)))

    def get_variables_that_gen_empty(self, variables_gen_empty=[]):
        """
                # get_variables_that_gen_empty ::
                Checks which variables can make an empty production. This function is used in remove_empty_productions
        """
        recursive_call = False

        if variables_gen_empty == []:
            variables_gen_empty = [rule.head for rule in self.rules if self.empty_symbol in rule.tail]

        buffer = []
        # dont check rules from variables that are already confirmed to generate empty string
        rules_to_check = [rule for rule in self.rules if rule.head not in variables_gen_empty]

        for (head, tail) in rules_to_check:
            # if every variable in tail is in variables_gen_empty, tail will generate empty
            if self._will_produce_empty(tail, variables_gen_empty):
                buffer.append(head)
                recursive_call = True

        if recursive_call:
            return self.get_variables_that_gen_empty(variables_gen_empty + buffer)
        else:
            return variables_gen_empty + buffer

    def _will_produce_empty(self, tail, variables_gen_emtpy):
        """
                # _will_produce_empty ::     --> Boolean
                Checks in a set of chars if any of the productions of 'tail' is an empty production.
                Used in get_variables_that_gen_empt
        """
        for symbol in tail:
            if symbol not in variables_gen_emtpy:
                return False

        # tail is not empty? True : False
        return tail != ()

    def _derivate_rules(self, variable, acc_rules=set(), new_rules=None):
        rules_buffer = set()

        # base case
        if new_rules is None:
            new_rules = self.rules.copy()

        for head, rule_tail in new_rules:
            index_to_remove = [i for i, symbol in enumerate(rule_tail) if symbol == variable]

            if index_to_remove == []:
                acc_rules.add(Rule(head, rule_tail))
                # the rule_tail can no longer be divided, therefore, just add it to the accumulator we will return later

            else:
                for i in index_to_remove:
                    rules_buffer.add(Rule(head, rule_tail[:i] + rule_tail[i + 1:]))

            acc_rules = acc_rules | new_rules

        if rules_buffer == set():  # buffer is empty?
            # return only the rules whose tail is not an empty tuple
            return {rule for rule in acc_rules if rule.tail != tuple()}
        else:
            return self._derivate_rules(variable, acc_rules, rules_buffer)

    def remove_useless_symbols(self):
        """
            # remove_useless_symbols ::
            Removes useless symbols in the grammar. Looks for variables that can't be achieved and erases them. Looks for
            terminals that can't be achieved and erases them. And then, removes rules that became useless.


        """
        # clear variables that don't achieve a terminal
        # have to send a copy otherwise the terminals themselves will be altered
        # obs.: empty symbol is also a terminal
        self.variables = self._achieve_terminals(self.terminals.copy() | {self.empty_symbol})

        # clear symbols that can't be achieved through the initial variable
        achievable_symbols = self._filter_achievable_symbols()

        self.variables = {x for x in achievable_symbols if x in self.variables}
        self.terminals = {x for x in achievable_symbols if x in self.terminals}

        # remove rules that became useless
        self.rules = {rule for rule in self.rules if rule.head in self.variables and self.is_valid_rule(rule)}

    # clear variables that don't achieve a terminal
    def _achieve_terminals(self, target_symbols):
        recursive_call = False
        for (generator_symbol, rule_tail) in self.rules:
            add = True
            for symbol in rule_tail:

                reaches_terminal = symbol in target_symbols
                is_new_symbol = generator_symbol not in target_symbols

                if not reaches_terminal or not is_new_symbol:
                    add = False
                    break  # if add is set as False we know that this rule will not be added so we can stop the loop

            if add:
                target_symbols.add(generator_symbol)
                recursive_call = True

        if recursive_call:
            return self._achieve_terminals(target_symbols)
        else:
            # empty symbol was added to the set, therefore we have to remove it
            target_symbols.remove(self.empty_symbol)
            return {x for x in target_symbols if x not in self.terminals}

            # up until now the terminals were in the target_symbols, but this function must return
            # variables only, therefore we must filter them out here

    def _filter_achievable_symbols(self, achieved_symbols=set(), new_achievable_symbols=None):
        """
            # _filter_achievable_symbols :: symbols --> [symbols]
            This function receives a symbol and return a set of all symbols that can be achieved by that symbol
            ex:


        """
        if new_achievable_symbols is None:  # the only symbol achievable by default is the initial
            new_achievable_symbols = {self.initial}

        recursive_call = False
        new_symbols_buffer = set()  # just a buffer for the soon to be new symbols

        # new_achievable_symbols is only separated so that we don't go over the symbols we have already gone through
        # however, they are already symbols that have been achieved so we can add them to achieved_symbols
        achieved_symbols = achieved_symbols | new_achievable_symbols
        for generator in new_achievable_symbols:
            rules_for_generator = [rule for rule in self.rules if rule.head == generator]
            for rule in rules_for_generator:
                if self.is_valid_rule(rule):
                    for symbol in rule.tail:
                        # new symbols arte separated into another variable for efficiency purposes
                        # we dont want to go over everyone we already tested, just the new added symbols
                        if symbol not in new_symbols_buffer and symbol not in achieved_symbols:
                            new_symbols_buffer.add(symbol)
                            recursive_call = True

        if recursive_call:  # loop only over the newly achieved symbols
            return self._filter_achievable_symbols(achieved_symbols, new_symbols_buffer)
        else:
            return achieved_symbols

    def is_valid_rule(self, rule):
        """
            # is_valid_rule :: head, [tail]-> boolean
            Checks if 'rule' is a valid rule.
            ex:


        """
        for symbol in rule.tail:
            if symbol not in self.variables and symbol not in self.terminals and symbol != self.empty_symbol:
                return False

        return True

    def remove_unit_productions(self):
        ''' 
        Remove rules of the form A->B, creating rules A->alpha
        if B->C is a unit rule  and C->alpha is a non-unit rule,
        for any variables A, B and C, and any string alpha of terminals
        or variables that isn't comprised of a single variable.
        '''
        # --------- begin is_unit_production ---------
        def is_unit_production(rule):
            if len(rule.tail) == 1 and rule.tail[0] in self.variables:
                    return True
            else:
                return False
        # --------- end is_unit_production ---------

        # --------- begin variable_unit_closure ---------
        def variable_unit_closure(v):
            def immediate_unit_closure(v):
                unit_productions_of_v = \
                    [rule for rule in self.rules if \
                     rule.head == v and is_unit_production(rule)]
                return set(var for var in \
                           [rule.tail[0] for rule in unit_productions_of_v])

            # set of variables which we are to return
            unit_closure_v = set() 

            visited = dict((var, False) for var in self.variables)
            queue = deque() # init queue
            queue.append(v)

            while queue:
                u = queue.popleft()
                # this is a graph BFS; we get u's adjacent nodes
                immediate_closure_u = immediate_unit_closure(u)
                for element in immediate_closure_u:
                    if not visited[element]:
                        unit_closure_v.update(element)
                        queue.append(element)
                visited[u] = True

            return unit_closure_v
        # --------- end variable_unit_closure ---------
        
        # Start off with all original non-unitary rules
        new_rules = {rule for rule in self.rules if not is_unit_production(rule)}

        # For every variable V and for every other variable U in V's unit-closure,
        # if U is the head of some non-unit production P,
        # create a new rule headed by V, but with the tail originally produced by U
        for v in self.variables:
            for u in variable_unit_closure(v):
                non_unit_rules_of_u = {rule for rule in self.rules if \
                                       rule.head == u and \
                                       not is_unit_production(rule)}
                new_rules = new_rules.union( {Rule(v, rule.tail) for rule in non_unit_rules_of_u} )
       
        # Finally assign the newly created set of rules 
        # to that of the grammar
        self.rules = new_rules

def extract_symbol(encoded_symbol):
    """
        # extract_symbol :: [char]-> String
        Receives a list of char and returns a string with the following chars removed: '[' and ']' and ' '.
        ex:
            extract_symbol(['[', 'H', ']']) --> H
            extract_symbol(['[', 'H', ']', ' ', '[', 'B', ']']) --> H
            extract_symbol('[][][][][][x][][][][]') --> x

    """
    return ''.join([c for c in encoded_symbol if c not in ' []'])  # pick every char except if char is ' ' or '[' or ']'
    # join function is used to join the characters form the generated list to a single string (list of char -> String)

def clean_line(string, stop_char):
    """
            # clean_line :: String char -> String
            Receives a String and a 'stop_char'.
            Scans the string backwards and cuts at the first 'stop_char', returning the new String
            ex:
                clean_line("this is a # string", '#')  --> "this is a "
                clean_line("[ X ] > [ V ]  # V eh a palavra vazia.", '#')  --> "[ X ] > [ V ]  "
                clean_line("[ X ] > [ V ]  # V eh a # palavra vazia.", '#')  --> "[ X ] > [ V ]  # V eh a "
    """
    pos = len(string) - 1
    cut_pos = 0
    stop_char_found = False

    while stop_char_found is False and pos >= 0:

        if string[pos] == stop_char:
            cut_pos = pos + 1
            stop_char_found = True

        pos -= 1

    return string[:cut_pos]

