"""
Because pycharm's own html preview feature is broken and can't even load fonts in CSS,
we doin' it manually.

Currently using dumb method to trunc dest path & copying all existing resources again,
so if you use ramdisk
"""

import pathlib

import trio
from selenium import webdriver

from watchdog_file_events_m import *
from dumb_trio_server_O import serve_files
import build


# --- Config ---

ROOT = pathlib.Path(__file__).parent

WATCH_DIRS = {
    ROOT / "html_parts",
    ROOT / "md_pages",
}
SERVE_DIR = ROOT / "docs"

## Used to ignore files & dirs with this suffix, e.g. `much_wow.py~`
IGNORE_SUFFIX = "~"

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


def register_handlers(handler: CustomHandler):

    src_roots = {ROOT / "html_parts", ROOT / "md_pages"}

    def get_dirs(str_path: str) -> tuple[pathlib.Path | None, pathlib.Path | None]:
        """Just a terribly named syntax sugar to reduce writing same thing 8 times.

        Returns:
            (file path, parent src root) - (None, None) if not within src roots
        """

        path = pathlib.Path(str_path)
        parent = set(path.parents) & src_roots
        return (path, parent.pop()) if parent else (None, None)

    def remove_empty_dirs_in_dest():
        # too lazy to manually reverse-traverse so gonna do this way

        for root, _dn, _fn in SERVE_DIR.walk(top_down=False):
            if root == SERVE_DIR:
                return

            if len(_dn) + len(_fn):
                continue

            root.rmdir()

    def file_created_or_modified(event: FileSystemEvent):
        path, parent = get_dirs(event.src_path)

        if parent:
            src_path = parent
            dest_path = SERVE_DIR / path.relative_to(src_path)
            src_path.copy(dest_path, preserve_metadata=True)

    handler.register_on_file_creation(file_created_or_modified)
    handler.register_on_file_modification(file_created_or_modified)

    def file_deleted(event: FileSystemEvent):
        path, parent = get_dirs(event.src_path)

        if parent:
            dest_path = SERVE_DIR / path.relative_to(parent)
            dest_path.unlink(missing_ok=True)

            remove_empty_dirs_in_dest()

    handler.register_on_file_deletion(file_deleted)

    def file_moved(event: FileSystemEvent):
        src_path, src_parent = get_dirs(event.src_path)
        moved_path, moved_parent = get_dirs(event.dest_path)

        if src_parent and moved_parent:
            dest_src = SERVE_DIR / src_path.relative_to(src_parent)
            dest_moved = SERVE_DIR / moved_path.relative_to(moved_parent)

            if dest_src != dest_moved:
                dest_src.move(dest_moved)

                remove_empty_dirs_in_dest()

    handler.register_on_file_move(file_moved)


# --- Drivers ---


async def main():

    # TODO: use either loguru or copy logging setting from my other repo

    build.main()

    ANSI.print("Starting webdriver", color="YELLOW")
    driver = webdriver.Firefox()
    ANSI.print("Webdriver started", color="GREEN")

    # should be fine for race condition
    update_required = False

    def on_update(event: FileSystemEvent):
        nonlocal update_required

        eff_path = event.dest_path if event.dest_path else event.src_path

        if not eff_path[-1] != IGNORE_SUFFIX:
            update_required = True

    with start_watchdog(WATCH_DIRS, True) as handler:

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
                        update_required = False

            except KeyboardInterrupt:
                ANSI.print("Stopping webdriver (may take a while)", color="YELLOW")
                driver.quit()
                ANSI.print("Webdriver stopped", color="GREEN")

                nursery.cancel_scope.cancel()


if __name__ == "__main__":
    try:
        trio.run(main)
        # trio.run(serve_files, SERVE_DIR)
    except KeyboardInterrupt:
        exit(1)
