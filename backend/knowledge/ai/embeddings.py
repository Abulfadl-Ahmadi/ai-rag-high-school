import os
import json
import math
import re
import hashlib
from typing import List
import urllib.request
import urllib.error
from knowledge.ingestion.normalizer import PersianNormalizer

DEFAULT_ARVAN_API_KEY = "9d1b41ed-2fc9-5fb3-b203-3fd611ad1d76"

class BaseEmbedder:
    def embed_text(self, text: str) -> List[float]:
        raise NotImplementedError

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        return float(dot)

class ArvanBGEM3Embedder(BaseEmbedder):
    """
    Client for ArvanCloud AI Gateway BGE-M3 Neural Embedding Model.
    """
    DEFAULT_ENDPOINT = "https://arvancloudai.ir/gateway/models/Bge-m3/QaeoSuj3zwNUUKAOFKFBmLR0dXk8UtZCE8IOLuLlp9vpGHc-1s1CExlR0a8izyR8yAOSjy8Lgw0oVCO7ymxlrKuPgBZgWlaga-K6oaGwaSevrGPsDr6vK6i8AX4hLpcp5AI2IfgFcN8_g7HrxW1U79-nUnswAOUCEVryGJKqfN4q5i6r42QJHTAyb5btD9gHsqSKGvNjAb3y7ilIpmggQkXf79jj9JIiIJ1gWnPkuah_Cw/v1"

    def __init__(self, endpoint_url: str = None, model: str = "Bge-m3-1y6v1", api_key: str = None):
        self.endpoint_url = (endpoint_url or os.getenv("ARVAN_GATEWAY_URL") or self.DEFAULT_ENDPOINT).rstrip('/')
        self.model = model or os.getenv("ARVAN_MODEL_NAME") or "Bge-m3-1y6v1"
        self.api_key = api_key or os.getenv("ARVAN_API_KEY") or DEFAULT_ARVAN_API_KEY

    def embed_text(self, text: str) -> List[float]:
        clean_text = PersianNormalizer.clean_text(text)
        url = f"{self.endpoint_url}/embeddings"
        payload = json.dumps({
            "model": self.model,
            "input": clean_text
        }).encode('utf-8')

        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}" if not self.api_key.startswith("Bearer ") and not self.api_key.startswith("Apikey ") else self.api_key

        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data["data"][0]["embedding"]
        except Exception as e:
            # Fallback to local embedding if API call fails
            return LightweightPersianEmbedder().embed_text(clean_text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]

class LightweightPersianEmbedder(BaseEmbedder):
    """
    Local Lightweight Persian Embedder (d=512) for instant zero-dependency vector operations.
    """
    DIMENSION = 512

    def __init__(self, dimension: int = 512):
        self.dimension = dimension

    def _tokenize(self, text: str) -> List[str]:
        cleaned = PersianNormalizer.clean_text(text).lower()
        words = re.findall(r'[\w\u200c]+', cleaned)
        tokens = list(words)
        for i in range(len(words) - 1):
            tokens.append(f"{words[i]}_{words[i+1]}")
        return tokens

    def embed_text(self, text: str) -> List[float]:
        tokens = self._tokenize(text)
        if not tokens:
            return [0.0] * self.dimension

        vector = [0.0] * self.dimension
        for token in tokens:
            h = int(hashlib.md5(token.encode('utf-8')).hexdigest(), 16)
            index = h % self.dimension
            sign = 1.0 if ((h >> 8) & 1) == 0 else -1.0
            
            weight = 1.0
            if any(k in token for k in ['توحید', 'سنت', 'توبه', 'اخلاص', 'ابتلا', 'استدراج', 'قضا', 'قدر', 'اختیار', 'تمدن', 'فقر']):
                weight = 3.0
            
            vector[index] += sign * weight

        norm = math.sqrt(sum(x * x for x in vector))
        if norm > 1e-9:
            vector = [round(x / norm, 6) for x in vector]
        return vector

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]

class EmbeddingFactory:
    @staticmethod
    def get_embedder() -> BaseEmbedder:
        return ArvanBGEM3Embedder()
