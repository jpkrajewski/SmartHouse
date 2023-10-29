from pydantic import BaseModel, Field, validator
from uuid import uuid4
from enum import Enum
from core.file_handler.data_models import BaseFile


class ReportFile(BaseFile):
    name: str = Field(default_factory=lambda: uuid4().hex)
