from abc import ABC, abstractmethod

class DocumentParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> dict:
        """
        Parses a document from the given file path and returns a raw dictionary representation.
        """
        pass
