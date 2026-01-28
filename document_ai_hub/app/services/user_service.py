from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database.model import UserChunk

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password = pwd_context.hash("141407")

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