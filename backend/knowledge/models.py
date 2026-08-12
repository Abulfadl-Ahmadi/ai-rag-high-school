from django.db import models

class Document(models.Model):
    STATUS_CHOICES = (
        ('UPLOADED', 'Uploaded'),
        ('PARSING', 'Parsing'),
        ('STRUCTURING', 'Structuring'),
        ('VALIDATING', 'Validating'),
        ('CHUNKING', 'Chunking'),
        ('EMBEDDING', 'Embedding'),
        ('READY', 'Ready'),
        ('FAILED', 'Failed'),
    )

    source_file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=50, blank=True, null=True)
    processing_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UPLOADED')
    parser_version = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.source_file.name} - {self.processing_status}"

class DocumentElement(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='elements')
    page_number = models.IntegerField(null=True, blank=True)
    element_type = models.CharField(max_length=50) # e.g., heading, paragraph, picture
    text = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['page_number', 'order']

    def __str__(self):
        return f"{self.element_type} (Page {self.page_number})"
