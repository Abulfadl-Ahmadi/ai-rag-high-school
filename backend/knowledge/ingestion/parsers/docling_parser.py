from .base import DocumentParser
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions
from docling.datamodel.base_models import InputFormat
import json

class DoclingParser(DocumentParser):
    def __init__(self):
        pipeline_options = PdfPipelineOptions()
        # Enable EasyOCR with Persian and Arabic support
        pipeline_options.do_ocr = True
        pipeline_options.ocr_options = EasyOcrOptions(lang=['fa', 'ar', 'en'], force_full_page_ocr=True)

        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def parse(self, file_path: str) -> dict:
        """
        Uses Docling to convert the PDF to a structured representation.
        """
        result = self.converter.convert(file_path)
        # result.document contains the DoclingDocument
        # We export it to a dictionary
        return result.document.export_to_dict()
