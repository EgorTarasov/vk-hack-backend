from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DATABASE_URL = (
    f"postgresql://${getenv('DB_USER')}:${getenv('DB_PASS')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/${getenv('DB_NAME')}" if getenv("DB_HOST") else "db:sqlite:///db.sqlite"
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
