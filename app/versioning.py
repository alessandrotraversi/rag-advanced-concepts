"""Versioning of documents and of the index (ADR 0012).

Every document carries one editorial version and three hashes, each with one job:

| Signal           | Covers                                | When it changes                          |
| ---------------- | ------------------------------------- | ---------------------------------------- |
| `version`        | front matter label, owned by author   | the author bumps it (e.g. 2026-01)       |
| `body_hash`      | the Markdown body as written          | the author must also bump `version`      |
| `embedding_hash` | final chunk texts (what is embedded)  | new chunk ids, chunks are re-embedded    |
| `metadata_hash`  | the front matter                      | stored metadata is updated, no embedding |

The index as a whole has a fingerprint (embedding model, table, manifest format).
When it changes, every stored vector is stale and the table is rebuilt.

``VersionRegistry`` is the manifest (``data/index_manifest.json``): which version of
each document is live in the index, and under which fingerprint.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PROJECT_ROOT / "data" / "index_manifest.json"
MANIFEST_FORMAT = 2

# Editorial versions are year-month labels, e.g. "2026-01".
EDITORIAL_VERSION_PATTERN = r"\d{4}-(0[1-9]|1[0-2])"

HASH_FIELDS = ("body_hash", "embedding_hash", "metadata_hash")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_hash(value: Any) -> str:
    """SHA-256 of a JSON-serialisable value, independent of key order."""
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, default=str))


def index_fingerprint(embedding_model: str, table_name: str) -> str:
    # Chunking parameters and the context header are deliberately not listed: they
    # change the chunk texts, so they already show up per document in embedding_hash.
    return stable_hash(
        {
            "embedding_model": embedding_model,
            "table": table_name,
            "manifest_format": MANIFEST_FORMAT,
        }
    )


@dataclass(frozen=True)
class DocumentVersion:
    source_file: str
    version: str | None
    body_hash: str
    embedding_hash: str
    metadata_hash: str

    @classmethod
    def build(
        cls,
        source_file: str,
        front_matter: Mapping[str, Any],
        body: str,
        chunk_texts: Iterable[str],
    ) -> DocumentVersion:
        version = front_matter.get("version")
        return cls(
            source_file=source_file,
            version=str(version) if version is not None else None,
            body_hash=sha256(body),
            embedding_hash=stable_hash(list(chunk_texts)),
            metadata_hash=stable_hash(dict(front_matter)),
        )

    @classmethod
    def from_metadata(cls, metadata: Mapping[str, Any]) -> DocumentVersion:
        """Rebuild the version from the metadata stamped on any of its chunks."""
        return cls(
            source_file=metadata["source_file"],
            version=metadata.get("version"),
            **{name: metadata[name] for name in HASH_FIELDS},
        )

    def chunk_id(self, index: int) -> str:
        # Deterministic and content-addressed: same embedded texts + same position =
        # same id; any change to what is embedded gives the document new ids.
        return f"{Path(self.source_file).stem}-{self.embedding_hash[:12]}-{index:04d}"

    def manifest_entry(self, metadata: Mapping[str, Any], chunk_ids: list[str]) -> dict:
        entry = {key: value for key, value in asdict(self).items() if key != "source_file"}
        for key in ("title", "tenant", "product", "status"):
            entry[key] = metadata.get(key)
        entry["chunk_ids"] = chunk_ids
        return entry


@dataclass
class ChangeSet:
    new: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)  # embedded text changed
    metadata_only: list[str] = field(default_factory=list)  # same text, new front matter
    unchanged: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)


@dataclass
class VersionRegistry:
    format: int | None = None
    fingerprint: str | None = None
    sources: dict[str, dict] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path = MANIFEST_PATH) -> VersionRegistry:
        if not path.exists():
            return cls()
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        return cls(
            format=data.get("format"),
            fingerprint=data.get("index_fingerprint"),
            sources=data.get("sources", {}),
        )

    @staticmethod
    def write(
        fingerprint: str, sources: Mapping[str, dict], path: Path = MANIFEST_PATH
    ) -> None:
        manifest = {
            "format": MANIFEST_FORMAT,
            "index_fingerprint": fingerprint,
            "indexed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "sources": dict(sources),
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        # Write to a temporary file and rename, so a crash never leaves half a manifest.
        tmp = path.with_suffix(path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            json.dump(manifest, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        tmp.replace(path)

    def rebuild_reason(self, fingerprint: str) -> str | None:
        """Why the stored index cannot be diffed against, or None if it can."""
        if not self.sources:
            return "no manifest"
        if self.format != MANIFEST_FORMAT:
            return f"manifest format {self.format} (expected {MANIFEST_FORMAT})"
        if self.fingerprint != fingerprint:
            return "index fingerprint changed (embedding model or table)"
        return None

    def diff(self, current: Mapping[str, DocumentVersion]) -> ChangeSet:
        changes = ChangeSet()
        for source, version in current.items():
            previous = self.sources.get(source)
            if previous is None:
                changes.new.append(source)
            elif previous.get("embedding_hash") != version.embedding_hash:
                changes.changed.append(source)
            elif previous.get("metadata_hash") != version.metadata_hash:
                changes.metadata_only.append(source)
            else:
                changes.unchanged.append(source)
        changes.removed = [source for source in self.sources if source not in current]
        return changes

    def chunk_ids(self, sources: Iterable[str]) -> list[str]:
        return [
            chunk_id for source in sources for chunk_id in self.sources[source]["chunk_ids"]
        ]

    def stale_editorial_versions(self, current: Mapping[str, DocumentVersion]) -> list[str]:
        """Documents whose body changed since the last index but whose version did not."""
        stale = []
        for source, version in current.items():
            previous = self.sources.get(source) or {}
            body_hash = previous.get("body_hash")
            if body_hash and body_hash != version.body_hash and (
                previous.get("version") == version.version
            ):
                stale.append(source)
        return sorted(stale)
