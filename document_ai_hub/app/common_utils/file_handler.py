from pathlib import Path
import uuid

DATA_DIR = Path("data/documents")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def save_file(file):
    file_id = str(uuid.uuid4())
    file_path = DATA_DIR / f"{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_id