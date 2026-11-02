# 0004. Structured answer, application-built sources and explicit refusal

- **Status:** Accepted
- **Date:** 2026-07-13
- **Code:** `app/rag_pipeline.py` (`RagAnswer`, `SYSTEM_PROMPT`, `build_sources`, `_no_answer`), `app/rerank.py` (`select_documents_by_ids`)

## Context

With a free-text answer, the model can invent sources, cite chunks it never saw, or
answer from prior knowledge. The application has no way to verify any of it. "I don't
know" must also be a reliable, recognizable outcome — not something parsed out of
prose.

## Decision

1. The answer model is bound to a schema with structured output:
   `RagAnswer(answer, has_answer, used_chunk_ids)`.
2. The prompt allows only the given context, forbids invented information or sources,
   and fixes the refusal: `has_answer=false`, the exact `NO_ANSWER_MESSAGE`, empty
   `used_chunk_ids`.
3. **Sources are built by the application**: `used_chunk_ids` are intersected with the
   documents actually sent in the context, de-duplicated, and each surviving document's
   own metadata becomes a `Source(source_file, title, section, version)`. Unknown ids
   are discarded.
4. Refusal is decided at three gates — no retrieval results, empty rerank selection,
   `has_answer=false` — and always returns `NO_ANSWER_MESSAGE` with `sources=[]`.
   The first two gates skip the remaining model calls.
5. Clarification (`needs_clarification=true`) is a distinct outcome from refusal.
6. Terminal and API share one result type, `RagPipelineResult`.

## Consequences

- Every source shown to a user is guaranteed to have been in the prompt, with the
  correct file, section and version.
- Hallucinated citations cannot reach the user; at worst a source is missing.
- Callers can branch on booleans (`has_answer`, `needs_clarification`) instead of
  parsing text.
- The model is still trusted to decide *which* context chunks support the answer and
  whether the answer is supported; that is measured, not enforced.

## Alternatives considered

- **Let the model write citations in the text** — unverifiable.
- **Show every retrieved chunk as a source** — honest but noisy; includes chunks that
  did not support the answer.
- **Detect refusal by keyword** — brittle and language-dependent.
