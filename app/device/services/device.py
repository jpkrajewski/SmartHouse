from typing import Optional, List

from sqlalchemy import or_, select, and_

from app.user.models import User
from app.device.models import Device
from app.user.schemas.user import LoginResponseSchema
from core.db import Transactional, session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from core.utils.token_helper import TokenHelper


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
