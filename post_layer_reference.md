# Instagram Post - 299 Layer Referansı
> Tamamlanmış Kapak (cover) slaydı örneği. Yeni Kapak postları oluştururken bu yapıya uy.

Screenshot: `Desktop/post299.png`

---

## Frame Bilgisi
- **Node ID**: 888:2
- **Ad**: Instagram post - 299
- **Boyut**: 1080 × 1350 px
- **Pozisyon (canvas)**: x=-50325, y=-15957
- **Fill**: SOLID #dbd9dd (frame fill — arka planda çok az görünür, görseller kaplar)
- **clipsContent**: true

---

## Layer Sırası (alttan üste = children[0] → children[7])

### [0] Rectangle 2 — Koyu Daire Arka Plan
| Özellik | Değer |
|---|---|
| ID | 888:4 |
| Tip | RECTANGLE |
| Pozisyon (frame içi) | x=-118, y=-361 |
| Boyut | 1711 × 1711 px |
| Fill | SOLID **#111111** (neredeyse siyah) |
| Stroke | yok |
| Opacity | 1 |
| Rotation | ~0 (float hassasiyet) |
| **Rol** | Frame'in tamamını kaplayan büyük koyu daire. Frame clips yüzünden 1080×1350'ye kırpılır. Sol/üst kısmı görünür siyah arka plan sağlar. |

---

### [1] Frame 9 — Boş Yapısal Çerçeve
| Özellik | Değer |
|---|---|
| ID | 888:9 |
| Tip | FRAME |
| Pozisyon | x=0, y=0 |
| Boyut | 1080 × 1350 px |
| Fill | YOK (şeffaf) |
| Auto Layout | YOK |
| Child | Frame 10 (888:10) — boş, auto-layout VERTICAL |
| **Rol** | Görsel içermeyen yapısal container. Görünmez. Frame 10 da boş. |

---

### [2] Arka Plan Görseli — TAM FRAME KAPLAR ← **BURAYA KOYULUR**
| Özellik | Değer |
|---|---|
| ID | 895:8 |
| Ad | Cognitive_buffer_overflow_visual…_202606180913 1 |
| Tip | RECTANGLE |
| Pozisyon | **x=0, y=0** |
| Boyut | **1080 × 1350 px** |
| Fill | IMAGE, scaleMode=**FILL** |
| imageHash | 2a7e86052361a13ffcfa6d1f8d338c3881f05a4b |
| Opacity | 1 |
| **Rol** | **ANA ARKA PLAN GÖRSELİ.** Tüm frame'i kaplar. Yeni post oluştururken bu node silinip yerine yeni görsel aynı boyut/pozisyonda konulur. |

---

### [3] Group 227 — Marka Logosu
| Özellik | Değer |
|---|---|
| ID | 888:11 |
| Tip | GROUP |
| Pozisyon | x=96, y=96 |
| Boyut | 64 × 64 px |
| **Rol** | Sol üst köşedeki Rotailecrew virgül logosu. Değiştirilmez. |

**Çocukları:**
- `Rectangle 2` (888:12): 64×64px, fill+stroke **#111111**, cornerRadius=16 → logo arka planı
- `Mask group` (888:13): 26.9×52.9px → virgül/apostrophe ikonu

---

### [4] TEXT — Ana Başlık (Kapak)
| Özellik | Değer |
|---|---|
| ID | 888:16 |
| Tip | TEXT |
| Pozisyon | x=96, y=88 |
| Boyut | 888 × 1094 px |
| Metin | "BEYNİN DOLU!" (Türkçe başlık buraya) |
| Font | **Bebas Neue Regular** |
| Boyut | **200 px** |
| Line Height | **200 px** (fixed) |
| Letter Spacing | 0% |
| Fill (renk) | **#ffffff** (beyaz) |
| Stroke | **#0022ff** (koyu mavi outline) stroke weight: 1 |
| TextAlign | LEFT |
| **Rol** | Post başlığı. Her yeni post için metin güncellenir. |

> ⚠️ Not: Post 305 şablonunda başlık İNGİLİZCE, post 299'da TÜRKÇE. Kapak postlarında hangi dilin kullanıldığını kullanıcıya sor.

---

### [5] Group 248 — "Kaydır" CTA Butonu
| Özellik | Değer |
|---|---|
| ID | 888:17 |
| Tip | GROUP |
| Pozisyon | x=737, y=1043 |
| Boyut | 395 × 64 px |
| **Rol** | Sabit "Kaydır" butonu. **Değiştirilmez.** |

**Çocukları:**
- `TEXT "Kaydır"` (888:18): x=797, y=1060, 335×26px, fill **#f4f4f4**, font Bebas Neue(?)
- `Rectangle 19` (888:19): x=737, y=1043, 241×64px, fill YOK, stroke **#f5f5f5**
- `Arrow 1` (888:20): x=1080, y=1076, 102×0px (çizgi/ok), stroke **#ffffff**

---

### [6] TEXT — Alt Yazı / Tagline
| Özellik | Değer |
|---|---|
| ID | 889:2 |
| Tip | TEXT |
| Pozisyon | x=96, y=1033 |
| Boyut | 820 × 80 px |
| Metin | "Ne anlama geldiğini gör..." |
| Font | **Architects Daughter Regular** |
| Boyut | **60 px** |
| Line Height | AUTO |
| Letter Spacing | 0% |
| Fill | **#f4f4f4** (açık beyaz/krem) |
| **Rol** | Post altındaki davet metni. Her post için güncellenir (opsiyonel). |

---

### [7] upscaled virgül — Dekoratif Virgül Overlay (EN ÜSTTE)
| Özellik | Değer |
|---|---|
| ID | 895:6 |
| Tip | RECTANGLE |
| Pozisyon | **x=540, y=-158** |
| Boyut | **949.9 × 1864 px** |
| Fill | IMAGE, scaleMode=**FILL** |
| imageHash | 72c4de127dd2ec9c62380978d78956d744df67c5 |
| Opacity | 1 |
| **Rol** | Rotailecrew marka virgülü (büyük, sağ tarafa konumlanmış). Arka plan görseli üzerine artistik overlay olarak çalışır. **Değiştirilmez.** |

---

## Kritik Kurallar

1. **Arka plan görseli her zaman index [2]'de** (Rectangle 2 ve Frame 9'un üstünde)
2. **Boyut her zaman 1080×1350, x=0, y=0** (tam frame doldurur)
3. **scaleMode = FILL**
4. **Metin node'ları (logo, başlık, alt yazı, buton) direkt frame'in child'ı** — Frame 9 içinde DEĞİL
5. **upscaled virgül her zaman en üstte** [index 7] — asla dokunulmaz
6. **Rectangle 2 her zaman en altta** [index 0] — asla dokunulur

## Yeni Post Oluştururken Yapılacaklar

1. Referans postu (en son Kapak) **duplicate** et
2. Duplicate'teki referans arka plan görselini (index [2], x=0,y=0, 1080×1350) **sil**
3. Yeni görseli `create_image` ile **aynı pozisyon/boyutta** ekle: `x=0, y=0, w=1080, h=1350, scaleMode=FILL`
4. `insertAtIndex=2` kullan (Rectangle 2 ve Frame 9'un üstüne gelsin)
5. Başlık TEXT node'unu `set_text_content` ile güncelle
6. Alt yazı TEXT node'unu güncelle (gerekiyorsa)
7. upscaled virgül'e, Group 248'e, Group 227'ye **dokunma**
