# -*- coding: utf-8 -*-
import json, requests

fk = "unsaved-mqkmjzhb-nqbseckj"

test_text = "İki Zıt Güç"  # İki Zıt Güç

payload = {
    "tool": "set_text_content",
    "nodeIds": ["941:124"],
    "params": {"text": test_text},
    "fileKey": fk
}

body = json.dumps(payload, ensure_ascii=True)
print("JSON:", body[body.find('"text"'):body.find('"text"')+50])

r = requests.post(
    "http://localhost:1994/rpc",
    headers={"Content-Type": "application/json"},
    data=body.encode("ascii"),
    timeout=15
)
result = r.json()
chars = result.get("data", {}).get("characters", "")

print("Girdi codepoints:", [hex(ord(c)) for c in test_text])
print("Cikti codepoints:", [hex(ord(c)) for c in chars])
print("Eslesen:", chars == test_text)
