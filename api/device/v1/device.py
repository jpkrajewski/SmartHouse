from typing import List, Annotated
from datetime import datetime
from fastapi import APIRouter, Response, Depends, Request, Query
from app.device.schemas import GetDeviceListResponseSchema
from app.device.services import DeviceService
from core.fastapi.dependencies import PermissionDependency, AllowAll
from fastapi.responses import FileResponse
from app.device.schemas import ExceptionResponseSchema
from core.file_handler import BaseFileExtension, FileUploadPlace, FileUploaderFactory
from core.report_generators import ReportGeneratorFactory


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
    "/{device_id}/report",
    response_class=FileResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def get_device_report(
    request: Request,
    device_id: int,
    extension: Annotated[
        BaseFileExtension, Query(description="Report format")
    ] = BaseFileExtension.CSV,
    upload_to: Annotated[
        FileUploadPlace, Query(description="Save report to")
    ] = FileUploadPlace.LOCAL,
    start_date: Annotated[
        datetime | None, Query(description="Start date of report")
    ] = None,
    end_date: Annotated[
        datetime | None, Query(description="End date of report")
    ] = None,
):
    generator = ReportGeneratorFactory.create(extension)
    report_file = await DeviceService().get_device_report(
        request.user.id, device_id, start_date, end_date, generator
    )
    uploader = FileUploaderFactory.create(upload_to)
    uploader.upload(report_file)
    return Response(
        content=report_file.content,
        media_type=report_file.media_type,
        headers=report_file.headers,
    )
