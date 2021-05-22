"""
Widget to practice time.
"""

import datetime
import itertools
from typing import Generator, Tuple

from browser import document, html


HOUR = "時"
MINUTE = "分"


class UIWrapper:
    def __init__(self):

        # Generating UI

        main_div = html.DIV(id="TimePractise")
        assert document <= main_div

        table = html.TABLE(id="time_main_table")
        assert main_div <= table

        self.hour_dropdown = html.SELECT(html.OPTION(n) for n in range(1, 13))
        self.min_dropdown = html.SELECT(html.OPTION(n) for n in range(60))
        self.am_pm_dropdown = html.SELECT(html.OPTION(merid) for merid in ("AM", "PM"))

        assert table <= html.TR(self.hour_dropdown + ":" + self.min_dropdown + " " + self.am_pm_dropdown, colspan=7)

        self.refresh_td = html.TD("\u21BB", colspan=1)
        self.input_field = html.INPUT(id="time_input_field")
        assert table <= html.TR(html.TD(self.input_field, colspan=6) + self.refresh_td)


ui_element = UIWrapper()


def time_translate_closure():
    hour_dict = {
        "1": "いちじ",
        "2": "にじ",
        "3": "さんじ",
        "4": "よじ",
        "5": "ごじ",
        "6": "ろくじ",
        "7": "しちじ",
        "8": "はちじ",
        "9": "くじ",
        "10": "じゅうじ",
        "11": "じゅういちじ",
        "12": "じゅうにじ",
    }

