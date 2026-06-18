# Rotailecrew Figma Automation - Kurulum Scripti

Write-Host "=== Rotailecrew Figma Automation Kurulumu ===" -ForegroundColor Cyan

# 1. Node.js kontrolu
Write-Host "`n[1/4] Node.js kontrol ediliyor..." -ForegroundColor Yellow
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "HATA: Node.js bulunamadi. https://nodejs.org adresinden yukleyin." -ForegroundColor Red
    exit 1
}
Write-Host "Node.js OK: $(node --version)" -ForegroundColor Green

# 2. Claude Code kontrolu
Write-Host "`n[2/4] Claude Code kontrol ediliyor..." -ForegroundColor Yellow
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Write-Host "Claude Code bulunamadi, yukleniyor..." -ForegroundColor Yellow
    npm install -g @anthropic-ai/claude-code
} else {
    Write-Host "Claude Code OK: $(claude --version)" -ForegroundColor Green
}

# 3. settings.local.json olustur
Write-Host "`n[3/4] API key ayarlari..." -ForegroundColor Yellow
$localSettings = ".claude\settings.local.json"
if (-not (Test-Path $localSettings)) {
    Copy-Item "settings.local.template.json" $localSettings
    Write-Host "settings.local.json olusturuldu. Icine API key'lerini gir:" -ForegroundColor Yellow
    Write-Host "  Dosya: $((Resolve-Path $localSettings).Path)" -ForegroundColor White
} else {
    Write-Host "settings.local.json zaten var." -ForegroundColor Green
}

# 4. Figma plugin talimat
Write-Host "`n[4/4] Figma Plugin Kurulumu (Manuel):" -ForegroundColor Yellow
$pluginPath = (Resolve-Path "figma-bridge-plugin\manifest.json").Path
Write-Host "  1. Figma'yi ac" -ForegroundColor White
Write-Host "  2. Plugins > Development > Import plugin from manifest" -ForegroundColor White
Write-Host "  3. Su dosyayi sec: $pluginPath" -ForegroundColor Cyan
Write-Host "  4. Plugini calistir, WebSocket Connected gormelisin" -ForegroundColor White

Write-Host "`n=== Kurulum Tamamlandi ===" -ForegroundColor Cyan
Write-Host "Kullanim: Bu klasorde 'claude' komutunu calistir." -ForegroundColor Green
