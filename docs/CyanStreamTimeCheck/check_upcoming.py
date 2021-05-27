"""
Tiny script to fetch streamer - especially cyan's - streaming time.
Video embedding must be enabled to show on channel feed.
"""


from urllib import request
from functools import reduce
import operator
import datetime
import itertools
import json
from typing import Tuple, List, Union

from browser import document, html, window, aio


DEBUG = True

# Limits number of videos to check in channel
FETCH_LIM = 3

# ID of your favorite channel
CHANNEL_ID = "UC9wbdkwvYVSgKtOZ3Oov98g"

# Proxy source, and queries for youtube. Proxy server should return json.
# PROXY_SOURCE = "https://yt-data.cyannyan.workers.dev/"
PROXY_SOURCE = "https://nyarukoishi.mooo.com/yt_proxy/"
# VIDEO_QUERY = "video/"
VIDEO_QUERY = "watch?v="
CHANNEL_QUERY = "channel/"

# Pre-determined keys for returned json objects.
SCHEDULED_TIME_KEY = (
    "playabilityStatus",
    "liveStreamability",
    "liveStreamabilityRenderer",
    "offlineSlate",
    "liveStreamOfflineSlateRenderer",
    "scheduledStartTime",
)
UPCOMING_KEY = ("videoDetails", "isUpcoming")
LIVE_KEY = ("videoDetails", "isLive")
DESCRIPTION_KEY = ("videoDetails", "shortDescription")
TITLE_KEY = ("videoDetails", "title")

# Separator(start_delimiter, end_delimiter) for actual description to exclude boilerplate.
SEPARATORS = ("", "\n────")
DESCRIPTION_LIMIT = 200

# Youtube image format
# default, hqdefault, mqdefault, sddefault, maxresdefault + variants like maxresdefault_live
YT_IMAGE_URL = "https://i.ytimg.com/vi/{}/mqdefault.jpg"


def debugging_closure():
    """
    Simply determines whether to output on activity or not.

    :return: log function
    """
    if DEBUG:

        def inner(message):
            ui.activity.text = message
            print(message)

    else:

        def inner(message):
            print(message)

    return inner


log = debugging_closure()


def get_timezone():
    """
    Get timezone using javascript function. Unfortunately without pytz I can't utilize this.
    """
    try:
        return window.Intl.DateTimeFormat().resolvedOptions().timeZone
    except AttributeError:
        return "Local test mode"


def find_key(key, dict_: dict) -> Union[List[str], None]:
    """
    Simple recursive function to figure out what key I need. Only used in development.
    key list globals was generated by this.
    :param key: key of interest
    :param dict_: json parsed dictionary
    :return: list of keys in sequence. Returns None if nothing is found.
    """
    for k, v in dict_.items():
        try:
            flattened = json.dumps(v)
        except TypeError:
            flattened = str(v)

        if isinstance(v, dict) and key in flattened:
            nested = find_key(key, v)

            if None in nested:
                continue

            return [k] + nested

        if k == key:
            return [k]

    return None


def format_description(description: str):
    """
    Separates actual descriptions using SEPARATORS global variable.
    """

    # Separate actual descriptions
    if SEPARATORS[0]:
        description = description.split(SEPARATORS[0])[-1]

    if SEPARATORS[1]:
        description = description.split(SEPARATORS[1])[0]

    if len(description) > DESCRIPTION_LIMIT:
        description = description[: DESCRIPTION_LIMIT - 3] + "..."

    return description.strip("\n")


class VideoInfo:
    """
    Class that holds bare minimum information of video.
    """

    # start_time_pattern = re.compile(r'scheduledStartTime"[^"]*"([^"]*)')
    # title_pattern = re.compile(r'<title>([^"]*)</title>')

    def __init__(self, vid_id: str, json_data: dict):
        log(f"Initializing VideoInfo for {vid_id}.")

        self.vid_id = vid_id
        self.url = f"https://www.youtube.com/watch?v={vid_id}"

        self.json_parsed = json_data

        # No need to check both but for convenience.
        self.is_live = self.get_live_status()
        self.is_upcoming = self.get_upcoming_status()

        if self.is_live or self.is_upcoming:
            self.start_time = self.get_timestamp()
            self.title = self.get_title()
            self.description = self.get_description()

    def __bool__(self):
        return self.is_upcoming or self.is_live

    def get_live_status(self) -> bool:
        """
        Fetch live status.

        :return: True if upcoming, else False.
        """

        # LIVE_STREAM_OFFLINE
        try:
            return reduce(operator.getitem, LIVE_KEY, self.json_parsed)
        except KeyError:
            return False

    def get_upcoming_status(self) -> bool:
        """
        Fetch upcoming status.

        :return: True if upcoming, else False.
        """

        try:
            # In this script all reduce part is showing error, but this is expected. It's not error.
            return reduce(operator.getitem, UPCOMING_KEY, self.json_parsed)
        except KeyError:
            return False

    def get_timestamp(self) -> Union[datetime.datetime, bool]:
        """
        Fetch scheduled stream timestamp from video HTML.
        Will replace this method on it's own after first call.

        :return: timestamp
        """

        try:
            return datetime.datetime.fromtimestamp(
                int(reduce(operator.getitem, SCHEDULED_TIME_KEY, self.json_parsed))
            )
        except KeyError:
            return False

    def get_title(self):
        """
        Fetch stream title from video HTML.

        :return: stream name
        """

        return reduce(operator.getitem, TITLE_KEY, self.json_parsed)

    def get_description(self):
        """
        Fetch stream descriptions from video HTML.

        :return: string
        """

        return format_description(
            reduce(operator.getitem, DESCRIPTION_KEY, self.json_parsed)
        )


class UI:
    def __init__(self):
        # Building UI

        self.main_div = html.DIV(id="Main")
        assert document <= self.main_div

        timezone_data = html.DIV(get_timezone(), Class="top_line")
        self.streams_count_div = html.DIV(
            "No upcoming streams found.", id="StreamsCount"
        )

        div = html.DIV()
        assert div <= timezone_data

        # For local testing
        try:
            self.refresh = html.A("Refresh", href=window.location.href, Class="top_line")
            trouble_shoot = html.A(
                "Stream isn't showing up",
                target="_blank",
                href="https://smashballoon.com/doc/my-upcoming-live-stream-is-not-showing-up-in-the-feed-or-wont-play-on-my-site/",
                Class="top_line"
            )
        except AttributeError:
            pass
        else:
            assert div <= self.refresh
            assert div <= trouble_shoot

        self.activity = html.DIV("Loading scripts, please be patient.")

        assert self.main_div <= div
        assert self.main_div <= self.activity
        assert self.main_div <= self.streams_count_div

        self.upcoming_div = html.DIV(Class="UpcomingVideoFeed")

        assert self.main_div <= self.upcoming_div

        self.streams_count = 0

    def insert_new_video(self, vid: VideoInfo):
        """
        Add new upcoming video to feed.

        :param vid: VideoInfo instance containing valid upcoming stream information.
        """

        log(f"Inserting new video {vid.vid_id}.")

        image_link = YT_IMAGE_URL.format(vid.vid_id)

        img = html.IMG(Class="Thumbnail", src=image_link)
        img_link = html.A(href=vid.url, target="_blank")

        assert img_link <= img

        link = html.A(
            vid.title,
            Class="VideoLink",
            href=vid.url,
            target="_blank",
            style={"display": "block"},
        )

        if vid.is_live:
            time_string = html.DIV("Already live", Class="TimeString LiveString")
        else:
            date_string = vid.start_time.strftime("%Y-%m-%d %a - %I:%M %p")
            diff_string = f"{round((vid.start_time - started_time).total_seconds() / 3600, 1)} hr left"

            time_string = html.DIV(f"{date_string} / {diff_string}", Class="TimeString")

        table = html.TABLE(Class="live" if vid.is_live else "upcoming")

        assert table <= html.TR(
            html.TD(img_link, rowspan=3) + html.TR(link) + html.TR(time_string) + html.TR(vid.description)
        )

        assert self.upcoming_div <= table

        self.streams_count += 1
        self.streams_count_div.text = f"{self.streams_count} upcoming streams found."

    def show_refresh_link(self):
        self.refresh.text = "Refresh"


async def get_html(query: str) -> str:
    """
    Fetches HTML from proxy.

    :param query: url excluding youtube domain.
    :return: string of html data
    """

    log(f"Fetching html for {query}.")

    try:
        req = await aio.ajax("GET", PROXY_SOURCE + query)

    except Exception as err:

        print(f"Fatal Failure! url was {PROXY_SOURCE + query}")
        log(
            f"Got Error {err}. Make sure browser is in desktop mode, "
            f"Or if already on desktop mode, please report this back to jupiterbjy."
        )
        raise

    html_ = req.data

    # If server has brain, it has to be utf8.
    try:
        data = html_.decode("utf8")
    except AttributeError:
        # It's already decoded!
        data = html_

    return data


async def video_list(channel_id: str, max_results: int) -> Tuple[str, ...]:
    """
    List topmost `max_results` number of videos in channel.

    :param channel_id: Channel ID
    :param max_results: number of video to extract
    :return: Tuple of unique videos, ordered.
    """

    log(f"On video_list, param: {channel_id}, {max_results}.")

    data = await get_html(CHANNEL_QUERY + channel_id)

    # Compile regex pattern
    # pattern = re.compile(r'videoIds"[^"]*"([^"]*)')

    def inner_gen():
        for sep in (sep_ for sep_ in data.split("listService") if "videoIds" in sep_):
            for part in (sep_ for sep_ in sep.split(",") if "videoIds" in sep_):
                yield part.split(":")[-1].strip('"[]{}')

    # Fetch unique keys in appearing order, streams are likely to appear at top.
    return tuple(
        k for (k, v), _ in zip(itertools.groupby(inner_gen()), range(max_results))
    )


def extract_json_from_yt_ch(html_data: str):

    data = html_data.split("ytInitialData = ")[-1].split(";")[0]


async def task(vid_id: str):
    """
    Task coroutine to be ran asynchronously.

    :param vid_id: id of video
    """
    global counter

    log(f"Task {vid_id} spawned.")

    try:
        html_data = await get_html(VIDEO_QUERY + vid_id)
        log(f"Received {len(html_data)}")

        # Testing if received data is valid
        assert html_data

    except Exception as err:
        message = (
            f"Task {vid_id} Exception - Missing CORS header / Detail: {err}.\n"
            f"Try refreshing browser manually."
        )
        log(message)

        ui.upcoming_div.text = message

    else:
        # check if it's html or json
        try:
            parsed = json.loads(html_data)
        except Exception:
            log("Received non-json data, attempting to extract.")

            try:
                extracted = (
                    html_data.split("ytInitialPlayerResponse =")[-1]
                    .split("</script>")[0]
                    .split(";var")[0]
                )

                log(f"Fetched {len(extracted)}")

                print(extracted)

                parsed = json.loads(extracted)
            except Exception:
                log("Complete failure fetching json!")
                return

        vid_info = VideoInfo(vid_id, parsed)

        if vid_info:
            ui.insert_new_video(vid_info)
            log(f"Task {vid_id} inserting new video")

        else:
            log(f"Task {vid_id} got non-upcoming stream.")

    log(f"Task {vid_id} finished.")
    counter -= 1

    await cleanup()


async def cleanup():
    if not counter:
        ui.activity.text = ""
        ui.show_refresh_link()


async def main():
    """
    Main routine
    """

    vid_list = await video_list(CHANNEL_ID, FETCH_LIM)
    log(vid_list)

    for vid_id in vid_list:
        aio.run(task(vid_id))


ui = UI()
counter = FETCH_LIM
started_time = datetime.datetime.now()
aio.run(main())
