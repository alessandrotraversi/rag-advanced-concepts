# 0001. Markdown-aware chunking with document metadata on every chunk

- **Status:** Accepted
- **Date:** 2026-07-09
- **Code:** `app/ingest.py` (`load_document`, `chunk_document`), `app/metadata.py` (`METADATA_SCHEMA`)

## Context

The knowledge base is a set of Markdown documents about different plans, document
types and products. Retrieval must be filterable (tenant, product, plan, type, status)
and answers must cite file, section and version. A chunk that does not know where it
came from supports neither.

Fixed-size splitting of the raw text cuts across headings and tables, and mixes
unrelated sections in one chunk.

## Decision

1. Every document declares its metadata once, in YAML front matter. The keys `title`,
   `tenant`, `product`, `plan`, `doc_type`, `version`, `status` and `visibility` are
   **mandatory**; ingestion fails with a clear error when any is missing, when the file
   or body is empty, or when there is no front matter.
2. Chunking is two-stage: `MarkdownHeaderTextSplitter` (h1/h2/h3) first, then
   `RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)` for long
   sections.
3. Every chunk copies **all** document metadata and adds `chunk_id`, `source_file`,
   `chunk_index`, `section` (most specific heading), `content_length` and
   `document_hash`.
4. Chunks are written to `data/chunks.jsonl` (`{"content", "metadata"}` per line), a
   reviewable artifact between ingestion and indexing.

## Consequences

- Any metadata field can be used as a pgvector filter and as a source attribute with
  no extra lookup.
- Sections stay coherent; `section` gives precise citations.
- Metadata is duplicated in every row (cheap at this scale).
- Required keys are checked for presence, not for allowed values (see ADR 0008 and
  ADR 0011 for where values are enforced).
- Ingestion and indexing are separate commands; `chunks.jsonl` can be inspected or
  diffed before spending embeddings.

## Alternatives considered

- **Fixed-size character chunks** — simpler, but break headings/tables and lose the
  section.
- **Metadata in a separate table joined at query time** — normalized, but filters
  would need a join and `PGVectorStore` filters work on the row metadata.
- **Optional metadata with defaults** — silently produces chunks that no filter can
  find.
