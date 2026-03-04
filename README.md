<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Logo_Unifei.svg/2560px-Logo_Unifei.svg.png" width="180" alt="UNIFEI Logo">
  
  <br><br>
  
  <h1><b>Otimização Topológica de VQE<br>via Razão Áurea e Anéis de Borromeo</b></h1>
  
  <p>
    <b>Universidade Federal de Itajubá (UNIFEI)</b><br>
    <i>Especialização / Ciência de Dados Aplicada</i>
  </p>

  <div>
    <img src="https://img.shields.io/badge/Status-Pesquisa_Em_Desenvolvimento-004d99?style=for-the-badge&logo=github" alt="Status">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/NVIDIA_CUDA--Q-76B900?style=for-the-badge&logo=nvidia&logoColor=white" alt="CUDA-Q">
    <img src="https://img.shields.io/badge/Licen%C3%A7a-MIT-green?style=for-the-badge" alt="License">
  </div>
</div>

---

## 👨‍🔬 Equipe de Pesquisa
- **Pesquisador:** Daniel A. Palma
- **Orientador / Coordenador:** Prof. Dr. Matheus Brendon

---

## 📝 Resumo do Projeto

Este projeto de pesquisa propõe uma abordagem inovadora para resolver o problema de lentidão na convergência e alta demanda de recursos do algoritmo **HiVQE** (*Hardware-efficient Variational Quantum Eigensolver*), o atual estado da arte em computação quântica para simulação de moléculas.

Enquanto os métodos tradicionais sofrem com a inicialização randômica (que gera desperdício computacional) e emaranhamento linear (frequentemente frágil ou suscetível a *barren plateaus*), esta proposta utiliza **constantes matemáticas da natureza** (A Razão Áurea) e **topologias complexas** (Anéis de Borromeo) para otimizar drasticamente o processo de convergência do algoritmo na QPU real ou simulada.

## 🎯 Objetivos

### Objetivo Geral
Demonstrar que a utilização de topologias não-orientáveis no emaranhamento e a inicialização de parâmetros determinísticos podem reduzir o uso de chamadas ao hardware quântico em mais de **50%** em comparação ao HiVQE padrão.

### Objetivos Específicos
- [ ] Implementar um circuito de emaranhamento (*entanglement layer*) baseado na topologia geométrica de **Anéis de Borromeo** através de portas de Clifford.
- [ ] Substituir a inicialização randômica clássica por uma técnica baseada na **Razão Áurea ($\Phi$)**.
- [ ] Simular algoritmos de emaranhamento avançados utilizando a infraestrutura da **NVIDIA CUDA-Q** para atestar a velocidade de convergência do Ansatz.
- [ ] Estabelecer um referencial comparativo (benchmark) rigoroso contra os métodos tradicionais.

## 💡 Fundamentação Teórica e Arquitetura

> A documentação e fundamentação matemática encontram-se na pasta detalhada em `/docs`.

### O Problema (Benchmarking do "Estado da Arte")
Atualmente, a execução do algoritmo VQE consome tempos impraticáveis à medida que os *qubits* escalam, motivado principalmente por:
1. **Inicialização Randômica dos Parâmetros:** Requerer milhares de passos excessivos do otimizador clássico apenas para encontrar regiões de gradiente não-nulo.
2. **Emaranhamento Frágil (Linear/Circular):** Ansatzes típicos de vizinhos-mais-próximos geram baixo poder expressivo do estado quântico no começo das rotinas de Machine Learning Quântico e Química Quântica.

### A Novidade Proposta
1. **Topologia de Borromeo:** Estrutura onde os 3 ou mais qubits estão travados de forma que o corte de qualquer das medições destrói as propriedades conjuntas – garantindo um estado de emaranhamento profundo (GHZ/W States) com menor profundidade do circuito.
2. **Distribuição em Razão Áurea ($\Phi \approx 1.61803$):** Distribuir os pesos iniciais das rotações $R_y$ e $R_z$ mapeados pelos números de Fibonacci ou divisão Áurea gera uma amostragem que historicamente cobre o espaço de distâncias na Esfera de Bloch de forma ótima.

## 🛠️ Stack Tecnológica

| Camada | Tecnologia Principal | Uso no Projeto |
| :--- | :--- | :--- |
| **Simulação Híbrida** | `NVIDIA CUDA-Q` | Framework escalável para delegação inteligente entre CPU/GPU/QPU. |
| **Linguagem Base** | `Python 3.10+` | Construção lógica do modelo VQE e orquestração. |
| **Cálculo de Otimização** | `SciPy` / `PyTorch` | Otimizadores matemáticos clássicos acoplados aos gradientes quânticos. |

## 📁 Estrutura de Diretórios

```text
hivqe-geometric-optimizer/
├── src/                # Código fonte primário (Ansatz, Gate Definitions, Custo)
├── results/            # Dataframes, Gráficos matplotlib e outputs gravados
├── docs/               # Monografia, Trabalhos acadêmicos e PDFs LaTeX
├── benchmarks/         # Testes quantitativos (Scripts comparando HiVQE/Old vs New)
├── LICENSE             # Declaração MIT License
└── README.md           # Visão geral do repositório
```

## 📚 Referências Bibliográficas

1. TILLY, J. et al. *The Variational Quantum Eigensolver: A review of methods and best practices*. Physics Reports, 2022.
2. [Inserir referência acadêmica sobre Anéis de Borromeo em Teoria da Informação Quântica].
3. [Inserir referência do Prof. ou paper sobre Distribuição Áurea / Otimização Global].

---
<div align="center">
  <i>Projeto desenvolvido como requisito científico junto à <b>Universidade Federal de Itajubá (UNIFEI)</b>.<br>Grupo de Computação Quântica e Ciência de Dados Aplicada (2026).</i>
</div>
