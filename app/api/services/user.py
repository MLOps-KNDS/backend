from sqlalchemy.orm import Session
from schemas import user as user_schemas
from models import user as user_models


def get_user_by_id(db: Session, id: int):
    return db.query(user_models.User).filter(user_models.User.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_models.User).filter(user_models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(user_models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user_data: user_schemas.UserCreate):
    db_user = user_models.User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, id: int):
    db.query(user_models.User).filter(user_models.User.id == id).delete()
    db.commit()
    return {"detail": "success"}
