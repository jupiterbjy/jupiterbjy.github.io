"""
As `# noinspection PyStatementEffect` on start of file did not stop pycharm
from showing "statement has no effect" warnings, I just added assert to
DOM assignments.
"""

import itertools
import random
import datetime
import calendar

from typing import Generator, Tuple
from browser import document, html


TARGET_YEAR = 2000

table = html.TABLE(id="main_table")
month_display = html.DIV("0", id="month_display")

date_input_field = html.INPUT(id="date_input_field")
refresh_td = html.TD("\u21BB", id="refresh", colspan=1)

dropdown_month = html.SELECT(html.OPTION(n + 1) for n in range(12))
dropdown_day = html.SELECT(html.OPTION(n + 1) for n in range(31))

assert document <= table
assert table <= html.TR(html.TD(month_display, colspan=7))

assert table <= html.TR(html.TD(day, id=f"day_{day}") for day in "日月火水木金土")
assert table <= (
    html.TR(html.TH(d + r * 7, id=f"cal_{d + r * 7}") for d in range(7))
    for r in range(6)
)

assert table <= html.TR(html.TD(dropdown_month + "月", colspan=1) +
                        html.TD(dropdown_day + "日", colspan=1))
assert table <= html.TR(html.TD(date_input_field, colspan=6) + refresh_td)


def date_translate_closure():
    month_dict = {
        "1": "いちがつ",
        "2": "にがつ",
        "3": "さんがつ",
        "4": "しがつ",
        "5": "ごがつ",
        "6": "ろくがつ",
        "7": "しちがつ",
        "8": "はちがつ",
        "9": "くがつ",
        "10": "じゅうがつ",
        "11": "じゅういちがつ",
        "12": "じゅうにがつ",
    }

    day_dict = {
        "1": "ついたち",
        "2": "ふつか",
        "3": "みっか",
        "4": "よっか",
        "5": "いつか",
        "6": "むいか",
        "7": "なのか",
        "8": "ようか",
        "9": "ここのか",
        "10": "とおか",
        "11": "じゅういちにち",
        "12": "じゅうににち",
        "13": "じゅうさんにち",
        "14": "じゅうよっか",
        "15": "じゅうごにち",
        "16": "じゅうろくにち",
        "17": "じゅうしちにち",
        "18": "じゅうはちにち",
        "19": "じゅうくにち",
        "20": "はつか",
        "21": "にじゅういちにち",
        "22": "にじゅうににち",
        "23": "にじゅうさんにち",
        "24": "にじゅうよっか",
        "25": "にじゅうごにち",
        "26": "にじゅうろくにち",
        "27": "にじゅうしちにち",
        "28": "にじゅうはちにち",
        "29": "にじゅうくにち",
        "30": "さんじゅうにち",
        "31": "さんじゅういちにち",
    }

    def inner(month, day):
        # also accept 01 sort of number strings, albeit not the case
        return month_dict[str(int(month))], day_dict[str(int(day))]

    return inner


date_translate = date_translate_closure()


def cell_iter_gen():
    """
    A generator to provide iteration interface for calender cells.
    """

    for n in range(42):
        yield document[f"cal_{n}"]


class CalenderWrapper:
    def __init__(self):
        self._gen_instance = self.create_new_main_gen()

    @property
    def date(self):
        return dropdown_day.selectedIndex + 1

    @date.setter
    def date(self, val):
        dropdown_day.selectedIndex = val - 1
        self.validate_n_fix_date()
        self.write_to_calender()

    @property
    def month(self):
        return dropdown_month.selectedIndex + 1

    @month.setter
    def month(self, val):
        dropdown_month.selectedIndex = val - 1
        self.validate_n_fix_date()
        self.write_to_calender()

    def set_new_random_date(self):
        """
        Sets new random date and update calender.
        """
        date_input_field.value = ""
        date_input_field.placeholder = "Type month & day in hiragana"

        month, date = next(date_gen_instance)

        self.month = month
        self.date = date

        self.write_to_calender()

    def create_new_main_gen(self):
        """
        Main loop. Obviously it's waste to run normal loop and look for user input.
        Instead using event loop so user signals code when to run.
        """

        def inner_gen():
            while True:
                self.set_new_random_date()

                while True:
                    yield

                    answer_month, answer_date = date_translate(self.month, self.date)
                    string = date_input_field.value

                    if answer_month in string and answer_date in string:
                        break

                    date_input_field.value = ""
                    date_input_field.placeholder = f"{answer_month} {answer_date}"

        gen = inner_gen()
        next(gen)
        return gen

    def progress(self):
        next(self._gen_instance)

    def validate_n_fix_date(self):
        """
        Will check date is within month range and fix if needed.

        :return: Will return True if date was wrong and performed fix, else False.
        """
        _, duration = calendar.monthrange(TARGET_YEAR, self.month)

        if self.date > duration:
            self.date = duration
            return True

        return False

    def write_to_calender(self):
        """
        Update calender to current values.
        Uses dumb and powerful erase-all-then-write way, for simplicity.
        """

        month = self.month
        date = self.date

        month_display.text = f"{month}月"

        start_date, duration = calendar.monthrange(TARGET_YEAR, month)

        # Converting mon-sun to sun-sat
        start_date = start_date + 1 if start_date != 6 else 0

        for cell in cell_iter_gen():
            cell.text = "\u2800"
            cell.removeAttribute("style")

        for idx, cell in enumerate(
                itertools.islice(cell_iter_gen(), start_date, start_date + duration), 1
        ):
            cell.text = idx
            cell.style = {
                "background-color": "#efefef"
            }

        document[f"cal_{start_date + date - 1}"].style = {
            "background-color": "#55CA5A"
        }


def date_gen_closure() -> Generator[Tuple[int, int], None, None]:
    """
    Instantiate random date generator.

    :return Generator instance.
    """

    start_time = int(datetime.datetime.strptime(f"{TARGET_YEAR}-01-01", "%Y-%m-%d").timestamp())
    end_time = int(datetime.datetime.strptime(f"{TARGET_YEAR}-12-31", "%Y-%m-%d").timestamp())

    def inner_date_gen():
        nonlocal start_time, end_time

        while True:
            date = datetime.datetime.fromtimestamp(
                random.randint(start_time, end_time)
            ).date()

            yield date.month, date.day

    return inner_date_gen()


date_gen_instance = date_gen_closure()


def keypress(event):
    """
    Keypress event handler, will only react to 13 which is enter.

    :param event: event object, passed by brython.
    """

    if event.keyCode == 13:
        main_instance.progress()
        date_input_field.clear()

    event.stopPropagation()


def trigger_refresh(event):
    """
    Set new random dates and update calender.

    :param event: event object, passed by brython.
    """

    main_instance.set_new_random_date()
    event.stopPropagation()


def set_date(event):
    """
    Sets specific date.
    Day might change to compensate for length difference between months.

    :param event: event object, passed by brython.
    """

    dropdown = event.target
    main_instance.date = dropdown.selectedIndex + 1
    event.stopPropagation()


def set_month(event):
    """
    Sets specific Month.
    Day might change to compensate for length difference between months.

    :param event: event object, passed by brython.
    """

    dropdown = event.target
    main_instance.month = dropdown.selectedIndex + 1
    event.stopPropagation()


date_input_field.bind("keyup", keypress)
refresh_td.bind("click", trigger_refresh)
dropdown_day.bind("change", set_date)
dropdown_month.bind("change", set_month)

main_instance = CalenderWrapper()
