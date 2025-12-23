"""Command-line interface for pypie-lang."""

import argparse
import sys
from pathlib import Path

from pypie_lang.parser import PieParser
from pypie_lang.repl import repl


def interpret_file(filepath: str):
    """Interpret expressions from a file."""
    path = Path(filepath)

    if not path.exists():
        print(f"Error: File '{filepath}' not found", file=sys.stderr)
        sys.exit(1)

    if not path.is_file():
        print(f"Error: '{filepath}' is not a file", file=sys.stderr)
        sys.exit(1)

    try:
        content = path.read_text()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Split into lines and evaluate each expression
    lines = content.strip().split("\n")

    for line_num, line in enumerate(lines, start=1):
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#") or line.startswith(";"):
            continue

        try:
            parser = PieParser(line)
            result = parser.parse_expression()
            print(f"{result}")
        except Exception as e:
            print(f"Error on line {line_num}: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PyPie-Lang: A Python implementation of the Pie language",
        prog="pypie",
    )

    parser.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        help="interpret expressions from a file",
    )

    parser.add_argument(
        "-e",
        "--eval",
        metavar="EXPR",
        help="evaluate a single expression",
    )

    args = parser.parse_args()

    if args.file:
        interpret_file(args.file)
    elif args.eval:
        try:
            parser_obj = PieParser(args.eval)
            result = parser_obj.parse_expression()
            print(result)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # No arguments, start REPL
        repl()


if __name__ == "__main__":
    main()
