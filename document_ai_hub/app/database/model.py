from sqlalchemy import Column, Integer, String
from app.database.session import Base

class UserChunk(Base):
    __tablename__ = "user_chunks"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True, nullable=False)
    user_password = Column(String, nullable=False)
    role = Column(String, index=True, nullable=False)