#!/usr/bin/env python3
"""Sanity-check the static pages: balanced tags, no unescaped <placeholder> text,
and every in-page anchor (href="#x") resolves to an id on that page."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
KNOWN = {
    "a", "abbr", "aside", "b", "blockquote", "body", "br", "button", "caption", "code", "col", "colgroup",
    "dd", "details", "div", "dl", "dt", "em", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head",
    "header", "hr", "html", "i", "img", "input", "kbd", "label", "li", "link", "main", "mark", "meta",
    "nav", "ol", "option", "p", "path", "pre", "script", "section", "select", "small", "span", "strong",
    "style", "sub", "summary", "sup", "svg", "table", "tbody", "td", "th", "thead", "title", "tr", "ul",
}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errors, self.ids, self.hrefs = [], [], set(), []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.hrefs.append((attrs["href"], self.getpos()[0]))
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"line {self.getpos()[0]}: unexpected </{tag}> (open: {self.stack[-1] if self.stack else None})")


def check(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    c = Checker()
    c.feed(text)
    errors = list(c.errors)
    errors += [f"line {ln}: unclosed <{t}>" for t, ln in c.stack]
    for n, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r"<(/?)([A-Za-z][A-Za-z0-9_-]*)", line):
            if m.group(2).lower() not in KNOWN:
                errors.append(f"line {n}: unescaped <{m.group(2)}> (use &lt;…&gt;)")
    for href, ln in c.hrefs:
        if href != "#" and href[1:] not in c.ids:
            errors.append(f"line {ln}: dangling anchor {href}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    bad = 0
    for f in sorted(root.glob("*.html")):
        errs = check(f)
        print(f"{f.name}: {'OK' if not errs else f'{len(errs)} problem(s)'}")
        for e in errs:
            print(f"  {e}")
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
