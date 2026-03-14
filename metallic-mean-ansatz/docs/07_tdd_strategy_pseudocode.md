# 🧪 Documento 7: Estratégia de Testes TDD (Pseudocódigo Integrado)

> **Fase 2 do Akita Way:** Testes Primeiro, Sempre.
> O código de produção só é escrito **depois** que os testes existem e falham (Red → Green → Refactor).

---

## 1. Filosofia: TDD como Método Científico

No M²QA, cada ciclo **Red-Green-Refactor** equivale ao método científico:

| TDD | Ciência |
| :--- | :--- |
| 🔴 Red (Teste falha) | Hipótese formulada e testada — resultado negativo esperado. |
| 🟢 Green (Teste passa) | Experimento confirmou a hipótese com dados mensuráveis. |
| 🔄 Refactor (Otimização) | Revisão por pares e simplificação do modelo experimental. |

---

## 2. Suite de Testes Unitários (Pseudocódigo `pytest`)

### 2.1. Módulo `connectome-core` (Grafos Biológicos)

```python
# tests/test_graph_parser.py

def test_parse_json_to_adjacency_matrix():
    """
    Red: Não existe parser. ImportError.
    Green: Parser retorna np.ndarray com shape correto.
    """
    fake_connectome = {
        "neurons": [
            {"id": "OSN_CO2_001", "type": "sensory_neuron", "threshold": -55.0},
            {"id": "LN_Glom_001", "type": "local_neuron",   "threshold": -60.0},
            {"id": "PN_Output_001", "type": "projection_neuron", "threshold": -55.0}
        ],
        "synapses": [
            {"source": "OSN_CO2_001", "target": "LN_Glom_001", "weight": 0.85, "latency_ms": 1.2},
            {"source": "LN_Glom_001", "target": "PN_Output_001", "weight": 0.60, "latency_ms": 0.8}
        ]
    }
    matrix = parse_to_adjacency_matrix(fake_connectome)
    
    assert matrix.shape == (3, 3)
    assert matrix[0, 1] == 0.85   # OSN -> LN
    assert matrix[1, 2] == 0.60   # LN -> PN
    assert matrix[2, 0] == 0.0    # Sem conexão reversa


def test_sparse_conversion_preserves_non_zero_count():
    """
    Valida que a conversão Dense -> Sparse não perde arestas sinápticas.
    """
    dense = parse_to_adjacency_matrix(fake_connectome)
    sparse = to_sparse_csr(dense)
    
    assert sparse.nnz == 2  # Apenas 2 conexões ativas


def test_reject_invalid_neuron_schema():
    """
    Edge case: JSON sem campo 'threshold_potential' deve levantar ValueError.
    """
    broken = {"neurons": [{"id": "X", "type": "unknown"}], "synapses": []}
    with pytest.raises(ValueError, match="threshold"):
        parse_to_adjacency_matrix(broken)
```

### 2.2. Módulo `brain-simulator` (SNN Engine)

```python
# tests/test_snn_engine.py

def test_lif_neuron_fires_above_threshold():
    """
    Red: Neurônio não implementado.
    Green: Neurônio dispara quando I_ext(t) suficiente.
    """
    neuron = LIFNeuron(v_rest=-70.0, v_threshold=-55.0, tau_m=10.0)
    
    # Injetar corrente forte por 15ms simulados
    spikes = neuron.simulate(current=20.0, duration_ms=15.0, dt=0.1)
    
    assert len(spikes) > 0, "Neurônio deveria ter disparado!"
    assert spikes[0] < 15.0, "Spike deve ocorrer antes de 15ms"


def test_lif_neuron_silent_below_threshold():
    """
    Baseline: Sem estímulo suficiente, silêncio total.
    """
    neuron = LIFNeuron(v_rest=-70.0, v_threshold=-55.0, tau_m=10.0)
    spikes = neuron.simulate(current=0.5, duration_ms=50.0, dt=0.1)
    
    assert len(spikes) == 0, "Neurônio NÃO deveria disparar com corrente mínima"


def test_inhibitory_synapse_blocks_signal():
    """
    O Objetivo Final: molécula inibidora desliga o sistema.
    """
    network = AedesTwinNetwork.from_connectome(fake_connectome)
    
    # Estímulo de CO2 MAIS molécula inibidora do VQE
    result = network.simulate(
        stimulus={"CO2": 1.0, "inhibitor_energy": -5.609},
        duration_ms=30.0
    )
    
    pn_spikes = result.get_spikes("PN_Output_001")
    assert len(pn_spikes) == 0, "PN NÃO deveria disparar — molécula bloqueou receptor"
```

### 2.3. Módulo `quantum_engine` (Ansatz M²QA)

```python
# tests/test_borromean_ansatz.py

def test_borromean_topology_collapses_on_partial_trace():
    """
    TQ-01: Validação Topológica.
    Se medirmos q0, o emaranhamento entre q1 e q2 DEVE ser destruído.
    """
    ansatz = BorromeanAnsatz(n_qubits=3, ratio=SILVER_RATIO)
    circuit = ansatz.build()
    
    # Traço parcial eliminando q0
    reduced_dm = partial_trace(circuit, keep=[1, 2])
    concurrence = compute_concurrence(reduced_dm)
    
    assert concurrence < 0.01, "Emaranhamento residual! Topologia NÃO é Borromeana"


def test_silver_ratio_initialization_avoids_zero_angles():
    """
    TQ-02: Nenhum ângulo pode ser zero (causaria Barren Plateau).
    """
    ansatz = BorromeanAnsatz(n_qubits=3, ratio=SILVER_RATIO)
    angles = ansatz.get_initial_angles()
    
    for i, theta in enumerate(angles):
        assert abs(theta) > 1e-6, f"Ângulo θ[{i}] é zero! Violação Silver Ratio"
        assert abs(theta - round(theta, 0)) > 1e-3, f"Ângulo θ[{i}] é racional! Violação MMA"


def test_golden_vs_silver_convergence():
    """
    O benchmark central do paper M²QA.
    """
    results_gold = run_vqe(ratio=GOLDEN_RATIO, max_epochs=500)
    results_silver = run_vqe(ratio=SILVER_RATIO, max_epochs=500)
    
    assert results_silver["epochs_to_converge"] < results_gold["epochs_to_converge"], \
        "Hipótese REJEITADA: Prata deve convergir mais rápido que Ouro"
    assert results_silver["final_fidelity"] > 0.95, \
        "Fidelidade da Prata insuficiente para aplicação no AedesTwin"
```

---

## 3. Suite de Testes de Integração

```python
# tests/test_integration_pipeline.py

def test_full_pipeline_vqe_to_snn():
    """
    O Grande Teste: VQE encontra molécula → SNN confirma bloqueio.
    """
    # Fase 1: VQE encontra o Ground State (molécula ideal)
    vqe_result = run_vqe(ratio=SILVER_RATIO, max_epochs=1000)
    inhibitor_energy = vqe_result["ground_state_energy"]
    
    # Fase 2: Injetar no AedesTwin
    network = AedesTwinNetwork.from_connectome(real_connectome)
    sim_result = network.simulate(
        stimulus={"CO2": 1.0, "inhibitor_energy": inhibitor_energy},
        duration_ms=100.0
    )
    
    # Fase 3: Verificar bloqueio
    total_pn_spikes = sum(
        len(sim_result.get_spikes(pn)) for pn in network.projection_neurons
    )
    
    assert total_pn_spikes == 0, (
        f"PIPELINE FALHOU: {total_pn_spikes} spikes detectados nos PNs. "
        f"A molécula com E={inhibitor_energy:.4f} NÃO bloqueou o receptor."
    )
```

---

## 4. Checklist TDD (Fase 2 — Akita Way)

Antes de qualquer `git push`:

- [ ] Todos os testes unitários de `connectome-core` passam?
- [ ] Todos os testes unitários de `brain-simulator` passam?
- [ ] Todos os testes unitários de `quantum_engine` (Borromean) passam?
- [ ] O teste de integração `test_full_pipeline_vqe_to_snn` passa?
- [ ] `CLAUDE.MD` foi atualizado com o novo estado dos componentes?
- [ ] Nenhum código de produção foi escrito sem o teste correspondente existir antes?
