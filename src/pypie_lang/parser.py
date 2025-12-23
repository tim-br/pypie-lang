import io

from pypie_lang.tokenizer import Tokenizer
from pypie_lang.types import Atom, Nat, Pair


class PieParser:
    def __init__(self, text):
        self.tokenizer = Tokenizer(io.StringIO(text))

    def parse_word(self):
        return_atom = ""
        c = self.tokenizer.peek(False)
        while c and (not c.isspace()) and (not c == ")"):
            return_atom = return_atom + c
            self.tokenizer.advance(False)
            c = self.tokenizer.peek(False)
        return return_atom

    def parse_atom(self):
        c = self.tokenizer.peek(False)
        if c.isspace():
            self.tokenizer.advance(True)
        self.tokenizer.munch("'")
        return self.parse_word()

    def parse_type(self):
        """Parse a type expression like 'Atom' or '(Pair Atom Atom)'."""
        ch = self.tokenizer.peek(True)

        if ch == "(":
            self.tokenizer.advance(True)
            type_name = self.parse_word()
            if type_name == "Pair":
                # Parse the two type arguments
                self.parse_type()  # first type
                self.parse_type()  # second type
            self.tokenizer.munch(")")
            return type_name
        else:
            # Simple type like 'Atom'
            return self.parse_word()

    def parse_expression(self):
        ch = self.tokenizer.peek(True)

        return_value = None

        if ch == "(":
            self.tokenizer.advance(True)
            c = self.tokenizer.peek(True)

            if not c.isdigit() and not c == "'":
                keyword = self.parse_word()

                if keyword == "the":
                    # Parse type annotation: (the Type expression)
                    type_expr = self.parse_type()
                    value_expr = self.parse_expression()
                    self.tokenizer.munch(")")

                    # Wrap in appropriate type
                    if type_expr == "Atom":
                        # Atom type must have a quoted string, not a Pair
                        if isinstance(value_expr, Pair):
                            raise ValueError(
                                "Type error: (the Atom ...) requires a quoted atom, not a Pair"
                            )
                        if isinstance(value_expr, str) and value_expr.startswith("'"):
                            return Atom(value_expr)
                        return Atom(value_expr)
                    elif type_expr == "Pair":
                        # Pair type must have a cons expression
                        if not isinstance(value_expr, Pair):
                            raise ValueError(
                                f"Type error: (the Pair ...) requires a cons expression, "
                                f"got {type(value_expr).__name__}"
                            )
                        return value_expr
                    elif type_expr == "Nat":
                        # Nat type must have zero, add1, or int literal
                        if not isinstance(value_expr, Nat):
                            raise ValueError(
                                f"Type error: (the Nat ...) requires a natural number, "
                                f"got {type(value_expr).__name__}"
                            )
                        return value_expr
                    else:
                        # For other types, return the value as-is
                        return value_expr

                elif keyword == "zero":
                    # Parse zero: (zero) but we also allow just 'zero
                    self.tokenizer.munch(")")
                    return Nat.zero()

                elif keyword == "add1":
                    # Parse add1: (add1 n)
                    n = self.parse_expression()
                    self.tokenizer.munch(")")
                    if not isinstance(n, Nat):
                        raise ValueError(f"add1 requires a Nat, got {type(n).__name__}")
                    return Nat.add1(n)

                elif keyword == "cons":
                    # Parse cons expression: (cons first second)
                    fst = self.parse_expression()
                    snd = self.parse_expression()
                    pair = Pair(fst, snd)
                    if not (self.tokenizer.peek(False) == ")"):
                        self.tokenizer.advance(True)
                    self.tokenizer.munch(")")
                    return pair
                else:
                    raise ValueError(f"Unknown keyword: {keyword}")

            return self.parse_expression()

        if ch == "'":
            return_value = "'" + self.parse_atom()
            return return_value

        # Check for numeric literal or bare word like "zero"
        if ch and (ch.isdigit() or ch.isalpha()):
            word = self.parse_word()

            # Check if it's "zero"
            if word == "zero":
                return Nat.zero()

            # Check if it's a number
            if word.isdigit():
                return Nat(int(word))

            # Otherwise it's an unknown symbol
            raise ValueError(f"Unknown symbol: {word}")

        return None
