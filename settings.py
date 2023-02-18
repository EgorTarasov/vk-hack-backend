from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DATABASE_URL = (
    f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}" if getenv("POSTGRES_HOST") else "db:sqlite:///db.sqlite"
)

ACCESS_TOKEN_EXPIRE_MINUTES = (
    getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    if getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    else 30
)

SECRET_KEY = getenv("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("Invalid SECRET_KEY in environment")
ALGORITHM = getenv("ALGORITHM") if getenv("ALGORITHM") else "HS256"
