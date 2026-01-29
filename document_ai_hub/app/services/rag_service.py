from app.services.vector_service import similarity_search
from groq import Groq

from app.services.user_service import authorize_access

client = Groq()
MODEL_NAME = "llama-3.1-8b-instant"


def build_context(docs) -> str:
    context_blocks = []

    for i, doc in enumerate(docs, start=1):
        block = f"[Document {i}]\n{doc.page_content}"
        context_blocks.append(block)

    return "\n\n".join(context_blocks)


def build_prompt(query: str, context: str, response_format: str, mode : str) -> str:
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
    elif mode == "Legal_mode":
        prompt_mode = "Act as a Senior Legal Analyst. Your task is to review the provided legal documents to extract key clauses (e.g., Indemnification, Termination, Force Majeure) and summarize contract terms in plain language. Highlight any non-standard language or potential risks for the client. Maintain a formal, objective tone and ensure all citations refer to specific sections of the document. Do not provide binding legal advice; provide analysis only."

    elif mode == "heathcare_mode":
        prompt_mode = "Act as a Medical Informatics Specialist. Process the provided patient records to extract a chronological history, including previous diagnoses, medications, and allergies. Based on clinical guidelines, suggest potential treatment pathways for the physician to review. Disclaimer: Note that these are suggestions for clinical decision support only and must be verified by a licensed professional. Prioritize patient safety and data privacy rules (HIPAA compliance) in your formatting."
    
    elif mode == "academic_mode":
        prompt_mode = "Act as an Academic Research Assistant. Your role is to summarize dense research papers by identifying the hypothesis, methodology, key findings, and limitations. Use a structured format with clear headings. Additionally, generate accurate citations in [APA/MLA/Chicago] format for any text referenced. Focus on maintaining the intellectual integrity of the original work while making it accessible."

    elif mode == "finance_mode":
        prompt_mode = "Act as a Banking and Finance Specialist. You will answer queries regarding bank policies, loan structures, and credit terms based on the provided documentation. Break down complex financial jargon into digestible sections. When discussing loans, clearly define interest rates, tenure, and eligibility criteria. If information is missing from the source text, state that clearly rather than estimating. Use tables for comparing different financial products."

    elif mode == "business_mode":
        prompt_mode = "Act as an Executive Secretary. Analyze the provided meeting transcript to produce a high-level executive summary. Your primary output must be a categorized list of 'Action Items,' including who is responsible and the deadline if mentioned. Use bullet points for readability. Omit small talk and focus entirely on decisions made and next steps for the team."
    
    
    
    
    return f"""
{prompt_mode}

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


def generate_answer(query: str, response_format: str, doc_domain: str, user_role: str, mode: str) -> dict:


    if not authorize_access(user_role, doc_domain, mode):
        raise Exception("Unauthorized access")
    else:
        docs = similarity_search(query, k=3)
        context = build_context(docs)

        prompt = build_prompt(query, context, response_format,mode)

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
            temperature=0.1,
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