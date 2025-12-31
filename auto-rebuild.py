"""
Because pycharm's own html preview feature is broken and can't even load fonts in CSS,
we doin' it manually
"""

import pathlib

import trio
from selenium import webdriver

from watchdog_file_events_m import start_watchdog, FileSystemEvent
from dumb_trio_server_O import serve_files
import build


# --- Config ---

ROOT = pathlib.Path(__file__).parent

WATCH_DIRS = {
    ROOT / "html_parts",
    ROOT / "md_pages",
}
SERVE_DIR = ROOT / "docs"

REFRESH_MIN_INTERVAL = 1

ADDR = "127.0.0.1"
PORT = 8000
URL = f"http://{ADDR}:{PORT}/"


# --- Utilities ---


class ANSI:
    """Some colorful ANSI printer"""

    _table = {
        "RED": "\x1b[31m",
        "GREEN": "\x1b[32m",
        "YELLOW": "\x1b[33m",
        "": "",
    }
    _end = "\x1b[0m"

    @classmethod
    def print(cls, *args, color="", sep=" ", **kwargs):
        """Colored print"""

        print(f"{cls._table[color]}{sep.join(args)}{cls._end}", **kwargs)


def refresh_all_tabs(wd: webdriver.Firefox):
    """Refreshes all selenium tabs"""

    # cur_handle = wd.current_window_handle

    for handle in wd.window_handles:
        wd.switch_to.window(handle)
        wd.refresh()

    # wd.switch_to.window(cur_handle)


# --- Logics ---


async def main():

    # TODO: use either loguru or copy logging setting from my other repo

    build.main()

    ANSI.print("Starting webdriver", color="YELLOW")
    driver = webdriver.Firefox()
    ANSI.print("Webdriver started", color="GREEN")

    update_required = []

    with start_watchdog(ROOT, True) as handler:

        def on_update(event: FileSystemEvent):
            # nonlocal update_required

            parents = set(pathlib.Path(event.src_path).parents)

            if not any(parents & WATCH_DIRS):
                return

            ANSI.print(
                f"Reloading required due to {event.__class__.__name__} at {event.src_path}",
                color="YELLOW",
            )

            update_required.append(None)

        handler.register_global(on_update)

        async with trio.open_nursery() as nursery:

            # proc: trio.Process = await nursery.start(
            #     partial(trio.run_process, "python3 -m http.server", cwd=SERVE_DIR)
            # )
            # print(f"Server started at {URL}")
            nursery.start_soon(serve_files, SERVE_DIR)

            # since it blocks server startup has to be delegated
            await trio.to_thread.run_sync(driver.get, URL)

            try:
                while True:
                    await trio.sleep(REFRESH_MIN_INTERVAL)

                    if update_required:
                        ANSI.print("Rebuilding site", color="YELLOW")
                        build.main()

                        ANSI.print("Reloading page", color="YELLOW")
                        await trio.to_thread.run_sync(refresh_all_tabs, driver)

                        ANSI.print("Update done!", color="GREEN")
                        update_required.clear()

            except KeyboardInterrupt:
                ANSI.print("Stopping webdriver (may take a while)", color="YELLOW")
                driver.quit()
                ANSI.print("Webdriver stopped", color="GREEN")

                nursery.cancel_scope.cancel()


# --- Drivers ---

if __name__ == "__main__":
    try:
        trio.run(main)
        # trio.run(serve_files, SERVE_DIR)
    except KeyboardInterrupt:
        exit(1)
