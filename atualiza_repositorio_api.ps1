$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "    ATUALIZANDO NOME E ABOUT DO REPOSITORIO GITHUB" -ForegroundColor Cyan
Write-Host "=========================================================`n" -ForegroundColor Cyan

# ATENÇÃO: O GitHub bloqueou e removeu o token antigo por segurança após ele vazar no commit anterior.
# Você precisará gerar um novo Personal Access Token no GitHub para rodar este script!
$token = "SEU_NOVO_TOKEN_AQUI"
$repoAtual = "WebServiceDankar/hivqe-geometric-optimizer"

$headers = @{
    "Authorization" = "token $token"
    "Accept"        = "application/vnd.github.v3+json"
}

# 1. Definindo o Nome do Repositório e a Descrição Principal
# O usuário optou por manter a tradição do nome e a descrição com foco no VQE e Razão Áurea!
$novoNome = "hivqe-geometric-optimizer"
$novaDescricao = "Pesquisa: Otimizacao Topologica de VQE via Razao Aurea e Aneis de Borromeo (UNIFEI - Ciencia de Dados Aplicada)"

$bodyRepo = @{
    name = $novoNome
    description = $novaDescricao
} | ConvertTo-Json

Write-Host "`n[1/2] Enviando o novo nome ($novoNome) e a descricao abrangente..." -ForegroundColor Cyan
try {
    Invoke-RestMethod -Uri "https://api.github.com/repos/$repoAtual" `
        -Method Patch `
        -Headers $headers `
        -Body $bodyRepo `
        -ContentType "application/json" | Out-Null
    Write-Host "  [OK] Repositorio renomeado e descricao atualizada com sucesso no GitHub!" -ForegroundColor Green
}
catch {
    Write-Host "  [ERRO] Falha ao atualizar. Seu token de acesso pode ser invalido ou nao ter permissao de 'repo'." -ForegroundColor Red
    exit
}

# 2. Atualizando a URL origin do Git no seu computador local para apontar pro nome novo
Write-Host "`n[2/2] Sincronizando o Git local para a nova URL..." -ForegroundColor Cyan
try {
    git remote set-url origin "https://github.com/WebServiceDankar/$novoNome.git"
    Write-Host "  [OK] Origin do git local apontado para a URL nova: https://github.com/WebServiceDankar/$novoNome.git" -ForegroundColor Green
}
catch {
    Write-Host "  [ERRO] Falha ao atualizar o URL local remoto." -ForegroundColor Red
}

Write-Host "`n[SUCESSO] O SEU GITHUB AGORA ABRAÇA O CÓDIGO INTEIRO COMO UM VERDADEIRO MONOREPO!`n" -ForegroundColor Green
