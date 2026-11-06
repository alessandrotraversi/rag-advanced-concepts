# 0012. Version registry with split hashes and an index fingerprint

- **Status:** Accepted
- **Date:** 2026-11-06
- **Supersedes:** [0003](0003-content-addressed-chunk-ids.md) · **Amends:** [0010](0010-manifest-based-idempotent-incremental-indexing.md), [0011](0011-publication-status-as-approval-gate.md)
- **Code:** `app/versioning.py` (`DocumentVersion`, `VersionRegistry`, `index_fingerprint`), `app/metadata.py` (`Scope.VERSION`, `pattern`), `app/ingest.py` (`check_editorial_versions`), `app/index.py` (`update_metadata`, `main`)

## Context

Versioning was spread over three modules (`manifest.py`, `metadata.py`, `index.py`) and
relied on a single `document_hash` of the raw file. That had four problems:

1. The manifest recorded `pipeline: rag-v1` but never compared it. Changing the
   embedding model left vectors from two models in one table (or failed on the vector
   dimension) while every document looked `unchanged`.
2. One hash for everything: a front-matter-only edit such as `status: draft →
   published` produced new chunk ids and re-embedded the whole document, although the
   embedded text was identical.
3. The editorial `version` was never checked: an author could edit the body and forget
   to bump it, leaving a stale label in every citation.
4. `version` had no format, so `2026-1`, `v2` or `jan` were all accepted.

## Decision

1. **One module owns versioning.** `app/versioning.py` holds `DocumentVersion` (the
   version of one document and its chunk-id rule) and `VersionRegistry` (the manifest:
   load, atomic write, diff, rebuild decision, editorial check).
2. **Three hashes, one job each**, computed once per document and stamped on every
   chunk through the new `Scope.VERSION` of the metadata schema:

   | Hash | Covers | A change means |
   | --- | --- | --- |
   | `embedding_hash` | the final chunk texts (context header included) | new `chunk_id`s, delete + re-embed |
   | `metadata_hash` | the front matter | update the stored JSON metadata in place, no embeddings |
   | `body_hash` | the Markdown body as written | the author must bump `version` |

   `chunk_id = f"{file_stem}-{embedding_hash[:12]}-{chunk_index:04d}"`.
3. **The index has a fingerprint**: hash of the embedding model, table name and
   manifest format. If it differs from the manifest's (or the manifest has an older
   format), the table is rebuilt. Chunking parameters and the context header are not in
   the fingerprint because they change the chunk texts, which `embedding_hash` already
   catches per document.
4. **The diff gains a state**: `new`, `changed`, `metadata_only`, `unchanged`, `removed`.
5. **Editorial versions are validated**: `version` must match `YYYY-MM`
   (`MetadataField.pattern`), and `ingest` warns when `body_hash` changed since the last
   index but `version` did not; `ingest --strict-versions` turns the warning into an
   error.

## Consequences

- Changing `OPENAI_EMBEDDING_MODEL` rebuilds the index automatically; `--force` is only
  needed to recover from a corrupted state.
- Approving a document (status change) costs zero embedding calls and keeps its chunk
  ids; the `status` filter sees the new value immediately after `index`.
- A `version` bump changes the context header, so it re-embeds the document — intended,
  since the label is part of the embedded text.
- Changing chunk size, overlap or the header marks every document as `changed`, not as
  a rebuild: same result, without dropping the table.
- The first run after this change rebuilds the index once (old manifest format).
- The editorial check compares against the local manifest, so it only works where the
  manifest exists; a CI check against the Git base is still future work.
- Still one live version per document; history stays in Git.

## Alternatives considered

- **Keep one raw-file hash** — simplest, but every metadata edit re-embeds.
- **Fingerprint the chunking parameters too** — redundant with `embedding_hash` and
  would rebuild the table where a per-document replace is enough.
- **Metadata as dedicated table columns** — makes in-place updates trivial but changes
  the table schema and the filter code; the JSON column update is enough here.
- **Fail ingestion on a missing bump by default** — too strict while the manifest is
  local state; opt-in `--strict-versions` instead.
