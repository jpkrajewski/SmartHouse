from abc import ABC, abstractmethod
import csv
import io
from .enum import ReportData, ReportExtension


class ReportGenerator(ABC):
    EXTENSION = None

    @abstractmethod
    def generate(self, data: dict) -> str:
        pass


class CSVDeviceReportGenerator(ReportGenerator):
    EXTENSION = ReportExtension.CSV

    def generate(self, data: dict) -> str:
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        header = ["1", "2"]
        writer.writerow(header)
        for row_data in [[1, 2], [3, 4], [5, 6]]:
            writer.writerow(row_data)
        content = buffer.getvalue()
        buffer.close()
        return ReportData(
            content=content,
            extension=self.EXTENSION,
        )


class ExcelDeviceReportGenerator(ReportGenerator):
    def generate(self, data: dict) -> str:
        pass


class PDFDeviceReportGenerator(ReportGenerator):
    def generate(self, data: dict) -> str:
        pass
