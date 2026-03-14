# 🦟 Documento 6: Especificação do Dataset Biológico (Conectoma AedesTwin)

> **Classificação:** Onde a Biologia encontra a Ciência de Dados.
> O mosquito deixa de ser um animal e passa a ser um **sistema cibernético de processamento de informação** — uma rede complexa de nós e arestas que pode ser armazenada, consultada e manipulada.

---

## 1. Visão Geral

Este documento define a arquitetura de dados e os esquemas estruturais (*schemas*) utilizados para emular o sistema olfativo do *Aedes aegypti*. O AedesTwin **não** simula a física do mosquito inteiro, mas foca estritamente no seu "hardware de entrada de dados": as **antenas**, os **palpos maxilares** e o **lóbulo antenal**. O objetivo é criar um grafo direcionado de alta fidelidade que receberá os estímulos de energia calculados pela rede híbrida CUDA-Q/VQE.

---

## 2. Estrutura do Grafo Neural ($G = \{V, E\}$)

A rede biológica será traduzida para a teoria dos grafos. Isso permite que algoritmos clássicos percorram a rede e calculem a propagação do sinal antes de delegar as interações de nível quântico para a QPU.

### 2.1. Nós ($V$ — Vértices / Neurônios)

Cada neurônio relevante para a olfação é um nó no banco de dados. Eles são classificados em três camadas:

| Camada | Classe | Localização | Função |
| :--- | :--- | :--- | :--- |
| **Input** | OSNs (Olfactory Sensory Neurons) | Antenas | Sensores que interagem diretamente com a molécula (o alvo do nosso VQE). |
| **Oculta** | LNs (Local Neurons) | Glomérulos | Processamento lateral inibitório ou excitatório dentro do lóbulo antenal. |
| **Output** | PNs (Projection Neurons) | Corpos Cogumelo | Enviam a informação processada ("Encontrei CO₂/Sangue") para centros superiores do cérebro. |

**Schema de Dados do Nó (JSON/Dict):**

```json
{
  "node_id": "OSN_CO2_001",
  "type": "sensory_neuron",
  "layer": "input",
  "receptor_protein": "cpA",
  "threshold_potential": -55.0,
  "resting_potential": -70.0
}
```

### 2.2. Arestas ($E$ — Edges / Sinapses)

As conexões físicas entre os neurônios. Como estamos lidando com um modelo cibernético de transdução de sinal, as arestas contêm pesos matemáticos que definem a força da conexão.

**Schema de Dados da Aresta:**

```json
{
  "source": "OSN_CO2_001",
  "target": "PN_Glomerulus_1",
  "weight": 0.85,
  "neurotransmitter": "GABA",
  "synapse_type": "inhibitory",
  "latency_ms": 1.2
}
```

---

## 3. Armazenamento e Processamento (Matriz de Adjacência)

Para que o ambiente NVIDIA consiga processar o AedesTwin rapidamente, o grafo **não** será lido como um arquivo de texto linha por linha. O dataset biológico será convertido em uma **Matriz Esparsa de Adjacência**.

Nesta matriz:
- As **linhas** e **colunas** representam os neurônios ($V$).
- Os **valores** na interseção representam os pesos sinápticos ($E$).
- Como a maioria dos neurônios não se conecta diretamente com todos os outros, a matriz será preenchida majoritariamente por zeros.

Utilizaremos tensores otimizados para GPU (`scipy.sparse` → `cupy.sparse`) para armazenar apenas as conexões ativas, garantindo máxima eficiência de memória.

```python
# Conversão Conceitual: Grafo NetworkX → Matriz Esparsa → Tensor GPU
import networkx as nx
import scipy.sparse as sp

G = nx.DiGraph()
# ... populando G com nós e arestas do conectoma ...
adj_matrix = nx.to_scipy_sparse_array(G, weight='weight', format='csr')
# Pronto para delegação ao CUDA-Q ou ao Brian2 SNN Engine.
```

---

## 4. O Modelo Funcional (Leaky Integrate-and-Fire — LIF)

Como esses nós reagem? Usaremos uma variação do modelo **LIF**. Cada nó acumula a "energia" (sinal) que recebe das arestas. Se essa energia ultrapassar o `threshold_potential`, o nó **"dispara"** (*fire*) enviando o sinal adiante, e depois **"vaza"** (*leaky*) de volta ao estado de repouso.

A diferença do AedesTwin é o **input**: o sinal inicial que entra nos OSNs **não** é um número aleatório. É o valor da **energia de ligação ($E$) calculada pela Hamiltoniana** no Whitepaper (Doc 01).

$$ \tau_m \frac{dV}{dt} = -(V - V_{rest}) + R_m \cdot I_{ext}(t) $$

Onde:
- $V$ é o potencial de membrana do neurônio.
- $V_{rest}$ é o potencial de repouso ($-70mV$).
- $\tau_m$ é a constante de tempo da membrana.
- $I_{ext}(t)$ é a corrente de entrada externa (vinda dos estímulos virtuais ou da molécula VQE).
- $R_m$ é a resistência da membrana.

---

## 5. Especificação TDD (Cibernética de Validação)

A integridade deste banco de dados será validada estritamente através do TDD, testando o fluxo de informação de ponta a ponta.

### Teste BioData-01: O Baseline (Comportamento Neutro)
- **Input:** $E_{ambiente}$ (Ruído atmosférico normal).
- **🔴 Red:** A rede dispara sinais caóticos de detecção na camada PN.
- **🟢 Green:** A rede se mantém em estado de repouso (silêncio neural).

### Teste BioData-02: A Detecção Positiva (Transdução Funcional)
- **Input:** $E_{CO_2}$ (Assinatura energética simulada do dióxido de carbono).
- **🔴 Red:** Os PNs não registram atividade superior a 90% do limiar de disparo.
- **🟢 Green:** Cascata de sinal confirmada. A via de navegação olfativa "acende".

### Teste BioData-03: O Objetivo Final (O Bloqueio M²QA)
- **Input:** $E_{CO_2}$ + $E_{molécula\_inibitora}$ (Assinatura vinda do VQE).
- **🔴 Red:** O sinal de detecção contorna o bloqueio; o mosquito digital ainda "vê" o alvo.
- **🟢 Green:** Colapso da informação. A molécula inibidora projetada altera a dinâmica do nó OSN, impedindo-o de atingir o `threshold_potential`. A rede entra em **inanição sensorial**.
