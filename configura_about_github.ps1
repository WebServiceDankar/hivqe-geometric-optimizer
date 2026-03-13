$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "    ATUALIZANDO A VITRINE LATERAL (ABOUT) DO GITHUB" -ForegroundColor Cyan
Write-Host "=========================================================`n" -ForegroundColor Cyan

# Usando o token que você me passou
$token = "SEU_TOKEN_AQUI"
$repo = "WebServiceDankar/hivqe-geometric-optimizer"

$headers = @{
    "Authorization" = "token $token"
    "Accept"        = "application/vnd.github.v3+json"
}

# 1. Atualizando a Descrição Principal
$bodyRepo = @{
    description = "Pesquisa: Otimizacao Topologica de VQE via Razao Aurea e Aneis de Borromeo (UNIFEI - Ciencia de Dados Aplicada)"
} | ConvertTo-Json

Write-Host "`n[1/2] Injetando a descricao oficial do repositorio..." -ForegroundColor Cyan
try {
    Invoke-RestMethod -Uri "https://api.github.com/repos/$repo" `
        -Method Patch `
        -Headers $headers `
        -Body $bodyRepo `
        -ContentType "application/json" | Out-Null
    Write-Host "  [OK] Descricao atualizada com sucesso!" -ForegroundColor Green
}
catch {
    Write-Host "  [ERRO] Falha ao atualizar a descricao. (Talvez o GitHub tenha revogado a chave por seguranca)." -ForegroundColor Red
}

# 2. Injetando as Etiquetas (Topics)
$bodyTopics = @{
    names = @("quantum-computing", "vqe", "qiskit", "cuda-q", "unifei", "data-science", "golden-ratio", "borromean-rings")
} | ConvertTo-Json

Write-Host "`n[2/2] Colocando as Etiquetas (Badges) de tecnologia..." -ForegroundColor Cyan
try {
    Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/topics" `
        -Method Put `
        -Headers $headers `
        -Body $bodyTopics `
        -ContentType "application/json" | Out-Null
    Write-Host "  [OK] Tags/Topicos adicionados!" -ForegroundColor Green
}
catch {
    Write-Host "  [ERRO] Falha ao atualizar as Tags." -ForegroundColor Red
}

Write-Host "`n[SUCESSO] O ABOUT DO SEU GITHUB AGORA ESTA PROFISSIONAL E COMPLETO!`n" -ForegroundColor Green
