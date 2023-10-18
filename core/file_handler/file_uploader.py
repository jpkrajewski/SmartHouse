from abc import ABC, abstractmethod
from core.config import config
from pathlib import Path
import os
from datetime import datetime
from .data_models import FileUploadPlace


class FileUploader(ABC):
    @abstractmethod
    def upload(self, data: dict) -> str:
        pass


class LocalStorgeFileUploader(FileUploader):
    """
    Local storage for FastAPI.
    """

    def upload(self, file, folder: str = "files"):
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
            return True
        except Exception as err:
            return False


class S3FileUploader(FileUploader):
    def save(self, data: dict) -> str:
        pass


class FileUploaderFactory:
    @staticmethod
    def create(upload_to: FileUploadPlace) -> FileUploader:
        if upload_to == FileUploadPlace.LOCAL:
            return LocalStorgeFileUploader()
        elif upload_to == FileUploadPlace.AWS:
            return S3FileUploader()
        else:
            raise ValueError("Invalid storage configuration.")
