# Task 4: REST API & Server-Sent Events (SSE) Streaming Endpoints

## 🎯 Objective
Build Django REST Framework endpoints and real-time streaming handlers for conversations, curriculum navigation, hybrid search, and exam intelligence.

## 📁 Allowed Files
- `backend/knowledge/views.py` [MODIFY]
- `backend/knowledge/urls.py` [NEW]
- `backend/backend/urls.py` [MODIFY]
- `backend/knowledge/serializers.py` [NEW]

## 🛠️ Implementation Rules
1. **Curriculum Endpoints**:
   - `GET /api/curriculum/lessons/`: List lessons with metadata and page spans.
   - `GET /api/curriculum/lessons/<int:lesson_number>/`: Retrieve lesson sections and verses.
2. **Chat & Streaming Endpoints**:
   - `POST /api/chat/ask/`: Synchronous JSON response with answer, sources, and citations.
   - `POST /api/chat/stream/`: Server-Sent Events (SSE) stream emitting `metadata` (citations/lesson/page) followed by token `delta`s and `done`.
3. **Search & Exam Endpoints**:
   - `GET /api/search/`: Direct hybrid search query returning ranked chunks and scores.
   - `GET /api/exams/questions/`: Filterable list of final exam questions with official answer keys.

## 📊 Deliverables
- Fully functional REST and SSE API endpoints.
- Execution report saved to `./tasks/reports/report_task_4.md`.
