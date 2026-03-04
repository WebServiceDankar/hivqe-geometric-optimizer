Otimização Topológica de VQE via Razão Áurea e Anéis de Borromeo
StatusLinguagemFramework

Autor:Daniel A. Palma Orientador/Coordenador: Prof. Dr. Matheus BrendonInstituição: UNIFEI - Curso de Ciências de Dados Aplicada

📝 Resumo do Projeto
Este projeto de pesquisa propõe uma abordagem inovadora para resolver o problema de lentidão na convergência do algoritmo HiVQE (Hardware-efficient Variational Quantum Eigensolver), o atual estado da arte em computação quântica.

Enquanto os métodos tradicionais sofrem com a inicialização randômica (que gera desperdício computacional) e emaranhamento linear (pouco robusto), esta proposta utiliza constantess matemáticas da natureza e topologias complexas para otimizar o processo.

🎯 Objetivos
Objetivo Geral
Demonstrar que a utilização de topologias não-orientáveis e inicialização determinística pode reduzir o uso de hardware quântico em mais de 50% em comparação ao HiVQE padrão.

Objetivos Específicos
Implementar um circuito de emaranhamento baseado em Anéis de Borromeo utilizando portas de Clifford.
Substituir a inicialização randômica por uma estratégia baseada na Razão Áurea (Phi).
Simular os circuitos via NVIDIA CUDA-Q para validar a eficiência e tempo de convergência.
Comparar os resultados com o modelo HiVQE tradicional (benchmark).
💡 Fundamentação Teórica (A Lógica)
Para o detalhamento técnico completo, consulte a pasta /docs.

O Problema (Estado da Arte)
O HiVQE atual funciona como um "tiro no escuro":

Inicialização Randômica: O algoritmo começa com chutes aleatórios, desperdiçando ciclos de processamento.
Emaranhamento Linear: Conexões em linha reta são frágeis e propensas a demorar na convergência.
A Solução Proposta
Topologia de Borromeo: Estrutura geométrica onde a remoção de um elo rompe o todo. Isso força o sistema quântico a uma coerência mais robusta e rápida.
Razão Áurea: O uso da proporção natural (1.618...) oferece um ponto de partida otimizado, reduzindo o espaço de busca do algoritmo.
🛠️ Metodologia e Ferramentas
Simulação: NVIDIA CUDA-Q (Integração GPU/QPU).
Matemática: Geometria pura aplicada a portas lógicas quânticas.
Linguagem: Python 3.x.
📁 Estrutura do Repositório
/
├── src/ # Código fonte (Circuitos, Funções de Inicialização)
├── results/ # Gráficos e dados comparativos de convergência
├── docs/ # Artigos, relatórios e slides acadêmicos
├── benchmarks/ # Comparação entre HiVQE tradicional vs. Modelo Proposto
└── README.md # Este arquivo


