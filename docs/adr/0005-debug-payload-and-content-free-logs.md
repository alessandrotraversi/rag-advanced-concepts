# 0005. Opt-in debug payload and content-free structured logs

- **Status:** Accepted
- **Date:** 2026-07-14
- **Code:** `app/rag_pipeline.py` (`RagDebug`, `PipelineTimings`, `ModelUsage`, `_log_run`), `app/rag_chat.py`, `app/api.py`

## Context

A RAG answer is the product of several steps (plan, filters, retrieval, rerank,
answer). When an answer is wrong, the cause is usually upstream of the answer model.
Developers need to see every step; operators need per-request metrics; and neither
should leak prompts, documents or secrets into logs or API responses.

## Decision

1. Every run gets a `request_id` (UUID), per-step timings and token usage per model
   (`UsageMetadataCallbackHandler`).
2. A `RagDebug` object (query plan + search query + filters, retrieved chunks with
   score and a 300-char preview, selected chunk ids, timings, model usage) is **always
   built** and returned only when asked (`--debug`, `"debug": true`).
3. Prompts are shown only in the terminal, through an `on_prompt` callback
   (`--show-prompt`); the API never returns them.
4. Every run writes **one JSON log line** with ids, flags, counts, source file names,
   timings and token usage — never prompts, chunk text, answers or credentials. Errors
   add `error_type`/`error_message`; the API answers a generic `500`.

## Consequences

- A wrong answer can be traced to the step that caused it with the same tooling in the
  terminal and in the API.
- Logs are safe to ship to a shared log system.
- Cost is visible as tokens; prices are not computed (LangChain provides tokens only).
- Debug previews do contain document text — acceptable because debug is opt-in and the
  documents are internal.

## Alternatives considered

- **Log full prompts and answers** — easiest to debug, unacceptable for privacy.
- **Separate debug endpoint** — duplicates the pipeline; a flag on the same call keeps
  one code path.
- **Tracing platform from day one** — explored in later branches
  (OpenTelemetry/Langfuse); out of scope here.
