Write-Host "`n[1/3] Voltando no tempo (desfazendo o commit com a senha)..." -ForegroundColor Yellow
git reset HEAD~1

Write-Host "`n[2/3] Apagando as provas do crime (removendo o script)..." -ForegroundColor Yellow
if (Test-Path "sync_github.ps1") {
    Remove-Item "sync_github.ps1" -Force
}

Write-Host "`n[3/3] Enviando apenas o nosso trabalho limpo!" -ForegroundColor Yellow
git add README.md LICENSE docs\*
git commit -m "docs: Estruturação premium do repositório (Nível Especialização UNIFEI)"
git push origin main

Write-Host "`n✨ FEITO! O guarda do GitHub deixou a gente passar agora! ✨`n" -ForegroundColor Green
