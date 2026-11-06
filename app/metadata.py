"""Declarative metadata schema for ingestion.

Every metadata field a chunk carries is declared once, in ``METADATA_SCHEMA``:
where its value comes from, whether it is required, which values are allowed and
whether it goes into the context header that reaches the embedding.

To add a field:
- front matter field  -> ``MetadataField("owner", required=True)``
- derived field       -> ``MetadataField("word_count", scope=Scope.CONTENT,
                              compute=lambda ctx: len(ctx.content.split()))``
- embed it in text    -> add ``header_label="Owner"``
- constrain format    -> add ``pattern=r"[a-z-]+"`` (regex for the whole value)

Fields are resolved in declaration order within each scope, so a computed field can
read any field resolved before it from ``ctx.metadata``.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from app.versioning import EDITORIAL_VERSION_PATTERN, DocumentVersion


class MetadataError(Exception):
    pass


class Scope(str, Enum):
    FRONT_MATTER = "front_matter"  # read from the document's YAML front matter
    DOCUMENT = "document"  # computed once per document, from the raw file
    CHUNK = "chunk"  # computed per chunk, before the context header is built
    CONTENT = "content"  # computed per chunk, from the final text (header included)
    VERSION = "version"  # computed per chunk, once every chunk of the document is final


@dataclass(frozen=True)
class FieldContext:
    path: Path
    metadata: dict[str, Any]  # fields resolved so far
    raw: str = ""  # complete file text, front matter included (DOCUMENT scope only)
    index: int | None = None  # chunk position inside the document
    headers: dict[str, str] = field(default_factory=dict)  # h1/h2/h3 of the chunk
    content: str | None = None  # final chunk text (CONTENT scope only)
    version: DocumentVersion | None = None  # document version (VERSION scope only)


Compute = Callable[[FieldContext], Any]


@dataclass(frozen=True)
class MetadataField:
    name: str
    scope: Scope = Scope.FRONT_MATTER
    required: bool = False
    choices: tuple[str, ...] | None = None
    pattern: str | None = None  # regex the whole value must match
    header_label: str | None = None
    compute: Compute | None = None

    def __post_init__(self) -> None:
        if self.scope is Scope.FRONT_MATTER and self.compute is not None:
            raise ValueError(f"{self.name}: front matter fields cannot be computed")
        if self.scope is not Scope.FRONT_MATTER and self.compute is None:
            raise ValueError(f"{self.name}: {self.scope.value} fields need a compute")


# --- Computed fields -------------------------------------------------------------


def _version_field(name: str) -> Compute:
    # Version hashes are computed once per document in app/versioning.py (ADR 0012)
    # and stamped on every chunk, so the indexer can diff without re-reading files.
    return lambda ctx: getattr(ctx.version, name)


def _chunk_id(ctx: FieldContext) -> str:
    return ctx.version.chunk_id(ctx.index)


def _section(ctx: FieldContext) -> str | None:
    for key in ("h3", "h2", "h1"):
        if ctx.headers.get(key):
            return ctx.headers[key]
    return None


# --- Schema ----------------------------------------------------------------------

STATUSES = ("draft", "published", "archived")  # ADR 0011

METADATA_SCHEMA: tuple[MetadataField, ...] = (
    MetadataField("title", required=True, header_label="Document title"),
    MetadataField("tenant", required=True),
    MetadataField("product", required=True, header_label="Product"),
    MetadataField("plan", required=True, header_label="Plan"),
    MetadataField("doc_type", required=True, header_label="Document type"),
    MetadataField(
        "version",
        required=True,
        pattern=EDITORIAL_VERSION_PATTERN,
        header_label="Version",
    ),
    MetadataField("status", required=True, choices=STATUSES),
    MetadataField("visibility", required=True),
    MetadataField("source_file", Scope.CHUNK, compute=lambda ctx: ctx.path.name),
    MetadataField("chunk_index", Scope.CHUNK, compute=lambda ctx: ctx.index),
    MetadataField("section", Scope.CHUNK, header_label="Section", compute=_section),
    MetadataField(
        "content_length", Scope.CONTENT, compute=lambda ctx: len(ctx.content)
    ),
    MetadataField("body_hash", Scope.VERSION, compute=_version_field("body_hash")),
    MetadataField(
        "embedding_hash", Scope.VERSION, compute=_version_field("embedding_hash")
    ),
    MetadataField(
        "metadata_hash", Scope.VERSION, compute=_version_field("metadata_hash")
    ),
    MetadataField("chunk_id", Scope.VERSION, compute=_chunk_id),
)

# Order of the lines in the context header (by field name). Kept separate from the
# schema order because the header reads best from general to specific.
CONTEXT_HEADER_ORDER: tuple[str, ...] = (
    "title",
    "doc_type",
    "product",
    "plan",
    "version",
    "section",
)


class MetadataSchema:
    def __init__(
        self,
        fields: Iterable[MetadataField],
        header_order: Iterable[str] | None = None,
    ) -> None:
        self.fields = tuple(fields)
        names = [f.name for f in self.fields]
        duplicated = {name for name in names if names.count(name) > 1}
        if duplicated:
            raise ValueError(f"duplicated metadata fields: {sorted(duplicated)}")

        by_name = {f.name: f for f in self.fields}
        labelled = [f.name for f in self.fields if f.header_label]
        order = list(header_order) if header_order is not None else labelled
        if sorted(order) != sorted(labelled):
            raise ValueError(
                "context header order must list exactly the fields with a "
                f"header_label: {labelled}"
            )
        self.header_fields = tuple(by_name[name] for name in order)

    def in_scope(self, scope: Scope) -> tuple[MetadataField, ...]:
        return tuple(f for f in self.fields if f.scope is scope)

    @property
    def computed(self) -> tuple[str, ...]:
        return tuple(f.name for f in self.fields if f.scope is not Scope.FRONT_MATTER)

    def front_matter(self, metadata: dict[str, Any]) -> dict[str, Any]:
        """The author-written part of ``metadata`` (everything not computed)."""
        return {k: v for k, v in metadata.items() if k not in self.computed}

    @property
    def required(self) -> tuple[str, ...]:
        return tuple(f.name for f in self.in_scope(Scope.FRONT_MATTER) if f.required)

    def validate_front_matter(self, source: str, metadata: dict[str, Any]) -> None:
        errors = []
        missing = [name for name in self.required if name not in metadata]
        if missing:
            errors.append(f"missing required metadata: {', '.join(missing)}")
        for f in self.in_scope(Scope.FRONT_MATTER):
            value = metadata.get(f.name)
            if f.choices and value is not None and value not in f.choices:
                errors.append(
                    f"invalid {f.name}: {value!r} (allowed: {', '.join(f.choices)})"
                )
            if f.pattern and value is not None and not re.fullmatch(f.pattern, str(value)):
                errors.append(f"invalid {f.name}: {value!r} (must match {f.pattern})")
        if errors:
            raise MetadataError(f"{source}: {'; '.join(errors)}")

    def resolve(self, scope: Scope, ctx: FieldContext) -> dict[str, Any]:
        """Compute the fields of ``scope`` into ``ctx.metadata`` (in place)."""
        for f in self.in_scope(scope):
            ctx.metadata[f.name] = f.compute(ctx)
        return ctx.metadata

    def context_header(self, metadata: dict[str, Any]) -> str:
        return "\n".join(
            f"{f.header_label}: {metadata[f.name]}"
            for f in self.header_fields
            if metadata.get(f.name)
        )


SCHEMA = MetadataSchema(METADATA_SCHEMA, CONTEXT_HEADER_ORDER)
