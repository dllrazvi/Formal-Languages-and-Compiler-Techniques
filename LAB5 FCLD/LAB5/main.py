from Grammar import Grammar

def main():
    # Load the grammar from the g2.txt file
    grammar_file = "g2.txt"
    try:
        grammar = Grammar.fromFile(grammar_file)
    except Exception as e:
        print(f"Error loading grammar: {e}")
        return

    print("Grammar successfully loaded:")
    print(grammar)

    while True:
        print("\nEnter a sequence of tokens to parse (comma-separated) or type 'exit' to quit:")
        user_input = input("> ").strip()

        if user_input.lower() == "exit":
            break

        # Convert input to a list of tokens
        tokens = [token.strip() for token in user_input.split(",")]

        print(f"Parsing tokens: {tokens}")

        # Attempt to parse the tokens
        if grammar.parse(tokens):
            print("The input is valid according to the grammar.")
        else:
            print("The input is invalid.")

if __name__ == "__main__":
    main()
