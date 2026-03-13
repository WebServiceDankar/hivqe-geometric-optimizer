"""
Testes do Quantum Engine — Ansatz Ouroboros com Borromean Rings.

Escritos ANTES da implementação (TDD - Red Phase).
Focam na construção correta do circuito e na interface de avaliação.

NOTA: Estes testes usam SOMENTE o simulador (StatevectorEstimator).
      Não exigem token IBM nem acesso à rede.
"""
import unittest
import numpy as np


class TestAnsatzConstruction(unittest.TestCase):
    """Testa a construção do circuito Ansatz Ouroboros."""

    def test_circuit_has_correct_num_qubits(self):
        """O circuito deve ter exatamente NUM_QUBITS qubits."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)
        self.assertEqual(engine.circuit.num_qubits, 6)

    def test_circuit_has_correct_num_parameters(self):
        """O Ansatz Ouroboros usa 2 parâmetros por qubit (Rx + Rz)."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)
        # 6 qubits × 2 rotações = 12 parâmetros
        self.assertEqual(engine.num_parameters, 12)

    def test_circuit_has_entanglement_gates(self):
        """O circuito deve conter portas CZ para emaranhamento circular (Borromeo)."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)
        gate_names = [instr.operation.name for instr in engine.circuit.data]

        self.assertIn("cz", gate_names, "Circuito não contém portas CZ de emaranhamento")

    def test_entanglement_is_circular(self):
        """O último qubit deve estar conectado ao primeiro (anel fechado)."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=4, use_real_hardware=False)

        cz_pairs = []
        for instr in engine.circuit.data:
            if instr.operation.name == "cz":
                qubits = [q._index for q in instr.qubits]
                cz_pairs.append(tuple(qubits))

        # Para 4 qubits, esperamos CZ em: (0,1), (1,2), (2,3), (3,0)
        self.assertIn((3, 0), cz_pairs,
                      f"Emaranhamento circular ausente. Pares CZ encontrados: {cz_pairs}")


class TestHamiltonianConstruction(unittest.TestCase):
    """Testa a construção do Hamiltoniano F_μν."""

    def test_hamiltonian_is_not_none(self):
        """O hamiltoniano deve ser construído com sucesso."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)
        self.assertIsNotNone(engine.hamiltonian)

    def test_hamiltonian_has_correct_num_qubits(self):
        """O hamiltoniano deve operar no mesmo número de qubits do circuito."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)
        self.assertEqual(engine.hamiltonian.num_qubits, 6)


class TestEnergyEvaluation(unittest.TestCase):
    """Testa a avaliação de energia via simulador (sem IBM)."""

    def test_evaluate_returns_float(self):
        """A avaliação deve retornar um float (energia)."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)
        theta = np.random.uniform(0, np.pi, engine.num_parameters)
        energy = engine.evaluate(theta)

        self.assertIsInstance(energy, float)

    def test_evaluate_returns_finite_value(self):
        """A energia retornada nunca deve ser NaN ou Inf."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)
        theta = np.random.uniform(0, np.pi, engine.num_parameters)
        energy = engine.evaluate(theta)

        self.assertTrue(np.isfinite(energy), f"Energia não-finita: {energy}")

    def test_different_thetas_give_different_energies(self):
        """Parâmetros θ distintos devem (em geral) produzir energias distintas."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)

        theta_a = np.zeros(engine.num_parameters)
        theta_b = np.ones(engine.num_parameters) * np.pi / 2

        e_a = engine.evaluate(theta_a)
        e_b = engine.evaluate(theta_b)

        self.assertNotAlmostEqual(e_a, e_b, places=3,
                                  msg="Duas configurações θ muito diferentes deram a mesma energia")

    def test_evaluate_with_wrong_param_count_raises(self):
        """Passar θ com tamanho errado deve levantar exceção."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)
        wrong_theta = np.array([0.1, 0.2])  # Apenas 2 params, deveria ser 12

        with self.assertRaises(ValueError):
            engine.evaluate(wrong_theta)


class TestGoldenRatioInitialization(unittest.TestCase):
    """Testa a geração de parâmetros iniciais via Razão Áurea (Φ)."""

    def test_golden_ratio_params_has_correct_length(self):
        """O vetor de ângulos iniciais tem tamanho == num_parameters."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)
        theta_0 = engine.golden_ratio_init()

        self.assertEqual(len(theta_0), engine.num_parameters)

    def test_golden_ratio_params_within_range(self):
        """Todos os ângulos devem estar em [0, 2π)."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)
        theta_0 = engine.golden_ratio_init()

        for angle in theta_0:
            self.assertGreaterEqual(angle, 0)
            self.assertLess(angle, 2 * np.pi)

    def test_golden_ratio_params_are_deterministic(self):
        """A mesma engine deve produzir os mesmos ângulos iniciais (são determinísticos)."""
        from src.quantum_engine import QuantumEngine

        engine = QuantumEngine(num_qubits=6, use_real_hardware=False)
        t1 = engine.golden_ratio_init()
        t2 = engine.golden_ratio_init()

        np.testing.assert_array_equal(t1, t2)


if __name__ == "__main__":
    unittest.main()
