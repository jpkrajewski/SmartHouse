from typing import List

from fastapi import APIRouter, Response, Depends, Request
from app.device.schemas import GetDeviceResponseSchema, CreateDeviceRequestSchema, UpdateDeviceRequestSchema
from app.device.services import DeviceService
from core.fastapi.dependencies import PermissionDependency, AllowAll


device_router = APIRouter()


@device_router.get(
    "",
    response_model=List[GetDeviceResponseSchema],
    response_model_exclude={"id"},
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def get_devices(device=Depends(DeviceService.get_device_list)):
    return device


@device_router.get(
    "/{device_id}",
    response_model_exclude={"id"},
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def get_device(request: Request, device_id: int):  # dane
    result = await DeviceService.get_device(request, device_id)  # <----
    return result


@device_router.post("", dependencies=[Depends(PermissionDependency([AllowAll]))])
async def create_device(request: Request, request_data: CreateDeviceRequestSchema):
    result = await DeviceService.create_device(request, request_data)
    return result

@device_router.put(
        "/{device_id}", 
        response_model=GetDeviceResponseSchema,
        response_model_exclude={"id"},
        dependencies=[Depends(PermissionDependency([AllowAll]))])
async def update_device(
    request: Request,
    device_id: int,
    request_data: UpdateDeviceRequestSchema
):
    result = await DeviceService.update_device(request, device_id, request_data)
    return result
       