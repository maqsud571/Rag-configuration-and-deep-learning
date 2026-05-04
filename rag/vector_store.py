import time
import numpy as np
from sqlalchemy import text
from db.database import engine
from rag.embedder import get_embedding
from utils.log import logger


def add_document(content: str):
    start_total = time.time()

    # EMBEDDING
    start_embed = time.time()
    embedding = get_embedding(content)
    embed_time = time.time() - start_embed

    logger.info(f"Embedding time: {embed_time:.4f}s")

    # DB INSERT
    start_db = time.time()

    query = text("""
        INSERT INTO documents (content, embedding)
        VALUES (:content, :embedding)
    """)

    with engine.connect() as conn:
        conn.execute(query, {
            "content": content,
            "embedding": embedding
        })
        conn.commit()

    db_time = time.time() - start_db
    logger.info(f"DB insert time: {db_time:.4f}s")

    total_time = time.time() - start_total
    logger.info(f"TOTAL add_document: {total_time:.4f}s")


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search(query_text: str, top_k=3):
    start_total = time.time()

    # QUERY EMBEDDING
    start_embed = time.time()
    query_embedding = get_embedding(query_text)
    embed_time = time.time() - start_embed
    logger.info(f"Query embedding time: {embed_time:.4f}s")

    # DB FETCH
    start_db = time.time()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT content, embedding FROM documents"))
        rows = result.fetchall()
    db_time = time.time() - start_db
    logger.info(f"DB fetch time: {db_time:.4f}s")

    # SIMILARITY
    start_sim = time.time()

    scored = []
    for content, emb in rows:
        score = cosine_similarity(query_embedding, emb)
        scored.append((content, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    sim_time = time.time() - start_sim
    logger.info(f"Similarity calc time: {sim_time:.4f}s")

    total_time = time.time() - start_total
    logger.info(f"TOTAL search: {total_time:.4f}s")

    return [x[0] for x in scored[:top_k]]


# Tme qoshilmagan oddiy versiya:

# import numpy as np
# from sqlalchemy import text
# from db.database import engine
# from rag.embedder import get_embedding

# def add_document(content: str):
#     embedding = get_embedding(content)

#     query = text("""
#         INSERT INTO documents (content, embedding)
#         VALUES (:content, :embedding)
#     """)

#     with engine.connect() as conn:
#         conn.execute(query, {
#             "content": content,
#             "embedding": embedding
#         })
#         conn.commit()


# def cosine_similarity(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# def search(query_text: str, top_k=3):
#     query_embedding = get_embedding(query_text)

#     with engine.connect() as conn:
#         result = conn.execute(text("SELECT content, embedding FROM documents"))
#         rows = result.fetchall()

#     scored = []
#     for content, emb in rows:
#         score = cosine_similarity(query_embedding, emb)
#         scored.append((content, score))

#     scored.sort(key=lambda x: x[1], reverse=True)
#     return [x[0] for x in scored[:top_k]]
