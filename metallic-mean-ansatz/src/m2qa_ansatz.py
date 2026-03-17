import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

class M2QA_Ansatz:
    """
    Metallic Mean Quantum Ansatz (M²QA)
    Arquitetura de circuito com entrelacamento Borromeano e 
    inicialização baseada na Razão de Prata (Silver Ratio).
    """
    def __init__(self, n_qubits=6, layers=1):
        self.n_qubits = n_qubits
        self.layers = layers
        self.delta_s = 1 + np.sqrt(2) # Razão de Prata
        
    def generate_silver_angles(self, n_params):
        """
        Gera ângulos baseados na série de Pell: pi / delta_s^k.
        Garante que o otimizador fuja de Barren Plateaus racionais.
        """
        return [np.pi / (self.delta_s**k) for k in range(n_params)]

    def get_initial_params(self):
        """Retorna o vetor de parâmetros inicial para o otimizador."""
        return self.generate_silver_angles(self.n_qubits * self.layers)

    def build_circuit(self, params=None):
        """
        Constrói o circuito quântico (Qiskit).
        Aplica camadas de rotação Ry e o entrelacamento Borromeano cíclico.
        """
        qc = QuantumCircuit(self.n_qubits)
        
        # Se params for None, usamos nomes simbólicos para o Qiskit
        if params is None or isinstance(params[0], (int, float, np.float64, np.float32)) == False:
            theta = ParameterVector('θ', self.n_qubits * self.layers)
        else:
            theta = params

        param_idx = 0
        for l in range(self.layers):
            # 1. Camada de Rotação Ry
            for i in range(self.n_qubits):
                qc.ry(theta[param_idx], i)
                param_idx += 1
            
            # 2. Camada Borromeana (Ciclos de 3-qubits)
            # Conecta (0,1,2), (3,4,5)...
            for i in range(0, self.n_qubits - 2, 3):
                qc.cx(i, i+1)
                qc.cx(i+1, i+2)
                qc.cx(i+2, i)
            
            # Se sobrar qubits (ex: n=4 ou 5), fazemos uma conexão linear residual
            remainder = self.n_qubits % 3
            if remainder != 0 and self.n_qubits > 1:
                last_idx = self.n_qubits - 1
                qc.cx(last_idx - 1, last_idx)

        return qc

if __name__ == "__main__":
    # Demonstração rápida
    ansatz = M2QA_Ansatz(n_qubits=3, layers=1)
    circuit = ansatz.build_circuit()
    print("M²QA Ansatz (Borromean Topology) 3-qubits:")
    print(circuit.draw())
    print("\nParâmetros Iniciais (Silver Ratio):")
    print(ansatz.get_initial_params())
