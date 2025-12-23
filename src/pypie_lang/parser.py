import io

from pypie_lang.tokenizer import Tokenizer


class Atom:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"Atom({self.value})"

    def __eq__(self, other):
        if isinstance(other, Atom):
            return self.value == other.value
        return False

    def __repr__(self):
        return self.__str__()


class Pair[T1, T2]:
    def __init__(self, first: T1, second: T2):
        self.first = first
        self.second = second

    def fst(self):
        return self.first

    def snd(self):
        return self.second

    def __str__(self):
        return f"Pair({self.first}, {self.second})"

    def __eq__(self, other):
        if isinstance(other, Pair):
            return self.first == other.first and self.second == other.second
        return False

    def __repr__(self):
        return self.__str__()


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
                    else:
                        # For other types, return the value as-is
                        return value_expr

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
