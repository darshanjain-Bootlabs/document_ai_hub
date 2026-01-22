import io
from PyPDF2 import PdfReader

def text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = []

    for page in reader.pages:
        text.append(page.extract_text() + "\n")
    return text