from fastapi import FastAPI
from document_ai_hub.app.api.routers import router

app = FastAPI(title="Document AI Hub")
app.include_router(router)

@app.get("/")
async def health_server():
    return {"Health": "ALL OK!!, Server is running smoothly."}