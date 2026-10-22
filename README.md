# MLOps Interview Cram Sheet — TCS

Two self-contained static pages for last-minute MLOps interview prep (TCS, Bangalore). No build step, no dependencies.

**Live:** https://arvindcr4.github.io/mlops-tcs-cram/

| Page | What it covers |
|---|---|
| [`index.html`](index.html) | 21 sections: interview format, résumé edge, ML fundamentals, metrics, MLOps lifecycle, experiment tracking, orchestration, Docker, Kubernetes, CI/CD/CT, serving & deployment strategies, monitoring & drift, feature stores, cloud ML platforms, LLMOps, Python/SQL quick reference, ML system design framework, top-60 Q&A, behavioral/STAR, project narrative template, cheat tables, glossary |
| [`negotiation.html`](negotiation.html) | HR salary negotiation: reality check, Bangalore bands, your numbers, core scripts, direct account assignment + live phone call, likely HR questions, pre-call checklist |

## Features

- Sticky table of contents with the active section highlighted as you scroll
- Live filter box (`Filter everything…`) that hides non-matching sections and auto-expands matching Q&A
- Reading-progress bar
- Collapsible `<details>` blocks for rehearsing answers before revealing them
- Prints cleanly

## Usage

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
# http://localhost:8000/
```

Section 18 (*Your Project Narrative*) is a template: fill in your own answers before the interview.

## Checks

`scripts/check_html.py` verifies both pages have balanced tags, no unescaped `<placeholder>` text inside code blocks (which browsers swallow as tags), and no dangling `#anchor` links. It runs in CI on every push and pull request.

```sh
python3 scripts/check_html.py
```
