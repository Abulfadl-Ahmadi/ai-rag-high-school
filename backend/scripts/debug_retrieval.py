import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from knowledge.evaluation.evaluator import RAGEvaluator

evaluator = RAGEvaluator()
results = evaluator.run_benchmark(top_k=5)

print(f"Total: {results['total_benchmark_questions']}, Hits@5: {results['recall_at_5_percent']}%")
print("\nFailed Queries:")
for r in results['detailed_results']:
    if not r['hit_5']:
        print(f"[Q{r['id']}] Target: Lesson {r['target_lesson']} | Query: {r['query']}")
        print(f"       Retrieved: {r['retrieved_lessons']}")
