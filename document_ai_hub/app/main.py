from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request

from app.api.routes import router
from app.utility.auth_router import auth_router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Document AI Hub")

app.include_router(auth_router)
app.include_router(router)

Limiter = Limiter(key_func=get_remote_address)
app.state.limiter = Limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )
