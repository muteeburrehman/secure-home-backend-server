import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads/")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Database Configuration
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "fastapi_db")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

settings = Settings()
