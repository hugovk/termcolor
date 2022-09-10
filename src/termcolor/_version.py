from __future__ import annotations

try:
    # Python 3.8+
    import importlib.metadata as importlib_metadata
except ImportError:
    # Python 3.7 and lower
    import importlib_metadata  # type: ignore


def _convert_version_string_to_tuple(version_string: str) -> tuple[int | str, ...]:
    version_list: list[int | str] = []
    for part in version_string.split("."):
        try:
            version_list.append(int(part))
        except ValueError:
            version_list.append(part)
    return tuple(version_list)


__version__ = importlib_metadata.version("termcolor")
VERSION = _convert_version_string_to_tuple(__version__)
