import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

ALGORITHM = os.getenv("ALGORITHM")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")
