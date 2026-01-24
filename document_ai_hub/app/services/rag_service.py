from app.services.vector_service import similarity_search
from groq import Groq
from typing import List

client = Groq()
MODEL_NAME = "llama3-8b-8192"

def build_context(docs) -> str:
    context_blocks = []

    for i, doc in enumerate(docs,start=1):
        block = f"[Document {i}]\n{doc.page_content}"
        context_blocks.append(block)
    return "\n\n".join(context_blocks)


def build_prompt(query: str, context: str, response_format: str) -> str:
    if response_format == "json":
        format_instruction = """
Return the answer strictly as valid JSON with the following keys:
- answer
- key_points (array)
- sources (array)
"""
    elif response_format == "markdown":
        format_instruction = """
Return the answer in Markdown format with:
- A heading
- Bullet points
- A short summary
"""
    elif response_format == "table":
        format_instruction = """
Return the answer as a table with columns:
- Topic
- Explanation
"""
    else:
        format_instruction = "Return a plain text answer."

    return f"""
Answer the question using only the context below. 
First, identify relevant information. Then, summarize it. Finally, give a clear answer.
 If uncertain, state that "i dont know ".

Context:
{context}

Question:
{query}

{format_instruction}
"""

def generate_answer(query: str, response_format: str, top_k: int = 3) -> str:
        docs = similarity_search(query, k=top_k)
        context = build_context(docs)
        prompt = build_prompt(query, context, response_format)
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=600,
        ).choices[0].message.content

        return {
        "answer": response,
        "sources": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "format": response_format
            }
            for doc in docs
        ]    
}
