import re
from typing import Dict, Any, List, Optional

class PedagogicalPromptEngine:
    """
    Assembles pedagogical system prompts and user prompts strictly aligned with
    Iranian High School curriculum and National Examination standards.
    """

    SYSTEM_PROMPT_DINI_12 = """شما دبیر و مدرس ارشد و رسمی کتاب «دین و زندگی ۳» (پایه دوازدهم) هستید.
وظیفه شما پاسخ‌گویی جامع، مفهومی، دقیق و آموزشی به دانش‌آموز بر اساس محتوای کتاب درسی و کلید تصحیح امتحانات نهایی است.

ضوابط پاسخ‌دهی:
۱. در پاسخ به درخواست آموزش یا خلاصه درس، سرفصل‌ها، مفاهیم اصلی، پیام آیات و نکات نهایی را به صورت دسته‌بندی‌شده و کامل ارائه دهید.
۲. در پاسخ به سوالات مفهومی و اصطلاحات، مفهوم دقیق کتاب درسی را تحلیل کرده و ارجاع صفحه را در انتهای متن ذکر کنید.
۳. در مواجهه با سلام و احوال‌پرسی، محترمانه و صمیمی پاسخ داده و دانش‌آموز را برای پرسش درباره دروس دوازدهم راهنمایی کنید.
"""

    GREETING_PATTERNS = [
        r'^\s*(سلام|سالم|درود|سلام\s*علیکم|وقت\s*بخیر|خسته\s*نباشید|سلام\s*خوبی|hi|hello)\s*[!.,؟?]*\s*$'
    ]

    @classmethod
    def is_simple_greeting(cls, text: str) -> bool:
        cleaned = text.strip().lower()
        if cleaned in ["سلام", "سالم", "درود", "سلام وقت بخیر", "سلام خوبی", "سلام خسته نباشید", "hi", "hello"]:
            return True
        for pattern in cls.GREETING_PATTERNS:
            if re.match(pattern, cleaned):
                return True
        return False

    @classmethod
    def get_greeting_response(cls) -> str:
        return (
            "سلام و درود بر شما دانش‌آموز گرامی! وقت شما بخیر 🌸\n\n"
            "من دستیار تخصصی و دبیر هوشمند **دین و زندگی ۳ (پایه دوازدهم)** هستم.\n"
            "می‌توانید هر سوال، مفهوم، پیام آیه یا آموزش کاملی از **۱۰ درس کتاب** و نکات امتحانات نهایی را مطرح کنید تا با ارجاع دقیق به متن کتاب درسی شما را راهنمایی کنم."
        )

    @classmethod
    def assemble_prompt(cls, user_question: str, context_text: str = "", lesson_filter: Optional[int] = None) -> List[Dict[str, str]]:
        context_str = context_text.strip() if context_text else "هیچ متنی مرتبط با این پرسش در کتاب درسی یافت نشد."
        system_text = f"{cls.SYSTEM_PROMPT_DINI_12}\n\nمحتوای معتبر بازیابی‌شده از کتاب درسی:\n{context_str}"
        
        user_text = f"پرسش دانش‌آموز:\n{user_question}"
        if lesson_filter:
            user_text += f"\n(تمرکز درس: درس {lesson_filter})"

        return [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text}
        ]
