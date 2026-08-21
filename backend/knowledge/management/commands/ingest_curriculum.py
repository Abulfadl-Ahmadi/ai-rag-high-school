import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from knowledge.models import (
    Grade, FieldOfStudy, Subject, Book, Lesson, BookSection, Verse,
    DocumentChunk, Exam, ExamQuestion, ExamAnswerKey
)
from knowledge.ai.embeddings import LightweightPersianEmbedder

class Command(BaseCommand):
    help = 'Ingests canonical curriculum JSON into relational & vector database'

    def add_arguments(self, parser):
        parser.add_argument('--json-path', type=str, default='dataset/canonical_dini12.json', help='Path to canonical JSON file')

    def handle(self, *args, **options):
        json_path = Path(options.get('json_path', 'dataset/canonical_dini12.json'))
        if not json_path.exists():
            self.stderr.write(f"Error: File {json_path} does not exist.")
            return

        self.stdout.write(f"Loading canonical curriculum from {json_path}...")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        embedder = LightweightPersianEmbedder()

        with transaction.atomic():
            # 1. Base Curriculum Entities
            grade, _ = Grade.objects.get_or_create(code=12, defaults={'name': 'دوازدهم'})
            field, _ = FieldOfStudy.objects.get_or_create(slug='experimental-and-math', defaults={'name': 'علوم تجربی و ریاضی و فیزیک'})
            subject, _ = Subject.objects.get_or_create(slug='dini', defaults={'name': 'دین و زندگی'})
            
            book, _ = Book.objects.get_or_create(
                grade=grade,
                field=field,
                subject=subject,
                title='دین و زندگی ۳',
                defaults={
                    'academic_year': '1404-1405',
                    'source_pdf_path': 'dataset/textbooks/dini-12.pdf'
                }
            )

            # Clear old records for clean re-ingestion
            Lesson.objects.filter(book=book).delete()
            Exam.objects.filter(book=book).delete()

            total_chunks = 0
            total_sections = 0
            total_verses = 0

            # 2. Ingest Lessons, Sections, Verses, Chunks
            for l_data in data.get('lessons', []):
                lesson = Lesson.objects.create(
                    book=book,
                    lesson_number=l_data['lesson_number'],
                    title=l_data['lesson_title'],
                    part_title=l_data.get('part_title', ''),
                    page_start=l_data['page_start'],
                    page_end=l_data['page_end']
                )

                for s_data in l_data.get('sections', []):
                    total_sections += 1
                    section = BookSection.objects.create(
                        lesson=lesson,
                        section_id=s_data.get('section_id', ''),
                        section_type=s_data.get('section_type', 'main_text'),
                        section_title=s_data.get('section_title', ''),
                        page_start=s_data.get('page_start', lesson.page_start),
                        page_end=s_data.get('page_end', lesson.page_end),
                        content=s_data.get('content', '')
                    )

                    # Ingest Verses
                    for v_data in s_data.get('verses', []):
                        total_verses += 1
                        Verse.objects.create(
                            section=section,
                            lesson=lesson,
                            surah=v_data.get('surah', ''),
                            ayah=v_data.get('ayah', 1),
                            reference=v_data.get('reference', '')
                        )

                    # Create Chunks
                    raw_content = section.content.strip()
                    if raw_content:
                        # Anthropic Contextual Retrieval Enrichment Header
                        context_header = f"[کتاب: {book.title} | {lesson.title} (درس {lesson.lesson_number}) | بخش: {section.section_title} | صفحه: {section.page_start}]"
                        contextual_content = f"{context_header}\n{raw_content}"
                        
                        # Generate dense vector embedding
                        vector = embedder.embed_text(contextual_content)
                        
                        DocumentChunk.objects.create(
                            section=section,
                            lesson=lesson,
                            book=book,
                            chunk_index=total_chunks,
                            original_content=raw_content,
                            contextual_content=contextual_content,
                            page_start=section.page_start,
                            page_end=section.page_end,
                            token_count=len(raw_content.split()),
                            metadata={
                                'lesson_number': lesson.lesson_number,
                                'section_type': section.section_type,
                                'section_title': section.section_title,
                                'page_start': section.page_start
                            },
                            embedding_vector=vector
                        )
                        total_chunks += 1

            # 3. Populate Sample National Exam Bank (1400-1403)
            exam_1403, _ = Exam.objects.get_or_create(
                book=book,
                academic_year='1403',
                term='khordad',
                defaults={'total_score': 20.00}
            )

            # Sample high-yield final exam questions
            exam_q1 = ExamQuestion.objects.create(
                exam=exam_1403,
                lesson=Lesson.objects.get(book=book, lesson_number=6),
                question_number=4,
                question_type='descriptive',
                question_text='سنت ابتلا را تعریف کنید و دو مورد از اهداف این سنت الهی را طبق متن کتاب درسی بنویسید.',
                score=1.5,
                topic_tags=['سنتهای الهی', 'ابتلا', 'امتحان نهایی ۱۴۰۳']
            )
            ExamAnswerKey.objects.create(
                question=exam_q1,
                official_answer='سنت ابتلا به معنای قرار دادن انسان در تنگناها و سختی‌ها و شرایط مختلف برای شکوفا شدن استعدادهای درونی و تمایز درجات ایمان است. (۱.۵ نمره)',
                rubric_breakdown=[
                    {'part': 'تعریف سنت ابتلا', 'score': 0.5},
                    {'part': 'شکوفایی استعدادها', 'score': 0.5},
                    {'part': 'تمایز مومنان از غیرمومنان', 'score': 0.5}
                ]
            )

            exam_q2 = ExamQuestion.objects.create(
                exam=exam_1403,
                lesson=Lesson.objects.get(book=book, lesson_number=7),
                question_number=8,
                question_type='verse_message',
                question_text='آیه شریفه «يَا أَيُّهَا الَّذِينَ آمَنُوا تُوبُوا إِلَى اللَّهِ تَوْبَةً نَصُوحًا» به کدام مرحله از توبه اشاره دارد و توبه نصوح به چه معناست؟',
                score=1.0,
                topic_tags=['توبه', 'توبه نصوح', 'پیام آیات']
            )
            ExamAnswerKey.objects.create(
                question=exam_q2,
                official_answer='توبه نصوح به معنای بازگشت خالصانه و قاطع و بدون بازگشت به سوی خداوند است. (۱ نمره)',
                rubric_breakdown=[{'part': 'مفهوم توبه نصوح', 'score': 1.0}]
            )

        self.stdout.write(self.style.SUCCESS(
            f"Successfully ingested curriculum:\n"
            f"- 1 Book: {book.title}\n"
            f"- 10 Lessons\n"
            f"- {total_sections} Sections\n"
            f"- {total_verses} Verses\n"
            f"- {total_chunks} Vector Document Chunks\n"
            f"- Exam Questions & Answer Keys loaded"
        ))
