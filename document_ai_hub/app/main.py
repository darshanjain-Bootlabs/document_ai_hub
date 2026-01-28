from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from app.api.routes import router
from app.utility.auth_router import auth_router

app = FastAPI(title="Document AI Hub")

app.include_router(auth_router)
app.include_router(router)
