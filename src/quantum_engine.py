"""
Quantum Engine — Ansatz Ouroboros com Borromean Rings + Golden Ratio.

Responsabilidade:
  - Construir o circuito Ansatz (Rx/Rz + CZ circular).
  - Construir o Hamiltoniano F_μν.
  - Avaliar energia via simulador ou hardware IBM.
  - Gerar parâmetros iniciais via Razão Áurea (Φ).

Referência: CLAUDE.MD → seção "quantum_engine.py"
"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator


# Constante da Razão Áurea
PHI = (1 + np.sqrt(5)) / 2  # ≈ 1.6180339887


class QuantumEngine:
    """
    Motor quântico para avaliação de energia do Ansatz Ouroboros.

    Args:
        num_qubits: Número de qubits do circuito.
        use_real_hardware: Se True, conecta à IBM. Se False, usa simulador local.
    """

    def __init__(self, num_qubits=6, use_real_hardware=False):
        self.num_qubits = num_qubits
        self.use_real_hardware = use_real_hardware
        self.num_parameters = num_qubits * 2  # Rx + Rz por qubit

        self.circuit, self._params = self._build_ansatz()
        self.hamiltonian = self._build_hamiltonian()
        self._estimator = self._setup_estimator()

    def _build_ansatz(self):
        """
        Constrói o circuito Ansatz Ouroboros:
          1. Camada de rotação: Rx(θ) + Rz(θ) em cada qubit.
          2. Camada de emaranhamento circular: CZ entre vizinhos + CZ(last, 0).
        """
        qc = QuantumCircuit(self.num_qubits)
        theta = ParameterVector('θ', self.num_parameters)

        # Camada de rotação parametrizada
        idx = 0
        for i in range(self.num_qubits):
            qc.rx(theta[idx], i)
            idx += 1
            qc.rz(theta[idx], i)
            idx += 1

        qc.barrier()

        # Camada de emaranhamento circular (Borromean Rings)
        for i in range(self.num_qubits - 1):
            qc.cz(i, i + 1)
        qc.cz(self.num_qubits - 1, 0)  # Fecha o anel

        return qc, theta

    def _build_hamiltonian(self):
        """
        Constrói o Hamiltoniano F_μν geometry.
        Termos Z com coef -1.0 e termos X com coef 0.5 para cada qubit.
        """
        pauli_strings = []
        coeffs = []

        for i in range(self.num_qubits):
            # Termo Z
            z_str = ['I'] * self.num_qubits
            z_str[i] = 'Z'
            pauli_strings.append("".join(z_str)[::-1])
            coeffs.append(-1.0)

            # Termo X
            x_str = ['I'] * self.num_qubits
            x_str[i] = 'X'
            pauli_strings.append("".join(x_str)[::-1])
            coeffs.append(0.5)

        return SparsePauliOp(pauli_strings, coeffs)

    def _setup_estimator(self):
        """Configura o estimador (simulador local ou IBM)."""
        if self.use_real_hardware:
            raise NotImplementedError(
                "Hardware real requer configuração de token IBM. "
                "Use use_real_hardware=False para desenvolvimento."
            )
        return StatevectorEstimator()

    def evaluate(self, theta):
        """
        Avalia a energia do Ansatz para um vetor de parâmetros θ.

        Args:
            theta: Array de floats com len == self.num_parameters.

        Returns:
            Energia (float).

        Raises:
            ValueError: Se len(theta) != self.num_parameters.
        """
        theta = np.asarray(theta, dtype=float)

        if len(theta) != self.num_parameters:
            raise ValueError(
                f"Esperados {self.num_parameters} parâmetros, "
                f"recebidos {len(theta)}."
            )

        pub = (self.circuit, self.hamiltonian, theta)
        job = self._estimator.run([pub])
        energy = float(job.result()[0].data.evs)

        return energy

    def golden_ratio_init(self):
        """
        Gera parâmetros iniciais determinísticos via Razão Áurea (Φ).

        Distribui os ângulos usando a sequência de Weyl:
            θ_k = (k * Φ) mod 2π

        Isso cobre o espaço angular de forma quasi-uniforme,
        evitando barren plateaus típicos da inicialização randômica.

        Returns:
            Array de floats com len == self.num_parameters, todos em [0, 2π).
        """
        indices = np.arange(1, self.num_parameters + 1)
        angles = (indices * PHI * 2 * np.pi) % (2 * np.pi)
        return angles
