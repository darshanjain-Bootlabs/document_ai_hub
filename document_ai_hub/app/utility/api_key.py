from fastapi import Header, HTTPException, status
from app.core.config import VALID_API_KEYS

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return VALID_API_KEYS[x_api_key]