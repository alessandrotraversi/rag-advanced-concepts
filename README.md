# RAG Knowledge Chat

A Knowledge Chat with RAG built with Python, LangChain (v1) and Postgres with pgvector.

> This repository is an English copy of
> [devfullcycle/mba-ia-rag](https://github.com/devfullcycle/mba-ia-rag) (open-source
> MBA course material), with the code, knowledge base and documentation translated to
> English and an added [design doc](docs/design-doc.md) and
> [Architecture Decision Records](docs/adr/README.md).

The project implements a complete RAG pipeline in small, independent modules: ingestion
and chunking of Markdown documents, vector indexing in Postgres, a **query planner**
(the model interprets the question and plans the search before retrieval),
metadata-filtered vector search and answers with sources. The sample base is the
internal documentation of a fictitious SaaS company (FCAI), but the structure works for
any base of Markdown documents with metadata.

## Documentation

| Document | What it covers |
| --- | --- |
| [docs/design-doc.md](docs/design-doc.md) | How each RAG concept is structured in the code: chunks with metadata, chunk versioning, answers with sources/refusal/debug, question rewriting, query planner, reranking, manifest + hash + idempotent reindexing, and the approval flow |
| [docs/adr/](docs/adr/README.md) | The Architecture Decision Records behind those designs |

## How it works

Flow of a question in the chat:

```
user question
   │
   ▼
query planner (model, structured output)
   │        └── ambiguous question? → returns a clarification question and stops
   ▼
vector search in pgvector
   (normalized question + exact terms, with metadata filters)
   │
   ▼
reranking (model, structured output)
   │        └── no chunk supports the answer? → answers "not found" and stops
   ▼
answer model (structured output)
   │
   ▼
Answer + Sources (sources are built by the application, not by the model)
```

The chat model is called at exactly three points: in the query planner, in the
reranking step and in the final answer. Ingestion and indexing never call the chat
model — only the embedding model.

This flow lives in `app/rag_pipeline.py` and is the same in both usage modes: the
terminal chat (`app/rag_chat.py`) and the HTTP API (`app/api.py`).

## Requirements

- Python 3.11+
- Docker and Docker Compose
- An OpenAI API key

## Setup

1. Create `.env` from the example and fill in `OPENAI_API_KEY` (the example already
   includes the chat model, the embedding model and the database URL):

   ```bash
   cp .env.example .env
   ```

2. Start Postgres with pgvector:

   ```bash
   docker compose up -d
   ```

3. Create the virtual environment and install the dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Validate the environment, the connection and the pgvector extension:

   ```bash
   python -m app.main
   ```

## Preparing the base

```bash
python -m app.ingest   # reads, validates and generates the chunks (data/chunks.jsonl)
python -m app.index    # generates embeddings and indexes them into pgvector
```

`ingest` validates the front matter of every document (required metadata: `title`,
`tenant`, `product`, `plan`, `doc_type`, `version`, `status`, `visibility`) and fails
with a clear error when something is missing. Chunking preserves the Markdown structure
(`MarkdownHeaderTextSplitter` by sections, then `RecursiveCharacterTextSplitter` with
`chunk_size=900` and `chunk_overlap=150`), and every chunk carries the document
metadata plus its own (`chunk_id`, `source_file`, `chunk_index`, `section`,
`content_length`, `document_hash`).

Every chunk is prefixed with a **context header** (title, type, product, plan, version
and section) before it is indexed. Metadata does not reach the embedding — only the
filter — so this header is what makes a chunk taken from the middle of a document
self-explanatory for the search and for the final prompt. The `--no-context-header`
flag generates the chunks without the header, useful to compare retrieval quality with
and without it.

`index` writes the chunks to the `fcai_knowledge_base` table using `chunk_id` as the id
(`PGEngine` + `PGVectorStore`, the current `langchain-postgres` API) and reindexes
**only what changed** since the last run — see the next section.

## Incremental indexing

The pgvector index stays consistent when documents change, without ever reindexing
everything:

- `python -m app.ingest` generates `data/chunks.jsonl` with a `document_hash` (SHA256
  of the complete file, front matter included) in every chunk. The `chunk_id` is
  **deterministic** — `file` + hash prefix + position, e.g.
  `product-support-sla-8f3a91c2b4d0-0001` — so the same content always produces the
  same ids, and an edited document produces new ids.
- `python -m app.index` compares the current chunks with the manifest of the last
  indexing run (`data/index_manifest.json`) and classifies each document:

  | State | Action |
  |---|---|
  | `new` | indexes the document's chunks |
  | `changed` | deletes the old chunks (ids from the manifest) and indexes the new ones |
  | `removed` | deletes the old chunks from the index |
  | `unchanged` | does nothing (no embedding calls) |

- At the end, the manifest is rewritten with the current state (hash, metadata and
  `chunk_ids` per document). Running `index` twice in a row duplicates nothing and
  spends no embeddings; changing a document replaces only its chunks; removing a
  document (and running `ingest` + `index`) cleans its orphan chunks from the index.
- `python -m app.index --force` deletes every chunk registered in the manifest and
  reindexes all current chunks, rebuilding the index from scratch.
- Without a manifest (first indexing run) the table is recreated from scratch, since
  there is no way to know what it contains.
- The chat **never** reindexes documents at runtime: indexing only happens through
  `app.ingest` + `app.index`.

## Using the chat

```bash
python -m app.rag_chat                # the RAG chat
python -m app.rag_chat --debug        # prints the QueryPlan, the retrieved chunks and the selected ones
python -m app.rag_chat --show-prompt  # prints the planner, reranker and answer prompts
python -m app.rag_chat --no-rerank    # skips reranking (uses the top 4 from retrieval)
```

Type `exit` or `quit` to leave.

The answer model returns structured output (`answer`, `has_answer`, `used_chunk_ids`)
and is instructed to answer **only based on the retrieved context**. **Sources are not
written by the model**: the application builds them by joining the `used_chunk_ids`
with the metadata of the chunks that were really retrieved (`source_file`, `title`,
`section`, `version`) — invented ids are discarded. When the context does not support
the answer, the chat says there is not enough information and prints
`Sources: No sources.`.

Questions to watch the planner at work (with `--debug`):

- What if something serious breaks on Enterprise? → normalizes to P1 + SLA,
  `plan=enterprise`
- How does support work on the company plan? → ambiguous, asks for clarification
- What is the support e-mail? → `doc_types` includes `sla` (the e-mail lives in the SLA
  doc)
- What happens if I exceed the ingestion quota? → `plan=null`, the answer covers all
  three plans

## API

The same pipeline as the terminal is exposed as an HTTP API with FastAPI:

```bash
uvicorn app.api:app --reload
```

The API **does not run ingestion or indexing** — `/chat` only queries the index already
created in Postgres. Before using it, prepare the base:

```bash
python -m app.ingest
python -m app.index
```

Endpoints:

- `GET /health` → `{"status": "ok"}`
- `POST /chat` → runs the full pipeline (planner → retrieval → reranking → answer)

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question": "What is the SLA for P1 incidents on the Enterprise plan?"}'
```

Optional request fields: `debug` (default `false`) includes the query plan, the
retrieved chunks and the `selected_chunk_ids` in the response; `use_rerank` (default
`true`) allows skipping the reranking step. An empty question returns `400`; an
ambiguous question returns the clarification question with `needs_clarification=true`.
Sources are built by the application, never by the model, and the API exposes neither
prompts nor secrets.

The `test.http` file at the root has all these requests ready for the VS Code
**REST Client** extension.

## Pipeline observability

Every pipeline run generates a `request_id` (UUID), measures the time of each step
(`query_planning_ms`, `retrieval_ms`, `reranking_ms`, `answer_generation_ms`,
`total_ms`) and aggregates the tokens consumed per model (`model_usage`, via
LangChain's `UsageMetadataCallbackHandler` — cost is not calculated because LangChain
provides tokens, not prices).

- **In the API**, `debug=true` returns the diagnostic information: `request_id`,
  `query_plan`, `retrieved_chunks`, `selected_chunk_ids`, `timings` and `model_usage`.
  With `debug=false` the response stays lean, with none of that.
- **In the terminal**, `--debug` shows the query plan, the retrieved chunks, the
  selected ones and a `Pipeline debug` block with the `request_id`, the timings and the
  tokens per model.
- **Structured logs**: every run emits one JSON line on stdout with `request_id`,
  `has_answer`, `needs_clarification`, `used_rerank`, chunk counts, `source_files`,
  `timings` and `model_usage` (tokens per model) — enough to audit the pipeline
  **without** exposing prompts, full context, documents or credentials. On error, the
  line carries `error_type` and `error_message`, and the API responds `500` with a
  generic message (no stack trace).
- Ingestion and indexing remain separate from the runtime: observability does not
  change the fact that the chat and the API only query the existing index.

## The query planner

The question the user types is almost never the best question to search the database
with. Before retrieval, the chat calls the model with structured output (`QueryPlan`,
in `app/query_planner.py`), which interprets the question and plans the search. Each
field of the plan has a concrete effect:

| Field | What it does |
| --- | --- |
| `normalized_question` | self-contained rewrite of the question; it is the text of the semantic search |
| `exact_terms` | literals (P1, SSO, 99.9%…) appended to the search text, so the embedding does not lose them |
| `doc_types` | becomes the filter `doc_type IN (...)` |
| `plan` | becomes the filter `plan IN [plan, "all"]` |
| `needs_clarification` | stops the flow before retrieval and returns a clarification question |

The original question is still the one the final model answers — the normalized one is
only used for searching.

### Filters: what belongs to the model and what belongs to the application

The model **only suggests content filters** (`doc_types` and `plan`). The safe filters
are fixed in the application and the model never decides on them:

```python
SAFE_FILTERS = {"tenant": "fcai", "product": "fcai-cloud", "status": "published"}
```

Tenant, product, status and authorization are the application's responsibility —
letting the model choose them would mean giving up access control.

### The filter is eliminatory: `doc_types` is a generous list

The metadata filter runs **before** the semantic search, like a `WHERE`: whatever does
not pass it cannot be retrieved, even if it contains exactly the answer. Since the
filter comes from a guess by the model, it needs to be generous — the planner lists
**every** type that might contain the answer, not a single one:

| Question | `doc_types` | Where the answer lives |
| --- | --- | --- |
| How much does the Pro plan cost? | `plan`, `policy` | price section of `pro-plan.md` |
| Does Enterprise have SSO and SCIM? | `plan`, `product` | `enterprise-plan.md` |
| P1 response time on Enterprise? | `plan`, `sla` | `enterprise-plan.md` + `product-support-sla.md` |

When it is impossible to know, the list stays empty and **no type filter is applied**.
Filters increase precision and lower recall; when in doubt, it is better to search
everything.

For the same reason, the type catalog in the planner prompt describes what each type
**really contains**, not what the name suggests — `sla` also covers support channels
and maintenance windows; `company` also covers the contact e-mails of every department.
The planner only sees the base through this catalog.

### When the planner asks for clarification

Only when the question has more than one reasonable reading, each leading to a
different answer. Two cases that look alike are handled differently:

- a question that **points to a specific plan without naming it** ("my plan", "the
  company plan") → ambiguous: asks for clarification instead of guessing;
- a question that **mentions no plan at all** → a single reading, whose answer just
  varies per plan: `plan=null` and the answer covers all of them.

### The contract between the planner and the index

`DocType` and `Plan` are `Literal`s: structured output guarantees the planner never
invents a type. The other side of that guarantee: a new indexed `doc_type` that the
planner does not know can never be chosen — its documents would silently vanish from
every filtered search. That is why the chat validates the contract at startup
(`ensure_planner_covers_index()`): the distinct `doc_type` and `plan` values in the
index are compared with what the planner knows, and the chat exits with a clear
instruction when something is unknown:

```
The index has metadata the planner does not know: faq. Update DocType/Plan and the
catalog in PLANNER_SYSTEM_PROMPT (app/query_planner.py).
```

### Design decisions

- **`temperature=0`** — the planner is a classifier: the same question must produce
  the same plan, including the decision to ask for clarification.
- **`TOP_K=8`** — retrieval is generous on purpose: it brings plenty of candidates for
  the reranker to choose from, instead of cutting the answer out too early.

## Reranking

Retrieval optimizes **recall**: it brings up to 8 candidates that might help. Reranking
(`app/rerank.py`) optimizes **precision**: a model call with structured output
(`RerankResult`) receives the original question, the normalized question, the exact
terms and the candidates, and selects **at most 4 chunk_ids** that directly help answer
— preferring specific chunks over generic ones and chunks that contain the exact terms.
Only the selected chunks go into the final prompt and the sources.

The reranker also works as a safety gate: when no candidate supports the answer, it
returns an empty list and the chat answers "not found" **without calling the final
model** — irrelevant candidates never reach the answer prompt. Ids outside the
candidates are discarded by the application, with the same pattern as the sources.

To inspect and compare:

- `--debug` shows the retrieved chunks (candidates) and then the selected ones;
- `--show-prompt` shows the three prompts, in order: planner, reranker and final
  answer;
- `--no-rerank` skips reranking and sends the top 4 from retrieval straight to the
  final prompt — useful to compare both flows with the same question.

## Isolated retrieval

To inspect the search without calling the chat model:

```bash
python -m app.retrieve "What is the SLA for P1 incidents on the Enterprise plan?"
python -m app.retrieve "What is the SLA for P1?" --top-k 5 --doc-type sla --plan all
```

Accepts `--top-k` and metadata filters (`--tenant`, `--product`, `--plan`,
`--doc-type`, `--status`). For each result it prints the score, `chunk_id`, file,
title, section, plan, type, version, status and an excerpt of the content. Useful to
check whether the right context is being retrieved and to observe the effect of the
filters — the same question with a wrong `--doc-type` shows, in practice, the
eliminatory filter hiding the answer.

## Comparison utilities

- `python -m app.chat` — chat **without RAG**: sends the question straight to the
  model, with streaming. A baseline to compare with the RAG answers.
- `python -m app.context_chat [file.md]` — chat with **an entire document in the
  prompt** (no embeddings, no retrieval). Works for small documents and shows the limit
  that RAG solves: many documents, token cost and selective search.

## Knowledge base

The documents live in `knowledge_base/`: eight Markdown files in English about FCAI,
covering company information (`company`), product overview (`product`), commercial and
billing policies (`policy`), support SLA (`sla`) and one document per plan — Starter,
Pro and Enterprise (`plan`).

Every document has YAML front matter with the required metadata. `plan: all` marks
documents valid for any plan — the plan filter uses `plan IN [plan, "all"]` so they are
never discarded.

### Adding documents

1. Create the `.md` in `knowledge_base/` with the complete front matter.
2. If the document introduces a new `doc_type` or `plan`, update the `DocType`/`Plan`
   `Literal`s **and** the catalog in `PLANNER_SYSTEM_PROMPT` (`app/query_planner.py`) —
   the startup validation points exactly to that if you forget.
3. Regenerate and reindex: `python -m app.ingest && python -m app.index` — only the
   new/changed document is indexed (see **Incremental indexing**).

## Possible uses

- **Internal support assistant** over a company's or product's documentation — swap
  the documents in `knowledge_base/`, adjust the metadata and the `SAFE_FILTERS`.
- **RAG experimentation bench** — each module runs in isolation (retrieval without an
  LLM, chat without RAG, full document in the prompt, full RAG), which allows comparing
  approaches and measuring the effect of each piece (context header, filters, query
  planner) with the debug flags.
- **Foundation for further work** — hybrid search (BM25), a frontend, conversation
  history and answer streaming are natural extensions on top of this structure; none of
  them is implemented.

## Structure

```
app/
  config.py        # loads and validates environment variables
  db.py            # Postgres connection and pgvector extension
  main.py          # environment validation script
  chat.py          # chat without RAG (baseline)
  context_chat.py  # chat with an entire document in the prompt (no RAG)
  ingest.py        # reads, validates and chunks the knowledge_base (with document_hash)
  index.py         # indexes into pgvector only what changed (new/changed/removed)
  manifest.py      # document hashing and reading/writing of index_manifest.json
  retrieve.py      # isolated search in pgvector, with filters (no RAG answer)
  query_planner.py # plans the search: understands the question, builds the filters and searches
  rerank.py        # selects which retrieved chunks go into the final prompt
  rag_pipeline.py  # the complete RAG pipeline, shared by the terminal and the API
  rag_chat.py      # the terminal chat, on top of the pipeline
  api.py           # the HTTP API (FastAPI), on top of the pipeline
docs/
  design-doc.md    # how the RAG concepts are structured
  adr/             # Architecture Decision Records
knowledge_base/    # Markdown documents with metadata front matter
test.http          # ready-made requests for the VS Code REST Client extension
docker-compose.yml
requirements.txt
.env.example
```
