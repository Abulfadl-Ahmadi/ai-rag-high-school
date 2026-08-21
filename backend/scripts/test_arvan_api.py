import urllib.request
import urllib.error
import json

token = 'QaeoSuj3zwNUUKAOFKFBmLR0dXk8UtZCE8IOLuLlp9vpGHc-1s1CExlR0a8izyR8yAOSjy8Lgw0oVCO7ymxlrKuPgBZgWlaga-K6oaGwaSevrGPsDr6vK6i8AX4hLpcp5AI2IfgFcN8_g7HrxW1U79-nUnswAOUCEVryGJKqfN4q5i6r42QJHTAyb5btD9gHsqSKGvNjAb3y7ilIpmggQkXf79jj9JIiIJ1gWnPkuah_Cw'
urls = [
    f'https://arvancloudai.ir/gateway/models/Bge-m3/{token}/v1/embeddings',
    'https://arvancloudai.ir/gateway/models/Bge-m3/v1/embeddings',
    'https://arvancloudai.ir/gateway/v1/embeddings',
    f'https://arvancloudai.ir/gateway/models/Bge-m3/{token}/embeddings'
]

models = ['Bge-m3-1y6v1', 'Bge-m3', 'bge-m3']

headers_list = [
    {'Content-Type': 'application/json'},
    {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'},
    {'Content-Type': 'application/json', 'Authorization': f'Apikey {token}'},
    {'Content-Type': 'application/json', 'Authorization': token},
    {'Content-Type': 'application/json', 'api-key': token},
    {'Content-Type': 'application/json', 'x-api-key': token},
    {'Content-Type': 'application/json', 'apiKey': token},
]

success = False
for u in urls:
    for m in models:
        payload = json.dumps({'model': m, 'input': 'تست سامانه'}).encode('utf-8')
        for h in headers_list:
            try:
                req = urllib.request.Request(u, data=payload, headers=h)
                resp = urllib.request.urlopen(req, timeout=8)
                res = json.loads(resp.read())
                dim = len(res['data'][0]['embedding'])
                print(f"SUCCESS! URL: {u}\nModel: {m}\nHeaders: {h}\nVector dimension: {dim}")
                success = True
                break
            except urllib.error.HTTPError as e:
                # print(f"HTTP {e.code} for {u} - {e.read().decode('utf-8', errors='ignore')}")
                pass
            except Exception as e:
                pass
        if success:
            break
    if success:
        break

if not success:
    print("Could not connect to ArvanCloud endpoint.")
