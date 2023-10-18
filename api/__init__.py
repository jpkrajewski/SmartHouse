from fastapi import APIRouter

from api.user.v1.user import user_router as user_v1_router
from api.device.v1.device import device_router as devices_v1_router
from api.auth.auth import auth_router

router = APIRouter()
router.include_router(user_v1_router, prefix="/api/v1/users", tags=["User"])
router.include_router(devices_v1_router, prefix="/api/v1/devices", tags=["Devices"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])


__all__ = ["router"]
