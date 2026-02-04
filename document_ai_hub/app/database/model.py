from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from app.database.session import Base

class UserChunk(Base):
    __tablename__ = "user_chunks"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True, nullable=False)
    user_password = Column(String, nullable=False)
    role = Column(String, index=True, nullable=False, default="user")
    email = Column(String, unique=True, index=True, nullable=False)

class DocumentMetaData(Base):
    __tablename__ = "document_metadata"

    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, index=True, nullable=False)
    file_domain = Column(String, index=True, nullable=True)
    uploaded_by = Column(String, index=True, nullable=False)

class RoleUpdateRequest(BaseModel):
    role: str

class RoleUpdateResponse(BaseModel):
    id: int
    user_name: str
    role: str
