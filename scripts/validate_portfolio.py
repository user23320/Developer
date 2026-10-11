#!/usr/bin/env python3
"""Check the built portfolio's routes, accessibility structure and evidence boundaries."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "docs"


class Page(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.assets: list[str] = []
        self.headings: list[str] = []
        self.heading: str | None = None
        self.text: list[str] = []
        self.tags: list[str] = []
        self.metadata: dict[str, str] = {}
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        self.tags.append(tag)
        if data.get("id"):
            if data["id"] in self.ids:
                self.errors.append("Duplicate id: " + data["id"])
            self.ids.add(data["id"])
        if tag == "a":
            if not data.get("href"):
                self.errors.append("Anchor without href")
            else:
                self.links.append(data["href"])
        if tag == "link" and data.get("rel") in {"stylesheet", "icon"}:
            self.assets.append(data.get("href", ""))
        if tag in {"script", "img"}:
            self.assets.append(data.get("src", ""))
        if tag == "img" and "alt" not in data:
            self.errors.append("Image without alt")
        if tag == "meta" and data.get("name"):
            self.metadata[data["name"]] = data.get("content", "")
        if tag in {"h1", "h2", "h3"}:
            self.heading = ""
        if tag == "html" and data.get("lang") != "en":
            self.errors.append("Missing document language")
        if tag == "button" and data.get("class") == "nav-toggle":
            if data.get("aria-controls") != "primary-nav" or data.get("aria-expanded") != "false":
                self.errors.append("Menu button missing initial accessible state")

    def handle_endtag(self, tag):
        if tag in {"h1", "h2", "h3"} and self.heading is not None:
            self.headings.append(self.heading.strip())
            self.heading = None

    def handle_data(self, data):
        self.text.append(data)
        if self.heading is not None:
            self.heading += data


def resolve(page: Path, value: str) -> tuple[Path, str] | None:
    parts = urlsplit(value)
    if parts.scheme or parts.netloc:
        return None
    path = unquote(parts.path)
    if path.startswith("/"):
        if not path.startswith("/Developer/"):
            raise ValueError("Root-relative URL misses GitHub Pages project prefix: " + value)
        target = PUBLIC / path.removeprefix("/Developer/")
    else:
        target = page.parent / path if path else page
    if target.is_dir():
        target = target / "index.html"
    target = target.resolve()
    if not target.is_relative_to(PUBLIC.resolve()):
        raise ValueError("Link escapes published docs: " + value)
    return target, unquote(parts.fragment)


def main():
    files = sorted(PUBLIC.rglob("*.html"))
    parsed: dict[Path, Page] = {}
    errors = []
    for file in files:
        page = Page(str(file.relative_to(PUBLIC)))
        page.feed(file.read_text(encoding="utf-8"))
        parsed[file.resolve()] = page
        if page.tags.count("h1") != 1:
            page.errors.append("Expected exactly one h1")
        if page.tags.count("main") != 1:
            page.errors.append("Expected exactly one main landmark")
        if "viewport" not in page.metadata or "description" not in page.metadata:
            page.errors.append("Missing viewport or description")
        if not {"main-content", "primary-nav"}.issubset(page.ids):
            page.errors.append("Missing skip-link target or navigation")
        errors.extend(f"{page.source}: {e}" for e in page.errors)
    if len(files) != 17:
        errors.append(f"Expected 17 public HTML pages; found {len(files)}")
    local_links = 0
    for file, page in parsed.items():
        for value in page.links + page.assets:
            try:
                destination = resolve(file, value)
                if destination is None:
                    continue
                target, fragment = destination
                local_links += 1
                if not target.is_file():
                    errors.append(f"{page.source}: missing local target {value}")
                elif fragment and target in parsed and fragment not in parsed[target].ids:
                    errors.append(f"{page.source}: missing fragment {value}")
                if target.suffix == ".md":
                    errors.append(f"{page.source}: untranslated local Markdown link {value}")
            except ValueError as e:
                errors.append(f"{page.source}: {e}")
    # Only public links already recorded in the source documents, plus portfolio URLs,
    # may be presented. This catches invented demonstrations/private locations.
    source_urls = {"https://github.com/user23320/Developer"}
    for path in [ROOT / "README.md", *(ROOT / "projects").rglob("*.md"), *(ROOT / "evidence").rglob("*.md")]:
        source_urls.update(re.findall(r"\]\((https://[^)]+)\)", path.read_text(encoding="utf-8")))
    for file, page in parsed.items():
        for url in page.links:
            if urlsplit(url).scheme:
                if url not in source_urls and not url.startswith("https://github.com/user23320/Developer/blob/main/"):
                    errors.append(f"{page.source}: public link not grounded in portfolio sources: {url}")
    home = parsed[(PUBLIC / "index.html").resolve()]
    home_text = " ".join(home.text)
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    statuses = re.findall(r"^\| \*\*([^|]+)\*\* \| \*\*([^|]+)\*\* \|", readme, re.M)
    if len(statuses) != 6:
        errors.append("Expected six authoritative README project status labels")
    for name, status in statuses:
        if name not in home_text or status not in home_text:
            errors.append("Home page lost exact project name/status: " + name)
    for folder in (ROOT / "evidence").iterdir():
        if folder.is_dir():
            page = parsed[(PUBLIC / "evidence" / folder.name / "index.html").resolve()]
            if not {"Available", "Private", "Planned"}.issubset(set(page.headings)):
                errors.append(f"{page.source}: evidence availability headings are not separated")
    for statement in ["October 2026", "11 October 2026", "not independent validation", "not the proprietary applications", "production accounts", "protected business logic"]:
        if statement not in home_text:
            errors.append("Home page lost review boundary/date: " + statement)
    if errors:
        raise SystemExit("Portfolio validation failed:\n" + "\n".join(errors))
    print(f"Validated {len(files)} pages, {local_links} local links/assets, six project statuses and six evidence indexes.")
    print("External product websites and browser layout/interaction were not tested.")


if __name__ == "__main__":
    main()
