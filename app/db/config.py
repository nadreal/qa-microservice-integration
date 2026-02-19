from dotenv import load_dotenv
import os

load_dotenv()  

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/qa_microservice")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    DEBUG: bool = os.getenv("DEBUG", "1") == "1"

settings = Settings()