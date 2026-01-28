from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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

@signup_router.post("/signup")
def signup(
    username: str,
    password: str,
    role: str,
    db: Session = Depends(get_db)
):
    try:
        user = create_user(db, username, password, role)
        return {
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "username": user.user_name,
                "role": user.role
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))