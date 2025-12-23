import unittest

from pypie_lang.parser import PieParser
from pypie_lang.types import Atom, Nat, Pair


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

    def test_nat_zero(self):
        """Test parsing zero."""
        expression = "zero"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertIsInstance(result, Nat)
        self.assertEqual(result.to_int(), 0)
        self.assertEqual(str(result), "zero")

    def test_nat_zero_parens(self):
        """Test parsing (zero)."""
        expression = "(zero)"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertIsInstance(result, Nat)
        self.assertEqual(result.to_int(), 0)

    def test_nat_add1(self):
        """Test parsing (add1 zero)."""
        expression = "(add1 zero)"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertIsInstance(result, Nat)
        self.assertEqual(result.to_int(), 1)
        self.assertEqual(str(result), "(add1 zero)")

    def test_nat_add1_nested(self):
        """Test parsing (add1 (add1 (add1 zero)))."""
        expression = "(add1 (add1 (add1 zero)))"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertIsInstance(result, Nat)
        self.assertEqual(result.to_int(), 3)
        self.assertEqual(str(result), "(add1 (add1 (add1 zero)))")

    def test_nat_literal(self):
        """Test parsing numeric literal 5."""
        expression = "5"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertIsInstance(result, Nat)
        self.assertEqual(result.to_int(), 5)

    def test_nat_literal_zero(self):
        """Test parsing numeric literal 0."""
        expression = "0"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertIsInstance(result, Nat)
        self.assertEqual(result.to_int(), 0)

    def test_the_nat(self):
        """Test (the Nat 3) syntax."""
        expression = "(the Nat 3)"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertIsInstance(result, Nat)
        self.assertEqual(result.to_int(), 3)

    def test_the_nat_zero(self):
        """Test (the Nat zero) syntax."""
        expression = "(the Nat zero)"
        parser = PieParser(expression)
        result = parser.parse_expression()
        self.assertIsInstance(result, Nat)
        self.assertEqual(result.to_int(), 0)

    def test_the_nat_with_atom(self):
        """Test (the Nat 'foo) should fail."""
        expression = "(the Nat 'foo)"
        parser = PieParser(expression)
        with self.assertRaises(ValueError) as context:
            parser.parse_expression()
        self.assertIn("requires a natural number", str(context.exception))
