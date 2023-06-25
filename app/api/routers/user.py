"""
This module contains the API routes and their corresponding
functions for handling user-related requests.
"""

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import user as user_schemas
from services import UserService, get_db
from auth.jwt_bearer import JWTBearer


router = APIRouter(prefix="/user", tags=["user"], dependencies=[Depends(JWTBearer())])


@router.get("/{user_id}", response_model=user_schemas.User, status_code=200)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the information of a specific user by ID.

    :param user_data: the information of the new user to be created.
    :param db: Database session

    :raise HTTPException: 404 status code with "User not found!" message
    if the specified user ID does not exist in the database.

    :return: the user data corresponding to the given ID
    """
    user = UserService.get_user_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return user


@router.get("/", response_model=list[user_schemas.User], status_code=200)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0),
    db: Session = Depends(get_db),
):
    """
    Retrieves a list of users with pagination options (skip, limit).

    :param db: Database session
    :param skip: (optional) the number of records to skip (default: 0)
    :param limit: (optional) the maximum number of records to retrieve (default: 100)

    :raise HTTPException: 404 status code with "User not found!" message
    if the specified range of user ID's does not exist in the database.

    :return: a list of user data, where skip < user_id < limit
    """
    users = UserService.get_users(skip=skip, limit=limit, db=db)
    return users


@router.put("/", response_model=user_schemas.User, status_code=201)
async def put_user(user_data: user_schemas.UserPut, db: Session = Depends(get_db)):
    """
    Creates a new user with the given information and returns the user information.

    :param user_data: the information of the new user to be created.
    :param db: Database session

    :raise HTTPException: 409 status code with "Email already registered"
    message if the provided email already exists in the database.

    :return: the newly-inserted user record
    """
    if UserService.get_user_by_email(db=db, email=user_data.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return UserService.put_user(db=db, user_data=user_data)


@router.patch("/{user_id}", response_model=user_schemas.User, status_code=200)
async def patch_user(
    user_id: int, user_data: user_schemas.UserPatch, db: Session = Depends(get_db)
):
    """
    Updates the information of an existing user with the provided data and
    returns the updated user information.

    :param user_id: the user ID to patch
    :param user_data: the information of the new user to be created.
    :param db: Database session

    :raise HTTPException: 404 status code with "User not found!" message
    if the specified user ID does not exist in the database.
    :raise HTTPException: 409 status code with "Email already registered"
    message if the provided email already exists in the database.

    :return: the updated user record
    """
    if not UserService.get_user_by_id(db=db, id=user_id):
        raise HTTPException(status_code=404, detail="User not found!")
    if UserService.get_user_by_email(db=db, email=user_data.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return UserService.patch_user(db=db, user_id=user_id, user_data=user_data)


@router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes the user with the specified email.

    :param id: The id of the user to be deleted.
    :param db: Database session

    :raise HTTPException: 404 status code with "User not found!" message
    if the specified user ID does not exist in the database.

    :return: the updated user record
    """
    if not UserService.get_user_by_id(db=db, id=user_id):
        raise HTTPException(status_code=404, detail="User not found!")
    return UserService.delete_user(db=db, id=user_id)
