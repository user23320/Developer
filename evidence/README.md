# Evidence index

[Portfolio](../README.md) · [Project case studies](../projects/README.md) · [Reusable artifact template](TEMPLATE.md)

This directory gives reviewers one place to find public references and future sanitized artifacts for the six portfolio projects. Inventory reviewed on **11 October 2026**.

**Published now:** this index, six project indexes, and the reusable template. The existing case studies and their public links are listed below. No screenshot collection, demonstration package, architecture package, completed academic report/presentation, application code sample, or test-results package is attached here yet. Creating an index does not establish that those artifacts exist.

## Availability labels

| Label | Meaning | What a reviewer can inspect |
| --- | --- | --- |
| **Available** | An existing repository document or a public reference carried forward from the case study, with a link and its limits stated. | The linked document or public-facing page. External sites can change; their availability and workflows were not retested for this inventory update. |
| **Private** | Material stays outside the public repository. A review may require owner/academic permission and preparation; readiness is stated for each item. | Only a separately arranged, authorized, sanitized review. This label does not promise that a review package is ready. |
| **Planned** | A candidate artifact has no published file or demonstration link in this repository. | Its proposed scope only. It is not completed evidence or a delivery commitment. |

Project maturity and evidence availability are separate. A live system can have planned evidence; an available design document does not make an MVP or academic prototype a production deployment.

## Project indexes

| Project | Evidence index | Available scope |
| --- | --- | --- |
| DALEAM EDU | [Open index](daleam-edu/README.md) | Author-written case study and public product-page references |
| Assist Shop Management (DALEAM WEB) | [Open index](assist-shop-management/README.md) | Author-written case study, public product pages, and a recorded homepage tutorial reference |
| Real Tech Electricals | [Open index](real-tech-electricals/README.md) | Author-written case study and public website reference |
| EasyShopen | [Open index](easyshopen/README.md) | Author-written case study and public storefront/service references |
| SafeRide GH Rider | [Open index](saferide-gh-rider/README.md) | Author-written MVP scope; the company website is a general contact link |
| Smart Campus Environment Monitoring System | [Open index](smart-campus-environment-monitoring/README.md) | Author-written academic design scope |

Case studies record the developer's account and, where stated, earlier public-page reviews. They are not independent verification of authorship, feature completion, security, performance, adoption, academic approval, or commercial outcomes. Repository commits document this portfolio, not the proprietary applications' development history.

## Adding an artifact

1. Prepare an authorized, sanitized artifact using fictional demonstration data. Keep raw and private material outside this repository, including branches and history.
2. Copy [TEMPLATE.md](TEMPLATE.md) into the relevant project folder as an artifact record. Use a descriptive filename, such as `pos-demo-2026-10-11.md`; the example is a naming pattern, not an existing artifact.
3. Record the capture/creation date, version or design stage, contributor/source, permission basis, review date, demonstrated scope, and limitations. Report only checks and results actually performed.
4. Add the sanitized asset alongside its record, or in a project subfolder such as `screenshots/`, `architecture/`, `reports/`, or `code/` when needed. Create folders when they contain real artifacts; do not add empty collections or placeholder download links.
5. Apply the publication checks below to the final exported files. For **Private** items, keep the files elsewhere and record only safe availability information; do not include private file locations or access instructions.
6. Mark an item **Available** only after its public file or permitted public link exists and is reviewable. Link the record from the project index, state what it proves, and update the inventory date and any affected README availability wording.

## Publication checks

- Exclude credentials, passwords, PINs, tokens, API keys, session identifiers, and secrets from every file, frame, URL, log, and code sample.
- Replace customer, student, parent, employee, shop, order, and transaction records with fictional demonstration data. Exclude actual payment data, account details, receipts, and private database contents. Label simulated or sandbox payment statuses clearly.
- Exclude private infrastructure: internal hostnames, IP addresses, server paths, configuration, connection strings, deployment files, and protected schemas. Use generic components for architecture summaries.
- Exclude protected business logic and internal commercial rules. Any code sample must be a permitted, isolated example whose scope and origin are stated.
- Check image/video frames, browser chrome, filenames, document properties, hidden sheets, comments/revisions, and export metadata. Remove sensitive content before export and inspect the final result; publish only the sanitized version.
- Record the permission basis where another owner, organization, participant, or academic site is involved. A private report's existence does not establish permission to republish it or supervisor approval.
- State whether the artifact is a design, synthetic walkthrough, test result, or production observation. Do not infer completion, independent validation, measured outcomes, or nationwide coverage from a screenshot or public website.

These requirements apply to both public artifacts and separately arranged private reviews. Production accounts and live customer data are outside the portfolio review scope.
