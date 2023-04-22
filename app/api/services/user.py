"""
This module provides services which are used
to send requests directly to the database
"""

from typing import List
from sqlalchemy.orm import Session
from schemas import user as user_schemas
from models import user as user_models
from fastapi.responses import JSONResponse


def get_user_by_id(db: Session, id: int) -> user_models.User | None:
    """
    Returns the user data found by user id

    :param db: Database session
    :param id: the user ID to retrieve

    :return: the user data corresponding to the given ID or None if not found
    """
    return db.query(user_models.User).filter(user_models.User.id == id).first()


def get_user_by_email(db: Session, email: str) -> user_models.User | None:
    """
    Returns the user data found by user email

    :param db: Database session
    :param email: the user email to retrieve

    :return: the user data corresponding to the given email or None if not found
    """
    return db.query(user_models.User).filter(user_models.User.email == email).first()


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> List[user_models.User] | None:
    """
    Returns a list of user data, with optional pagination

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :return: a list of user data, where skip < user_id < limit
    """

    return db.query(user_models.User).offset(skip).limit(limit).all()

def put_user(db: Session, user_data: user_schemas.UserPut) -> user_models.User:
    """
    Inserts a new user record into the database

    :param db: Database session
    :param user_data: the user data to insert

    :return: the newly-inserted user record
    """
    db_user = user_models.User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def patch_user(
    db: Session, user_id: int, user_data: user_schemas.UserPatch
) -> user_models.User:
    """
    Updates an existing user record in the database

    :param db: Database session
    :param user_id: the user ID to patch
    :param user_data: the user data to update

    :return: the updated user record
    db_user = get_user_by_id(db=db, id=user_id)
    for key, value in user_data.dict(exclude_none=True).items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, id: str) -> JSONResponse:
    """
    Deletes a user record from the database

    :param db: Database sessioner
    :param id: the user ID to delete

    :return: a json with a "detail" key indicating success
    """
    db.query(user_models.User).filter(user_models.User.id == id).delete()
    db.commit()
    return JSONResponse({"detail": "success"}, status_code=200)
