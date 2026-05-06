from retriever import retrieve
from config import GROQ_API_KEY, TOP_K, PRIMARY_MODEL, MAX_EXPLANATION_TOKENS, EXPLANATION_TEMPERATURE
import json
from groq import Groq
from prompts import build_prompt

chunks_json = json.load(open("data/chunks.json", "r", encoding="utf-8"))


def ask_tutor(query):
    retrieved_chunks = retrieve(query, chunks_json, top_k=TOP_K)

    if not retrieved_chunks:
        return "Error -> Empty Chunks"

    final_prompt = build_prompt(query, retrieved_chunks)
    client = Groq(api_key=GROQ_API_KEY)
    messages = [
        {"role": "system", "content": "You are a helpful and precise assistant for answering questions about machine learning based on textbook excerpts."},
        {"role": "user", "content": final_prompt}
    ]
    response = client.chat.completions.create(messages=messages, model=PRIMARY_MODEL, max_tokens=MAX_EXPLANATION_TOKENS, temperature=EXPLANATION_TEMPERATURE)
    response_content = response.choices[0].message.content
    return response_content, retrieved_chunks


    

