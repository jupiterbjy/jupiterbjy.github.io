import itertools
import random
import datetime
import calendar

from browser import document, html
from browser.widgets.dialog import InfoDialog


table = html.TABLE(id="main_table")
document <= table

month_display = html.DIV("0", id="month_display")
table <= html.TR(html.TD(month_display, colspan=7))

table <= html.TR(html.TD(day, id=f"day_{day}") for day in "日月火水木金土")
table <= (html.TR(html.TH(d + r * 7, id=f"cal_{d + r * 7}") for d in range(7)) for r in range(6))

info_label = html.LABEL()
table <= html.TR(html.TD(info_label, colspan=6))

date_input_field = html.INPUT(id="date_input_field")
refresh_td = html.TD("\u21BB", id="refresh", colspan=1)
table <= html.TR(html.TD(date_input_field, colspan=6) + refresh_td)


def date_gen_closure():
    start_time = int(datetime.datetime.strptime("2000-01-01", "%Y-%m-%d").timestamp())
    end_time = int(datetime.datetime.strptime("2001-12-31", "%Y-%m-%d").timestamp())

    def get_month_detail(month_):
        """
        Returns first day and duration of given month.
        0-6 represents sun-sat.

        :param month_: month
        :return: first day of the week and duration of given month.
        """

        start_, duration_ = calendar.monthrange(2000, month_)
        return (start_ + 1 if start_ != 6 else 0), duration_

    def cell_iter_gen():
        for n in range(42):
            yield document[f"cal_{n}"]

    def inner_date_gen():
        nonlocal start_time, end_time

        while True:
            date = datetime.datetime.fromtimestamp(random.randint(start_time, end_time)).date()

            start_date, duration = get_month_detail(date.month)

            for cell in cell_iter_gen():
                cell.text = "\u2800"
                cell.removeAttribute("style")

            for idx, cell in enumerate(itertools.islice(cell_iter_gen(), start_date, start_date + duration), 1):
                cell.text = idx

            document[f"cal_{start_date + date.day}"].style = {"background-color": "#55CA5A"}

            yield date.month, date.day

    return inner_date_gen()


date_gen = date_gen_closure()


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
        "12": "じゅうにがつ"
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
        "31": "さんじゅういちにち"
    }

    def inner(month, day):
        return month_dict[str(month)], day_dict[str(day)]

    return inner


date_translate = date_translate_closure()


def check_answer(input_, answer):
    for part in answer:
        if part in input_:
            continue

        break

    else:
        return True

    return False


def main_gen():
    while True:
        month, day = next(date_gen)
        answer = date_translate(month, day)

        month_display.text = f"{month}月"
        info_label.text = "Type month and day in hiragana"
        yield

        while not check_answer(date_input_field.value, answer):
            info_label.text = f"{month}月 {day}日: {answer[0]}  {answer[1]}"
            yield


gen_instance = main_gen()
next(gen_instance)


def keypress(event):
    # Enter = 13
    print(event.keyCode)
    if event.keyCode == 13:
        next(gen_instance)
        date_input_field.value = ""

    event.stopPropagation()


def trigger_refresh(event):
    global gen_instance
    gen_instance = main_gen()
    next(gen_instance)
    event.stopPropagation()


date_input_field.bind("keyup", keypress)
refresh_td.bind("click", trigger_refresh)
