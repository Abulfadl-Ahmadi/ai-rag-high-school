import json
import re
from pathlib import Path
from typing import Dict, List, Any
from .normalizer import PersianNormalizer

class CanonicalCurriculumParser:
    """
    Parses OCR / Text markdown into canonical structured educational JSON.
    """
    
    LESSON_METADATA = [
        {"lesson_number": 1, "title": "هستی‌بخش", "part": "بخش اول : تفکر و اندیشه", "page_start": 8, "page_end": 17},
        {"lesson_number": 2, "title": "یگانه بی‌همتا", "part": "بخش اول : تفکر و اندیشه", "page_start": 18, "page_end": 29},
        {"lesson_number": 3, "title": "توحید و سبک زندگی", "part": "بخش اول : تفکر و اندیشه", "page_start": 30, "page_end": 41},
        {"lesson_number": 4, "title": "فقط برای تو", "part": "بخش اول : تفکر و اندیشه", "page_start": 42, "page_end": 51},
        {"lesson_number": 5, "title": "قدرت پرواز", "part": "بخش اول : تفکر و اندیشه", "page_start": 52, "page_end": 63},
        {"lesson_number": 6, "title": "سنت‌های خداوند در زندگی", "part": "بخش اول : تفکر و اندیشه", "page_start": 64, "page_end": 79},
        {"lesson_number": 7, "title": "بازگشت", "part": "بخش دوم : در مسیر", "page_start": 80, "page_end": 93},
        {"lesson_number": 8, "title": "زندگی در دنیای امروز و عمل به احکام الهی", "part": "بخش دوم : در مسیر", "page_start": 94, "page_end": 107},
        {"lesson_number": 9, "title": "پایه‌های استوار", "part": "بخش دوم : در مسیر", "page_start": 108, "page_end": 125},
        {"lesson_number": 10, "title": "تمدن جدید و مسئولیت ما", "part": "بخش دوم : در مسیر", "page_start": 126, "page_end": 142}
    ]

    SECTION_PATTERNS = [
        ("verse_reflection", r"(تفکر در آیات|تدبر در قرآن|پیام آیات|آیات و روایات)"),
        ("review", r"(بررسی|بررسی و پاسخ|تطبیق)"),
        ("thought_and_research", r"(اندیشه و تحقیق|تفکر و تحقیق)"),
        ("activity", r"(فعالیت کلاسی|فعالیت داخل درس|کار کلاسی)"),
        ("suggestion", r"(پیشنهاد|مطالعه بیشتر)"),
        ("reading", r"(قرائت|استماع و قرائت)"),
        ("main_text", r"(مقدمه|متن اصلی|توضیحات)")
    ]

    def __init__(self, raw_md_path: str):
        self.raw_md_path = Path(raw_md_path)

    def parse_pages(self) -> Dict[int, str]:
        """
        Splits markdown file by page markers: ================== PAGE X ==================
        """
        with open(self.raw_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        pages = {}
        page_chunks = re.split(r'={10,}\s*PAGE\s+(\d+)\s*={10,}', content, flags=re.IGNORECASE)
        
        # page_chunks alternates: [preamble, page_num_1, content_1, page_num_2, content_2, ...]
        for i in range(1, len(page_chunks), 2):
            page_num = int(page_chunks[i])
            page_text = page_chunks[i+1].strip()
            pages[page_num] = page_text
            
        return pages

    def detect_sections_in_text(self, page_num: int, raw_text: str) -> List[Dict[str, Any]]:
        """
        Parses headings, verses, and content blocks on a single or span of pages.
        """
        clean_text = PersianNormalizer.extract_clean_content_without_ocr_captions(raw_text)
        if not clean_text:
            return []

        sections = []
        lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
        
        current_type = "main_text"
        current_title = "متن درس"
        current_lines = []

        for line in lines:
            # Check for section header trigger
            matched_header = False
            for sec_type, pattern in self.SECTION_PATTERNS:
                if re.search(pattern, line):
                    if current_lines:
                        sections.append({
                            "section_type": current_type,
                            "section_title": current_title,
                            "page_start": page_num,
                            "page_end": page_num,
                            "content": "\n".join(current_lines),
                            "verses": self.extract_verses("\n".join(current_lines))
                        })
                        current_lines = []
                    current_type = sec_type
                    current_title = line
                    matched_header = True
                    break
            
            if not matched_header:
                current_lines.append(line)

        if current_lines:
            sections.append({
                "section_type": current_type,
                "section_title": current_title,
                "page_start": page_num,
                "page_end": page_num,
                "content": "\n".join(current_lines),
                "verses": self.extract_verses("\n".join(current_lines))
            })

        return sections

    def extract_verses(self, text: str) -> List[Dict[str, str]]:
        """
        Detects Quranic verses and translations if present in block.
        """
        verses = []
        # Match Surah patterns like (سوره فاطر، آیه ۱۵) or (بقره / ۲۵۵)
        surah_matches = re.finditer(r'\((?:سوره\s+)?([^\d\(\)]+)[،/:\s]+(?:آیه\s+)?(\d+)\)', text)
        for m in surah_matches:
            surah_name = m.group(1).strip()
            ayah_num = m.group(2).strip()
            verses.append({
                "surah": surah_name,
                "ayah": int(ayah_num),
                "reference": f"سوره {surah_name}، آیه {ayah_num}"
            })
        return verses

    def build_canonical_json(self) -> Dict[str, Any]:
        pages = self.parse_pages()
        
        canonical_doc = {
            "schema_version": "1.0.0",
            "document_type": "textbook",
            "metadata": {
                "grade": 12,
                "grade_title": "دوازدهم",
                "field": "experimental_and_mathematics",
                "field_title": "رشته‌های تجربی و ریاضی",
                "subject": "دین و زندگی",
                "book_title": "دین و زندگی ۳",
                "academic_year": "1404-1405",
                "total_pages": max(pages.keys()) if pages else 142
            },
            "lessons": []
        }

        for meta in self.LESSON_METADATA:
            lesson_obj = {
                "lesson_number": meta["lesson_number"],
                "lesson_title": meta["title"],
                "part_title": meta["part"],
                "page_start": meta["page_start"],
                "page_end": meta["page_end"],
                "sections": []
            }
            
            # Aggregate pages for this lesson
            for p in range(meta["page_start"], meta["page_end"] + 1):
                if p in pages:
                    page_sections = self.detect_sections_in_text(p, pages[p])
                    for s in page_sections:
                        s["section_id"] = f"sec-dini12-l{meta['lesson_number']}-p{p}-{len(lesson_obj['sections'])+1}"
                        lesson_obj["sections"].append(s)
            
            canonical_doc["lessons"].append(lesson_obj)

        return canonical_doc

    def export_canonical_json(self, output_path: str) -> str:
        data = self.build_canonical_json()
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(out_file)
