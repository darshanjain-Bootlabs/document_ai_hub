from slowapi import Limiter
from slowapi.errors import RateLimitExceeded

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.utility.auth_router import auth_router
from dotenv import load_dotenv

from app.core.rate_limiter import get_remote_email
from pydantic import BaseModel

load_dotenv()

class RoleUpdateRequest(BaseModel):
    role: str

app = FastAPI(title="Document AI Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(router)

Limiter = Limiter(key_func=get_remote_email)
app.state.limiter = Limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )

