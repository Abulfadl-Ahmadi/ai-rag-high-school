import os
from django.core.management.base import BaseCommand
from knowledge.ingestion.pipeline import ingest_document

class Command(BaseCommand):
    help = 'Ingests a document through the document pipeline'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the document to ingest')

    def handle(self, *args, **options):
        file_path = options['file_path']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File "{file_path}" does not exist.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Starting ingestion for {file_path}'))
        
        try:
            ingest_document(file_path)
            self.stdout.write(self.style.SUCCESS('Successfully completed Milestone 1 ingestion.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during ingestion: {str(e)}'))
