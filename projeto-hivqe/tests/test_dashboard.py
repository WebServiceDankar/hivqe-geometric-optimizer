"""
Testes do Dashboard — contrato de dados e servidor HTTP.

Escritos ANTES da implementação (TDD).
Focam em garantir que o JSON produzido pelo orchestrator é consumível
pelo frontend, e que o servidor HTTP funciona.
"""
import unittest
import json
import os
import tempfile
import threading
import time
import urllib.request
from unittest.mock import MagicMock


class TestJsonContract(unittest.TestCase):
    """Garante que o JSON do orchestrator tem o formato que o frontend espera."""

    def _run_orchestrator_and_get_json(self):
        """Helper: roda o orchestrator com mock e retorna o JSON gerado."""
        from src.orchestrator import Orchestrator

        tmpdir = tempfile.mkdtemp()
        output_file = os.path.join(tmpdir, "live_data.json")

        mock_engine = MagicMock()
        mock_engine.evaluate.return_value = -4.0
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
            return json.load(f)

    def test_json_has_epochs_array(self):
        """Frontend espera data.epochs como array de inteiros."""
        data = self._run_orchestrator_and_get_json()
        self.assertIsInstance(data["epochs"], list)
        self.assertTrue(all(isinstance(e, int) for e in data["epochs"]))

    def test_json_has_quantum_raw_array_of_floats(self):
        """Frontend espera data.quantum_raw como array de números."""
        data = self._run_orchestrator_and_get_json()
        self.assertIsInstance(data["quantum_raw"], list)
        self.assertTrue(all(isinstance(v, (int, float)) for v in data["quantum_raw"]))

    def test_json_has_classical_pred_array_of_floats(self):
        """Frontend espera data.classical_pred como array de números."""
        data = self._run_orchestrator_and_get_json()
        self.assertIsInstance(data["classical_pred"], list)
        self.assertTrue(all(isinstance(v, (int, float)) for v in data["classical_pred"]))

    def test_json_has_status_string(self):
        """Frontend espera data.status como string."""
        data = self._run_orchestrator_and_get_json()
        self.assertIsInstance(data["status"], str)
        self.assertIn(data["status"], ["rodando", "concluido", "record", "concluido/record"])

    def test_json_arrays_are_same_length(self):
        """Frontend assume que epochs, quantum_raw e classical_pred tem mesmo tamanho."""
        data = self._run_orchestrator_and_get_json()
        n = len(data["epochs"])
        self.assertEqual(len(data["quantum_raw"]), n)
        self.assertEqual(len(data["classical_pred"]), n)

    def test_json_is_valid_utf8(self):
        """O JSON deve ser parseável sem erros."""
        from src.orchestrator import Orchestrator

        tmpdir = tempfile.mkdtemp()
        output_file = os.path.join(tmpdir, "live_data.json")

        mock_engine = MagicMock()
        mock_engine.evaluate.return_value = -3.5
        mock_engine.num_parameters = 12
        mock_engine.golden_ratio_init.return_value = [0.0] * 12

        orch = Orchestrator(
            engine=mock_engine, max_epochs=3,
            target_energy=-5.609, output_path=output_file,
        )
        orch.run()

        with open(output_file, "r", encoding="utf-8") as f:
            raw = f.read()

        # Não deve levantar exceção
        parsed = json.loads(raw)
        self.assertIsNotNone(parsed)


class TestServeModule(unittest.TestCase):
    """Testa que o módulo serve.py é importável e tem a interface esperada."""

    def test_create_server_function_exists(self):
        """serve.py deve expor uma função create_server(port, directory)."""
        from dashboard.serve import create_server
        self.assertTrue(callable(create_server))

    def test_server_starts_and_serves_file(self):
        """O servidor deve conseguir servir um arquivo estático."""
        from dashboard.serve import create_server

        tmpdir = tempfile.mkdtemp()
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("HELLO_TEST")

        server = create_server(port=0, directory=tmpdir)  # porta 0 = OS escolhe
        port = server.server_address[1]

        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            time.sleep(0.3)
            url = f"http://localhost:{port}/test.txt"
            response = urllib.request.urlopen(url, timeout=3)
            content = response.read().decode("utf-8")
            self.assertEqual(content, "HELLO_TEST")
        finally:
            server.shutdown()


if __name__ == "__main__":
    unittest.main()
