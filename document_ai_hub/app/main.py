from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Document AI Hub")

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "Document AI Hub is running"}