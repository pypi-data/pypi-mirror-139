import textwrap
from typing import Any

_STRING_FORMATTER_KWARGS = {"break_long_words": False, "width": 88}


def format_multiline_string(text: str, **kwargs: Any) -> str:
    """
    Align text left and remove newlines.

    Args:
        text:
            The string to convert.
        kwargs:
            keyword arguments passed to `textwrap.wrap` in order to format text.
            Default args are {"tabsize": 4, "break_long_words": False, "width": 88}

    Returns:
        A copy of the converted string.
    """
    has_random_whitespace = textwrap.fill(
        text, **_STRING_FORMATTER_KWARGS, **kwargs
    ).strip()
    # `textwrap.fill` appears to keep random whitespace in paragraphs. Note
    # that all whitespace is spaces (' ').
    # The following code removes the whitespace by iteratively replacing
    # multiple whitespaces with a single whitespace until multi-whitespace is
    # gone.
    maybe_removed_of_random_whitespace = has_random_whitespace
    while True:
        maybe_removed_of_random_whitespace = maybe_removed_of_random_whitespace.replace(
            "  ", " "
        )
        if maybe_removed_of_random_whitespace == has_random_whitespace:
            return maybe_removed_of_random_whitespace
        has_random_whitespace = maybe_removed_of_random_whitespace
