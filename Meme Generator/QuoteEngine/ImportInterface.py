"""
This class serves as an abstract base class(ABC) for classes that will perform data ingestion from various file formats.

It includes two class methods, can_ingest and parse, which must be implemented by concrete subclasses.
"""

import os
from abc import ABC, abstractmethod


class IngestorInterface(ABC):
    """This class has two functions: ont to ingest data and another to parse data form files."""

    allowed_ext = []

    @classmethod
    def can_ingest(cls, filepath: str) -> bool:
        """Determine whether a given file can be ingested by a concrete subclass."""
        file_ext = os.path.splitext(filepath)[1]
        return file_ext in cls.allowed_ext

    @classmethod
    @abstractmethod
    def parse(cls, path: str):
        """Implement a parse method as an abstract method."""
        pass
