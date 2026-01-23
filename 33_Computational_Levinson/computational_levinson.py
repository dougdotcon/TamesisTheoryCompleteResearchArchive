"""
Stage 33: Teorema de Levinson Computacional
===========================================

O TEOREMA DE LEVINSON ORIGINAL:
-------------------------------
Para a funcao zeta de Riemann:

    N(T) = (1/pi) * theta(T) + 1 + S(T)

onde S(T) = (1/pi) * arg(zeta(1/2 + iT))

Levinson mostrou que:
    lim_{T->infty} S(T) / log(T) = 0

ou seja: a "fase de espalhamento" S(T) cresce mais devagar que log(T).

A VERSAO COMPUTACIONAL:
-----------------------
Para um algoritmo A com operador L_A e zeta Z_A(s):

    N_A(T) = (numero de autovalores de L_A com |lambda| > e^{-T})

Definimos:
    theta_A(T) = parte "suave" de N_A(T)  (lei de Weyl computacional)
    S_A(T) = N_A(T) - theta_A(T)          (flutuacao)

CONJECTURA (Levinson computacional):
------------------------------------
S_A(T) = numero de "primos computacionais" (ciclos primitivos)

Ou seja: as flutuacoes do espectro SAO os primos.

O QUE VAMOS TESTAR:
-------------------
1. Calcular N_A(T) para varios algoritmos
2. Separar theta_A(T) e S_A(T)
3. Verificar se S_A correlaciona com contagem de ciclos
"""

import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
import warnings

warnings.filterwarnings('ignore')


class ComputationalSpectrum:
    """
    O espectro de um algoritmo visto como sistema dinamico.
    
    Dado um operador de transferencia L, os autovalores {lambda_i}
    determinam as propriedades do algoritmo.
    """
    
    def __init__(self, L: np.ndarray, name: str = "Algorithm"):
        self.L = L
        self.name = name
        self.n = L.shape[0]
        
        # Calcula espectro
        self.eigenvalues = np.linalg.eigvals(L)
        self.eigenvalues_sorted = sorted(self.eigenvalues, key=lambda x: -abs(x))
    
    def counting_function(self, T: float) -> int:
        """
        N_A(T) = numero de autovalores com |lambda| > e^{-T}
        
        Analogo de N(T) para Riemann (numero de zeros com Im(rho) < T).
        """
        threshold = np.exp(-T)
        return sum(1 for lam in self.eigenvalues if abs(lam) > threshold)
    
    def smooth_counting(self, T: float) -> float:
        """
        theta_A(T) = parte suave de N_A(T)
        
        Lei de Weyl computacional: theta_A(T) ~ c * T^d para algum d.
        """
        # Para matrizes finitas, estimamos a parte suave
        # como interpolacao logaritmica
        if T <= 0:
            return 0.0
        
        # Aproximacao: n * (1 - e^{-T})
        # Isso da a "densidade media" de autovalores
        return self.n * (1 - np.exp(-T))
    
    def fluctuation(self, T: float) -> float:
        """
        S_A(T) = N_A(T) - theta_A(T)
        
        Esta e a "fase de espalhamento" computacional.
        
        HIPOTESE: S_A(T) correlaciona com numero de ciclos primitivos.
        """
        N = self.counting_function(T)
        theta = self.smooth_counting(T)
        return N - theta


class CyclePrimeCounting:
    """
    Contagem de ciclos primitivos ("primos computacionais").
    """
    
    def __init__(self, L: np.ndarray):
        self.L = L
        self.n = L.shape[0]
    
    def trace_power(self, k: int) -> float:
        """Tr(L^k) = soma de lambda_i^k"""
        L_k = np.linalg.matrix_power(self.L, k)
        return np.trace(L_k).real
    
    def primitive_count_mobius(self, max_length: int = 20) -> Dict[int, int]:
        """
        Conta ciclos primitivos usando inversao de Mobius.
        
        Se N_k = Tr(L^k), entao:
        Primos de comprimento k = (1/k) * sum_{d|k} mu(k/d) * N_d
        """
        # Funcao de Mobius
        def mobius(n):
            if n == 1:
                return 1
            # Fatoracao simples
            factors = []
            temp = n
            for p in range(2, int(np.sqrt(n)) + 2):
                count = 0
                while temp % p == 0:
                    temp //= p
                    count += 1
                if count > 0:
                    factors.append((p, count))
            if temp > 1:
                factors.append((temp, 1))
            
            # Se algum fator tem expoente > 1, mu = 0
            for _, exp in factors:
                if exp > 1:
                    return 0
            
            return (-1) ** len(factors)
        
        # Divisores
        def divisors(n):
            divs = []
            for i in range(1, int(np.sqrt(n)) + 1):
                if n % i == 0:
                    divs.append(i)
                    if i != n // i:
                        divs.append(n // i)
            return sorted(divs)
        
        # Conta primos por comprimento
        traces = {k: self.trace_power(k) for k in range(1, max_length + 1)}
        
        primes = {}
        for k in range(1, max_length + 1):
            # Formula de inversao
            total = sum(mobius(k // d) * traces[d] for d in divisors(k))
            primes[k] = max(0, int(round(total / k)))
        
        return primes
    
    def total_primes_up_to(self, max_length: int) -> int:
        """pi_A(n) = numero total de primos de comprimento <= n"""
        primes = self.primitive_count_mobius(max_length)
        return sum(primes.values())


class LevinsonCorrelation:
    """
    Testa a correlacao entre S_A(T) e contagem de primos.
    
    HIPOTESE CENTRAL:
    S_A(T) ~ sum_{l <= T} (primos de comprimento l)
    
    ou seja: as flutuacoes espectrais SAO os primos.
    """
    
    def __init__(self, L: np.ndarray, name: str = "Algorithm"):
        self.spectrum = ComputationalSpectrum(L, name)
        self.primes = CyclePrimeCounting(L)
        self.name = name
    
    def compute_levinson_data(self, T_values: List[float]) -> List[Dict]:
        """
        Computa dados para verificar a relacao de Levinson.
        """
        results = []
        
        for T in T_values:
            N = self.spectrum.counting_function(T)
            theta = self.spectrum.smooth_counting(T)
            S = self.spectrum.fluctuation(T)
            
            # Primos ate comprimento T
            pi = self.primes.total_primes_up_to(int(max(1, T)))
            
            results.append({
                'T': T,
                'N_A': N,
                'theta_A': theta,
                'S_A': S,
                'pi_A': pi,
                'ratio': S / pi if pi > 0 else 0
            })
        
        return results
    
    def test_levinson_hypothesis(self) -> Dict:
        """
        Testa: S_A(T) / pi_A(T) -> constante quando T -> infinito?
        """
        T_values = [1, 2, 3, 5, 8, 10, 15, 20]
        data = self.compute_levinson_data(T_values)
        
        # Verifica se ratio converge
        ratios = [d['ratio'] for d in data if d['pi_A'] > 0]
        
        if len(ratios) < 2:
            return {'converges': False, 'mean_ratio': 0, 'std_ratio': 0, 'data': data}
        
        return {
            'converges': np.std(ratios) < np.mean(ratios) if np.mean(ratios) > 0 else False,
            'mean_ratio': np.mean(ratios),
            'std_ratio': np.std(ratios),
            'data': data
        }


def create_test_operators() -> List[Tuple[np.ndarray, str]]:
    """
    Cria operadores de teste com diferentes estruturas.
    """
    operators = []
    
    # 1. Mapa de Gauss discretizado (fracao continua)
    N = 40
    L_gauss = np.zeros((N, N))
    for j in range(N):
        x_j = (j + 1) / N
        for n in range(1, N // 2):
            x_pre = 1 / (n + x_j)
            if 0 < x_pre <= 1:
                i = int(x_pre * N) - 1
                if 0 <= i < N:
                    L_gauss[j, i] += 1 / (n + x_j)**2
    # Normaliza
    col_sums = L_gauss.sum(axis=0, keepdims=True)
    col_sums[col_sums == 0] = 1
    L_gauss = L_gauss / col_sums
    operators.append((L_gauss, "Gauss Map"))
    
    # 2. Random walk em grafo
    N = 40
    np.random.seed(42)
    A = (np.random.random((N, N)) < 0.2).astype(float)
    np.fill_diagonal(A, 0)
    col_sums = A.sum(axis=0, keepdims=True)
    col_sums[col_sums == 0] = 1
    L_random = A / col_sums
    operators.append((L_random, "Random Graph"))
    
    # 3. Shift circular (nao caotico)
    N = 40
    L_shift = np.zeros((N, N))
    for i in range(N):
        L_shift[(i + 1) % N, i] = 1.0
    operators.append((L_shift, "Circular Shift"))
    
    # 4. Cat map discretizado
    N = 20
    L_cat = np.zeros((N * N, N * N))
    A = np.array([[2, 1], [1, 1]])
    for i in range(N):
        for j in range(N):
            idx_from = i * N + j
            new_coords = (A @ np.array([i, j])) % N
            idx_to = int(new_coords[0]) * N + int(new_coords[1])
            L_cat[idx_to, idx_from] = 1.0
    operators.append((L_cat, "Cat Map"))
    
    return operators


def demonstrate_levinson():
    """
    Demonstra o teorema de Levinson computacional.
    """
    print("=" * 70)
    print("STAGE 33: TEOREMA DE LEVINSON COMPUTACIONAL")
    print("Fase de espalhamento = contagem de primos?")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("1. O TEOREMA CLASSICO DE LEVINSON")
    print("=" * 70)
    
    print("""
    Para Riemann:
        N(T) = theta(T) + S(T)
    
    onde:
        N(T) = numero de zeros com Im(rho) < T
        theta(T) = (T/2pi) * log(T/2pi) - T/2pi  (parte suave)
        S(T) = flutuacao
    
    Levinson: S(T) = O(log T)
    
    VERSAO COMPUTACIONAL:
        N_A(T) = theta_A(T) + S_A(T)
    
    HIPOTESE: S_A(T) ~ pi_A(T) (numero de primos computacionais)
    """)
    
    print("\n" + "=" * 70)
    print("2. OPERADORES DE TESTE")
    print("=" * 70)
    
    operators = create_test_operators()
    
    for L, name in operators:
        print(f"\n  {name}: {L.shape[0]} estados")
    
    print("\n" + "=" * 70)
    print("3. TESTE DA HIPOTESE DE LEVINSON")
    print("=" * 70)
    
    for L, name in operators:
        print(f"\n{name}")
        print("-" * 60)
        
        levinson = LevinsonCorrelation(L, name)
        result = levinson.test_levinson_hypothesis()
        
        print(f"{'T':>6} {'N_A':>8} {'theta_A':>10} {'S_A':>10} {'pi_A':>8} {'S/pi':>10}")
        print("-" * 60)
        
        for d in result['data']:
            ratio_str = f"{d['ratio']:.3f}" if d['pi_A'] > 0 else "N/A"
            print(f"{d['T']:6.1f} {d['N_A']:8d} {d['theta_A']:10.2f} "
                  f"{d['S_A']:10.2f} {d['pi_A']:8d} {ratio_str:>10}")
        
        print(f"\nConverge? {result['converges']}")
        print(f"Ratio medio: {result['mean_ratio']:.3f} +/- {result['std_ratio']:.3f}")
    
    print("\n" + "=" * 70)
    print("4. ANALISE ESPECTRAL DETALHADA")
    print("=" * 70)
    
    for L, name in operators[:2]:  # So os dois primeiros
        print(f"\n{name}")
        print("-" * 40)
        
        spectrum = ComputationalSpectrum(L, name)
        
        print("Maiores autovalores:")
        for i, lam in enumerate(spectrum.eigenvalues_sorted[:8]):
            print(f"  lambda_{i}: |{abs(lam):.6f}| (fase: {np.angle(lam):.4f})")
    
    print("\n" + "=" * 70)
    print("5. RESULTADO")
    print("=" * 70)
    
    print("""
    O QUE OBSERVAMOS:
    -----------------
    1. A funcao N_A(T) conta autovalores (analogo dos zeros)
    2. theta_A(T) e a parte suave (lei de Weyl)
    3. S_A(T) = N_A - theta_A sao as flutuacoes
    
    A HIPOTESE DE LEVINSON:
    -----------------------
    S_A(T) / pi_A(T) -> constante
    
    ou seja: flutuacoes espectrais = primos computacionais
    
    VERIFICACAO:
    ------------
    - Em alguns sistemas, a razao S/pi parece estabilizar
    - Em outros, a correlacao e fraca
    - Precisamos de mais analise para conclusoes firmes
    
    SIGNIFICADO (se verdadeiro):
    ----------------------------
    Os "primos" de um algoritmo NAO sao input arbitrario.
    Eles EMERGEM das flutuacoes do espectro.
    
    Isso conectaria:
    - Teoria de numeros (Levinson original)
    - Caos (Ruelle-Pollicott)
    - Computacao (este trabalho)
    
    em um UNICO framework espectral.
    """)
    
    print("=" * 70)


def main():
    demonstrate_levinson()


if __name__ == "__main__":
    main()
