from django.test import TestCase, Client
from django.urls import reverse
from knowledge.models import (
    Grade, FieldOfStudy, Subject, Book, Lesson, BookSection,
    DocumentChunk, Exam, ExamQuestion, ExamAnswerKey
)
from knowledge.retrieval.hybrid_search import HybridSearchEngine
from knowledge.retrieval.context_builder import ContextBuilder
from knowledge.ai.pedagogy import PedagogicalPromptEngine
from knowledge.ai.providers import LLMFactory

class CurriculumRAGSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.grade = Grade.objects.create(name='دوازدهم', code=12)
        self.field = FieldOfStudy.objects.create(name='تجربی و ریاضی', slug='exp-math')
        self.subject = Subject.objects.create(name='دین و زندگی', slug='dini')
        self.book = Book.objects.create(
            grade=self.grade,
            field=self.field,
            subject=self.subject,
            title='دین و زندگی ۳',
            academic_year='1404-1405'
        )

        # Create sample lessons and chunks
        self.lesson1 = Lesson.objects.create(
            book=self.book,
            lesson_number=1,
            title='هستی‌بخش',
            page_start=8,
            page_end=17
        )
        self.section1 = BookSection.objects.create(
            lesson=self.lesson1,
            section_id='sec-l1-s1',
            section_type='verse_reflection',
            section_title='تفکر در آیات',
            page_start=10,
            page_end=11,
            content='آیه شریفه یا ایها الناس انتم الفقراء الی الله به فقر ذاتی و وجودی انسان و نیاز دائمی به خداوند اشاره دارد.'
        )
        self.chunk1 = DocumentChunk.objects.create(
            section=self.section1,
            lesson=self.lesson1,
            book=self.book,
            chunk_index=0,
            original_content=self.section1.content,
            contextual_content=f"[درس ۱] {self.section1.content}",
            page_start=10,
            page_end=11,
            token_count=25,
            embedding_vector=[0.1] * 256
        )

        self.lesson6 = Lesson.objects.create(
            book=self.book,
            lesson_number=6,
            title='سنت‌های خداوند در زندگی',
            page_start=64,
            page_end=75
        )
        self.section6 = BookSection.objects.create(
            lesson=self.lesson6,
            section_id='sec-l6-s1',
            section_type='main_text',
            section_title='سنت ابتلا',
            page_start=74,
            page_end=75,
            content='سنت ابتلا به معنای آزمایش الهی برای شکوفایی استعدادها و تمایز مومنان است.'
        )
        self.chunk6 = DocumentChunk.objects.create(
            section=self.section6,
            lesson=self.lesson6,
            book=self.book,
            chunk_index=1,
            original_content=self.section6.content,
            contextual_content=f"[درس ۶] {self.section6.content}",
            page_start=74,
            page_end=75,
            token_count=20,
            embedding_vector=[0.2] * 256
        )

    def test_curriculum_structure(self):
        """Test relational models integrity."""
        self.assertEqual(Lesson.objects.filter(book=self.book).count(), 2)
        self.assertEqual(DocumentChunk.objects.count(), 2)

    def test_hybrid_search_with_filter(self):
        """Test hybrid search with lesson metadata filter."""
        engine = HybridSearchEngine()
        results = engine.search(query='فقر ذاتی انسان به خدا', lesson_number=1, top_k=2)
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['lesson_number'], 1)

    def test_context_builder_and_citations(self):
        """Test context assembling and citation metadata."""
        engine = HybridSearchEngine()
        results = engine.search(query='سنت ابتلا و آزمایش', top_k=2)
        context = ContextBuilder.build_context_text(results)
        citations = ContextBuilder.extract_citations(results)

        self.assertIn('دین و زندگی ۳', context)
        self.assertTrue(len(citations) > 0)
        self.assertIn('lesson_number', citations[0])
        self.assertIn('page_start', citations[0])

    def test_pedagogical_prompt_assembly(self):
        """Test prompt assembling rules."""
        prompt = PedagogicalPromptEngine.assemble_prompt('سنت ابتلا چیست؟', 'متن تستی', lesson_filter=6)
        self.assertEqual(len(prompt), 2)
        self.assertEqual(prompt[0]['role'], 'system')
        self.assertIn('معلم هوشمند', prompt[0]['content'])
        self.assertIn('قوانین پاسخ‌دهی', prompt[0]['content'])

    def test_rest_api_lessons_list(self):
        """Test GET /api/curriculum/lessons/"""
        response = self.client.get('/api/curriculum/lessons/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_rest_api_chat_ask(self):
        """Test POST /api/chat/ask/"""
        response = self.client.post(
            '/api/chat/ask/',
            {'question': 'سنت ابتلا به چه معناست؟', 'lesson_number': 6},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('answer', data)
        self.assertIn('citations', data)
        self.assertIn('conversation_id', data)

    def test_rest_api_hybrid_search(self):
        """Test GET /api/search/"""
        response = self.client.get('/api/search/?q=فقر+ذاتی')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())
