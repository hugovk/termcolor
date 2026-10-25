"""Tests for the Code objects: termcolor.fg, .bg, .attrs and .codes"""

from __future__ import annotations

import copy
import pickle

import pytest

import termcolor
from termcolor import ATTRIBUTES, COLORS, HIGHLIGHTS, RESET, Code, attrs, bg, codes, fg

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Generator


def _env(**env: str) -> Generator[None]:
    # Code objects decide whether colour is enabled when used, via the cache.
    with pytest.MonkeyPatch.context() as mp:
        for var in ("ANSI_COLORS_DISABLED", "NO_COLOR", "FORCE_COLOR"):
            mp.delenv(var, raising=False)
        for var, value in env.items():
            mp.setenv(var, value)
        termcolor.can_colorize.cache_clear()
        yield
    termcolor.can_colorize.cache_clear()


@pytest.fixture
def _color() -> Generator[None]:
    yield from _env(FORCE_COLOR="1")


@pytest.fixture
def _no_color() -> Generator[None]:
    yield from _env(NO_COLOR="1")


@pytest.mark.usefixtures("_color")
def test_string_form() -> None:
    assert f"{codes.red}{codes.on_blue}Hi{codes.reset}" == "\x1b[31m\x1b[44mHi\x1b[0m"
    assert f"{attrs.bold}{attrs.italic}Hi{codes.reset}" == "\x1b[1m\x1b[3mHi\x1b[0m"


@pytest.mark.usefixtures("_color")
def test_string_like() -> None:
    assert isinstance(fg.red, Code)
    assert str(fg.red) == "\x1b[31m"
    assert format(fg.red) == "\x1b[31m"
    assert f"{fg.red:>6}" == " \x1b[31m"
    assert "%s" % fg.red == "\x1b[31m"  # noqa: UP031  # test %-formatting works
    assert fg.red + "Hi" == "\x1b[31mHi"
    assert "Hi" + fg.red == "Hi\x1b[31m"
    assert fg.red + codes.on_blue == "\x1b[31m\x1b[44m"
    assert "".join(map(str, [fg.red, "Hi", codes.reset])) == "\x1b[31mHi\x1b[0m"


@pytest.mark.usefixtures("_color")
def test_call_form() -> None:
    assert codes.red("Hi") == "\x1b[31mHi\x1b[39m"
    assert codes.on_blue("Hi") == "\x1b[44mHi\x1b[49m"
    assert codes.bold("Hi") == "\x1b[1mHi\x1b[22m"
    assert codes.red(42) == "\x1b[31m42\x1b[39m"


@pytest.mark.usefixtures("_color")
def test_call_form_nests() -> None:
    # Only the inner style is switched off, so the outer one continues
    assert codes.italic(f"{codes.red('a')} b") == "\x1b[3m\x1b[31ma\x1b[39m b\x1b[23m"
    assert codes.bold(codes.red("Hi")) == "\x1b[1m\x1b[31mHi\x1b[39m\x1b[22m"


@pytest.mark.usefixtures("_color")
@pytest.mark.parametrize("name", COLORS)
def test_fg(name: str) -> None:
    code = getattr(fg, name)
    assert code is getattr(codes, name) is getattr(termcolor, name)
    assert str(code) == f"\x1b[{COLORS[name]}m"
    assert code("Hi") == f"\x1b[{COLORS[name]}mHi\x1b[39m"


@pytest.mark.usefixtures("_color")
@pytest.mark.parametrize("name", HIGHLIGHTS)
def test_bg(name: str) -> None:
    code = getattr(bg, name.removeprefix("on_"))
    assert code is getattr(codes, name) is getattr(termcolor, name)
    assert str(code) == f"\x1b[{HIGHLIGHTS[name]}m"
    assert code("Hi") == f"\x1b[{HIGHLIGHTS[name]}mHi\x1b[49m"


@pytest.mark.usefixtures("_color")
@pytest.mark.parametrize(
    "name, off",
    [
        ("bold", 22),
        ("dark", 22),
        ("italic", 23),
        ("underline", 24),
        ("blink", 25),
        ("reverse", 27),
        ("concealed", 28),
        ("strike", 29),
    ],
)
def test_attrs(name: str, off: int) -> None:
    code = getattr(attrs, name)
    assert code is getattr(codes, name) is getattr(termcolor, name)
    assert str(code) == f"\x1b[{ATTRIBUTES[name]}m"
    assert code("Hi") == f"\x1b[{ATTRIBUTES[name]}mHi\x1b[{off}m"


@pytest.mark.usefixtures("_color")
def test_rgb() -> None:
    assert str(fg.rgb(1, 2, 3)) == "\x1b[38;2;1;2;3m"
    assert fg.rgb(1, 2, 3)("Hi") == "\x1b[38;2;1;2;3mHi\x1b[39m"
    assert str(bg.rgb(1, 2, 3)) == "\x1b[48;2;1;2;3m"
    assert bg.rgb(1, 2, 3)("Hi") == "\x1b[48;2;1;2;3mHi\x1b[49m"


@pytest.mark.parametrize("r, g, b", [(256, 0, 0), (0, -1, 0)])
def test_rgb_invalid(r: int, g: int, b: int) -> None:
    with pytest.raises(ValueError, match="Expected a tuple of 3 ints in range 0-255"):
        fg.rgb(r, g, b)
    with pytest.raises(ValueError, match="Expected a tuple of 3 ints in range 0-255"):
        bg.rgb(r, g, b)


@pytest.mark.usefixtures("_color")
def test_reset() -> None:
    assert str(codes.reset) == RESET == "\x1b[0m"


@pytest.mark.usefixtures("_color")
def test_overrides_when_enabled() -> None:
    assert codes.red("Hi", no_color=True) == "Hi"
    assert codes.red("Hi", force_color=True) == "\x1b[31mHi\x1b[39m"


@pytest.mark.usefixtures("_no_color")
def test_disabled() -> None:
    assert str(codes.red) == ""
    assert str(codes.reset) == ""
    assert f"{codes.red}Hi{codes.reset}" == "Hi"
    assert codes.red + "Hi" == "Hi"
    assert codes.red("Hi") == "Hi"
    assert codes.bold(codes.red("Hi")) == "Hi"
    assert str(fg.rgb(1, 2, 3)) == ""
    # Codes stay distinct when disabled
    assert codes.red != codes.blue
    assert codes.red


@pytest.mark.usefixtures("_no_color")
def test_overrides_when_disabled() -> None:
    assert codes.red("Hi", force_color=True) == "\x1b[31mHi\x1b[39m"
    assert codes.red("Hi", no_color=True) == "Hi"


def test_eq_hash() -> None:
    assert fg.red == Code("\x1b[31m", "\x1b[39m")
    assert fg.red != fg.blue
    assert fg.red != "\x1b[31m"
    assert hash(fg.red) == hash(Code("\x1b[31m", "\x1b[39m"))
    assert len({fg.red, fg.blue, fg.red}) == 2
    assert fg.red


@pytest.mark.parametrize("fn", [copy.copy, copy.deepcopy])
def test_copy(fn: object) -> None:
    assert fn(fg.red) == fg.red  # type: ignore[operator]


def test_pickle() -> None:
    assert pickle.loads(pickle.dumps(fg.red)) == fg.red  # noqa: S301


def test_str_of_text_consistent() -> None:
    class Obj:
        def __str__(self) -> str:
            return "S"

        def __format__(self, spec: str) -> str:
            return "FMT"

    assert fg.red(Obj(), force_color=True) == "\x1b[31mS\x1b[39m"
    assert fg.red(Obj(), no_color=True) == "S"


def test_repr() -> None:
    assert repr(fg.red) == "Code('\\x1b[31m', '\\x1b[39m')"
    assert repr(Code("on", "off")) == "Code('on', 'off')"


def test_all() -> None:
    assert set(fg.__all__) == {*COLORS, "rgb"}
    assert set(bg.__all__) == {name.removeprefix("on_") for name in HIGHLIGHTS} | {
        "rgb"
    }
    assert set(attrs.__all__) == set(ATTRIBUTES)
    assert set(codes.__all__) == {*COLORS, *HIGHLIGHTS, *ATTRIBUTES, "reset"}
    assert set(codes.__all__) <= set(termcolor.__all__)
    for module in (fg, bg, attrs, codes, termcolor):
        for name in module.__all__:
            assert hasattr(module, name), f"{module.__name__}.{name}"
