from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Document AI HUB"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 
    class Config:
        env_file = ".env"
settings = Settings()