from abc import ABC, abstractmethod
from pathlib import Path

from core.config import config

from .data_models import BaseFile, FileMetaData, FileUploadPlace


class FileUploader(ABC):
    @abstractmethod
    def upload(self, file: BaseFile) -> FileMetaData:
        pass


class NoUploadFileUploader(FileUploader):
    """No storage for FastAPI."""

    def upload(self, file: BaseFile) -> FileMetaData:
        return FileMetaData(filename="", path=None)


class LocalStorgeFileUploader(FileUploader):
    """Local storage for FastAPI."""

    def upload(self, file: BaseFile, folder: str = "files") -> FileMetaData:
        dest = Path(config.STORAGE_LOCAL_PATH, folder)
        dest.mkdir(parents=True, exist_ok=True)
        file_path = Path(dest, file.filename)
        with open(file_path, "w") as f:
            f.write(file.content)
        return FileMetaData(filename=file.filename, path=file_path)


class S3FileUploader(FileUploader):
    """AWS S3 storage for FastAPI."""

    def upload(self, file: BaseFile) -> FileMetaData:
        pass


class FileUploaderFactory:
    @staticmethod
    def create(upload_to: FileUploadPlace) -> FileUploader:
        file_uploaders = {
            FileUploadPlace.NO_UPLOAD: NoUploadFileUploader(),
            FileUploadPlace.LOCAL: LocalStorgeFileUploader(),
            FileUploadPlace.AWS: S3FileUploader(),
        }
        if upload_to in file_uploaders:
            return file_uploaders[upload_to]
        raise ValueError("Invalid storage configuration.")
