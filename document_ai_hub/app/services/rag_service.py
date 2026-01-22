import subprocess
from app.services.vector_service import similarity_search

def build_context(docs) -> str:
    context_blocks = []

    for i, doc in enumerate(docs,start=1):
        block = f"[Document {i}]\n{doc.page_content}"
        context_blocks.append(block)
    return "\n\n".join(context_blocks)

def call_ollama(prompt: str) -> str:
    process = subprocess.run(
        ["ollama","run","tinyllama"], 
        input = prompt,
            text = True,
            capture_output = True
        )
    return process.stdout.strip()

def generate_answer(query: str, top_k: int = 3) -> str:
        docs = similarity_search(query, k=top_k)
        context = build_context(docs)
        prompt = f"""
Answer the question using only the context below. 
First, identify relevant information. Then, summarize it. Finally, give a clear answer.
 If uncertain, state that. Question: {query} Context: {context}
"""
        answer = call_ollama(prompt)
        return {
        "answer": answer,
        "sources": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
        ]    
}