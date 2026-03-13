# CLAUDE.MD — Spec do Pipeline Híbrido HiVQE
> Fonte de verdade viva do projeto. Atualizar antes de qualquer implementação.

## Estado Atual (2026-03-08)

| Componente | Status |
|---|---|
| `src/classical_mitigator.py` | ✅ Implementado — 12 testes passando |
| `src/quantum_engine.py` | ✅ Implementado — 13 testes passando |
| `src/orchestrator.py` | ✅ Implementado — 7 testes passando |
| `dashboard/index.html` | ❌ PENDENTE — próximo ciclo Anti-Vibe |
| `dashboard/serve.py` | ❌ PENDENTE — próximo ciclo Anti-Vibe |

### Limpeza pendente
Os seguintes artefatos de "vibe coding" precisam ser removidos manualmente:
- `dashboard/v2/` (pasta inteira)
- `dashboard/index.html` (versão vibe coding)
- `dashboard/live_vqe.py`
- `dashboard/live_data.json`
- `run_tests.py` (scratch file)
- `docs/extract_pdf.py` e `docs/extract_pdf_v2.py` (scratch files)

---

## Stack Tecnológica

| Camada | Tecnologia | Versão Mínima |
|---|---|---|
| Linguagem | Python | 3.10+ |
| Quantum SDK | Qiskit | 1.x |
| IBM Runtime | qiskit-ibm-runtime | últia estável |
| Otimizador Clássico | SciPy (minimize/COBYLA) | 1.10+ |
| Cálculos numéricos | NumPy | 1.24+ |
| Frontend | HTML5 Canvas + Vanilla JS | N/A |
| Fontes | Inter + JetBrains Mono (Google Fonts CDN) | N/A |
| Servidor local | http.server (stdlib) | N/A |

## Variáveis de Ambiente

| Variável | Descrição | Obrigatório? |
|---|---|---|
| `IBM_QUANTUM_TOKEN` | Token de acesso à IBM Quantum Platform | Somente para hardware real |

## Estrutura de Diretórios

```
hivqe-geometric-optimizer/
├── CLAUDE.MD                   ← Este arquivo
├── src/
│   ├── __init__.py
│   ├── quantum_engine.py       # Ansatz Borromeo + interface QPU/simulador
│   ├── classical_mitigator.py  # Regressão linear + convergência
│   └── orchestrator.py         # Loop híbrido principal
├── tests/
│   ├── __init__.py
│   ├── test_quantum_engine.py
│   ├── test_mitigator.py
│   └── test_orchestrator.py
├── dashboard/
│   ├── index.html              # Dashboard de telemetria (Canvas)
│   └── serve.py                # Servidor HTTP local
├── benchmarks/
│   └── run_ibm_marathon.py     # Maratona original IBM (preservada)
├── results/
│   ├── live_data.json          # Dados em tempo real (gerado pelo orchestrator)
│   └── maratona_ouroboros_ibm.png
└── docs/
```

## Responsabilidade dos Módulos

### `quantum_engine.py`
- Constrói o circuito Ansatz Ouroboros (Borromean Rings + Golden Ratio Φ).
- Interface com backend: StatevectorEstimator (simulador) ou EstimatorV2 (IBM Torino).
- Recebe vetor θ de parâmetros, retorna energia bruta (float) + metadados.
- Hamiltoniano: F_μν geometry (SparsePauliOp com termos Z e X).
- Num qubits: 6.

### `classical_mitigator.py`
- Recebe séries temporais `(epoch, energy)`.
- Mantém buffer de janela deslizante de tamanho WINDOW_SIZE=5.
- Calcula regressão linear (mínimos quadrados manuais, sem sklearn):
  - m = Σ(xᵢ−x̄)(yᵢ−ȳ) / Σ(xᵢ−x̄)²
  - b = ȳ − m·x̄
  - R² = 1 − SQR/SQT
- Retorna: energy_predicted, m, b, R², converged (bool).
- Critério de convergência: |energy_pred − target| < threshold (0.05) por patience (5) epochs consecutivos.

### `orchestrator.py`
- Loop principal: Engine → Mitigator → salva JSON → verifica convergência → repete.
- Configurações: max_epochs=60, target_energy=-5.609, convergence_threshold=0.05, patience=5.
- Output: `results/live_data.json` atualizado a cada iteração.
- Formato do JSON:
```json
{
  "status": "rodando|concluido|record",
  "config": { "target": -5.609, "backend": "simulator|ibm_torino" },
  "epochs": [1, 2, 3, ...],
  "quantum_raw": [-2.34, -3.12, ...],
  "classical_pred": [-2.34, -3.05, ...],
  "stats": { "m": -0.12, "b": -1.5, "R2": 0.87 }
}
```

### `dashboard/index.html`
- Faz polling de `live_data.json` via fetch HTTP a cada 300ms.
- Renderiza em Canvas:
  - Cruzinhas (✕) para amostras brutas da QPU (dispersão/ruído).
  - Linha contínua para predição clássica (regressão).
  - Linha tracejada dourada para target energy.
  - Resíduos (linhas verticais) entre bruto e predito.
- Painel lateral com métricas em tempo real.

## Decisões de Design

1. **Sem frameworks JS** — Vanilla JS + Canvas puro para zero dependências no frontend.
2. **Comunicação via arquivo JSON** — Simples, sem WebSocket/API. O Python escreve, o JS lê.
3. **Regressão manual** — Implementada do zero em NumPy, sem sklearn, para fins acadêmicos.
4. **Backend configurável** — Simulador local para dev/testes, IBM Torino para benchmark final.
5. **`run_ibm_marathon.py` preservado** — Código legado intacto na pasta benchmarks.
6. **Dashboards V1/V2 anteriores** — Mantidos como referência visual na pasta dashboard/v1 e dashboard/v2.

## Regras de Negócio

- A regressão linear só é calculada quando existem >= 3 pontos no buffer.
- A convergência exige patience=5 epochs abaixo do threshold, não apenas 1.
- O JSON é sobrescrito a cada epoch (não append, para simplicidade de parsing no JS).
- O frontend nunca escreve dados, apenas lê.
