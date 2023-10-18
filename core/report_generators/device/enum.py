from pydantic import BaseModel, Field
from uuid import uuid4
from enum import Enum


class ReportExtension(Enum):
    EXCEL: str = "xlsx"
    CSV: str = "csv"
    PDF: str = "pdf"


class ReportData(BaseModel):
    name: str = Field(default_factory=lambda: uuid4().hex)
    content: str | bytes
    extension: ReportExtension

    @property
    def filename(self) -> str:
        return f"{self.name}.{self.extension.value}"
