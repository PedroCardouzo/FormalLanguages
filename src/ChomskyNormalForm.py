from src.Grammar import Grammar, Rule
from copy import deepcopy

class ChomskyNormalForm(Grammar):

    def __str__(self):
        return super().__str__()

    def __init__(self, grammar):

        # remove empty rule from grammar as CNF doesn't have it
        super().__init__()

        grammar = deepcopy(grammar)  # make sure we have a copy of grammar

        empty_rule = Rule(grammar.initial, tuple(grammar.empty_symbol))
        if empty_rule in grammar.rules:
            grammar.rules.remove(empty_rule)

        self.variables = grammar.variables
        self.terminals = grammar.terminals
        self.rules = grammar.rules
        self.initial = grammar.initial
        self.empty_symbol = None

        self.generate_single_terminal()
        self.set_production_size_two()

    def generate_single_terminal(self):
        temp_map = dict((term, '_'+term.upper()+'_') for term in self.terminals)

        for rule in self.rules.copy():
            self.rules.remove(rule)
            self.rules.add(self._transform_rule(rule, temp_map))

        for term, generator in temp_map.items():
            self.rules.add(Rule(generator, tuple(term)))
            self.variables.add(generator)

    def _transform_rule(self, rule, mapping):
        new_tail = tuple(x if x not in self.terminals else mapping[x] for x in rule.tail)
        return Rule(rule.head, new_tail)

    def set_production_size_two(self):
        pass
