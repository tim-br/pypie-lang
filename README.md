# pypie-lang

A Python implementation of the Pie language with support for atoms, pairs, and type annotations.

## Installation

```bash
uv pip install -e .
```

## Usage

### REPL (Interactive Mode)

Start the interactive REPL by running `pypie` without arguments:

```bash
uv run pypie
```

Example session:
```
PyPie-Lang REPL
Type expressions to evaluate them, or 'quit' to exit.

pypie> (the Atom 'hello)
Atom('hello)
pypie> (cons 'a 'b)
Pair('a, 'b)
pypie> zero
zero
pypie> (add1 (add1 zero))
(add1 (add1 zero))
pypie> 5
(add1 (add1 (add1 (add1 (add1 zero)))))
pypie> quit
Goodbye!
```

### Evaluate Single Expression

Use the `-e` flag to evaluate a single expression:

```bash
uv run pypie -e "(the Atom 'hello)"
# Output: Atom('hello)

uv run pypie -e "(cons 'a 'b)"
# Output: Pair('a, 'b)
```

### Interpret File

Create a `.pie` file with expressions (one per line):

```pie
# examples/demo.pie
(the Atom 'hello)
(cons 'first 'second)
(the (Pair Atom Atom) (cons 'a 'b))
```

Run it with the `-f` flag:

```bash
uv run pypie -f examples/demo.pie
# Output:
# Atom('hello)
# Pair('first, 'second)
# Pair('a, 'b)
```

### Language Features

- **Atoms**: Quoted values like `'hello`
  - Type annotation: `(the Atom 'value)`
- **Pairs**: Constructed with `cons`
  - Simple: `(cons 'first 'second)`
  - Type annotation: `(the (Pair Atom Atom) (cons 'a 'b))`
- **Natural Numbers**: Peano-style natural numbers
  - Zero: `zero` or `(zero)` or literal `0`
  - Successor: `(add1 zero)` for 1, `(add1 (add1 zero))` for 2, etc.
  - Numeric literals: `5` (equivalent to `(add1 (add1 (add1 (add1 (add1 zero)))))`)
  - Type annotation: `(the Nat 3)`
- **Comments**: Lines starting with `#` or `;` (in files)

## Development

This project uses [UV](https://github.com/astral-sh/uv) for dependency management.

### Setup

```bash
# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate
```

### Running Tests

```bash
# Run all tests
uv run python -m unittest discover -s tests

# Run specific test file
uv run python -m unittest tests.test_basic

# Run with verbose output
uv run python -m unittest discover -s tests -v
```

### Code Formatting and Linting

This project uses [Ruff](https://docs.astral.sh/ruff/) for formatting and linting.

```bash
# Format code
uv run ruff format

# Lint code
uv run ruff check

# Lint and auto-fix issues
uv run ruff check --fix

# Check formatting without changing files
uv run ruff format --check
```

### Project Structure

```
pypie-lang/
├── src/
│   └── pypie_lang/        # Main package
│       ├── __init__.py
│       ├── tokenizer.py   # Lexical analysis
│       ├── parser.py      # Parser and AST types (Atom, Pair)
│       ├── repl.py        # Interactive REPL
│       ├── cli.py         # Command-line interface
│       └── py.typed       # PEP 561 marker for type hints
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_basic.py
│   └── test_parser.py
├── pyproject.toml         # Project configuration
└── README.md
```

## License

GNU General Public License v3
