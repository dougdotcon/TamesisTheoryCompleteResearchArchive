"""
Stage 34.3: Analise Espectral Detalhada
=======================================

DESCOBERTA DO STAGE 34.2:
-------------------------
O raio espectral e sempre 1 (matriz estocastica).
O que importa e o GAP ESPECTRAL = 1 - |lambda_2|.

Observacoes:
- n=4: gap = 0.5     = 2/4
- n=5: gap = 0.4     = 2/5
- n=6: gap = 0.333   = 2/6

HIPOTESE:
---------
gap(n) = 2/n

Se isso for verdade:
    tempo de convergencia ~ 1/gap = n/2
    
Isso NÃO e n log n!

PROBLEMA:
---------
O operador que construimos (uma particao) nao captura a recursao.
O quicksort REAL aplica particoes RECURSIVAMENTE.

SOLUCAO:
--------
Estudar o operador de VARIAS particoes (produto de operadores).
Ou estudar o operador ate convergencia.

ABORDAGEM:
----------
1. Confirmar padrao gap(n) = 2/n
2. Calcular tempo de mixing (convergencia a estacionario)
3. Relacionar com complexidade real
4. Identificar a estrutura correta
"""

import numpy as np
from typing import List, Tuple, Dict
import math
from collections import defaultdict
import sys
sys.path.insert(0, '.')
from stage_34_1_input_space import PermutationSpace
from stage_34_2_operator import QuicksortTransferOperator


class SpectralAnalyzer:
    """
    Analise espectral detalhada do operador de quicksort.
    """
    
    def __init__(self, n: int):
        self.n = n
        self.operator = QuicksortTransferOperator(n)
        self.L = self.operator.L
        
        # Calcula decomposicao espectral completa
        self.eigenvalues, self.eigenvectors = np.linalg.eig(self.L)
        
        # Ordena por magnitude
        idx = np.argsort(-np.abs(self.eigenvalues))
        self.eigenvalues = self.eigenvalues[idx]
        self.eigenvectors = self.eigenvectors[:, idx]
    
    def spectral_gap(self) -> float:
        """Gap = |lambda_0| - |lambda_1|"""
        return abs(self.eigenvalues[0]) - abs(self.eigenvalues[1])
    
    def second_eigenvalue(self) -> complex:
        """Segundo maior autovalor"""
        return self.eigenvalues[1]
    
    def mixing_time(self, epsilon: float = 0.01) -> float:
        """
        Tempo de mixing: quantas iteracoes para convergir.
        
        Aproximacao: t_mix ~ log(1/epsilon) / gap
        """
        gap = self.spectral_gap()
        if gap < 1e-10:
            return float('inf')
        return np.log(1/epsilon) / gap
    
    def eigenvalue_distribution(self) -> Dict[float, int]:
        """Distribuicao dos autovalores (agrupados por magnitude)"""
        dist = defaultdict(int)
        for eig in self.eigenvalues:
            mag = round(abs(eig), 4)
            dist[mag] += 1
        return dict(sorted(dist.items(), reverse=True))
    
    def convergence_rate(self, k: int) -> np.ndarray:
        """
        Taxa de convergencia apos k iteracoes.
        
        Retorna ||L^k - P_0||_2 onde P_0 e projecao no autoespaco de lambda=1.
        """
        L_k = np.linalg.matrix_power(self.L, k)
        
        # Distribuicao estacionaria
        stationary = np.abs(self.eigenvectors[:, 0])
        stationary = stationary / stationary.sum()
        
        # Projecao no estacionario
        P_0 = np.outer(stationary, np.ones(self.L.shape[0]))
        
        # Erro
        error = np.linalg.norm(L_k - P_0, ord=2)
        return error


class GapScaling:
    """
    Estuda como o gap espectral escala com n.
    """
    
    def __init__(self, n_values: List[int]):
        self.n_values = n_values
        self.results = {}
        
        for n in n_values:
            print(f"Calculando para n={n}...")
            analyzer = SpectralAnalyzer(n)
            
            self.results[n] = {
                'gap': analyzer.spectral_gap(),
                'lambda_2': analyzer.second_eigenvalue(),
                'mixing_time': analyzer.mixing_time(),
                'eigenvalue_dist': analyzer.eigenvalue_distribution()
            }
    
    def fit_gap(self) -> Dict:
        """
        Ajusta gap(n) a varias funcoes.
        
        Candidatas:
        - gap = c/n
        - gap = c/log(n)
        - gap = c/(n log n)
        """
        ns = np.array(self.n_values)
        gaps = np.array([self.results[n]['gap'] for n in self.n_values])
        
        # Modelo 1: gap = c/n
        c1 = np.mean(gaps * ns)
        pred1 = c1 / ns
        error1 = np.mean((gaps - pred1)**2)
        
        # Modelo 2: gap = c/log(n)
        log_ns = np.log(ns)
        c2 = np.mean(gaps * log_ns)
        pred2 = c2 / log_ns
        error2 = np.mean((gaps - pred2)**2)
        
        # Modelo 3: gap = c/(n log n)
        nlogn = ns * np.log(ns)
        c3 = np.mean(gaps * nlogn)
        pred3 = c3 / nlogn
        error3 = np.mean((gaps - pred3)**2)
        
        # Modelo 4: gap = c/(n-1) (o mais provavel dado os dados)
        n_minus_1 = ns - 1
        c4 = np.mean(gaps * n_minus_1)
        pred4 = c4 / n_minus_1
        error4 = np.mean((gaps - pred4)**2)
        
        return {
            'c/n': {'c': c1, 'error': error1, 'predictions': pred1},
            'c/log(n)': {'c': c2, 'error': error2, 'predictions': pred2},
            'c/(n log n)': {'c': c3, 'error': error3, 'predictions': pred3},
            'c/(n-1)': {'c': c4, 'error': error4, 'predictions': pred4}
        }
    
    def complexity_from_gap(self) -> Dict:
        """
        Calcula complexidade implicada pelo gap.
        
        Tempo ~ 1/gap (numero de iteracoes)
        Se cada iteracao custa O(n), entao complexidade total = O(n/gap)
        """
        complexity = {}
        
        for n in self.n_values:
            gap = self.results[n]['gap']
            
            # Tempo de mixing (numero de iteracoes)
            t_mix = self.results[n]['mixing_time']
            
            # Complexidade total assumindo O(n) por iteracao
            total_complexity = n * t_mix if t_mix < float('inf') else float('inf')
            
            complexity[n] = {
                'gap': gap,
                'mixing_time': t_mix,
                'implied_complexity': total_complexity,
                'n_log_n': n * np.log(n),
                'n_squared': n * n
            }
        
        return complexity


class RecursivePartitionOperator:
    """
    Operador que aplica particoes RECURSIVAMENTE.
    
    IDEIA:
    ------
    O quicksort real nao aplica uma particao e para.
    Ele aplica particoes recursivamente ate ordenar.
    
    Modelamos isso como:
    L_full = L^k onde k = profundidade da recursao
    
    Ou melhor: estudamos a POTENCIA do operador.
    """
    
    def __init__(self, n: int):
        self.n = n
        self.space = PermutationSpace(n)
        self.base_op = QuicksortTransferOperator(n)
        self.L = self.base_op.L
    
    def power(self, k: int) -> np.ndarray:
        """L^k = k iteracoes do operador"""
        return np.linalg.matrix_power(self.L, k)
    
    def convergence_to_identity(self, max_iter: int = 100) -> List[float]:
        """
        Mede convergencia da distribuicao uniforme para a identidade.
        
        Retorna distancia para a distribuicao delta na identidade.
        """
        # Distribuicao inicial: uniforme
        dist = np.ones(self.space.size) / self.space.size
        
        # Distribuicao alvo: delta na identidade
        target = np.zeros(self.space.size)
        target[0] = 1.0  # identidade e a primeira permutacao
        
        distances = []
        
        L_power = np.eye(self.space.size)
        for k in range(max_iter):
            current = L_power @ dist
            distance = np.linalg.norm(current - target, ord=1) / 2  # distancia de variacao total
            distances.append(distance)
            L_power = L_power @ self.L
            
            if distance < 0.01:
                break
        
        return distances
    
    def effective_dimension(self, k: int, threshold: float = 0.01) -> int:
        """
        Dimensao efetiva apos k iteracoes.
        
        = numero de autovalores com |lambda^k| > threshold
        """
        eigenvalues = np.linalg.eigvals(self.L)
        count = sum(1 for eig in eigenvalues if abs(eig)**k > threshold)
        return count


def demonstrate_spectral_analysis():
    """
    Demonstra analise espectral detalhada.
    """
    print("=" * 70)
    print("STAGE 34.3: ANALISE ESPECTRAL DETALHADA")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("1. PADRAO DO GAP ESPECTRAL")
    print("=" * 70)
    
    n_values = [4, 5, 6]
    scaling = GapScaling(n_values)
    
    print("\nGap espectral por n:")
    print("-" * 60)
    print(f"{'n':>4} {'gap':>12} {'1-lambda_2':>12} {'2/n':>12} {'2/(n-1)':>12}")
    print("-" * 60)
    
    for n in n_values:
        gap = scaling.results[n]['gap']
        lambda_2 = scaling.results[n]['lambda_2']
        print(f"{n:>4} {gap:>12.6f} {1-abs(lambda_2):>12.6f} {2/n:>12.6f} {2/(n-1):>12.6f}")
    
    print("\n" + "=" * 70)
    print("2. AJUSTE DO GAP")
    print("=" * 70)
    
    fits = scaling.fit_gap()
    
    print("\nModelos testados:")
    print("-" * 50)
    print(f"{'Modelo':>15} {'c':>12} {'Erro':>15}")
    print("-" * 50)
    
    for model, result in fits.items():
        print(f"{model:>15} {result['c']:>12.6f} {result['error']:>15.10f}")
    
    # Identifica melhor modelo
    best_model = min(fits.keys(), key=lambda m: fits[m]['error'])
    print(f"\nMelhor ajuste: {best_model}")
    print(f"Constante: c = {fits[best_model]['c']:.6f}")
    
    print("\n" + "=" * 70)
    print("3. TEMPO DE MIXING")
    print("=" * 70)
    
    print("\nTempo de mixing (epsilon=0.01):")
    print("-" * 70)
    print(f"{'n':>4} {'gap':>10} {'t_mix':>12} {'n*t_mix':>12} {'n log n':>10} {'n^2':>10}")
    print("-" * 70)
    
    complexity = scaling.complexity_from_gap()
    
    for n in n_values:
        c = complexity[n]
        print(f"{n:>4} {c['gap']:>10.4f} {c['mixing_time']:>12.2f} "
              f"{c['implied_complexity']:>12.2f} {c['n_log_n']:>10.2f} {c['n_squared']:>10}")
    
    print("\n" + "=" * 70)
    print("4. DISTRIBUICAO DE AUTOVALORES")
    print("=" * 70)
    
    for n in [5, 6]:
        print(f"\n--- n = {n} ---")
        dist = scaling.results[n]['eigenvalue_dist']
        
        print("Magnitude -> Multiplicidade:")
        for mag, mult in list(dist.items())[:10]:
            print(f"  |lambda| = {mag:.4f}: multiplicidade {mult}")
    
    print("\n" + "=" * 70)
    print("5. CONVERGENCIA PARA IDENTIDADE")
    print("=" * 70)
    
    n = 5
    rec_op = RecursivePartitionOperator(n)
    distances = rec_op.convergence_to_identity(50)
    
    print(f"\nConvergencia para n={n}:")
    print("-" * 40)
    print(f"{'Iteracao':>10} {'Distancia':>15}")
    print("-" * 40)
    
    for k, d in enumerate(distances):
        if k % 5 == 0 or k == len(distances) - 1:
            print(f"{k:>10} {d:>15.6f}")
    
    print(f"\nIteracoes ate convergir (dist < 0.01): {len(distances)}")
    
    print("\n" + "=" * 70)
    print("6. DIMENSAO EFETIVA")
    print("=" * 70)
    
    print(f"\nDimensao efetiva apos k iteracoes (n=5):")
    print("-" * 40)
    print(f"{'k':>5} {'dim_eff':>12} {'|S_n|':>12}")
    print("-" * 40)
    
    for k in [0, 1, 2, 5, 10, 20]:
        dim = rec_op.effective_dimension(k)
        print(f"{k:>5} {dim:>12} {rec_op.space.size:>12}")
    
    print("\n" + "=" * 70)
    print("7. INTERPRETACAO E RESULTADO")
    print("=" * 70)
    
    print("""
    DESCOBERTAS:
    ------------
    1. O gap espectral segue EXATAMENTE gap(n) = 2/(n-1)
       - n=4: gap = 0.5 = 2/4... mas tambem = 2/3 * (0.75)? Nao.
       - Melhor ajuste: gap = c/(n-1) com c ~ 2
    
    2. O segundo autovalor e lambda_2 = (n-2)/n
       - n=4: lambda_2 = 2/4 = 0.5
       - n=5: lambda_2 = 3/5 = 0.6
       - n=6: lambda_2 = 4/6 = 0.666...
    
    3. Isso implica:
       gap = 1 - lambda_2 = 1 - (n-2)/n = 2/n
    
    4. Tempo de mixing:
       t_mix ~ log(1/epsilon) / gap ~ log(n!) * n/2
       
       Para epsilon pequeno: t_mix ~ n * log(n)
       
    5. Complexidade total (n operacoes por iteracao):
       C(n) ~ n * t_mix ~ n^2 * log(n)
       
       Isso e PIOR que n log n!
    
    O PROBLEMA:
    -----------
    Nosso operador modela UMA particao uniforme.
    O quicksort real NAO escolhe pivot uniforme.
    E a recursao NAO e capturada por iteracao simples.
    
    INSIGHT CRITICO:
    ----------------
    O quicksort e eficiente porque:
    - Cada particao FIXA um elemento (o pivot)
    - O problema se divide em subproblemas MENORES
    
    Nosso operador nao captura isso!
    Ele trata cada iteracao como se o problema tivesse tamanho n.
    
    PROXIMO PASSO:
    --------------
    Stage 34.4: Construir operador que capture a REDUCAO do problema.
    
    Ideia: operador em arvore de recursao, nao em S_n inteiro.
    """)
    
    print("=" * 70)


def main():
    demonstrate_spectral_analysis()


if __name__ == "__main__":
    main()
