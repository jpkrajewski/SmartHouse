from app.device.models import DeviceMeasurement
from core.db import Transactional, session
from sqlalchemy import select


async def get_measurements():
    query = select(DeviceMeasurement)
    result = await session.execute(query)
    data = result.scalars().all()
    return data


@Transactional()
async def add_measurement(data: dict):
    record = DeviceMeasurement(**data)
    print(record)
    session.add(record)
    return record
