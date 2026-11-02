# 0006. Rewrite the question for retrieval only; answer the original

- **Status:** Accepted
- **Date:** 2026-07-14
- **Code:** `app/query_planner.py` (`QueryPlan.normalized_question`, `exact_terms`, `needs_clarification`, `build_search_query`), `app/rerank.py`

## Context

User questions are short, colloquial and context-dependent ("what if something serious
breaks on Enterprise?"). Embedded as-is they retrieve poorly. A model rewrite helps,
but a rewrite can also drop literal terms the documents use (P1, SCIM, 99.9%) or drift
from what the user meant. Some questions are truly ambiguous ("the company plan") and
any guess is a coin flip.

## Decision

1. The planner returns a `normalized_question`: self-contained, specific, in English.
   It is the text used for the semantic search.
2. The planner returns `exact_terms`, which `build_search_query()` **appends** to the
   normalized question, so literals survive the rewrite.
3. The rewrite is used **only for retrieval**. The reranker receives both questions
   plus the exact terms; the answer model receives the **original** question.
4. If the question has more than one reasonable reading with different answers, the
   planner sets `needs_clarification=true` and a `clarification_question`; the
   pipeline returns it **before retrieval**. A question that names no plan is not
   ambiguous — its answer simply covers every plan.
5. The planner runs with `temperature=0`.

## Consequences

- Better recall for colloquial questions without changing what is answered.
- Literal identifiers keep their weight in the embedding.
- Ambiguous questions cost one model call and zero retrieval.
- The clarification is single-turn: the chat has no memory, so the user re-asks the
  full question.
- The clarify/don't-clarify boundary lives in the prompt and its examples, and must be
  covered by evaluation.

## Alternatives considered

- **Embed the raw question** — baseline; misses colloquial and implicit questions.
- **Multi-query / HyDE** — more recall, several embeddings or generations per question.
- **Answer the rewritten question** — a drifted rewrite would silently change the
  answer.
- **Always guess, never clarify** — wrong half of the time on ambiguous questions.
