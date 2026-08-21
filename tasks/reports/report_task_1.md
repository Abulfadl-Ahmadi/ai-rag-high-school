# Task 1 Execution Report: Curriculum Ingestion & Canonical Parsing

## 📌 Summary
Successfully extracted and structured the complete 12th Grade Religious Studies (دین و زندگی ۳) curriculum from raw OCR markdown into a standardized, canonical JSON format.

## 📁 Files Created & Modified
- `backend/knowledge/ingestion/normalizer.py` [NEW]: Persian unicode normalization, ZWNJ alignment, Arabic char mapping (`ی/ک`), and OCR figure filter.
- `backend/knowledge/ingestion/canonical_parser.py` [NEW]: Multi-page parser with section categorization (`تفکر در آیات`, `بررسی`, `اندیشه و تحقیق`, `فعالیت کلاسی`, `متن اصلی`), verse extraction, and page mapping.
- `dataset/canonical_dini12.json` [NEW]: Versioned canonical schema with 10 lessons and 156 granular sections.

## 📊 Ingestion Statistics
- **Total Lessons**: 10
- **Total Sections Extracted**: 156
- **Page Coverage**: Pages 8 to 142 (100% textbook coverage)
- **Verse & Activity Mapping**: Integrated
