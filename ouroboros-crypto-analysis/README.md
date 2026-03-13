# 🔐 Ouroboros - Criptoanálise Quântica (SHA-256)

Este diretório abriga a pesquisa focada em vulnerabilidades criptográficas utilizando computação híbrida quantum-clássica. O projeto Ouroboros representa uma aplicação prática de circuitos não triviais para tentar estreitar o espaço de busca na quebra da função de hash seguro **SHA-256**.

## 📌 Contexto da Pesquisa

A premissa do Ouroboros envolve utilizar processadores quânticos baseados em chips supercondutores (especificamente os da topologia *Eagle/Heron* da IBM) para preparar estados correlacionados e gerar *human-readable shadows* ("sombras" de dados). Essas assinaturas probabilísticas, após uma rigorosa mitigação de erros (Error Mitigation), alimentam um motor de mutação computacional clássico.

### Objetivos

- Avaliar e validar a topologia de circuitos **Scout Pentagram** desenhados para capturar dependências de bits da codificação do SHA-256.
- Desenvolver rotinas de mitigação clássicas baseadas nos níveis de ruído dos backends reais da **IBM Quantum** (como o *ibm_torino*).
- Reduzir matematicamente a complexidade exponencial da descoberta de uma *pre-image* original.

## 🛠 Modelagem Inicial

A estrutura atual conta com testes de circuitos em simulação estatística utilizando:
- **Qiskit SDK** para modelagem de portas.
- **Python / NumPy** para processamento clássico da mutação de strings e força-bruta local guiada.

*Consulte a documentação secundária para conferir o roteiro de execução e os diários de logs de compilação dos testes nos Dataframes locais.*
