import logging
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).one_or_none()


def save_user(db: Session, user_data: schemas.UserData) -> models.User | None:

    db_user = models.User(
        id=user_data.vkid,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def get_event(db: Session, event_id: int) -> models.Event | None:
    return db.query(models.Event).filter(models.Event.id == event_id).one_or_none()


def create_event(
    db: Session, event_data: schemas.EventData, user: models.User
) -> models.Event | None:

    db_event = get_event(db, event_data.id)
    if db_event:
        return None
    db_event = models.Event(
        name=event_data.name,
        description=event_data.description,
        owner_id=user.id,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(db: Session, event_data: schemas.EventData) -> models.Event | None:
    event_id = event_data.id
    db_event = get_event(db, event_id)
    if db_event:
        return db_event
    db_event = models.Event(**event_data)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
