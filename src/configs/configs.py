import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = os.getenv("DATABASE_URL")

ALGORITHM = os.getenv("ALGORITHM")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")
