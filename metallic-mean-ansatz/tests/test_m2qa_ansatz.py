import pytest
import numpy as np
from qiskit import QuantumCircuit
# Importaremos o que ainda não existe para forçar o RED
try:
    from src.m2qa_ansatz import M2QA_Ansatz
except ImportError:
    M2QA_Ansatz = None

def test_silver_ratio_mathematics():
    """Valida se a constante de prata e os ângulos iniciais estão corretos."""
    ansatz = M2QA_Ansatz(n_qubits=3)
    # delta_s = 1 + sqrt(2) approx 2.4142
    delta_s = 1 + np.sqrt(2)
    expected_angle_0 = np.pi / (delta_s**0) # pi
    expected_angle_1 = np.pi / (delta_s**1) # pi / 2.414...
    
    angles = ansatz.generate_silver_angles(n_params=2)
    assert np.isclose(angles[0], expected_angle_0)
    assert np.isclose(angles[1], expected_angle_1)

def test_borromean_connectivity():
    """Valida se o circuito possui o entrelacamento tripartite (0-1, 1-2, 2-0)."""
    n_qubits = 3
    ansatz_engine = M2QA_Ansatz(n_qubits=n_qubits)
    qc = ansatz_engine.build_circuit(params=[0,0,0]) # Parâmetros zerados para teste de estrutura
    
    # Extrair as instruções de CNOT do Qiskit
    ops = [op.operation.name for op in qc.data]
    assert 'cx' in ops # cx = cnot no qiskit
    
    # Verificar se temos pelo menos 3 conexões (o ciclo Borromeo)
    cnot_count = ops.count('cx')
    assert cnot_count >= 3

def test_parameter_integrity():
    """Garante que o número de parâmetros bate com n_qubits * n_layers."""
    n_qubits = 6
    layers = 2
    ansatz = M2QA_Ansatz(n_qubits=n_qubits, layers=layers)
    params = ansatz.get_initial_params()
    
    assert len(params) == n_qubits * layers
    # Proibido inicialização aleatória
    assert params[0] != params[1] # Devem ser distintos seguindo a série de Pell
