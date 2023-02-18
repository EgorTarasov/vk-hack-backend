from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import BaseModel
from .models import Event


class UserData(BaseModel):
    vkid: int
    first_name: str
    last_name: str


class UserCreate(UserData):
    pass


class UserUpdate(BaseModel):
    vkid: int
    wallet_public_key: str


class Token(BaseModel):
    access_token: str
    token_type: str


EventCreate = sqlalchemy_to_pydantic(Event, exclude=["id", "owner_id"])
EventUpdate = sqlalchemy_to_pydantic(Event, exclude=["id" "owner_id"])
EventData = sqlalchemy_to_pydantic(Event, exclude=["start_datetime"])
