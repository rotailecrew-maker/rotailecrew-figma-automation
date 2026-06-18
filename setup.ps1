# Rotailecrew Figma Automation - Kurulum Scripti

Write-Host "=== Rotailecrew Figma Automation Kurulumu ===" -ForegroundColor Cyan
Write-Host ""

# -------------------------------------------------------
# 1. Node.js kontrolu
# -------------------------------------------------------
Write-Host "[1/6] Node.js kontrol ediliyor..." -ForegroundColor Yellow
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "  HATA: Node.js bulunamadi." -ForegroundColor Red
    Write-Host "  Cozum: https://nodejs.org adresinden v18+ yukle, sonra bu scripti tekrar calistir." -ForegroundColor Red
    exit 1
}
Write-Host "  OK: $(node --version)" -ForegroundColor Green

# -------------------------------------------------------
# 2. Claude Code kontrolu
# -------------------------------------------------------
Write-Host "[2/6] Claude Code kontrol ediliyor..." -ForegroundColor Yellow
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Write-Host "  Claude Code bulunamadi, yukleniyor..." -ForegroundColor Yellow
    npm install -g @anthropic-ai/claude-code
    if (-not $?) {
        Write-Host "  HATA: Claude Code yuklenemedi. npm calistigindan emin ol." -ForegroundColor Red
        exit 1
    }
}
Write-Host "  OK: $(claude --version)" -ForegroundColor Green

# -------------------------------------------------------
# 3. settings.local.json kontrolu
# -------------------------------------------------------
Write-Host "[3/6] API key ayarlari kontrol ediliyor..." -ForegroundColor Yellow
$localSettings = ".claude\settings.local.json"

if (-not (Test-Path $localSettings)) {
    Copy-Item "settings.local.template.json" $localSettings
    Write-Host "  settings.local.json olusturuldu." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  YAPILACAK: Asagidaki dosyayi ac ve API keylerini doldur:" -ForegroundColor Red
    Write-Host "  $((Resolve-Path $localSettings).Path)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  GEMINI_API_KEY : https://aistudio.google.com -> Get API Key" -ForegroundColor White
    Write-Host "  FIGMA_TOKEN    : Figma -> Account Settings -> Personal Access Tokens" -ForegroundColor White
    Write-Host ""
    Write-Host "  Doldurduktan sonra bu scripti tekrar calistir." -ForegroundColor Yellow
    exit 0
}

# Placeholder degerler hala duruyorsa uyar
$settingsContent = Get-Content $localSettings -Raw
$geminiMissing = $settingsContent -match "BURAYA_API_KEY_YAZ"
$figmaMissing  = $settingsContent -match "BURAYA_FIGMA_TOKEN_YAZI"

if ($geminiMissing -or $figmaMissing) {
    Write-Host "  HATA: API keyleri henuz doldurulmamis:" -ForegroundColor Red
    if ($geminiMissing) { Write-Host "    - GEMINI_API_KEY eksik  -> https://aistudio.google.com -> Get API Key" -ForegroundColor Red }
    if ($figmaMissing)  { Write-Host "    - FIGMA_TOKEN eksik     -> Figma -> Account Settings -> Personal Access Tokens" -ForegroundColor Red }
    Write-Host "  Dosyayi ac ve doldur: $((Resolve-Path $localSettings).Path)" -ForegroundColor Cyan
    exit 1
}
Write-Host "  OK: GEMINI_API_KEY ve FIGMA_TOKEN mevcut." -ForegroundColor Green

# -------------------------------------------------------
# 4. Figma plugin talimat
# -------------------------------------------------------
Write-Host "[4/6] Figma Plugin..." -ForegroundColor Yellow
$pluginPath = Join-Path (Get-Location) "figma-bridge-plugin\manifest.json"
Write-Host "  Figma'da plugin kurulu degil mi? Adimlar:" -ForegroundColor White
Write-Host "    1. Figma'yi ac" -ForegroundColor White
Write-Host "    2. Plugins > Development > Import plugin from manifest" -ForegroundColor White
Write-Host "    3. Su dosyayi sec:" -ForegroundColor White
Write-Host "       $pluginPath" -ForegroundColor Cyan
Write-Host "  (Daha once kurduysan bu adimi atla)" -ForegroundColor DarkGray

# -------------------------------------------------------
# 5. Bridge sunucusu - port 1994 kontrolu ve baslat
# -------------------------------------------------------
Write-Host "[5/6] Figma MCP Bridge sunucusu kontrol ediliyor..." -ForegroundColor Yellow

$port1994 = netstat -ano | Select-String "0.0.0.0:1994.*LISTENING"
if ($port1994) {
    Write-Host "  OK: Bridge sunucusu zaten port 1994'te calisiyor." -ForegroundColor Green
} else {
    Write-Host "  Bridge sunucusu baslatiliyor (arka planda)..." -ForegroundColor Yellow
    Start-Process -FilePath "npx" -ArgumentList "@gethopp/figma-mcp-bridge@0.0.15" -WindowStyle Normal
    Write-Host "  Yeni bir terminal penceresi acildi. 5 saniye bekleniyor..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5

    $port1994 = netstat -ano | Select-String "0.0.0.0:1994.*LISTENING"
    if ($port1994) {
        Write-Host "  OK: Bridge sunucusu baslatildi, port 1994 aktif." -ForegroundColor Green
    } else {
        Write-Host "  UYARI: Port 1994 henuz aktif degil. Birkas saniye bekle ve Figma pluginini ac." -ForegroundColor Yellow
        Write-Host "  Elle baslatmak icin yeni bir terminalde su komutu calistir:" -ForegroundColor White
        Write-Host "    npx @gethopp/figma-mcp-bridge@0.0.15" -ForegroundColor Cyan
        Write-Host "  Bu terminali KAPAMA - bridge sunucusu burada calisiyor olmali." -ForegroundColor Red
    }
}

# -------------------------------------------------------
# 6. Ozet ve baslangic talimat
# -------------------------------------------------------
Write-Host ""
Write-Host "[6/6] Kurulum tamamlandi!" -ForegroundColor Green
Write-Host ""
Write-Host "=== KULLANIM ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Her bilgisayarda ilk baslatmada yapilacaklar:" -ForegroundColor White
Write-Host "  1. Figma'yi ac, plugin'i calistir (Plugins > Development > Figma MCP Bridge > Run)" -ForegroundColor White
Write-Host "     -> 'WebSocket Connected' gormeli" -ForegroundColor Green
Write-Host "     -> 'Disconnected' goruyorsan: yeni terminalde 'npx @gethopp/figma-mcp-bridge@0.0.15' calistir" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Bu klasorde Claude Code'u baslat:" -ForegroundColor White
Write-Host "     claude" -ForegroundColor Cyan
Write-Host ""
Write-Host "  3. Claude'a icerik ver:" -ForegroundColor White
Write-Host "     1-Post Basligi (Ingilizce)" -ForegroundColor DarkGray
Write-Host "     2-Post Basligi (Turkce)" -ForegroundColor DarkGray
Write-Host "     3-Aciklama metni" -ForegroundColor DarkGray
Write-Host ""
Write-Host "=== SORUN GIDERME ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Plugin 'Disconnected' gosteriyorsa:" -ForegroundColor White
Write-Host "  -> Yeni bir terminal ac" -ForegroundColor White
Write-Host "  -> Calistir: npx @gethopp/figma-mcp-bridge@0.0.15" -ForegroundColor Cyan
Write-Host "  -> O terminali KAPAMA, bridge orada calisiyor" -ForegroundColor Red
Write-Host "  -> Figma'da plugini kapat ve tekrar ac" -ForegroundColor White
Write-Host ""
Write-Host "Port 1994 kontrolu (sorun varsa calistir):" -ForegroundColor White
Write-Host "  netstat -ano | Select-String ':1994'" -ForegroundColor Cyan
Write-Host "  -> 'LISTENING' gorulmeli. Gorunmuyorsa bridge baslatilmamis demektir." -ForegroundColor White
Write-Host ""
Write-Host "API key hatasi aliyorsan:" -ForegroundColor White
Write-Host "  -> .claude\settings.local.json dosyasini kontrol et" -ForegroundColor Cyan
Write-Host "  -> GEMINI_API_KEY ve FIGMA_TOKEN dolu olmali" -ForegroundColor White
Write-Host ""
