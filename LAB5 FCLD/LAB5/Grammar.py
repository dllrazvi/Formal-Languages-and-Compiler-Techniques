class Grammar:
    def __init__(self, N, E, P, S):
        """
        :param N: set of nonterminals
        :param E: set of terminals
        :param P: productions (dictionary where key is a nonterminal, value is a list of productions)
        :param S: start symbol
        """
        self.N = N  # Non-terminals
        self.E = E  # Terminals
        self.P = P  # Productions
        self.S = S  # Start symbol
        self.tokens = []  # Tokens to parse
        self.index = 0  # Current position in the tokens

    @staticmethod
    def validate(N, E, P, S):
        """
        Validates whether the given grammar is context-free.
        """
        if S not in N:
            return False
        for lhs, rhs_list in P.items():
            if lhs not in N:
                return False
            for rhs in rhs_list:
                for symbol in rhs[0].split():
                    if symbol not in N and symbol not in E and symbol != 'E':
                        return False
        return True

    @staticmethod
    def parseLine(line):
        return [value.strip() for value in line.strip().split('=')[1].strip()[1:-1].split(',')]

    @staticmethod
    def parseRules(rules):
        result = {}
        index = 1
        for rule in rules:
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            rhs = [value.strip() for value in rhs.split('|')]

            for value in rhs:
                if lhs in result:
                    result[lhs].append((value, index))
                else:
                    result[lhs] = [(value, index)]
                index += 1

        return result

    @staticmethod
    def fromFile(fileName):
        with open(fileName, 'r') as file:
            N = Grammar.parseLine(file.readline())
            E = Grammar.parseLine(file.readline())
            S = file.readline().split('=')[1].strip()
            P = Grammar.parseRules(Grammar.parseLine(''.join([line for line in file])))

            if not Grammar.validate(N, E, P, S):
                raise Exception("Invalid CFG in input file.")

            return Grammar(N, E, P, S)

    def isNonTerminal(self, value):
        return value in self.N

    def isTerminal(self, value):
        return value in self.E

    def getProductionsFor(self, nonTerminal):
        if not self.isNonTerminal(nonTerminal):
            raise Exception(f"Cannot show productions for '{nonTerminal}': not a non-terminal.")
        return self.P.get(nonTerminal, [])

    def getProductionForIndex(self, index):
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                if rhs[1] == index:
                    return lhs, rhs[0]
        return None

    def checkCFG(self):
        return Grammar.validate(self.N, self.E, self.P, self.S)

    def parse(self, tokens):
        """
        Parses a sequence of tokens using recursive descent.
        :param tokens: List of tokens to parse.
        :return: True if the input matches the grammar; otherwise False.
        """
        self.tokens = tokens
        self.index = 0
        if self._parse_non_terminal(self.S) and self.index == len(self.tokens):
            print("Input string is valid.")
            return True
        else:
            print("Input string is invalid.")
            return False

    def _parse_non_terminal(self, non_terminal):
        """
        Recursive descent for a non-terminal.
        """
        if non_terminal not in self.P:
            raise Exception(f"No rules defined for non-terminal '{non_terminal}'")

        for production in self.P[non_terminal]:
            start_index = self.index  # Save the state for backtracking
            success = True
            for symbol in production[0].split():
                if self.isNonTerminal(symbol):
                    if not self._parse_non_terminal(symbol):
                        success = False
                        break
                elif self.isTerminal(symbol):
                    if not self._match(symbol):
                        success = False
                        break
                else:
                    raise Exception(f"Unexpected symbol '{symbol}' in production.")
            if success:
                return True
            self.index = start_index  # Backtrack
        return False

    def _match(self, terminal):
        """
        Matches a terminal against the current token.
        """
        if self.index < len(self.tokens) and self.tokens[self.index] == terminal:
            self.index += 1
            return True
        return False

    def __str__(self):
        productions = []
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                productions.append(f"{lhs} -> {rhs[0]} [{rhs[1]}]")

        return (
            f"N = {{ {', '.join(self.N)} }}\n"
            f"E = {{ {', '.join(self.E)} }}\n"
            f"P = {{ {' | '.join(productions)} }}\n"
            f"S = {self.S}\n"
        )
