import os
import sys
import glob
import base64
import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

API_KEY = "9d1b41ed-2fc9-5fb3-b203-3fd611ad1d76"
BASE_URL = "https://arvancloudai.ir/gateway/models/Gemma-4-31B-IT/vYyTvPEve95G8FT7J2ZfKidm_ZXD-PPMAqkuf9whOLgVUAhcMo1dap6ZZ_AUfZd5dxH2eNPzKdQFWyIRKM6UiH1OFaRhNkyxK-H0BlbBCuE7591mzZuoH6r0Ib6PUoDef41d2NZinKkNBAMcVr6iP-wrJCF7nfG6As6BgWrZR_fOgpovDZKab1n7H9N2D1UhYSz97a1cubG0AEGyNVnXHu8PwYTR-afTKYNzZ5bCB7XBPY2P3njKwK9S8jQxQaIQNeI/v1"
MODEL_ID = "gemma-4-31b-it"

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def process_single_page(img_path, prompt_text, out_dir, max_retries=4):
    filename = os.path.basename(img_path)
    base_name = os.path.splitext(filename)[0]
    out_file = os.path.join(out_dir, f"{base_name}.txt")

    # Resume capability: Skip if already processed and non-empty
    if os.path.exists(out_file) and os.path.getsize(out_file) > 50:
        with open(out_file, "r", encoding="utf-8") as f:
            content = f.read()
        return (filename, True, content, 0, True)

    b64_img = encode_image(img_path)
    
    payload = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64_img}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.1,
        "max_tokens": 4096
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    start_time = time.time()
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(
                f"{BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                timeout=180
            )
            if resp.status_code == 200:
                result_json = resp.json()
                content = result_json["choices"][0]["message"]["content"]
                elapsed = time.time() - start_time

                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(content.strip())

                print(f"[Gemma-4-31B-IT] ✓ {filename} processed in {elapsed:.1f}s")
                return (filename, True, content, elapsed, False)
            elif resp.status_code == 429:
                wait_time = attempt * 5
                print(f"[Gemma-4-31B-IT] ⚠️ Rate limited on {filename}. Waiting {wait_time}s (attempt {attempt}/{max_retries})...")
                time.sleep(wait_time)
            else:
                print(f"[Gemma-4-31B-IT] ✗ Error {resp.status_code} on {filename}: {resp.text[:120]} (attempt {attempt}/{max_retries})")
                time.sleep(attempt * 2)
        except Exception as e:
            print(f"[Gemma-4-31B-IT] ✗ Exception on {filename}: {e} (attempt {attempt}/{max_retries})")
            time.sleep(attempt * 3)

    print(f"[Gemma-4-31B-IT] ❌ FAILED to process {filename} after {max_retries} attempts.")
    return (filename, False, None, 0, False)

def combine_all_pages(out_dir, combined_file):
    txt_files = sorted(glob.glob(os.path.join(out_dir, "page_*.txt")))
    combined_content = []
    
    for txt_path in txt_files:
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                combined_content.append(content)
                
    with open(combined_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(combined_content))
        
    print(f"\n=======================================================")
    print(f"🎉 Successfully combined {len(combined_content)} pages into:")
    print(f"   {combined_file}")
    print(f"=======================================================\n")

def main(workers=3):
    images_dir = r"f:\ai_rag_high_school\dataset\textbooks\dini-12_images"
    prompt_file = r"f:\ai_rag_high_school\prompts\ocr.md"
    out_dir = r"f:\ai_rag_high_school\dataset\ocr_results\gemma_4_31b_it"
    combined_file = r"f:\ai_rag_high_school\dataset\ocr_results\dini_12_gemma_complete.md"

    if not os.path.exists(images_dir):
        print(f"Error: Images directory '{images_dir}' does not exist.")
        return

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    os.makedirs(out_dir, exist_ok=True)
    all_images = sorted(glob.glob(os.path.join(images_dir, "page_*.png")))
    total_images = len(all_images)

    print(f"=======================================================")
    print(f"🚀 Starting Bulk OCR with Gemma-4-31B-IT")
    print(f"📁 Target Images: {total_images} pages ({images_dir})")
    print(f"🧵 Concurrency: {workers} workers")
    print(f"💾 Output Directory: {out_dir}")
    print(f"=======================================================\n")

    completed = 0
    skipped = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_img = {
            executor.submit(process_single_page, img, prompt_text, out_dir): img
            for img in all_images
        }

        for future in as_completed(future_to_img):
            filename, success, _, elapsed, was_cached = future.result()
            completed += 1
            if was_cached:
                skipped += 1
                print(f"[Cached] ⏩ {filename} ({completed}/{total_images} - {completed/total_images*100:.1f}%)")
            else:
                print(f"[Progress] 📊 {completed}/{total_images} ({completed/total_images*100:.1f}%)")

    # Combine all pages into one master markdown
    combine_all_pages(out_dir, combined_file)

if __name__ == "__main__":
    main(workers=3)
