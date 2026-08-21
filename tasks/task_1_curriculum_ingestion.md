# Task 1: Curriculum Ingestion & Canonical Knowledge Extraction

## 🎯 Objective
Extract and transform the complete 12th Grade Religious Studies (دین و زندگی ۳) curriculum from the dataset (`dataset/ocr_results/dini_12_gemma_complete.md` and `dataset/textbooks/dini-12.pdf`) into structured, canonical JSON knowledge (`dataset/canonical_dini12.json`).

## 📁 Allowed Files
- `backend/knowledge/ingestion/canonical_parser.py` [NEW]
- `backend/knowledge/ingestion/normalizer.py` [NEW]
- `backend/knowledge/ingestion/pipeline.py` [MODIFY]
- `dataset/canonical_dini12.json` [NEW]

## 🛠️ Implementation Rules
1. **Hierarchy Preservation**: Capture Book -> 10 Lessons -> Sections (تفکر در آیات, بررسی, اندیشه و تحقیق, متن اصلی, فعالیت کلاسی) -> Verses (Arabic, translation, surah/ayah) -> Page numbers.
2. **Persian Text Normalization**: Normalize Arabic characters (`ی`, `ک`), ZWNJ (نیم‌فاصله), and clean OCR artifacts.
3. **Exact Page Mapping**: Every section and chunk must have accurate `page_start` and `page_end` for verbatim citations.
4. **Validation**: Validate that all 10 lessons from page 1 to 142 are fully parsed without data loss.

## 📊 Deliverables
- `dataset/canonical_dini12.json` containing complete structured data.
- Execution report saved to `./tasks/reports/report_task_1.md`.
