from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from .dependencies import get_query_token, get_token_header
from sql import models, database

# from .routers import users, places, region, token
from .controllers import router
from sql import models

# models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.include_router(router)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
