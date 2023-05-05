from fastapi import APIRouter

from .pool import router as pool_router
from .pool_model import router as pool_model_router


router = APIRouter(prefix="/pool")

router.include_router(pool_router)
router.include_router(pool_model_router)
