from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()
class Settings(BaseSettings):
    app_name: str = "Document AI HUB"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 
    DATABASE_URL: str
    GROQ_API_KEY: str
    JWT_SECRET_KEY: str
    class Config:
        env_file = ".env"
settings = Settings()


ROLE_DOMAIN_ACCESS = {
    "doctor": ["healthcare"],
    "nurse": ["healthcare"],
    "lawyer": ["legal"],
    "bank_officer": ["finance"],
    "student": ["academic"],
    "business_user": ["business"],
    "admin": ["healthcare", "legal", "finance", "academic", "business"]
}


MODE_DOMAIN_MAP = {
    "healthcare_mode": ["healthcare"],
    "legal_mode": ["legal"],
    "finance_mode": ["finance"],
    "academic_mode": ["academic"],
    "business_mode": ["business"],
    "general": ["healthcare", "legal", "finance", "academic", "business"]

}


VALID_API_KEYS = {
    "swagger-key-123": "swagger",
    "frontend-key-456": "frontend"
}