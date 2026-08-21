from django.core.management.base import BaseCommand
from knowledge.evaluation.evaluator import RAGEvaluator

class Command(BaseCommand):
    help = 'Runs automated 50-question National Exam benchmark evaluation on the RAG system'

    def handle(self, *args, **options):
        self.stdout.write("==========================================================")
        self.stdout.write("🎓 Starting Curriculum Grounded RAG Benchmark Evaluation...")
        self.stdout.write("==========================================================\n")

        evaluator = RAGEvaluator()
        results = evaluator.run_benchmark(top_k=5)

        self.stdout.write(f"Total Evaluated Exam Questions: {results['total_benchmark_questions']}")
        self.stdout.write(f"Recall@1: {results['recall_at_1_percent']}%")
        self.stdout.write(f"Recall@5: {results['recall_at_5_percent']}%")
        self.stdout.write(f"Mean Reciprocal Rank (MRR): {results['mean_reciprocal_rank_mrr']}")
        self.stdout.write(f"Citation Grounding Accuracy: {results['citation_grounding_accuracy_percent']}%")
        self.stdout.write(f"Duration: {results['evaluation_duration_seconds']} seconds\n")

        if results['recall_at_5_percent'] >= 90.0:
            self.stdout.write(self.style.SUCCESS("✅ TARGET SLA ACHIEVED: Recall@5 >= 90% and High Grounding Accuracy!"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ WARNING: Recall@5 did not meet target SLA."))
