class FiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.final_states = set()

    def add_state(self, state, is_final=False):
        self.states.add(state)
        if is_final:
            self.final_states.add(state)

    def add_transition(self, from_state, symbol, to_state):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][symbol] = to_state

    def set_initial_state(self, state):
        self.initial_state = state

    def get_states(self):
        return self.states

    def get_alphabet(self):
        return self.alphabet

    def get_final_states(self):
        return self.final_states

    def get_initial_state(self):
        return self.initial_state

    def write_transitions(self):
        transitions_str = ""
        for from_state, trans in self.transitions.items():
            for symbol, to_state in trans.items():
                transitions_str += f"{from_state} --{symbol}--> {to_state}\n"
        return transitions_str

    def check_if_deterministic(self):
        for state, trans in self.transitions.items():
            if len(trans) != len(set(trans.values())):
                return False
        return True

    def display(self):
        print(f"States: {self.states}")
        print(f"Alphabet: {self.alphabet}")
        print(f"Initial State: {self.initial_state}")
        print(f"Final States: {self.final_states}")
        print("Transitions:")
        for state, trans in self.transitions.items():
            for symbol, to_state in trans.items():
                print(f"  {state} --{symbol}--> {to_state}")



    def parse_fa_file(self, fa_file):
        with open(fa_file, 'r') as file:
            lines = file.readlines()


        states_line = lines[0].strip().split(';')
        self.states.update(states_line)

        self.set_initial_state(lines[1].strip())


        final_states_line = lines[2].strip().split(';')
        for final_state in final_states_line:
            self.add_state(final_state, is_final=True)


        for line in lines[3:]:
            transition_parts = line.strip().split()
            if len(transition_parts) == 3:
                from_state, symbol, to_state = transition_parts
                self.add_transition(from_state, symbol, to_state)
                self.alphabet.add(symbol)

    def is_accepted(self, input_string):
        current_state = self.initial_state
        for symbol in input_string:
            if symbol not in self.transitions.get(current_state, {}):
                return False
            current_state = self.transitions[current_state][symbol]
        return current_state in self.final_states