import os
from utils.finite_automata import FiniteAutomaton


def print_menu():
    print("1. Print states.")
    print("2. Print alphabet.")
    print("3. Print final states.")
    print("4. Print transitions.")
    print("5. Print initial state.")
    print("6. Print is deterministic.")
    print("7. Check if sequence is accepted by DFA.")
    print("0. Exit.")


def options_for_dfa():
    # Load the finite automaton from the specified file
    fa = FiniteAutomaton()

    # Get the FA file and parse it
    fa_file = "Input_Output/FA.in"

    if not os.path.exists(fa_file):
        print(f"Error: The FA file '{fa_file}' does not exist.")
        return

    fa.parse_fa_file(fa_file)  # Parse the FA file
    print("FA read from file.")

    # Print menu for user to choose an option
    print_menu()

    while True:
        option = input("Your option: ")

        if option == '0':
            break

        elif option == '1':
            print("States:")
            print(fa.get_states())
            print()
            print_menu()

        elif option == '2':
            print("Alphabet:")
            print(fa.get_alphabet())
            print()
            print_menu()

        elif option == '3':
            print("Final states:")
            print(fa.get_final_states())
            print()
            print_menu()

        elif option == '4':
            print("Transitions:")
            print(fa.write_transitions())
            print()
            print_menu()

        elif option == '5':
            print("Initial state:")
            print(fa.get_initial_state())
            print()
            print_menu()

        elif option == '6':
            print("Is deterministic?")
            print(fa.check_if_deterministic())
            print()
            print_menu()

        elif option == '7':
            input_string = input("Enter the sequence to check: ")
            if fa.is_accepted(input_string):
                print(f"Sequence '{input_string}' is valid.")
            else:
                print(f"Sequence '{input_string}' is invalid.")
            print()
            print_menu()

        elif option == '0':
            break

        else:
            print("Invalid option! Please try again.")
            print_menu()

if __name__ == "__main__":
    options_for_dfa()

