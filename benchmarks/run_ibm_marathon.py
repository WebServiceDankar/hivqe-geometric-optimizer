# ==============================================================================
# 🌪️ TESTE 2 - A MARATONA: VQE F_mu_nu + TRE (50 ITERAÇÕES REAIS)
# ==============================================================================
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from IPython.display import display, clear_output
import time

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from qiskit.primitives import StatevectorEstimator
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, EstimatorOptions

# ⚙️ CHAVES DA MISSÃO
NUM_QUBITS = 6
USE_REAL_HARDWARE = True
# 🔒 SEGURANÇA: Buscando a chave da variável de ambiente ao invés de fixar no código
API_TOKEN = os.getenv("IBM_QUANTUM_TOKEN", "COLOQUE_SEU_TOKEN_AQUI_SE_RODAR_LOCAL")
MAX_ITERATIONS = 50 # A MARATONA ESTÁ DECLARADA!

class GolemRelativisticMarathon:
    def __init__(self):
        self.num_qubits = NUM_QUBITS
        self.energy_history =[]
        self.iteration_count = 0

        self._setup_backend()
        self.hamiltonian = self._build_f_mu_nu_geometry()
        self.ansatz, self.params = self._build_ouroboros_ansatz()

        print(f"⚙️ Compilando circuito para otimização máxima (Nível 2)...")
        pm = generate_preset_pass_manager(target=self.target_backend, optimization_level=2)
        self.isa_circuit = pm.run(self.ansatz)
        self.isa_hamiltonian = self.hamiltonian.apply_layout(self.isa_circuit.layout)

    def _setup_backend(self):
        if USE_REAL_HARDWARE:
            print(f"🛰️[IBM] Autenticando com nível máximo de acesso...")
            self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=API_TOKEN)

            backend_name_str = 'ibm_torino'

            # Retrieve the BackendV2 object directly
            found_backend_obj = None
            try:
                for b in self.service.backends(operational=True, simulator=False):
                    if b.name == backend_name_str:
                        found_backend_obj = b
                        break
            except Exception as e:
                print(f"⚠️ Erro ao listar backends via service.backends(): {e}. Tentando outra abordagem.")

            if found_backend_obj:
                self.backend = found_backend_obj
                print(f"✅ ALVO IBM TRAVADO: {self.backend.name}")
            else:
                print(f"⚠️ Aviso: Backend '{backend_name_str}' não encontrado ou não operacional via service.backends().")
                raise ValueError(f"Não foi possível obter o objeto BackendV2 para '{backend_name_str}'. Não é possível inicializar EstimatorV2.")

            print(f"🛡️ Filtros Ativos: Mitigação TRE (Lvl 1) + Desacoplamento Dinâmico.")
            options = EstimatorOptions()
            options.resilience_level = 1
            options.dynamical_decoupling.enable = True

            self.estimator = EstimatorV2(mode=self.backend, options=options)
            self.target_backend = self.backend.target

        else:
            self.estimator = StatevectorEstimator()
            from qiskit.providers.fake_provider import GenericBackendV2
            self.backend = GenericBackendV2(num_qubits=self.num_qubits)
            self.target_backend = self.backend.target

    def _build_f_mu_nu_geometry(self):
        pauli_strings = []
        coeffs =[]
        for i in range(self.num_qubits):
            z_string = ['I'] * self.num_qubits
            z_string[i] = 'Z'
            pauli_strings.append("".join(z_string)[::-1])
            coeffs.append(-1.0)

            x_string = ['I'] * self.num_qubits
            x_string[i] = 'X'
            pauli_strings.append("".join(x_string)[::-1])
            coeffs.append(0.5)

        H = SparsePauliOp(pauli_strings, coeffs)
        return H

    def _build_ouroboros_ansatz(self):
        qc = QuantumCircuit(self.num_qubits)
        theta = ParameterVector('θ', self.num_qubits * 2)

        param_idx = 0
        for i in range(self.num_qubits):
            qc.rx(theta[param_idx], i)
            param_idx += 1
            qc.rz(theta[param_idx], i)
            param_idx += 1

        qc.barrier()
        for i in range(self.num_qubits - 1):
            qc.cz(i, i+1)
        qc.cz(self.num_qubits-1, 0)

        return qc, theta

    def _cost_function(self, current_thetas):
        self.iteration_count += 1

        if USE_REAL_HARDWARE:
            print(f"   📡[IBM] Iteração {self.iteration_count}/{MAX_ITERATIONS} na fila...")

        pub = (self.isa_circuit, self.isa_hamiltonian, current_thetas)
        job = self.estimator.run([pub])
        float_energy = float(job.result()[0].data.evs)

        if USE_REAL_HARDWARE:
            print(f"   📥[CPU] Energia recebida: {float_energy:.4f} | Rastreio salvo.")

        self.energy_history.append(float_energy)
        return float_energy

    def run(self):
        print("\n" + "="*60)
        backend_display_name = self.backend.name if hasattr(self.backend, 'name') else str(self.backend)
        print(f"🔥 INICIANDO MARATONA DE 50 ITERAÇÕES ({backend_display_name})")
        print("Prepare o café. O hardware será levado ao limite físico.")
        print("="*60)

        initial_guess = np.random.uniform(0, np.pi, len(self.params))
        start_time = time.time()

        if USE_REAL_HARDWARE:
            result = minimize(
                self._cost_function,
                initial_guess,
                method='COBYLA',
                options={'maxiter': MAX_ITERATIONS}
            )

            elapsed = time.time() - start_time

            clear_output(wait=True)
            plt.figure(figsize=(12, 6))
            plt.plot(self.energy_history, color='#00ffcc', linewidth=2.0, marker='o', markersize=5, markerfacecolor='#ff00ff')

            plt.title('VQE Marathon: Ouroboros vs F_μν (50 Epochs / Real Hardware)', fontsize=16, color='white', pad=15)
            plt.xlabel('Epochs (Iterações do SciPy)', fontsize=13, color='white')
            plt.ylabel('Energy (Entropia Mitigada)', fontsize=13, color='white')
            plt.grid(color='#444444', linestyle='--', linewidth=0.5)

            ax = plt.gca()
            ax.set_facecolor('#0a0a0a')
            plt.gcf().patch.set_facecolor('#000000')
            ax.tick_params(colors='white')

            min_energy = min(self.energy_history)
            min_index = self.energy_history.index(min_energy)
            plt.annotate(f'Ground State Alcançado:\n{min_energy:.3f}',
                         xy=(min_index, min_energy), xytext=(min_index, min_energy + 1.5),
                         arrowprops=dict(facecolor='yellow', shrink=0.05),
                         color='yellow', fontsize=11, fontweight='bold', ha='center')

            # Salva o gráfico automaticamente na pasta results do repositório
            os.makedirs(os.path.join(os.path.dirname(__file__), "..", "results"), exist_ok=True)
            plt.savefig(os.path.join(os.path.dirname(__file__), "..", "results", "maratona_ouroboros_ibm.png"), dpi=300, bbox_inches='tight')
            
            plt.show()
        else:
            print("Configure USE_REAL_HARDWARE = True para rodar esta maratona na IBM!")
            return

        print("\n" + "="*60)
        print("🏁 MARATONA CONCLUÍDA COM SUCESSO!")
        print(f"⏱️ Tempo Total de Hardware: {elapsed/60:.2f} minutos")
        print(f"📉 Fundo do Poço Absoluto (Menor Energia): {min_energy:.5f}")
        print("="*60)

if __name__ == "__main__":
    marathon = GolemRelativisticMarathon()
    marathon.run()
