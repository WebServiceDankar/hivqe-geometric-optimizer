# 🦟 AedesTwin In-Silico

**Digital Twin de conectomas de insetos para erradicação de vetores da Dengue.**
Um projeto de Ciência de Dados Aplicada focando em processamento de Grafos Neurais e Spiking Neural Networks (SNN).

## 🎯 O Desafio
Testar repelentes e atrativos biológicos in vivo é caro e lento. Este projeto aplica a filosofia de desenvolvimento contínuo para construir um simulador *in silico*. Utilizando dados de conectomas abertos (iniciando com a *Drosophila* via FlyWire), mapeamos a rede neural do inseto em matrizes de adjacência matemáticas e simulamos sua resposta a estímulos virtuais (CO2 e Calor) usando Python e SNNs.

## 🛠 Metodologia de Desenvolvimento (Akita Way)
Este repositório não aceita "vibe coding" gerado puramente por IA de forma randômica. Operamos sob regras estritas:
1. **Design First:** A arquitetura multisserviço foi desenhada antes da primeira linha de código (veja `CLAUDE.md`).
2. **TDD como Fundação:** Toda conversão de grafos e simulação de neurônios é coberta por `pytest` antes da implementação real.
3. **Contratos de Dados Rígidos:** Comunicação entre o simulador do cérebro e o ambiente virtual usa esquemas Pydantic estritos para evitar falhas de tipagem.

## 🚀 Como Executar Localmente

### 1. Preparando o Ambiente
Recomendamos o uso de `venv` ou `conda`:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

### 2. Validando a Rede de Segurança (Testes)
Nenhum commit é feito sem passar por isso:
```bash
pytest packages/connectome-core/tests/
pytest apps/brain-simulator/tests/
```

### 3. Subindo a Arquitetura
```bash
docker-compose up -d
```
Acesse o Dashboard interativo via http://localhost:8501.

## 🧠 Próximos Passos na Arquitetura

- Implementar a conversão JSON do NeuroMorpho para Matriz Numpy (`connectome-core`).
- Criar o teste de integração (Testando o disparo neural contra uma nuvem virtual de CO2).
- Desenvolver o loop do modelo Leaky Integrate-and-Fire usando a biblioteca Brian2.

---

### Como você (O Humano) deve operar a IA a partir daqui:

**Exemplo de fluxo prático seguindo o "Akita Way":**

Você não vai dizer para a IA: *"Crie o simulador do cérebro da mosca pra mim"*. (Isso é Vibe Coding).

Você vai abrir o terminal, criar o repositório, colocar o `CLAUDE.md` e dar o seguinte prompt para a IA (como o Claude ou ChatGPT):

> *"Leia o arquivo CLAUDE.md para pegar o contexto do projeto. Nossa tarefa hoje é na Fase 2: TDD. Vamos começar pelo `packages/connectome-core`. Quero que você crie o arquivo `test_graph_parser.py`. O teste deve simular a entrada de um JSON fictício com 3 neurônios e 2 sinapses, e verificar se a nossa função `parse_to_adjacency_matrix` (que ainda não existe) retorna uma matriz Numpy 3x3 correta. Apenas escreva o código do teste."*

Quando ela escrever o teste (e você rodar e ver que falhou vermelho), aí sim você pede: 
> *"Ótimo. Agora escreva a implementação real no arquivo `graph_parser.py` para fazer esse teste passar."*

Com essa estrutura, seu TCC deixa de ser apenas "um script em Python" e se torna uma **Arquitetura de Engenharia de Software e Dados Profissional**, pronta para impressionar qualquer banca universitária.
