"""
Metalloenzyme NDM-1 Active Site Simulator
This module generates the electronic structure representation of the NDM-1 di-Zinc active site.
It leverages PySCF to construct the molecular Hamiltonian and maps it to Pauli strings via Jordan-Wigner.
"""

import numpy as np
import warnings
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

# Simulated PySCF and OpenFermion imports for the IC project structure
try:
    from pyscf import gto, scf, mcscf
    from openfermion.chem import MolecularData
    from openfermionpyscf import run_pyscf
    from openfermion.transforms import get_fermion_operator, jordan_wigner
    HAS_PYSCF = True
except ImportError:
    HAS_PYSCF = False
    warnings.warn("Bibliotecas Químicas (PySCF/OpenFermion) não encontradas. O sistema rodará no modo Mock. Instale-as via WSL2 (Linux) para rodar o hamiltoniano real.")

class NDM1_ActiveSite:
    def __init__(self, use_mock=(not HAS_PYSCF)):
        self.use_mock = use_mock
        self.molecule_coords = self._define_geometry()
        # Redução do Espaço Ativo (Active Space) da NDM-1: 2 Zincos, 1 Oxigênio (ponte), 1 Hidrogênio
        self.basis = 'sto-3g'  # Base mínima para a prova de conceito
        self.multiplicity = 1  # Singlet
        self.charge = 1        # Carga +1 simplificada do núcleo di-Zinco hidróxido
        
    def _define_geometry(self):
        """
        Geometria agressivamente truncada do sítio ativo do NDM-1.
        Distâncias aproximadas em Angstroms para os íons Zn1 e Zn2.
        """
        geometry = [
            ('Zn', (0.000000, 0.000000, 0.000000)),
            ('Zn', (3.800000, 0.000000, 0.000000)),
            ('O',  (1.900000, 1.500000, 0.000000)),
            ('H',  (1.900000, 2.400000, 0.000000))
        ]
        return geometry

    def get_hamiltonian(self):
        """
        Gera o Hamiltoniano Fermiônico e o converte para um Hamiltoniano
        de Qubits (Strings de Pauli) usando a Transformação de Jordan-Wigner.
        """
        if self.use_mock:
            print("\n[Mock] Gerando Hamiltoniano Quântico Falso (Fallback WSL)...")
            return [
                (0.53, "Z0 Z1 Z2"),
                (-0.21, "X0 Y1 Y2"),
                (0.15, "X0 X1 Z2 Z3"),
                (1.20, "Z4 Z5")
            ]
        
        print("\n[PySCF] Construindo o Hamiltoniano Molecular do sítio NDM-1...")
        # 1. Configurar os dados moleculares no OpenFermion
        molecule = MolecularData(
            self.molecule_coords, 
            self.basis, 
            self.multiplicity, 
            self.charge
        )
        
        print("[PySCF] Rodando Hartree-Fock / Extraindo integrais...")
        # 2. Rodar o backend do PySCF para extrair integrais 1-corpo e 2-corpos
        molecule = run_pyscf(molecule, run_scf=True, run_mp2=False, run_cisd=False, run_ccsd=False, run_fci=False)
        
        print("[OpenFermion] Convertendo para Operador Fermiônico...")
        # 3. Extrair os operadores fermiônicos
        # PS: Em uma simulação de scale máximo, faríamos `get_active_space_hamiltonian` aqui.
        fermionic_hamiltonian = get_fermion_operator(molecule.get_molecular_hamiltonian())
        
        print("[OpenFermion] Mapeamento Jordan-Wigner para Qubits (String de Pauli)...")
        # 4. Transformar os férmions (elétrons do zinco) na linguagem do computador quântico
        qubit_hamiltonian = jordan_wigner(fermionic_hamiltonian)
        
        return qubit_hamiltonian

    def get_exact_energy(self, qubit_hamiltonian=None):
        """
        Calcula a energia exata do estado fundamental usando Diagonalização Exata (ED).
        Serve como o 'Gabarito' (Ground Truth) para validar o VQE.
        """
        if self.use_mock:
            # Em modo Mock, a energia de ED é fixada para fins de demonstração
            return -5.6092  # Hartree
            
        print("[ED] Executando Diagonalização Exata para obter Ground Truth...")
        # Nota: O qubit_hamiltonian do OpenFermion pode ser convertido para uma matriz
        # Para sistemas pequenos (< 15 qubits), eigsh do scipy é eficiente.
        from openfermion.linalg import get_sparse_operator
        sparse_mat = get_sparse_operator(qubit_hamiltonian)
        
        # Encontrar o menor autovalor (Ground State)
        evals, _ = eigsh(sparse_mat, k=1, which='SA')
        return evals[0]

if __name__ == "__main__":
    print("--- Inicializando NDM-1 Sítio Ativo Quântico ---")
    site = NDM1_ActiveSite()
    
    print("\n[Geometria da Enzima]")
    for atom, coords in site.molecule_coords:
        print(f"  {atom:2s} : {coords}")
    
    H = site.get_hamiltonian()
    
    print("\n[Validação: Modelo Analítico]")
    e_exact = site.get_exact_energy(H)
    print(f"  Energia Exata (ED): {e_exact:.6f} Hartree")
    
    print("\n[Resultado: Hamiltoniano de Qubits (Amostra)]")
    if site.use_mock:
        for coef, obs in H:
            print(f" {obs:10s} : {coef:+.4f}")
    else:
        print("Hamiltoniano autêntico mapeado com sucesso! (Top 5 termos)")
        print(str(H)[:300] + "\n...")
