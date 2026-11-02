# 0011. Publication status as the approval gate

- **Status:** Accepted
- **Date:** 2026-07-14
- **Code:** `app/ingest.py` (`REQUIRED_METADATA`), `app/query_planner.py` (`SAFE_FILTERS`, `build_filters`), `app/index.py` (`manifest_entry`), `app/retrieve.py` (`--status`)

## Context

A knowledge base contains content at different stages: drafts, content under review,
approved content and retired content. Only approved content may be used to answer
users. The approval must not depend on the model's judgment, must survive prompt
injection, and must be auditable.

## Decision

1. The lifecycle state of a document is the mandatory front-matter field `status`
   (`draft` → `published` → `archived`); `visibility` is also mandatory.
2. Approving a document is an **edit to the document** (`status: published`), reviewed
   through the normal Git workflow (pull request). The edit changes the file hash, so
   the next `ingest` + `index` replaces its chunks (ADR 0003, ADR 0010).
3. The index may contain documents in any state, but the query path always applies
   `status = "published"` through the application-owned `SAFE_FILTERS` (ADR 0007).
   The planner cannot change it.
4. Reviewers can inspect how unpublished content would be retrieved with
   `python -m app.retrieve --status draft "<question>"`, outside the chat and the API.
5. The manifest records `status` and `version` per document; sources expose `version`.

## Consequences

- No unapproved content can reach an answer, regardless of the question.
- Approval, its reviewer and its timestamp are in Git history, not in the index.
- Drafts can be indexed and tested before publication without a second index.
- `status` values are not validated: a typo makes a document silently unanswerable.
  Validating allowed values at ingestion is the next step.
- `visibility` is not yet enforced as a filter; it is reserved for caller-based access
  control once callers are authenticated.
- Drafts count for the planner↔index contract check (ADR 0008).

## Alternatives considered

- **Keep drafts out of the repository / out of the index** — safe, but prevents
  testing drafts against the real retrieval.
- **Separate index per status** — strong isolation, double indexing and configuration.
- **Approval metadata in the index (approved_by, approved_at)** — duplicates Git
  history; could be added if documents stop living in Git.
