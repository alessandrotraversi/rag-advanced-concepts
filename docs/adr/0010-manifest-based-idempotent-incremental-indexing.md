# 0010. Manifest-based, idempotent incremental indexing

- **Status:** Accepted · Amended by [0012](0012-version-registry-with-split-hashes-and-index-fingerprint.md) (index fingerprint, `metadata_only` state)
- **Date:** 2026-07-14
- **Code:** `app/manifest.py`, `app/index.py` (`classify_sources`, `manifest_entry`, `main`)

## Context

The first version recreated the table on every `index` run: every run re-embedded the
whole base (time and money) and the index was empty while it ran. Simply appending new
chunks instead would leave chunks of previous versions and of deleted documents in the
index, and they would keep being retrieved.

## Decision

1. `ingest` stamps every chunk with `document_hash` (SHA-256 of the full file) and a
   deterministic `chunk_id` (ADR 0003).
2. After each successful run, `index` writes `data/index_manifest.json`: `pipeline`,
   `indexed_at`, and per `source_file` the `document_hash`, `title`, `tenant`,
   `product`, `version`, `status` and the list of `chunk_ids` in the index.
3. On the next run, each source is classified against the manifest:
   `new` → add; `changed` (hash differs) → delete the manifest's ids, add the new
   chunks; `removed` (in the manifest, not in the chunks) → delete; `unchanged` →
   nothing.
4. If there is no manifest or the table does not exist, the state is unknown: the
   table is recreated and everything is indexed.
5. `--force` deletes every id recorded in the manifest and re-adds all chunks.
6. The chat and the API never index.

## Consequences

- Re-running `index` with no changes performs no writes and no embedding calls.
- Editing or deleting one document touches only its chunks; no orphans remain.
- Because ids are deterministic and the store upserts on `chunk_id`, an interrupted run
  can be repeated safely.
- The manifest is local state that must stay paired with its database.
- `pipeline` is recorded but not compared: changing chunking parameters, the context
  header or the embedding model requires `--force`.
- Delete and add are not atomic.

## Alternatives considered

- **Always rebuild** — simple, costly, causes downtime.
- **Query the table for existing hashes instead of a manifest** — no extra file, but
  couples indexing to the table's metadata layout and needs a scan.
- **LangChain `RecordManager` / indexing API** — similar semantics, but adds an extra
  table and is less transparent for teaching purposes.
