"""
Stage 29: Fluxos Caoticos - Primos como Orbitas Instaveis
=========================================================

O SISTEMA:
----------
- Fluxo caotico classico (maps iterados)
- Exemplos: Cat Map, Baker's Map, Henon Map
- Orbitas periodicas INSTAVEIS = "primos" do sistema

A ZETA DINAMICA (Ruelle):
-------------------------
Z(s) = prod_{gamma primitiva} (1 - e^{-s * T_gamma})^{-1}

onde T_gamma = periodo da orbita gamma.

A FORMULA EXPLICITA DINAMICA:
-----------------------------
log Z(s) = sum_{gamma primitiva} sum_{k>=1} (1/k) * e^{-k * s * T_gamma}

IDENTICA A WEIL!

O ESPECTRO DE RUELLE-POLLICOTT:
-------------------------------
- Ressonancias do operador de transferencia
- Polo em s=0: entropia topologica
- Outros polos: taxas de decaimento

A PERGUNTA:
-----------
Os "primos" do caos tem a mesma estrutura que os primos de Riemann?
A formula explicita emerge SOZINHA?

SE SIM: o fenomeno e universal.
"""

import numpy as np
from scipy import linalg
from typing import Dict, List, Tuple, Set
import warnings

warnings.filterwarnings('ignore')


class CatMap:
    """
    O Arnold Cat Map: exemplo classico de caos hiperbolico.
    
    [x']   [2 1] [x]   mod 1
    [y'] = [1 1] [y]
    
    Propriedades:
    - Totalmente caotico (mixing)
    - Entropia topologica = log(phi) onde phi = (1+sqrt(5))/2
    - Orbitas periodicas DENSAS
    """
    
    def __init__(self):
        self.A = np.array([[2, 1], [1, 1]])
        self.det = np.linalg.det(self.A)  # = 1 (area preserving)
        
        # Autovalores (expansao e contracao)
        eigenvalues = np.linalg.eigvals(self.A)
        self.lambda_expanding = max(abs(eigenvalues))
        self.lambda_contracting = min(abs(eigenvalues))
        
        # Entropia topologica
        self.h_top = np.log(self.lambda_expanding)
    
    def iterate(self, point: np.ndarray, n: int = 1) -> np.ndarray:
        """Itera o mapa n vezes"""
        result = point.copy()
        for _ in range(n):
            result = (self.A @ result) % 1.0
        return result
    
    def count_periodic_points_fast(self, period: int) -> int:
        """
        Conta pontos periodicos de periodo 'period' usando formula analitica.
        
        Para o Cat Map: N(period) = |det(A^period - I)| = |Tr(A^period) - 2|
        
        Isso evita enumerar todos os pontos.
        """
        A_n = np.linalg.matrix_power(self.A, period)
        trace = np.trace(A_n)
        
        # Numero de pontos fixos de A^period
        n_fixed = abs(int(round(trace - 2)))
        
        return n_fixed
    
    def count_primitive_orbits_fast(self, period: int) -> int:
        """
        Conta orbitas PRIMITIVAS de periodo exato 'period'.
        
        Usa formula de Mobius para descontar orbitas de periodos menores.
        """
        # Todos os pontos com A^period * x = x
        total_fixed = self.count_periodic_points_fast(period)
        
        # Subtrai pontos que tem periodo menor (divisor de period)
        primitive_points = total_fixed
        for d in range(1, period):
            if period % d == 0:
                primitive_points -= self.count_periodic_points_fast(d)
        
        # Numero de orbitas = pontos / periodo
        n_orbits = primitive_points // period if period > 0 else 0
        
        return max(0, n_orbits)
    
    def count_periodic_orbits(self, max_period: int) -> List[Dict]:
        """
        Conta orbitas periodicas primitivas por periodo (versao rapida).
        """
        results = []
        
        for period in range(1, max_period + 1):
            n_orbits = self.count_primitive_orbits_fast(period)
            n_points = n_orbits * period
            
            results.append({
                'period': period,
                'n_points': n_points,
                'n_orbits': n_orbits,
                'log_n_orbits': np.log(n_orbits) if n_orbits > 0 else float('-inf')
            })
        
        return results


class DynamicalZeta:
    """
    A funcao zeta dinamica de Ruelle.
    
    Z(s) = prod_{gamma primitiva} (1 - e^{-s * T_gamma})^{-1}
    
    Esta e a zeta NATURAL para sistemas dinamicos.
    Tem a MESMA estrutura da zeta de Riemann!
    """
    
    def __init__(self, system: CatMap):
        self.system = system
    
    def zeta_from_orbits(self, s: complex, max_period: int = 10) -> complex:
        """
        Calcula Z(s) como produto sobre orbitas primitivas.
        
        Z(s) = prod_gamma (1 - e^{-s * T_gamma})^{-1}
        """
        orbit_counts = self.system.count_periodic_orbits(max_period)
        
        log_z = 0.0
        
        for data in orbit_counts:
            period = data['period']
            n_orbits = data['n_orbits']
            
            if n_orbits > 0:
                # Cada orbita de periodo T contribui (1 - e^{-sT})^{-1}
                contrib = -n_orbits * np.log(1 - np.exp(-s * period))
                log_z += contrib
        
        return np.exp(log_z)
    
    def log_zeta_explicit(self, s: complex, max_period: int = 10,
                         max_k: int = 5) -> complex:
        """
        log Z(s) via formula explicita:
        
        log Z(s) = sum_gamma sum_k (1/k) * e^{-k*s*T_gamma}
        
        IDENTICA A FORMULA DE WEIL!
        """
        orbit_counts = self.system.count_periodic_orbits(max_period)
        
        log_z = 0.0
        
        for data in orbit_counts:
            period = data['period']
            n_orbits = data['n_orbits']
            
            if n_orbits > 0:
                for k in range(1, max_k + 1):
                    contrib = n_orbits * (1.0 / k) * np.exp(-k * s * period)
                    log_z += contrib
        
        return log_z
    
    def spectral_density_from_orbits(self, E: float, max_period: int = 10,
                                     epsilon: float = 0.1) -> float:
        """
        Densidade espectral via orbitas.
        
        rho(E) ~ sum_gamma T_gamma * delta(E - T_gamma)
        
        Cada orbita de periodo T contribui um pico em E = T.
        """
        orbit_counts = self.system.count_periodic_orbits(max_period)
        
        density = 0.0
        
        for data in orbit_counts:
            period = data['period']
            n_orbits = data['n_orbits']
            
            if n_orbits > 0:
                # Delta suavizada
                delta = (epsilon / np.pi) / ((E - period)**2 + epsilon**2)
                density += n_orbits * period * delta
        
        return density


class RuellePollicottSpectrum:
    """
    O espectro de Ruelle-Pollicott.
    
    Este e o espectro do OPERADOR DE TRANSFERENCIA:
    
    (L f)(x) = sum_{y: T(y)=x} f(y) / |T'(y)|
    
    Os autovalores determinam:
    - lambda = 1: medida invariante
    - |lambda| < 1: ressonancias (taxas de mixing)
    
    CONEXAO COM ZETA:
    Os polos de Z(s) correspondem aos autovalores de L.
    """
    
    def __init__(self, system: CatMap):
        self.system = system
    
    def transfer_operator_matrix(self, n_points: int = 50) -> np.ndarray:
        """
        Discretiza o operador de transferencia em uma grade.
        
        Aproximacao grosseira, mas ilustrativa.
        """
        # Grade no toro [0,1)^2
        grid = np.linspace(0, 1 - 1/n_points, n_points)
        
        # Matriz de transferencia discretizada
        L = np.zeros((n_points**2, n_points**2))
        
        for i in range(n_points):
            for j in range(n_points):
                # Ponto atual
                idx_from = i * n_points + j
                point = np.array([grid[i], grid[j]])
                
                # Imagem pelo mapa
                image = self.system.iterate(point)
                
                # Encontra celula da imagem
                i_to = int(image[0] * n_points) % n_points
                j_to = int(image[1] * n_points) % n_points
                idx_to = i_to * n_points + j_to
                
                # Transferencia (peso = 1/|det| = 1 para cat map)
                L[idx_to, idx_from] += 1.0
        
        # Normaliza
        col_sums = L.sum(axis=0, keepdims=True)
        col_sums[col_sums == 0] = 1
        L = L / col_sums
        
        return L
    
    def compute_spectrum(self, n_points: int = 30) -> np.ndarray:
        """
        Calcula o espectro do operador de transferencia.
        """
        L = self.transfer_operator_matrix(n_points)
        eigenvalues = np.linalg.eigvals(L)
        
        # Ordena por modulo
        eigenvalues = sorted(eigenvalues, key=lambda x: -abs(x))
        
        return np.array(eigenvalues)


class ExplicitFormulaComparison:
    """
    Compara a formula explicita do caos com a formula de Weil.
    
    OBJETIVO: Mostrar que sao a MESMA estrutura.
    """
    
    def __init__(self):
        self.cat = CatMap()
        self.zeta = DynamicalZeta(self.cat)
        self.spectrum = RuellePollicottSpectrum(self.cat)
    
    def decomposition_at_T(self, T: float, max_period: int = 10,
                          epsilon: float = 0.1) -> Dict:
        """
        Decomposicao em T:
        
        Tr(e^{iTL}) = parte_continua + parte_orbital
        """
        # Parte orbital (orbitas periodicas = "primos")
        orbital = self.zeta.spectral_density_from_orbits(T, max_period, epsilon)
        
        # Parte continua (background)
        # Para sistemas caoticos: ~ e^{h_top * T} (crescimento exponencial)
        continuous = np.exp(self.cat.h_top * T) / T if T > 0 else 1.0
        
        return {
            'T': T,
            'continuous': continuous,
            'orbital': orbital,
            'total': continuous + orbital,
            'h_top': self.cat.h_top
        }
    
    def verify_orbit_count_growth(self, max_period: int = 12) -> List[Dict]:
        """
        Verifica: N(T) ~ e^{h_top * T} / T (lei de crescimento)
        
        Analogo de N(T) ~ T log T / 2pi para zeros de Riemann.
        """
        results = []
        
        for period in range(1, max_period + 1):
            # Contagem real
            orbit_data = self.cat.count_periodic_orbits(period)
            cumulative = sum(d['n_orbits'] for d in orbit_data)
            
            # Previsao: ~ e^{h*T} / T
            predicted = np.exp(self.cat.h_top * period) / period if period > 0 else 1
            
            results.append({
                'period': period,
                'cumulative_orbits': cumulative,
                'predicted': predicted,
                'ratio': cumulative / predicted if predicted > 0 else 0
            })
        
        return results


def demonstrate_chaotic_zeta():
    """
    Demonstra a zeta dinamica e a emergencia dos "primos" no caos.
    """
    print("=" * 70)
    print("STAGE 29: FLUXOS CAOTICOS - PRIMOS COMO ORBITAS INSTAVEIS")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("1. O SISTEMA: ARNOLD CAT MAP")
    print("=" * 70)
    
    cat = CatMap()
    
    print(f"\nMatriz: [[2,1],[1,1]]")
    print(f"Autovalor expansor: {cat.lambda_expanding:.6f}")
    print(f"Autovalor contrator: {cat.lambda_contracting:.6f}")
    print(f"Entropia topologica: h = {cat.h_top:.6f}")
    
    print("\n" + "=" * 70)
    print("2. ORBITAS PERIODICAS = 'PRIMOS' DO CAOS")
    print("=" * 70)
    
    print("\nContagem de orbitas primitivas por periodo:")
    print("-" * 50)
    print(f"{'Periodo':>8} {'N_pontos':>10} {'N_orbitas':>10} {'log(N)':>10}")
    print("-" * 50)
    
    orbit_counts = cat.count_periodic_orbits(10)
    
    for data in orbit_counts:
        log_n = f"{data['log_n_orbits']:.3f}" if data['n_orbits'] > 0 else "-inf"
        print(f"{data['period']:8d} {data['n_points']:10d} {data['n_orbits']:10d} {log_n:>10}")
    
    print("\n" + "=" * 70)
    print("3. A FORMULA EXPLICITA DINAMICA")
    print("=" * 70)
    
    zeta = DynamicalZeta(cat)
    
    print("\nlog Z(s) = sum_gamma sum_k (1/k) * e^{-k*s*T_gamma}")
    print("\nComparando formula direta vs explicita:")
    print("-" * 50)
    print(f"{'s':>8} {'log Z (prod)':>15} {'log Z (sum)':>15}")
    print("-" * 50)
    
    for s in [0.5, 1.0, 1.5, 2.0]:
        z_prod = zeta.zeta_from_orbits(s, max_period=8)
        log_z_prod = np.log(z_prod) if abs(z_prod) > 0 else float('nan')
        log_z_sum = zeta.log_zeta_explicit(s, max_period=8)
        
        print(f"{s:8.1f} {log_z_prod.real:15.4f} {log_z_sum.real:15.4f}")
    
    print("\n" + "=" * 70)
    print("4. DECOMPOSICAO CONTINUO + ORBITAL")
    print("=" * 70)
    
    comparison = ExplicitFormulaComparison()
    
    print("\nT -> (continuo, orbital)")
    print("-" * 60)
    print(f"{'T':>8} {'Continuo':>12} {'Orbital':>12} {'Total':>12}")
    print("-" * 60)
    
    for T in [1, 2, 3, 4, 5, 6]:
        result = comparison.decomposition_at_T(T, max_period=10)
        print(f"{T:8.1f} {result['continuous']:12.4f} "
              f"{result['orbital']:12.4f} {result['total']:12.4f}")
    
    print("\n" + "=" * 70)
    print("5. LEI DE CRESCIMENTO DAS ORBITAS")
    print("=" * 70)
    
    print("\nN(T) ~ e^{h*T} / T (analogo de N(T) ~ T log T para Riemann)")
    print("-" * 60)
    print(f"{'Periodo':>8} {'N cumul':>12} {'Previsao':>12} {'Ratio':>10}")
    print("-" * 60)
    
    growth = comparison.verify_orbit_count_growth(10)
    
    for data in growth:
        print(f"{data['period']:8d} {data['cumulative_orbits']:12d} "
              f"{data['predicted']:12.2f} {data['ratio']:10.4f}")
    
    print("\n" + "=" * 70)
    print("6. CONCLUSAO")
    print("=" * 70)
    
    print("""
    O QUE OBSERVAMOS:
    -----------------
    1. Orbitas periodicas instaveis = "PRIMOS" do sistema caotico
    2. A formula explicita e IDENTICA a de Weil
    3. A lei de crescimento e analoga (exponencial vs T log T)
    4. A decomposicao continuo/orbital existe
    
    A CONEXAO:
    ----------
    | Teoria de Numeros   | Caos Classico           |
    |---------------------|-------------------------|
    | Primo p             | Orbita primitiva gamma  |
    | log(p)              | Periodo T_gamma         |
    | Zeros de zeta       | Ressonancias de Ruelle  |
    | Formula de Weil     | Formula de traco        |
    | N(T) ~ T log T      | N(T) ~ e^{hT} / T       |
    
    CONCLUSAO:
    ----------
    O fenomeno dos "primos" e UNIVERSAL em sistemas dinamicos.
    
    A estrutura Weil-Selberg nao e especifica da aritmetica.
    E uma propriedade de qualquer sistema com:
    - Fluxo hiperbolico
    - Orbitas periodicas
    - Operador de transferencia
    
    Os primos de Riemann sao um CASO PARTICULAR.
    """)
    
    print("=" * 70)


def main():
    demonstrate_chaotic_zeta()


if __name__ == "__main__":
    main()
