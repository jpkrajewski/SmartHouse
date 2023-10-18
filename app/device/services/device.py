from typing import Optional, List

from sqlalchemy import or_, select, and_
import csv
from pathlib import Path
from app.user.models import User
from app.device.models import Device
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
from core.file_handler import LocalStorgeFileUploader, FileResponder


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

    async def get_device_report(
        self,
        user_id: int,
        device_id: int,
        start_date: Optional[str],
        end_date: Optional[str],
        generator: ReportGenerator,
    ) -> Path:
        query = select(Device).where(Device.user_id == user_id)
        result = await session.execute(query)
        data = result.scalars().all()

        # if not data:
        #     raise DeviceNotFoundException

        csv_data = generator.generate(data)
        return FileResponder.get_response(csv_data)
