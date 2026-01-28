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