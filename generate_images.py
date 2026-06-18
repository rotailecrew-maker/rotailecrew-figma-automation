import requests
import json
import base64
import os

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY env var eksik. .claude/settings.local.json dosyasina ekle.")

def generate_image(prompt, output_path):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "3:4"
        }
    }
    resp = requests.post(url, json=payload, timeout=90)
    if resp.status_code != 200:
        print(f"Imagen4 error {resp.status_code}: {resp.text[:300]}")
        return False
    data = resp.json()
    img_b64 = data["predictions"][0]["bytesBase64Encoded"]
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(img_b64))
    print(f"Saved: {output_path}")
    return True

def generate_image_flash(prompt, output_path):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
    }
    resp = requests.post(url, json=payload, timeout=90)
    if resp.status_code != 200:
        print(f"Flash error {resp.status_code}: {resp.text[:300]}")
        return False
    data = resp.json()
    for part in data["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(part["inlineData"]["data"]))
            print(f"Saved: {output_path}")
            return True
    print("No image in response")
    return False

COVER_PROMPT = (
    "Dark cinematic editorial photograph representing confirmation bias. "
    "A person surrounded by mirrors and echo chambers, each reflection showing the same distorted truth. "
    "Deep blacks, moody dramatic lighting, sharp contrast. "
    "Abstract data streams and filtered information. "
    "High-end magazine visual, 4:5 portrait, no text."
)

HAP_PROMPT = (
    "Dark editorial photograph showing a brain or mind selectively picking information from a sea of data. "
    "Financial charts, stock market graphs faintly visible in background. "
    "Hands or mind filtering out unwanted data, keeping only confirming evidence. "
    "Deep dark background, cinematic high-contrast lighting, moody atmosphere. "
    "4:5 portrait format, no text, magazine quality."
)

out_cover = os.path.join(os.path.expanduser("~"), "Documents", "confirmation_bias_cover.png")
out_hap = os.path.join(os.path.expanduser("~"), "Documents", "confirmation_bias_hap.png")

import time

def generate_image_fast(prompt, output_path):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={API_KEY}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": "3:4"}
    }
    resp = requests.post(url, json=payload, timeout=90)
    if resp.status_code != 200:
        print(f"Imagen4-fast error {resp.status_code}: {resp.text[:200]}")
        return False
    data = resp.json()
    img_b64 = data["predictions"][0]["bytesBase64Encoded"]
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(img_b64))
    print(f"Saved: {output_path}")
    return True

def generate_image_flash_retry(prompt, output_path, retries=3, wait=30):
    for i in range(retries):
        if i > 0:
            print(f"Waiting {wait}s before retry {i+1}...")
            time.sleep(wait)
        ok = generate_image_flash(prompt, output_path)
        if ok:
            return True
    return False

print("Generating cover image...")
ok = generate_image_fast(COVER_PROMPT, out_cover)
if not ok:
    ok = generate_image(COVER_PROMPT, out_cover)
if not ok:
    print("Falling back to Gemini Flash (with retries)...")
    generate_image_flash_retry(COVER_PROMPT, out_cover)

print("Generating hap bilgi image...")
ok = generate_image_fast(HAP_PROMPT, out_hap)
if not ok:
    ok = generate_image(HAP_PROMPT, out_hap)
if not ok:
    print("Falling back to Gemini Flash (with retries)...")
    generate_image_flash_retry(HAP_PROMPT, out_hap)

print("Done.")
