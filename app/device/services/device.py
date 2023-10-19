from typing import Optional, List

from sqlalchemy import or_, select, and_
import csv
from pathlib import Path
from app.user.models import User
from app.device.models import Device, DeviceRaport
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
