"""
Thermodynamic Turing Machine (TTM) - Módulo Base

Implementação de um simulador de Annealing Quântico para validação
da hipótese termodinâmica de que P ≠ NP.

Baseado no Modelo de Ising Transverso:
    H(s) = (1-s) * H_driver + s * H_problem

Onde:
    H_driver = -Σ σx_i  (campo transverso)
    H_problem = Σ J_ij σz_i σz_j + Σ h_i σz_i  (Hamiltoniano de Ising)

Referências:
    - Farhi et al., "Quantum Computation by Adiabatic Evolution" (2000)
    - Altshuler et al., "Anderson localization makes adiabatic quantum optimization fail" (2010)

Author: Douglas H. M. Fulber
"""

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as sla
from dataclasses import dataclass
from typing import Tuple, List, Optional


@dataclass
class ThermodynamicSimulation:
    """
    Simulador de Annealing Quântico para validação de hipóteses P≠NP.
    
    Attributes:
        N: Número de qubits/spins
        J: Matriz de acoplamento N×N (o problema NP codificado)
        h: Vetor de campos locais (bias)
    """
    N: int
    J: np.ndarray
    h: np.ndarray
    
    def __post_init__(self):
        """Inicializa os Hamiltonianos após a criação do objeto."""
        self.dim = 2 ** self.N
        
        # Construção dos operadores de Pauli no espaço de Hilbert total
        self.sigma_x = [self._build_pauli('x', i) for i in range(self.N)]
        self.sigma_z = [self._build_pauli('z', i) for i in range(self.N)]
        
        # Hamiltoniano Driver (Campo Transverso - "Energia Cinética Lógica")
        # H_driver = -Σ σx_i
        self.H_driver = sum([-1.0 * sx for sx in self.sigma_x])
        
        # Hamiltoniano do Problema (Ising - "Energia Potencial Lógica")
        # H_problem = Σ J_ij σz_i σz_j + Σ h_i σz_i
        self.H_problem = sparse.csr_matrix((self.dim, self.dim), dtype=np.float64)
        
        # Termos de interação de dois corpos
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if self.J[i, j] != 0:
                    self.H_problem += self.J[i, j] * (self.sigma_z[i] @ self.sigma_z[j])
        
        # Termos de campo local (um corpo)
        for i in range(self.N):
            if self.h[i] != 0:
                self.H_problem += self.h[i] * self.sigma_z[i]
    
    def _build_pauli(self, axis: str, idx: int) -> sparse.csr_matrix:
        """
        Constrói operador de Pauli para o qubit `idx` no espaço de Hilbert total.
        
        Args:
            axis: 'x' para σx ou 'z' para σz
            idx: Índice do qubit (0 a N-1)
        
        Returns:
            Matriz esparsa 2^N × 2^N representando σ_axis no qubit idx
        """
        I = sparse.eye(2, format='csr')
        X = sparse.csr_matrix([[0, 1], [1, 0]], dtype=np.float64)
        Z = sparse.csr_matrix([[1, 0], [0, -1]], dtype=np.float64)
        
        op = X if axis == 'x' else Z
        
        # Produto tensorial: I ⊗ I ⊗ ... ⊗ op ⊗ ... ⊗ I
        matrices = [I] * self.N
        matrices[idx] = op
        
        result = matrices[0]
        for m in matrices[1:]:
            result = sparse.kron(result, m, format='csr')
        
        return result
    
    def get_hamiltonian(self, s: float) -> sparse.csr_matrix:
        """
        Retorna o Hamiltoniano total para o parâmetro de annealing s.
        
        H(s) = (1-s) * H_driver + s * H_problem
        
        Args:
            s: Parâmetro de annealing em [0, 1]
               s=0: Estado inicial (superposição uniforme)
               s=1: Estado final (solução do problema)
        
        Returns:
            Hamiltoniano total como matriz esparsa
        """
        return (1 - s) * self.H_driver + s * self.H_problem
    
    def get_spectrum(self, s: float, num_eigen: int = 2) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula os k primeiros autovalores e autovetores para o parâmetro s.
        
        Args:
            s: Parâmetro de annealing
            num_eigen: Número de autovalores a calcular (default: 2 para gap)
        
        Returns:
            Tuple (eigenvalues, eigenvectors)
        """
        H_total = self.get_hamiltonian(s)
        
        if self.N <= 12:
            # Solver denso para sistemas pequenos (mais estável para gaps pequenos)
            evals, evecs = np.linalg.eigh(H_total.toarray())
            evals = evals[:num_eigen]
            evecs = evecs[:, :num_eigen]
        else:
            # Lanczos/Arnoldi para matrizes esparsas grandes
            evals, evecs = sla.eigsh(H_total, k=num_eigen, which='SA')
            # Ordenar por autovalor
            idx = np.argsort(evals)
            evals = evals[idx]
            evecs = evecs[:, idx]
        
        return evals, evecs
    
    def find_minimum_gap(self, num_points: int = 100) -> Tuple[float, float, np.ndarray]:
        """
        Varre o parâmetro s para encontrar o gap espectral mínimo.
        
        Args:
            num_points: Número de pontos na varredura de s
        
        Returns:
            Tuple (gap_mínimo, s_crítico, autovetor_fundamental_no_ponto_crítico)
        """
        s_vals = np.linspace(0.01, 0.99, num_points)
        min_gap = float('inf')
        critical_s = 0.5
        ground_state = None
        
        for s in s_vals:
            evals, evecs = self.get_spectrum(s)
            gap = evals[1] - evals[0]
            
            if gap < min_gap:
                min_gap = gap
                critical_s = s
                ground_state = evecs[:, 0]
        
        return min_gap, critical_s, ground_state
    
    def inverse_participation_ratio(self, eigenvector: np.ndarray) -> float:
        """
        Calcula a Razão de Participação Inversa (IPR) para testar localização.
        
        IPR = Σ |ψ_i|^4
        
        - IPR ≈ 1: Estado localizado (concentrado em poucos estados da base)
        - IPR ≈ 1/2^N: Estado deslocalizado (distribuído uniformemente)
        
        Args:
            eigenvector: Autovetor normalizado
        
        Returns:
            Valor do IPR
        """
        probs = np.abs(eigenvector) ** 2
        return np.sum(probs ** 2)
    
    def shannon_entropy(self, eigenvector: np.ndarray) -> float:
        """
        Calcula a entropia de Shannon da distribuição de probabilidades.
        
        S = -Σ p_i log(p_i)
        
        Args:
            eigenvector: Autovetor normalizado
        
        Returns:
            Entropia em bits
        """
        probs = np.abs(eigenvector) ** 2
        # Evitar log(0)
        probs = probs[probs > 1e-15]
        return -np.sum(probs * np.log2(probs))
    
    def get_full_spectrum_evolution(self, num_points: int = 50, num_levels: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula a evolução do espectro de energia durante o annealing.
        
        Args:
            num_points: Número de pontos em s
            num_levels: Número de níveis de energia a rastrear
        
        Returns:
            Tuple (s_values, energy_levels[num_points, num_levels])
        """
        s_vals = np.linspace(0, 1, num_points)
        energies = np.zeros((num_points, num_levels))
        
        for i, s in enumerate(s_vals):
            evals, _ = self.get_spectrum(s, num_eigen=num_levels)
            energies[i, :len(evals)] = evals
        
        return s_vals, energies


def generate_random_spin_glass(n: int, seed: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Gera uma instância aleatória de Spin Glass (Sherrington-Kirkpatrick).
    
    J_ij ~ N(0, 1/N) para simular frustração típica de problemas NP-hard.
    
    Args:
        n: Número de spins
        seed: Seed para reprodutibilidade
    
    Returns:
        Tuple (J, h) onde J é a matriz de acoplamento e h são campos locais
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Matriz de acoplamento simétrica com variância 1/N
    J = np.random.randn(n, n) / np.sqrt(n)
    J = np.triu(J, k=1)  # Apenas triângulo superior
    J = J + J.T  # Simetrizar
    
    # Campos locais (podemos deixar zero para modelo SK puro)
    h = np.zeros(n)
    
    return J, h


def generate_3sat_ising(n: int, clause_ratio: float = 4.2, seed: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Gera um Hamiltoniano de Ising equivalente a uma instância de 3-SAT.
    
    Cada cláusula (x_i ∨ x_j ∨ x_k) é mapeada para um termo do Hamiltoniano
    que penaliza configurações que violam a cláusula.
    
    Args:
        n: Número de variáveis
        clause_ratio: Razão cláusulas/variáveis (4.2 é o ponto crítico)
        seed: Seed para reprodutibilidade
    
    Returns:
        Tuple (J, h)
    """
    if seed is not None:
        np.random.seed(seed)
    
    num_clauses = int(clause_ratio * n)
    J = np.zeros((n, n))
    h = np.zeros(n)
    
    for _ in range(num_clauses):
        # Escolher 3 variáveis distintas
        vars_idx = np.random.choice(n, size=3, replace=False)
        # Escolher polaridades (negada ou não)
        signs = np.random.choice([-1, 1], size=3)
        
        i, j, k = vars_idx
        si, sj, sk = signs
        
        # Contribuição ao Hamiltoniano para penalizar violação
        # A cláusula é satisfeita se pelo menos um literal é verdadeiro
        h[i] += si / 8
        h[j] += sj / 8
        h[k] += sk / 8
        
        J[min(i, j), max(i, j)] += si * sj / 8
        J[min(i, k), max(i, k)] += si * sk / 8
        J[min(j, k), max(j, k)] += sj * sk / 8
    
    return J, h


if __name__ == "__main__":
    # Teste básico do módulo
    print("Testando ThermodynamicSimulation...")
    
    N = 4
    J, h = generate_random_spin_glass(N, seed=42)
    sim = ThermodynamicSimulation(N, J, h)
    
    # Encontrar gap mínimo
    min_gap, s_crit, ground_state = sim.find_minimum_gap()
    print(f"N={N}: Gap mínimo = {min_gap:.6f} em s = {s_crit:.3f}")
    
    # Calcular IPR
    ipr = sim.inverse_participation_ratio(ground_state)
    print(f"IPR do estado fundamental = {ipr:.4f}")
    
    # Calcular entropia
    entropy = sim.shannon_entropy(ground_state)
    print(f"Entropia de Shannon = {entropy:.4f} bits")
    
    print("\nMódulo carregado com sucesso!")
