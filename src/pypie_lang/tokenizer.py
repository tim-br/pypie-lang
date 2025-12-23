import io


class Tokenizer:
    def __init__(self, reader):
        self.reader = reader
        c = self.reader.read(1)
        self.current_char = c if c else None
        self.position = 1
    def get_position(self):
        return self.position

    def peek(self, skip_whitespace):
        if self.current_char is None or (skip_whitespace and self.current_char.isspace()):
            self.advance(skip_whitespace)
        return self.current_char

    def advance(self, skip_whitespace):
        if self.current_char is None:
            return
        while True:
            self.position += 1
            c = self.reader.read(1)
            if not c:  # EOF
                self.current_char = None
                return
            if not (skip_whitespace and c.isspace()):
                self.current_char = c
                return

    def munch(self, c):
        ch = self.peek(False)

        if self.peek(False) != c:
            raise ValueError(
                f"Munching error at character position {self.position}")
        else:
            self.advance(True)
