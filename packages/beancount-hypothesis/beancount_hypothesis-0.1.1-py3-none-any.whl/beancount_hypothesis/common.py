import string

from hypothesis import strategies as s
from random_words import RandomWords  # type: ignore


def currency(currencies: list[str] = None) -> s.SearchStrategy[str]:
    """Generates a random currency from the given list or a random one if None.

    Args:
        currencies: A list of currencies to sample from.

    Returns:
        A random currency."""
    if currencies:
        return s.sampled_from(currencies)
    else:
        return s.text(string.ascii_uppercase, min_size=3, max_size=3)


@s.composite
def filename(draw: s.DrawFn) -> str:
    """Generates a random filename string.

    Returns:
        A random filename string.
    """
    file_parts = draw(s.lists(word(), min_size=2, max_size=5))
    file_ext = draw(s.text(string.ascii_lowercase, min_size=3, max_size=3))
    return "/".join(file_parts) + "." + file_ext


@s.composite
def word(_) -> str:
    """Generates a random word.

    Returns:
        A new strategy
    """
    rw = RandomWords()
    return rw.random_word()


@s.composite
def words(draw: s.DrawFn, min=3, max=5):
    """Generates a string of random words.

    Args:
        min: The minimum number of words to generate
        max: The maximum number of words to generate

    Returns:
        A new strategy
    """
    return " ".join(draw(s.lists(word(), min_size=min, max_size=max)))
