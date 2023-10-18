from typing import List

from fastapi import APIRouter, Response, Depends, Request
from app.device.schemas import GetDeviceListResponseSchema
from app.device.services import DeviceService
from core.fastapi.dependencies import PermissionDependency, AllowAll


device_router = APIRouter()


@device_router.get("", dependencies=[Depends(PermissionDependency([AllowAll]))])
async def get_devices():
    return Response(status_code=200)


@device_router.get(
    "/{device_id}",
    response_model=List[GetDeviceListResponseSchema],
    response_model_exclude={"id"},
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def get_device(request: Request, device_id: int):
    return DeviceService().get_device_list(request.user.id, device_id=device_id)
