from app.services.vector_service import similarity_search
from groq import Groq
from typing import List

client = Groq()
MODEL_NAME = "llama-3.1-8b-instant"


def build_context(docs) -> str:
    context_blocks = []

    for i, doc in enumerate(docs, start=1):
        block = f"[Document {i}]\n{doc.page_content}"
        context_blocks.append(block)

    return "\n\n".join(context_blocks)


def build_prompt(query: str, context: str, response_format: str) -> str:
    if response_format == "json":
        format_instruction = """
Return the answer strictly as valid JSON with the following keys:
- answer (string)
- key_points (array of strings)
- sources (array of short strings)
"""
    elif response_format == "markdown":
        format_instruction = """
Return the answer in Markdown format with:
- A clear heading
- Bullet points
- A short summary section
"""
    elif response_format == "table":
        format_instruction = """
Return the answer as a Markdown table with columns:
- Topic
- Explanation
"""
    else:
        format_instruction = "Return a plain text answer."

    return f"""
You are a RAG-based assistant.

Rules:
- Use ONLY the context provided
- Do NOT use outside knowledge
- If the answer is not present, say: "I don't know"

Context:
{context}

Question:
{query}

{format_instruction}
"""


def generate_answer(query: str, response_format: str, top_k: int = 3):
    docs = similarity_search(query, k=top_k)

    context = build_context(docs)

    prompt = build_prompt(query, context, response_format)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers strictly from context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=600,
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "format": response_format
            }
            for doc in docs
        ]
    }