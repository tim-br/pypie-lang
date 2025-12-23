# pypie-lang

A Python language implementation project.

## Installation

```bash
uv pip install -e .
```

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
│       └── py.typed       # PEP 561 marker for type hints
├── tests/                 # Test suite
│   ├── __init__.py
│   └── test_basic.py
├── pyproject.toml         # Project configuration
└── README.md
```

## License

GNU General Public License v3
