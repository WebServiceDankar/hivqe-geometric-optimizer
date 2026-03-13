# Roteiro de Pesquisa e Metodologia - Decodificação Cerebral

**Objetivo Geral**
Replicar e evoluir os experimentos de neurociência visual por meio de Mapeamento de Espaço Latente, utilizando Modelos de Difusão e Dados BOLD de alta resolução (fMRI humano).

## Fase 1: Aquisição e Entendimento dos Dados
1. [ ] Explorar o ecosistema do **Natural Scenes Dataset (NSD)**.
2. [ ] Revisar conceitos de tensores BOLD e padronizar resoluções tridimensionais voxel-a-voxel pelo banco de dados público da *Kamitami Lab*.
3. [ ] Construir o pipeline básico com `nibabel` e `nilearn` para visualização das fatias corticais brutas.

## Fase 2: O Codificador de Imagem (Features Visuals)
1. [ ] Instalar as instâncias do CLIP da OpenAI localmente via `transformers`.
2. [ ] Passar as 72.000 imagens `ground-truth` que as cobaias observaram pelo CLIP.
3. [ ] Exportar e persisir o vetor-latente (Embedding do Significado) com Shape (768,) para uso no target $Y$.

## Fase 3: Treinamento e Predição Ridge (O Modelo de Tradução Cerebro-Máquina)
1. [ ] Treinar um Scikit-learn regressão robusta de regularização (Ridge Regression) e L2 penalty mapeando BOLD ($X$) -> Embedding do CLIP ($Y$).
2. [ ] Validar generalização aplicando os dados retidos de fMRI a imagens nunca antes vistas pelo modelo (Cross Validation K-Fold).
3. [ ] Avaliar distâncias angulares do cálculo Cosine Similarity.

## Fase 4: Engenharia do Stable Diffusion (Brain to Prompt)
1. [ ] Alimentar os condicionamentos com a predição cerebral (em vez do input de texto em `HuggingFace pipelines`).
2. [ ] Renderizar e estabilizar as imagens com alta resolução e baixa latência computacional.
3. [ ] Fazer benchmarking da acurácia e perda de similaridade em relação à Otimização Clássica de Pixels da *Drosophila* ou Gatos.
