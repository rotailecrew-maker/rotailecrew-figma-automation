# -*- coding: utf-8 -*-
import json, requests

fk = "unsaved-mqkseo9k-wm8q0x3r"
BASE = "http://localhost:1994/rpc"

def get_chars(node_id):
    p = {"tool": "get_node", "nodeIds": [node_id], "fileKey": fk}
    r = requests.post(BASE, headers={"Content-Type": "application/json"},
                      data=json.dumps(p).encode("utf-8"), timeout=15)
    return r.json()["data"]["characters"]

baslik = get_chars("933:35")
aciklama = get_chars("933:36")

# Türkçe karakter kontrolü
turkce = {0x131: 'ı', 0x130: 'İ', 0xFC: 'ü', 0xF6: 'ö',
          0x15F: 'ş', 0x11F: 'ğ', 0xE7: 'ç', 0x11E: 'Ğ',
          0xD6: 'Ö', 0xDC: 'Ü', 0x15E: 'Ş', 0x106: 'Ć'}

b_tr = sum(1 for c in baslik if ord(c) in turkce)
a_tr = sum(1 for c in aciklama if ord(c) in turkce)

print(f"Baslik  ({len(baslik)} char, {b_tr} Turkce): OK")
print(f"Aciklama({len(aciklama)} char, {a_tr} Turkce): OK")

# Beklenen kontrol
beklenen_baslik = "Batık Maliyet Yanılgısı"
beklenen_acik = "Geçmişte harcadığınız"
print(f"Baslik eslesen: {baslik == beklenen_baslik}")
print(f"Aciklama baslangici eslesen: {aciklama[:len(beklenen_acik)] == beklenen_acik}")
