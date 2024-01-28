from uuid import uuid4

from core.file_handler.data_models import BaseFile
from pydantic import Field


class ReportFile(BaseFile):
    name: str = Field(default_factory=lambda: uuid4().hex)
