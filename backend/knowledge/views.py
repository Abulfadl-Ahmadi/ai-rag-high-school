import json
import re
from typing import Optional
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from knowledge.models import Lesson, DocumentChunk, ExamQuestion, Conversation, Message, MessageCitation
from knowledge.serializers import LessonSerializer as LessonListSerializer, LessonDetailSerializer, ExamQuestionSerializer
from knowledge.retrieval.hybrid_search import HybridSearchEngine
from knowledge.retrieval.context_builder import ContextBuilder
from knowledge.ai.pedagogy import PedagogicalPromptEngine
from knowledge.ai.providers import LLMFactory

def extract_lesson_from_query(text: str) -> Optional[int]:
    persian_numbers = {
        '1': 1, '۱': 1, 'اول': 1, 'یک': 1,
        '2': 2, '۲': 2, 'دوم': 2, 'دو': 2,
        '3': 3, '۳': 3, 'سوم': 3, 'سه': 3,
        '4': 4, '۴': 4, 'چهارم': 4, 'چهار': 4,
        '5': 5, '۵': 5, 'پنجم': 5, 'پنج': 5,
        '6': 6, '۶': 6, 'ششم': 6, 'شش': 6,
        '7': 7, '۷': 7, 'هفتم': 7, 'هفت': 7,
        '8': 8, '۸': 8, 'هشتم': 8, 'هشت': 8,
        '9': 9, '۹': 9, 'نهم': 9, 'نه': 9,
        '10': 10, '۱۰': 10, 'دهم': 10, 'ده': 10,
    }
    match = re.search(r'درس\s*([0-9\u06F0-\u06F9]+|[^\s\d]+)', text)
    if match:
        word = match.group(1).strip()
        return persian_numbers.get(word)
    return None

def index_view(request):
    return render(request, 'knowledge/index.html')

class LessonListView(APIView):
    def get(self, request):
        lessons = Lesson.objects.all().order_by('lesson_number')
        serializer = LessonListSerializer(lessons, many=True)
        return Response(serializer.data)

class LessonDetailView(APIView):
    def get(self, request, pk):
        try:
            lesson = Lesson.objects.prefetch_related('sections', 'verses').get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({'error': 'درس مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LessonDetailSerializer(lesson)
        return Response(serializer.data)

class SearchChunksView(APIView):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        lesson_num = request.GET.get('lesson')
        section_type = request.GET.get('type')
        top_k = int(request.GET.get('top_k', 5))

        if not query:
            return Response({'error': 'عبارت جستجو نمی‌تواند خالی باشد.'}, status=status.HTTP_400_BAD_REQUEST)

        lesson_int = int(lesson_num) if lesson_num and lesson_num.isdigit() else None

        engine = HybridSearchEngine()
        results = engine.search(
            query=query,
            lesson_number=lesson_int,
            section_type=section_type,
            top_k=top_k
        )
        return Response(results)

class AskQuestionView(APIView):
    def post(self, request):
        question = request.data.get('question') or request.data.get('message')
        if question:
            question = question.strip()
        lesson_num = request.data.get('lesson_number')
        conversation_id = request.data.get('conversation_id')

        if not question:
            return Response({'error': 'متن سوال الزامی است.'}, status=status.HTTP_400_BAD_REQUEST)

        lesson_int = int(lesson_num) if lesson_num else extract_lesson_from_query(question)

        # 1. Manage Conversation
        if conversation_id:
            try:
                conv = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                conv = Conversation.objects.create(title=question[:40])
        else:
            conv = Conversation.objects.create(title=question[:40])

        if lesson_int and not conv.lesson:
            try:
                conv.lesson = Lesson.objects.get(lesson_number=lesson_int)
                conv.save()
            except Lesson.DoesNotExist:
                pass

        # Save User Message
        user_msg = Message.objects.create(
            conversation=conv,
            role='user',
            content=question
        )

        # 2. Hybrid Search
        engine = HybridSearchEngine()
        search_results = engine.search(
            query=question,
            lesson_number=lesson_int,
            top_k=4
        )

        context_text = ContextBuilder.build_context_text(search_results) if search_results else ""
        citations = ContextBuilder.extract_citations(search_results) if search_results else []

        # If question is lesson-specific and no citations, attach default lesson citation
        if lesson_int and not citations:
            lesson_obj = Lesson.objects.filter(lesson_number=lesson_int).first()
            if lesson_obj:
                citations = [{
                    'lesson_number': lesson_obj.lesson_number,
                    'lesson_title': lesson_obj.title,
                    'page_start': lesson_obj.page_start,
                    'page_end': lesson_obj.page_end,
                    'snippet': f"کتاب درسی دین و زندگی ۳ (درس {lesson_obj.lesson_number}: {lesson_obj.title}، صفحات {lesson_obj.page_start} تا {lesson_obj.page_end})",
                    'relevance_score': 100
                }]

        # 3. Prompt Assembly & LLM Generation
        prompt_messages = PedagogicalPromptEngine.assemble_prompt(
            user_question=question,
            context_text=context_text,
            lesson_filter=lesson_int
        )
        model_name = request.data.get('model') or request.data.get('model_name')
        provider = LLMFactory.get_provider(model_name)
        answer = provider.generate(prompt_messages)

        # Save Assistant Message & Citations
        assistant_msg = Message.objects.create(
            conversation=conv,
            role='assistant',
            content=answer
        )

        for cit in citations:
            chunk_id = cit.get('chunk_id')
            if chunk_id:
                try:
                    chunk = DocumentChunk.objects.get(id=chunk_id)
                    MessageCitation.objects.create(
                        message=assistant_msg,
                        chunk=chunk,
                        lesson_number=cit.get('lesson_number') or chunk.lesson.lesson_number,
                        page_number=cit.get('page_start') or chunk.page_start,
                        quote_snippet=cit.get('snippet') or chunk.original_content[:200],
                        relevance_score=cit.get('rrf_score') or cit.get('relevance_score', 1.0)
                    )
                except DocumentChunk.DoesNotExist:
                    pass

        return Response({
            'conversation_id': str(conv.id),
            'question': question,
            'answer': answer,
            'citations': citations
        })

class StreamAskQuestionView(APIView):
    def get(self, request):
        question = request.GET.get('q', '').strip()
        lesson_num = request.GET.get('lesson')
        if not question:
            return Response({'error': 'متن سوال الزامی است.'}, status=status.HTTP_400_BAD_REQUEST)

        lesson_int = int(lesson_num) if lesson_num and lesson_num.isdigit() else extract_lesson_from_query(question)

        # 1. Retrieval
        engine = HybridSearchEngine()
        search_results = engine.search(
            query=question,
            lesson_number=lesson_int,
            top_k=4
        )

        context_text = ContextBuilder.build_context_text(search_results) if search_results else ""
        citations = ContextBuilder.extract_citations(search_results) if search_results else []

        prompt_messages = PedagogicalPromptEngine.assemble_prompt(
            user_question=question,
            context_text=context_text,
            lesson_filter=lesson_int
        )

        model_name = request.GET.get('model') or request.GET.get('model_name')
        provider = LLMFactory.get_provider(model_name)

        def event_stream():
            metadata_payload = {
                'citations': citations,
                'primary_lesson': citations[0]['lesson_number'] if citations else lesson_int,
                'primary_page': citations[0]['page_start'] if citations else 8,
            }
            yield f"event: metadata\ndata: {json.dumps(metadata_payload, ensure_ascii=False)}\n\n"

            for chunk in provider.stream(prompt_messages):
                yield f"event: delta\ndata: {json.dumps({'text': chunk}, ensure_ascii=False)}\n\n"

            yield "event: done\ndata: [DONE]\n\n"

        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

class ExamQuestionListView(APIView):
    def get(self, request):
        lesson_num = request.GET.get('lesson')
        q_type = request.GET.get('type')
        questions = ExamQuestion.objects.all().select_related('exam', 'lesson')

        if lesson_num and lesson_num.isdigit():
            questions = questions.filter(lesson__lesson_number=int(lesson_num))

        if q_type:
            questions = questions.filter(question_type=q_type)

# Backward-compatible view aliases for URL routing
HybridSearchView = SearchChunksView
ChatAskView = AskQuestionView
ChatStreamView = StreamAskQuestionView
ExamQuestionsListView = ExamQuestionListView
