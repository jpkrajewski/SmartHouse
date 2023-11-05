from app.device.services import DeviceService
from core.file_handler import FileResponse, FileUploader, FileUploaderFactory
from core.report_generators import ReportGenerator, ReportGeneratorFactory
from fastapi import Depends, Request


async def report_creation_handler(
    device_reportable_data: dict = Depends(DeviceService.get_device_reportable_data),
    generator: ReportGenerator = Depends(ReportGeneratorFactory.create),
    uploader: FileUploader = Depends(FileUploaderFactory.create),
):
    file = generator.generate(device_reportable_data)
    file_metadata = uploader.upload(file)
    return FileResponse(**file.dict(), metadata=file_metadata)


async def report_handler(
    request: Request,
    device_id: int,
    file: FileResponse = Depends(report_creation_handler),
):
    await DeviceService.create_device_raport_metadata(request, device_id, file=file.metadata)
    return file
