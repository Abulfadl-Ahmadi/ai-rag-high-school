from django.contrib import admin
from .models import (
    Grade, FieldOfStudy, Subject, Book, Lesson, BookSection, Verse,
    DocumentChunk, Exam, ExamQuestion, ExamAnswerKey,
    Conversation, Message, MessageCitation
)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade', 'subject', 'academic_year')
    list_filter = ('grade', 'subject', 'academic_year')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_number', 'title', 'book', 'page_start', 'page_end')
    list_filter = ('book',)

@admin.register(BookSection)
class BookSectionAdmin(admin.ModelAdmin):
    list_display = ('section_title', 'section_type', 'lesson', 'page_start')
    list_filter = ('section_type', 'lesson')
    search_fields = ('section_title', 'content')

@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = ('surah', 'ayah', 'lesson', 'reference')
    list_filter = ('lesson', 'surah')

@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'page_start', 'page_end', 'token_count')
    list_filter = ('lesson',)
    search_fields = ('original_content', 'contextual_content')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('academic_year', 'term', 'book', 'total_score')
    list_filter = ('academic_year', 'term')

@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'exam', 'lesson', 'question_type', 'score')
    list_filter = ('question_type', 'exam', 'lesson')
    search_fields = ('question_text',)

@admin.register(ExamAnswerKey)
class ExamAnswerKeyAdmin(admin.ModelAdmin):
    list_display = ('question', 'official_answer')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user_id', 'lesson', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'role', 'intent_detected', 'created_at')

@admin.register(MessageCitation)
class MessageCitationAdmin(admin.ModelAdmin):
    list_display = ('message', 'lesson_number', 'page_number', 'relevance_score')
