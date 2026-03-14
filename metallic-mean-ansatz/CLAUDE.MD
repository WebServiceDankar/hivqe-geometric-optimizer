# CLAUDE.MD — Spec do Project M²QA (Metallic Mean Quantum Ansatz)
> Fonte de verdade viva do projeto. Atualizar antes de qualquer implementação.
> **Metodologia:** Akita Way (Anti-Vibe Coding) — TDD obrigatório, Design First.

## Estado Atual (2026-03-13)

| Componente | Status |
|---|---|
| `src/classical_mitigator.py` | ✅ Implementado — 12 testes passando |
| `src/quantum_engine.py` | ✅ Implementado — 13 testes passando |
| `src/orchestrator.py` | ✅ Implementado — 7 testes passando |
| `packages/connectome-core/graph_parser.py` | ❌ PENDENTE — Teste Red escrito (`test_graph_parser.py`) |
| `apps/brain-simulator/snn_engine.py` | ❌ PENDENTE — Pseudocódigo TDD pronto (Doc 07) |
| `apps/virtual-environment/stimulus_api.py` | ❌ PENDENTE — Spec definida (Doc 06) |
| `dashboard/index.html` | ❌ PENDENTE — próximo ciclo |
| `dashboard/serve.py` | ❌ PENDENTE — próximo ciclo |

### Documentação do Plano Diretor

| Doc | Título | Status |
|---|---|---|
| 01 | Whitepaper Ansatz (Matemática Topológica) | ✅ Publicado |
| 02 | Data Dictionary / Connectome Mapping | ✅ Publicado |
| 03 | TDD Test Suite Matrix (Físico-Computacional) | ✅ Publicado |
| 04 | Digital Ethics & Governance (Cibernética) | ✅ Publicado |
| 05 | Hardware Benchmarking (CUDA-Q vs CPU) | ✅ Publicado |
| 06 | Biological Dataset Spec (Schemas OSN/LN/PN) | ✅ Publicado |
| 07 | TDD Strategy (Pseudocódigo pytest completo) | ✅ Publicado |
| 08 | Simulation Pipeline (Diagrama de Blocos E2E) | ✅ Publicado |

### Limpeza pendente
Os seguintes artefatos de sessões anteriores precisam ser removidos manualmente:
- `dashboard/v2/` (pasta inteira)
- `dashboard/index.html` (versão legada)
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
| IBM Runtime | qiskit-ibm-runtime | última estável |
| GPU Quantum | NVIDIA CUDA-Q | última estável |
| Otimizador Clássico | SciPy (minimize/COBYLA) | 1.10+ |
| Cálculos numéricos | NumPy | 1.24+ |
| Grafos | NetworkX | 3.x |
| SNN Engine | Brian2 ou NEST Simulator | 2.x |
| API Interna | FastAPI | 0.100+ |
| Contratos de Dados | Pydantic | 2.x |
| Testes | pytest | 7.x+ |
| Tipagem Estática | mypy | 1.x |
| Frontend | HTML5 Canvas + Vanilla JS | N/A |
| Fontes | Inter + JetBrains Mono (Google Fonts CDN) | N/A |
| Servidor local | http.server (stdlib) | N/A |

## Variáveis de Ambiente

| Variável | Descrição | Obrigatório? |
|---|---|---|
| `IBM_QUANTUM_TOKEN` | Token de acesso à IBM Quantum Platform | Somente para hardware real |
| `NEUROMORPHO_API_KEY` | Chave para baixar os datasets abertos | Somente para download de conectomas |
| `SIMULATION_RESOLUTION_MS` | Resolução do tempo da SNN (default: 0.1ms) | Não |
| `ENVIRONMENT_API_URL` | URL da API do ambiente virtual (default: http://localhost:8000) | Não |

## Estrutura de Diretórios

```
metallic-mean-ansatz/
├── CLAUDE.MD                           ← Este arquivo (Spec Viva)
├── README.md                           ← Apresentação M²QA + Tabela Experimental
├── src/
│   ├── __init__.py
│   ├── quantum_engine.py               # Ansatz Borromeo + interface QPU/simulador
│   ├── classical_mitigator.py          # Regressão linear + convergência
│   └── orchestrator.py                 # Loop híbrido principal VQE
├── tests/
│   ├── __init__.py
│   ├── test_quantum_engine.py
│   ├── test_mitigator.py
│   ├── test_orchestrator.py
│   └── test_dashboard.py
├── packages/
│   ├── connectome-core/
│   │   ├── graph_parser.py             # PENDENTE: Conversão JSON → Adjacency Matrix
│   │   └── tests/
│   │       └── test_graph_parser.py    # ✅ Teste Red escrito
│   └── shared-types/                   # Contratos de dados Pydantic (PENDENTE)
├── apps/
│   ├── brain-simulator/                # SNN Engine (Brian2/NEST) — PENDENTE
│   ├── virtual-environment/            # API FastAPI de estímulos — PENDENTE
│   └── data-dashboard/                 # Frontend Streamlit — PENDENTE
├── dashboard/
│   ├── index.html                      # Dashboard de telemetria VQE (Canvas)
│   └── serve.py                        # Servidor HTTP local
├── benchmarks/
│   └── run_ibm_marathon.py             # Maratona original IBM (preservada)
├── results/
│   ├── live_data.json                  # Dados em tempo real (orchestrator)
│   └── maratona_ouroboros_ibm.png
├── docs/
│   ├── 01_whitepaper_ansatz.md
│   ├── 02_data_dictionary_connectome.md
│   ├── 03_tdd_test_suite_matrix.md
│   ├── 04_digital_ethics_governance.md
│   ├── 05_hardware_benchmarking.md
│   ├── 06_biological_dataset_spec.md
│   ├── 07_tdd_strategy_pseudocode.md
│   ├── 08_simulation_pipeline.md
│   └── logo_projeto.png
├── docker-compose.yml
└── requirements-dev.txt
```

## Responsabilidade dos Módulos

### `quantum_engine.py`
- Constrói o circuito Ansatz Borromeano (Borromean Rings + Silver Ratio δ_S).
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

### `packages/connectome-core/graph_parser.py` (PENDENTE)
- Responsável EXCLUSIVO por baixar dados de conectoma (NeuroMorpho/FlyWire).
- Limpar os grafos e converter em Matrizes de Adjacência (Sparse CSR).
- Validar schemas de nós (OSN, LN, PN) e arestas (weight, latency_ms).

### `apps/brain-simulator/` (PENDENTE)
- Consome o `connectome-core`.
- Roda o motor LIF (Leaky Integrate-and-Fire) via Brian2.
- Recebe tensores de estímulos (CO2, Ácido Lático) + energia inibitória do VQE.
- Retorna contagem de spikes nos Projection Neurons.

### `apps/virtual-environment/` (PENDENTE)
- Motor de estímulos simplificado (FastAPI).
- Envia matrizes de concentração de CO₂ para o simulador via API REST.

## Decisões de Design

1. **Sem frameworks JS** — Vanilla JS + Canvas puro para zero dependências no frontend.
2. **Comunicação via arquivo JSON** — Simples, sem WebSocket/API. O Python escreve, o JS lê.
3. **Regressão manual** — Implementada do zero em NumPy, sem sklearn, para fins acadêmicos.
4. **Backend configurável** — Simulador local para dev/testes, IBM Torino para benchmark final.
5. **Topologia Borromeana** — GHZ três-partido como base do Ansatz (proteção contra decoerência local).
6. **Médias Metálicas** — Ângulos inicializados via série de Pell (Silver Ratio δ_S), nunca aleatórios.
7. **TDD como Método Científico** — Red = Hipótese, Green = Experimento confirmado, Refactor = Revisão por pares.

## Regras de Negócio

- A regressão linear só é calculada quando existem >= 3 pontos no buffer.
- A convergência exige patience=5 epochs abaixo do threshold, não apenas 1.
- O JSON é sobrescrito a cada epoch (não append, para simplicidade de parsing no JS).
- O frontend nunca escreve dados, apenas lê.
- Nenhum código de produção é escrito sem teste (Fase 2 Akita Way).
- Documentação (`CLAUDE.MD`) é atualizada **antes** de implementação (Fase 1 Akita Way).
