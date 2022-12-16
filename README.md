# termcolor

[![PyPI version](https://img.shields.io/pypi/v/termcolor.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/termcolor)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/termcolor.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/termcolor)
[![PyPI downloads](https://img.shields.io/pypi/dm/termcolor.svg)](https://pypistats.org/packages/termcolor)
[![GitHub Actions status](https://github.com/termcolor/termcolor/workflows/Test/badge.svg)](https://github.com/termcolor/termcolor/actions)
[![Codecov](https://codecov.io/gh/termcolor/termcolor/branch/main/graph/badge.svg)](https://codecov.io/gh/termcolor/termcolor)
[![Licence](https://img.shields.io/github/license/termcolor/termcolor.svg)](COPYING.txt)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)
[![Tidelift](https://tidelift.com/badges/package/pypi/termcolor)](https://tidelift.com/subscription/pkg/pypi-termcolor?utm_source=pypi-termcolor&utm_medium=referral&utm_campaign=readme)

## Installation

### From PyPI

```bash
python3 -m pip install --upgrade termcolor
```

### From source

```bash
git clone https://github.com/termcolor/termcolor
cd termcolor
python3 -m pip install .
```

### Demo

To see demo output, run:

```bash
python3 -m termcolor
```

## Example

```python
import sys

from termcolor import colored, cprint

text = colored("Hello, World!", "red", attrs=["reverse", "blink"])
print(text)
cprint("Hello, World!", "green", "on_red")

print_red_on_cyan = lambda x: cprint(x, "red", "on_cyan")
print_red_on_cyan("Hello, World!")
print_red_on_cyan("Hello, Universe!")

for i in range(10):
    cprint(i, "magenta", end=" ")

cprint("Attention!", "red", attrs=["bold"], file=sys.stderr)
```

## Text properties

| Text colors     | Text highlights    | Attributes  |
| --------------- | ------------------ | ----------- |
| `black`         | `on_black`         | `bold`      |
| `red`           | `on_red`           | `dark`      |
| `green`         | `on_green`         | `underline` |
| `yellow`        | `on_yellow`        | `blink`     |
| `blue`          | `on_blue`          | `reverse`   |
| `magenta`       | `on_magenta`       | `concealed` |
| `cyan`          | `on_cyan`          |             |
| `white`         | `on_white`         |             |
| `light_grey`    | `on_light_grey`    |             |
| `dark_grey`     | `on_dark_grey`     |             |
| `light_red`     | `on_light_red`     |             |
| `light_green`   | `on_light_green`   |             |
| `light_yellow`  | `on_light_yellow`  |             |
| `light_blue`    | `on_light_blue`    |             |
| `light_magenta` | `on_light_magenta` |             |
| `light_cyan`    | `on_light_cyan`    |             |

## Terminal properties

| Terminal     | bold    | dark | underline | blink      | reverse | concealed |
| ------------ | ------- | ---- | --------- | ---------- | ------- | --------- |
| xterm        | yes     | no   | yes       | bold       | yes     | yes       |
| linux        | yes     | yes  | bold      | yes        | yes     | no        |
| rxvt         | yes     | no   | yes       | bold/black | yes     | no        |
| dtterm       | yes     | yes  | yes       | reverse    | yes     | yes       |
| teraterm     | reverse | no   | yes       | rev/red    | yes     | no        |
| aixterm      | normal  | no   | yes       | no         | yes     | yes       |
| PuTTY        | color   | no   | yes       | no         | yes     | no        |
| Windows      | no      | no   | no        | no         | yes     | no        |
| Cygwin SSH   | yes     | no   | color     | color      | color   | yes       |
| Mac Terminal | yes     | no   | yes       | yes        | yes     | yes       |

## Environment variables

Colour can be disabled or enabled via the presence of environment variables (regardless
of value, but a truthy value recommended).

In priority order, if one of these is set, the later vars are not checked.

| Env var                | Action                                   |
| ---------------------- | ---------------------------------------- |
| `ANSI_COLORS_DISABLED` | Disable colour                           |
| `NO_COLOR`             | Disable colour, see https://no-color.org |
| `FORCE_COLOR`          | Enable colour                            |

For example, set `FORCE_COLOR=1` to always output in colour.
