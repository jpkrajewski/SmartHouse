from typing import List

from app.device.schemas import GetDeviceMeasurementResponseSchema
from app.device.services import get_measurements
from core.fastapi.dependencies import AllowAll, PermissionDependency
from fastapi import APIRouter, Depends

device_measurements_router = APIRouter()


@device_measurements_router.get(
    "",
    response_model=List[GetDeviceMeasurementResponseSchema],
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def get_devices(result=Depends(get_measurements)):
    return result
