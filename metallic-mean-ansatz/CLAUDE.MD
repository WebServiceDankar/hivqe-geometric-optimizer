# CLAUDE.MD — Spec do Project M²QA (Metallic Mean Quantum Ansatz)
> Fonte de verdade viva do projeto. Atualizar antes de qualquer implementação.
> **Metodologia:** Anti-Vibe Coding (Akita Way) — TDD obrigatório, Design First.

## 🎯 Domínio do Problema: NDM-1 & Superbactérias
O objetivo é simular o sítio ativo da enzima NDM-1 (Forte Correlação Eletrônica em di-Zinco) para validar inibidores candidatos, utilizando um Ansatz quântico robusto que evite Barren Plateaus.

## 🛠️ Stack Tecnológica
- **Simulador:** NVIDIA CUDA-Q (Primary) / Qiskit (Fallback/Local).
- **Química:** PySCF + OpenFermion (Hamiltoniano Molecular).
- **Validação:** Diagonalização Exata (ED) via SciPy.
- **Otimização:** COBYLA (Clássico).
- **Linguagem:** Python 3.10+.

## 📂 Estrutura de Diretórios
```
metallic-mean-ansatz/
├── CLAUDE.MD               # Esta Spec
├── src/
│   ├── ndm1_active_site.py # Hamiltoniano (NDM-1) + ED Ground Truth
│   ├── m2qa_ansatz.py      # Core: Topologia Borromeana + Razão de Prata (A IMPLEMENTAR)
│   ├── orchestrator.py     # Loop VQE Híbrido
├── tests/
│   ├── test_active_site.py
│   ├── test_m2qa_ansatz.py # TDD para o Ansatz (A IMPLEMENTAR)
├── docs/
│   ├── PROJETO_IC_NDM1.md  # Documento de IC Acadêmico
│   └── M2QA_PAPER_DRAFT.md # Draft do Artigo Científico
```

## 📜 Regras de Negócio & Design
1. **Anti-Vibe:** Proibida implementação de circuitos sem testes unitários de fidelidade e profundidade.
2. **Borromean Topology:** Entrelacamento tripartite cíclico (0->1, 1->2, 2->0). Deve ser detectável via colapso de estado.
3. **Metallic Initialization:** Ângulos iniciais fixos baseados em $\theta_k = \pi / \delta_S^k$, onde $\delta_S = 1 + \sqrt{2}$. **Proibido `random.uniform`**.
4. **Validação ED:** Todo resultado VQE deve ser comparado com o valor de `get_exact_energy()` do `ndm1_active_site.py`.

## 🚀 Estado Atual
- ✅ Hamiltoniano NDM-1 estruturado (Mock/PySCF ready).
- ✅ Ground Truth via ED implementado.
- 🚧 Próximo Passo: TDD do `m2qa_ansatz.py`.
