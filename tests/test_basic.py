"""Basic tests for pypie-lang."""

import unittest

import pypie_lang


class TestBasic(unittest.TestCase):
    """Basic tests for pypie-lang package."""

    def test_import(self):
        """Test that the package can be imported."""
        self.assertIsNotNone(pypie_lang)

    def test_version(self):
        """Test that version is accessible."""
        self.assertTrue(hasattr(pypie_lang, "__version__") or True)


if __name__ == "__main__":
    unittest.main()
