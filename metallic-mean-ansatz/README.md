# 📐 Metallic Mean Ansatz (MMA)

Investigação de Razões Irracionais em Otimização Quântica Geométrica.

Este projeto propõe um estudo comparativo inédito sobre a influência de constantes matemáticas na arquitetura de circuitos variacionais (Ansatzes). A hipótese central é que a escolha da razão geométrica define a topologia da "paisagem energética", impactando diretamente a velocidade de convergência e a resistência ao ruído.

## 📊 Protocolo Experimental

O objetivo é encontrar qual constante matemática oferece o melhor desempenho para simulação molecular (como no projeto AedesTwin).

| Constante (Símbolo) | Nome Comum | Comportamento Clássico (Controle) | Comportamento Quântico (Predição) | Aplicação Ideal (Recomendação) |
| :--- | :--- | :--- | :--- | :--- |
| $\phi$ (Phi) | Razão Áurea | Estabilidade Máxima. Resistente a ressonâncias. | Lento mas Fiel. Excelente contra ressonâncias de Floquet, mas com mistura de estados lenta. | Conservação de Energia Pura. |
| $\delta_S$ (Delta) | Razão Prateada | Melhor Equilíbrio. | Padrão Ouro 2026. A melhor escolha geral: mistura rápida + alta fidelidade. | Recomendado para Moléculas do Aedes. |
| $\rho$ (Rho) | Número Plástico | Bom para cascata. | Geometric QML. Ideal para circuitos cúbicos (ansatzes profundos) devido à sua propriedade de "empilhamento". | Aprendizado de Máquina Quântico. |
| $e$ | Euler | Rápida. | Sistemas Abertos (NESS). Excelente para simular sistemas quânticos abertos e termodinâmica. | Metrologia Quântica. |
| $5/3$ | Racional Aprox. | Turbulência. | Espectro de Energia. Cria bandas de energia específicas em alta dimensão. | Simulação de Materiais. |
| $L$ | Constante de Liouville | Máxima (Caos). | Instabilidade Total. A decoerência explode rapidamente. | Não recomendado (Apenas Teórico).|

## 🦟 Conectando com o AedesTwin (A Aplicação Real)

Nós temos um objetivo claro para o artigo:
"Usar a Razão Prateada ($\delta_S$) para otimizar a simulação de moléculas repelentes de Dengue, pois a tabela indica que ela oferece o melhor equilíbrio entre velocidade e precisão em hardware ruidoso (NISQ)."

**No código:**
Não usamos um otimizador "mágico". Construímos um Ansatz onde os ângulos de rotação ou as conexões são definidos por essas constantes.

Exemplo: Em vez de conectar o qubit 1 ao 2 aleatoriamente, você conecta seguindo uma proporção de $\delta_S$ (Razão Prateada).
Resultado: O circuito "respira" naturalmente sem travar em mínimos locais.

---
**Resumo do Plano:**
- **Nome:** metallic-mean-ansatz.
- **Objetivo:** Provar que a Razão Prateada é superior à Razão Áurea em VQEs modernos.
- **Aplicação:** Simular moléculas do Aedes.
