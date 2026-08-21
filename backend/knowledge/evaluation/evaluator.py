import time
from typing import Dict, Any, List
from knowledge.retrieval.hybrid_search import HybridSearchEngine
from knowledge.retrieval.context_builder import ContextBuilder
from knowledge.ai.pedagogy import PedagogicalPromptEngine
from knowledge.ai.providers import LLMFactory
from .benchmark_dataset import BENCHMARK_QUESTIONS

class RAGEvaluator:
    """
    Automated Benchmark Evaluator for Curriculum RAG Engine.
    Evaluates Recall@1, Recall@5, MRR (Mean Reciprocal Rank), and Grounding Citation Accuracy.
    """

    def __init__(self):
        self.search_engine = HybridSearchEngine()
        self.llm_provider = LLMFactory.get_provider()

    def run_benchmark(self, top_k: int = 5) -> Dict[str, Any]:
        total_questions = len(BENCHMARK_QUESTIONS)
        hits_at_1 = 0
        hits_at_5 = 0
        reciprocal_ranks = []
        citation_valid_count = 0

        start_time = time.time()
        detailed_results = []

        for item in BENCHMARK_QUESTIONS:
            q_id = item["id"]
            query = item["query"]
            target_lesson = item["lesson"]
            target_keywords = item["keywords"]

            # 1. Execute Retrieval
            results = self.search_engine.search(query=query, top_k=top_k)
            retrieved_lessons = [r["lesson_number"] for r in results]

            # Check Hit@1
            hit_1 = False
            if retrieved_lessons and retrieved_lessons[0] == target_lesson:
                hits_at_1 += 1
                hit_1 = True

            # Check Hit@5 and compute Reciprocal Rank
            hit_5 = False
            rr = 0.0
            for rank, r_lesson in enumerate(retrieved_lessons, 1):
                if r_lesson == target_lesson:
                    hit_5 = True
                    rr = 1.0 / rank
                    break

            if hit_5:
                hits_at_5 += 1
            reciprocal_ranks.append(rr)

            # 2. Test Generation & Citation
            context_text = ContextBuilder.build_context_text(results)
            citations = ContextBuilder.extract_citations(results)
            prompt = PedagogicalPromptEngine.assemble_prompt(query, context_text, lesson_filter=target_lesson)
            answer = self.llm_provider.generate(prompt)

            # Validate citation
            if citations and any(c['lesson_number'] == target_lesson for c in citations):
                citation_valid_count += 1

            detailed_results.append({
                "id": q_id,
                "query": query,
                "target_lesson": target_lesson,
                "retrieved_lessons": retrieved_lessons,
                "hit_1": hit_1,
                "hit_5": hit_5,
                "rr": rr,
                "citations_count": len(citations),
                "primary_citation": citations[0] if citations else None
            })

        duration = time.time() - start_time
        recall_at_1 = (hits_at_1 / total_questions) * 100
        recall_at_5 = (hits_at_5 / total_questions) * 100
        mrr = sum(reciprocal_ranks) / total_questions
        citation_accuracy = (citation_valid_count / total_questions) * 100

        summary = {
            "total_benchmark_questions": total_questions,
            "recall_at_1_percent": round(recall_at_1, 2),
            "recall_at_5_percent": round(recall_at_5, 2),
            "mean_reciprocal_rank_mrr": round(mrr, 4),
            "citation_grounding_accuracy_percent": round(citation_accuracy, 2),
            "evaluation_duration_seconds": round(duration, 2),
            "detailed_results": detailed_results
        }
        return summary
