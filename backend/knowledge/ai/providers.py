import os
import json
import logging
from typing import List, Dict, Any, Generator
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

DEFAULT_ARVAN_API_KEY = "9d1b41ed-2fc9-5fb3-b203-3fd611ad1d76"

class BaseLLMProvider:
    def generate(self, messages: List[Dict[str, str]]) -> str:
        raise NotImplementedError

    def stream(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        raise NotImplementedError

class OpenAICompatibleProvider(BaseLLMProvider):
    """
    Standard OpenAI-compatible Chat Completions Client with native SSE Streaming.
    """
    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model: str = "deepseek-chat"
    ):
        self.api_key = api_key or os.getenv("LLM_API_KEY") or DEFAULT_ARVAN_API_KEY
        self.base_url = (base_url or os.getenv("LLM_BASE_URL") or "https://api.openai.com/v1").rstrip('/')
        self.model = model

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            auth_val = f"Bearer {self.api_key}" if not self.api_key.startswith("Bearer ") and not self.api_key.startswith("Apikey ") else self.api_key
            headers["Authorization"] = auth_val
        return headers

    def generate(self, messages: List[Dict[str, str]]) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = self._get_headers()
        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1500,
            "stream": False
        }).encode('utf-8')

        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"LLM generate error from {self.model} at {self.base_url}: {e}")
            raise RuntimeError(f"خطا در برقراری ارتباط با مدل هوش مصنوعی ({self.model}): {str(e)}")

    def stream(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        url = f"{self.base_url}/chat/completions"
        headers = self._get_headers()
        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1500,
            "stream": True
        }).encode('utf-8')

        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                for line in resp:
                    decoded = line.decode('utf-8').strip()
                    if not decoded:
                        continue
                    if decoded.startswith("data: "):
                        raw_data = decoded[6:].strip()
                        if raw_data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(raw_data)
                            delta = chunk.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except Exception:
                            continue
        except Exception as e:
            logger.error(f"LLM stream error from {self.model} at {self.base_url}: {e}")
            raise RuntimeError(f"خطا در استریم پاسخ از مدل هوش مصنوعی ({self.model}): {str(e)}")

class DeepSeekFlashProvider(OpenAICompatibleProvider):
    """
    Client for ArvanCloud DeepSeek-V4-Flash Gateway.
    """
    DEFAULT_GATEWAY = "https://arvancloudai.ir/gateway/models/DeepSeek-V4-Flash/lO_TGTL-afcwI19pttKCo9tarYp6Q3Szl54g2vBlKbycsq8Too4Xp2RKSJfFAj_Xh9UDZyYQu3Ck8VCs4lsA_BqsN_0A3Cim2H6Bm1Wh1sBm2tApx6jYgocC1PAegzKzthABzCG9xbSysUDDrwM9leT3Dl8JJAeESwc0Z5O1iOJ6cXMxdDSS7AmuNg3MlF5gBmUHAGw3y5c-7qDlAEVSXiKnLgCwXcbiyFecc_QE2Jis07WS6SI8urArRMmRyUFhMRM623tbG5M/v1"

    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model: str = "DeepSeek-V4-Flash-lje10"
    ):
        key = api_key or os.getenv("DEEPSEEK_API_KEY") or os.getenv("ARVAN_API_KEY") or DEFAULT_ARVAN_API_KEY
        url = (base_url or os.getenv("DEEPSEEK_GATEWAY_URL") or self.DEFAULT_GATEWAY).rstrip('/')
        super().__init__(api_key=key, base_url=url, model=model)

class GemmaProvider(OpenAICompatibleProvider):
    """
    Client for ArvanCloud Gemma-4-31B-IT Gateway.
    """
    DEFAULT_GATEWAY = "https://arvancloudai.ir/gateway/models/Gemma-4-31B-IT/vYyTvPEve95G8FT7J2ZfKidm_ZXD-PPMAqkuf9whOLgVUAhcMo1dap6ZZ_AUfZd5dxH2eNPzKdQFWyIRKM6UiH1OFaRhNkyxK-H0BlbBCuE7591mzZuoH6r0Ib6PUoDef41d2NZinKkNBAMcVr6iP-wrJCF7nfG6As6BgWrZR_fOgpovDZKab1n7H9N2D1UhYSz97a1cubG0AEGyNVnXHu8PwYTR-afTKYNzZ5bCB7XBPY2P3njKwK9S8jQxQaIQNeI/v1"

    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model: str = "gemma-4-31b-it"
    ):
        key = api_key or os.getenv("GEMMA_API_KEY") or os.getenv("ARVAN_API_KEY") or DEFAULT_ARVAN_API_KEY
        url = (base_url or os.getenv("GEMMA_GATEWAY_URL") or self.DEFAULT_GATEWAY).rstrip('/')
        super().__init__(api_key=key, base_url=url, model=model)

class LLMFactory:
    @staticmethod
    def get_provider(model_name: str = None) -> BaseLLMProvider:
        if model_name:
            m = model_name.lower()
            if "gemma" in m:
                return GemmaProvider(model="gemma-4-31b-it")
            if "deepseek" in m or "flash" in m:
                return DeepSeekFlashProvider(model="DeepSeek-V4-Flash-lje10")
        return DeepSeekFlashProvider(model="DeepSeek-V4-Flash-lje10")
