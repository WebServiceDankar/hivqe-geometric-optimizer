# ⚡ Documento 8: Pipeline de Simulação (Diagrama de Blocos)

> **Arquitetura End-to-End:** Como a Matriz Matemática do Whitepaper (Doc 01) interage computacionalmente com o Grafo Biológico (Doc 06).

---

## 1. Visão Geral do Fluxo

O pipeline M²QA opera em **3 estágios sequenciais**, cada um validado por TDD antes de alimentar o próximo:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PIPELINE M²QA (End-to-End)                       │
│                                                                     │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────────┐  │
│  │   ESTÁGIO 1  │───▶│    ESTÁGIO 2     │───▶│    ESTÁGIO 3      │  │
│  │  Quantum VQE │    │  Data Bridge     │    │  SNN AedesTwin    │  │
│  │  (CUDA-Q)    │    │  (Fermion→Qubit) │    │  (Brain Sim)      │  │
│  └──────────────┘    └──────────────────┘    └───────────────────┘  │
│        │                     │                        │             │
│   Borromean Ansatz     Jordan-Wigner           Leaky I&F (LIF)     │
│   + Silver Ratio       Mapping                 + SNN Network       │
│   + COBYLA Optimizer   + PCA Compression       + Stimulus Inject   │
│        │                     │                        │             │
│        ▼                     ▼                        ▼             │
│   E_ground_state        Pauli Strings           Spike Count = 0?   │
│   (float: -5.609)       (SparsePauliOp)         (BLOQUEIO OK!)     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Estágio 1: Motor Quântico VQE (CUDA-Q / Qiskit)

**Entrada:** Hamiltoniana molecular ($\mathcal{H}$) do sistema Receptor + Molécula Inibidora.
**Saída:** Energia do Estado Fundamental ($E_{ground}$) — o "encaixe perfeito" da molécula no receptor.

### Componentes Internos

```
┌───────────────────────────────────────────────┐
│           ESTÁGIO 1: QUANTUM ENGINE            │
│                                                │
│   ┌─────────────────┐   ┌──────────────────┐  │
│   │ BorromeanAnsatz  │──▶│  StatevectorSim  │  │
│   │ (3 qubits GHZ)  │   │  ou IBM Torino   │  │
│   │ θ = π × δ_S^i   │   │  (QPU real)      │  │
│   └─────────────────┘   └──────┬───────────┘  │
│                                │               │
│                    ┌───────────▼────────────┐  │
│                    │ ClassicalMitigator     │  │
│                    │ (Regressão Linear +    │  │
│                    │  Convergência R²)      │  │
│                    └───────────┬────────────┘  │
│                                │               │
│                    ┌───────────▼────────────┐  │
│                    │ COBYLA / Adam          │  │
│                    │ (Otimizador Clássico)  │  │
│                    └───────────┬────────────┘  │
│                                │               │
│                    ┌───────────▼────────────┐  │
│                    │ OUTPUT:                │  │
│                    │ E_ground = -5.609 Ha   │  │
│                    │ Fidelidade = 97.8%     │  │
│                    │ Iterações = 450        │  │
│                    └────────────────────────┘  │
└────────────────────────────────────────────────┘
```

**Ciclo TDD:**
- 🔴 **Red:** Ansatz aleatório → mais de 5.800 iterações → sem convergência.
- 🟢 **Green:** Ansatz Borromeano + $\delta_S$ → 450 iterações → $E = -5.609$.

---

## 3. Estágio 2: Data Bridge (Tradução Fermion → Qubit)

**Entrada:** Conectoma biológico ($G = \{V, E\}$) + Hamiltoniana de interação molecular.
**Saída:** Operador quântico (`SparsePauliOp`) pronto para o Estágio 1.

### Fluxo de Transformação

```
┌────────────────────────────────────────────────────────┐
│              ESTÁGIO 2: DATA BRIDGE                     │
│                                                         │
│   Connectome JSON         Molecular Hamiltonian         │
│        │                        │                       │
│        ▼                        ▼                       │
│   ┌──────────┐           ┌──────────────┐               │
│   │ graph_   │           │ OpenFermion / │               │
│   │ parser   │           │ Qiskit Nature │               │
│   └────┬─────┘           └──────┬───────┘               │
│        │                        │                       │
│        ▼                        ▼                       │
│   Adjacency Matrix      FermionicOp (2nd Quant)         │
│   (sparse, csr)                │                        │
│        │                       ▼                        │
│        │              ┌────────────────┐                │
│        │              │ Jordan-Wigner  │                │
│        │              │ Mapper         │                │
│        │              └───────┬────────┘                │
│        │                      │                         │
│        ▼                      ▼                         │
│   PCA Compression       SparsePauliOp                   │
│   (500-1000 comp)       (Pauli Strings)                 │
│        │                      │                         │
│        └──────────┬───────────┘                         │
│                   ▼                                     │
│          Tensor unificado para                          │
│          GPU (cupy / CUDA-Q)                            │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Estágio 3: Simulador SNN AedesTwin (Brian2/NEST)

**Entrada:** Matriz de adjacência + Tensor de estímulos + $E_{ground}$ do VQE.
**Saída:** Contagem de spikes nos PNs (Projection Neurons). Se **zero**, o bloqueio foi eficaz.

### Fluxo de Simulação

```
┌─────────────────────────────────────────────────────┐
│           ESTÁGIO 3: SNN AEDESTWIN                   │
│                                                      │
│   ┌──────────┐   ┌───────────┐   ┌───────────────┐  │
│   │ Stimulus │──▶│   OSNs    │──▶│     LNs       │  │
│   │ Tensor   │   │ (Input)   │   │   (Hidden)    │  │
│   │ CO2 +    │   │ Receptor  │   │  Inibitório/  │  │
│   │ E_inhib  │   │ cpA/IR    │   │  Exitatório   │  │
│   └──────────┘   └───────────┘   └──────┬────────┘  │
│                                         │            │
│                                         ▼            │
│                                  ┌──────────────┐    │
│                                  │     PNs      │    │
│                                  │   (Output)   │    │
│                                  │  Spike Count │    │
│                                  └──────┬───────┘    │
│                                         │            │
│                           ┌─────────────▼─────────┐  │
│                           │  VEREDICTO:           │  │
│                           │  Spikes == 0 → GREEN  │  │
│                           │  Spikes > 0  → RED    │  │
│                           └───────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

**Ciclo TDD:**
- 🔴 **Red:** Mosquito detecta CO₂ normalmente → spikes nos PNs → molécula falhou.
- 🟢 **Green:** VQE + Borromeo + $\delta_S$ → $E_{ground}$ bloqueia receptor → PNs silenciosos → **INANIÇÃO SENSORIAL**.

---

## 5. Diagrama de Sequência Temporal

```
Tempo ──────────────────────────────────────────────────▶

  [Quantum Engine]          [Data Bridge]           [SNN AedesTwin]
       │                        │                        │
       │ 1. Build Borromean     │                        │
       │    Ansatz (θ=πδ_S)    │                        │
       │─────────────────────▶ │                        │
       │                        │ 2. Jordan-Wigner      │
       │                        │    Mapping             │
       │ ◀─────────────────────│                        │
       │                        │                        │
       │ 3. VQE Loop           │                        │
       │    (450 iterações)    │                        │
       │    E_ground = -5.609  │                        │
       │─────────────────────────────────────────────▶  │
       │                        │                        │ 4. Inject
       │                        │                        │    E_ground + CO2
       │                        │                        │
       │                        │                        │ 5. Run LIF Model
       │                        │                        │    (100ms sim)
       │                        │                        │
       │                        │                        │ 6. PN Spikes = 0
       │ ◀──────────────────────────────────────────────│
       │                        │                        │
       │ ✅ PIPELINE GREEN     │                        │
       │    Molécula Validada  │                        │
```

---

## 6. Mapa de Dependências entre Documentos

| Documento | Alimenta | Consome |
| :--- | :--- | :--- |
| 01 — Whitepaper Ansatz | Estágio 1 (Quantum Engine) | — |
| 02 — Data Dictionary | Estágio 2 (Data Bridge) | — |
| 03 — TDD Suite Matrix | Validação de todos os estágios | Todos |
| 05 — Hardware Benchmarking | Estágio 1 (métricas de GPU) | Estágio 1 |
| **06 — Bio Dataset Spec** | **Estágio 3 (SNN)** | — |
| **07 — TDD Pseudocódigo** | **Código de testes reais** | Docs 01, 06 |
| **08 — Pipeline (Este doc)** | **Visão Integrada de Tudo** | **Todos** |
