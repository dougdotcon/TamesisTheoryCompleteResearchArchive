"""
STEP 4.3: Escala Critica da Transicao
=====================================

OBJETIVO:
---------
Encontrar a escala exata delta_c(n) que controla a transicao.

HIPOTESES A TESTAR:
-------------------
1. delta_c ~ 1/n         (escala linear)
2. delta_c ~ 1/log(n)    (escala logaritmica)
3. delta_c ~ 1/n^alpha   (escala potencia)
4. delta_c ~ 1/sqrt(n)   (escala raiz)

METODOLOGIA:
------------
Fixar epsilon(n) = 1 - c/f(n) para diferentes f(n).
Medir E[autovalores unitarios] / n para varios n.
Se a escala for correta, a fracao deve ser CONSTANTE em n.

CRITERIO DE SUCESSO:
--------------------
Encontrar f(n) tal que:
E[|eig|=1] / n = phi(c) para todos n

onde phi(c) e uma funcao universal de c apenas.
"""

import numpy as np
from typing import List, Dict, Tuple, Callable
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')


class CriticalScalingAnalysis:
    """
    Analise da escala critica da transicao.
    """
    
    def __init__(self, n: int, epsilon: float, seed: int = None):
        self.n = n
        self.epsilon = epsilon
        
        if seed is not None:
            np.random.seed(seed)
        
        self.f = self._generate_map()
        self.L = self._build_transfer_operator()
        self.cycles = self._find_all_cycles()
    
    def _generate_map(self) -> np.ndarray:
        f = np.random.permutation(self.n)
        for i in range(self.n):
            if np.random.random() > self.epsilon:
                f[i] = np.random.randint(0, self.n)
        return f
    
    def _build_transfer_operator(self) -> np.ndarray:
        L = np.zeros((self.n, self.n))
        for j in range(self.n):
            i = self.f[j]
            L[i, j] = 1.0
        return L
    
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
    
    def count_unit_eigenvalues(self, tol: float = 1e-6) -> int:
        eigenvalues = np.linalg.eigvals(self.L)
        mags = np.abs(eigenvalues)
        return np.sum(np.isclose(mags, 1.0, atol=tol))
    
    def total_cycle_length(self) -> int:
        return sum(len(c) for c in self.cycles)


def ensemble_statistics(n: int, epsilon: float, n_samples: int = 30) -> Dict:
    """
    Estatisticas do ensemble para (n, epsilon).
    """
    unit_counts = []
    cycle_totals = []
    
    for _ in range(n_samples):
        analysis = CriticalScalingAnalysis(n, epsilon)
        unit_counts.append(analysis.count_unit_eigenvalues())
        cycle_totals.append(analysis.total_cycle_length())
    
    return {
        'n': n,
        'epsilon': epsilon,
        'mean_unit': np.mean(unit_counts),
        'std_unit': np.std(unit_counts),
        'mean_cycle': np.mean(cycle_totals),
        'fraction_unit': np.mean(unit_counts) / n
    }


def test_scaling(scale_func: Callable[[int], float], 
                 c_values: List[float],
                 n_values: List[int],
                 n_samples: int = 30) -> Dict:
    """
    Testa se epsilon(n) = 1 - c/scale_func(n) produz colapso de dados.
    
    Se a escala for correta, fraction_unit deve ser funcao apenas de c.
    """
    results = []
    
    for c in c_values:
        for n in n_values:
            scale = scale_func(n)
            delta = c / scale
            epsilon = 1.0 - delta
            
            if epsilon < 0 or epsilon > 1:
                continue
            
            stats = ensemble_statistics(n, epsilon, n_samples)
            stats['c'] = c
            stats['scale'] = scale
            stats['delta'] = delta
            results.append(stats)
    
    return results


def analyze_critical_scaling():
    """
    Analise completa da escala critica.
    """
    print("=" * 70)
    print("STEP 4.3: ESCALA CRITICA DA TRANSICAO")
    print("=" * 70)
    
    n_values = [100, 150, 200, 300]
    n_samples = 25
    
    print("\n" + "=" * 70)
    print("1. TESTE: delta = c / n")
    print("=" * 70)
    
    c_values = [0.5, 1.0, 2.0, 5.0, 10.0]
    scale_n = lambda n: n
    
    results_n = test_scaling(scale_n, c_values, n_values, n_samples)
    
    print("\nSe escala correta: fraction_unit deve ser constante para cada c")
    print("-" * 70)
    print(f"{'c':>8} {'n':>6} {'delta':>10} {'frac_unit':>12} {'E[unit]':>10}")
    print("-" * 70)
    
    for r in results_n:
        print(f"{r['c']:>8.1f} {r['n']:>6} {r['delta']:>10.4f} {r['fraction_unit']:>12.3f} {r['mean_unit']:>10.1f}")
    
    # Calcula variancia por c
    print("\nVariancia de fraction_unit para cada c:")
    for c in c_values:
        fracs = [r['fraction_unit'] for r in results_n if r['c'] == c]
        if len(fracs) > 1:
            var = np.var(fracs)
            mean = np.mean(fracs)
            cv = np.std(fracs) / mean if mean > 0 else 0
            print(f"  c = {c}: mean = {mean:.3f}, CV = {cv:.3f}")
    
    print("\n" + "=" * 70)
    print("2. TESTE: delta = c / log(n)")
    print("=" * 70)
    
    c_values_log = [0.1, 0.2, 0.5, 1.0, 2.0]
    scale_log = lambda n: np.log(n)
    
    results_log = test_scaling(scale_log, c_values_log, n_values, n_samples)
    
    print("\nSe escala correta: fraction_unit deve ser constante para cada c")
    print("-" * 70)
    print(f"{'c':>8} {'n':>6} {'delta':>10} {'frac_unit':>12} {'E[unit]':>10}")
    print("-" * 70)
    
    for r in results_log:
        print(f"{r['c']:>8.2f} {r['n']:>6} {r['delta']:>10.4f} {r['fraction_unit']:>12.3f} {r['mean_unit']:>10.1f}")
    
    print("\nVariancia de fraction_unit para cada c:")
    for c in c_values_log:
        fracs = [r['fraction_unit'] for r in results_log if r['c'] == c]
        if len(fracs) > 1:
            var = np.var(fracs)
            mean = np.mean(fracs)
            cv = np.std(fracs) / mean if mean > 0 else 0
            print(f"  c = {c}: mean = {mean:.3f}, CV = {cv:.3f}")
    
    print("\n" + "=" * 70)
    print("3. TESTE: delta = c / sqrt(n)")
    print("=" * 70)
    
    c_values_sqrt = [0.1, 0.2, 0.5, 1.0, 2.0]
    scale_sqrt = lambda n: np.sqrt(n)
    
    results_sqrt = test_scaling(scale_sqrt, c_values_sqrt, n_values, n_samples)
    
    print("\nSe escala correta: fraction_unit deve ser constante para cada c")
    print("-" * 70)
    print(f"{'c':>8} {'n':>6} {'delta':>10} {'frac_unit':>12} {'E[unit]':>10}")
    print("-" * 70)
    
    for r in results_sqrt:
        print(f"{r['c']:>8.2f} {r['n']:>6} {r['delta']:>10.4f} {r['fraction_unit']:>12.3f} {r['mean_unit']:>10.1f}")
    
    print("\nVariancia de fraction_unit para cada c:")
    for c in c_values_sqrt:
        fracs = [r['fraction_unit'] for r in results_sqrt if r['c'] == c]
        if len(fracs) > 1:
            var = np.var(fracs)
            mean = np.mean(fracs)
            cv = np.std(fracs) / mean if mean > 0 else 0
            print(f"  c = {c}: mean = {mean:.3f}, CV = {cv:.3f}")
    
    print("\n" + "=" * 70)
    print("4. COMPARACAO: QUAL ESCALA COLAPSA MELHOR?")
    print("=" * 70)
    
    # Calcula coeficiente de variacao medio para cada escala
    def mean_cv(results, c_values):
        cvs = []
        for c in c_values:
            fracs = [r['fraction_unit'] for r in results if r['c'] == c]
            if len(fracs) > 1 and np.mean(fracs) > 0:
                cvs.append(np.std(fracs) / np.mean(fracs))
        return np.mean(cvs) if cvs else float('inf')
    
    cv_n = mean_cv(results_n, c_values)
    cv_log = mean_cv(results_log, c_values_log)
    cv_sqrt = mean_cv(results_sqrt, c_values_sqrt)
    
    print(f"\nCoeficiente de variacao medio (menor = melhor colapso):")
    print(f"  delta = c/n:      CV = {cv_n:.4f}")
    print(f"  delta = c/log(n): CV = {cv_log:.4f}")
    print(f"  delta = c/sqrt(n): CV = {cv_sqrt:.4f}")
    
    best = min([('n', cv_n), ('log(n)', cv_log), ('sqrt(n)', cv_sqrt)], key=lambda x: x[1])
    print(f"\nMelhor escala: delta = c / {best[0]}")
    
    print("\n" + "=" * 70)
    print("5. FUNCAO DE ESCALA phi(c)")
    print("=" * 70)
    
    # Usa a melhor escala para determinar phi(c)
    if best[0] == 'n':
        results_best = results_n
        c_vals = c_values
    elif best[0] == 'log(n)':
        results_best = results_log
        c_vals = c_values_log
    else:
        results_best = results_sqrt
        c_vals = c_values_sqrt
    
    print(f"\nPara delta = c / {best[0]}:")
    print("-" * 40)
    print(f"{'c':>8} {'phi(c) = E[frac_unit]':>20}")
    print("-" * 40)
    
    for c in c_vals:
        fracs = [r['fraction_unit'] for r in results_best if r['c'] == c]
        if fracs:
            phi = np.mean(fracs)
            print(f"{c:>8.2f} {phi:>20.3f}")
    
    print("\n" + "=" * 70)
    print("6. CONCLUSOES DO STEP 4.3")
    print("=" * 70)
    
    print(f"""
    DESCOBERTA PRINCIPAL:
    ---------------------
    A escala critica e delta_c ~ c / {best[0]}
    
    Isso significa:
    - E[autovalores unitarios] / n = phi(c * {best[0]} / n)
    - A funcao phi(c) controla a transicao
    - Para c grande: phi -> 1 (permutacao)
    - Para c pequeno: phi -> O(log(n)/n) (random map)
    
    INTERPRETACAO FISICA:
    ---------------------
    O parametro c mede a "distancia" do ponto critico.
    A escala {best[0]} e a escala natural do sistema.
    
    ANALOGIA COM FISICA ESTATISTICA:
    --------------------------------
    Isso e similar a uma transicao de fase de segunda ordem:
    - Parametro de ordem: fraction_unit
    - Parametro de controle: epsilon
    - Escala critica: {best[0]}
    - Expoente critico: implicitamente codificado em phi(c)
    """)
    
    print("=" * 70)


def finite_size_scaling():
    """
    Analise de finite-size scaling mais detalhada.
    """
    print("\n" + "=" * 70)
    print("7. FINITE-SIZE SCALING DETALHADO")
    print("=" * 70)
    
    # Testa diferentes valores de n para delta fixo
    n_values = [50, 100, 150, 200, 300, 400]
    deltas = [0.01, 0.02, 0.05, 0.1]
    n_samples = 20
    
    print("\nE[autovalores unitarios] / n para delta fixo:")
    print("-" * 70)
    header = f"{'n':>6}" + "".join([f"{'d='+str(d):>12}" for d in deltas])
    print(header)
    print("-" * 70)
    
    for n in n_values:
        row = f"{n:>6}"
        for delta in deltas:
            epsilon = 1.0 - delta
            stats = ensemble_statistics(n, epsilon, n_samples)
            row += f"{stats['fraction_unit']:>12.3f}"
        print(row)
    
    print("\nSe frac_unit e constante em n para delta fixo:")
    print("  -> A escala correta NAO e delta = c/n")
    print("\nSe frac_unit MUDA com n para delta fixo:")
    print("  -> A escala correta PODE ser delta = c/n")


def main():
    analyze_critical_scaling()
    finite_size_scaling()


if __name__ == "__main__":
    main()
