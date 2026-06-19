import os
import base64
import requests

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY env var eksik. .claude/settings.local.json dosyasina ekle.")

COVER_PROMPT = (
    "Dark cinematic photograph: a massive glass skyscraper with the word LEHMAN reflected in its facade, "
    "crumbling and shattering in slow motion against a stormy Manhattan skyline at night. "
    "Broken glass, shredded financial documents and dollar bills falling through dark air. "
    "A second pristine tower stands untouched in the background, symbolizing Goldman Sachs survival. "
    "Deep dramatic chiaroscuro lighting, ominous storm clouds, cinematic atmosphere. "
    "No text. Portrait orientation. High contrast, dark editorial style."
)

HAP_PROMPT = (
    "Dark cinematic editorial photograph: a split scene — on the left, polished marble and gold "
    "inside a grand Wall Street bank vault filled with stacks of cash and gold bars, gleaming under warm light; "
    "on the right, the same vault door rusted shut with BANKRUPT stamped in red across it, surrounded by darkness. "
    "A single dramatic spotlight divides the two worlds. Deep shadows, high contrast, no text. "
    "Portrait orientation, magazine quality, moody financial atmosphere."
)

out_cover = os.path.join(os.path.expanduser("~"), "Documents", "cover.png")
out_hap   = os.path.join(os.path.expanduser("~"), "Documents", "hap.png")


def generate_image(prompt, output_path):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1536",
        "quality": "medium",
    }
    print(f"Generating: {output_path} ...")
    resp = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=payload,
        timeout=120,
    )
    if resp.status_code != 200:
        print(f"Error {resp.status_code}: {resp.text[:400]}")
        return False
    data = resp.json()
    img_b64 = data["data"][0]["b64_json"]
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(img_b64))
    print(f"Saved: {output_path}")
    return True


print("Generating cover image...")
generate_image(COVER_PROMPT, out_cover)

print("Generating hap bilgi image...")
generate_image(HAP_PROMPT, out_hap)

print("Done.")
