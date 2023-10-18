from fastapi.responses import Response
from .data_models import BaseFile, FileResponse


class FileResponder:
    @staticmethod
    def get_response(file: BaseFile) -> FileResponse:
        return FileResponse(**dict(file))
