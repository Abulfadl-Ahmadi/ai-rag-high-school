import re
import unicodedata

class PersianNormalizer:
    """
    Normalizes Persian and Arabic text:
    - Strips all Arabic/Quranic diacritics (Harakat / Tanwin / Shadda / Sukun)
    - Unifies Alif forms (آ, أ, إ, ٱ -> ا)
    - Unifies Ya and Kaf (ي, ى -> ی / ك -> ک)
    - Unifies Ta Marbuta (ة, ۀ -> ه)
    - Cleans ZWNJ (نیم‌فاصله)
    """
    
    ARABIC_CHAR_MAP = {
        'ي': 'ی',
        'ى': 'ی',
        'ئ': 'ی',
        'ك': 'ک',
        'ة': 'ه',
        'ۀ': 'ه',
        'ؤ': 'و',
        'إ': 'ا',
        'أ': 'ا',
        'آ': 'ا',
        'ٱ': 'ا',
        'ء': '',
    }
    
    PERSIAN_NUMBERS = {'۰':'0', '۱':'1', '۲':'2', '۳':'3', '۴':'4', '۵':'5', '۶':'6', '۷':'7', '۸':'8', '۹':'9'}
    ARABIC_NUMBERS = {'٠':'0', '١':'1', '٢':'2', '٣':'3', '٤':'4', '٥':'5', '٦':'6', '٧':'7', '٨':'8', '٩':'9'}

    @classmethod
    def clean_text(cls, text: str) -> str:
        if not text:
            return ""
        
        # 1. Unicode normalization (NFKC)
        text = unicodedata.normalize('NFKC', text)
        
        # 2. Strip all Arabic diacritics / Harakat (Fatha, Damma, Kasra, Sukun, Shadda, Tanwin, etc.)
        text = re.sub(r'[\u064b-\u065f\u0670]', '', text)
        
        # 3. Strip directional marks
        text = re.sub(r'[\u200e\u200f\u202a-\u202e]', '', text)
        
        # 4. Standardize characters
        for ar, fa in cls.ARABIC_CHAR_MAP.items():
            text = text.replace(ar, fa)
            
        # 5. Normalize digits
        for p, d in cls.PERSIAN_NUMBERS.items():
            text = text.replace(p, d)
        for a, d in cls.ARABIC_NUMBERS.items():
            text = text.replace(a, d)

        # 6. Standardize ZWNJ
        text = re.sub(r'\s+می\s+', ' می‌', text)
        text = re.sub(r'\s+نمی\s+', ' نمی‌', text)
        text = re.sub(r'\s+ها\s+', '‌ها ', text)
        text = re.sub(r'\s+های\s+', '‌های ', text)
        text = re.sub(r'\s+تر\s+', '‌تر ', text)
        text = re.sub(r'\s+ترین\s+', '‌ترین ', text)
        
        # Collapse multiple spaces and newlines
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()

    @classmethod
    def extract_clean_content_without_ocr_captions(cls, text: str) -> str:
        cleaned = re.sub(r'\[fig:[^\]]+\]\s*\([^\)]*\)', '', text)
        return cls.clean_text(cleaned)
