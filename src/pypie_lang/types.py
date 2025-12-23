"""Data types for pypie-lang."""


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


class Nat:
    """Represents a natural number in Peano arithmetic."""

    def __init__(self, value: int = 0):
        """Create a Nat from a Python int."""
        if value < 0:
            raise ValueError("Natural numbers must be non-negative")
        self._value = value

    @staticmethod
    def zero():
        """Return the natural number zero."""
        return Nat(0)

    @staticmethod
    def add1(n):
        """Return the successor of n."""
        if isinstance(n, Nat):
            return Nat(n._value + 1)
        raise TypeError("add1 requires a Nat")

    def to_int(self):
        """Convert Nat to Python int."""
        return self._value

    def __str__(self):
        """Return string representation as nested add1/zero."""
        if self._value == 0:
            return "zero"
        result = "zero"
        for _ in range(self._value):
            result = f"(add1 {result})"
        return result

    def __eq__(self, other):
        if isinstance(other, Nat):
            return self._value == other._value
        return False

    def __repr__(self):
        return self.__str__()
