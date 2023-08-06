"""
This example shows how to display content in columns.
The data is pulled from https://randomuser.me
"""

import json
from urllib.request import urlopen
from itertools import accumulate
from bisect import bisect
from random import randrange
from unicodedata import name as unicode_name


from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel


UNICODE_VERSION = 6

# Sauce: http://www.unicode.org/charts/PDF/U1F300.pdf
EMOJI_RANGES_UNICODE = {
    6: [
        ('\U0001F300', '\U0001F320'),
        ('\U0001F330', '\U0001F335'),
        ('\U0001F337', '\U0001F37C'),
        ('\U0001F380', '\U0001F393'),
        ('\U0001F3A0', '\U0001F3C4'),
        ('\U0001F3C6', '\U0001F3CA'),
        ('\U0001F3E0', '\U0001F3F0'),
        ('\U0001F400', '\U0001F43E'),
        ('\U0001F440', ),
        ('\U0001F442', '\U0001F4F7'),
        ('\U0001F4F9', '\U0001F4FC'),
        ('\U0001F500', '\U0001F53C'),
        ('\U0001F540', '\U0001F543'),
        ('\U0001F550', '\U0001F567'),
        ('\U0001F5FB', '\U0001F5FF')
    ],
    7: [
        ('\U0001F300', '\U0001F32C'),
        ('\U0001F330', '\U0001F37D'),
        ('\U0001F380', '\U0001F3CE'),
        ('\U0001F3D4', '\U0001F3F7'),
        ('\U0001F400', '\U0001F4FE'),
        ('\U0001F500', '\U0001F54A'),
        ('\U0001F550', '\U0001F579'),
        ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')
    ],
    8: [
        ('\U0001F300', '\U0001F579'),
        ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')
    ]
}

NO_NAME_ERROR = '(No name found for this codepoint)'


def get_random_emoji(unicode_version=6):
    if unicode_version in EMOJI_RANGES_UNICODE:
        emoji_ranges = EMOJI_RANGES_UNICODE[unicode_version]
    else:
        emoji_ranges = EMOJI_RANGES_UNICODE[-1]

    # Weighted distribution
    count = [ord(r[-1]) - ord(r[0]) + 1 for r in emoji_ranges]
    weight_distr = list(accumulate(count))

    # Get one point in the multiple ranges
    point = randrange(weight_distr[-1])

    # Select the correct range
    emoji_range_idx = bisect(weight_distr, point)
    emoji_range = emoji_ranges[emoji_range_idx]

    # Calculate the index in the selected range
    point_in_range = point
    if emoji_range_idx != 0:
        point_in_range = point - weight_distr[emoji_range_idx - 1]

    # Emoji 😄
    emoji = chr(ord(emoji_range[0]) + point_in_range)
    emoji_name = unicode_name(emoji, NO_NAME_ERROR).capitalize()
    emoji_codepoint = "U+{}".format(hex(ord(emoji))[2:].upper())

    return (emoji, emoji_codepoint, emoji_name)





def get_panel_desc(version):
    p = f'{get_random_emoji()[0]} Author: Lucas Jin\n' + \
        f'{get_random_emoji()[0]} Github: https://github.com/jinfagang/onnxexplorer, please star 🌟\n' + \
        f'{get_random_emoji()[0]} Version: {version}\n' + \
        f'{get_random_emoji()[0]} Since: 2021.10 \n' + \
        f'{get_random_emoji()[0]} Promote: onnxexp glance -m a.onnx'
    return p


def print_welcome_msg(version):
    console = Console()
    p = Panel(get_panel_desc(version),
            title=f'{get_random_emoji()[0]} Welcome to onnxexp! {get_random_emoji()[0]}', highlight=True, expand=True)
    console.print(p, width=90)
