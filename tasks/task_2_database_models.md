# Task 2: Database Schema & Relational Models (Curriculum, Chunks, Exams)

## 🎯 Objective
Design and implement the full relational and vector schema in Django models matching the master blueprint in `IDEA.md`.

## 📁 Allowed Files
- `backend/knowledge/models.py` [MODIFY]
- `backend/knowledge/admin.py` [MODIFY]
- `backend/knowledge/management/commands/ingest_curriculum.py` [NEW]
- `backend/knowledge/migrations/*` [NEW]

## 🛠️ Implementation Rules
1. **Curriculum Models**: `Grade`, `FieldOfStudy`, `Subject`, `Book`, `Lesson`, `BookSection`, `Verse`.
2. **Chunking & Vector Store**: `DocumentChunk` with `original_content`, `contextual_content`, `page_start`, `page_end`, `token_count`, `metadata`, `embedding_vector` (stored as binary/json array with pgvector support), and search text fields.
3. **Exam Bank Models**: `Exam`, `ExamQuestion`, `ExamAnswerKey` for 1400-1404 final exam questions.
4. **Chat & Citation Models**: `Conversation`, `Message`, `MessageCitation`.
5. **Management Command**: `python manage.py ingest_curriculum` to load `canonical_dini12.json` and generate chunk records and embeddings.

## 📊 Deliverables
- Migrated Django models with clean admin interfaces.
- Execution report saved to `./tasks/reports/report_task_2.md`.
