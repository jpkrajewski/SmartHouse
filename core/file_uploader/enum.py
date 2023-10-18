from pydantic import BaseModel
from pathlib import Path


class FileData(BaseModel):
    """
    Represents the result of an upload operation
    Attributes:
        data (str | bytes): File data (bytes or string)
        path (Path | str): Path to file in local storage
        url (str): URL to file in remote storage
        filename (str): Name of the file.
        status (bool): True if the upload is successful else False.
        error (str): Error message for failed upload.
        message: Response Message
    """

    data: str | bytes = ""
    path: Path | str = ""
    url: str = ""
    filename: str = ""
    content_type: str = ""
    status: bool = True
    error: str = ""
    message: str = ""
