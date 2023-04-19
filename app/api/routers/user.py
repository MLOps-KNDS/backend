from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from schemas import user as user_schemas
from services import user as user_services
from services.deps import get_db


router = APIRouter()


@router.post("/users/", response_model=user_schemas.User)
def create_user(user_data: user_schemas.UserCreate, db: Session = Depends(get_db)):
    if user_services.get_user_by_email(db=db, email=user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_services.create_user(db=db, user_data=user_data)


@router.get("/users/", response_model=List[user_schemas.User])
def read_users(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    users = user_services.get_users(skip=skip, limit=limit, db=db)
    return users


@router.get("/users/{user_id}", response_model=user_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = user_services.get_user_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return user


@router.post("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not user_services.get_user_by_id(db=db, id=user_id):
        raise HTTPException(status_code=404, detail="User not found!")
    return user_services.delete_user(user_id=user_id, db=db)
