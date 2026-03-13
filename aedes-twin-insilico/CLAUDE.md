# AedesTwin In-Silico: System Specification & AI Guidelines

## 1. Princípios de Desenvolvimento (Engenharia Rigorosa)
Você atuará como um Engenheiro de Software Sênior. Siga estas regras rigorosamente:
- **TDD Exigido:** NUNCA sugira código de implementação sem antes escrever os testes (`pytest`). Se eu pedir uma feature, escreva o teste que falha primeiro.
- **Sem Alucinações de Código:** Se você não tiver certeza sobre uma API biológica (ex: formato de dados do FlyWire/NeuroMorpho), PARE e me peça os dados estruturados.
- **Documentação é Código:** Nenhuma mudança de arquitetura deve ser feita sem antes atualizar este arquivo `CLAUDE.md`.

## 2. Domínio do Problema
O objetivo é simular o conectoma da *Drosophila melanogaster* (como *proxy* metodológico para o *Aedes aegypti*) usando Spiking Neural Networks (SNNs). O sistema simula o cérebro recebendo estímulos virtuais (CO2, Calor) e retorna o padrão de disparo neural.

## 3. Stack Tecnológica
- **Linguagem:** Python 3.11+ (Tipagem estática obrigatória com `mypy`).
- **Engine SNN:** `Brian2` ou `NEST Simulator` (para simulação de neurônios).
- **Manipulação de Dados/Grafos:** `NetworkX` e `Pandas`.
- **APIs de Comunicação:** `FastAPI` (para comunicação entre o Ambiente Virtual e o Simulador).
- **Testes:** `pytest` (Testes unitários no core, testes de integração entre APIs).

## 4. Arquitetura e Responsabilidades
- **`packages/connectome-core`**: Responsável EXCLUSIVO por baixar dados de conectoma (NeuroMorpho/FlyWire), limpar os grafos e converter em Matrizes de Adjacência.
- **`apps/brain-simulator`**: Consome o `connectome-core`. Roda o motor Brian2. Recebe tensores representando cheiro/visão, processa no tempo (ms) e devolve a resposta motora do inseto.
- **`apps/virtual-environment`**: Motor físico simplificado. Envia matrizes de concentração de CO2 para o simulador via API REST/gRPC.

## 5. Variáveis de Ambiente Necessárias (Local)
- `NEUROMORPHO_API_KEY`: Chave para baixar os datasets abertos.
- `SIMULATION_RESOLUTION_MS`: Resolução do tempo da SNN (default: 0.1ms).
- `ENVIRONMENT_API_URL`: "http://localhost:8000"
