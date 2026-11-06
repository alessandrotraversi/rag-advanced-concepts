import argparse
import json
import sys
from pathlib import Path

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGEngine, PGVectorStore
from psycopg.types.json import Json

from app.config import settings
from app.db import enable_vector_extension, get_connection
from app.ingest import OUTPUT_PATH as CHUNKS_PATH
from app.versioning import (
    HASH_FIELDS,
    MANIFEST_PATH,
    DocumentVersion,
    VersionRegistry,
    index_fingerprint,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TABLE_NAME = "fcai_knowledge_base"
ID_COLUMN = {"name": "chunk_id", "data_type": "TEXT", "nullable": False}
METADATA_COLUMN = "langchain_metadata"  # PGVectorStore's default JSON column


class IndexingError(Exception):
    pass


def load_chunks() -> list[Document]:
    if not CHUNKS_PATH.exists():
        raise IndexingError(f"chunks file not found: {CHUNKS_PATH}")

    documents: list[Document] = []
    with CHUNKS_PATH.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise IndexingError(f"line {number}: invalid JSON ({exc})")

            content = record.get("content")
            metadata = record.get("metadata") or {}
            if not content:
                raise IndexingError(f"line {number}: missing content")
            for field in ("chunk_id", "source_file", *HASH_FIELDS):
                if not metadata.get(field):
                    raise IndexingError(f"line {number}: missing metadata.{field}")

            documents.append(Document(page_content=content, metadata=metadata))

    if not documents:
        raise IndexingError(f"no chunks found in {CHUNKS_PATH}")

    return documents


def group_by_source(documents: list[Document]) -> dict[str, list[Document]]:
    grouped: dict[str, list[Document]] = {}
    for document in documents:
        grouped.setdefault(document.metadata["source_file"], []).append(document)
    return grouped


def table_exists() -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT to_regclass(%s)", (f"public.{TABLE_NAME}",)
        ).fetchone()
    return row[0] is not None


def connect_store(embeddings: OpenAIEmbeddings, create_table: bool) -> PGVectorStore:
    engine = PGEngine.from_connection_string(url=settings.database_url)
    if create_table:
        # The table column size must match the embedding model, so ask the
        # model for one embedding to learn its vector dimension.
        vector_size = len(embeddings.embed_query("dimension probe"))
        engine.init_vectorstore_table(
            table_name=TABLE_NAME,
            vector_size=vector_size,
            id_column=ID_COLUMN,
            overwrite_existing=True,
        )
    return PGVectorStore.create_sync(
        engine=engine,
        embedding_service=embeddings,
        table_name=TABLE_NAME,
        id_column=ID_COLUMN["name"],
    )


def update_metadata(documents: list[Document]) -> None:
    # Same embedded text means same chunk ids and same vectors: only the JSON
    # metadata column changes (e.g. status draft -> published), no embedding calls.
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(
                f'UPDATE "{TABLE_NAME}" SET "{METADATA_COLUMN}" = %s '
                f'WHERE "{ID_COLUMN["name"]}" = %s',
                [
                    (Json(document.metadata), document.metadata["chunk_id"])
                    for document in documents
                ],
            )
        conn.commit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Index chunks into pgvector, reindexing only what changed."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="delete every indexed chunk and reindex all current chunks",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print(f"Loading chunks from {CHUNKS_PATH.relative_to(PROJECT_ROOT)}...")
    try:
        documents = load_chunks()
    except IndexingError as exc:
        print(f"Indexing failed: {exc}", file=sys.stderr)
        raise SystemExit(1)

    grouped = group_by_source(documents)
    print(f"Loaded chunks: {len(documents)}")
    print(f"Sources in chunks: {len(grouped)}")

    print("Connecting to Postgres...")
    enable_vector_extension()

    fingerprint = index_fingerprint(settings.openai_embedding_model, TABLE_NAME)
    registry = VersionRegistry.load()
    current = {
        source: DocumentVersion.from_metadata(docs[0].metadata)
        for source, docs in grouped.items()
    }

    # Without a compatible manifest (none, older format, other embedding model) or
    # without the table, the stored vectors cannot be trusted: rebuild from scratch.
    reason = registry.rebuild_reason(fingerprint)
    if reason is None and not table_exists():
        reason = "table missing"
    rebuild = reason is not None
    if rebuild:
        print(f"Rebuilding the index: {reason}")
        registry = VersionRegistry()

    changes = registry.diff(current)
    print(f"New sources: {len(changes.new)}")
    print(f"Changed sources: {len(changes.changed)}")
    print(f"Metadata-only sources: {len(changes.metadata_only)}")
    print(f"Removed sources: {len(changes.removed)}")
    print(f"Unchanged sources: {len(changes.unchanged)}")

    if args.force:
        delete_ids = registry.chunk_ids(registry.sources)
        sources_to_index = list(grouped)
        sources_to_update = []
    else:
        delete_ids = registry.chunk_ids(changes.removed + changes.changed)
        sources_to_index = changes.new + changes.changed
        sources_to_update = changes.metadata_only

    documents_to_index = [
        document for source in sources_to_index for document in grouped[source]
    ]
    documents_to_update = [
        document for source in sources_to_update for document in grouped[source]
    ]

    embeddings = OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        api_key=settings.openai_api_key,
    )
    store = connect_store(embeddings, create_table=rebuild)

    if delete_ids:
        store.delete(ids=delete_ids)
    if documents_to_index:
        store.add_documents(
            documents_to_index,
            ids=[document.metadata["chunk_id"] for document in documents_to_index],
        )
    if documents_to_update:
        update_metadata(documents_to_update)

    VersionRegistry.write(
        fingerprint,
        {
            source: current[source].manifest_entry(
                docs[0].metadata, [document.metadata["chunk_id"] for document in docs]
            )
            for source, docs in grouped.items()
        },
    )

    print(f"Deleted chunks: {len(delete_ids)}")
    print(f"Indexed chunks: {len(documents_to_index)}")
    print(f"Metadata-updated chunks: {len(documents_to_update)}")
    print(f"Manifest saved to {MANIFEST_PATH.relative_to(PROJECT_ROOT)}")
    print("Indexing completed.")


if __name__ == "__main__":
    main()
