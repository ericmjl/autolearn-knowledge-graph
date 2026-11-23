#!/usr/bin/env python3
"""Stage the autolearn knowledge wiki into this repo's ``content/`` folder.

Only an allowlist is published: Index.md (as index.md), MOCs/, evergreen/,
source-notes/ and raw/. Raw sources are republished as plain text with a
credit block (author, title, publication, date, original link) at the top.
Everything else in the wiki (archive/, .kg-tmp/, pipeline/, webapp/, .venv,
graph data, configs) stays out.

Usage: python3 scripts/sync_content.py [--wiki PATH] [--no-llm]
Exit code 3 means a possible secret was found and nothing was staged.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "content"
CREDITS = REPO / "site" / "credits.json"
THEME = REPO / "site" / "theme.json"
INKLING = "http://localhost:8101/v1/chat/completions"

FOLDERS = {  # wiki folder -> published folder name
    "MOCs": "Maps of Content",
    "evergreen": "Evergreen Notes",
    "source-notes": "Source Notes",
    "raw": "Raw Sources",
}
FOLDER_BLURBS = {
    "Maps of Content": "Theme pages. Each one lists the sources and evergreen notes on one part of the wiki.",
    "Evergreen Notes": "Synthesis notes. Each one connects at least two sources or notes and is titled as a claim.",
    "Source Notes": "One note per archived source: what it says and the claims drawn from it.",
    "Raw Sources": "The archived plain text of every source, credited to its original authors.",
}

SECRET_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9_-])" + p)
    for p in (
        r"gh[pousr]_[A-Za-z0-9]{30,}",
        r"github_pat_[A-Za-z0-9_]{40,}",
        r"sk-[A-Za-z0-9_-]{32,}",
        r"AKIA[0-9A-Z]{16}",
        r"xox[baprs]-[A-Za-z0-9-]{10,}",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"hf_[A-Za-z0-9]{30,}",
        r"AIza[0-9A-Za-z_-]{35}",
    )
]

WIKILINK = re.compile(r"\[\[([^\]|#]+)(#[^\]|]*)?(\|[^\]]*)?\]\]")
FENCE = re.compile(r"^(```|~~~)")


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5 :]
    return "", text


def fm_get(fm: str, key: str) -> str:
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm, re.M)
    return m.group(1) if m else ""


def yq(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def fix_links(text: str, published: set[str]) -> str:
    """Turn wikilinks to unpublished targets into plain text."""

    def repl(m: re.Match) -> str:
        target = m.group(1).strip()
        if target in published:
            return m.group(0)
        alias = (m.group(3) or "")[1:]
        return alias or target

    return WIKILINK.sub(repl, text)


MEDIA_BLOCK = re.compile(
    r"<(script|style|iframe|object|embed|video|audio|svg|picture|noscript|canvas|form)\b.*?</\1\s*>",
    re.I | re.S,
)
MD_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)|!\[\[[^\]]*\]\]")
HTML_TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(\s[^<>]*)?/?>")


def plain_text(body: str) -> str:
    """Strip images, scripts, embeds and any HTML so the page is plain text."""
    body = MEDIA_BLOCK.sub("", body)
    out, in_fence = [], False
    for line in body.split("\n"):
        if FENCE.match(line.strip()):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence:
            line = MD_IMAGE.sub("", line)
            line = HTML_TAG.sub("", line)
            # escape any leftover angle brackets except <https://...> autolinks
            line = re.sub(r"<(?!https?://)", "&lt;", line)
            line = re.sub(r"(?<!\\)\$", r"\\$", line)  # prices, not LaTeX
            # archived text is one paragraph per line; keep those breaks in markdown
            is_item = bool(re.match(r"\s*([-*+]|\d+\.)\s", line))
            prev = out[-1] if out else ""
            prev_item = bool(re.match(r"\s*([-*+]|\d+\.)\s", prev))
            if line.strip() and prev.strip() and not (is_item and prev_item):
                out.append("")
        out.append(line)
    return "\n".join(out)


def heuristic_credit(fm: str, body: str) -> dict:
    title = fm_get(fm, "title")
    url = fm_get(fm, "url")
    host = urlparse(url).netloc.removeprefix("www.")
    credit = {"title": title, "url": url, "authors": "", "publication": "", "date": ""}
    m = re.search(r"^- What this is: (.*)$", body, re.M)
    line = m.group(1) if m else ""
    if line.startswith("arXiv"):
        credit["publication"] = "arXiv"
        d = re.search(r"\((\d{4}-\d{2}-\d{2})\)", line)
        credit["date"] = d.group(1) if d else ""
    else:
        p = re.search(r"Web page from (.*?)(?:, by (.*?))?, dated (\d{4}-\d{2}-\d{2})", line)
        if p:
            credit["publication"] = p.group(1)
            credit["authors"] = (p.group(2) or "").replace("; ", ", ")
            credit["date"] = p.group(3)
    if not credit["publication"]:
        credit["publication"] = host
    pub_fix = {"AnthropicAI": "Anthropic", "arxiv.org": "arXiv", "langchain.com": "LangChain Blog"}
    credit["publication"] = pub_fix.get(credit["publication"], credit["publication"])
    if "wikipedia.org" in host:
        credit["publication"] = "Wikipedia"
        credit["authors"] = "Wikipedia contributors"
    if not credit["authors"]:
        a = re.search(r"\(([^()]*)\)\s*$", title)
        if a:
            names = re.sub(r",?\s*(Google|ICLR|\d{4}).*$", "", a.group(1)).strip(" ,")
            if names and not re.fullmatch(r"(Anthropic|LangChain|Wikipedia|X post|Google)", names):
                credit["authors"] = names
    return credit


def ask_inkling(credit: dict, body: str) -> dict:
    prompt = (
        "From this archived web page, extract who wrote it. Return ONLY JSON with keys "
        '"authors" (comma-separated full names, or "" if not stated), "publication" '
        '(site or venue name), "date" (YYYY-MM-DD or ""). Do not guess names that are not in the text.\n\n'
        f"Title: {credit['title']}\nURL: {credit['url']}\nCurrent guess: {json.dumps(credit)}\n\n"
        f"Text:\n{body[:5000]}"
    )
    req = {
        "model": "inkling-2-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0,
    }
    r = urllib.request.urlopen(
        urllib.request.Request(INKLING, json.dumps(req).encode(), {"Content-Type": "application/json"}),
        timeout=120,
    )
    content = json.load(r)["choices"][0]["message"]["content"] or ""
    m = re.search(r"\{.*\}", content, re.S)
    return json.loads(m.group(0)) if m else {}


def credit_for(stem: str, fm: str, body: str, cache: dict, use_llm: bool) -> dict:
    if stem in cache:
        return cache[stem]
    credit = heuristic_credit(fm, body)
    if use_llm and (not credit["authors"] or "et al" in credit["authors"]):
        try:
            got = ask_inkling(credit, body)
            names = str(got.get("authors", "")).strip()
            # only accept names that actually occur in the archived text
            if names and all(n.strip() and n.strip() in body for n in names.split(",")):
                credit["authors"] = names
            if not credit["date"] and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(got.get("date", ""))):
                credit["date"] = got["date"]
        except Exception as exc:  # noqa: BLE001
            print(f"[sync] inkling credit lookup failed for {stem}: {exc}", file=sys.stderr)
            return credit  # not cached, retried next run
    if use_llm:
        cache[stem] = credit
    return credit


def drop_leading_h1(text: str) -> str:
    """Quartz already shows the page title, so drop a duplicate leading ``# Title``."""
    fm, body = split_frontmatter(text)
    new_body = re.sub(r"\A\s*# [^\n]*\n+", "", body, count=1)
    return (f"---\n{fm}\n---\n" if fm else "") + new_body


def render_raw(stem: str, text: str, published: set[str], cache: dict, use_llm: bool) -> str:
    fm, body = split_frontmatter(text)
    c = credit_for(stem, fm, body, cache, use_llm)
    # drop the wiki's own header block (title + bullets) before the first ---
    parts = re.split(r"^---\s*$", body, maxsplit=1, flags=re.M)
    header, article = (parts[0], parts[1]) if len(parts) == 2 else ("", body)
    topics = re.search(r"^- Topics it supports: (.*)$", header, re.M)
    why = re.search(r"^- Why you kept it: (.*)$", header, re.M)
    notes_stem = "notes-on-" + stem
    if not c["authors"]:
        who = f"{c['publication']} (no individual author named)" if c["publication"] else "Not stated in the archived text"
        c = {**c, "authors": who}
    lines = [
        "---",
        f"title: {yq(c['title'])}",
        'type: "raw-source"',
        f"url: {yq(c['url'])}",
        f"author: {yq(c['authors'])}",
        f"publication: {yq(c['publication'])}",
        f"published: {yq(c['date'])}",
        f"archived: {yq(fm_get(fm, 'fetched_at'))}",
        "---",
        "",
        '> [!quote] Original source',
        f"> **Author(s):** {c['authors']}  ",
        f"> **Title:** {c['title']}  ",
        f"> **Published in:** {c['publication'] or 'Unknown'}  ",
        f"> **Date:** {c['date'] or 'Unknown'}  ",
        f"> **Original:** <{c['url']}>",
        ">",
        "> This is a plain-text archive kept so the wiki's notes can be checked against the source. "
        "Images, scripts and embedded media were removed. All rights stay with the original author(s); "
        "read and cite the original at the link above.",
        "",
    ]
    if notes_stem in published:
        lines.append(f"Notes on this source: [[{notes_stem}|Source note]]")
    if topics:
        lines.append(f"Themes: {topics.group(1)}")
    if why:
        lines.append(f"Why it was archived: {why.group(1)}")
    lines += ["", "## Archived text", "", plain_text(article).strip(), ""]
    return fix_links("\n".join(lines), published)


def render_source_note(text: str, published: set[str]) -> str:
    text = re.sub(
        r"^- Source: \[\[([^\]|]+)\]\]",
        lambda m: f"- Archived full text: [[{m.group(1)}|Full archived text, with credits]]",
        text,
        flags=re.M,
    )
    return fix_links(text, published)


def render_index(text: str, wiki: Path) -> str:
    theme = json.loads(THEME.read_text()) if THEME.exists() else {}
    tagline = theme.get("tagline", "")
    counts = {k: len(list((wiki / k).glob("*.md"))) for k in FOLDERS}
    hero = [
        "---",
        'title: "Home"',
        "---",
        "",
        '<div class="kg-hero">',
        f'<p class="kg-tagline">{tagline}</p>',
        f'<p class="kg-stats">{counts["evergreen"]} evergreen notes · {counts["raw"]} archived sources · '
        f'{counts["MOCs"]} theme pages · grows every hour</p>',
        "</div>",
        "",
        "This wiki writes itself. Every hour an agent running Inkling 2 Mini on a local GB10 box reads a few "
        "random evergreen notes, asks what they leave open, searches the web, archives one article, and writes "
        "one new evergreen note that ties the article to what is already here.",
        "",
        "Start with a theme page, or open the graph to see how the notes connect.",
        "",
        "",
    ]
    _, body = split_frontmatter(text)
    body = re.sub(r"^# Index\s*\n", "", body).replace("## MOCs", "## Themes")
    return "\n".join(hero) + body


def scan_secrets(root: Path) -> list[str]:
    hits = []
    for p in root.rglob("*.md"):
        t = p.read_text(encoding="utf-8", errors="replace")
        for pat in SECRET_PATTERNS:
            if pat.search(t):
                hits.append(f"{p.relative_to(root)}: {pat.pattern}")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", type=Path, default=Path.home() / "autolearn-knowledge-graph")
    ap.add_argument("--no-llm", action="store_true")
    args = ap.parse_args()
    wiki = args.wiki
    published = {"Index"} | {p.stem for k in FOLDERS for p in (wiki / k).glob("*.md")}
    cache = json.loads(CREDITS.read_text()) if CREDITS.exists() else {}

    stage = REPO / ".content-staging"
    shutil.rmtree(stage, ignore_errors=True)
    stage.mkdir()
    (stage / "index.md").write_text(render_index((wiki / "Index.md").read_text(), wiki))
    for src, dst in FOLDERS.items():
        out = stage / dst
        out.mkdir()
        (out / "index.md").write_text(f"---\ntitle: {yq(dst)}\n---\n\n{FOLDER_BLURBS[dst]}\n")
        for p in sorted((wiki / src).glob("*.md")):
            text = p.read_text(encoding="utf-8")
            if src == "raw":
                text = render_raw(p.stem, text, published, cache, not args.no_llm)
                # Quoted example keys in archived articles: blank them, keep the scan as a backstop.
                for pat in SECRET_PATTERNS:
                    text = pat.sub("[key-like string removed]", text)
            elif src == "source-notes":
                text = render_source_note(text, published)
            else:
                text = fix_links(text, published)
            if src != "raw":
                text = drop_leading_h1(text)
            (out / p.name).write_text(text, encoding="utf-8")

    hits = scan_secrets(stage)
    if hits:
        print("[sync] possible secrets found, not publishing:\n  " + "\n  ".join(hits), file=sys.stderr)
        shutil.rmtree(stage)
        return 3
    shutil.rmtree(CONTENT, ignore_errors=True)
    stage.rename(CONTENT)
    CREDITS.write_text(json.dumps(dict(sorted(cache.items())), indent=1, ensure_ascii=False) + "\n")
    print(f"[sync] staged {sum(1 for _ in CONTENT.rglob('*.md'))} pages into {CONTENT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
