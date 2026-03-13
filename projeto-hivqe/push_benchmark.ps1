Write-Host "`n[1/3] Adicionando o Benchmark na área de stage..." -ForegroundColor Cyan
git add benchmarks/run_ibm_marathon.py

Write-Host "`n[2/3] Registrando o código na história do repositório..." -ForegroundColor Cyan
git commit -m "feat(benchmarks): Adiciona Maratona VQE (50 Iterações) na IBM com Token Seguro"

Write-Host "`n[3/3] Sincronizando com a Nuvem VIP..." -ForegroundColor Cyan
git push origin main

Write-Host "`n🚀 BENCHMARK PROTEGIDO E NO AR! 🚀`n" -ForegroundColor Green
