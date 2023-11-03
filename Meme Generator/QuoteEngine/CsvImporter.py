"""
This code is designed to parse data from a .csv file and extract quotes from it.

It follows a specific structure, using the python-docx library for parsing the Word document.
"""

import pandas
from QuoteEngine.ImportInterface import IngestorInterface
import QuoteEngine.QuoteModel1 as QuoteModel1

class CSVImporter(IngestorInterface):
    """This class extract quotes from a .csv file."""

    allowed_ext = ['.csv']

    @classmethod
    def parse(cls, path: str):
        """Parse the content in the file and returns a list of quotes."""
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        quotes = []
        data = pandas.read_csv(path, header=0)

        for index, row in data.iterrows():
            new_quote = QuoteModel1.QuoteModel(row['body'], row['author'])
            quotes.append(new_quote)
        return quotes
