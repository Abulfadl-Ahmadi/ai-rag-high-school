import urllib.request
import urllib.error
import json

base_url = "https://arvancloudai.ir/gateway/models/Bge-m3/QaeoSuj3zwNUUKAOFKFBmLR0dXk8UtZCE8IOLuLlp9vpGHc-1s1CExlR0a8izyR8yAOSjy8Lgw0oVCO7ymxlrKuPgBZgWlaga-K6oaGwaSevrGPsDr6vK6i8AX4hLpcp5AI2IfgFcN8_g7HrxW1U79-nUnswAOUCEVryGJKqfN4q5i6r42QJHTAyb5btD9gHsqSKGvNjAb3y7ilIpmggQkXf79jj9JIiIJ1gWnPkuah_Cw/v1"

endpoints = [
    f"{base_url}/embeddings",
    f"{base_url}/models",
    f"{base_url}/chat/completions",
    "https://arvancloudai.ir/gateway/models/Bge-m3/v1/embeddings"
]

for ep in endpoints:
    print(f"\n--- Testing Endpoint: {ep} ---")
    
    # 1. Test GET
    try:
        req = urllib.request.Request(ep)
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"GET Success {resp.status}: {resp.read().decode('utf-8')[:300]}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        print(f"GET HTTPError {e.code}: {body[:300]}")
    except Exception as e:
        print(f"GET Exception: {e}")

    # 2. Test POST
    payload = json.dumps({"model": "Bge-m3-1y6v1", "input": ["تست"]}).encode('utf-8')
    try:
        req = urllib.request.Request(ep, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"POST Success {resp.status}: {resp.read().decode('utf-8')[:300]}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        print(f"POST HTTPError {e.code}: {body[:300]}")
    except Exception as e:
        print(f"POST Exception: {e}")
