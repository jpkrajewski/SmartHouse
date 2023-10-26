from typing import List, Annotated
from datetime import datetime
from fastapi import APIRouter, Response, Depends, Request, Query
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

device_reports_router = APIRouter()


@device_reports_router.get(
    "",
    response_model=List[GetDeviceRaportListResponseSchema],
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def get_device_reports(report=Depends(DeviceService.get_device_reports)):
    return report
