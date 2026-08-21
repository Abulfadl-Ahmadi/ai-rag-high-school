import uuid
from django.db import models

class Grade(models.Model):
    name = models.CharField(max_length=50) # e.g. دوازدهم
    code = models.IntegerField(unique=True) # e.g. 12

    def __str__(self):
        return f"پایه {self.name} ({self.code})"

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=100) # e.g. علوم تجربی و ریاضی
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100) # e.g. دین و زندگی
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='books')
    field = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE, related_name='books')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200) # e.g. دین و زندگی ۳
    academic_year = models.CharField(max_length=20, default='1404-1405')
    source_pdf_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.grade.name} ({self.academic_year})"

class Lesson(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='lessons')
    lesson_number = models.IntegerField()
    title = models.CharField(max_length=250)
    part_title = models.CharField(max_length=250, blank=True, null=True)
    page_start = models.IntegerField()
    page_end = models.IntegerField()
    summary = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['book', 'lesson_number']
        unique_together = ('book', 'lesson_number')

    def __str__(self):
        return f"درس {self.lesson_number}: {self.title} (ص {self.page_start}-{self.page_end})"

class BookSection(models.Model):
    SECTION_TYPES = (
        ('main_text', 'متن اصلی'),
        ('verse_reflection', 'تفکر در آیات و روایات'),
        ('review', 'بررسی و تطبیق'),
        ('thought_and_research', 'اندیشه و تحقیق'),
        ('activity', 'فعالیت کلاسی'),
        ('suggestion', 'پیشنهاد و مطالعه'),
        ('reading', 'استماع و قرائت'),
    )

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='sections')
    section_id = models.CharField(max_length=100, blank=True, null=True)
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES, default='main_text')
    section_title = models.CharField(max_length=250, blank=True, null=True)
    page_start = models.IntegerField()
    page_end = models.IntegerField()
    content = models.TextField()

    class Meta:
        ordering = ['lesson', 'page_start', 'id']

    def __str__(self):
        return f"{self.lesson.title} - {self.section_title} (ص {self.page_start})"

class Verse(models.Model):
    section = models.ForeignKey(BookSection, on_delete=models.CASCADE, related_name='verses', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='verses')
    surah = models.CharField(max_length=100)
    ayah = models.IntegerField()
    arabic_text = models.TextField(blank=True, null=True)
    translation = models.TextField(blank=True, null=True)
    reference = models.CharField(max_length=200)

    def __str__(self):
        return f"سوره {self.surah} آیه {self.ayah} (درس {self.lesson.lesson_number})"

class DocumentChunk(models.Model):
    section = models.ForeignKey(BookSection, on_delete=models.CASCADE, related_name='chunks', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='chunks')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chunks')
    
    chunk_index = models.IntegerField(default=0)
    original_content = models.TextField()
    contextual_content = models.TextField(blank=True, null=True)
    
    page_start = models.IntegerField()
    page_end = models.IntegerField()
    token_count = models.IntegerField(default=0)
    
    metadata = models.JSONField(default=dict, blank=True)
    # Stored as JSON array of floats for cross-platform SQLite / Postgres portability
    embedding_vector = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['book', 'lesson', 'page_start', 'chunk_index']

    def __str__(self):
        return f"Chunk {self.id} | درس {self.lesson.lesson_number} ص {self.page_start}"

class Exam(models.Model):
    TERM_CHOICES = (
        ('khordad', 'خرداد'),
        ('shahrivar', 'شهریور'),
        ('dey', 'دی'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='exams')
    academic_year = models.CharField(max_length=20) # e.g. 1403
    term = models.CharField(max_length=30, choices=TERM_CHOICES)
    exam_date = models.DateField(blank=True, null=True)
    total_score = models.DecimalField(max_digits=4, decimal_places=2, default=20.00)

    def __str__(self):
        return f"امتحان نهایی {self.get_term_display()} {self.academic_year} ({self.book.title})"

class ExamQuestion(models.Model):
    QUESTION_TYPES = (
        ('descriptive', 'تشریحی'),
        ('fill_in_blank', 'جای خالی'),
        ('true_false', 'صحیح / غلط'),
        ('multiple_choice', 'چهارگزینه‌ای'),
        ('verse_message', 'پیام آیه'),
        ('short_answer', 'پاسخ کوتاه'),
    )

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='exam_questions')
    question_number = models.IntegerField()
    question_text = models.TextField()
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES, default='descriptive')
    score = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    topic_tags = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"سوال {self.question_number} ({self.exam})"

class ExamAnswerKey(models.Model):
    question = models.OneToOneField(ExamQuestion, on_delete=models.CASCADE, related_name='answer_key')
    official_answer = models.TextField()
    rubric_breakdown = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"کلید تصحیح سوال {self.question.question_number}"

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, default='anonymous')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, default='گفتگوی جدید')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.id})"

class Message(models.Model):
    ROLE_CHOICES = (
        ('user', 'کاربر'),
        ('assistant', 'معلم هوشمند'),
        ('system', 'سیستم'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    intent_detected = models.CharField(max_length=50, blank=True, null=True)
    tokens_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:30]}..."

class MessageCitation(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='citations')
    chunk = models.ForeignKey(DocumentChunk, on_delete=models.CASCADE, related_name='citations')
    lesson_number = models.IntegerField()
    page_number = models.IntegerField()
    quote_snippet = models.TextField()
    relevance_score = models.FloatField(default=1.0)

    def __str__(self):
        return f"ارجاع به درس {self.lesson_number} ص {self.page_number}"
