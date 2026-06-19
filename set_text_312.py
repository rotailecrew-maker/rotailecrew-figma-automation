# -*- coding: utf-8 -*-
import json, requests

fk = "unsaved-mqkmjzhb-nqbseckj"
BASE = "http://localhost:1994/rpc"

def set_text(node_id, text):
    payload = {
        "tool": "set_text_content",
        "nodeIds": [node_id],
        "params": {"text": text},
        "fileKey": fk
    }
    body = json.dumps(payload, ensure_ascii=True).encode("ascii")
    r = requests.post(BASE, headers={"Content-Type": "application/json"}, data=body, timeout=15)
    result = r.json()
    chars = result.get("data", {}).get("characters", "")
    return chars

# Post 312 başlık - Bebas Neue, kısa tutuyoruz
baslik = "Goldman vs Lehman"
c1 = set_text("941:124", baslik)
print(f"Baslik OK: {c1 == baslik}")

# Post 312 açıklama - Crimson Text, Türkçe karakterlerle
aciklama = (
    "Goldman Sachs, Apple ve Alibaba gibi devlerin halka arzlarını yönetti; "
    "piyasaların en büyük işlemlerinde sahne arkasındaki güçtür. "
    "Lehman Brothers ise 2008'de 639 milyar dolarlık varlığıyla "
    "tarihin en büyük iflasını açıkladı. "
    "Biri Wall Street'in gücünü, diğeri onun en derin "
    "kırılganlığını temsil eder."
)
c2 = set_text("941:125", aciklama)
print(f"Aciklama OK: {c2 == aciklama}")
print(f"Ornek: {c2[:60]}")
