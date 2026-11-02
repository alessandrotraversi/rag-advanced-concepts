# 0008. Generous `doc_types` filter and a planner↔index contract check

- **Status:** Accepted
- **Date:** 2026-07-14
- **Code:** `app/query_planner.py` (`PLANNER_SYSTEM_PROMPT` rule 3, `build_filters`, `ensure_planner_covers_index`)

## Context

Metadata filters run as a `WHERE` before similarity ranking: anything filtered out
cannot be retrieved, even if it holds the exact answer. In this base the same fact
often lives in several document types (a plan's price is in `policy` and in `plan`;
the support e-mail is in `sla`, `company` and `plan`). A planner that picks a single
"best" type will hide answers.

A second failure mode is silent: if a document is indexed with a `doc_type` or `plan`
the planner's `Literal`s do not contain, the planner can never select it and the
document disappears from every filtered search without any error.

## Decision

1. `doc_types` is a **list**, and the prompt asks for **every** type that could hold
   the answer, with concrete multi-type examples. When unsure, the list is empty and
   **no type filter** is applied.
2. `plan` is filled only when the question is about exactly one plan; comparisons and
   plan-less questions leave it `null`.
3. At pipeline startup, `ensure_planner_covers_index()` reads the distinct
   `doc_type`/`plan` values from the table and exits with an actionable message if any
   value is unknown to the planner (`plan=all` is always allowed).

## Consequences

- Recall is protected: a too-wide filter costs a little precision (recovered by the
  reranker), a too-narrow one would cost the answer.
- Adding a new document type is a two-place change (`Literal` + catalog), and forgetting
  it fails loudly at startup instead of silently degrading answers.
- The startup check needs the database and runs on every `RagPipeline` creation.

## Alternatives considered

- **Single `doc_type`** — simpler schema, hides multi-type answers.
- **Filter as a soft boost instead of a hard filter** — not supported by the
  `PGVectorStore` filter API without custom SQL.
- **Free-text `doc_type`** — no `Literal` safety; invented types would return nothing.
