import unittest
from Grammar import Grammar
from Parser import Parser

class TestParser(unittest.TestCase):

    def setUp(self):
        self.grammar_file = "g1.txt"  # Grammar definition file
        self.sequence_file = "seq.txt"  # Input sequence file containing: a b b
        self.output_file = "outg1.txt"  # Output file for parsing logs
        self.grammar = Grammar()
        self.grammar.load_grammar(self.grammar_file)
        self.parser = Parser(self.grammar, self.output_file, self.sequence_file)

    def test_momentaryInsuccess(self):
        self.parser._momentary_insuccess()
        self.assertEqual(self.parser.get_state(), 'b')

    def test_advance(self):
        self.parser.set_input_stack(['a', 'A'])
        self.parser.set_working_stack([('S', 1)])
        self.parser.set_index(0)  # Adjusted index to reflect starting position
        self.parser._advance()
        self.assertEqual(self.parser.get_index(), 1)
        self.assertEqual(self.parser.get_input_stack(), ['A'])
        self.assertEqual(self.parser.get_working_stack(), [('S', 1), 'a'])

    def test_expand(self):
        self.parser.set_input_stack(['S'])
        self.parser.set_working_stack([])
        self.parser.set_index(0)
        self.parser._expand()
        self.assertEqual(self.parser.get_input_stack(), ['a', 'A'])
        self.assertEqual(self.parser.get_working_stack(), [('S', 1)])
        self.assertEqual(self.parser.get_index(), 0)

    def test_success(self):
        self.parser._success()
        self.assertEqual(self.parser.get_state(), "f")

    def test_back(self):
        self.parser.set_state("b")
        self.parser.set_index(1)
        self.parser.set_working_stack([("S", 1), "a"])
        self.parser.set_input_stack(["b", "b"])
        self.parser._backtrack()
        self.assertEqual(self.parser.get_working_stack(), [("S", 1)])
        self.assertEqual(self.parser.get_input_stack(), ["a", "b", "b"])
        self.assertEqual(self.parser.get_index(), 0)

    def test_another_try(self):
        self.parser.set_state("b")
        self.parser.set_index(2)
        self.parser.set_working_stack([("S", 1), "a", ("A", 1)])
        self.parser.set_input_stack(["b", "b"])
        self.parser._try_next_production()
        self.assertEqual(self.parser.get_working_stack(), [("S", 1), "a", ("A", 2)])
        self.assertEqual(self.parser.get_input_stack(), ["b", "b"])
        self.assertEqual(self.parser.get_state(), 'q')


if __name__ == "__main__":
    unittest.main()
