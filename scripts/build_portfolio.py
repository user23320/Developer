#!/usr/bin/env python3
"""Render the public Markdown portfolio as a dependency-free GitHub Pages site.

The existing README, case studies and evidence indexes remain the source of truth.
Only their public text is read. No private application files or runtime data are used.
"""

from __future__ import annotations

import argparse
import html
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"
REPOSITORY = "https://github.com/user23320/Developer"
SITE = "https://user23320.github.io/Developer/"
PROJECTS = [
    ("daleam-edu", "Education", "DE"),
    ("assist-shop-management", "Retail & POS", "AS"),
    ("real-tech-electricals", "Service operations", "RT"),
    ("easyshopen", "E-commerce", "ES"),
    ("saferide-gh-rider", "Mobile development", "SR"),
    ("smart-campus-environment-monitoring", "Academic IoT & cloud", "SC"),
]
ROUTES = {
    "README.md": "index.html",
    "projects/README.md": "projects/index.html",
    "evidence/README.md": "evidence/index.html",
    "evidence/TEMPLATE.md": "evidence/template/index.html",
}
for slug, _, _ in PROJECTS:
    ROUTES[f"projects/{slug}.md"] = f"projects/{slug}/index.html"
    ROUTES[f"evidence/{slug}/README.md"] = f"evidence/{slug}/index.html"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def anchor(value: str) -> str:
    value = re.sub(r"[*_`]", "", value).lower()
    value = "".join(c for c in value if c.isalnum() or c in " -_")
    return re.sub(r"\s", "-", value)


def relative(target: str, page: str) -> str:
    return posixpath.relpath(target, posixpath.dirname(page) or ".")


def link_target(url: str, source: str, page: str) -> str:
    parts = urlsplit(url)
    if parts.scheme:
        if parts.scheme not in {"https", "http", "mailto"}:
            raise ValueError(f"Unsupported link scheme in {source}: {parts.scheme}")
        return url
    if parts.netloc or url.startswith("/"):
        raise ValueError(f"Use explicit public URLs or relative paths in {source}")
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), parts.path)) if parts.path else source
    if resolved not in ROUTES:
        raise ValueError(f"No published route for {resolved}, referenced in {source}")
    target = relative(ROUTES[resolved], page)
    return target + ("#" + parts.fragment if parts.fragment else "")


def inline(text: str, source: str, page: str) -> str:
    pattern = re.compile(r"(\[([^\]]+)\]\(([^)]+)\)|`([^`]+)`|\*\*(.+?)\*\*|(?<!\w)_([^_]+)_(?!\w))")
    rendered = []
    offset = 0
    for match in pattern.finditer(text):
        rendered.append(esc(text[offset:match.start()]))
        if match.group(2) is not None:
            href = link_target(match.group(3), source, page)
            rendered.append(f'<a href="{esc(href)}">{inline(match.group(2), source, page)}</a>')
        elif match.group(4) is not None:
            rendered.append(f"<code>{esc(match.group(4))}</code>")
        elif match.group(5) is not None:
            rendered.append(f"<strong>{inline(match.group(5), source, page)}</strong>")
        else:
            rendered.append(f"<em>{inline(match.group(6), source, page)}</em>")
        offset = match.end()
    rendered.append(esc(text[offset:]))
    return "".join(rendered)


def markdown(text: str, source: str, page: str) -> str:
    """Render the headings, paragraphs, lists and tables used by these sources.

    Escape raw HTML and fail on unsupported blocks rather than silently omit content.
    """
    lines = text.splitlines()
    result = []
    i = 0
    heading_counts: dict[str, int] = {}
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith(("```", ">", "![")):
            raise ValueError(f"Unsupported Markdown block in {source}: {line[:50]}")
        heading = re.match(r"^(#{1,6}) (.+)$", line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2)
            base_id = anchor(title)
            occurrence = heading_counts.get(base_id, 0)
            heading_counts[base_id] = occurrence + 1
            heading_id = base_id + (f"-{occurrence}" if occurrence else "")
            badge = f' class="availability-heading {title.lower()}"' if title in {"Available", "Private", "Planned"} else ""
            result.append(f'<h{level} id="{esc(heading_id)}"{badge}>{inline(title, source, page)}</h{level}>')
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\s*\|(?:\s*:?-+:?\s*\|)+\s*", lines[i + 1]):
            headers = [cell.strip() for cell in line.strip("|").split("|")]
            rows = []
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
                if len(cells) != len(headers):
                    raise ValueError(f"Inconsistent table row in {source}")
                rows.append(cells)
                i += 1
            header = "".join(f'<th scope="col">{inline(cell, source, page)}</th>' for cell in headers)
            body = "".join("<tr>" + "".join(f'<td data-label="{esc(re.sub(r"[*_`]", "", label))}">{inline(cell, source, page)}</td>' for label, cell in zip(headers, cells)) + "</tr>" for cells in rows)
            result.append(f'<div class="table-wrap"><table role="table"><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table></div>')
            continue
        list_match = re.match(r"^(- |\d+\. )(.+)$", line)
        if list_match:
            ordered = list_match.group(1) != "- "
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines):
                item = re.match(r"^(\d+\. |\- )(.+)$", lines[i].strip())
                if not item or (item.group(1) != "- ") != ordered:
                    break
                items.append(f"<li>{inline(item.group(2), source, page)}</li>")
                i += 1
            result.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6} |\||- |\d+\. )", lines[i].strip()):
            paragraph.append(lines[i].strip())
            i += 1
        result.append(f'<p>{inline(" ".join(paragraph), source, page)}</p>')
    return "\n".join(result)


def section(text: str, heading: str) -> str:
    marker = f"## {heading}\n"
    if marker not in text:
        raise ValueError(f"Required README heading missing: {heading}")
    return text.split(marker, 1)[1].split("\n## ", 1)[0].strip()


def trimmed_document(text: str) -> str:
    """Replace the Markdown title/navigation with the website's accessible shell."""
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError("Document must start with one level-one title")
    lines = lines[1:]
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith("[") and " · " in lines[0]:
        lines.pop(0)
    return "\n".join(lines).strip()


def status_class(status: str) -> str:
    return "live" if status.startswith("Live") else "ongoing"


def status_label(status: str) -> str:
    return f'<span class="status {status_class(status)}">{esc(status)}</span>'


def shell(page: str, title: str, description: str, body: str, active: str = "", document: bool = False) -> str:
    def route(target: str) -> str:
        return relative(target, page)
    home = route("index.html")
    nav = []
    for name, target, key in [("Profile", home + "#profile", "profile"), ("Skills", home + "#skills", "skills"), ("Projects", route("projects/index.html"), "projects"), ("Evidence", route("evidence/index.html"), "evidence"), ("Contact", home + "#contact", "contact")]:
        current = ' aria-current="page"' if active == key else ""
        nav.append(f'<a href="{esc(target)}"{current}>{name}</a>')
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(description)}">
  <meta name="theme-color" content="#102d31">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(SITE + page.removesuffix('index.html'))}">
  <link rel="canonical" href="{esc(SITE + page.removesuffix('index.html'))}">
  <link rel="icon" href="{route('assets/favicon.svg')}" type="image/svg+xml">
  <link rel="stylesheet" href="{route('assets/styles.css')}">
  <script src="{route('assets/site.js')}" defer></script>
  <title>{esc(title)}</title>
</head>
<body class="{'document-page' if document else 'portfolio-page'}">
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="{home}" aria-label="David Abayateye Lomotey — portfolio home"><span class="brand-mark" aria-hidden="true">DL<span>.</span></span><span class="brand-name">David Lomotey<span>Software developer · Ghana</span></span></a>
      <button class="nav-toggle" type="button" hidden aria-controls="primary-nav" aria-expanded="false"><span>Menu</span><span class="menu-icon" aria-hidden="true"></span></button>
      <nav id="primary-nav" class="primary-nav" aria-label="Main navigation">{''.join(nav)}</nav>
    </div>
  </header>
  <main id="main-content" tabindex="-1">{body}</main>
  <footer class="site-footer">
    <div class="container footer-inner">
      <div><a class="footer-name" href="{home}">David Abayateye Lomotey</a><p>Software Developer · Systems Builder · DALEAM Technology</p></div>
      <div class="footer-links"><a href="{REPOSITORY}">Source repository</a><a href="{route('evidence/index.html')}">Evidence &amp; limitations</a><a href="#main-content">Back to top ↑</a></div>
    </div>
    <div class="container footer-note">Project status: October 2026 · Evidence inventory: 11 October 2026. Public references can change.</div>
  </footer>
</body>
</html>
'''


def project_cards(rows: list[dict[str, str]], page: str) -> str:
    cards = []
    for i, ((slug, category, monogram), row) in enumerate(zip(PROJECTS, rows), 1):
        detail = relative(f"projects/{slug}/index.html", page)
        evidence = relative(f"evidence/{slug}/index.html", page)
        public = re.search(r"\[Website\]\((https://[^)]+)\)", row["scope"])
        if public:
            public_link = f'<a href="{esc(public.group(1))}" class="public-reference">Public website ↗</a>'
            availability = "Case study, evidence index &amp; public pages"
        elif slug == "saferide-gh-rider":
            public_link = '<a href="https://daleamtechnology.net" class="public-reference">Company / contact ↗</a>'
            availability = "Case study &amp; evidence index; no app release"
        else:
            public_link = '<span class="public-reference">Academic design · no deployment</span>'
            availability = "Case study &amp; evidence index; design scope"
        summary = row["scope"].split("**Public now:**", 1)[0].strip()
        cards.append(f'''<article class="project-card" data-project-status="{status_class(row['status'])}">
          <div class="project-topline"><span class="project-number">0{i} / {esc(category)}</span><span class="project-monogram" aria-hidden="true">{monogram}</span></div>
          <h3><a href="{detail}">{esc(row['name'])}</a></h3>
          {status_label(row['status'])}
          <p class="project-description">{inline(summary, 'README.md', page)}</p>
          <dl class="card-evidence"><div><dt>Available</dt><dd>{availability}</dd></div><div><dt>Private</dt><dd>Conditional review; readiness unconfirmed</dd></div><div><dt>Planned</dt><dd>Supporting artifacts not published</dd></div></dl>
          <div class="project-links"><a class="text-link" href="{detail}">Read case study <span aria-hidden="true">→</span></a><a href="{evidence}">Evidence index</a></div>
          <div class="project-public-link">{public_link}</div>
        </article>''')
    return "\n".join(cards)


def build_home(readme: str, rows: list[dict[str, str]]) -> str:
    page = "index.html"
    intro = readme.split("\n\n", 3)[2]
    focus = section(readme, "Professional Focus")
    skills = section(readme, "Technical Skills")
    stack = section(readme, "Technology Stack")
    contact = section(readme, "Contact")
    body = f'''
    <section class="hero container" id="profile" aria-labelledby="profile-title">
      <div class="hero-copy">
        <p class="eyebrow"><span class="small-rule"></span>Ghana · DALEAM Technology</p>
        <h1 id="profile-title">David Abayateye<br><span>Lomotey<span class="name-period">.</span></span></h1>
        <p class="hero-role">Software Developer <span aria-hidden="true">/</span> Systems Builder</p>
        <p class="hero-description">{esc(intro)}</p>
        <div class="hero-actions"><a class="button button-primary" href="#projects">Explore selected work <span aria-hidden="true">↘</span></a><a class="button button-outline" href="#contact">Professional enquiries <span aria-hidden="true">↗</span></a></div>
      </div>
      <aside class="hero-index" aria-labelledby="hero-index-title">
        <div class="index-heading"><p class="eyebrow">Selected work</p><span class="index-date">October 2026</span></div>
        <h2 id="hero-index-title">Practical systems.<br>Clear documentation.</h2>
        <ol class="hero-project-list">{''.join(f'<li><a href="projects/{slug}/index.html"><span class="index-counter">0{i}</span><span>{esc(row["name"])}</span><span class="index-arrow" aria-hidden="true">↗</span></a></li>' for i, ((slug, _, _), row) in enumerate(zip(PROJECTS, rows), 1))}</ol>
        <p class="index-note">Explore each project's scope, contribution, current status, and evidence limits.</p>
      </aside>
    </section>
    <div class="intro-band"><div class="container"><p>Web systems <span aria-hidden="true">/</span> Mobile development <span aria-hidden="true">/</span> IoT &amp; cloud design</p><a href="evidence/index.html">Review the evidence inventory <span aria-hidden="true">→</span></a></div></div>
    <section class="section container" id="skills" aria-labelledby="skills-title">
      <div class="section-heading"><p class="eyebrow">01 / Capabilities</p><h2 id="skills-title">From operational needs<br>to usable software.</h2></div>
      <div class="capabilities"><div class="focus-column"><h3>Professional focus</h3>{markdown(focus, 'README.md', page)}</div><div class="skills-column"><h3>Technical skills</h3>{markdown(skills, 'README.md', page)}</div></div>
      <details class="stack-details"><summary>Technology stack <span>Languages, data, interfaces, integrations &amp; operations</span></summary><div class="document-content">{markdown(stack, 'README.md', page)}<p class="small-copy">This is the general portfolio stack. Project-specific technology areas are recorded in each case study.</p></div></details>
    </section>
    <section class="project-section section" id="projects" aria-labelledby="projects-title">
      <div class="container"><div class="section-heading section-heading-row"><div><p class="eyebrow">02 / Selected projects</p><h2 id="projects-title">Work grounded in<br>everyday operations.</h2></div><p class="section-description">Six documented projects across education, retail, services, e-commerce, mobile, and academic IoT. Status wording preserved from October 2026.</p></div>
      <div class="project-grid">{project_cards(rows, page)}</div>
      <div class="status-key"><p><strong>Live</strong> means a public deployment is accessible. <strong>Ongoing</strong> means development, testing, documentation, or design work continues.</p><p>These are the repository's October 2026 descriptions; public sites and private workflows were not retested for this website.</p></div></div>
    </section>
    <section class="section container" id="evidence" aria-labelledby="evidence-title">
      <div class="section-heading section-heading-row"><div><p class="eyebrow">03 / Evidence for reviewers</p><h2 id="evidence-title">Know what you can review.</h2></div><p class="section-description">Project maturity and evidence availability are separate. Inventory reviewed on 11 October 2026.</p></div>
      <div class="evidence-grid">
        <article class="evidence-panel available"><p class="availability-label">Available</p><h3>Public documents &amp; references</h3><p>This portfolio, six author-written case studies, project evidence indexes, and public-facing website links. External pages can change and were not retested for this inventory.</p><a class="text-link" href="evidence/index.html#project-indexes">Explore project indexes <span aria-hidden="true">→</span></a></article>
        <article class="evidence-panel private"><p class="availability-label">Private</p><h3>Review by arrangement</h3><p>Sanitized demonstrations, screenshots, and high-level summaries may be arranged subject to owner permission, availability, and preparation. A prepared review package is not confirmed.</p><p class="small-copy">Real Tech's previously supplied private academic report has unconfirmed external-sharing permission and readiness.</p><a class="text-link" href="evidence/real-tech-electricals/index.html#private">Read private-review conditions <span aria-hidden="true">→</span></a></article>
        <article class="evidence-panel planned"><p class="availability-label">Planned</p><h3>Unpublished supporting artifacts</h3><p>Demonstration packages, screenshots, architecture diagrams, completed academic reports/presentations, application code samples, and recorded test results are not attached.</p><p class="small-copy">The reusable template helps document future artifacts; it is not implementation evidence or a record of completed checks.</p><a class="text-link" href="evidence/template/index.html">View the artifact template <span aria-hidden="true">→</span></a></article>
      </div>
      <div class="review-limits"><h3>Scope &amp; limitations</h3><p>Case studies are author-written accounts, not independent validation of authorship, implementation, security, performance, or every listed feature. Public pages do not verify private workflows or business outcomes. SafeRide is an MVP in development; Smart Campus is an academic design.</p><p>Repository commits document this portfolio, not the proprietary applications' development history. Indexes do not establish that planned artifacts are complete.</p><a href="{REPOSITORY}/commits/main/">Review documentation history ↗</a></div>
      <div class="publication-boundary"><span class="boundary-mark" aria-hidden="true">↳</span><p><strong>Publication boundary.</strong> Credentials, API keys, secrets, customer/student records, payment data, private database contents, internal infrastructure and configuration, and protected business logic are excluded. Any arranged review must use synthetic or appropriately sanitized material; production accounts and live customer data are outside the review scope.</p></div>
    </section>
    <section class="contact-section" id="contact" aria-labelledby="contact-title"><div class="container contact-layout"><div><p class="eyebrow">04 / Contact</p><h2 id="contact-title">Let's discuss<br>the work.</h2></div><div class="contact-copy document-content">{markdown(contact, 'README.md', page)}<div class="contact-actions"><a class="button button-primary" href="https://daleamtechnology.net">DALEAM Technology <span aria-hidden="true">↗</span></a><a class="button button-outline" href="https://github.com/user23320">GitHub profile <span aria-hidden="true">↗</span></a></div></div></div></section>
    '''
    return shell(page, "David Abayateye Lomotey | Software Developer", "Ghana-based software developer and systems builder at DALEAM Technology. Explore six project case studies, October 2026 status, and clearly labelled evidence.", body)


def build_document(source: str, text: str, rows: list[dict[str, str]]) -> tuple[str, str]:
    page = ROUTES[source]
    title = text.splitlines()[0].removeprefix("# ")
    content = trimmed_document(text)
    is_project = source.startswith("projects/") and source != "projects/README.md"
    is_evidence = source.startswith("evidence/")
    active = "evidence" if is_evidence else "projects"
    eyebrow = "Evidence inventory · 11 October 2026" if is_evidence else "Project case study · October 2026"
    lead = ""
    contextual = []
    if is_project:
        slug = Path(source).stem
        row = rows[[s[0] for s in PROJECTS].index(slug)]
        lead = status_label(row["status"])
        contextual.append(("Project evidence index", f"evidence/{slug}/index.html"))
    elif source == "projects/README.md":
        eyebrow = "Selected projects · October 2026"
        contextual.append(("Evidence overview", "evidence/index.html"))
    elif source == "evidence/README.md":
        contextual.append(("Reusable artifact template", "evidence/template/index.html"))
    elif source == "evidence/TEMPLATE.md":
        eyebrow = "Publication aid · Not supplied implementation evidence"
        contextual.append(("Evidence overview", "evidence/index.html"))
    else:
        slug = source.split("/")[1]
        contextual.append(("Read project case study", f"projects/{slug}/index.html"))
        contextual.append(("Artifact template", "evidence/template/index.html"))
    contextual.append(("View Markdown source ↗", f"{REPOSITORY}/blob/main/{source}"))
    actions = "".join(f'<a href="{esc(target if target.startswith("https://") else relative(target, page))}">{esc(label)}</a>' for label, target in contextual)
    toc = []
    for match in re.finditer(r"^## (.+)$", content, re.M):
        toc.append(f'<li><a href="#{anchor(match.group(1))}">{esc(match.group(1))}</a></li>')
    parent = "evidence/index.html" if is_evidence else "projects/index.html"
    body = f'''<div class="container document-shell">
      <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{relative('index.html', page)}">Portfolio</a><span aria-hidden="true">/</span><a href="{relative(parent, page)}">{'Evidence' if is_evidence else 'Projects'}</a></nav>
      <header class="document-header"><p class="eyebrow">{esc(eyebrow)}</p><h1>{esc(title)}</h1>{lead}<div class="document-actions">{actions}</div></header>
      <div class="document-layout"><aside class="document-toc"><nav aria-label="On this page"><p class="eyebrow">On this page</p><ul>{''.join(toc)}</ul></nav></aside><article class="document-content">{markdown(content, source, page)}</article></div>
    </div>'''
    return page, shell(page, f"{title} | David Abayateye Lomotey", f"{title}. Public portfolio documentation with October 2026 status, contribution, evidence availability, and review limitations.", body, active, True)


def generate() -> dict[str, str]:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    table = section(readme, "Selected Projects")
    rows = []
    for line in table.splitlines():
        if line.startswith("| **"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) != 3:
                raise ValueError("Expected three cells in README project table")
            rows.append({"name": cells[0].replace("**", ""), "status": cells[1].replace("**", ""), "scope": cells[2]})
    if len(rows) != len(PROJECTS):
        raise ValueError("Expected six README projects")
    files = {"index.html": build_home(readme, rows)}
    for source in ROUTES:
        if source != "README.md":
            page, content = build_document(source, (ROOT / source).read_text(encoding="utf-8"), rows)
            files[page] = content
    page = "404.html"
    files[page] = shell(page, "Page not found | David Abayateye Lomotey", "Return to David Abayateye Lomotey's software portfolio.", '<section class="container not-found"><p class="eyebrow">404 / Page not found</p><h1>Let’s get you<br>back to the work.</h1><p>This page may have moved. Explore the portfolio or browse the project case studies.</p><div class="hero-actions"><a class="button button-primary" href="/Developer/">Portfolio home →</a><a class="button button-outline" href="/Developer/projects/">Project case studies →</a></div></section>')
    # A missing URL can be nested arbitrarily; absolute project paths keep 404 assets usable.
    files[page] = files[page].replace('href="assets/', 'href="/Developer/assets/').replace('src="assets/', 'src="/Developer/assets/').replace('href="index.html', 'href="/Developer/').replace('href="projects/index.html"', 'href="/Developer/projects/"').replace('href="evidence/index.html"', 'href="/Developer/evidence/"')
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when generated HTML is missing or differs from its sources")
    args = parser.parse_args()
    files = generate()
    stale = []
    for page, content in files.items():
        target = OUT / page
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != content:
                stale.append(page)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Regenerate portfolio pages: " + ", ".join(stale))
    print(f"{'Checked' if args.check else 'Generated'} {len(files)} static pages from the public portfolio sources.")


if __name__ == "__main__":
    main()
