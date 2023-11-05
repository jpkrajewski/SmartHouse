import asyncio
from datetime import datetime, timedelta
from typing import Annotated, List

from app.device.models import Device, DeviceAutomatedTask, DeviceRaport
from app.device.schemas import (
    CreateDeviceRequestSchema,
    DeleteDeviceResponseSchema,
    UpdateDeviceRequestSchema,
    UpdateDeviceResponseSchema,
)
from core.db import Transactional, session
from core.exceptions import DeviceNotFoundException
from core.file_handler import FileMetaData
from fastapi import Query, Request
from sqlalchemy import and_, delete, select, update


class DeviceService:
    @staticmethod
    async def get_device_list(
        request: Request,
    ) -> List[Device]:
        query = select(Device).where(Device.user_id == request.user.id)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_device(
        request: Request,
        device_id: int,
    ) -> Device:
        query = select(Device).where(Device.id == device_id, Device.user_id == request.user.id)
        result = await session.execute(query)
        return result.scalar()

    @Transactional()
    @staticmethod
    async def create_device(
        request: Request,
        request_data: CreateDeviceRequestSchema,
    ) -> Device:
        device = Device(
            user_id=request.user.id,
            name=request_data.name,
            description=request_data.description,
        )
        session.add(device)
        return device

    @Transactional()
    @staticmethod
    async def delete_device(
        request: Request,
        device_id: int,
    ) -> DeleteDeviceResponseSchema:
        query = delete(Device).where(Device.id == device_id, Device.user_id == request.user.id)
        result = await session.execute(query)
        if result.rowcount == 0:
            raise DeviceNotFoundException
        return DeleteDeviceResponseSchema(id=device_id)

    @Transactional()
    @staticmethod
    async def update_device(
        request: Request,
        device_id: int,
        data: UpdateDeviceRequestSchema,
    ) -> UpdateDeviceResponseSchema:
        query = (
            update(Device)
            .where(Device.id == device_id, Device.user_id == request.user.id)
            .values(name=data.name, description=data.description)
        )
        result = await session.execute(query)
        if result.rowcount == 0:
            raise DeviceNotFoundException
        return UpdateDeviceResponseSchema(
            id=device_id,
            name=data.name,
            description=data.description,
            is_active=data.is_active,
        )

    @staticmethod
    async def get_device_reportable_data(
        request: Request,
        device_id: int,
        start_date: Annotated[datetime, Query()] = Query(
            None, description="Start raport data details starting this datatime"
        ),
        end_date: Annotated[datetime, Query()] = Query(None, description="Raport data details to this datatime"),
    ) -> list[Device]:
        """Get device info and other history data."""
        query = select(Device).where(Device.user_id == request.user.id)
        result = await session.execute(query)
        if not result:
            raise DeviceNotFoundException
        return result.scalars().all()

    @Transactional()
    @staticmethod
    async def create_device_raport_metadata(request: Request, device_id: int, file: FileMetaData) -> None:
        if file.path is None:
            return

        device_raport = DeviceRaport(
            user_id=request.user.id,
            device_id=device_id,
            name=file.filename,
            path=str(file.path),
        )
        session.add(device_raport)

    @staticmethod
    async def get_device_reports(
        request: Request,
    ) -> list[DeviceRaport]:
        """Get device info and other history data."""

        query = select(DeviceRaport).where(DeviceRaport.user_id == request.user.id)
        result = await session.execute(query)
        data = result.scalars().all()
        if not data:
            raise DeviceNotFoundException
        return data

    @Transactional()
    @staticmethod
    async def check_invockable_device_automated_task(rounded_datetime: datetime):
        result = (
            session.query(DeviceAutomatedTask)
            .filter(
                and_(
                    DeviceAutomatedTask.start_date <= rounded_datetime - timedelta(minutes=1),
                    # add between =- 2 minutes
                    DeviceAutomatedTask.start_date >= rounded_datetime + timedelta(minutes=1),
                    DeviceAutomatedTask.is_done is False,
                    DeviceAutomatedTask.recurring is True,
                )
            )
            .all()
        )
        tasks = []
        for task in result:
            task.is_done = True
            session.add(task)
            tasks.append(DeviceService.invoke_device_automated_task(task))
            responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

    @staticmethod
    async def invoke_device_automated_task(task: DeviceAutomatedTask):
        command = task.command
        await asyncio.sleep(1)  # will implement later
        return command

    @Transactional()
    @staticmethod
    async def change_device_automated_task_to_undone() -> None:
        result = session.query(DeviceAutomatedTask).update({DeviceAutomatedTask.is_done: False})
        return result

    @Transactional()
    @staticmethod
    async def clear_device_automated_task_no_reocurring() -> None:
        result = session.query(DeviceAutomatedTask).filter(DeviceAutomatedTask.recurring is False).delete()
        return result

    @staticmethod
    async def get_device_automated_task_list(
        request: Request,
    ) -> List[DeviceAutomatedTask]:
        query = select(DeviceAutomatedTask).where(DeviceAutomatedTask.user_id == request.user.id)
        result = await session.execute(query)
        return result.scalars().all()
