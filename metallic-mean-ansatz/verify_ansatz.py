import sys
import os
sys.path.append(os.path.abspath('src'))
from m2qa_ansatz import M2QA_Ansatz
import numpy as np

print("Iniciando verificação manual de lógica...")
ansatz = M2QA_Ansatz(n_qubits=3)
delta_s = 1 + np.sqrt(2)
angles = ansatz.generate_silver_angles(n_params=2)
print(f"Ângulos gerados: {angles}")
expected = [np.pi, np.pi/delta_s]
print(f"Esperado: {expected}")
if np.allclose(angles, expected):
    print("MATEMÁTICA: OK")
else:
    print("MATEMÁTICA: FALHA")

print("Construindo circuito...")
qc = ansatz.build_circuit()
print("Circuito construído com sucesso!")
print(qc.draw())
