$ErrorActionPreference = "Stop"

Write-Host "`n[1/3] Preparando a mudanca na bilheteria..." -ForegroundColor Cyan
git add README.md

Write-Host "`n[2/3] Assinando a inclusao do ABOUT..." -ForegroundColor Cyan
git commit -m "docs(intro): Adiciona secao 'Sobre o Projeto' para visitantes"

Write-Host "`n[3/3] Mandando pra nuvem..." -ForegroundColor Cyan
git push origin main

Write-Host "`n[SUCESSO] Secao ABOUT incrementada com sucesso!`n" -ForegroundColor Green
