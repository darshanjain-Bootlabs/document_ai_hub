from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database.model import UserChunk
from app.core.config import MODE_DOMAIN_MAP, ROLE_DOMAIN_ACCESS
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, username: str, password: str, role: str):
    existing = db.query(UserChunk).filter(UserChunk.user_name == username).first()
    if existing:
        raise ValueError("User already exists")
    hashed_password = pwd_context.hash(password)

    user = UserChunk(
        user_name=username,
        user_password=hashed_password,
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UserChunk).filter(UserChunk.user_name == username).first()
    if not user:
        return None
    if not verify_password(password, user.user_password):
        return None
    return user

def authorize_access(user_role: str, doc_domain: str, mode: str):
    if doc_domain not in ROLE_DOMAIN_ACCESS.get(user_role, []):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this document"
        )

    expected_domain = MODE_DOMAIN_MAP.get(mode, [])
    if doc_domain not in expected_domain:
        raise HTTPException(
            status_code=400,
            detail="Invalid mode for this document type"
        )
    
    return True
    
    