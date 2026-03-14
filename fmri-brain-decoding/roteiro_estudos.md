# Roteiro de Pesquisa - Decodificação Cerebral (Revisado)

**Objetivo Geral**
Replicar e evoluir os experimentos de neurociência visual por meio de Mapeamento de Espaço Latente, utilizando Modelos de Difusão e Dados BOLD de alta resolução (fMRI humano).

---

## 🟢 Fase 1: Aquisição e Pré-Processamento (O Gargalo)
*Onde 90% dos projetos travam. Dados de fMRI são sujos e pesados.*

1.  [ ] **Download Seletivo:** Baixar apenas o sujeito `subj01` do **Natural Scenes Dataset (NSD)** para prototipagem rápida (o dataset completo é imenso).
2.  [ ] **Pré-Processamento Crítico:** Utilizar os dados já pré-processados pelo NSD (formato `fsaverage` ou `nativesurface`) para pular a etapa de realinhamento e correção de movimento. *Dica:* Não tente fazer o pré-processamento bruto ("raw fMRI") agora; isso exige ferramentas como FSL/SPM e é um projeto inteiro separado.
3.  [ ] **Máscara de ROI (Region of Interest):** Definir uma máscara para o **Córtex Visual (V1, V2, V4)**. Tentar usar o cérebro inteiro vai gerar um vetor de entrada de 100.000+ dimensões, o que inviabiliza a regressão. Foco na área visual é essencial.

---

## 🟡 Fase 2: O Codificador de Imagem (Ground Truth)
*Transformar imagens em números que o modelo entenda.*

1.  [ ] **Seleção do Modelo CLIP:** Utilizar o `ViT-L/14` (o padrão usado nos papers recentes de alta resolução). Ele gera embeddings mais ricos que o padrão.
2.  [ ] **Pipeline de Embeddings:** Passar as 73.000 imagens (NSD conta repetições) pelo CLIP e salvar os tensores.
    *   *Ajuste:* O shape (768,) está correto para o ViT-L/14, mas verifique se você vai usar o embedding da camada de texto (text encoder) ou da de imagem (image encoder). Para reconstrução visual, usamos o **Image Encoder**.
3.  [ ] **Persistência:** Salvar em formato `.npy` ou `HDF5` para não ter que rodar isso de novo.

---

## 🔴 Fase 3: O "Tradutor" Cérebro-Máquina (O Coração do CI)
*Onde a Ciência de Dados Pura acontece.*

1.  [ ] **Redução de Dimensionalidade (CRUCIAL - Passo Faltante):**
    *   Antes de treinar, aplicar **PCA (Principal Component Analysis)** nos dados BOLD ($X$).
    *   *Por que:* O fMRI tem mais dimensões (voxels) do que amostras (imagens vistas). Sem reduzir dimensões, a regressão Ridge vai sofrer de *overfitting* brutal ou falhar matematicamente. Reduza para ~500-1000 componentes principais.
2.  [ ] **Treinamento Ridge:**
    *   Mapear $X_{reduzido}$ (atividade cerebral) $\rightarrow$ $Y$ (embedding CLIP).
    *   Otimizar o hiperparâmetro $\alpha$ (regularização L2) via Grid Search.
3.  [ ] **Validação:** Usar o conjunto de teste do NSD (imagens que o sujeito viu, mas que não foram treinadas). Métrica: **Cosine Similarity** e **Rank Accuracy** (entre as top-k imagens recuperadas).

---

## 🟣 Fase 4: Engenharia do Stable Diffusion (A Mágica)
*Gerar a imagem a partir da previsão.*

1.  [ ] **Injeção de Latent Code:** O Stable Diffusion funciona num espaço latente comprimido (VAE), não diretamente no espaço do CLIP. Você precisará de um "adapter" ou usar a técnica de **Optimization-based Generation** (otimizar o ruído inicial até que o embedding gerado bata com a previsão cerebral).
2.  [ ] **Decodificação:** Rodar o modelo de difusão (Denoising Loop) condicionado pelo vetor previsto na Fase 3.
3.  [ ] **Benchmarking:**
    *   Comparar a imagem gerada vs. imagem real usando métricas de percepção (LPIPS, SSIM) e não apenas pixel-a-pixel (MSE).
    *   *Correção:* A comparação com "Drosophila ou Gatos" é problemática (são sistemas visuais muito diferentes e modelos antigos). O ideal é comparar com o paper de referência **"High-Resolution Image Reconstruction with Latent Diffusion Models" (Takagi & Nishimoto, 2023)**.

---

### Dica Estratégica para o Artigo
O professor pediu uma aplicação inédita. A maioria dos papers foca em "reconstruir o que a pessoa viu".

**Sua inovação sugerida no e-mail anterior:**
> *"Comparar a eficiência de diferentes estratégias de regressão (Ridge Clássico vs. Regressão Quântica/Variacional) para mapear o sinal BOLD."*

Você pode tentar substituir a **Ridge Regression (Fase 3)** por uma regressão feita via **Quantum Kernel Ridge** (usando Qiskit) e ver se a precisão da reconstrução melhora em amostras pequenas. Isso uniria todos os seus projetos (Quantum + Neurociência + Aedes) de forma elegante.
