# autolearn-knowledge-graph

A wiki about building, evaluating and securing LLM agents that grows by itself, one source and one note per hour.

Site: <https://ericmjl.github.io/autolearn-knowledge-graph/>

## How it grows

An hourly job on my GB10 box runs an agent on Inkling 2 Mini. Each run, the agent:

1. Reads four evergreen notes picked at random.
2. Writes down a few questions those notes leave open.
3. Searches the web for answers through a local SearXNG instance.
4. Archives exactly one article it found.
5. Writes one evergreen note that links that article to at least one existing note.

A guard script checks every run. It rejects invented links, near-duplicate notes and edits outside the agent's own notes. When a run passes, this repo is synced and pushed, and GitHub Actions rebuilds the site.

## What is here

```text
content/index.md            home page
content/Maps of Content/    theme pages
content/Evergreen Notes/    synthesis notes, each built from two or more notes or sources
content/Source Notes/       one note per source: what it says and the claims taken from it
content/Raw Sources/        the archived plain text of each source, with credits
site/                       Quartz v4.5.2 config, layout, theme and build check
scripts/sync_content.py     copies the published folders out of the wiki
```

`content/` is generated, so please don't edit it by hand. The working wiki, with its pipeline, archive and scratch files, stays on the GB10.

## Credit for sources

Each page under Raw Sources is a plain-text copy of someone else's work, kept so the notes can be checked against what the source actually says. The top of each page names the author(s), title, publication, date and original URL. Images, scripts and embedded media are removed. All rights stay with the original authors, so please read and cite the originals. If you are an author and want your piece taken down, open an issue.

The notes are written by an agent, not by me, so treat them as leads to check rather than settled claims.

## Build

The site is built with [Quartz](https://quartz.jzhao.xyz) v4.5.2, set up the same way as [kenx-gxp-conference-east-2026](https://github.com/ericmjl/kenx-gxp-conference-east-2026). `.github/workflows/deploy.yml` checks out Quartz, copies in `site/` and `content/`, builds, runs `site/verify_build.py`, and deploys to GitHub Pages.
