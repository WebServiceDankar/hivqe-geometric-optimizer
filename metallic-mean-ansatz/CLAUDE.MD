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
│   ├── PROJETO_IC_NDM1.md    # Documento de IC Acadêmico
│   ├── M2QA_PAPER_DRAFT.md   # Draft do Artigo Científico
│   └── M2QA_TECHNICAL_SPEC.md # Spec Técnica e Fundamentação Teórica (NOVO)
```

## 📜 Regras de Negócio & Design
1. **Anti-Vibe:** Proibida implementação de circuitos sem testes unitários. Resultados devem ser tratados como hipóteses até validação por ED.
2. **Borromean Topology:** Entrelacamento tripartite cíclico. Definição formal em `M2QA_TECHNICAL_SPEC.md`.
3. **Metallic Initialization:** Uso obrigatório da Razão de Prata ($\delta_S$) para quebra de simetria e fuga de BP (Barren Plateaus).
4. **Validação ED:** O padrão-ouro é a Diagonalização Exata. Precisão Química alvo: < 1.6 mHa.

## 🚀 Estado Atual
- ✅ Hamiltoniano NDM-1 estruturado.
- ✅ Ground Truth via ED implementado no código.
- ✅ Documentação técnica detalhada (Theory & Specs) criada para o professor.
- 🚧 Próximo Passo: Benchmark empírico comparando M²QA vs HEA (Random) para provar a hipótese de BP.
