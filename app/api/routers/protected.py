from fastapi import APIRouter, Depends
from config.security import verify_google_token


router = APIRouter(
    prefix="/protected", tags=["protected"], dependencies=[Depends(verify_google_token)]
)


@router.get("/")
async def protected():
    return {"message": "Access granted"}
