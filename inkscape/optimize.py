"""
Script for scour optimization (which seems to be used in Inkscape)

This is python purely because I'm lazy to write shell scripts per OS
"""

import pathlib

from scour import scour

ROOT = pathlib.Path(__file__).parent

DEST_PATHS: list[pathlib.Path] = [
    # ROOT.parent / "docs" / "_optimized_svg",
    ROOT.parent
    / "html_parts"
    / "_optimized_svg"
]

ARGS = """
-i src -o dest --enable-viewboxing --enable-id-stripping --enable-comment-stripping --shorten-ids --indent=none
""".strip().split()


def run(src: pathlib.Path, dest: pathlib.Path):
    """Wrapper for scour since it doesn't support running as module"""

    args = ARGS.copy()
    args[1] = src.as_posix()
    args[3] = dest.as_posix()

    options = scour.parse_args(args)
    scour.start(options, *scour.getInOut(options))


def main():
    for p in DEST_PATHS:
        p.mkdir(parents=True, exist_ok=True)

    for p in ROOT.glob("*.svg"):
        fn = f"{p.stem}.svg"

        optim_p = DEST_PATHS[0] / fn
        run(p, optim_p)

        _bytes = optim_p.read_bytes()

        # duplicate rest to other dir
        for dest_p in DEST_PATHS[1:]:
            (dest_p / fn).write_bytes(_bytes)


if __name__ == "__main__":
    main()
