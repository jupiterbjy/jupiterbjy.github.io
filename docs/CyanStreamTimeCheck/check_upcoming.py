from urllib import request
import itertools
import re


def get_html(channel_id: str):
    req = request.urlopen(f"https://www.youtube.com/channel/{channel_id}")
    data = req.read().decode("utf8")
    return data


def video_list_gen(channel_id: str, max_results: int):

    # Compile regex pattern
    pattern = re.compile(r'videoIds"[^"]*"([^"]*)')

    while True:
        vid_ids = pattern.findall(get_html(channel_id))

        # Fetch unique keys in appearing order, streams are likely to appear at top.
        yield tuple(k for (k, v), _ in zip(itertools.groupby(vid_ids), range(max_results)))


print(get_html("UC9wbdkwvYVSgKtOZ3Oov98g"))
