# Architecture Decision Records

Each ADR records one decision: the context that forced it, what was decided, and the
consequences we accepted. The [design doc](../design-doc.md) explains how the pieces
fit together; the ADRs explain **why** each piece is the way it is.

Format: [Michael Nygard's template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
(Status · Context · Decision · Consequences), plus the alternatives that were considered.

| ADR | Title | Status | Design doc section |
| --- | --- | --- | --- |
| [0001](0001-markdown-aware-chunking-with-document-metadata.md) | Markdown-aware chunking with document metadata on every chunk | Accepted | 3. Chunks with metadata |
| [0002](0002-context-header-in-chunk-text.md) | Prepend a context header to the chunk text | Accepted | 3. Chunks with metadata |
| [0003](0003-content-addressed-chunk-ids.md) | Version chunks with content-addressed, deterministic ids | Superseded by 0012 | 4. Chunks with versioning |
| [0004](0004-structured-answer-with-application-built-sources.md) | Structured answer, application-built sources and explicit refusal | Accepted | 5. Sources, refusal and debug |
| [0005](0005-debug-payload-and-content-free-logs.md) | Opt-in debug payload and content-free structured logs | Accepted | 5. Sources, refusal and debug |
| [0006](0006-rewrite-the-question-for-retrieval-only.md) | Rewrite the question for retrieval only; answer the original | Accepted | 6. Improving the question |
| [0007](0007-llm-query-planner-with-application-owned-safe-filters.md) | LLM query planner with application-owned safe filters | Accepted | 7. Query planner |
| [0008](0008-generous-doc-type-filter-and-planner-index-contract.md) | Generous `doc_types` filter and a planner↔index contract check | Accepted | 7. Query planner |
| [0009](0009-llm-reranking-as-precision-step-and-refusal-gate.md) | LLM reranking as the precision step and a refusal gate | Accepted | 8. Reranking |
| [0010](0010-manifest-based-idempotent-incremental-indexing.md) | Manifest-based, idempotent incremental indexing | Accepted (amended by 0012) | 9. Manifest, hash and reindexing |
| [0011](0011-publication-status-as-approval-gate.md) | Publication status as the approval gate | Accepted (amended by 0012) | 10. Approval flow |
| [0012](0012-version-registry-with-split-hashes-and-index-fingerprint.md) | Version registry with split hashes and an index fingerprint | Accepted | 4. Chunks with versioning, 9. Manifest, hash and reindexing |

## Adding an ADR

1. Copy [template.md](template.md) to `NNNN-short-title.md` with the next number.
2. Start with `Status: Proposed`; change it to `Accepted` when merged.
3. Never rewrite an accepted ADR — supersede it with a new one and link both ways.
4. Add it to the table above.
