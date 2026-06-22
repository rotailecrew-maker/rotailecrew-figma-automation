# Rotailecrew Figma Otomasyon — Claude Talimatları

## Amaç
Kullanıcının verdiği içerikle Instagram post serisi (3 slayt) oluşturmak:
1. **Kapak** — İngilizce büyük başlık + arka plan görseli
2. **Hap Bilgi** — Türkçe başlık + açıklama metni + arka plan görseli
3. **Yönlendirme** — Sabit CTA, asla değişmez (önceki serinin son slaydından kopyalanır)

## Kullanıcıdan Alınacak Girdi
```
1-<İngilizce başlık>
2-<Türkçe başlık>
3-<Açıklama metni (Türkçe, kullanıcının verdiği metni aynen kullan, paraphrase etme)>
```

## Araçlar
- **figma-bridge MCP** → Figma node okuma/yazma
- **generate_images.py** → Görsel üretme (OpenAI gpt-image-1)
- **FIGMA_TOKEN** ve **OPENAI_API_KEY** env'den otomatik okunur

## Figma Dosyası
- figma-bridge bağlıyken `list_files` ile aktif fileKey'i al
- Tüm işlemlerde o fileKey'i kullan

## Mevcut Durum
- **Son seri: Post 368-370** (node ID'leri: `986:1719`, `986:1736`, `986:1777`)
- **Yeni seri: Post 371-373**
- Her seri sola doğru genişler (x azalır); yeni 371 kapak için:
  `x = 368.x − 3×1105 = -123274` (3 slot sola, 1080px + 25px boşluk)

## Node Yapısı (Post 368-370 referans)

### Kapak (post 368 — `986:1719`)
| Node | ID | İçerik |
|---|---|---|
| Background (arka plan görseli) | `986:1819` | Image fill |
| Group 228 (virgül) | `986:1721` | x=0, y=0 — bu pozisyonu koru |
| Frame 9 > Frame 10 > TEXT (İngilizce başlık) | `986:1731` | "The 3% Rule" → yeni EN başlık |

### Hap Bilgi (post 369 — `986:1736`)
| Node | ID | İçerik |
|---|---|---|
| Background (arka plan görseli) | `986:1820` | Image fill |
| Frame 228 > TEXT (Türkçe başlık) | `986:1766` | → yeni TR başlık |
| Frame 228 > TEXT (açıklama) | `986:1767` | → yeni açıklama |

### Yönlendirme (post 370 — `986:1777`)
**DEĞİŞTİRME.** Duplike et, pozisyonu ayarla, içeriğe dokunma.

## Adım Adım İş Akışı

### 1. Figma bağlantısını doğrula
```
list_files → aktif fileKey'i not al
```

### 2. Görselleri üret
`generate_images.py` dosyasındaki `COVER_PROMPT` ve `HAP_PROMPT` değişkenlerini
verilen içeriğe uygun İngilizce promptlarla güncelle, sonra çalıştır:
```powershell
python generate_images.py
```
Çıktı:
- `~/Documents/cover.png` → Kapak arka planı
- `~/Documents/hap.png` → Hap Bilgi arka planı

### 3. Son seriyi duplike et
```
duplicate_nodes(nodeIds=["986:1719", "986:1736", "986:1777"])
```
Dönen yeni node ID'lerini kaydet (yeni_kapak, yeni_hap, yeni_cta).

### 4. İsimlendirme ve konumlandırma
Her yeni frame için `set_node_properties` ile:
- `yeni_kapak`: name="Instagram post - 371", x=-123274, y=-14539
- `yeni_hap`: name="Instagram post - 372", x=-122169, y=-14539
- `yeni_cta`: name="Instagram post - 373", x=-121064, y=-14539

> Bir sonraki seride x değerleri 3×1105 daha sola kayar.

### 5. Yeni node ID'lerini bul
Duplike sonrası node ID'leri değişir. Her yeni frame için `get_node` ile ağacı gez:
- Kapak: "The 3% Rule" gibi isimli TEXT node'u bul → İngilizce başlık buraya
- Hap Bilgi: sarı başlık TEXT ve beyaz açıklama TEXT node'larını bul

### 6. Metinleri güncelle
```
set_text_content(nodeId=<yeni kapak TEXT>, characters="<İngilizce başlık>")
set_text_content(nodeId=<yeni hap TR başlık TEXT>, characters="<Türkçe başlık>")
set_text_content(nodeId=<yeni hap açıklama TEXT>, characters="<Açıklama — kullanıcının verdiği metni aynen koy>")
```

### 7. Arka plan görsellerini ata
`create_image` ile görseli frame içine ekle (parentId = yeni_kapak veya yeni_hap),
ardından z-order'ı düzelt:

**Z-order düzeltme adımları (her frame için):**
1. Frame içindeki diğer tüm child'ları (Background hariç) canvas root'a taşı (`reparent_nodes` → parentId=`0:1`)
2. Eski Background node'unu sil (`delete_nodes`)
3. `create_image` ile yeni görseli frame'e ekle (parentId=yeni_kapak, x=0, y=0, width=1080, height=1350)
4. Dışarı çıkardığın child'ları frame'e geri taşı (`reparent_nodes` → parentId=yeni_kapak)
   → Yeni image en altta, diğerleri üstte olur.

### 8. Sonucu doğrula
```
get_node(nodeId=yeni_kapak)
```
Başlık, görseller ve pozisyon doğruysa kullanıcıya tamamlandı mesajı ver.

## Görsel Prompt Yazma Kuralları
`generate_images.py` içindeki promptları güncellersen:
- **Dil**: İngilizce
- **Format**: 3:4 dikey, no text, cinematic/editorial fotoğraf stili
- **Ton**: Karanlık, dramatik, yüksek kontrast, siyah ağırlıklı
- Kapak görseli: konuyu sembolik/soyut temsil eder
- Hap Bilgi görseli: konunun pratik/finansal boyutunu gösterir

## Önemli Kurallar
- **Yönlendirme slaydına (son slayt) asla metin veya görsel yazma**
- **Açıklama metnini kullanıcının verdiği gibi aynen geçir, paraphrase etme**
- `figma-bridge` araçlarını doğrudan kullan, Figma REST API'ye gitme
- Her adımdan sonra kısa durum raporu ver
- Hata olursa açıkla ve alternatif öner
