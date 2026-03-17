# Projeto de Iniciação Científica (IC)

**Título:** Simulação Quântica de Inibidores da Metaloenzima NDM-1 utilizando o Otimizador Geométrico M²QA para o Combate à Resistência Antimicrobiana
**Aluno:** Daniel A. Palma
**Orientador:** [Nome do Professor]
**Instituição:** Universidade Federal de Itajubá (UNIFEI) - Instituto de Matemática e Computação (IMC) / Departamento de Ciência de Dados Aplicada

---

## Resumo

O surgimento de "superbactérias" resistentes aos antibióticos de último recurso é uma das maiores ameaças à saúde pública global. Essa resistência é frequentemente mediada por enzimas como a New Delhi metallo-beta-lactamase 1 (NDM-1), cujo sítio ativo bimetálico (contendo dois íons de Zinco) apresenta forte correlação eletrônica. Métodos clássicos de simulação química (como a Teoria do Funcional da Densidade - DFT) falham em prever com precisão as energias moleculares nesses casos. Este projeto propõe a utilização de Computação Quântica, especificamente o algoritmo *Variational Quantum Eigensolver* (VQE), para modelar o sítio ativo da NDM-1. Para mitigar o problema dos "barren plateaus" (platôs áridos) na otimização do VQE, será empregada a arquitetura inédita **M²QA** (Metallic Mean Quantum Ansatz), que combina o entrelaçamento topológico de anéis Borromeanos com uma inicialização de parâmetros baseada na Razão de Prata matemática. O objetivo é calcular a energia de ligação de potenciais inibidores com precisão química, estabelecendo um novo fluxo de trabalho quântico para design racional de fármacos.

---

## 1. Introdução e Justificativa

A resistência antimicrobiana (AMR) é um desafio crítico. Bactérias Gram-negativas equipadas com a enzima NDM-1 conseguem hidrolisar praticamente todos os antibióticos beta-lactâmicos, incluindo os carbapenêmicos. Desenvolver novos inibidores para bloquear a NDM-1 requer uma compreensão exata do seu sítio ativo, que opera com dois íons $Zn^{2+}$. 

A presença de metais de transição gera uma estrutura eletrônica de forte correlação. Computadores clássicos têm dificuldade exponencial em resolver a Equação de Schrödinger para tais sistemas. A Computação Quântica surge como a solução natural, usando algoritmos híbridos como o VQE em hardwares NISQ (*Noisy Intermediate-Scale Quantum*). 

O projeto propõe a utilização de Computação Quântica através do algoritmo inédito **M²QA** (Metallic Mean Quantum Ansatz), concebido pelo autor para solucionar o problema dos *barren plateaus* de maneira não heurística. Para validar os resultados computacionais na ausência de testes laboratoriais *in-vitro* imediatos, o projeto utilizará a **Diagonalização Exata (Exact Diagonalization - ED)** como padrão-ouro analítico. A ED permite obter a solução matemática exata para o Hamiltoniano do sítio ativo, servindo como base para quantificar a Precisão Química alcançada pelo simulador quântico.

Esta pesquisa justifica-se pela urgência na descoberta de inibidores da NDM-1 e pela necessidade fundamental de desenvolver Ansatzes quânticos mais eficientes e robustos contra ruídos e platôs evolutivos.

---

## 2. Objetivos

### 2.1 Objetivo Geral
Implementar, testar e avaliar a eficácia do algoritmo híbrido M²QA (Metallic Mean Quantum Ansatz) na simulação precisa do estado fundamental e da energia de ligação de inibidores no sítio ativo da metaloenzima NDM-1.

### 2.2 Objetivos Específicos
1. **Modelagem do Hamiltoniano:** Reduzir o sítio ativo bimetálico da NDM-1 para um espaço ativo tratável (e.g., 6 a 12 qubits) e mapear os operadores fermiônicos para operadores de spin de Pauli.
2. **Implementação do Algoritmo M²QA:** Codificar o VQE utilizando a topologia de portas lógicas Borromeanas e a rotina de inicialização matemática da Razão de Prata.
3. **Benchmarking:** Comparar a velocidade de convergência e a precisão do M²QA contra inicializações convencionais (Randômica) e a Razão Áurea, analisando a variância dos gradientes.
4. **Cálculo da Energia de Ligação ($\Delta E$):** Determinar a afinidade de compostos inibidores modelo (como derivados de Captopril) e comparar os resultados com métodos de Diagonalização Exata (ED).

---

## 3. Metodologia

O projeto será desenvolvido primariamente in-silico, através de simulações em supercomputadores clássicos emulando QPUs (Quantum Processing Units). A arquitetura híbrida construída pode ser observada no diagrama a seguir:

![M²QA Pipeline Híbrido](arquitetura.png)
*Figura 1. Pipeline Híbrido Quântico-Clássico para emulação computacional no combate à AMR.*

1.  **Framework:** Utilização do NVIDIA CUDA-Q e Qiskit para desenvolvimento do circuito e gerenciamento do ciclo quântico-clássico.
2.  **Química Computacional Quântica:** Geração da geometria molecular em PySCF e mapeamento de Jordan-Wigner para obter o Hamiltoniano em formato de strings de Pauli.
3.  **Desenho do Circuito (Ansatz):** Implementar blocos cíclicos de portas CNOT (entrelacionamento Borromeano) interpolados por rotações $R_y(\theta)$. Os ângulos $\theta$ iniciais seguirão a sequência de Pell ($\pi / \delta_S^k$).
4.  **Otimização:** Uso do otimizador COBYLA (classical optimizer) para refinar os ângulos de rotação até obter o limite inferior da energia (Princípio Variacional).
5.  **Análise de Dados:** Coleta das funções de custo por *epoch*, cálculo da energia de ligação (Energia do Complexo - [Energia da Enzima + Energia do Ligante]), e verificação do atingimento da "chemical accuracy" ($\sim 1 \text{ kcal/mol}$ ou $1.6 \text{ mHa}$).

---

## 4. Cronograma de Execução (12 meses)

| Mês | Atividades |
| :---: | :--- |
| **1-2** | Revisão bibliográfica sobre VQE, Resistência Antimicrobiana (NDM-1) e Ansatzes estruturados. Configuração do ambiente local (CUDA-Q). |
| **3-4** | Geração das geometrias moleculares reduzidas do sítio ativo do NDM-1 e extração dos Hamiltonianos via PySCF. |
| **5-7** | Implementação computacional do núcleo do Algoritmo M²QA (topologia Borromeana e Razão de Prata). |
| **8-9** | Execução de benchmarks do M²QA comparado aos Ansatzes de referência (Randômico) para análise da fuga de barren plateaus. |
| **10** | Simulação e extração das energias de ligação ($\Delta E$) dos ligantes candidatos na enzima modelo. |
| **11** | Análise estocástica dos resultados, compilação dos dados em gráficos e documentação final do código-fonte. |
| **12** | Escrita do Relatório Final da IC e eventual submissão de artigo científico aos periódicos propostos. |

---

## 5. Referências Bibliográficas Preliminares

1. Peruzzo, A. et al. (2014). "A variational eigenvalue solver on a photonic quantum processor." *Nature Communications*, 5(4213).
2. McClean, J. R. et al. (2018). "Barren plateaus in quantum neural network training landscapes." *Nature Communications*, 9(4812).
3. Cerezo, M. et al. (2021). "Cost function dependent barren plateaus in shallow parametrized quantum circuits." *Nature Communications*, 12(1791).
4. Yong, K. K. et al. (2011). "Structure of the New Delhi metallo-beta-lactamase 1 (NDM-1) and its interaction with antibiotic substrates." *Nature*, 475, 251-254.
5. Spinadel, M. (1999). "The metallic means family and multifractal spectra." *Nonlinear Analysis*, 36, 721-745.
6. King, D. T. et al. (2012). "Structural insights into the inhibition of the New Delhi metallo-beta-lactamase-1." *Journal of Biological Chemistry*, 287, 15451-15461.
