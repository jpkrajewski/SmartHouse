from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy import or_, select, and_
import csv
from pathlib import Path
import asyncio
from app.user.models import User
from app.device.models import Device, DeviceRaport, DeviceAutomatedTask
from app.user.schemas.user import LoginResponseSchema
from core.db import Transactional, session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
    DeviceNotFoundException,
)
from core.utils.token_helper import TokenHelper
from core.report_generators import ReportGeneratorFactory, ReportGenerator
from core.file_handler import LocalStorgeFileUploader
from fastapi import APIRouter, Response, Depends, Request, Query

from typing import Annotated
from datetime import datetime
from core.file_handler import FileMetaData


class DeviceService:
    def __init__(self) -> None:
        ...

    async def get_device_list(
        self,
        user_id: int,
        limit: int = 10,
        prev: Optional[int] = None,
    ) -> List[Device]:
        # get only user's devices

        query = select(Device).where(Device.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_device_reportable_data(
        request: Request,
        device_id: int,
        start_date: Annotated[datetime, Query()] = Query(
            None, description="Start raport data details starting this datatime"
        ),
        end_date: Annotated[datetime, Query()] = Query(
            None, description="Raport data details to this datatime"
        ),
    ) -> list[Device]:
        """Get device info and other history data."""

        query = select(Device).where(Device.user_id == request.user.id)
        result = await session.execute(query)
        data = result.scalars().all()

        # if not data:
        #     raise DeviceNotFoundException

        # start_date end_date filter

        return data

    @Transactional()
    @staticmethod
    async def create_device_raport_metadata(
        request: Request, device_id: int, file: FileMetaData
    ) -> None:
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
                    DeviceAutomatedTask.start_date
                    <= rounded_datetime - timedelta(minutes=1),
                    # add between =- 2 minutes
                    DeviceAutomatedTask.start_date
                    >= rounded_datetime + timedelta(minutes=1),
                    DeviceAutomatedTask.is_done == False,
                    DeviceAutomatedTask.recurring == True,
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
        result = session.query(DeviceAutomatedTask).update(
            {DeviceAutomatedTask.is_done: False}
        )
        return result

    @Transactional()
    @staticmethod
    async def clear_device_automated_task_no_reocurring() -> None:
        result = (
            session.query(DeviceAutomatedTask)
            .filter(DeviceAutomatedTask.recurring == False)
            .delete()
        )
        return result
