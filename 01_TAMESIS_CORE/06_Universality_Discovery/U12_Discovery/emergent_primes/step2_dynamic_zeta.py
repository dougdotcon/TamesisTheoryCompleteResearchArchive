"""
STEP 2: Zeta Dinamica Real para Random Maps
============================================

OBJETIVO:
---------
Ir alem da contagem de ciclos.
Estudar a ZETA COMPLETA:

Z_f(s) = prod_{gamma ciclo} (1 - exp(-s * |gamma|))^{-1}

Analisar:
- Raio de convergencia
- Singularidades
- Estabilidade sob perturbacao
- Conexao com Ruelle dynamical zeta

TEORIA DE FUNDO:
----------------
Para sistemas dinamicos, a zeta de Ruelle e:

Z_R(s) = prod_{gamma orbita primitiva} (1 - exp(-s * |gamma|))^{-1}

Singularidades de Z_R(s) estao relacionadas ao espectro do operador de transferencia.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')


class DynamicZeta:
    """
    Zeta dinamica completa para random maps.
    """
    
    def __init__(self, n: int, f: np.ndarray = None, seed: int = None):
        self.n = n
        
        if f is None:
            if seed is not None:
                np.random.seed(seed)
            self.f = np.random.randint(0, n, size=n)
        else:
            self.f = f
        
        self.cycles = self._find_all_cycles()
        self.cycle_lengths = [len(c) for c in self.cycles]
    
    def _find_all_cycles(self) -> List[List[int]]:
        """Encontra todos os ciclos"""
        visited = set()
        cycles = []
        
        for start in range(self.n):
            if start in visited:
                continue
            
            path = []
            x = start
            while x not in visited:
                visited.add(x)
                path.append(x)
                x = self.f[x]
            
            if x in path:
                cycle_start = path.index(x)
                cycle = path[cycle_start:]
                cycles.append(cycle)
        
        return cycles
    
    def zeta_euler_product(self, s: complex) -> complex:
        """
        Z_f(s) = prod_{gamma} (1 - exp(-s * |gamma|))^{-1}
        
        Produto de Euler sobre ciclos.
        """
        result = 1.0 + 0j
        
        for length in self.cycle_lengths:
            term = 1.0 - np.exp(-s * length)
            if abs(term) > 1e-15:
                result *= 1.0 / term
        
        return result
    
    def log_zeta(self, s: complex) -> complex:
        """
        log Z_f(s) = sum_{gamma} sum_{k>=1} (1/k) * exp(-k * s * |gamma|)
                   = sum_{gamma} -log(1 - exp(-s * |gamma|))
        """
        result = 0.0 + 0j
        
        for length in self.cycle_lengths:
            arg = np.exp(-s * length)
            if abs(arg) < 1:
                result += -np.log(1 - arg)
        
        return result
    
    def zeta_series(self, s: complex, max_k: int = 50) -> complex:
        """
        Expansao em serie:
        log Z_f(s) = sum_{m>=1} (a_m / m) * exp(-m * s)
        
        onde a_m = numero de pontos periodicos de periodo m.
        """
        # Conta pontos periodicos
        a = defaultdict(int)
        for length in self.cycle_lengths:
            # Cada ciclo de comprimento L contribui L para a_L
            a[length] += length
        
        result = 0.0 + 0j
        for m in range(1, max_k + 1):
            if m in a:
                result += (a[m] / m) * np.exp(-m * s)
        
        return result
    
    def derivative_log_zeta(self, s: complex, h: float = 1e-6) -> complex:
        """
        (d/ds) log Z_f(s)
        
        Calculado numericamente.
        """
        return (self.log_zeta(s + h) - self.log_zeta(s - h)) / (2 * h)
    
    def find_singularities(self, s_real_range: Tuple[float, float] = (-2, 2),
                           s_imag_range: Tuple[float, float] = (-5, 5),
                           resolution: int = 50) -> List[complex]:
        """
        Busca singularidades de Z_f(s) no plano complexo.
        
        Singularidades ocorrem onde |Z_f(s)| -> infinito.
        """
        s_reals = np.linspace(s_real_range[0], s_real_range[1], resolution)
        s_imags = np.linspace(s_imag_range[0], s_imag_range[1], resolution)
        
        singularities = []
        threshold = 100  # Considera singularidade se |Z| > threshold
        
        for sr in s_reals:
            for si in s_imags:
                s = sr + 1j * si
                try:
                    z = self.zeta_euler_product(s)
                    if abs(z) > threshold:
                        singularities.append(s)
                except:
                    pass
        
        return singularities
    
    def abscissa_of_convergence(self) -> float:
        """
        Estima a abscissa de convergencia sigma_c.
        
        A serie de Dirichlet converge para Re(s) > sigma_c.
        
        Para zeta finita, sigma_c e determinado pelo maior ciclo.
        """
        if not self.cycle_lengths:
            return 0.0
        
        max_length = max(self.cycle_lengths)
        # Convergencia requer |exp(-s * L)| < 1, ou seja Re(s) > 0
        # Para produto finito, sempre converge para Re(s) > 0
        return 0.0
    
    def spectral_determinant_connection(self) -> Dict:
        """
        Conexao com determinante espectral:
        
        Z_f(s) = det(I - exp(-s) * L_f)^{-1}
        
        onde L_f e a matriz de transferencia.
        """
        # Matriz de transferencia
        L = np.zeros((self.n, self.n))
        for i in range(self.n):
            j = self.f[i]
            L[j, i] = 1.0
        
        # Autovalores
        eigenvalues = np.linalg.eigvals(L)
        
        # Autovalores nao-zero
        nonzero_eigs = eigenvalues[np.abs(eigenvalues) > 1e-10]
        
        return {
            'transfer_matrix_rank': np.linalg.matrix_rank(L),
            'nonzero_eigenvalues': len(nonzero_eigs),
            'spectral_radius': np.max(np.abs(eigenvalues)),
            'eigenvalues': sorted(np.abs(nonzero_eigs), reverse=True)[:10]
        }


class ZetaEnsemble:
    """
    Ensemble de zetas para estudar propriedades estatisticas.
    """
    
    def __init__(self, n: int, n_samples: int = 50, epsilon: float = 0.0):
        self.n = n
        self.n_samples = n_samples
        self.epsilon = epsilon
        
        self.zetas = []
        for _ in range(n_samples):
            if epsilon == 0.0:
                f = np.random.randint(0, n, size=n)
            elif epsilon == 1.0:
                f = np.random.permutation(n)
            else:
                f = np.random.permutation(n)
                for i in range(n):
                    if np.random.random() > epsilon:
                        f[i] = np.random.randint(0, n)
            
            self.zetas.append(DynamicZeta(n, f))
    
    def mean_log_zeta(self, s: complex) -> Tuple[complex, complex]:
        """E[log Z_f(s)] e std"""
        values = [z.log_zeta(s) for z in self.zetas]
        return np.mean(values), np.std(values)
    
    def mean_zeta_magnitude(self, s: complex) -> Tuple[float, float]:
        """E[|Z_f(s)|] e std"""
        values = [abs(z.zeta_euler_product(s)) for z in self.zetas]
        return np.mean(values), np.std(values)
    
    def cycle_length_distribution(self) -> Dict[int, float]:
        """Distribuicao de comprimentos de ciclo"""
        all_lengths = []
        for z in self.zetas:
            all_lengths.extend(z.cycle_lengths)
        
        if not all_lengths:
            return {}
        
        counts = defaultdict(int)
        for l in all_lengths:
            counts[l] += 1
        
        total = len(all_lengths)
        return {k: v / total for k, v in sorted(counts.items())}


def analyze_dynamic_zeta():
    """
    Analise completa da zeta dinamica.
    """
    print("=" * 70)
    print("STEP 2: ZETA DINAMICA DE RANDOM MAPS")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("1. ZETA PARA UM RANDOM MAP ESPECIFICO")
    print("=" * 70)
    
    n = 500
    zeta = DynamicZeta(n, seed=42)
    
    print(f"\nRandom map com n={n}")
    print(f"Numero de ciclos: {len(zeta.cycles)}")
    print(f"Comprimentos: {zeta.cycle_lengths}")
    
    print("\nValores de Z_f(s) e log Z_f(s):")
    print("-" * 60)
    print(f"{'Re(s)':>8} {'|Z_f(s)|':>15} {'Re(log Z)':>15} {'Im(log Z)':>15}")
    print("-" * 60)
    
    for s_real in [0.1, 0.5, 1.0, 1.5, 2.0, 3.0]:
        s = s_real + 0j
        z = zeta.zeta_euler_product(s)
        log_z = zeta.log_zeta(s)
        print(f"{s_real:>8.1f} {abs(z):>15.4f} {log_z.real:>15.4f} {log_z.imag:>15.4f}")
    
    print("\n" + "=" * 70)
    print("2. COMPORTAMENTO NO EIXO CRITICO (Re(s) pequeno)")
    print("=" * 70)
    
    print("\nZeta ao longo de Re(s) -> 0:")
    print("-" * 50)
    
    for s_real in [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]:
        s = s_real + 0j
        z = zeta.zeta_euler_product(s)
        print(f"s = {s_real:.2f}: |Z_f(s)| = {abs(z):.4f}")
    
    print("\n" + "=" * 70)
    print("3. CONEXAO COM OPERADOR DE TRANSFERENCIA")
    print("=" * 70)
    
    spectral = zeta.spectral_determinant_connection()
    
    print(f"\nMatriz de transferencia L_f (n x n):")
    print(f"  Rank: {spectral['transfer_matrix_rank']}")
    print(f"  Autovalores nao-zero: {spectral['nonzero_eigenvalues']}")
    print(f"  Raio espectral: {spectral['spectral_radius']:.4f}")
    print(f"\n  Top 5 |autovalores|: {spectral['eigenvalues'][:5]}")
    
    print("\n" + "=" * 70)
    print("4. COMPARACAO: RANDOM MAP vs PERMUTACAO")
    print("=" * 70)
    
    n = 200
    
    print(f"\nn = {n}, comparando zetas:")
    print("-" * 70)
    print(f"{'s':>8} {'|Z_rm(s)|':>15} {'|Z_perm(s)|':>15} {'ratio':>12}")
    print("-" * 70)
    
    rm = DynamicZeta(n, seed=42)  # Random map
    perm_f = np.random.permutation(n)
    perm = DynamicZeta(n, f=perm_f)  # Permutacao
    
    for s_real in [0.5, 1.0, 1.5, 2.0]:
        s = s_real + 0j
        z_rm = abs(rm.zeta_euler_product(s))
        z_perm = abs(perm.zeta_euler_product(s))
        ratio = z_rm / z_perm if z_perm > 0 else 0
        print(f"{s_real:>8.1f} {z_rm:>15.4f} {z_perm:>15.4f} {ratio:>12.4f}")
    
    print(f"\nCiclos random map: {rm.cycle_lengths}")
    print(f"Ciclos permutacao: {perm.cycle_lengths[:10]}... (total: {len(perm.cycles)})")
    
    print("\n" + "=" * 70)
    print("5. ZETA NO PLANO COMPLEXO")
    print("=" * 70)
    
    n = 500
    zeta = DynamicZeta(n, seed=42)
    
    print("\n|Z_f(s)| ao longo de linhas no plano complexo:")
    print("-" * 60)
    
    print("\nLinha Re(s) = 1:")
    for t in [0, 1, 2, 5, 10]:
        s = 1.0 + 1j * t
        z = abs(zeta.zeta_euler_product(s))
        print(f"  s = 1 + {t}i: |Z_f(s)| = {z:.4f}")
    
    print("\nLinha Re(s) = 0.5:")
    for t in [0, 1, 2, 5, 10]:
        s = 0.5 + 1j * t
        z = abs(zeta.zeta_euler_product(s))
        print(f"  s = 0.5 + {t}i: |Z_f(s)| = {z:.4f}")
    
    print("\n" + "=" * 70)
    print("6. ESTATISTICAS SOBRE ENSEMBLE")
    print("=" * 70)
    
    n = 300
    n_samples = 50
    
    print(f"\nEnsemble: n={n}, samples={n_samples}")
    print("\nE[|Z_f(s)|] para diferentes s:")
    print("-" * 50)
    
    ensemble_rm = ZetaEnsemble(n, n_samples, epsilon=0.0)
    ensemble_perm = ZetaEnsemble(n, n_samples, epsilon=1.0)
    
    print(f"{'s':>8} {'E[|Z|] rm':>15} {'E[|Z|] perm':>15}")
    print("-" * 50)
    
    for s_real in [0.5, 1.0, 1.5, 2.0]:
        s = s_real + 0j
        mean_rm, _ = ensemble_rm.mean_zeta_magnitude(s)
        mean_perm, _ = ensemble_perm.mean_zeta_magnitude(s)
        print(f"{s_real:>8.1f} {mean_rm:>15.4f} {mean_perm:>15.4f}")
    
    print("\n" + "=" * 70)
    print("7. DISTRIBUICAO DE COMPRIMENTOS DE CICLO")
    print("=" * 70)
    
    dist_rm = ensemble_rm.cycle_length_distribution()
    dist_perm = ensemble_perm.cycle_length_distribution()
    
    print("\nDistribuicao P(|gamma| = k):")
    print("-" * 50)
    print(f"{'k':>4} {'P_rm(k)':>12} {'P_perm(k)':>12}")
    print("-" * 50)
    
    max_k = max(max(dist_rm.keys(), default=1), max(dist_perm.keys(), default=1))
    for k in range(1, min(15, max_k + 1)):
        p_rm = dist_rm.get(k, 0)
        p_perm = dist_perm.get(k, 0)
        print(f"{k:>4} {p_rm:>12.4f} {p_perm:>12.4f}")
    
    print("\n" + "=" * 70)
    print("8. CONCLUSOES DO STEP 2")
    print("=" * 70)
    
    print("""
    DESCOBERTAS:
    ------------
    1. ZETA FINITA:
       - Random maps tem zeta como PRODUTO FINITO
       - Numero de fatores = numero de ciclos ~ (1/2) log(n)
       - Sem zeros nao-triviais (diferente de Riemann)
    
    2. COMPORTAMENTO ESPECTRAL:
       - Matriz de transferencia L_f tem muitos autovalores zero
       - Rank(L_f) << n (tipicamente ~ numero de imagens distintas)
       - Raio espectral = 1 (sempre)
    
    3. COMPARACAO RM vs PERMUTACAO:
       - |Z_perm(s)| >> |Z_rm(s)| para s pequeno
       - Permutacoes tem MAIS ciclos, logo zeta maior
       - A diferenca DIMINUI com s (convergencia mais rapida)
    
    4. DISTRIBUICAO DE COMPRIMENTOS:
       - Random maps: concentrados em ciclos pequenos
       - Permutacoes: distribuicao mais uniforme
    
    INSIGHT CRITICO:
    ----------------
    A ZETA de random maps e "degenerada" comparada com Riemann:
    - Finita (nao infinita)
    - Sem zeros (produto de polos simples)
    - Comportamento completamente determinado pelos ciclos
    
    A DIFERENCA FUNDAMENTAL:
    Random map: poucos ciclos, zeta simples
    Permutacao: muitos ciclos, zeta mais rica
    Inteiros: infinitos primos, zeta complexa
    
    PERGUNTA PARA STEP 3:
    ---------------------
    O operador de Perron-Frobenius L_f tem espectro que
    codifica informacao sobre os ciclos?
    """)
    
    print("=" * 70)


def main():
    analyze_dynamic_zeta()


if __name__ == "__main__":
    main()
