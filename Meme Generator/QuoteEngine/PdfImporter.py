"""
This code is designed to parse data from a .pdf file and extract quotes from it.

It follows a specific structure, using the python-docx library for parsing the Word document.
"""

import subprocess
from QuoteEngine.ImportInterface import IngestorInterface
import QuoteEngine.QuoteModel1 as QuoteModel1


class PDFImporter(IngestorInterface):
    """This class extract quotes from a .pdf file."""

    allowed_ext = ['.pdf']

    @classmethod
    def parse(cls, path: str):
        """Parse the content in the file and returns a list of quotes."""
        output_file = 'output.txt'
        subprocess.run(['pdftotext', '-layout', path, output_file])

        quotes = []
        with open(output_file, 'r') as infile:
            for line in infile:
                parse = line.strip().split('-')
                if len(parse) == 2:
                    new_quote = QuoteModel1.QuoteModel(parse[0], parse[1])
                    quotes.append(new_quote)
        return quotes