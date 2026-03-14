"""
Orchestrator — Loop híbrido Quantum/Classical.

Responsabilidade:
  - Executar o ciclo Engine → Mitigator → JSON → Convergência.
  - Salvar dados em live_data.json a cada iteração.
  - Parar quando convergência detectada ou max_epochs atingido.

Referência: CLAUDE.MD → seção "orchestrator.py"
"""
import json
import os

from src.classical_mitigator import ClassicalMitigator


class Orchestrator:
    """
    Orquestra o pipeline híbrido quantum-clássico.

    Args:
        engine: Instância de QuantumEngine (ou mock com .evaluate() e .golden_ratio_init()).
        max_epochs: Número máximo de iterações.
        target_energy: Energia alvo (ground state).
        output_path: Caminho para o arquivo JSON de saída.
        convergence_threshold: Erro máximo aceitável para convergência.
        patience: Epochs consecutivos abaixo do threshold para declarar convergência.
        delay: Segundos entre iterações (0 para testes).
    """

    def __init__(self, engine, max_epochs, target_energy, output_path,
                 convergence_threshold=0.05, patience=5, delay=0):

        if max_epochs <= 0:
            raise ValueError(f"max_epochs deve ser > 0, recebido: {max_epochs}")
        if patience < 1:
            raise ValueError(f"patience deve ser >= 1, recebido: {patience}")

        self.engine = engine
        self.max_epochs = max_epochs
        self.target_energy = target_energy
        self.output_path = output_path
        self.convergence_threshold = convergence_threshold
        self.patience = patience
        self.delay = delay

        self.mitigator = ClassicalMitigator(
            window_size=5,
            target_energy=target_energy,
            convergence_threshold=convergence_threshold,
            patience=patience,
        )

        # Estado interno
        self._theta = None
        self._data = {
            "status": "rodando",
            "config": {
                "target": target_energy,
                "max_epochs": max_epochs,
            },
            "epochs": [],
            "quantum_raw": [],
            "classical_pred": [],
            "stats": {"m": 0, "b": 0, "R2": 0},
        }

    def _save(self):
        """Salva o estado atual no arquivo JSON."""
        os.makedirs(os.path.dirname(self.output_path) or ".", exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f)

    def run(self):
        """
        Executa o loop híbrido principal.

        Ciclo por epoch:
          1. Avalia circuito no engine → energia bruta.
          2. Passa pelo mitigator → energia predita + convergência.
          3. Salva JSON.
          4. Para se convergiu ou atingiu max_epochs.
        """
        # Inicializa parâmetros θ via Golden Ratio
        self._theta = self.engine.golden_ratio_init()

        for epoch in range(1, self.max_epochs + 1):
            # 1. Quantum Engine: avaliar energia bruta
            energy_raw = self.engine.evaluate(self._theta)

            # 2. Classical Mitigator: filtrar e verificar convergência
            mit_result = self.mitigator.update(epoch=epoch, energy_raw=energy_raw)

            # 3. Armazenar dados
            self._data["epochs"].append(epoch)
            self._data["quantum_raw"].append(round(energy_raw, 4))
            self._data["classical_pred"].append(round(mit_result["energy_pred"], 4))
            self._data["stats"] = {
                "m": round(mit_result["m"], 6),
                "b": round(mit_result["b"], 6),
                "R2": round(mit_result["R2"], 6),
            }

            # 4. Verificar convergência
            if mit_result["converged"]:
                self._data["status"] = "record"
                self._save()
                break

            # 5. Salvar progresso
            self._save()

            # 6. Delay (0 em testes)
            if self.delay > 0:
                import time
                time.sleep(self.delay)

        else:
            # Loop terminou sem convergência
            self._data["status"] = "concluido"
            self._save()
