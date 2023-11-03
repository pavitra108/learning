"""
This code is designed to parse data from a .txt file and extract quotes from it.

It follows a specific structure, using the python-docx library for parsing the Word document.
"""

from QuoteEngine.ImportInterface import IngestorInterface
import QuoteEngine.QuoteModel1 as QuoteModel1


class TXTImporter(IngestorInterface):
    """This class extract quotes from a .txt file."""

    allowed_ext = ['.txt']

    @classmethod
    def parse(cls, path: str):
        """Parse the content in the file and returns a list of quotes."""
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        quotes = []
        print(path)
        with open(path, 'r') as infile:
            for line in infile:
                parse = line.strip().split('-')
                new_quote = QuoteModel1.QuoteModel(parse[0], parse[1])
                quotes.append(new_quote)
        return quotes
