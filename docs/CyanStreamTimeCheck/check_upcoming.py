"""
Tiny script to fetch Cyan's streaming date in various timezones.
"""


from urllib import request

import datetime
import itertools
import re
from typing import Tuple

from browser import document, html, window


started_time = datetime.datetime.now()
youtube_image_url = "https://i.ytimg.com/vi/{}/mqdefault.jpg"
# default, hqdefault, mqdefault, sddefault, maxresdefault + variants like maxresdefault_live


def get_timezone():
    """
    Get timezone using javascript function. Unfortunately without pytz I can't utilize this.
    """
    try:
        return window.Intl.DateTimeFormat().resolvedOptions().timeZone
    except AttributeError:
        return "Local test mode"


class VideoInfo:
    start_time_pattern = re.compile(r'scheduledStartTime"[^"]*"([^"]*)')
    title_pattern = re.compile(r'<title>([^"]*)</title>')

    def __init__(self, vid_id: str):
        ui.activity.text = f"Initializing VideoInfo for {vid_id}."

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

        # just even using re makes everything insanely slow in brython. Doing this mess to fix it
        split = "".join(line for line in self.html_text.split("\n") if "scheduledStartTime" in line)
        split = "".join(line for line in split.split("<") if "scheduledStartTime" in line)
        split = "".join(line for line in split.split(",") if "scheduledStartTime" in line)
        split = "".join(line for line in split.split("{") if "scheduledStartTime" in line)

        try:
            matched = self.start_time_pattern.search(split).group(1)
        except AttributeError:
            self.is_upcoming = False
            return datetime.datetime.fromtimestamp(0)

        return datetime.datetime.fromtimestamp(int(matched))

    def get_title(self):
        """
        Fetch stream title from video HTML.

        :return: stream name
        """

        # just even using re makes everything insanely slow. Doing this mess to fix it
        split = self.html_text.split("<title>")[-1]
        matched = split.split("</title>")[0]

        # matched = self.title_pattern.search(self.html_text).group(1)

        return matched.removesuffix(" - YouTube")


class UI:
    def __init__(self):

        self.main_div = html.DIV(id="Main")
        document <= self.main_div

        timezone_data = html.DIV(get_timezone(), id="timezone-info")
        self.streams_count_div = html.DIV("No upcoming streams found.", id="StreamsCount")
        self.activity = html.DIV("Loading scripts, please be patient.")
        self.refresh = html.A("Refresh", href=window.location.href)

        div = html.DIV()
        div <= timezone_data
        div <= self.refresh

        self.main_div <= div
        self.main_div <= self.activity
        self.main_div <= self.streams_count_div

        self.upcoming_div = html.DIV(Class="UpcomingVideoFeed")

        self.main_div <= self.upcoming_div

        self.streams_count = 0

    def insert_new_video(self, vid: VideoInfo):
        """
        Add new upcoming video to feed.

        :param vid: VideoInfo instance containing valid upcoming stream information.
        """

        ui.activity.text = f"Inserting new video {vid.vid_id}."

        image_link = youtube_image_url.format(vid.vid_id)

        img = html.IMG(Class="Thumbnail", src=image_link)
        link = html.A(vid.title, Class="VideoLink", href=vid.url, target="_blank", style={"display": "block"}, )

        date_string = vid.start_time.strftime("%Y-%m-%d %a - %I:%M %p")
        diff_string = f"{(vid.start_time - started_time).total_seconds() / 3600:.2} hr left"

        time_string = html.DIV(f"{date_string} / {diff_string}", Class="TimeString")

        table = html.TABLE(Class="entry")

        table <= html.TR(html.TD(img, rowspan=2) + link + html.TR(time_string))

        self.upcoming_div <= table

        self.streams_count += 1
        self.streams_count_div.text = f"{self.streams_count} upcoming streams found."

    def show_refresh_link(self):
        self.refresh.text = "refresh"


def get_html(query: str) -> str:
    """
    Fetches HTML from proxy
    :param query: url excluding youtube domain.
    :return: string of html data
    """

    ui.activity.text = f"Fetching html for {query}."
    try:
        req = request.urlopen(f"https://nyarukoishi.mooo.com/yt_proxy/{query}")
    except Exception as err:
        try:
            req = request.urlopen(f"https://nyarukoishi.mooo.com/yt_proxy_m/{query}")
        except Exception as err_:

            ui.activity.text = f"Got Error {err}. Make sure browser is in desktop mode!"
            raise err_ from err

    html_ = req.read()

    # If server has brain, it has to be utf8.
    try:
        data = html_.decode("utf8")
    except AttributeError:
        # It's already decoded!
        data = html_

    return data


def video_list(channel_id: str, max_results: int) -> Tuple[str, ...]:
    """
    List topmost `max_results` number of videos in channel.

    :param channel_id: Channel ID
    :param max_results: number of video to extract
    :return: Tuple of unique videos, ordered.
    """

    ui.activity.text = f"On video_list, param: {channel_id}, {max_results}."

    # Compile regex pattern
    pattern = re.compile(r'videoIds"[^"]*"([^"]*)')

    data = get_html("channel/" + channel_id)

    # candidates = "\n".join(tuple(line for line in data.split(",") if "videoIds" in line))
    # candidates = "\n".join(tuple(line for line in re.split(r"[,;\n\s>]", data) if "videoIds" in line))

    # just even using re makes everything insanely slow.
    split = "".join(line for line in data.split("\n") if "videoIds" in line)
    split = "".join(line for line in split.split("<") if "videoIds" in line)
    split = "".join(line for line in split.split(",") if "videoIds" in line)
    split = "".join(line for line in split.split("{") if "videoIds" in line)

    vid_ids = pattern.findall(split)

    # Fetch unique keys in appearing order, streams are likely to appear at top.
    return tuple(k for (k, v), _ in zip(itertools.groupby(vid_ids), range(max_results)))


ui = UI()


def main():
    """
    Main routine
    """

    vid_list = video_list("UC9wbdkwvYVSgKtOZ3Oov98g", 3)
    vid_instances = map(VideoInfo, vid_list)

    for vid_info in (vid for vid in vid_instances if vid):
        ui.insert_new_video(vid_info)

    ui.activity.text = ""

    ui.show_refresh_link()

main()
