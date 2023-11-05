from typing import List

from app.device.dependencies.report import report_handler
from app.device.schemas import GetDeviceRaportListResponseSchema
from app.device.services import DeviceService
from core.fastapi.dependencies import AllowAll, PermissionDependency
from fastapi import APIRouter, Depends, Response

device_reports_router = APIRouter()


@device_reports_router.get(
    "",
    response_model=List[GetDeviceRaportListResponseSchema],
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def get_device_reports(report=Depends(DeviceService.get_device_reports)):
    return report


@device_reports_router.get(
    "/create-report/{device_id}",
    response_class=Response,
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def create_report(report=Depends(report_handler)):
    return Response(
        content=report.content,
        media_type=report.media_type,
        headers=report.headers,
    )
