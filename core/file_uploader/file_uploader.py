from abc import ABC, abstractmethod
from core.config import config
from core.file_uploader.enum import FileData
from pathlib import Path
import os
from datetime import datetime


class FileUploader(ABC):
    @abstractmethod
    def upload(self, data: dict) -> str:
        pass


class LocalStorgeFileUploader(FileUploader):
    """
    Local storage for FastAPI.
    """

    def upload(self, file: FileData, folder="files") -> FileData:
        """
        Upload a file to the destination.
        Args:
            file UploadFile: File to upload
        Returns:
            FileData: Result of file upload
        """
        try:
            dest = Path(config.STORAGE_LOCAL_PATH, folder)
            if not dest.exists():
                dest.mkdir(parents=True)

            file_path = Path(dest, file.filename)
            with open(file_path, "w") as fh:
                fh.write(file.content)
            return FileData(
                path=file_path,
                message=f"{file.filename} saved successfully",
                filename=file.filename,
            )
        except Exception as err:
            return FileData(
                status=False, error=str(err), message=f"Unable to save file"
            )


class S3FileUploader(FileUploader):
    def save(self, data: dict) -> str:
        pass
