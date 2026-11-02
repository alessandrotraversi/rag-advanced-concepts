# 0009. LLM reranking as the precision step and a refusal gate

- **Status:** Accepted
- **Date:** 2026-07-14
- **Code:** `app/rerank.py` (`RERANK_TOP_N`, `RerankResult`, `build_rerank_prompt`, `select_reranked_documents`), `app/rag_pipeline.py`

## Context

Retrieval is deliberately generous (`TOP_K=8`) to protect recall. Passing all
candidates to the answer model adds tokens, dilutes attention and invites it to cite
chunks that are only *similar*. Vector scores alone do not know about exact terms or
which plan a chunk belongs to.

## Decision

1. After retrieval, one structured-output call returns
   `RerankResult(selected_chunk_ids)`: at most `RERANK_TOP_N=4`, best first, only
   chunks that directly help, preferring specific chunks and chunks with the exact
   terms, and **an empty list when no candidate supports the answer**.
2. The prompt includes the original question, the normalized question, the exact terms
   and each candidate's id, source, title, section, version and content.
3. The application keeps only ids that were real candidates, de-duplicates, keeps the
   model's order and truncates to 4 (`select_reranked_documents`).
4. An empty selection returns the refusal **without calling the answer model**.
5. `--no-rerank` / `use_rerank=false` uses the top 4 by similarity, for comparison.

## Consequences

- Smaller, more relevant final prompts and sources.
- Irrelevant context never reaches the answer model; out-of-scope questions are refused
  one step earlier.
- One extra model call per question (`reranking_ms`, tokens in `model_usage`).
- The reranker can wrongly drop the right chunk; `--debug` shows retrieved vs selected
  to diagnose it.

## Alternatives considered

- **No reranking (top-k straight to the answer)** — kept as a flag; lower precision.
- **Cross-encoder reranker (e.g. bge-reranker, Cohere Rerank)** — faster per call and
  purpose-built, but an extra model/service to host or pay for, and it ignores the
  planner's exact terms.
- **Score threshold on vector similarity** — scores are not calibrated across
  questions.
