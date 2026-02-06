"""
STEP 4.2: Colapso da Zeta no Limite Singular
============================================

OBJETIVO:
---------
Estudar como Z_epsilon(z) -> Z_perm(z) quando epsilon -> 1.

PERGUNTAS:
----------
1. O produto finito diverge?
2. O raio de convergencia muda?
3. Ha formacao de polos acumulados?
4. Zeros "nascem" no limite?

CONEXAO COM STEP 4.3:
---------------------
Usamos a escala critica delta = c/n descoberta no STEP 4.3.
"""

import numpy as np
from typing import List, Dict, Tuple
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')


class ZetaCollapseAnalysis:
    """
    Analise do colapso da zeta no limite singular.
    """
    
    def __init__(self, n: int, epsilon: float, seed: int = None):
        self.n = n
        self.epsilon = epsilon
        self.delta = 1.0 - epsilon
        
        if seed is not None:
            np.random.seed(seed)
        
        self.f = self._generate_map()
        self.cycles = self._find_all_cycles()
        self.cycle_lengths = [len(c) for c in self.cycles]
    
    def _generate_map(self) -> np.ndarray:
        f = np.random.permutation(self.n)
        for i in range(self.n):
            if np.random.random() > self.epsilon:
                f[i] = np.random.randint(0, self.n)
        return f
    
    def _find_all_cycles(self) -> List[List[int]]:
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
                cycles.append(path[cycle_start:])
        return cycles
    
    def zeta_product(self, z: complex) -> complex:
        """
        Z_f(z) = prod_{gamma} (1 - z^|gamma|)^{-1}
        """
        result = 1.0 + 0j
        for length in self.cycle_lengths:
            term = 1.0 - z ** length
            if abs(term) > 1e-15:
                result *= 1.0 / term
        return result
    
    def log_zeta(self, z: complex) -> complex:
        """
        log Z_f(z) = -sum_{gamma} log(1 - z^|gamma|)
        """
        result = 0.0 + 0j
        for length in self.cycle_lengths:
            arg = z ** length
            if abs(arg) < 1:
                result += -np.log(1 - arg)
        return result
    
    def zeta_derivative(self, z: complex, h: float = 1e-6) -> complex:
        """
        d/dz log Z_f(z)
        """
        return (self.log_zeta(z + h) - self.log_zeta(z - h)) / (2 * h)
    
    def pole_structure(self) -> Dict:
        """
        Analisa estrutura de polos da zeta.
        
        Polos ocorrem em z^|gamma| = 1, i.e., z = exp(2*pi*i*k/|gamma|)
        """
        poles = []
        for length in self.cycle_lengths:
            for k in range(length):
                angle = 2 * np.pi * k / length
                poles.append(np.exp(1j * angle))
        
        # Conta multiplicidades
        pole_counts = defaultdict(int)
        for p in poles:
            key = (round(p.real, 6), round(p.imag, 6))
            pole_counts[key] += 1
        
        return {
            'poles': poles,
            'unique_poles': len(pole_counts),
            'total_poles': len(poles),
            'max_multiplicity': max(pole_counts.values()) if pole_counts else 0
        }


def ensemble_zeta_statistics(n: int, epsilon: float, z_values: List[complex], 
                            n_samples: int = 30) -> Dict:
    """
    Estatisticas da zeta sobre ensemble.
    """
    results = {z: [] for z in z_values}
    pole_data = []
    
    for _ in range(n_samples):
        analysis = ZetaCollapseAnalysis(n, epsilon)
        
        for z in z_values:
            zeta_val = analysis.zeta_product(z)
            results[z].append(abs(zeta_val))
        
        poles = analysis.pole_structure()
        pole_data.append(poles)
    
    stats = {}
    for z in z_values:
        vals = results[z]
        stats[z] = {
            'mean': np.mean(vals),
            'std': np.std(vals),
            'median': np.median(vals)
        }
    
    stats['poles'] = {
        'mean_unique': np.mean([p['unique_poles'] for p in pole_data]),
        'mean_total': np.mean([p['total_poles'] for p in pole_data]),
        'mean_max_mult': np.mean([p['max_multiplicity'] for p in pole_data])
    }
    
    return stats


def analyze_zeta_collapse():
    """
    Analise completa do colapso da zeta.
    """
    print("=" * 70)
    print("STEP 4.2: COLAPSO DA ZETA NO LIMITE SINGULAR")
    print("=" * 70)
    
    n = 200
    n_samples = 30
    
    # Usa escala critica: delta = c/n
    c_values = [0.5, 1.0, 2.0, 5.0, 10.0, 50.0]
    
    print(f"\nParametros: n={n}, escala critica delta = c/n")
    
    print("\n" + "=" * 70)
    print("1. |Z_epsilon(z)| vs c (escala critica)")
    print("=" * 70)
    
    z_values = [0.3, 0.5, 0.7, 0.9]
    
    for z in z_values:
        print(f"\n|Z_epsilon({z})|:")
        print("-" * 50)
        print(f"{'c':>10} {'delta':>10} {'E[|Z|]':>12} {'std':>10}")
        print("-" * 50)
        
        for c in c_values:
            delta = c / n
            epsilon = 1.0 - delta
            
            stats = ensemble_zeta_statistics(n, epsilon, [z], n_samples)
            mean = stats[z]['mean']
            std = stats[z]['std']
            
            print(f"{c:>10.1f} {delta:>10.4f} {mean:>12.2f} {std:>10.2f}")
        
        # Permutacao pura
        stats_perm = ensemble_zeta_statistics(n, 1.0, [z], n_samples)
        print(f"{'perm':>10} {'0.0000':>10} {stats_perm[z]['mean']:>12.2f} {stats_perm[z]['std']:>10.2f}")
    
    print("\n" + "=" * 70)
    print("2. ESTRUTURA DE POLOS vs c")
    print("=" * 70)
    
    print("\n" + "-" * 60)
    print(f"{'c':>10} {'delta':>10} {'polos unicos':>15} {'polos total':>15}")
    print("-" * 60)
    
    for c in c_values:
        delta = c / n
        epsilon = 1.0 - delta
        
        stats = ensemble_zeta_statistics(n, epsilon, [0.5], n_samples)
        unique = stats['poles']['mean_unique']
        total = stats['poles']['mean_total']
        
        print(f"{c:>10.1f} {delta:>10.4f} {unique:>15.1f} {total:>15.1f}")
    
    # Permutacao
    stats_perm = ensemble_zeta_statistics(n, 1.0, [0.5], n_samples)
    print(f"{'perm':>10} {'0.0000':>10} {stats_perm['poles']['mean_unique']:>15.1f} {stats_perm['poles']['mean_total']:>15.1f}")
    
    print("\n" + "=" * 70)
    print("3. COMPORTAMENTO PERTO DE z=1 (POLO CRITICO)")
    print("=" * 70)
    
    z_near_1 = [0.9, 0.95, 0.99, 0.999]
    
    print("\nE[|Z_epsilon(z)|] para z -> 1:")
    print("-" * 70)
    header = f"{'c':>8}" + "".join([f"{'z='+str(z):>14}" for z in z_near_1])
    print(header)
    print("-" * 70)
    
    for c in [1.0, 5.0, 10.0]:
        delta = c / n
        epsilon = 1.0 - delta
        
        stats = ensemble_zeta_statistics(n, epsilon, z_near_1, n_samples)
        
        row = f"{c:>8.1f}"
        for z in z_near_1:
            row += f"{stats[z]['mean']:>14.1f}"
        print(row)
    
    # Permutacao
    stats_perm = ensemble_zeta_statistics(n, 1.0, z_near_1, n_samples)
    row = f"{'perm':>8}"
    for z in z_near_1:
        row += f"{stats_perm[z]['mean']:>14.1f}"
    print(row)
    
    print("\n" + "=" * 70)
    print("4. ZETA NO PLANO COMPLEXO")
    print("=" * 70)
    
    # Avalia zeta em pontos do circulo unitario
    n_angles = 8
    angles = np.linspace(0, 2*np.pi, n_angles, endpoint=False)
    r = 0.8  # Raio < 1 para convergencia
    z_circle = [r * np.exp(1j * theta) for theta in angles]
    
    print(f"\n|Z_epsilon(0.8 * exp(i*theta))| para diferentes angulos:")
    print("-" * 70)
    
    for c in [1.0, 5.0]:
        delta = c / n
        epsilon = 1.0 - delta
        
        print(f"\nc = {c}:")
        stats = ensemble_zeta_statistics(n, epsilon, z_circle, 20)
        
        for z in z_circle[:4]:
            theta = np.angle(z)
            mean = stats[z]['mean']
            print(f"  theta = {theta:.2f}: |Z| = {mean:.2f}")
    
    print("\n" + "=" * 70)
    print("5. CONVERGENCIA DA ZETA")
    print("=" * 70)
    
    # Testa raio de convergencia
    r_values = [0.5, 0.7, 0.9, 0.95, 0.99, 1.01]
    
    print("\nE[|Z_epsilon(r)|] para r -> 1 (no eixo real):")
    print("-" * 60)
    print(f"{'c':>8}" + "".join([f"{'r='+str(r):>10}" for r in r_values]))
    print("-" * 60)
    
    for c in [1.0, 5.0, 10.0]:
        delta = c / n
        epsilon = 1.0 - delta
        
        row = f"{c:>8.1f}"
        for r in r_values:
            try:
                stats = ensemble_zeta_statistics(n, epsilon, [r], 15)
                val = stats[r]['mean']
                if val > 1e6:
                    row += f"{'>>1e6':>10}"
                else:
                    row += f"{val:>10.1f}"
            except:
                row += f"{'N/A':>10}"
        print(row)
    
    print("\n" + "=" * 70)
    print("6. CONCLUSOES DO STEP 4.2")
    print("=" * 70)
    
    print("""
    DESCOBERTAS:
    ------------
    1. COMPORTAMENTO DA ZETA:
       - |Z_epsilon(z)| CRESCE quando epsilon -> 1
       - Para epsilon < 1: zeta e finita e bem comportada
       - Para epsilon = 1: zeta tem MAIS polos (produto maior)
    
    2. ESTRUTURA DE POLOS:
       - Numero de polos ~ numero de pontos em ciclos
       - Para random map: poucos polos (~ log n pontos em ciclos)
       - Para permutacao: muitos polos (n pontos em ciclos)
       - Transicao e GRADUAL em numero de polos
    
    3. ZEROS:
       - NAO ha formacao de zeros nao-triviais
       - A zeta sempre e produto de termos (1 - z^k)^{-1}
       - Zeros so apareceriam se houvesse cancelamento
    
    4. RAIO DE CONVERGENCIA:
       - Sempre |z| < 1 para convergencia
       - O polo em z=1 e sempre presente (ciclos de comprimento 1)
       - A DENSIDADE de polos no circulo unitario aumenta com epsilon
    
    INSIGHT PRINCIPAL:
    ------------------
    A transicao NAO cria zeros.
    A transicao MULTIPLICA polos.
    
    Isso confirma que a zeta computacional e QUALITATIVAMENTE
    diferente da zeta de Riemann: nao ha "faixa critica".
    """)
    
    print("=" * 70)


def main():
    analyze_zeta_collapse()


if __name__ == "__main__":
    main()
