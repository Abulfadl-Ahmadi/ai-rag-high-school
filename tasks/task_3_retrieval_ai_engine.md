# Task 3: Advanced Hybrid Retrieval & Pedagogical AI Engine

## 🎯 Objective
Implement the multi-tier retrieval engine (Semantic Cosine Search + Lexical FTS + RRF) and the AI Gateway with pedagogical prompting.

## 📁 Allowed Files
- `backend/knowledge/ai/providers.py` [NEW]
- `backend/knowledge/ai/pedagogy.py` [NEW]
- `backend/knowledge/ai/embeddings.py` [NEW]
- `backend/knowledge/retrieval/hybrid_search.py` [NEW]
- `backend/knowledge/retrieval/context_builder.py` [NEW]

## 🛠️ Implementation Rules
1. **Embedding Provider**: Multi-provider embedding architecture with local lightweight fallback (e.g. TF-IDF/FastEmbed/SentenceTransformers) and remote API support (DeepSeek/OpenAI/Gemini).
2. **Hybrid Search with RRF**: Combine semantic dense vector cosine search with lexical text keyword matching using Reciprocal Rank Fusion (RRF $k=60$).
3. **Curriculum Filtering**: Support metadata pre-filtering by `lesson_number`, `grade`, and `section_type`.
4. **Pedagogical System Prompt**: Assemble system prompts enforcing strict grounding, textbook terminology, Quranic verse breakdown (متن/ترجمه/پیام), verbatim citations `[درس X، صفحه Y]`, and exam tips.
5. **LLM Provider**: Abstract interface supporting DeepSeek API, Gemini API, OpenAI API, and Offline Mock for local testing.

## 📊 Deliverables
- Fully working retrieval and AI generation pipeline.
- Execution report saved to `./tasks/reports/report_task_3.md`.
