"""
Builds very specific site from Markdown files in prehistoric way

:Author: jupiterbjy@gmail.com
"""

import re
import pathlib
from string import Template
from typing import TypedDict

from markdown_it import MarkdownIt


# --- Config ---

ENCODING = "utf8"

ROOT = pathlib.Path(__file__).parent

DEST_ROOT = ROOT / "docs"

# HTML Body parts, e.g. header & footer
HTML_PARTS_ROOT = ROOT / "html_parts"
HTML_PARTS: dict[str, str] = {}

# MD Pages
MD_PAGE_ROOT = ROOT / "md_pages"

# KEYWORD_PREFIX = "<!-- include "
# INCLUDE_RE = re.compile(r"^<!-- include (\S*) -->$")

# TITLE_PREFIX = "<!-- title "
# TITLE_RE = re.compile(r"^<!-- title ([\S\s]*) -->$")

DOC_HEADER_RE = re.compile(r"^<!-- HEADER\n([\S\s]*)\n-->")


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
    date: str
    layout: str
    tags: list[str]
    plugins: list[str]


def doc_header_parser(matched_str: str) -> DocHeader:
    """Parses header content from matched string"""

    result = DocHeader(title="", date="", layout="", tags=[], plugins=[])

    for line in matched_str.splitlines():
        key, val = map(str.strip, line.split(":", maxsplit=1))

        match key:
            case "title":
                result["title"] = val

            case "date":
                result["date"] = val

            case "layout":
                result["layout"] = val

            case "tags":
                result["tags"].extend(map(str.strip, val.split(" ")))

            case "plugins":
                result["plugins"].extend(map(str.strip, val.split(" ")))

    return result


# --- Logics ---


def build_html_page(raw_html: str) -> str:
    """Generates built HTML string"""

    title = ""

    matched = DOC_HEADER_RE.match(raw_html)

    if not matched:
        # probably not meant to be post
        return raw_html

    # extract header content
    doc_header = doc_header_parser(matched.group(1))

    # add plugins
    sections = [
        *(HTML_PARTS[f"plugin_{name}.html"] for name in doc_header["plugins"]),
        raw_html,
    ]

    # strip
    # start_idx, end_idx = matched.span()
    # raw_html = raw_html[start_idx:end_idx]

    t = Template(HTML_PARTS[f"layout_{doc_header['layout']}.html"])
    return t.substitute(
        title=doc_header["title"],
        header=HTML_PARTS["header.html"],
        body="\n".join(sections),
        footer=HTML_PARTS["footer.html"],
    )


def build_md_page(raw_md: str) -> str:
    """Generates built HTML string from Markdown"""

    md = MarkdownIt("gfm-like")
    md.add_render_rule("link_open", render_blank_link)

    return build_html_page(md.render(raw_md))


def copy_dependencies():
    """Copies all non-html contents from `html_part` dir to output dir"""

    # relative path for better printing
    rel_dest_root = DEST_ROOT.relative_to(ROOT)

    print("=== Copying dependencies ===")

    for path in HTML_PARTS_ROOT.relative_to(ROOT).iterdir():
        if path.suffix == ".html":
            continue

        dest = rel_dest_root / path.name
        print(f"  Copying {path} -> {dest}")

        path.copy(dest)


def build():

    print("=== Building Start ===")

    reload_html_parts()

    # nuke directory
    if DEST_ROOT.exists():
        remove_tree(DEST_ROOT)
    else:
        DEST_ROOT.mkdir()

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

                print(f"{depth_pad}Building {f_src_path} -> {f_dest_path}")
                f_dest_path.write_text(
                    build_md_page(f_src_path.read_text(ENCODING)), ENCODING
                )
                continue

            if f_src_path.suffix == ".html":
                print(f"{depth_pad}Building {f_src_path} -> {f_dest_path}")
                f_dest_path.write_text(
                    build_html_page(f_src_path.read_text(ENCODING)), ENCODING
                )
                continue

            # otherwise just copy
            print(f"{depth_pad}Copying {f_src_path} -> {f_dest_path}")
            f_dest_path.write_bytes(f_src_path.read_bytes())


# --- Drivers ---


def main():
    build()
    copy_dependencies()


if __name__ == "__main__":
    main()
