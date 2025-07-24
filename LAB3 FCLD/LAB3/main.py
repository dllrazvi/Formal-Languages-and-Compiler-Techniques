import os
from LAB3.utils.scanner import Scanner
from LAB3.utils.finite_automata import FiniteAutomaton


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

        elif option == '2':
            print("Alphabet:")
            print(fa.get_alphabet())
            print()

        elif option == '3':
            print("Final states:")
            print(fa.get_final_states())
            print()

        elif option == '4':
            print("Transitions:")
            print(fa.write_transitions())
            print()

        elif option == '5':
            print("Initial state:")
            print(fa.get_initial_state())
            print()

        elif option == '6':
            print("Is deterministic?")
            print(fa.check_if_deterministic())
            print()

        elif option == '7':
            input_string = input("Enter the sequence to check: ")
            if fa.is_accepted(input_string):
                print(f"Sequence '{input_string}' is valid.")
            else:
                print(f"Sequence '{input_string}' is invalid.")
            print()

        else:
            print("Invalid option! Please try again.")
            print_menu()


def run_scanner():
    files = ["Input_Output/p1.txt", "Input_Output/p2.txt", "Input_Output/p3.txt", "Input_Output/p1err.txt"]

    print("Available program files:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")

    try:
        selected_index = int(input("Enter the number of the file you want to run: ")) - 1
        if selected_index < 0 or selected_index >= len(files):
            print("Invalid file selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    selected_file = files[selected_index]
    print(f"Running scanner for {selected_file}...")

    token_file = "token.in"

    if not os.path.exists(token_file):
        print(f"Error: The token file '{token_file}' does not exist.")
        return

    if not os.path.exists(selected_file):
        print(f"Error: The program file '{selected_file}' does not exist.")
        return

    scanner = Scanner(token_file)
    if scanner.scan(selected_file):
        print("Scanning completed successfully.")
        scanner.write_outputs()
    else:
        print("Scanning failed due to lexical errors.")


def main():
    print("1. FA")
    print("2. Scanner")
    option = input("Your option: ")

    if option == '1':
        options_for_dfa()

    elif option == '2':
        run_scanner()

    else:
        print("Invalid option! Please choose 1 for FA or 2 for Scanner.")


if __name__ == "__main__":
    main()
