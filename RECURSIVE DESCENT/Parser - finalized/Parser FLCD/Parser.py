import logging
from Symbol import Symbol
from PrintParser import PrintParser

class Parser:
    def __init__(self, grammar, output_file, input_file):
        """
        Parser class to check if a sequence belongs to a given grammar using recursive descent parsing.

        Attributes:
        - working_stack: Stack to store the way the parse is built (alpha).
        - input_stack: Stack containing part of the tree to be built (beta).
        - state: Parsing state, which can be:
          - 'q': Normal state
          - 'b': Backtracking state
          - 'f': Final state (success)
          - 'e': Error state (failure)
        - index: Position of the current symbol in the input sequence.

        :param grammar: Grammar for parsing.
        :param output_file: File to store parsing progress and results.
        :param input_file: File containing the sequence to parse.
        """
        self._grammar = grammar
        self._working_stack = []
        self._input_stack = [self._grammar.start_sym()]
        self._state = "q"
        self._index = 0
        self._tree = []
        self._output_file = output_file
        self._sequence = []
        self._read_sequence(input_file)

        # Clear output file
        with open(self._output_file, 'w') as file:
            file.write("")

    def _read_sequence(self, sequence_file):
        """Read input sequence from a file."""
        with open(sequence_file) as file:
            if sequence_file == "PIF.out":
                for line in file:
                    tokens = line.split("'")
                    self._sequence.append(tokens[1])
            else:
                for line in file:
                    self._sequence.append(line.strip())

    def get_tree(self):
        return self._tree

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index

    def get_working_stack(self):
        return self._working_stack

    def set_working_stack(self, stack):
        self._working_stack = stack

    def get_input_stack(self):
        return self._input_stack

    def set_input_stack(self, stack):
        self._input_stack = stack

    def print_current_configuration(self):
        """Print the current parsing configuration to the console."""
        print('**************')
        print(f'State: {self._state}\n')
        print(f'Index: {self._index}\n')
        print(f'Working stack: {self._working_stack}\n')
        print(f'Input stack: {self._input_stack}\n')
        print('**************')

    def log_configuration_to_file(self):
        """Log the current parsing configuration to the output file."""
        with open(self._output_file, 'a') as file:
            file.write("\n--------------\n")
            file.write(f'State: {self._state} Index: {self._index}\n')
            file.write(f'Working stack: {self._working_stack}\n')
            file.write(f'Input stack: {self._input_stack}\n')

    def write_to_output_file(self, message, is_final=False):
        """Write a message to the output file."""
        with open(self._output_file, 'a') as file:
            if is_final:
                file.write(f"Sequence {message} is accepted!\n")
            else:
                file.write(message)

    def parsing_strategy(self):
        """Parse a sequence using recursive descent parsing."""
        sequence = self._sequence

        while self._state not in ('f', 'e'):
            self.log_configuration_to_file()
            if self._state == 'q':
                if self._index == len(sequence) and not self._input_stack:
                    self._success()
                elif not self._input_stack:
                    self._momentary_insuccess()
                elif self._input_stack[0] in self._grammar.non_terminals_list():
                    self._expand()
                elif self._index < len(sequence) and self._input_stack[0] == sequence[self._index]:
                    self._advance()
                else:
                    self._momentary_insuccess()
            elif self._state == 'b':
                if self._working_stack[-1] in self._grammar.terminals_list():
                    self._backtrack()
                else:
                    self._try_next_production()

        if self._state == 'e':
            print(f'Error at index {self._index}!')
        else:
            print(f'Sequence {sequence} is accepted!')
            print(self._working_stack)
            self.write_to_output_file(self._working_stack, True)
        self._build_parsing_tree()

    def _expand(self):
        """Expand the first non-terminal in the input stack using its first production."""
        self.write_to_output_file('expand\n')
        non_terminal = self._input_stack.pop(0)
        production = self._grammar.productions_for(non_terminal)[0]
        self._working_stack.append((non_terminal, production[1]))
        production_elements = production[0].split('$')
        self._input_stack = production_elements + self._input_stack

    def _advance(self):
        """Advance to the next symbol in the input sequence."""
        self.write_to_output_file('advance\n')
        terminal = self._input_stack.pop(0)
        self._working_stack.append(terminal)
        self._index += 1

    def _momentary_insuccess(self):
        """Switch to backtracking state."""
        self.write_to_output_file('momentary insuccess\n')
        self._state = 'b'

    def _backtrack(self):
        """Backtrack to the previous symbol in the input sequence."""
        self.write_to_output_file('back\n')
        last_symbol = self._working_stack.pop()
        self._input_stack.insert(0, last_symbol)
        self._index -= 1

    def _try_next_production(self):
        """Attempt the next production for a non-terminal in the working stack."""
        self.write_to_output_file('another try\n')
        last_entry = self._working_stack.pop()

        if self._grammar.has_additional_production(last_entry[0], last_entry[1]):
            self._state = 'q'
            self._working_stack.append((last_entry[0], last_entry[1] + 1))
            production_elements = self._grammar.specific_production(last_entry[0], last_entry[1] + 1)[0]
            production_length = len(production_elements.split('$'))
            self._input_stack = self._input_stack[production_length:]
            self._input_stack = production_elements.split('$') + self._input_stack
        elif self._index == 0 and last_entry[0] == self._grammar.start_sym():
            self._state = 'e'
        else:
            production_elements = self._grammar.specific_production(last_entry[0], last_entry[1])
            production_length = len(production_elements[0].split('$'))
            self._input_stack = self._input_stack[production_length:]
            self._input_stack.insert(0, last_entry[0])

    def _success(self):
        """Mark the parsing as successful."""
        self.write_to_output_file('success\n')
        self._state = 'f'

    def _build_parsing_tree(self):
        """Construct the parsing tree based on the working stack."""
        parent_index = -1

        for i, entry in enumerate(self._working_stack):
            if isinstance(entry, tuple):
                self._tree.append(Symbol(entry[0]))
                self._tree[i].production = entry[1]
            else:
                self._tree.append(Symbol(entry))

        for i, entry in enumerate(self._working_stack):
            if isinstance(entry, tuple):
                if self._tree[i].father == -1:
                    self._tree[i].father = parent_index
                parent_index = i

                production_length = len(self._grammar.specific_production(entry[0], entry[1])[0].split('$'))
                child_indices = [i + j for j in                 range(1, production_length + 1)]

                # Adjust child indices based on nested productions
                for j in range(len(child_indices)):
                    if self._tree[child_indices[j]].production != -1:
                        offset = self._get_subtree_length(child_indices[j])
                        for k in range(j + 1, len(child_indices)):
                            child_indices[k] += offset
                            if child_indices[k] >= len(self._tree):
                                child_indices[k] -= 1

                # Establish sibling and father relationships
                for j in range(len(child_indices) - 1):
                    self._tree[child_indices[j]].sibling = child_indices[j + 1]
                    if self._tree[child_indices[j]].father == -1:
                        self._tree[child_indices[j]].father = parent_index
                    if j == len(child_indices) - 2 and self._tree[child_indices[j + 1]].father == -1:
                        self._tree[child_indices[j + 1]].father = parent_index
            else:
                if self._tree[i].father == -1:
                    self._tree[i].father = parent_index
                parent_index = -1

    def _get_subtree_length(self, index):
        """Recursively compute the length of a subtree starting at the given index."""
        production_length = len(self._grammar.specific_production(
            self._working_stack[index][0], self._working_stack[index][1])[0].split('$'))
        total_length = production_length

        for j in range(1, production_length + 1):
            if isinstance(self._working_stack[index + j], tuple):
                total_length += self._get_subtree_length(index + j)

        return total_length
