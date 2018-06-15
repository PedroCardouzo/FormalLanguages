from src.Grammar import Grammar, Rule
from copy import deepcopy

CONST_VAR_NAMESPACE_SYMBOL = '&'
CONST_TERM_NAMESPACE_SYMBOL = ':'

class ChomskyNormalForm(Grammar):

    def __init__(self, grammar, log=False):

        # remove empty rule from grammar as CNF doesn't have it
        super().__init__()

        grammar = deepcopy(grammar)  # make sure we have a copy of grammar

        # check if empty_rule exists in grammar and removes it
        empty_rule = Rule(grammar.initial, tuple(grammar.empty_symbol))
        if empty_rule in grammar.rules:
            grammar.rules.remove(empty_rule)

        self.variables = grammar.variables
        self.terminals = grammar.terminals
        self.rules = grammar.rules
        self.initial = grammar.initial
        self._log = log

        # creates variable generator for when we will make new variables for achieving Chomsky Normal Form
        self._variable_generator = self._alpha_gen()

        self.minimize()  # make sure that the grammar is minimized
        self.generate_single_terminal()
        self.set_production_size_two()


    def __str__(self):
        return super().__str__()

    def _sort_variables_for_print(self):
        variables = list(self.variables)
        variables.remove(self.initial)
        variables.sort()

        # get the first character that is not marked with special namespace
        i = 0
        for v in variables:
            if v[0] != CONST_VAR_NAMESPACE_SYMBOL and v[0] != CONST_TERM_NAMESPACE_SYMBOL:
                break
            else:
                i += 1

        return [self.initial] + variables[i:] + variables[:i]

    @staticmethod
    # _alpha_gen :: 'int -> <generator object> | 'type means argument is optional
    # returns a generator that will produce $A -> $Z, then $A1 -> $Z1 until the number reaches max_num (default is 10
    # so it will produce $A -> $Z9)
    def _alpha_gen(max_num=10):
        j = 0
        while True:
            i = 'A'
            while i <= 'Z':
                if j == 0:
                    yield CONST_VAR_NAMESPACE_SYMBOL + i
                elif j < max_num:
                    yield CONST_VAR_NAMESPACE_SYMBOL + i + str(j)
                else:
                    raise StopIteration
                i = chr(ord(i) + 1)  # get next character of alphabet

            j += 1

    # _next_produced_variable :: void -> String
    # returns the next artificial variable produced by the generator
    def _next_produced_variable(self):
        return next(self._variable_generator)

    def generate_single_terminal(self):
        temp_map = dict((term, CONST_TERM_NAMESPACE_SYMBOL+term.upper()) for term in self.terminals)
        used_maps = set()

        for rule in self.rules.copy():
            if len(rule.tail) > 1:
                self.rules.remove(rule)
                self.rules.add(self._transform_rule(rule, temp_map, used_maps))

        # only adds new rules that we actually used
        for term, generator in temp_map.items():
            if generator in used_maps:
                self.rules.add(Rule(generator, tuple(term)))
                self.variables.add(generator)

    def _transform_rule(self, rule, mapping, used_maps):
        new_tail = tuple(x if x not in self.terminals else mapping[x] for x in rule.tail)
        buffer = []
        for x in rule.tail:
            if x in self.terminals:
                buffer.append(mapping[x])
                used_maps.add(mapping[x])
            else:
                buffer.append(x)
        return Rule(rule.head, new_tail)

    def set_production_size_two(self):
        rules_too_big = [rule for rule in self.rules if len(rule.tail) > 2]
        for rule in rules_too_big:
            self._break_rule(rule)

    # _break_rule :: Rule 'int -> void
    # breaks a rule up adding the new produced rules until rule has size 2 (for Chomsky NF, could be generified
    # to transform to an arbitrary size creating another argument and changing the 2 in if len(rule.tail) > 2 to
    # the new variable)
    def _break_rule(self, rule):
        if len(rule.tail) > 2:
            if rule in self.rules:
                self.rules.remove(rule)
            var = self._next_produced_variable()
            self.variables.add(var)
            r1 = Rule(rule.head, tuple([rule.tail[0], var]))
            r2 = Rule(var, rule.tail[1:])

            self.rules.add(r1)
            self._break_rule(r2)
        else:
            self.rules.add(rule)
