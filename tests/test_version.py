from __future__ import annotations

import pytest

from termcolor import VERSION, __version__
from termcolor._version import _convert_version_string_to_tuple


@pytest.mark.parametrize(
    "version_string, expected",
    [
        ("1.1.1", (1, 1, 1)),
        ("1.1.1.dev32", (1, 1, 1, "dev32")),
    ],
)
def test__convert_version_string_to_tuple(
    version_string: str, expected: tuple[int | str, ...]
) -> None:
    # Act
    version_tuple = _convert_version_string_to_tuple(version_string)
    # Assert
    assert version_tuple == expected


def test_version() -> None:
    assert isinstance(VERSION, tuple)
    assert isinstance(__version__, str)
