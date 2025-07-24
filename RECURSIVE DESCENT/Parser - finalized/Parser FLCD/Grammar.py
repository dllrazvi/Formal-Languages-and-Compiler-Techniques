class Grammar:
    def __init__(self):
        self.non_terminal_symbols = []
        self.terminal_symbols = []
        self.production_rules = {}
        self.starting_symbol = None

    def get_terminals(self):
        """
        :return: List of terminal symbols.
        """
        return self.terminal_symbols

    def get_non_terminals(self):
        """
        :return: List of non-terminal symbols.
        """
        return self.non_terminal_symbols

    def get_start_symbol(self):
        """
        :return: The starting symbol.
        """
        return self.starting_symbol

    def get_productions_for(self, non_terminal):
        """
        :param non_terminal: Non-terminal symbol to get productions for.
        :return: List of production rules for the given non-terminal.
        """
        return self.production_rules.get(non_terminal, [])

    def has_more_productions(self, non_terminal, production_index):
        """
        Checks if there is an additional production rule for a given non-terminal symbol.
        :param non_terminal: Non-terminal symbol to check.
        :param production_index: Current production index.
        :return: True if there is another production, False otherwise.
        """
        return self.production_rules[non_terminal][-1][1] != production_index

    def get_specific_production(self, non_terminal, production_index):
        """
        :param non_terminal: Non-terminal symbol to get the production for.
        :param production_index: The production index to retrieve.
        :return: Specific production rule if found, None otherwise.
        """
        for production in self.production_rules[non_terminal]:
            if production[1] == production_index:
                return production

    def load_grammar_from_file(self, file_path):
        """
        :param file_path: Path to the file containing the grammar.
        :raises ValueError: If the grammar is not a valid context-free grammar.
        """
        with open(file_path, 'r') as file:
            self.non_terminal_symbols = self._parse_symbols(file.readline())
            self.terminal_symbols = self._parse_symbols(file.readline())
            self.starting_symbol = file.readline().split('=')[1].strip()
            file.readline()
            raw_rules = [line.strip() for line in file]
            self.production_rules = self._interpret_production_rules(raw_rules)

            if not self._validate_cfg(raw_rules):
                raise ValueError('The provided grammar is not a valid CFG')

    def display_non_terminals(self):
        """
        :return: String of non-terminal symbols.
        """
        return str(self.non_terminal_symbols)

    def display_terminals(self):
        """
        :return: String of terminal symbols.
        """
        return str(self.terminal_symbols)

    def display_start_symbol(self):
        """
        :return: String of the starting symbol.
        """
        return str(self.starting_symbol)

    def display_productions(self):
        """
        :return: String of production rules.
        """
        return str(self.production_rules)

    @staticmethod
    def _parse_symbols(line):
        """
        :param line: Line from the grammar file.
        :return: List of symbols extracted from the line.
        """
        parts = line.strip().split('=', 1)[1]
        if parts.strip()[-1] == ',':
            parts = [',']
        return [item.strip() for item in parts.split(',')]

    @staticmethod
    def _interpret_production_rules(rule_lines):
        """
        :param rule_lines: Lines from the grammar file representing the rules.
        :return: Dictionary of interpreted production rules.
        """
        productions = {}
        production_counter = 1

        for rule in rule_lines:
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            rhs = [value.strip() for value in rhs.split('|')]

            for production in rhs:
                if lhs in productions:
                    productions[lhs].append((production, production_counter))
                else:
                    productions[lhs] = [(production, production_counter)]
                production_counter += 1
        return productions

    @staticmethod
    def _validate_cfg(rules):
        """
        Checks if the parsed grammar is a valid context-free grammar (CFG).
        Ensures that each production rule adheres to the format required for CFGs.
        :param rules: List of rules to be checked.
        :return: True if valid CFG, False otherwise.
        """
        for rule in rules:
            left_hand_side, _ = rule.split('->')
            left_hand_side = left_hand_side.strip()
            if sum(symbol.strip() in left_hand_side for symbol in left_hand_side.split('|')) > 1:
                return False
        return True

