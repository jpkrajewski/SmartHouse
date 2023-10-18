from abc import ABC, abstractmethod
import csv
import io
from core.file_handler import BaseFileExtension
from .data_models import ReportFile


class ReportGenerator(ABC):
    EXTENSION = None

    @abstractmethod
    def generate(self, data: dict) -> str:
        pass


class CSVDeviceReportGenerator(ReportGenerator):
    EXTENSION = BaseFileExtension.CSV

    def generate(self, data: dict) -> str:
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        header = ["1", "2"]
        writer.writerow(header)
        for row_data in [[1, 2], [3, 4], [5, 6]]:
            writer.writerow(row_data)
        content = bytes(buffer.getvalue(), encoding="utf-8")
        buffer.close()
        return ReportFile(
            content=content,
            extension=self.EXTENSION,
        )


class ExcelDeviceReportGenerator(ReportGenerator):
    EXTENSION = BaseFileExtension.EXCEL

    def generate(self, data: dict) -> str:
        pass


class PDFDeviceReportGenerator(ReportGenerator):
    EXTENSION = BaseFileExtension.PDF

    def generate(self, data: dict) -> str:
        pass


class ReportGeneratorFactory:
    @staticmethod
    def create(extension: BaseFileExtension) -> ReportGenerator:
        if extension == BaseFileExtension.CSV:
            return CSVDeviceReportGenerator()
        elif extension == BaseFileExtension.EXCEL:
            return ExcelDeviceReportGenerator()
        elif extension == BaseFileExtension.PDF:
            return PDFDeviceReportGenerator()
        else:
            raise ValueError(f"Invalid extension: {extension}")
