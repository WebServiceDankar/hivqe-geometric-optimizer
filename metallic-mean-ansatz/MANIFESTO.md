# MANIFESTO CIENTÍFICO

<div align="center">

## Project M²QA: Metallic Mean Quantum Ansatz
### Topologia Borromeana Parametrizada por Constantes Irracionais

**Universidade Federal de Itajubá (UNIFEI)**
Curso de Ciência de Dados Aplicada

**Pesquisador:** Daniel A. Palma
**Orientador:** *A definir*
**Data de início:** Março de 2026

---

*"Não buscamos a molécula perfeita. Buscamos a geometria que a revela."*

</div>

---

## I. Declaração de Propósito

Este manifesto estabelece a fundamentação científica, a motivação e o compromisso metodológico do **Project M²QA** — uma investigação na fronteira entre a **Teoria dos Números**, a **Computação Quântica** e a **Biologia Computacional**.

O projeto nasce de uma observação simples, porém matematicamente profunda: **se as constantes irracionais fundamentais governam estruturas da natureza** — dos braços de galáxias espirais ($\phi$) à cristalografia dos quasicristais ($\delta_S$) — **por que não deveriam governar também a topologia dos circuitos quânticos que simulam essa mesma natureza?**

---

## II. O Problema Científico

### 2.1. O Gargalo da Era NISQ

Os computadores quânticos atuais — classificados como **NISQ** (*Noisy Intermediate-Scale Quantum*) — operam com dezenas a centenas de qubits ruidosos. O principal algoritmo para extração de propriedades moleculares nesses dispositivos é o **VQE** (*Variational Quantum Eigensolver*), um método híbrido quantum-clássico.

O desempenho do VQE depende criticamente da escolha do **Ansatz**: a forma paramétrica do circuito quântico. Ansatzes mal desenhados sofrem de:

1. **Barren Plateaus** — Regiões planas no espaço de parâmetros onde o gradiente da função de custo decai exponencialmente ($\langle \partial_\theta C \rangle \to 0$), tornando o otimizador clássico cego.
2. **Mínimos Locais Acidentais** — Armadilhas energéticas que não correspondem ao estado fundamental real da molécula.
3. **Vulnerabilidade à Decoerência** — Circuitos profundos acumulam erros proporcionais ao número de portas.

### 2.2. A Lacuna na Literatura

A comunidade científica tem explorado extensivamente Ansatzes *hardware-efficient* (lineares, com conectividade restrita ao chip) e Ansatzes *chemically-inspired* (como UCCSD). No entanto, **a influência de constantes matemáticas irracionais na parametrização angular desses circuitos permanece largamente inexplorada**.

Trabalhos recentes demonstram que inicializações não-aleatórias podem mitigar Barren Plateaus (McClean et al., 2018; Cerezo et al., 2021), mas nenhum estudo propôs uma investigação sistemática utilizando a **família das Médias Metálicas** como base de inicialização topológica.

---

## III. A Hipótese Central

> **Hipótese M²QA:** A combinação de uma topologia de emaranhamento Borromeana (estrutura) com inicialização angular baseada na Razão Prateada ($\delta_S = 1 + \sqrt{2}$) (parâmetro) produz convergência significativamente mais rápida e com maior fidelidade no VQE, quando comparada a inicializações aleatórias ou baseadas na Razão Áurea ($\phi$), especificamente em hamiltonianos moleculares de relevância epidemiológica.

### Desdobramentos Testáveis

| # | Sub-hipótese | Métrica de Verificação |
| :---: | :--- | :--- |
| H1 | A topologia Borromeana (GHZ três-partido) oferece proteção contra decoerência local superior à conectividade linear. | Fidelidade do estado após introdução de erro em qubit individual. |
| H2 | A Razão Prateada ($\delta_S$) converge mais rápido que a Razão Áurea ($\phi$) e a inicialização aleatória. | Número de iterações VQE até $|E - E_{target}| < \epsilon$. |
| H3 | A combinação Borromeo + $\delta_S$ mitiga Barren Plateaus de forma mensurável. | Variância do gradiente $\text{Var}[\partial_\theta C]$ ao longo das épocas. |
| H4 | A molécula obtida via M²QA é capaz de bloquear a transdução olfativa do *Aedes aegypti* *in-silico*. | Contagem de spikes nos Projection Neurons (PNs) = 0 após injeção. |

---

## IV. A Aplicação: AedesTwin In-Silico

A pesquisa não é matemática abstrata. Ela possui um **alvo epidemiológico concreto**: a erradicação de vetores da Dengue, Zika e Chikungunya.

### 4.1. A Premissa Biológica

O *Aedes aegypti* localiza hospedeiros humanos primariamente através do seu sistema olfativo, detectando CO₂ exalado e ácido lático da pele. Se conseguirmos projetar uma molécula que **bloqueie os receptores sensoriais olfativos (OSNs)** do inseto, ele perde a capacidade de encontrar vítimas — entrando em **inanição sensorial**.

### 4.2. O Papel do M²QA

Calcular a energia de ligação exata dessa molécula bloqueadora requer simular interações quânticas entre o receptor proteico e o ligante candidato. Isso é um problema de **Química Quântica Computacional** — exatamente o domínio do VQE.

O M²QA não busca qualquer molécula. Ele busca a molécula cujo **estado fundamental** ($E_{ground}$) se encaixa geometricamente no receptor do mosquito com precisão suficiente para silenciar completamente a via neural olfativa.

---

## V. Metodologia

### 5.1. Desenvolvimento Orientado por Testes (TDD como Método Científico)

Este projeto adota o **Test-Driven Development** não como prática de engenharia de software, mas como **metodologia científica computacional**:

| Fase TDD | Equivalência Científica | Ação Concreta |
| :--- | :--- | :--- |
| 🔴 **Red** (Teste falha) | Formulação da hipótese | Escrever teste que exige resultado ainda impossível. |
| 🟢 **Green** (Teste passa) | Confirmação experimental | Implementar código mínimo que satisfaça a predição. |
| 🔄 **Refactor** (Otimização) | Revisão por pares | Simplificar sem alterar comportamento validado. |

### 5.2. Pipeline Computacional (3 Estágios)

```
ESTÁGIO 1              ESTÁGIO 2              ESTÁGIO 3
Quantum Engine    →    Data Bridge      →    SNN AedesTwin
(CUDA-Q / Qiskit)     (Jordan-Wigner)       (Brian2 / NEST)

Borromean Ansatz       Fermion → Qubit       OSN → LN → PN
+ Silver Ratio δ_S     + PCA Compression     + Leaky I&F Model
+ COBYLA Optimizer     + SparsePauliOp       + Stimulus Injection

OUTPUT:                OUTPUT:                OUTPUT:
E_ground (Hartree)     Pauli Strings          Spike Count = 0?
```

### 5.3. Infraestrutura

- **Simulação Local:** NVIDIA CUDA-Q (paralelismo GPU para otimização clássica).
- **Hardware Quântico Real:** IBM Quantum (QPU Torino/Eagle) para validação final.
- **Simulação Neural:** Brian2 (modelo Leaky Integrate-and-Fire em Python).

---

## VI. Contribuições Esperadas

Este projeto aspira entregar as seguintes contribuições à comunidade científica:

### Contribuição Teórica
1. **Uma taxonomia formalizada** da influência das Médias Metálicas ($\phi$, $\delta_S$, $\rho$, $e$, $\mathcal{L}$) na paisagem energética de VQEs, documentada na **M²QA Table**.
2. **Prova computacional** de que a Razão Prateada oferece equilíbrio superior entre velocidade de convergência e fidelidade quântica em hardware NISQ.

### Contribuição Aplicada
3. **Um Digital Twin funcional** (*in-silico*) do sistema olfativo do *Aedes aegypti*, calibrado com dados de conectomas públicos (FlyWire/NeuroMorpho).
4. **Candidatas moleculares computacionais** para bloqueio do receptor olfativo, geradas pelo pipeline M²QA e validadas contra a Spiking Neural Network do AedesTwin.

### Contribuição Metodológica
5. **Framework reprodutível** de TDD aplicado à pesquisa em computação quântica, demonstrando que o ciclo Red-Green-Refactor é isomorfo ao método científico clássico (Hipótese → Experimento → Revisão).

---

## VII. Posicionamento na Literatura

| Trabalho de Referência | Relação com M²QA |
| :--- | :--- |
| Peruzzo et al. (2014) — *"A variational eigenvalue solver on a photonic quantum processor"* | Fundação teórica do VQE. M²QA propõe um Ansatz alternativo. |
| McClean et al. (2018) — *"Barren plateaus in quantum neural network training landscapes"* | Identificou o problema. M²QA propõe mitigação via Médias Metálicas. |
| Kandala et al. (2017) — *"Hardware-efficient variational quantum eigensolver"* | Ansatz hardware-efficient linear. M²QA substitui por topologia Borromeana. |
| FlyWire Consortium (2024) — *"Whole-brain connectome of Drosophila"* | Fonte de dados para o proxy biológico do AedesTwin. |
| Takagi & Nishimoto (2023) — *"High-resolution image reconstruction with latent diffusion"* | Paralelo metodológico (fMRI → Latent Space). Inspira o mapeamento Neural → Qubit. |

---

## VIII. Compromissos Éticos

1. **Sandbox Computacional:** Toda simulação biológica opera em ambiente isolado. Nenhum circuito de feedback interage com organismos vivos reais.
2. **Open Science:** Código, dados e resultados serão publicados sob licença MIT, permitindo reprodutibilidade total.
3. **Finalidade Sanitarista:** Os outputs moleculares são estritamente destinados à pesquisa de erradicação de vetores epidemiológicos, nunca para formulação de bioagentes ou perturbação ecológica de polinizadores.

---

## IX. Declaração Final

O **Project M²QA** não é um exercício acadêmico isolado. É uma ponte deliberada entre três mundos que raramente conversam: a elegância abstrata da **Teoria dos Números**, o poder bruto da **Computação Quântica** e a urgência prática da **Saúde Pública**.

Se a Razão Prateada governa a estabilidade dos quasicristais, e os quasicristais governam a distribuição de energia em materiais, então não é irrazoável perguntar: **pode essa mesma razão governar a molécula que salva vidas?**

Este manifesto é o nosso compromisso em responder a essa pergunta com rigor, transparência e código testável.

---

<div align="center">

*Universidade Federal de Itajubá (UNIFEI)*
*Ciência de Dados Aplicada — 2026*

**Daniel A. Palma**
Pesquisador Principal

</div>
