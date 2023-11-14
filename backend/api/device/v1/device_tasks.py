from typing import List

from app.device.schemas import GetDeviceAutomatedTaskResponseSchema
from app.device.services import DeviceService
from core.fastapi.dependencies import IsAuthenticated, PermissionDependency
from fastapi import APIRouter, Depends

device_tasks_router = APIRouter()


@device_tasks_router.get(
    "",
    response_model=List[GetDeviceAutomatedTaskResponseSchema],
    response_model_exclude={"user_id"},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_device_tasks(
    result=Depends(DeviceService.get_device_automated_task_list),
):
    return result
