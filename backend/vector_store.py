import os
import logging
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

# ✅ FIXED IMPORT
from document_loader import load_templates

logger = logging.getLogger(__name__)

DB_PATH = "./chroma_db"
COLLECTION_NAME = "brd_templates"

_client = None
_collection = None


def _get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=DB_PATH)
    return _client


def create_vector_store():
    global _collection

    client = _get_client()
    ef = embedding_functions.DefaultEmbeddingFunction()

    _collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    existing = _collection.count()

    if existing > 0:
        logger.info(f"Vector store already contains {existing} documents")
        return

    logger.info("Loading templates into vector store...")

    try:
        documents = load_templates()

        if not documents:
            logger.warning("No templates found")
            return

        ids = [f"doc_{i}" for i in range(len(documents))]

        _collection.add(
            documents=documents,
            ids=ids
        )

        logger.info(f"Inserted {len(documents)} documents")

    except Exception as exc:
        logger.error(f"Failed to load templates: {exc}")
        raise


def get_collection():
    global _collection
    if _collection is None:
        raise RuntimeError("Vector store not initialised")
    return _collection