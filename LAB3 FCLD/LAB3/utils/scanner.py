import re
from LAB3.utils.symbol_table import SymbolTable
from LAB3.utils.finite_automata import FiniteAutomaton

class Scanner:
    def __init__(self, token_file):
        self.token_file = token_file
        self.token_list = self.load_tokens(token_file)
        self.pif = []
        self.errors = []
        self.symbol_table = SymbolTable(size=250)
        self.index_counter = 0
        self.unique_values = {}

        self.identifier_fa = FiniteAutomaton()
        self.identifier_fa.parse_fa_file("Input_Output/identifier_fa.txt")

        self.constant_fa = FiniteAutomaton()
        self.constant_fa.parse_fa_file("Input_Output/constant_fa.txt")

    def load_tokens(self, token_file):
        tokens = []
        try:
            with open(token_file, 'r') as file:
                tokens = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"Error: The token file '{token_file}' was not found.")
        except Exception as e:
            print(f"Error reading token file '{token_file}': {e}")
        return tokens

    def is_string_constant(self, token):
        string_pattern = r'^".{0,256}"$'
        return re.match(string_pattern, token) is not None

    def scan(self, program_file):
        with open(program_file, 'r') as f:
            for line_num, line in enumerate(f, start=1):
                self.scan_line(line.strip(), line_num)

        if self.errors:
            for error in self.errors:
                print(error)
            return False
        return True

    def scan_line(self, line, line_num):
        tokens = re.findall(
            r'\".*?\"|\'[^\']*\'|(?<!\d)[+-]?\d+(?!\d)|\b\w+\b|!=|==|<=|>=|[+\-*/%()]|[^\s\w]', line
        )

        for token in tokens:
            if re.match(r'^0\d+|[-+]?0\d+', token):
                self.errors.append(f"Lexical error at line {line_num}: invalid numeric literal '{token}'")
                continue

            if token in self.token_list:
                self.pif.append((token, -1, "keyword"))
                continue

            if token in ('+', '-', '*', '/', '%'):
                self.pif.append((token, -1, "operator"))
                continue

            if self.identifier_fa.is_accepted(token):
                if token not in self.unique_values:
                    self.unique_values[token] = self.index_counter
                    self.index_counter += 1
                pos = self.unique_values[token]
                self.pif.append((token, pos, "identifier"))

                if not self.symbol_table.contains_term(token):
                    self.symbol_table.add(token)

            elif self.is_string_constant(token):
                if token not in self.unique_values:
                    self.unique_values[token] = self.index_counter
                    self.index_counter += 1
                pos = self.unique_values[token]
                self.pif.append((token, pos, "string"))

                if not self.symbol_table.contains_term(token):
                    self.symbol_table.add(token)

            elif self.constant_fa.is_accepted(token):
                if token not in self.unique_values:
                    self.unique_values[token] = self.index_counter
                    self.index_counter += 1
                pos = self.unique_values[token]
                self.pif.append((token, pos, "int"))

                if not self.symbol_table.contains_term(token):
                    self.symbol_table.add(token)

            else:
                self.errors.append(f"Lexical error at line {line_num}: unknown token '{token}'")

    def write_outputs(self):
        with open('PIF.out', 'w') as pif_file:
            for token, pos, token_type in self.pif:
                pif_file.write(f"{token} {pos} {token_type}\n")

        with open('ST.out', 'w') as st_file:
            st_file.write(str(self.symbol_table))
