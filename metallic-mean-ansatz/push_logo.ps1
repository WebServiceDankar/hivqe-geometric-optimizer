$ErrorActionPreference = "Stop"

$docsDir = ".\docs"
if (-Not (Test-Path $docsDir)) {
    Write-Host "[1/4] Criando a pasta 'docs'..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $docsDir | Out-Null
}

Write-Host "`n[2/4] Buscando a nova e impecavel Logo do seu envio..." -ForegroundColor Cyan
$brainDir = "C:\Users\Daniel Palma\.gemini\antigravity\brain\d356b825-8fc9-4aaf-8c62-ddde9b78d058"
$imagemAlvo = ".\docs\logo_projeto.png"

# Pega o arquivo de imagem mais recente recebido da pasta (a Logo enviada agora)
$imagemBaixada = Get-ChildItem -Path $brainDir -Filter "*.png" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($imagemBaixada) {
    Copy-Item -Path $imagemBaixada.FullName -Destination $imagemAlvo -Force
    Write-Host "  [OK] Imagem '$($imagemBaixada.Name)' transformada em Logo Oficial!" -ForegroundColor Green
}
else {
    Write-Host "  [AVISO] A imagem nao foi encontrada automaticamente." -ForegroundColor Red
}

Write-Host "`n[3/4] Assinando o documento com as modificacoes..." -ForegroundColor Cyan
git add README.md docs/
git commit -m "docs(ui): Adiciona logotipo oficial premium Unifei CDA e atualiza capa"

Write-Host "`n[4/4] Subindo para o holofote do GitHub VIP..." -ForegroundColor Cyan
git push origin main

Write-Host "`n[SUCESSO] ESSA LOGO FICOU ABSURDA DE LINDA! REPOSITORIO ATUALIZADO!`n" -ForegroundColor Green
