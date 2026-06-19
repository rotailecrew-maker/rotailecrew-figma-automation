# -*- coding: utf-8 -*-
import json, requests

fk = "unsaved-mqkseo9k-wm8q0x3r"
BASE = "http://localhost:1994/rpc"

payload = {"tool": "get_node", "nodeIds": ["941:125"], "fileKey": fk}
r = requests.post(BASE, headers={"Content-Type": "application/json"},
                  data=json.dumps(payload).encode("utf-8"), timeout=15)

chars = r.json()["data"]["characters"]
print("Uzunluk:", len(chars))
print("Ilk 60 char codepoints:", [hex(ord(c)) for c in chars[:30]])

# Turkce karakterleri say
turkce_chars = {0x131: 'ı', 0x130: 'İ', 0xFC: 'ü', 0xF6: 'ö',
                0x15F: 'ş', 0x11F: 'ğ', 0xE7: 'ç', 0xC7: 'Ç',
                0xD6: 'Ö', 0xDC: 'Ü', 0x15E: 'Ş', 0x11E: 'Ğ'}
found = [(hex(ord(c)), turkce_chars.get(ord(c), '?')) for c in chars if ord(c) in turkce_chars]
print("Turkce karakter sayisi:", len(found))
print("Ornekler:", found[:10])

# Beklenen metin ile karsilastir
beklenen = "Goldman Sachs, Apple ve Alibaba gibi devlerin halka arzlarını yönetti"
gelen = chars[:len(beklenen)]
print("Eslesen mi:", gelen == beklenen)
