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
    if mode == "Legal_mode":
        prompt_mode = "Act as a Senior Legal Analyst. Extract key legal clauses from the provided contract. For each clause, provide a summary of the terms and categorize it as 'Standard' or 'High Risk' based on potential liability. Specifically look for deviations in Indemnification or Termination periods. Ensure every extraction includes a source reference (e.g., Section 4.2). If a common clause is missing, explicitly note its absence."

    elif mode == "healthcare_mode":
        prompt_mode = """Act as a Clinical Data Specialist. Extract patient history with a strict distinction between:

Chief Complaint: (The reason the patient sought care).

Presenting Symptoms: (What they felt).

Etiology/Clinical Cause: (The underlying reason identified by the physician, e.g., dietary indiscretion, medication non-adherence).

Treatment Plan: (Specific dosage changes and follow-ups). Ensure you do not confuse physical activities (e.g., mowing the lawn) with clinical causes (e.g., sodium intake/CHF). Use the 'Source' tags provided in the text for every data point."""
    
    elif mode == "academic_mode":
        prompt_mode = "Act as an Academic Researcher. Summarize the research paper by creating a 'Study Profile' that includes: Objective, Methodology, Sample Size, Key Findings, and Statistical Significance ($p$-values). Do not just summarize the abstract; look into the 'Discussion' and 'Results' sections for nuance. Generate citations in APA 7th edition and include a list of 'Limitations' as identified by the authors."

    elif mode == "finance_mode":
        prompt_mode = "Act as a Financial Policy Auditor. Answer queries regarding bank policies and credit terms by prioritizing 'Primary Policy' over 'General Terms.' Extract specific numerical values (interest rates, penalty percentages, grace periods) and present them in a Markdown table. If a query asks for a calculation, show the step-by-step logic based on the document's rules. If the document is silent on a specific fee, state: 'Information not provided in source."

    elif mode == "business_mode":
        prompt_mode = "Act as an Executive Secretary. Analyze the provided meeting transcript to produce a high-level executive summary. Your primary output must be a categorized list of 'Action Items,' including who is responsible and the deadline if mentioned. Use bullet points for readability. Omit small talk and focus entirely on decisions made and next steps for the team."
    else:
        pass
    
    
    
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