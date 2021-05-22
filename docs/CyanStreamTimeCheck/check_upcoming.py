"""
Tiny script to fetch Cyan's streaming date in various timezones.
"""


from urllib import request

import datetime
import itertools
import re
from typing import Tuple

from browser import document, html, window


youtube_image_url = "https://i.ytimg.com/vi/{}/hqdefault.jpg"
# default, hqdefault, mqdefault, sddefault, maxresdefault + variants like maxresdefault_live


def get_timezone():
    return window.Intl.DateTimeFormat().resolvedOptions().timeZone


class VideoInfo:
    start_time_pattern = re.compile(r'scheduledStartTime"[^"]*"([^"]*)')
    title_pattern = re.compile(r'<title>([^"]*)</title>')

    def __init__(self, vid_id: str):

        self.vid_id = vid_id
        self.url = f"https://www.youtube.com/watch?v={vid_id}"
        self.html_text = get_html("watch?v=" + vid_id)

        self.is_upcoming = True

        self.start_time = self.get_timestamp()
        self.title = self.get_title()

    def __bool__(self):
        return self.is_upcoming

    def get_timestamp(self) -> datetime.datetime:
        """
        Fetch scheduled stream timestamp from video HTML.
        Will replace this method on it's own after first call.

        :return: timestamp
        """

        try:
            matched = self.start_time_pattern.search(self.html_text).group(1)
        except AttributeError:
            self.is_upcoming = False
            return datetime.datetime.fromtimestamp(0)

        return datetime.datetime.fromtimestamp(int(matched))

    def get_title(self):
        """
        Fetch stream title from video HTML.

        :return: stream name
        """

        matched = self.title_pattern.search(self.html_text).group(1)
        return matched.removesuffix(" - YouTube")


class UI:
    def __init__(self):

        self.main_div = html.DIV(id="Main")
        assert document <= self.main_div

        timezone_data = html.DIV(get_timezone(), id="timezone-info")
        self.streams_count_div = html.DIV("No upcoming streams found.", id="timezone-info")

        assert self.main_div <= timezone_data
        assert self.main_div <= self.streams_count_div

        self.upcoming_div = html.DIV(className="UpcomingVideoFeed")

        assert self.main_div <= self.upcoming_div

        self.streams_count = 0

    def insert_new_video(self, vid: VideoInfo):

        image_link = youtube_image_url.format(vid.vid_id)

        img = html.IMG(className="Thumbnail", src=image_link)
        link = html.LINK(vid.title, className="VideoLink",href=vid.url)
        start_time = html.DIV(vid.start_time.strftime("%Y-%m-%d %a - %I:%M %p"), className="TimeString")

        table = html.TABLE(html.TR(html.TD(img, rowspan=2)), html.TR(link), html.TR(start_time))

        assert self.upcoming_div <= table

        self.streams_count += 1
        self.streams_count_div.text = f"{self.streams_count} upcoming streams found."


def get_html(query: str) -> str:
    req = request.urlopen(f"https://nyarukoishi.mooo.com/yt_proxy/{query}")

    # If server has brain, it has to be utf8.
    data = req.read().decode("utf8")
    return data


def video_list_gen(channel_id: str, max_results: int) -> Tuple[str, ...]:

    # Compile regex pattern
    pattern = re.compile(r'videoIds"[^"]*"([^"]*)')

    while True:
        vid_ids = pattern.findall(get_html("channel/" + channel_id))

        # Fetch unique keys in appearing order, streams are likely to appear at top.
        yield tuple(k for (k, v), _ in zip(itertools.groupby(vid_ids), range(max_results)))


def main():

    ui = UI()

    vid_list = video_list_gen("UC9wbdkwvYVSgKtOZ3Oov98g", 3)
    vid_instances = map(VideoInfo, vid_list)

    for vid_info in (vid for vid in vid_instances if vid):
        ui.insert_new_video(vid_info)


main()
