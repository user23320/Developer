# Portfolio website — publishing and maintenance

[Portfolio README](README.md) · [Website source](docs/index.html) · [Evidence inventory](evidence/README.md)

The static website presents the existing public portfolio content in a responsive layout. It contains a home page, a project directory, six complete case studies, an evidence directory, six project evidence indexes, the reusable artifact template, and a 404 page. It adds no application screenshots, private data, testimonials, metrics, completed-feature demonstrations, or new operational claims.

## Publish on GitHub Pages

At the initial check on 11 October 2026, `user23320/Developer` had GitHub Pages disabled. The website files are ready in `docs/`; availability at the intended URL must be checked after activation.

1. Open [the repository's Pages settings](https://github.com/user23320/Developer/settings/pages).
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. Select **main** and **/docs**, then **Save**.
4. Wait for GitHub's Pages deployment to complete. Check its status under **Actions** and the link shown in Pages settings.
5. The expected project-site address is `https://user23320.github.io/Developer/`. Confirm it loads before representing the site as published or adding it as an available public reference.

This branch publishing setup follows [GitHub's official publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). The checked-in HTML, CSS, JavaScript, SVG favicon, and `.nojekyll` marker require no framework, package installation, secret, or custom deployment workflow. Production application domains and hosting are separate from this portfolio.

## Content sources

| Website area | Source |
| --- | --- |
| Profile, focus, skills, stack, home project summaries/status, contact | `README.md` |
| Project directory and full case studies | `projects/README.md` and the six project Markdown files |
| Evidence overview, availability definitions, publication checks | `evidence/README.md` |
| Project evidence details | The six `evidence/<project>/README.md` files |
| Artifact record template | `evidence/TEMPLATE.md` |

The Python standard-library generator in `scripts/build_portfolio.py` converts these public documents into checked-in static pages. The existing Markdown remains the source of truth. Project categories and the presentation layout are defined in the generator; styles and progressive menu behavior live in `docs/assets/`.

## Update and validate

From the repository root, run:

```sh
python3 scripts/build_portfolio.py
python3 scripts/build_portfolio.py --check
python3 scripts/validate_portfolio.py
node --check docs/assets/site.js
```

Commit both the source-document changes and the regenerated HTML. With branch publishing enabled, changes to `main` / `docs` are published by GitHub. Changes only to Markdown do not regenerate the site automatically; run the generator before committing them. Do not edit generated HTML directly.

The generator intentionally supports the headings, paragraphs, simple lists, links, emphasis, code spans, and tables used by the current sources. It escapes raw HTML, rejects unsupported block types, and rejects unmapped local documents. Extend its renderer before adding different Markdown constructs or new project routes. `--check` verifies the output matches the current sources.

The validator checks local routes/assets and fragment targets, the GitHub Pages `/Developer/` path, page metadata and landmarks, the six exact README status labels, separate evidence headings, and public-link boundaries. It does not exercise the proprietary applications or retest external product websites.

## Review the presentation

After publication, check widths of approximately **320, 375, 768, and 1440 pixels**, including the home page, a long case study, and each evidence table. Verify the menu, keyboard focus, Escape-to-close behavior, internal links, readable tables, and the 404 page. Disable JavaScript once to confirm the navigation and all public content remain accessible. The mobile table layout preserves column labels alongside each value.

Structural/content checks and JavaScript syntax validation were performed during preparation. Browser layout and interaction testing were unavailable in that environment and remain to be checked on the published site. The responsive CSS, semantic HTML, and progressive enhancement support mobile access; this statement is not a claim of completed cross-browser testing.

## Status and publication boundaries

- Keep the recorded **October 2026** project status wording and **11 October 2026** evidence inventory until a new review justifies a dated update. The website does not silently replace historical observations with fresh verification claims.
- Keep **Available**, **Private**, and **Planned** distinct. A public product link does not verify private features, and a live project can have planned supporting evidence. The company link for SafeRide remains a general contact reference; Smart Campus remains an academic design.
- Keep all six original case studies and evidence indexes in the repository. The presentation layer does not supersede their scope or limitations.
- Website implementation files are not proprietary application source-code samples or evidence of those systems' performance. Website validation results do not belong in a project's application test-results package.
- Follow the existing [publication checks](evidence/README.md#publication-checks) before adding artifacts. Exclude credentials, customer/student records, actual payment data, private infrastructure/configuration, database contents, and protected business logic from files, branches, and history.
- Preserve real public links and the contact details already recorded in the README. Do not create a contact form without a delivery service, a placeholder download, a private access link, or a promise of a ready demonstration package.
