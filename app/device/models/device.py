from sqlalchemy import Column, Unicode, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import TimestampMixin


class Device(Base, TimestampMixin):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(255), nullable=False)
    is_in = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class DeviceAutomatedTask(Base, TimestampMixin):
    __tablename__ = "device_automated_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(255), nullable=False)
    command = Column(Unicode(255), nullable=False)
    recurring = Column(Boolean, default=True)
    is_done = Column(Boolean, default=False)
    start_date = Column(DateTime, nullable=False)

    invoke_after = Column(
        Integer, ForeignKey("device_automated_tasks.id"), nullable=True
    )
    invoke_after_task = relationship("DeviceAutomatedTask", remote_side=[id])
    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class DeviceRaport(Base):
    __tablename__ = "device_raports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), nullable=False)
    path = Column(Unicode(255), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
