"""Interactive REPL for pypie-lang."""

import sys

from pypie_lang.parser import PieParser


def repl():
    """Run the interactive REPL."""
    print("PyPie-Lang REPL")
    print("Type expressions to evaluate them, or 'quit' to exit.")
    print()

    while True:
        try:
            # Read input
            user_input = input("pypie> ").strip()

            # Check for exit commands
            if user_input.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break

            # Skip empty input
            if not user_input:
                continue

            # Parse and evaluate
            parser = PieParser(user_input)
            result = parser.parse_expression()

            # Print result
            print(result)

        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    repl()
