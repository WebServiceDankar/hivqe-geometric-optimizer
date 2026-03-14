# 💾 Dicionário de Dados e Mapeamento Conectômico

> **Architecture Flow:** De Inseto Físico para Dados Estruturados em Matrizes Quânticas.

## 1. Origem dos Dados
Emulando as descobertas da Bioinformática (Ex: Projeto FlyWire), extraímos propriedades de conectomas que beiram 125.000 neurônios do sistema olfativo simulado.

### 📌 Formato Bruto (`.JSON` ou `NetworkX`)
- **Nós (Neurons):** IDs únicos, Camada de origem (Sensorial, Interneurônio, Motor).
- **Arestas (Synapses):** Matrizes de pesos conectivos $W_{ij}$.

## 2. Redução de Dimensionalidade e Data Cleaning
Como VQEs da fase NISQ possuem limite rigoroso de número de Qubits (5 a 127 disponíveis sem falhar catastroficamente), o pipeline exige *Data Wrangling* purista.
Apenas conexões exclusivas ao Olfato do *Aedes*:
1.  **Filtro Sensorial:** Sub-grafos que interagem primariamente com detecção de Ácido Lático e CO2.
2.  **Compressão:** Matrizes são colapsadas usando as mesmas métricas dos projetos BOLD/fMRI (Análise de Componentes Principais - PCA) para definir nós virtuais agregados.

## 3. Matrizes Matemáticas e Tradução (O Core do AedesTwin)
O conectoma lapidado vira uma **Matriz de Adjacência** (Numpy Array). A afinidade biológica entre os neurotransmissores que regem a sinalização elétrica e a molécula inibidora projetada deve se igualar a uma **Distância Numérica Mínima**.

### Conversão Quântica
Essa matriz interage com as propriedades do *Ansatz* (O Molde). A matriz simula a Repulsão ou Atração Eletrônica da molécula simulada.
Usamos a biblioteca **OpenFermion** (ou similar no Qiskit/CUDA-Q Nature) acoplada a:

```python
# Pseudo-código Arquitetural para Tradução Biológico->Quântico
from qiskit_nature.second_q.mappers import JordanWignerMapper

# Transformação do Hamiltoniano Molecular Repelente para Pauli Strings
# que cabem no processador NVIDIA (GPUs ou QPUs)
mapper = JordanWignerMapper()
qubit_op = mapper.map(fermionic_op)
```

## 4. Estrutura do Tensor de Estímulo Virtual
O ambiente simulado enviará tensores representando, por exemplo, o cheiro de suor humano.
> **Shape Esperado ($T_{stimulus}$):** $[N_{sensores}, ms_{resolucao_{tempo}}]$

Se a molécula bloqueadora do VQE agir corretamente, o pulso elétrico gerado por $T_{stimulus}$ na Spiking Neural Network (SNN) deverá ser matematicamente zerado ($\approx 0.0$ de atividade).
