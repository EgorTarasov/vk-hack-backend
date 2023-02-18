import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DATABASE_URL = (
    os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") else "db:sqlite:///db.sqlite"
)
ACCESS_TOKEN_EXPIRE_MINUTES = (
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    if os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    else 30
)

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("invalid SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM") if os.getenv("ALGORITHM") else "HS256"
