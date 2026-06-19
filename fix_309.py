# -*- coding: utf-8 -*-
import json, requests

fk = "unsaved-mqkseo9k-wm8q0x3r"
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
    ok = chars == text
    print(f"{'OK' if ok else 'FAIL'} | id={node_id} | {repr(chars[:50])}")
    return ok

# Başlık — Batık Maliyet Yanılgısı
baslik = "Batık Maliyet Yanılgısı"
set_text("933:35", baslik)

# Açıklama — Türkçe
aciklama = (
    "Geçmişte harcadığınız para, zaman veya emek nedeniyle "
    "kötü bir kararı sürdürmek gelecekteki kayıplarınızı büyütür. "
    "Piyasalar geçmişinizi umursamaz; yalnızca şimdi ve geleceği fiyatlar. "
    "Zararlı pozisyonu kapatmak içgüdüsel olarak yanlış hissettirse de "
    "çoğu zaman en rasyonel karardır."
)
set_text("933:36", aciklama)
