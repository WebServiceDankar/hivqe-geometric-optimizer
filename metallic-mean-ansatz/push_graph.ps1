$ErrorActionPreference = "Stop"

$resultadosDir = ".\results"
if (-Not (Test-Path $resultadosDir)) {
    Write-Host "[1/4] Criando a pasta 'results'..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $resultadosDir | Out-Null
}

Write-Host "`n[2/4] Copiando o Grafico original da nossa conversa para a pasta..." -ForegroundColor Cyan
$brainDir = "C:\Users\Daniel Palma\.gemini\antigravity\brain\d356b825-8fc9-4aaf-8c62-ddde9b78d058"
$imagemAlvo = ".\results\maratona_ouroboros_ibm.png"

$imagemBaixada = Get-ChildItem -Path $brainDir -Filter "*.png" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($imagemBaixada) {
    Copy-Item -Path $imagemBaixada.FullName -Destination $imagemAlvo -Force
    Write-Host "  [OK] Grafico '$($imagemBaixada.Name)' copiado com sucesso!" -ForegroundColor Green
}
else {
    Write-Host "  [AVISO] A imagem nao foi encontrada automaticamente." -ForegroundColor Red
}

Write-Host "`n[3/4] Registrando as alteracoes (Grafico e README atualizado)..." -ForegroundColor Cyan
git add README.md results/
git commit -m "docs(results): Adiciona grafico de convergencia na IBM e atualiza README"

Write-Host "`n[4/4] Empurrando para a porta da frente do Professor..." -ForegroundColor Cyan
git push origin main

Write-Host "`n[SUCESSO] O REPOSITORIO AGORA E UMA OBRA DE ARTE COM GRAFICO OFICIAL!`n" -ForegroundColor Green
