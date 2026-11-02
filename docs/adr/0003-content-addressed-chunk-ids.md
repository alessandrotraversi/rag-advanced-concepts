# 0003. Version chunks with content-addressed, deterministic ids

- **Status:** Accepted
- **Date:** 2026-07-14
- **Code:** `app/manifest.py` (`document_hash`), `app/ingest.py` (`chunk_id`), `app/index.py`

## Context

Documents are edited over time. The system must (a) know which version of a document
an answer used, (b) never keep old and new chunks of the same document live at the same
time, and (c) not duplicate rows when the same content is indexed twice. Random ids
(UUIDs) satisfy none of these.

## Decision

1. Keep two version signals:
   - `version` (front matter, e.g. `2026-01`) — the **editorial** version, owned by the
     author, shown in the context header, rerank candidates and every `Source`;
   - `document_hash` — SHA-256 of the **complete raw file**, front matter included —
     the **content** version, owned by the code.
2. Derive the chunk id from the content version:
   `chunk_id = f"{file_stem}-{document_hash[:12]}-{chunk_index:04d}"`.
3. Use `chunk_id` as the primary key of the pgvector table.
4. Keep exactly **one live version per document**; history is kept by Git.

## Consequences

- Same bytes ⇒ same ids: re-indexing is an upsert, never a duplicate.
- Any edit (even front-matter only, such as a `status` change) ⇒ new hash ⇒ new ids;
  old and new chunks never collide and a change is handled as delete-old + add-new.
- A chunk id in a log or source identifies document **and** content version.
- Identical text in different positions gets different ids (position is part of the
  id) — intended.
- `version` is not checked against the hash: a forgotten bump leaves a stale label in
  citations while the index stays correct.
- Historical questions ("what was the price in 2025?") are not supported.

## Alternatives considered

- **UUID per chunk** — duplicates on re-run, no way to relate rows to a version.
- **Hash per chunk text** — stable across unrelated edits, but a document could end up
  with a mix of old and new chunks, and front-matter-only changes would go unnoticed.
- **`version` as the only version signal** — depends on humans remembering to bump it.
- **Multiple live versions with `version` as a filter** — more power, but every query
  would need a version policy; not needed for the use case.
