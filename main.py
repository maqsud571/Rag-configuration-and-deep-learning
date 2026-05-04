import time
from fastapi import FastAPI
from rag.retriever import get_context
from rag.generator import generate_answer
from rag.vector_store import add_document
from utils.log import logger

app = FastAPI()


@app.post("/add")
def add_doc(text: str):
    start = time.time()

    add_document(text)

    total = time.time() - start
    logger.info(f"/add TOTAL request: {total:.4f}s")

    return {"status": "added"}


@app.get("/ask")
def ask(query: str):
    start = time.time()

    context = get_context(query)
    answer = generate_answer(query, context)

    total = time.time() - start
    logger.info(f"/ask TOTAL request: {total:.4f}s")

    return {
        "query": query,
        "context": context,
        "answer": answer
    }