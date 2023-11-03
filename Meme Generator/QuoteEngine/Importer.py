"""This class creates a generic method that can handle different file formats and parse data."""

from QuoteEngine.ImportInterface import IngestorInterface
from .DocxImporter import DocxImporter
from .CsvImporter import CSVImporter
from .PdfImporter import PDFImporter
from .TxtImporter import TXTImporter


class Ingestor(IngestorInterface):
    """This class creates a generic method that can handle different file formats and parse data."""

    formats = [DocxImporter, PDFImporter, TXTImporter, CSVImporter]

    @classmethod
    def parse(cls, path: str):
        """Create a generic method to parse data from appropriate file formats."""
        for each in cls.formats:
            if each.can_ingest(path):
                return each.parse(path)

