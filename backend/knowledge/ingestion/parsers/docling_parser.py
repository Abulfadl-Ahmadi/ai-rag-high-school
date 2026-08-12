from .base import DocumentParser
from docling.document_converter import DocumentConverter
import json

class DoclingParser(DocumentParser):
    def __init__(self):
        self.converter = DocumentConverter()

    def parse(self, file_path: str) -> dict:
        """
        Uses Docling to convert the PDF to a structured representation.
        """
        result = self.converter.convert(file_path)
        # result.document contains the DoclingDocument
        # We export it to a dictionary
        return result.document.export_to_dict()
