import unittest

from pypie_lang.parser import Atom, Pair, PieParser


class TestBasic(unittest.TestCase):
    """Basic tests for pypie-lang package."""

    def test_char(self):
        """Test that the package can be imported."""
        expression = "  ( 'car)"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertEqual(result, "'car")

    def test_char2(self):
        """Test that the package can be imported."""
        expression = "  ( 'car   )"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertEqual(result, "'car")

    def test_char4(self):
        """Test that the package can be imported."""
        expression = "  ( cons 'foo 'bar  )"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertEqual(result, Pair("'foo", "'bar"))

    def test_char5(self):
        """Test that the package can be imported."""
        expression = "( cons (cons 'a (cons 'a 'b)) 'bar  )"
        parser = PieParser(expression)
        result = parser.parse_expression()
        print("result")
        print(result)
        self.assertEqual(result.fst().snd(), Pair("'a", "'b"))

    def test_the_atom(self):
        """Test (the Atom 'value) syntax."""
        expression = "(the Atom 'fine)"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertIsInstance(result, Atom)
        self.assertEqual(result, Atom("'fine"))

    def test_the_pair(self):
        """Test (the (Pair Atom Atom) (cons 'a 'b)) syntax."""
        expression = "(the (Pair Atom Atom) (cons 'a 'b))"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertIsInstance(result, Pair)
        self.assertEqual(result, Pair("'a", "'b"))

    def test_the_pair_simple(self):
        """Test (the Pair 'rie) syntax - should reject non-cons values."""
        expression = "(the Pair 'rie)"
        parser = PieParser(expression)
        with self.assertRaises(ValueError) as context:
            parser.parse_expression()
        self.assertIn("requires a cons expression", str(context.exception))

    def test_the_pair_with_cons(self):
        """Test (the Pair (cons 'a 'b)) syntax - should accept cons."""
        expression = "(the Pair (cons 'a 'b))"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertIsInstance(result, Pair)
        self.assertEqual(result, Pair("'a", "'b"))

    def test_the_atom_with_cons(self):
        """Test (the Atom (cons 'a 'b)) syntax - should reject cons values."""
        expression = "(the Atom (cons 'a 'b))"
        parser = PieParser(expression)
        with self.assertRaises(ValueError) as context:
            parser.parse_expression()
        self.assertIn("requires a quoted atom", str(context.exception))
