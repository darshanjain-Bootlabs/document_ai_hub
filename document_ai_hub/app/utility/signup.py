from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.session import SessionLocal
from app.services.user_service import create_user
from app.utility.auth import require_role

signup_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class SignupResponse(BaseModel):
    id: int
    username: str
    role: str
    email: str

@signup_router.post("/signup", response_model=SignupResponse)
def signup(
    signup_data: SignupRequest,
    db: Session = Depends(get_db),
):
    try:
        user = create_user(db, signup_data.username, signup_data.password, signup_data.email, role="user")
        return SignupResponse(
            id=user.id,
            username=user.user_name,
            role=user.role,
            email=user.email
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))