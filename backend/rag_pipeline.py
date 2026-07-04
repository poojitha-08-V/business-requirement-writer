import logging
from vector_store import get_collection

logger = logging.getLogger(__name__)


def search_documents(query: str, top_k: int = 3) -> list[str]:

    if not query or not query.strip():
        raise ValueError("Search query must not be empty.")

    try:
        collection = get_collection()

        results = collection.query(
            query_texts=[query.strip()],
            n_results=min(top_k, collection.count() or 1),
        )

        documents = results.get("documents", [[]])[0]

        logger.info(
            f"RAG search returned {len(documents)} results for query: '{query}'"
        )

        return documents

    except Exception as exc:
        logger.exception(f"RAG search error for query '{query}'")
        raise RuntimeError(f"Document search failed: {exc}") from exc