# 0007. LLM query planner with application-owned safe filters

- **Status:** Accepted
- **Date:** 2026-07-14
- **Code:** `app/query_planner.py` (`QueryPlan`, `DocType`, `Plan`, `SAFE_FILTERS`, `build_filters`, `TOP_K`)

## Context

Documents carry structured metadata (type, plan, tenant, status) that pure vector
similarity ignores. Filtering by type and plan improves precision, but the right filter
depends on the meaning of the question. Some filters, however, are not about meaning at
all: tenant, product and publication status are **authorization**, and must not depend
on anything the user (or an injected document) can influence.

## Decision

1. Before retrieval, one structured-output call (`temperature=0`) returns a
   `QueryPlan` with `doc_types: list[DocType]`, `plan: Plan | None`, plus the question
   fields from ADR 0006. `DocType` and `Plan` are `Literal`s.
2. `build_filters()` always starts from
   `SAFE_FILTERS = {"tenant": "fcai", "product": "fcai-cloud", "status": "published"}`
   and only **adds** `doc_type IN doc_types` and `plan IN [plan, "all"]`.
3. The model is never asked about, and can never output, tenant, product, status or
   visibility.
4. Retrieval takes `TOP_K=8` candidates (generous; precision is the reranker's job).
5. The planner prompt contains a catalog that describes what each `doc_type`
   **actually contains** — it is the planner's only view of the base.

## Consequences

- Filters are always valid values and safe filters cannot be widened by a prompt
  injection.
- Including `"all"` keeps cross-plan documents (SLA, policies) in plan-filtered
  searches.
- One extra model call per question (latency + tokens), visible in `query_planning_ms`.
- The catalog must be maintained together with the documents (enforced by ADR 0008).

## Alternatives considered

- **No filters** — simplest, but plan-specific sections get mixed.
- **Rule-based filter extraction (keywords)** — cheap and deterministic, but brittle
  with paraphrases ("serious problem" → P1).
- **Let the model choose every filter, including tenant/status** — gives up access
  control to the model.
- **LangChain self-query retriever** — same idea, but less control over the prompt,
  the safe filters and the debug output.
