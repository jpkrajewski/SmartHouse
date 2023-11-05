from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, FilePath, FileUrl


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


class FileMetaData(BaseModel):
    filename: str
    path: Optional[Union[FilePath, FileUrl]]


class FileResponse(BaseFile):
    metadata: Optional[FileMetaData]

    @property
    def headers(self) -> dict:
        return {"Content-Disposition": f'attachment; filename="{self.filename}"'}

    @property
    def media_type(self) -> str:
        return f"application/{self.extension.value}"


class FileUploadPlace(Enum):
    NO_UPLOAD = "no_upload"
    AWS = "aws"
    LOCAL = "local"
