# Decodificação Cerebral com fMRI e Stable Diffusion

Este repositório acadêmico contém a pesquisa de recriação de estímulos visuais na mente humana através da tradução de sinais de Ressonância Magnética Funcional (fMRI) na linguagem de IAs Geradoras de Imagens.

O objetivo do projeto é avançar além da clássica e custosa "otimização de pixels" utilizada na neurobiologia inicial. Abordamos a fronteira do estado da arte combinando **Modelos de Difusão** (Stable Diffusion) ao mapeamento de **Espaço Latente** (*Latent Space*).

---

## 🔬 A Arquitetura do Sistema

Em vez de reconstruir a biologia do cérebro para gerar contornos cinzas como fariam as regressões logísticas, esta pesquisa **ensina um modelo a traduzir a atividade cerebral para a "linguagem" (embeddings) de uma inteligência artificial que desenha**.

### Passo 1: O Dataset
Utilizamos sinais BOLD registrados por equipamentos de fMRI humano provenientes do **NSD (Natural Scenes Dataset)**. São matrizes numéricas que relacionam exatamente a atividade neural milimétrica sincronizada à imagem exata (`ground truth`) que a pessoa observava em repouso. 

### Passo 2: O Pipeline (3 Pilares)

1. **O Codificador de Imagem (OpenAI CLIP):** Atua como o nosso validador. Ele não lê cérebros, mas transforma as imagens reais em um *embedding* matemático (um vetor) que consolida o sentido e significado lógico daquela imagem.
2. **O Modelo Ponte (Heart of the Research):** Um modelo de machine learning treinado utilizando os dados fMRI (Input-$X$) e os tensores do CLIP das imagens (Target-$Y$). O objetivo deste modelo de regressão avançada (Ridge Regression / MLP) é que, ao receber um sinal cerebral inédito, consiga prever matematicamente o "vetor de significado".
3. **O Reconstrutor Visual (Stable Diffusion):** O vetor hipotético construído pelo modelo-ponte funciona como um *prompt invisível* e é injetado diretamente na biblioteca visual (Diffusers). O Stable Diffusion irá iterar a reconstrução a partir do espaço latente guiado pelo cérebro do paciente para renderizar o pensamento decodificado.

## 🛠️ Ferramentas & Stack

- **Linguagem Base:** Python 3.10+
- **Deep Learning:** PyTorch (Para retropropagação e manipulação de tensores)
- **Neuroimagem:** NiLearn
- **IA Generativa:** Diffusers (Hugging Face) e Transformers
- **Processamento:** Google Colab Pro com GPU VRAM elevada (A100 / V100) para compilações do gerador visual.

> *Para referência de inspiração bibliográfica, o método se baseia em Takagi & Nishimoto (2023): "High-resolution image reconstruction with latent diffusion models from human brain activity".*
