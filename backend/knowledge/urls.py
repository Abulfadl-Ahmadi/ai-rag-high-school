from django.urls import path
from .views import (
    LessonListView, LessonDetailView, HybridSearchView,
    ChatAskView, ChatStreamView, ExamQuestionsListView
)

urlpatterns = [
    # Curriculum
    path('curriculum/lessons/', LessonListView.as_view(), name='lesson-list'),
    path('curriculum/lessons/<int:lesson_number>/', LessonDetailView.as_view(), name='lesson-detail'),
    
    # Search
    path('search/', HybridSearchView.as_view(), name='hybrid-search'),
    
    # Chat & Streaming
    path('chat/ask/', ChatAskView.as_view(), name='chat-ask'),
    path('chat/stream/', ChatStreamView.as_view(), name='chat-stream'),
    
    # Exam Bank
    path('exams/questions/', ExamQuestionsListView.as_view(), name='exam-questions'),
]
