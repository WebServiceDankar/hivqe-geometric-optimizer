import pytest
import numpy as np

def test_parse_to_adjacency_matrix_returns_correct_shape_and_values():
    """
    Testa se o parser converte um JSON de grafo num Numpy Array de adjacência (Matriz 3x3).
    Temos 3 neurônios e 2 conexões sinápticas com pesos definidos.
    """
    # Arrange (Preparação)
    # JSON fictício: 3 neurônios (id: 0, 1, 2)
    # Sinapse 1: Neurônio 0 -> Neurônio 1 (peso 0.5)
    # Sinapse 2: Neurônio 1 -> Neurônio 2 (peso 1.2)
    fake_connectome_json = {
        "neurons": [
            {"id": 0, "type": "sensory"},
            {"id": 1, "type": "interneuron"},
            {"id": 2, "type": "motor"}
        ],
        "synapses": [
            {"pre": 0, "post": 1, "weight": 0.5},
            {"pre": 1, "post": 2, "weight": 1.2}
        ]
    }

    # Act (Ação) - Importação e execução propositalmente esperando falha (TDD Fase Red)
    try:
        from graph_parser import parse_to_adjacency_matrix
    except ImportError:
        pytest.fail("O arquivo graph_parser.py e a função parse_to_adjacency_matrix ainda não foram criados! É aqui que sua Fase Vermelha do TDD inicia.")

    adj_matrix = parse_to_adjacency_matrix(fake_connectome_json)

    # Assert (Verificação)
    assert isinstance(adj_matrix, np.ndarray), "O retorno deve ser um Numpy Array"
    assert adj_matrix.shape == (3, 3), f"A matriz deve ser 3x3. Retornou {adj_matrix.shape}"
    
    # Conferindo as sinapses existentes
    assert adj_matrix[0, 1] == 0.5, "Sinapse 0->1 deve ter peso 0.5"
    assert adj_matrix[1, 2] == 1.2, "Sinapse 1->2 deve ter peso 1.2"
    
    # Conferindo conexões inexistentes (devem ser 0)
    assert adj_matrix[0, 0] == 0.0, "Auto-Conexões não especificadas devem ser 0"
    assert adj_matrix[2, 0] == 0.0, "Caminho inverso (2->0) inexistente deve ser 0"
