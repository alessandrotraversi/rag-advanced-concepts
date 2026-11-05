# 0002. Prepend a context header to the chunk text

- **Status:** Accepted
- **Date:** 2026-07-13
- **Code:** `app/metadata.py` (`header_label`, `CONTEXT_HEADER_ORDER`, `MetadataSchema.context_header`), `--no-context-header`

## Context

Metadata is stored next to the vector and used by filters, but it is **not** part of
the embedded text. Many sections are almost identical across documents (e.g. the
"Support" section of the Starter, Pro and Enterprise plans). Embedded alone, a chunk
like "P1: response within 8 business hours" does not say *which plan* it is about, so
the search confuses them and the answer model cannot tell them apart either.

## Decision

Before indexing, prefix every chunk's text with a header built from its metadata:

```
Document title: <title>
Document type: <doc_type>
Product: <product>
Plan: <plan>
Version: <version>
Section: <section>
```

Empty fields are omitted. The header is on by default; `python -m app.ingest
--no-context-header` disables it for comparison. Because the header already carries
title, section, plan and version, the answer prompt only adds the `Chunk ID`.

## Consequences

- Retrieval distinguishes plan-specific chunks; a chunk is self-explanatory both to the
  embedding model and to the answer model.
- The answer prompt stays small (`format_context()` only adds the id).
- Every chunk is ~100 characters longer: more embedding and prompt tokens.
- Changing the header fields changes every chunk text but **not** the file hash; the
  index must be rebuilt with `index --force` (see ADR 0010).

## Alternatives considered

- **Rely on metadata filters only** — works only when the planner guesses the right
  filter; does not help the answer model.
- **Embed metadata separately / multi-vector** — more complex storage and queries for
  the same effect.
- **LLM-generated contextual summaries per chunk** — better context, but costs a chat
  model call per chunk at ingestion and is not deterministic.
