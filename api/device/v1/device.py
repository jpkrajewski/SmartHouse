from typing import List

from fastapi import APIRouter, Response, Depends, Request
from app.device.schemas import (
    GetDeviceResponseSchema,
    CreateDeviceRequestSchema,
    UpdateDeviceRequestSchema,
    DeleteDeviceResponseSchema,
    UpdateDeviceResponseSchema,
)
from app.device.services import DeviceService
from core.fastapi.dependencies import PermissionDependency, AllowAll, IsAuthenticated


device_router = APIRouter()


@device_router.get(
    "",
    response_model=List[GetDeviceResponseSchema],
    response_model_exclude={"user_id"},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_devices(result=Depends(DeviceService.get_device_list)):
    return result


@device_router.get(
    "/{device_id}",
    response_model=GetDeviceResponseSchema,
    response_model_exclude={"user_id"},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_device(request: Request, device_id: int):  # dane
    result = await DeviceService.get_device(request, device_id)  # <----
    return result


@device_router.post(
    "",
    response_model=GetDeviceResponseSchema,
    response_model_exclude={"user_id"},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def create_device(result=Depends(DeviceService.create_device)):
    return result


@device_router.delete(
    "/{device_id}",
    response_model=DeleteDeviceResponseSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def delete_device(result=Depends(DeviceService.delete_device)):
    return result


@device_router.put(
    "/{device_id}",
    response_model=UpdateDeviceResponseSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def update_device(
    result=Depends(DeviceService.update_device),
):
    return result


# "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJleHAiOjE2OTg2MDQ5NzJ9.hFeF_SqumJ8HY5inEcAprGtBb0BEsDpa-_7GFxah-8c"
