#!/usr/bin/env python3
"""Verify a Quartz build of the autolearn knowledge wiki.

Checks the landing page, graph/search/explorer/backlinks UI, that raw-source
pages carry their credit block, that nothing outside the allowlist leaked,
and that the content index (search + graph) has nodes and edges.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main(public: Path) -> int:
    fails: list[str] = []
    index = public / "index.html"
    if not index.is_file():
        fails.append("missing index.html")
    else:
        html = index.read_text(errors="replace")
        for needle in ("kg-hero", "graph-container", "global-graph-container", "search", "explorer"):
            if needle not in html:
                fails.append(f"index.html lacks {needle}")
    raw_pages = list((public / "Raw-Sources").glob("*.html"))
    raw_pages = [p for p in raw_pages if p.name != "index.html"]
    if not raw_pages:
        fails.append("no raw source pages")
    for p in raw_pages:
        t = p.read_text(errors="replace")
        if "Original source" not in t or "Author(s)" not in t:
            fails.append(f"{p.name} lacks credit block")
        if "<script" in t.split("<article", 1)[-1].split("</article>", 1)[0]:
            fails.append(f"{p.name} has a script inside the article")
    ev = [p for p in (public / "Evergreen-Notes").glob("*.html") if p.name != "index.html"]
    if not ev:
        fails.append("no evergreen pages")
    elif "backlinks" not in ev[0].read_text(errors="replace").lower():
        fails.append("evergreen page lacks backlinks")
    for bad in ("archive", ".kg-tmp", "pipeline", "webapp", ".venv"):
        if (public / bad).exists():
            fails.append(f"{bad} leaked into the site")
    ci = json.loads((public / "static" / "contentIndex.json").read_text())
    nodes = len(ci)
    edges = sum(len(r.get("links", [])) for r in ci.values() if isinstance(r, dict))
    print(f"pages: {nodes}, raw: {len(raw_pages)}, evergreen: {len(ev)}, graph edges: {edges}")
    if nodes < 50 or edges < 50:
        fails.append("graph too small")
    for f in fails:
        print("FAIL:", f, file=sys.stderr)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
