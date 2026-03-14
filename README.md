<div align="center">
  <img src="./docs/logo_projeto.png" width="250" alt="UNIFEI Logo">
  
  <br><br>
  
  <h1><b>Pesquisas e Projetos UNIFEI<br>Ciência de Dados Aplicada</b></h1>
  
  <p>
    <b>Universidade Federal de Itajubá (UNIFEI)</b><br>
    <i>Repositório Oficial de Pesquisas (Monorepo) — Pesquisador: Daniel A. Palma</i>
  </p>

  <div>
    <img src="https://img.shields.io/badge/Status-Monorepo_Ativo-004d99?style=for-the-badge&logo=github" alt="Status">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/NVIDIA_CUDA--Q-76B900?style=for-the-badge&logo=nvidia&logoColor=white" alt="CUDA-Q">
    <img src="https://img.shields.io/badge/Licen%C3%A7a-MIT-green?style=for-the-badge" alt="License">
  </div>
</div>

---

Bem-vindo ao repositório unificado de pesquisas e projetos acadêmicos associados à Universidade Federal de Itajubá (UNIFEI) na área de Ciência de Dados Aplicada.

Este repositório foi estruturado como um **Monorepo** para agregar múltiplos projetos em um único lugar, mantendo a organização da sua jornada, o histórico do Git e a facilidade de navegação com a estética original.

---

## 📂 Navegação de Projetos

Abaixo estão listados os projetos atuais abrigados neste repositório. Clique no nome do projeto para acessar os seus respectivos códigos, documentações e instruções.

### 1. [Project M²QA: Metallic Mean Quantum Ansatz](./metallic-mean-ansatz/)
Investigação da sinergia entre Topologia Quântica e Teoria dos Números. O projeto propõe um Ansatz híbrido inédito que casa a robustez da **Topologia Borromeana** (estrutura três-partida que protege contra decoerência e ruídos locais) com a eficiência de parametrizações baseadas em **Médias Metálicas** (como a Razão Prateada). Seu principal caso de uso atual aplica esta abordagem na simulação do sítio ativo fortemente correlacionado (di-Zinco) da metaloenzima **NDM-1** para a descoberta de inibidores contra superbactérias.
- **Status:** Validação da Hipótese: Topologia Borromeana + Razão Prateada ($\delta_{S}$) na Simulação de Metaloenzimas 📐
- **Tecnologias:** Python, Qiskit, NVIDIA CUDA-Q, PySCF, SciPy

### 2. [Decodificação Cerebral com fMRI e Stable Diffusion](./fmri-brain-decoding/)
Pesquisa focada na fronteira da visão computacional e neurociência. O projeto utiliza Machine Learning para traduzir atividade cerebral (sinais BOLD captados por ressonância magnética funcional) da visualização humana em representações no espaço latente (CLIP). Em seguida, injeta esses vetores de pensamento como *prompts* num Modelo de Difusão (Stable Diffusion) para reconstruir as imagens geradas pela mente.
- **Status:** Estruturação Inicial / Levantamento de Datasets (NSD) 🧠
- **Tecnologias:** Python, PyTorch, NiLearn, API Diffusers (HuggingFace), Scikit-learn

### 3. [Ouroboros - Criptoanálise Quântica (SHA-256)](./ouroboros-crypto-analysis/)
Sistema híbrido quantum-clássico desenhado para explorar o espaço de *pre-images* em funções hash seguras (SHA-256). A abordagem utiliza circuitos quânticos customizados integrados a um motor de mutação clássico para reduzir exponencialmente o espaço de busca, com testes e mitigação de erros validados na QPU IBM Torino.
- **Status:** Validação de Pre-images / Benchmark no IBM Torino 🔐
- **Tecnologias:** Python, Qiskit, IBM Quantum Runtime, Cryptanalysis

---

<div align="center">
  <i>Projetos mantidos por Daniel A. Palma de maneira isolada (Monorepo) e versionada para o programa acadêmico da UNIFEI.</i>
</div>
