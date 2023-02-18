from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from sql.models import User
from sql.schemas import Token, UserData, EventData, EventCreate, EventUpdate
import settings  # ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from sql import crud
from .dependencies import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(form: UserData, expires_data: Optional[timedelta] = None) -> str:
    # TODO: Save token
    form.dict()
    to_encode = {"vkid": form.vkid}
    if expires_data is not None:
        expire = datetime.utcnow() + expires_data
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return token


def decode_token_from_str(token) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        vkid: str = payload.get("vkid")
        if vkid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return vkid


def decode_token(db: Session, token: str) -> User | None:
    vkid = decode_token_from_str(token)
    user = crud.get_user(db, user_id=vkid)
    if user is None:
        raise HTTPException(404, "User not found")
    return user


async def authenticate_user(db: Session, form_data: UserData) -> User:
    user = crud.get_user(db, user_id=form_data.vkid)
    # exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Incorrect username or password",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    if user is None:
        crud.save_user(db, form_data)
    return user


@router.post("/token", response_model=Token)
async def get_token(form_data: UserData = Depends()):
    db = next(get_db())
    user = await authenticate_user(db, form_data)
    expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_token(form_data, expires_data=expires)
    return Token(access_token=access_token, token_type="Bearer")


@router.post("/login", response_model=Token)
async def login(login_data: UserData):
    db = next(get_db())
    user = await authenticate_user(db, **login_data.dict())
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(login_data, expires_data=expires)
    return Token(access_token=access_token, token_type="Bearer")


@router.get("/")
async def index(token: str = Depends(oauth2_scheme)):
    return {"the_token": token}


@router.post("/create_event", response_model=EventData)
async def create_event(event_data: EventCreate, token: str = Depends(oauth2_scheme)):
    db = next(get_db())
    user = decode_token(db, token=token)
    event = crud.create_event(db, event_data, user)
    if event:
        return EventData.from_orm(event)
    return HTTPException(500, "object already exists")


@router.post("/update_event", response_model=EventData)
async def update_event(event_data: EventUpdate, token: str = Depends(oauth2_scheme)):
    db = next(get_db())
    user = decode_token(db, token)
    event = crud.get_event(db, event_data.id)
    if event.owner.id != user.id:
        return {"error": "event was created by another user"}
    event = crud.update_event(db, event_data)
    return EventData.from_orm(event)




@router.post("/files/")
async def create_file(file: Union[bytes, None] = File(default=None)):
    # FIXME: реализовать загрузку файлов
    # https://hub.docker.com/r/halverneus/static-file-server
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
