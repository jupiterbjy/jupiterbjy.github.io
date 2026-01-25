"""
Builds very specific site from Markdown files in prehistoric way.

Synchronized file & directories between build destination & source, without overwriting files.

```text
=== Copying dependencies ===
f+ 0 / f- 9 / d+ 0 / d- 0
=== Building Start ===
  Building md_pages/index.md -> docs/index.html
   Building md_pages/about/index.md -> docs/about/index.html
   Building md_pages/posts/index.md -> docs/posts/index.html
    Building md_pages/posts/2021-03-02-feature_test/index.md -> docs/posts/2021-03-02-feature_test/index.html
   Building md_pages/projects/index.md -> docs/projects/index.html
    Building md_pages/projects/3d_print/index.md -> docs/projects/3d_print/index.html
    Building md_pages/projects/coding/index.md -> docs/projects/coding/index.html
    Building md_pages/projects/pc_hardware/index.md -> docs/projects/pc_hardware/index.html
    Building md_pages/projects/scribble/index.md -> docs/projects/scribble/index.html
```

:Author: jupiterbjy@gmail.com
"""

import datetime
import re
import pathlib
import bisect
from string import Template
from typing import TypedDict

# from datetime import datetime

from markdown_it import MarkdownIt

from periodic_dir_sync_O import multi_src_sync_dir, print_changes


# --- Config ---

ENCODING = "utf8"

ROOT = pathlib.Path(__file__).parent

DEST_ROOT = ROOT / "docs"

# HTML Body parts, e.g. header & footer
HTML_PARTS_ROOT = ROOT / "html_parts"
HTML_PARTS: dict[str, str] = {}

# MD Pages
MD_PAGE_ROOT = ROOT / "md_pages"

# Sync ignored file extensions
SYNC_EXCLUDED_EXTS = {".html", ".md"}
# SYNC_EXCLUDED_EXTS = {".html", ".md", ".py"}

# KEYWORD_PREFIX = "<!-- include "
# INCLUDE_RE = re.compile(r"^<!-- include (\S*) -->$")

# TITLE_PREFIX = "<!-- title "
# TITLE_RE = re.compile(r"^<!-- title ([\S\s]*) -->$")

DOC_HEADER_RE = re.compile(r"^<!-- HEADER\n([\S\s]*?)\n-->")

DOC_LISTING_RE = re.compile(r"\n<!-- LIST\s([\S\s]*?)\s-->")

# If dir starts with this prefix, it won't be listed when generating listing within post.
LISTING_IGNORED_DIR_PREFIX = "_"

LISTING_FORMAT = "### [{title}]({url}) / {date}\n"


# --- Utilities ---


def reload_html_parts():
    """Reload global html parts"""

    HTML_PARTS.clear()
    HTML_PARTS.update(
        {p.name: p.read_text(ENCODING) for p in (ROOT / "html_parts").glob("*.html")}
    )


def print_tree(path: pathlib.Path):
    """Prints given directory. Used for debugging"""

    for root, dirs, files in path.walk():

        depth_pad = " " * len(root.relative_to(path).parents)

        for name in files:
            print(depth_pad, (root / name).name, sep="")

        for name in dirs:
            print(depth_pad, (root / name).name, sep="")


def remove_tree(path: pathlib.Path):
    """Purges given directory"""

    for root, dirs, files in path.walk(top_down=False):
        for name in files:
            (root / name).unlink()

        for name in dirs:
            (root / name).rmdir()


def render_blank_link(self, tokens, idx, options, env):
    """Render rule for Markdown links to open in new tab

    References:
        https://markdown-it-py.readthedocs.io/en/latest/using.html#renderers
    """

    tokens[idx].attrSet("target", "_blank")
    tokens[idx].attrSet("rel", "noopener noreferrer")
    return self.renderToken(tokens, idx, options, env)


class DocHeader(TypedDict):
    title: str
    date: datetime.datetime | None
    layout: str
    tags: list[str]
    plugins: list[str]


def doc_header_parser(matched_str: str) -> DocHeader:
    """Parses header content from matched string"""

    result = DocHeader(title="", date=None, layout="post", tags=[], plugins=[])

    for line in matched_str.splitlines():
        try:
            key, val = map(str.strip, line.split(":", maxsplit=1))

        except ValueError:
            # probably no value specified e.g. (`plugins:` then empty)
            print(f"Ignoring invalid key: {line}")
            continue

        match key:
            case "title":
                result["title"] = val

            case "date":
                try:
                    result["date"] = datetime.datetime.fromisoformat(val)
                except ValueError:
                    print(f"Failed to parse date string '{val}'")

            case "layout":
                result["layout"] = val

            case "tags":
                result["tags"].extend(map(str.strip, val.split(" ")))

            case "plugins":
                if val:
                    result["plugins"].extend(map(str.strip, val.split(" ")))

    return result


def replace_listing(raw_html: str, current_dir: pathlib.Path) -> str:
    """Replaces listing placeholder in html if any.
    Listed dir must be subdir of current_dir.
    """

    matched = DOC_LISTING_RE.search(raw_html)
    if not matched:
        return raw_html

    start, end = matched.span()

    raw_path = matched.group(1)

    # idk what kind of fail condition there would be, welp future me can deal with it
    # listing_root = (current_dir / raw_path).resolve()
    listing_root = current_dir / raw_path

    # validate path is subdir
    if (
        not listing_root.exists()
        or not listing_root.is_dir()
        or (current_dir != listing_root and current_dir not in listing_root.parents)
    ):
        print("Ignoring invalid listing path:", raw_path)
        return raw_html

    # fetch valid post directories & create clickable entries for it
    # TODO: shield for quote-required path naming
    post_entries: list[tuple[datetime.datetime, str]] = []

    for path in listing_root.iterdir():
        if not path.is_dir() or path.stem.startswith(LISTING_IGNORED_DIR_PREFIX):
            continue

        index = path / "index.md"

        # try html if nonexistent, if even that fails just ignore it
        if not index.exists():
            index = path / "index.html"
            if not index.exists():
                continue

        # if no header still invalid file, continue
        # kinda inefficient to read here, then read again in build but welp
        header_matched = DOC_HEADER_RE.match(index.read_text(ENCODING))
        if not header_matched:
            continue

        header = doc_header_parser(header_matched.group(1))

        # TODO: Add tagging?
        post_entry = LISTING_FORMAT.format(
            title=header["title"],
            url=path.relative_to(current_dir).as_posix() + "/",
            date=(
                header["date"].strftime("%Y-%m-%d")
                if header["date"]
                else "DATE_FMT_ERR"
            ),
        )

        # make sure insertion is ordered
        bisect.insort(post_entries, (header["date"], post_entry), key=lambda x: x[0])

    # combine parts back since it's cheaper than replacement
    parts: list[str] = [raw_html[:start]]
    parts.extend(entry for _, entry in post_entries[::-1])
    parts.append(raw_html[end:])

    return "\n".join(parts)


# --- Logics ---


def build_html_page(raw_html: str, current_dir: pathlib.Path) -> str:
    """Generates built HTML string"""

    matched = DOC_HEADER_RE.match(raw_html)

    if not matched:
        # probably not meant to be post
        return raw_html

    # extract header content
    doc_header = doc_header_parser(matched.group(1))

    # check for listing
    # raw_html = replace_listing(raw_html, current_dir)

    # strip
    # start_idx, end_idx = matched.span()
    # raw_html = raw_html[start_idx:end_idx]

    # add plugins
    sections = [
        *(HTML_PARTS[f"plugin_{name}.html"] for name in doc_header["plugins"]),
        raw_html,
    ]

    # this mess is here because normal replace can't be used due to
    # curly braces in html files
    t = Template(HTML_PARTS[f"layout_{doc_header['layout']}.html"])
    return t.substitute(
        title=doc_header["title"],
        header=HTML_PARTS["header.html"],
        body="\n".join(sections),
        footer=HTML_PARTS["footer.html"],
    )


def build_md_page(raw_md: str, current_dir: pathlib.Path) -> str:
    """Generates built HTML string from Markdown"""

    # check for listing
    raw_md = replace_listing(raw_md, current_dir)

    md = MarkdownIt("gfm-like")
    # md.add_render_rule("link_open", render_blank_link)
    # ^ uncomment this to make all markdown links open in new tab

    return build_html_page(md.render(raw_md), current_dir)


def copy_dependencies():
    """Copies all non-html contents from `html_part` dir to output dir"""

    # relative path for better printing
    rel_dest_root = DEST_ROOT.relative_to(ROOT)

    print("=== Copying dependencies ===")

    # for path in HTML_PARTS_ROOT.relative_to(ROOT).iterdir():
    #     if path.suffix == ".html":
    #         continue
    #
    #     dest = rel_dest_root / path.name
    #     print(f"  Copying {path} -> {dest}")
    #
    #     path.copy(dest)

    # synchronize dangling files
    print_changes(
        multi_src_sync_dir(
            [MD_PAGE_ROOT, HTML_PARTS_ROOT], DEST_ROOT, SYNC_EXCLUDED_EXTS
        )
    )


def build():

    print("=== Building Start ===")

    reload_html_parts()

    # nuke directory
    # if DEST_ROOT.exists():
    #     remove_tree(DEST_ROOT)
    # else:
    #     DEST_ROOT.mkdir()

    # relative path for better printing
    rel_md_root = MD_PAGE_ROOT.relative_to(ROOT)
    rel_dest_root = DEST_ROOT.relative_to(ROOT)

    for path, dir_names, file_names in rel_md_root.walk():

        dest = rel_dest_root / path.relative_to(rel_md_root)
        dest.mkdir(exist_ok=True)

        for fn in file_names:
            f_src_path = path / fn
            f_dest_path = dest / fn

            depth_pad = " " * len(f_src_path.parents)

            # build site if either md or html
            if f_src_path.suffix == ".md":
                f_dest_path = f_dest_path.with_suffix(".html")

                print(
                    f"{depth_pad}Building {f_src_path.as_posix()} -> {f_dest_path.as_posix()}"
                )
                f_dest_path.write_text(
                    build_md_page(f_src_path.read_text(ENCODING), path), ENCODING
                )
                continue

            if f_src_path.suffix == ".html":
                print(
                    f"{depth_pad}Building {f_src_path.as_posix()} -> {f_dest_path.as_posix()}"
                )
                f_dest_path.write_text(
                    build_html_page(f_src_path.read_text(ENCODING), path), ENCODING
                )
                continue

            # otherwise just copy if it has different size or mtime
            # if f_dest_path.exists():
            #     src_stat = f_src_path.stat()
            #     dest_stat = f_dest_path.stat()
            #
            #     if (
            #         src_stat.st_size == dest_stat.st_size
            #         and src_stat.st_mtime == dest_stat.st_mtime
            #     ):
            #         print(f"{depth_pad}Skipping {f_src_path} -> {f_dest_path}")
            #         continue
            #
            # print(f"{depth_pad}Copying {f_src_path} -> {f_dest_path}")
            # f_dest_path.copy(f_src_path, preserve_metadata=True)


# --- Drivers ---


def main():
    copy_dependencies()
    build()


if __name__ == "__main__":
    main()
