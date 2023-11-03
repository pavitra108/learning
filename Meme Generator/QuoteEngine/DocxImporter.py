"""
This code is designed to parse data from a .docx file and extract quotes from it.

It follows a specific structure, using the python-docx library for parsing the Word document.
"""

import docx
from QuoteEngine.ImportInterface import IngestorInterface
from QuoteEngine.QuoteModel1 import QuoteModel

class DocxImporter(IngestorInterface):
    """This class extract quotes from a .docx file."""

    allowed_ext = ['.docx']

    @classmethod
    def parse(cls, path: str):
        """Parse the content in the file and returns a list of quotes."""
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        quotes = []
        print(path)
        doc = docx.Document(path)

        for para in doc.paragraphs:
            if para.text != "":
                parse = para.text.split('-')
                new_quote = QuoteModel(parse[0], parse[1])
                quotes.append(new_quote)
        return quotes
