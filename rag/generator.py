import time
from google import genai
import os
from dotenv import load_dotenv
from utils.log import logger

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(query: str, context: str):
    start = time.time()

    prompt = f"""
    Context:
    {context}

    Savol:
    {query}
    """
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    total = time.time() - start
    logger.info(f"LLM generation time: {total:.4f}s")

    return response.text