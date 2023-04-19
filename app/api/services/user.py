from sqlalchemy.orm import Session
from schemas.user import UserCreate
from models.user import User as UserScheme


def create_user(user_data: UserCreate, db: Session):
    db_user = UserScheme(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
