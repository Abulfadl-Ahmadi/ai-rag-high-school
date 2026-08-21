from typing import List, Dict, Any

class ContextBuilder:
    """
    Formats retrieved chunks into clean pedagogical context for LLM generation and extracts citations.
    """

    @classmethod
    def build_context_text(cls, search_results: List[Dict[str, Any]]) -> str:
        if not search_results:
            return "هیچ متنی مرتبط با این پرسش در کتاب درسی یافت نشد."

        context_blocks = []
        for idx, res in enumerate(search_results, 1):
            block = (
                f"--- [منبع {idx} | کتاب دین و زندگی ۳ | {res['lesson_title']} (درس {res['lesson_number']}) | "
                f"بخش: {res['section_title']} | صفحه: {res['page_start']}] ---\n"
                f"{res['content']}\n"
            )
            context_blocks.append(block)

        return "\n".join(context_blocks)

    @classmethod
    def extract_citations(cls, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        citations = []
        for res in search_results:
            chunk = res.get('chunk')
            citations.append({
                'chunk_id': chunk.id if chunk else None,
                'lesson_number': res['lesson_number'],
                'lesson_title': res['lesson_title'],
                'section_title': res['section_title'],
                'page_start': res['page_start'],
                'page_end': res['page_end'],
                'relevance_score': round(res.get('rrf_score', 1.0) * 100, 2),
                'snippet': res['content'][:200] + '...' if len(res['content']) > 200 else res['content']
            })
        return citations
