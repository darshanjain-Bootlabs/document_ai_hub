from fastapi import Request
from slowapi.util import get_remote_address

def get_remote_email(request: Request):
    user = getattr(request.state, "user", None)
    if user and "email" in user:
        return user["email"]
    return get_remote_address(request)
