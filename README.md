# Rotailecrew Figma Automation

Claude Code + Figma Bridge MCP ile Instagram post serisi otomasyonu.

## Genel Bakis

Claude'a icerigi ver (baslik + metin) → Figma'da kapak + hap bilgi + yonlendirme slaytlari otomatik olusturulsun.

**Post Yapisi:**
- **Kapak** — Buyuk baslik + arka plan gorseli
- **Hap Bilgi** — Aciklama metni + arka plan gorseli  
- **Yonlendirme** — Sabit CTA (Post 301 kopyasi, hic degismez)

## Gereksinimler

- [Node.js](https://nodejs.org) v18+
- [Claude Code](https://claude.ai/code) CLI
- Figma hesabi (Rotailecrew dosyasina erisim)
- Gemini API key (gorsel uretimi icin — ucretsiz tier)

## Kurulum

```powershell
git clone https://github.com/KULLANICI_ADI/rotailecrew-figma-automation.git
cd rotailecrew-figma-automation
.\setup.ps1
```

Script otomatik olarak:
- Node.js ve Claude Code kontrolu yapar
- MCP server ayarlarini yapar
- `settings.local.json` sablonu olusturur

### API Key'leri Ekle

`.claude\settings.local.json` dosyasini ac ve doldurun:

```json
{
  "env": {
    "GEMINI_API_KEY": "AIza...",
    "FIGMA_TOKEN": "figd_..."
  }
}
```

- **Gemini API Key:** [aistudio.google.com](https://aistudio.google.com) > Get API Key
- **Figma Token:** Figma > Account Settings > Personal Access Tokens

### Figma Plugin Yukle

1. Figma'yi ac
2. **Plugins > Development > Import plugin from manifest**
3. `figma-bridge-plugin\manifest.json` dosyasini sec
4. Plugini calistir → **"WebSocket Connected"** gormeli

## Kullanim

```powershell
cd rotailecrew-figma-automation
claude
```

Claude'a icerik ver:
```
1-Buffer Overflow
2-Tampon Bellek Asimi
3-Aciklama metni buraya...
```

Claude otomatik olarak:
1. Figma'da yeni post frame'lerini olusturur
2. Metinleri yerlestirir
3. Arka plan gorsellerini atar
4. Z-order'i duzenler

## Dosya Yapisi

```
rotailecrew-figma-automation/
├── .claude/
│   └── settings.json          # MCP server config (git'e girer)
├── figma-bridge-plugin/       # Figma gelistirici plugini
│   ├── manifest.json
│   └── dist/
├── generate_images.py         # Gemini ile gorsel uretici
├── settings.local.template.json
├── setup.ps1                  # Kurulum scripti
└── README.md
```

## Notlar

- `settings.local.json` git'e **girmez** (.gitignore'da)
- Figma dosyasi: `dePZYFYYLabkk3IQdfGOqH` (Rotailecrew)
- Post konumu: Post 299 referans, yeni postlar sola dogru devam eder
- figma-bridge-plugin MIT lisansi altinda ([GETHOPP LTD](https://github.com/gethopp))
