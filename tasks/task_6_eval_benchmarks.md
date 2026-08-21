# Task 6: Evaluation Benchmarks & Quality Verification Suite

## 🎯 Objective
Construct and execute an automated evaluation test suite running 50 real Grade 12 National Exam questions against the RAG system to measure Recall@5, Mean Reciprocal Rank (MRR), and Citation Grounding accuracy.

## 📁 Allowed Files
- `backend/knowledge/evaluation/benchmark_dataset.py` [NEW]
- `backend/knowledge/evaluation/evaluator.py` [NEW]
- `backend/knowledge/tests.py` [MODIFY]

## 🛠️ Implementation Rules
1. **Benchmark Questions**: 50 curated high-frequency exam questions spanning all 10 lessons of Din va Zendegi 3 (e.g., توحید افعالی, سنت ابتلا, استدراج, توبه, اخلاص, علل انحطاط تمدن اسلامی).
2. **Metrics**:
   - `Recall@5`: $\ge 90\%$ (ground-truth lesson and page present in top 5 chunks).
   - `MRR` (Mean Reciprocal Rank): $\ge 0.85$.
   - `Citation Grounding Rate`: $100\%$ valid citations.
3. **Execution**: Automated CLI test runner `python manage.py run_evaluation`.

## 📊 Deliverables
- Evaluation benchmark suite and verified test execution.
- Execution report saved to `./tasks/reports/report_task_6.md`.
