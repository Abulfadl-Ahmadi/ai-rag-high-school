from rest_framework import serializers
from .models import (
    Grade, Subject, Book, Lesson, BookSection, Verse,
    DocumentChunk, Exam, ExamQuestion, ExamAnswerKey,
    Conversation, Message, MessageCitation
)

class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id', 'surah', 'ayah', 'arabic_text', 'translation', 'reference']

class BookSectionSerializer(serializers.ModelSerializer):
    verses = VerseSerializer(many=True, read_only=True)

    class Meta:
        model = BookSection
        fields = ['id', 'section_id', 'section_type', 'section_title', 'page_start', 'page_end', 'content', 'verses']

class LessonSerializer(serializers.ModelSerializer):
    section_count = serializers.IntegerField(source='sections.count', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'lesson_number', 'title', 'part_title', 'page_start', 'page_end', 'summary', 'section_count']

class LessonDetailSerializer(serializers.ModelSerializer):
    sections = BookSectionSerializer(many=True, read_only=True)
    verses = VerseSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'lesson_number', 'title', 'part_title', 'page_start', 'page_end', 'summary', 'sections', 'verses']

class ExamAnswerKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAnswerKey
        fields = ['official_answer', 'rubric_breakdown']

class ExamQuestionSerializer(serializers.ModelSerializer):
    answer_key = ExamAnswerKeySerializer(read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    lesson_number = serializers.IntegerField(source='lesson.lesson_number', read_only=True)

    class Meta:
        model = ExamQuestion
        fields = ['id', 'question_number', 'question_type', 'question_text', 'score', 'topic_tags', 'lesson_number', 'lesson_title', 'answer_key']

class MessageCitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageCitation
        fields = ['id', 'lesson_number', 'page_number', 'quote_snippet', 'relevance_score']

class MessageSerializer(serializers.ModelSerializer):
    citations = MessageCitationSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'intent_detected', 'citations', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'user_id', 'lesson', 'messages', 'created_at', 'updated_at']
