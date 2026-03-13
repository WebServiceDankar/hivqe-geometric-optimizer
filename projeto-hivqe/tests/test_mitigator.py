"""
Testes do Classical Mitigator — Regressão Linear por Mínimos Quadrados.

Escritos ANTES da implementação (TDD - Red Phase).
Cada teste define o comportamento esperado do módulo classical_mitigator.py.
"""
import unittest
import math


class TestLinearRegression(unittest.TestCase):
    """Testa o cálculo puro de regressão linear (mínimos quadrados)."""

    def test_perfect_linear_returns_r2_one(self):
        """3 pontos perfeitamente colineares → R² = 1.0, SQR ≈ 0."""
        from src.classical_mitigator import compute_regression

        points = [(1, 2), (2, 4), (3, 6)]  # y = 2x
        result = compute_regression(points)

        self.assertAlmostEqual(result["m"], 2.0, places=5)
        self.assertAlmostEqual(result["b"], 0.0, places=5)
        self.assertAlmostEqual(result["R2"], 1.0, places=5)
        self.assertAlmostEqual(result["SQR"], 0.0, places=5)

    def test_negative_slope(self):
        """Pontos com inclinação negativa → m < 0."""
        from src.classical_mitigator import compute_regression

        points = [(1, 9), (2, 7), (3, 5), (4, 3)]  # y = -2x + 11
        result = compute_regression(points)

        self.assertAlmostEqual(result["m"], -2.0, places=5)
        self.assertAlmostEqual(result["b"], 11.0, places=5)
        self.assertAlmostEqual(result["R2"], 1.0, places=5)

    def test_scattered_data_low_r2(self):
        """Dados muito dispersos → R² < 0.5."""
        from src.classical_mitigator import compute_regression

        points = [(1, 8), (2, 2), (3, 7), (4, 1), (5, 9)]
        result = compute_regression(points)

        self.assertLess(result["R2"], 0.5)

    def test_insufficient_points_returns_none(self):
        """Com menos de 2 pontos, não há regressão possível."""
        from src.classical_mitigator import compute_regression

        self.assertIsNone(compute_regression([]))
        self.assertIsNone(compute_regression([(1, 2)]))

    def test_all_same_x_returns_none(self):
        """Todos os x iguais → sXX = 0, não há reta definida."""
        from src.classical_mitigator import compute_regression

        points = [(3, 1), (3, 5), (3, 9)]
        self.assertIsNone(compute_regression(points))

    def test_prediction_at_new_x(self):
        """Prevê y para um x não amostrado usando m e b calculados."""
        from src.classical_mitigator import compute_regression

        points = [(0, 1), (2, 5), (4, 9)]  # y = 2x + 1
        result = compute_regression(points)

        predicted_y = result["m"] * 3 + result["b"]  # x=3 → y=7
        self.assertAlmostEqual(predicted_y, 7.0, places=5)


class TestMitigatorBuffer(unittest.TestCase):
    """Testa o buffer de janela deslizante do Mitigator."""

    def test_buffer_respects_window_size(self):
        """O buffer nunca excede WINDOW_SIZE pontos."""
        from src.classical_mitigator import ClassicalMitigator

        mit = ClassicalMitigator(window_size=3, target_energy=-5.609)
        for i in range(10):
            mit.update(epoch=i + 1, energy_raw=-1.0 - i * 0.5)

        self.assertLessEqual(len(mit.buffer), 3)

    def test_initial_state_not_converged(self):
        """No início, o mitigador reporta não-convergido."""
        from src.classical_mitigator import ClassicalMitigator

        mit = ClassicalMitigator(window_size=5, target_energy=-5.609)
        result = mit.update(epoch=1, energy_raw=-2.0)

        self.assertFalse(result["converged"])

    def test_returns_raw_when_insufficient_data(self):
        """Com menos de 3 pontos no buffer, energy_pred = energy_raw."""
        from src.classical_mitigator import ClassicalMitigator

        mit = ClassicalMitigator(window_size=5, target_energy=-5.609)
        r1 = mit.update(epoch=1, energy_raw=-2.0)
        r2 = mit.update(epoch=2, energy_raw=-3.0)

        self.assertEqual(r1["energy_pred"], -2.0)
        self.assertEqual(r2["energy_pred"], -3.0)


class TestConvergenceDetection(unittest.TestCase):
    """Testa o critério de convergência: |pred - target| < threshold por patience epochs."""

    def test_converges_after_patience_epochs(self):
        """Se a energia fica próxima do target por patience epochs, converged=True."""
        from src.classical_mitigator import ClassicalMitigator

        target = -5.609
        threshold = 0.05
        patience = 3

        mit = ClassicalMitigator(
            window_size=5,
            target_energy=target,
            convergence_threshold=threshold,
            patience=patience,
        )

        # Alimenta pontos que convergem linearmente para o target
        energies = [-5.60, -5.61, -5.608, -5.609, -5.610,
                    -5.609, -5.610, -5.608, -5.609, -5.609]

        last_result = None
        for i, e in enumerate(energies):
            last_result = mit.update(epoch=i + 1, energy_raw=e)

        # Depois de muitos epochs perto do target, deve convergir
        self.assertTrue(last_result["converged"])

    def test_does_not_converge_if_oscillating(self):
        """Se a energia oscila muito, nunca converge."""
        from src.classical_mitigator import ClassicalMitigator

        mit = ClassicalMitigator(
            window_size=5,
            target_energy=-5.609,
            convergence_threshold=0.05,
            patience=5,
        )

        # Energia oscila violentamente
        energies = [-2.0, -5.6, -1.0, -5.5, -3.0, -5.7, -1.5, -5.8]
        last_result = None
        for i, e in enumerate(energies):
            last_result = mit.update(epoch=i + 1, energy_raw=e)

        self.assertFalse(last_result["converged"])


class TestOutputFormat(unittest.TestCase):
    """Garante que o output do mitigador tem todas as chaves necessárias."""

    def test_output_keys(self):
        """O dicionário de saída deve conter todas as chaves documentadas no CLAUDE.MD."""
        from src.classical_mitigator import ClassicalMitigator

        mit = ClassicalMitigator(window_size=5, target_energy=-5.609)

        # Alimenta dados suficientes para ter regressão
        for i in range(5):
            result = mit.update(epoch=i + 1, energy_raw=-1.0 - i)

        required_keys = {"energy_pred", "m", "b", "R2", "converged"}
        self.assertTrue(required_keys.issubset(result.keys()),
                        f"Faltam chaves: {required_keys - result.keys()}")


if __name__ == "__main__":
    unittest.main()
