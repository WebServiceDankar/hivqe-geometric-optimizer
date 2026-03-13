import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.classical_mitigator import compute_regression, ClassicalMitigator

# Teste 1: Regressão perfeita
r = compute_regression([(1,2),(2,4),(3,6)])
print(f"Test 1 (perfect linear): m={r['m']:.3f} b={r['b']:.3f} R2={r['R2']:.3f} -> {'PASS' if abs(r['m']-2.0)<0.001 and abs(r['R2']-1.0)<0.001 else 'FAIL'}")

# Teste 2: Negativo
r = compute_regression([(1,9),(2,7),(3,5),(4,3)])
print(f"Test 2 (negative slope): m={r['m']:.3f} b={r['b']:.3f} -> {'PASS' if abs(r['m']+2.0)<0.001 else 'FAIL'}")

# Teste 3: Insuficiente
r = compute_regression([(1,2)])
print(f"Test 3 (insufficient): {r} -> {'PASS' if r is None else 'FAIL'}")

# Teste 4: x iguais
r = compute_regression([(3,1),(3,5),(3,9)])
print(f"Test 4 (same x): {r} -> {'PASS' if r is None else 'FAIL'}")

# Teste 5: Buffer
mit = ClassicalMitigator(window_size=3, target_energy=-5.609)
for i in range(10):
    mit.update(epoch=i+1, energy_raw=-1.0-i*0.5)
print(f"Test 5 (buffer size): {len(mit.buffer)} -> {'PASS' if len(mit.buffer)<=3 else 'FAIL'}")

# Teste 6: Convergencia
mit2 = ClassicalMitigator(window_size=5, target_energy=-5.609, convergence_threshold=0.05, patience=3)
energies = [-5.60, -5.61, -5.608, -5.609, -5.610, -5.609, -5.610, -5.608, -5.609, -5.609]
last = None
for i, e in enumerate(energies):
    last = mit2.update(epoch=i+1, energy_raw=e)
print(f"Test 6 (convergence): converged={last['converged']} -> {'PASS' if last['converged'] else 'FAIL'}")

# Teste 7: Output keys
mit3 = ClassicalMitigator(window_size=5, target_energy=-5.609)
for i in range(5):
    result = mit3.update(epoch=i+1, energy_raw=-1.0-i)
required = {"energy_pred","m","b","R2","converged"}
print(f"Test 7 (keys): {required.issubset(result.keys())} -> {'PASS' if required.issubset(result.keys()) else 'FAIL'}")

print("\nDone!")
