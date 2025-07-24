from Grammar import ContextFreeGrammar
from Parser import Parser
from PrintParser import PrintParser


def main():
    print("Welcome to the Parser Program!")
    while True:
        print("Please choose a grammar file:")
        print("1. g1.txt")
        print("2. g2.txt")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            grammar_file = "g1.txt"
            input_file = "seq.txt"
            out_file = "out1.txt"
        elif choice == '2':
            grammar_file = "g2.txt"
            input_file = "seq.txt"
            out_file = "PIF.out"
        elif choice == '0':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Try again.")
            continue

        grammar = ContextFreeGrammar()
        try:
            grammar.load_grammar(grammar_file)
        except FileNotFoundError:
            print(f"Error: The file '{grammar_file}' could not be found.")
            return

        parser = Parser(grammar, out_file=out_file, in_file=input_file)
        parser.parsingStrategy('')

        if parser.getState() == 'f':
            print("Parsing completed successfully.")
            output = PrintParser(parser.getTree())
            output.printToFile('tree.txt')
            print("The parsing tree has been saved to 'tree.txt'.")
        else:
            print("Parsing failed. Check the output file for details.")


if __name__ == "__main__":
    main()
