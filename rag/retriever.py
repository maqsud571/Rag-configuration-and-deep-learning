from rag.vector_store import search

def get_context(query: str):
    docs = search(query)
    return "\n".join(docs) 