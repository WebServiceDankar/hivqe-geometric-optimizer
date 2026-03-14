"""
Testes do Orchestrator — Loop híbrido Quantum/Classical.

Escritos ANTES da implementação (TDD - Red Phase).
Testam o ciclo completo: Engine → Mitigator → JSON → Convergência.

NOTA: Usam mocks para isolar o Orchestrator dos módulos reais.
"""
import unittest
import json
import os
import tempfile
from unittest.mock import MagicMock, patch


class TestOrchestratorLoop(unittest.TestCase):
    """Testa o loop principal do Orchestrator."""

    def test_runs_until_max_epochs(self):
        """Se não há convergência, o loop deve parar em max_epochs."""
        from src.orchestrator import Orchestrator

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "live_data.json")

            # Mock do engine que retorna energia constante (nunca converge)
            mock_engine = MagicMock()
            mock_engine.evaluate.return_value = -2.0
            mock_engine.num_parameters = 12
            mock_engine.golden_ratio_init.return_value = [0.0] * 12

            orch = Orchestrator(
                engine=mock_engine,
                max_epochs=10,
                target_energy=-5.609,
                output_path=output_file,
            )
            orch.run()

            with open(output_file, "r") as f:
                data = json.load(f)

            self.assertEqual(len(data["epochs"]), 10)

    def test_stops_early_on_convergence(self):
        """Se converge, deve parar antes de max_epochs."""
        from src.orchestrator import Orchestrator

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "live_data.json")

            # Mock que retorna energia muito próxima do target desde o início
            mock_engine = MagicMock()
            mock_engine.evaluate.return_value = -5.609
            mock_engine.num_parameters = 12
            mock_engine.golden_ratio_init.return_value = [0.0] * 12

            orch = Orchestrator(
                engine=mock_engine,
                max_epochs=60,
                target_energy=-5.609,
                output_path=output_file,
                convergence_threshold=0.05,
                patience=3,
            )
            orch.run()

            with open(output_file, "r") as f:
                data = json.load(f)

            # Deve ter parado BEM antes de 60
            self.assertLess(len(data["epochs"]), 60)

    def test_output_json_has_required_structure(self):
        """O arquivo JSON gerado deve conter todas as chaves documentadas no CLAUDE.MD."""
        from src.orchestrator import Orchestrator

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "live_data.json")

            mock_engine = MagicMock()
            mock_engine.evaluate.return_value = -3.0
            mock_engine.num_parameters = 12
            mock_engine.golden_ratio_init.return_value = [0.0] * 12

            orch = Orchestrator(
                engine=mock_engine,
                max_epochs=5,
                target_energy=-5.609,
                output_path=output_file,
            )
            orch.run()

            with open(output_file, "r") as f:
                data = json.load(f)

            required_keys = {"status", "epochs", "quantum_raw", "classical_pred"}
            self.assertTrue(required_keys.issubset(data.keys()),
                            f"JSON incompleto. Chaves presentes: {data.keys()}")

    def test_epochs_and_energies_have_same_length(self):
        """Os arrays epochs, quantum_raw e classical_pred devem ter mesmo tamanho."""
        from src.orchestrator import Orchestrator

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "live_data.json")

            mock_engine = MagicMock()
            mock_engine.evaluate.return_value = -4.0
            mock_engine.num_parameters = 12
            mock_engine.golden_ratio_init.return_value = [0.0] * 12

            orch = Orchestrator(
                engine=mock_engine,
                max_epochs=8,
                target_energy=-5.609,
                output_path=output_file,
            )
            orch.run()

            with open(output_file, "r") as f:
                data = json.load(f)

            n = len(data["epochs"])
            self.assertEqual(len(data["quantum_raw"]), n)
            self.assertEqual(len(data["classical_pred"]), n)

    def test_status_is_record_when_converged(self):
        """Se convergiu, o status final deve ser 'record'."""
        from src.orchestrator import Orchestrator

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "live_data.json")

            mock_engine = MagicMock()
            mock_engine.evaluate.return_value = -5.610   # Muito perto do target
            mock_engine.num_parameters = 12
            mock_engine.golden_ratio_init.return_value = [0.0] * 12

            orch = Orchestrator(
                engine=mock_engine,
                max_epochs=60,
                target_energy=-5.609,
                output_path=output_file,
                convergence_threshold=0.05,
                patience=3,
            )
            orch.run()

            with open(output_file, "r") as f:
                data = json.load(f)

            self.assertIn(data["status"], ["record", "concluido/record"])


class TestOrchestratorConfig(unittest.TestCase):
    """Testa as configurações do Orchestrator."""

    def test_rejects_invalid_max_epochs(self):
        """max_epochs <= 0 deve levantar ValueError."""
        from src.orchestrator import Orchestrator

        mock_engine = MagicMock()
        mock_engine.num_parameters = 12
        mock_engine.golden_ratio_init.return_value = [0.0] * 12

        with self.assertRaises(ValueError):
            Orchestrator(
                engine=mock_engine,
                max_epochs=0,
                target_energy=-5.609,
                output_path="/tmp/test.json",
            )

    def test_rejects_negative_patience(self):
        """patience < 1 deve levantar ValueError."""
        from src.orchestrator import Orchestrator

        mock_engine = MagicMock()
        mock_engine.num_parameters = 12
        mock_engine.golden_ratio_init.return_value = [0.0] * 12

        with self.assertRaises(ValueError):
            Orchestrator(
                engine=mock_engine,
                max_epochs=10,
                target_energy=-5.609,
                output_path="/tmp/test.json",
                patience=0,
            )


if __name__ == "__main__":
    unittest.main()
