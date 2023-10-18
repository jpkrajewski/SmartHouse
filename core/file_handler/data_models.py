from pydantic import BaseModel, validator, Field
from pathlib import Path
from enum import Enum


class BaseFileExtension(Enum):
    EXCEL: str = "xlsx"
    CSV: str = "csv"
    PDF: str = "pdf"


class BaseFile(BaseModel):
    name: str
    content: str | bytes
    extension: BaseFileExtension

    @property
    def filename(self) -> str:
        return f"{self.name}.{self.extension.value}"


class FileResponse(BaseFile):
    name: str = Field(exclude=True)

    @property
    def headers(self) -> dict:
        return {"Content-Disposition": f'attachment; filename="{self.filename}"'}

    @property
    def media_type(self) -> str:
        return f"application/{self.extension.value}"


class FileUploadPlace(Enum):
    AWS = "aws"
    LOCAL = "local"
