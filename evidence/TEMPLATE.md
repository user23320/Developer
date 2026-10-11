# Artifact record template

[Evidence index](README.md)

Copy this file into a project evidence folder and replace the fields before using it. **This is a reusable template, not a supplied artifact or a record of completed checks.** For a copied record, change the navigation link above to `../README.md`.

## Identity and availability

| Field | Value to supply |
| --- | --- |
| Project and artifact title | Exact project name and a descriptive title |
| Artifact type | Screenshot, walkthrough, architecture, academic document, testing summary, or permitted code sample |
| Availability | **Available**, **Private**, or **Planned**, using the evidence index definitions |
| Readiness | Published; prepared for authorized private review; readiness unconfirmed; or not prepared |
| Public artifact link | Link to the actual published file/page only when it exists; otherwise write “Not published” |
| Created or captured | Actual date, or “Not recorded” |
| Project version or stage | Public-safe version identifier or design/MVP stage; do not substitute a portfolio commit for an application version |
| Contributor and source | Who created it and whether it is an author account, sample demonstration, or recorded test |
| Sanitization review | Actual review date and safe reviewer attribution, or “Pending” |
| Permission basis | Owner authorization or other applicable permission; write “Pending” if not established |

**Private** records must not contain private URLs, storage paths, credentials, or account-access instructions. State whether review is conditional or ready without attaching the private material. **Planned** records must not include placeholder download links or imply a completed artifact.

## What this artifact shows

Describe the specific workflow, component, design, or contribution that can be inspected. Separate implemented behavior from proposed behavior. State whether the material uses fictional data, a sandbox, a simulation, or an approved sanitized observation.

## How to review it

Give public-safe steps for inspecting the artifact. For a recording, identify the relevant sequence or timestamps. For a code sample, describe its isolated purpose and any synthetic inputs. Do not request production-account access or real transactions.

## Checks actually performed

| Check | Expected result | Observed result | Date and conditions |
| --- | --- | --- | --- |
| Replace with a check that was actually run | State the expectation | Record the observation, including failures | State the date, version/stage, and relevant conditions |

If no checks were performed, replace the table with “No test results supplied.” Proposed checks belong in a separate planned section. Do not invent results, adoption figures, performance measurements, or independent approval.

## Limitations

State what the artifact cannot verify: for example, security, synchronization reliability, full feature completion, production performance, authorship, nationwide operational coverage, or academic approval. Identify any untested steps and simulated statuses.

## Publication review

Record the outcome of each applicable check from the [publication checks](README.md#publication-checks) in the evidence index. In a copied project record, change that link to `../README.md#publication-checks`.

- Secrets, credentials, access tokens, and session details removed: **Pending**
- Identifying records and actual payment data excluded; demonstration data labelled: **Pending**
- Private infrastructure, configuration, schemas, and protected logic excluded: **Pending**
- Final images, video frames, documents, metadata, and code inspected: **Pending**
- Publication permission and attribution established where required: **Pending**
- Links, scope, dates, and availability labels checked: **Pending**

Change each item to an accurate outcome only after checking it; explain “Not applicable” when appropriate. Keep an artifact **Planned** until publication permission and sanitization are complete and the public artifact is accessible. For private review, state readiness separately and keep the material outside Git.
