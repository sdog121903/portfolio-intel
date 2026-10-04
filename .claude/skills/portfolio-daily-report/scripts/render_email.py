#!/usr/bin/env python3
"""Convert the email markdown (templates/email.md filled in) into simple, mobile-friendly HTML.

Supports: headings, paragraphs, **bold**, *italic*, [links](url), bullet and numbered lists,
tables, block quotes and horizontal rules. Standard library only.
Usage: python render_email.py reports/daily/2026/10/2026-10-05-email.md > out.html
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

STYLE = ("font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.5;color:#1d1d1f;"
         "max-width:680px;margin:0 auto;padding:8px")


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def convert(md: str) -> str:
    out, para, lst, table = [], [], None, []

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    def flush_list():
        nonlocal lst
        if lst:
            tag, items = lst
            out.append(f"<{tag}>" + "".join(f"<li>{inline(i)}</li>" for i in items) + f"</{tag}>")
            lst = None

    def flush_table():
        if table:
            rows = [r for r in table if not re.match(r"^\|?\s*:?-{2,}", r.strip())]
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            h = "<tr>" + "".join(f'<th style="text-align:left;border-bottom:1px solid #ccc;padding:4px 8px">{inline(c)}</th>' for c in cells[0]) + "</tr>"
            b = "".join("<tr>" + "".join(f'<td style="border-bottom:1px solid #eee;padding:4px 8px">{inline(c)}</td>' for c in r) + "</tr>" for r in cells[1:])
            out.append(f'<table style="border-collapse:collapse;font-size:14px">{h}{b}</table>')
            table.clear()

    for raw in md.splitlines():
        line = raw.rstrip()
        if line.strip().startswith("|"):
            flush_para(); flush_list(); table.append(line); continue
        flush_table()
        if not line.strip():
            flush_para(); flush_list(); continue
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            flush_para(); flush_list()
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>"); continue
        if re.match(r"^\s*[-*]\s+", line):
            flush_para()
            if not lst or lst[0] != "ul":
                flush_list(); lst = ("ul", [])
            lst[1].append(re.sub(r"^\s*[-*]\s+", "", line)); continue
        if re.match(r"^\s*\d+\.\s+", line):
            flush_para()
            if not lst or lst[0] != "ol":
                flush_list(); lst = ("ol", [])
            lst[1].append(re.sub(r"^\s*\d+\.\s+", "", line)); continue
        if line.startswith(">"):
            flush_para(); flush_list()
            out.append(f'<blockquote style="border-left:3px solid #ccc;margin:8px 0;padding-left:10px;color:#555">{inline(line.lstrip("> "))}</blockquote>')
            continue
        if re.match(r"^-{3,}$", line.strip()):
            flush_para(); flush_list(); out.append("<hr>"); continue
        para.append(line.strip())
    flush_para(); flush_list(); flush_table()
    return f'<div style="{STYLE}">' + "\n".join(out) + "</div>"


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    print(convert(Path(argv[0]).read_text(encoding="utf-8")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
