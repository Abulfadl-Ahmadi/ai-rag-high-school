import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

import math
import re
from collections import Counter
from knowledge.models import DocumentChunk
from knowledge.ingestion.normalizer import PersianNormalizer
from knowledge.evaluation.benchmark_dataset import BENCHMARK_QUESTIONS

chunks = list(DocumentChunk.objects.select_related('lesson', 'section', 'book').all())
N = len(chunks)

def tokenize(text):
    clean = PersianNormalizer.clean_text(text).lower()
    words = re.findall(r'[\w\u200c]+', clean)
    toks = list(words)
    for i in range(len(words)-1):
        toks.append(f"{words[i]}_{words[i+1]}")
    return toks

doc_tokens = {}
df = Counter()
doc_lens = {}

for c in chunks:
    rich_text = (
        f"{c.lesson.title} {c.lesson.title} "
        f"{c.section.section_title or ''} {c.section.section_title or ''} "
        f"{c.contextual_content or ''} {c.original_content}"
    )
    toks = tokenize(rich_text)
    doc_tokens[c.id] = toks
    doc_lens[c.id] = len(toks)
    for t in set(toks):
        df[t] += 1

avgdl = sum(doc_lens.values()) / max(N, 1)

def search_hybrid_bm25(query, top_k=5, k1=1.4, b=0.6):
    q_toks = tokenize(query)
    scores = []
    
    for c in chunks:
        toks = doc_tokens[c.id]
        t_counts = Counter(toks)
        dl = doc_lens[c.id]
        score = 0.0
        
        for q in q_toks:
            if len(q) < 2:
                continue
            n_q = df.get(q, 0)
            if n_q == 0:
                continue
            
            idf = math.log(1.0 + (N - n_q + 0.5) / (n_q + 0.5))
            tf = t_counts.get(q, 0)
            if tf > 0:
                tf_norm = (tf * (k1 + 1.0)) / (tf + k1 * (1.0 - b + b * (dl / avgdl)))
                score += idf * tf_norm
        
        # Exact bigram boost
        for i in range(len(q_toks)-1):
            bg = f"{q_toks[i]}_{q_toks[i+1]}"
            if bg in t_counts:
                score += 4.0
                
        scores.append((c, score))
        
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]

hits_1 = 0
hits_5 = 0
failed = []

for q in BENCHMARK_QUESTIONS:
    res = search_hybrid_bm25(q['query'], top_k=5)
    retrieved_lessons = [c.lesson.lesson_number for c, s in res]
    target = q['lesson']
    
    if retrieved_lessons and retrieved_lessons[0] == target:
        hits_1 += 1
    
    if target in retrieved_lessons:
        hits_5 += 1
    else:
        failed.append((q['id'], target, q['query'], retrieved_lessons))

print(f"Recall@1: {hits_1 / len(BENCHMARK_QUESTIONS) * 100:.1f}%")
print(f"Recall@5: {hits_5 / len(BENCHMARK_QUESTIONS) * 100:.1f}%")
print(f"Failed Count: {len(failed)}")
for fid, t, query, ret in failed:
    print(f"Q{fid} (Lesson {t}): {query} -> Retrieved: {ret}")
