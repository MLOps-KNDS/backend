from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from services import user
from services.deps import get_db

router = APIRouter()


@router.post("/users/", tags=["users"])
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return user.create_user(db=db, user_data=user_data)
