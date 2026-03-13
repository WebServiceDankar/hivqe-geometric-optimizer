"""
Script de execução rápida: gera dados de simulação e inicia o dashboard.
Usa mock do engine para não depender do Qiskit (rápido).
"""
import sys
import os
import threading
import time
import random
import json

# Garantir que importamos do src/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.classical_mitigator import ClassicalMitigator
from dashboard.serve import create_server


def simulate_and_serve():
    """Simula o pipeline híbrido E serve o dashboard ao mesmo tempo."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, "results", "live_data.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Inicializa JSON vazio
    with open(output_path, "w") as f:
        json.dump({"status": "aguardando", "epochs": [], "quantum_raw": [],
                    "classical_pred": [], "stats": {}, "config": {"target": -5.609}}, f)

    # Sobe o servidor HTTP
    server = create_server(port=8081, directory=project_root)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Dashboard: http://localhost:8081/dashboard/index.html")

    time.sleep(1)

    # Simula o pipeline
    target = -5.609
    mitigator = ClassicalMitigator(window_size=5, target_energy=target,
                                    convergence_threshold=0.05, patience=5)
    energy_raw = -1.5
    data = {"status": "rodando", "epochs": [], "quantum_raw": [],
            "classical_pred": [], "stats": {}, "config": {"target": target, "max_epochs": 60}}

    print("Iniciando simulação híbrida...")

    for epoch in range(1, 61):
        # Simula QPU (descida + ruído)
        step = abs(target - energy_raw) * 0.18
        noise = random.uniform(-0.35, 0.35)
        energy_raw -= step
        energy_raw += noise
        if energy_raw < target:
            energy_raw = target + random.uniform(-0.05, 0.05)

        result = mitigator.update(epoch=epoch, energy_raw=energy_raw)

        data["epochs"].append(epoch)
        data["quantum_raw"].append(round(energy_raw, 4))
        data["classical_pred"].append(round(result["energy_pred"], 4))
        data["stats"] = {"m": round(result["m"], 6), "b": round(result["b"], 4),
                         "R2": round(result["R2"], 4)}

        if result["converged"]:
            data["status"] = "record"
            with open(output_path, "w") as f:
                json.dump(data, f)
            print(f"  RECORDE na iteração {epoch}!")
            break

        with open(output_path, "w") as f:
            json.dump(data, f)

        time.sleep(0.35)

    if data["status"] != "record":
        data["status"] = "concluido"
        with open(output_path, "w") as f:
            json.dump(data, f)

    print("Simulação concluída. Dashboard continua ativo.")
    print("Ctrl+C para parar.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    simulate_and_serve()
