from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data["exp"] = expire
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def require_role(required_role: list[str]):
    def role_checker(user = Depends(get_current_user)):
        if user["role"] not in required_role:
            raise HTTPException(
                status_code=401,
                detail="NOT AUTHORIZED TO ACCESS THIS RESOURCE"
            )
        return user
    return role_checker

    
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if not username or not role:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {
            "username": username,
            "role": role
        }
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )