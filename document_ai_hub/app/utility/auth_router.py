from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.services.user_service import authenticate_user
from app.utility.auth import create_access_token
from app.utility.signup import get_db
from sqlalchemy.orm import Session  

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.user_name, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}