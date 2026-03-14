# 📜 Especificação Matemática e Topológica (Whitepaper M²QA)

> **Documento Núcleo:** Formulação Algébrica e Topológica do *Project M²QA* (Metallic Mean Quantum Ansatz).

Este documento detalha a dedução matemática que fundamenta a nossa pesquisa de Otimização Geométrica em VQEs, utilizando a arquitetura Borromeana associada às Médias Metálicas.

## 1. A Hamiltoniana do Sistema
A Hamiltoniana $\mathcal{H}$ descreve a energia do sistema acoplado (Receptor Olfativo do *Aedes* + Molécula Inibidora).
O mapeamento Fermion-to-Qubit é realizado via transformação de **Jordan-Wigner**, convertendo operadores de criação e aniquilação fermiônicos em matrizes de Pauli ($\sigma_x, \sigma_y, \sigma_z$).

$$ \mathcal{H} = \sum_{i,j} h_{ij} a_i^\dagger a_j + \frac{1}{2} \sum_{i,j,k,l} h_{ijkl} a_i^\dagger a_j^\dagger a_k a_l \xrightarrow{J.W.} \sum_k c_k P_k $$

## 2. Topologia Borromeana (Emaranhamento Três-Partido)
A arquitetura do circuito é fundamentada no estado GHZ-like estruturado como Anéis de Borromeo:
*   **Propriedade Borromeana:** Um estado $|\Psi_B\rangle$ de 3 qubits onde a medição ou colapso (decoerência) de qualquer qubit individual $q_i$ destrói o emaranhamento restante, reduzindo o sistema a um estado misto separável.
*   **Vantagem:** Essa codificação topológica blinda os dados contra "alucinações" quânticas parciais. Se o ruído corromper um nó, o estado inteiro colapsa (Fail-Fast), essencial para nossa aderência ao TDD (Teste Red imediato).

## 3. Parametrização Dinâmica: Razão Prateada ($\delta_S$)
Para mitigar o temido problema dos *Barren Plateaus* (onde o gradiente da função de custo decai exponencialmente $\langle \partial_\theta C \rangle \to 0$), eliminamos a aleatoriedade inicial através da injeção de constantes matemáticas.

A Inicialização de Rotação segue a Razão Prateada:
$$ \delta_S = 1 + \sqrt{2} \approx 2.414 $$

Os ângulos das portas paramétricas $R_y(\theta)$ são inicializados baseados na série de Pell associada à Razão Prateada:
$$ \theta_i = \pi \times \frac{1}{\delta_S^i} $$

Essa assimetria irracional estrutural força o *optimizer* clássico a navegar o *Landcape* Energético de forma determinística desde a primeira iteração, furando o platô de gradiente nulo.
