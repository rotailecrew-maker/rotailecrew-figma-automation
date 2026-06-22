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
3-<Açıklama metni (Türkçe, 2-4 cümle)>
```

## Araçlar
- **figma-bridge MCP** → Figma node okuma/yazma
- **generate_images.py** → Görsel üretme (OpenAI gpt-image-1)
- **FIGMA_TOKEN** ve **OPENAI_API_KEY** env'den otomatik okunur

## Figma Dosyası
- File key: `dePZYFYYLabkk3IQdfGOqH` (Rotailecrew)
- figma-bridge bağlıyken `list_files` ile aktif fileKey'i al
- Tüm işlemlerde o fileKey'i kullan

## Mevcut Durum
- **Son seri: Post 305-307** (node ID'leri: `919:174`, `919:194`, `919:218`)
- **Yeni seri: Post 308-310**
- Her seri sola doğru genişler (x azalır); yeni 308 kapak için:
  `x = 305.x − 1105` (1080px genişlik + 25px boşluk)

## Node Yapısı (Post 305-307 referans)

### Kapak (post 305 — `919:174`)
| Node | ID | İçerik |
|---|---|---|
| Background (arka plan görseli) | `919:260` | Image fill |
| Frame 10 > TEXT (İngilizce başlık) | `919:189` | "Cost of Waiting" → yeni EN başlık |

### Hap Bilgi (post 306 — `919:194`)
| Node | ID | İçerik |
|---|---|---|
| Background (arka plan görseli) | `919:261` | Image fill |
| Frame 228 > TEXT (Türkçe başlık) | `919:207` | "Beklemenin Maliyeti" → yeni TR başlık |
| Frame 228 > TEXT (açıklama) | `919:208` | uzun açıklama metni → yeni açıklama |

### Yönlendirme (post 307 — `919:218`)
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
duplicate_nodes(nodeIds=["919:174","919:194","919:218"])
```
Dönen yeni node ID'lerini kaydet (yeni_kapak, yeni_hap, yeni_cta).

### 4. İsimlendirme ve konumlandırma
Her yeni frame için `set_node_properties` ile:
- `yeni_kapak`: name="Instagram post - 308", x=<305.x − 1105>, y=<305.y>
- `yeni_hap`: name="Instagram post - 309", x=<308.x + 1105>, y=<305.y>
- `yeni_cta`: name="Instagram post - 310", x=<309.x + 1105>, y=<305.y>

### 5. Metinleri güncelle
```
set_text_content(nodeId=<yeni Kapak içindeki başlık TEXT node'u>, characters="<İngilizce başlık>")
set_text_content(nodeId=<yeni Hap içindeki TR başlık TEXT node'u>, characters="<Türkçe başlık>")
set_text_content(nodeId=<yeni Hap içindeki açıklama TEXT node'u>, characters="<Açıklama>")
```

> Yeni node ID'lerini bulmak için: `get_node(nodeId=yeni_kapak)` ile ağacı gez,
> "Cost of Waiting" ve "Beklemenin Maliyeti" gibi isimli TEXT node'larını bul.

### 6. Arka plan görsellerini ata
`create_image` aracıyla görselleri yükle ve ilgili Background rectangle'a ata:
- Kapak Background (`919:260` → yeni karşılığı): `~/Documents/cover.png`
- Hap Bilgi Background (`919:261` → yeni karşılığı): `~/Documents/hap.png`

### 7. Sonucu doğrula
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
- `figma-bridge` araçlarını doğrudan kullan, Figma REST API'ye gitme
- Her adımdan sonra kısa durum raporu ver
- Hata olursa açıkla ve alternatif öner
