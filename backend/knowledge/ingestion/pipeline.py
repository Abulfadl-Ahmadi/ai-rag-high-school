import json
from pathlib import Path
from knowledge.models import Document
from .parsers.docling_parser import DoclingParser

def ingest_document(file_path: str):
    print(f"Starting ingestion for {file_path}")
    
    # 1. Create Document Record
    # We create a dummy Document object for now since we're testing the pipeline
    doc_record = Document.objects.create(
        source_file=file_path,
        processing_status='PARSING',
        parser_version='docling-v1'
    )

    try:
        # 2. Parse using Docling
        parser = DoclingParser()
        parsed_data = parser.parse(file_path)

        doc_record.processing_status = 'STRUCTURING' # We stop here for Milestone 1
        doc_record.save()

        # Save the raw JSON to a file for inspection
        output_path = Path(file_path).with_suffix('.raw.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)

        print(f"✓ PDF parsed successfully")
        print(f"✓ Raw JSON saved to {output_path}")

        # The next steps (cleaner, classifier, structure_detector) will be built 
        # after we inspect the raw Docling JSON.
        
        return doc_record

    except Exception as e:
        doc_record.processing_status = 'FAILED'
        doc_record.error_message = str(e)
        doc_record.save()
        print(f"❌ Ingestion failed: {str(e)}")
        raise
