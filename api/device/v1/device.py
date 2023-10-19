from typing import List, Annotated
from datetime import datetime
from fastapi import APIRouter, Response, Depends, Request, Query
from app.device.schemas import GetDeviceListResponseSchema
from app.device.services import DeviceService
from core.fastapi.dependencies import PermissionDependency, AllowAll
from fastapi.responses import FileResponse
from app.device.schemas import (
    ExceptionResponseSchema,
    GetDeviceRaportListResponseSchema,
)
from core.file_handler import (
    BaseFileExtension,
    FileUploadPlace,
    FileUploaderFactory,
    FileResponse,
)
from core.report_generators import ReportGeneratorFactory
from app.device.dependencies.report import report_creation_handler, report_handler
from app.device.services import DeviceService


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


@device_router.get(
    "/{device_id}/generate-report",
    response_class=Response,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def get_create_device_report(report_file=Depends(report_handler)):
    return Response(
        content=report_file.content,
        media_type=report_file.media_type,
        headers=report_file.headers,
    )
