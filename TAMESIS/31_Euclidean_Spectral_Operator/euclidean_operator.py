"""
Stage 31: Operador Espectral do Algoritmo de Euclides
=====================================================

A PERGUNTA FUNDACIONAL:
-----------------------
Qual e o operador canonico L_A associado a um algoritmo A?

O CASO DE TESTE: ALGORITMO DE EUCLIDES
--------------------------------------
gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

Por que Euclides:
1. Simples o suficiente para analise completa
2. Complexidade conhecida: O(log(min(a,b))) em media
3. Estrutura de Fibonacci e conhecida (pior caso)
4. Conexao com fracoes continuas (geometria hiperbolica!)

O OPERADOR:
-----------
Definimos L_E como operador de transferencia no espaco de estados (a, b).

A dinamica e:
    T(a, b) = (b, a mod b)

O operador L_E age em funcoes f: N x N -> C:
    (L_E f)(a, b) = sum_{(a', b'): T(a', b') = (a, b)} f(a', b') / J(a', b')

onde J e o Jacobiano (numero de pre-imagens).

A ZETA DO EUCLIDES:
-------------------
Z_E(s) = det(I - e^{-s} L_E)^{-1}

OBJETIVO:
---------
1. Construir L_E explicitamente
2. Encontrar ciclos primitivos = "primos de Euclides"
3. Verificar se log Z_E satisfaz formula explicita
4. Conectar espectro com complexidade
"""

import numpy as np
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import warnings

warnings.filterwarnings('ignore')


class EuclideanDynamics:
    """
    A dinamica do algoritmo de Euclides como sistema dinamico.
    
    Estado: (a, b) com a >= b > 0
    Transicao: T(a, b) = (b, a mod b)
    Estado final: b = 0
    """
    
    def __init__(self, max_val: int = 100):
        self.max_val = max_val
    
    def step(self, a: int, b: int) -> Tuple[int, int]:
        """Um passo do algoritmo de Euclides"""
        if b == 0:
            return (a, 0)
        return (b, a % b)
    
    def full_trajectory(self, a: int, b: int) -> List[Tuple[int, int]]:
        """Trajetoria completa ate gcd"""
        trajectory = [(a, b)]
        while b != 0:
            a, b = self.step(a, b)
            trajectory.append((a, b))
        return trajectory
    
    def step_count(self, a: int, b: int) -> int:
        """Numero de passos ate terminar"""
        count = 0
        while b != 0:
            a, b = self.step(a, b)
            count += 1
        return count
    
    def quotient_sequence(self, a: int, b: int) -> List[int]:
        """
        Sequencia de quocientes (fracao continua).
        
        gcd(a, b) via Euclides produz a fracao continua de a/b.
        """
        quotients = []
        while b != 0:
            q = a // b
            quotients.append(q)
            a, b = b, a % b
        return quotients


class GaussMapTransferOperator:
    """
    O MAPA DE GAUSS: a versao "infinita" do algoritmo de Euclides.
    
    DEFINICAO:
    ----------
    T(x) = 1/x - floor(1/x)  para x em (0, 1]
    T(0) = 0
    
    Este e o mapa que gera fracoes continuas:
    x = 1/(a1 + 1/(a2 + ...))  =>  a_n = floor(1/T^{n-1}(x))
    
    PROPRIEDADES:
    -------------
    - Caotico, ergodico
    - Medida invariante: mu(dx) = dx / ((1 + x) * log 2)
    - Entropia: log 2 (bits por iteracao)
    
    O OPERADOR DE TRANSFERENCIA:
    ----------------------------
    (L f)(x) = sum_{n=1}^infty (1/(x+n)^2) * f(1/(x+n))
    
    Este e o operador de Perron-Frobenius para o mapa de Gauss.
    
    ESPECTRO:
    ---------
    - Autovalor 1: medida invariante
    - Outros autovalores: taxas de mixing
    - Gap espectral: taxa de convergencia
    """
    
    def __init__(self, N: int = 50):
        self.N = N  # Discretizacao
        
        # Grade em (0, 1]
        self.grid = np.linspace(1/N, 1, N)
        self.dx = 1 / N
        
        # Matriz de transferencia
        self.L = None
        self._build_transfer_matrix()
    
    def gauss_map(self, x: float) -> float:
        """O mapa de Gauss: T(x) = 1/x - floor(1/x)"""
        if x <= 0:
            return 0.0
        return 1/x - np.floor(1/x)
    
    def _build_transfer_matrix(self):
        """
        Constroi matriz de transferencia via discretizacao.
        
        L[i, j] ~ probabilidade de ir de celula j para celula i
        """
        self.L = np.zeros((self.N, self.N))
        
        for j in range(self.N):
            x_j = self.grid[j]
            
            # O mapa de Gauss tem multiplas pre-imagens
            # Pre-imagem de y: x = 1/(n + y) para n = 1, 2, 3, ...
            for n in range(1, self.N + 1):
                # Pre-imagem
                x_pre = 1 / (n + x_j)
                
                if x_pre <= 0 or x_pre > 1:
                    continue
                
                # Encontra celula da pre-imagem
                i = int(x_pre * self.N) - 1
                i = max(0, min(self.N - 1, i))
                
                # Peso: derivada da inversa = 1/(n+y)^2
                weight = 1 / (n + x_j)**2
                
                self.L[j, i] += weight
        
        # Normaliza colunas (operador estocastico)
        col_sums = self.L.sum(axis=0, keepdims=True)
        col_sums[col_sums == 0] = 1
        self.L = self.L / col_sums
    
    def spectrum(self, n_eigenvalues: int = 20) -> np.ndarray:
        """Calcula os maiores autovalores"""
        eigenvalues = np.linalg.eigvals(self.L)
        eigenvalues = sorted(eigenvalues, key=lambda x: -abs(x))
        return np.array(eigenvalues[:n_eigenvalues])
    
    def spectral_gap(self) -> float:
        """Gap espectral = |lambda_1| - |lambda_2|"""
        eigs = self.spectrum(5)
        if len(eigs) < 2:
            return 0.0
        return abs(eigs[0]) - abs(eigs[1])
    
    def invariant_measure(self) -> np.ndarray:
        """
        Medida invariante (autovetor com autovalor 1).
        
        Teorica: mu(x) = 1 / ((1 + x) * log 2)
        """
        # Autovetor a esquerda com autovalor 1
        eigenvalues, eigenvectors = np.linalg.eig(self.L.T)
        
        idx = np.argmax(np.abs(eigenvalues))
        measure = np.abs(eigenvectors[:, idx])
        measure = measure / measure.sum()
        
        return measure


class EuclideanTransferOperator:
    """
    Wrapper que usa o mapa de Gauss (versao correta).
    """
    
    def __init__(self, N: int = 50):
        self.gauss = GaussMapTransferOperator(N)
        self.N = N
        self.n_states = N
        self.L = self.gauss.L
    
    def spectrum(self, n_eigenvalues: int = 20) -> np.ndarray:
        return self.gauss.spectrum(n_eigenvalues)
    
    def spectral_gap(self) -> float:
        return self.gauss.spectral_gap()


class EuclideanCycles:
    """
    Ciclos no espaco de estados do algoritmo de Euclides.
    
    FATO CRUCIAL:
    -------------
    O algoritmo de Euclides NAO tem ciclos infinitos!
    Ele sempre termina.
    
    MAS: podemos estudar ciclos no "espaco estendido"
    onde consideramos a dinamica modular T(a, b) = (b, a mod b)
    sem a condicao de parada.
    
    ALTERNATIVA:
    ------------
    Estudar ciclos na FRACAO CONTINUA associada.
    Fracoes continuas periodicas <-> numeros quadraticos.
    """
    
    def __init__(self, N: int = 100):
        self.N = N
        self.dynamics = EuclideanDynamics(N)
    
    def find_periodic_continued_fractions(self, max_period: int = 10) -> List[Dict]:
        """
        Encontra fracoes continuas periodicas.
        
        Fracao continua [a0; a1, a2, ...] e periodica se
        existe k tal que a_{n+k} = a_n para todo n suficientemente grande.
        
        Isso corresponde a sqrt(D) para D nao-quadrado perfeito.
        """
        periodic = []
        
        # Para cada D nao-quadrado, sqrt(D) tem fracao continua periodica
        for D in range(2, self.N):
            sqrt_D = np.sqrt(D)
            if sqrt_D == int(sqrt_D):
                continue  # Quadrado perfeito
            
            # Gera fracao continua de sqrt(D)
            cf = self._continued_fraction_sqrt(D, max_terms=2 * max_period)
            
            # Encontra periodo
            period = self._find_period(cf)
            
            if period and period <= max_period:
                periodic.append({
                    'D': D,
                    'sqrt_D': sqrt_D,
                    'continued_fraction': cf[:period + 5],
                    'period': period,
                    'periodic_part': cf[1:period + 1] if period else []
                })
        
        return periodic
    
    def _continued_fraction_sqrt(self, D: int, max_terms: int = 50) -> List[int]:
        """
        Fracao continua de sqrt(D).
        
        sqrt(D) = a0 + 1/(a1 + 1/(a2 + ...))
        """
        a0 = int(np.sqrt(D))
        cf = [a0]
        
        # Algoritmo para sqrt(D)
        m, d, a = 0, 1, a0
        seen = {}
        
        for _ in range(max_terms):
            m = d * a - m
            d = (D - m * m) // d
            if d == 0:
                break
            a = (a0 + m) // d
            
            state = (m, d)
            if state in seen:
                break
            seen[state] = len(cf)
            cf.append(a)
        
        return cf
    
    def _find_period(self, cf: List[int]) -> int:
        """Encontra periodo da parte periodica"""
        if len(cf) < 3:
            return 0
        
        # Procura repeticao
        for period in range(1, len(cf) // 2):
            is_periodic = True
            for i in range(period, min(2 * period, len(cf) - 1)):
                if cf[i] != cf[i - period + 1]:
                    is_periodic = False
                    break
            if is_periodic:
                return period
        
        return 0


class EuclideanZeta:
    """
    A funcao zeta do MAPA DE GAUSS (algoritmo de Euclides infinito).
    
    DEFINICAO:
    ----------
    Z_G(s) = det(I - e^{-s} L_G)^{-1}
    
    Via formula de traco:
    log Z_G(s) = sum_n (1/n) Tr(L_G^n) e^{-ns}
    
    INTERPRETACAO:
    --------------
    - Tr(L_G^n) = numero de trajetorias periodicas de comprimento n
    - "Primos de Gauss" = orbitas primitivas
    
    CONEXAO COM COMPLEXIDADE:
    -------------------------
    O polo dominante de Z_G(s) determina:
    - Taxa de producao de entropia
    - Bits por iteracao ~ log 2
    """
    
    def __init__(self, N: int = 30):
        self.transfer = EuclideanTransferOperator(N)
        self.L = self.transfer.L
        self.n_states = self.transfer.N
    
    def trace_power(self, n: int) -> float:
        """Tr(L^n) = numero de caminhos fechados de comprimento n"""
        L_n = np.linalg.matrix_power(self.L, n)
        return np.trace(L_n)
    
    def zeta_determinant(self, s: complex) -> complex:
        """
        Z_E(s) = 1 / det(I - e^{-s} L)
        """
        I = np.eye(self.n_states)
        M = I - np.exp(-s) * self.L
        
        det_val = np.linalg.det(M)
        
        if abs(det_val) < 1e-15:
            return complex('inf')
        
        return 1.0 / det_val
    
    def log_zeta_from_traces(self, s: complex, max_n: int = 20) -> complex:
        """
        log Z(s) = sum_n (1/n) Tr(L^n) e^{-ns}
        
        Esta e a formula de orbitas!
        """
        log_z = 0.0
        
        for n in range(1, max_n + 1):
            tr_n = self.trace_power(n)
            if tr_n > 0:
                log_z += (1.0 / n) * tr_n * np.exp(-n * s)
        
        return log_z
    
    def find_primitive_orbits(self, max_length: int = 10) -> List[Dict]:
        """
        Encontra "orbitas primitivas" = "primos de Euclides".
        
        Uma orbita de comprimento n e primitiva se nao e
        repeticao de orbita menor.
        """
        primitives = []
        
        for n in range(1, max_length + 1):
            # Tr(L^n) inclui todas as orbitas de comprimento n
            tr_n = self.trace_power(n)
            
            # Subtrai contribuicoes de orbitas menores (Mobius)
            primitive_count = tr_n
            for d in range(1, n):
                if n % d == 0:
                    tr_d = self.trace_power(d)
                    # Cada orbita de comprimento d contribui n/d vezes em Tr(L^n)
                    primitive_count -= tr_d
            
            primitive_orbits = primitive_count / n if n > 0 else 0
            
            primitives.append({
                'length': n,
                'trace': tr_n,
                'primitive_count': max(0, int(round(primitive_orbits))),
                'log_count': np.log(max(1, primitive_orbits)) if primitive_orbits > 0 else 0
            })
        
        return primitives
    
    def complexity_from_zeta(self) -> Dict:
        """
        Extrai informacao de complexidade da zeta.
        
        O polo dominante de Z(s) em Re(s) = sigma_0 implica:
        - Numero de trajetorias de comprimento n ~ e^{sigma_0 * n}
        - Complexidade media ~ sigma_0^{-1}
        """
        # Encontra polo dominante via espectro de L
        eigenvalues = np.linalg.eigvals(self.L)
        max_eigenvalue = max(abs(eigenvalues))
        
        # Polo em s_0 onde e^{-s_0} = lambda_max
        # Ou seja: s_0 = -log(lambda_max)
        if max_eigenvalue > 0:
            s_0 = -np.log(max_eigenvalue)
        else:
            s_0 = float('inf')
        
        return {
            'max_eigenvalue': max_eigenvalue,
            'dominant_pole': s_0,
            'growth_rate': max_eigenvalue,
            'interpretation': f"Trajetorias crescem como {max_eigenvalue:.4f}^n"
        }


def demonstrate_euclidean_spectral():
    """
    Demonstra o operador espectral do algoritmo de Euclides.
    """
    print("=" * 70)
    print("STAGE 31: OPERADOR ESPECTRAL DO ALGORITMO DE EUCLIDES")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("1. O ALGORITMO COMO SISTEMA DINAMICO")
    print("=" * 70)
    
    dynamics = EuclideanDynamics()
    
    print("\nExemplo: gcd(89, 55) - numeros de Fibonacci")
    trajectory = dynamics.full_trajectory(89, 55)
    quotients = dynamics.quotient_sequence(89, 55)
    
    print(f"Trajetoria: {trajectory}")
    print(f"Quocientes (fracao continua): {quotients}")
    print(f"Numero de passos: {dynamics.step_count(89, 55)}")
    
    print("\n" + "=" * 70)
    print("2. OPERADOR DE TRANSFERENCIA L_E")
    print("=" * 70)
    
    N = 30
    transfer = EuclideanTransferOperator(N)
    
    print(f"\nEspaco de estados: {transfer.n_states} estados (pares (a,b) com b <= a <= {N})")
    print(f"Matriz L_E: {transfer.n_states} x {transfer.n_states}")
    
    print("\nEspectro de L_E (maiores autovalores):")
    spectrum = transfer.spectrum(10)
    
    for i, eig in enumerate(spectrum[:10]):
        print(f"  lambda_{i}: {abs(eig):.6f}")
    
    print(f"\nGap espectral: {transfer.spectral_gap():.6f}")
    
    print("\n" + "=" * 70)
    print("3. ZETA DO EUCLIDES")
    print("=" * 70)
    
    zeta = EuclideanZeta(N)
    
    print("\nZ_E(s) = det(I - e^{-s} L)^{-1}")
    print("\nValores:")
    print("-" * 50)
    print(f"{'s':>8} {'|Z_E(s)|':>15} {'log Z (trace)':>18}")
    print("-" * 50)
    
    for s in [0.5, 1.0, 1.5, 2.0, 2.5]:
        z_det = zeta.zeta_determinant(s)
        log_z_trace = zeta.log_zeta_from_traces(s)
        print(f"{s:8.1f} {abs(z_det):15.6f} {log_z_trace.real:18.6f}")
    
    print("\n" + "=" * 70)
    print("4. PRIMOS DE EUCLIDES (ORBITAS PRIMITIVAS)")
    print("=" * 70)
    
    print("\n'Primos' = orbitas primitivas no espaco de estados")
    print("-" * 50)
    print(f"{'Comprimento':>12} {'Tr(L^n)':>12} {'N primitivas':>14}")
    print("-" * 50)
    
    primitives = zeta.find_primitive_orbits(12)
    
    for p in primitives:
        print(f"{p['length']:12d} {p['trace']:12.0f} {p['primitive_count']:14d}")
    
    print("\n" + "=" * 70)
    print("5. COMPLEXIDADE VIA ZETA")
    print("=" * 70)
    
    complexity = zeta.complexity_from_zeta()
    
    print(f"\nAutovalor dominante: {complexity['max_eigenvalue']:.6f}")
    print(f"Polo dominante: s_0 = {complexity['dominant_pole']:.6f}")
    print(f"Interpretacao: {complexity['interpretation']}")
    
    print("\n" + "=" * 70)
    print("6. FRACOES CONTINUAS PERIODICAS")
    print("=" * 70)
    
    cycles = EuclideanCycles(50)
    periodic = cycles.find_periodic_continued_fractions(8)
    
    print("\nFracoes continuas periodicas (sqrt(D)):")
    print("-" * 60)
    
    for p in periodic[:10]:
        cf_str = str(p['continued_fraction'][:6])
        print(f"  sqrt({p['D']:2d}) = {p['sqrt_D']:.4f}, periodo={p['period']}, "
              f"CF={cf_str}...")
    
    print("\n" + "=" * 70)
    print("7. RESULTADO")
    print("=" * 70)
    
    print("""
    O QUE CONSTRUIMOS:
    ------------------
    1. Operador de transferencia L_E para Euclides
    2. Zeta do algoritmo: Z_E(s) = det(I - e^{-s} L)^{-1}
    3. "Primos de Euclides" = orbitas primitivas
    4. Conexao: autovalor dominante -> taxa de crescimento
    
    OBSERVACOES:
    ------------
    - O algoritmo de Euclides NAO tem ciclos infinitos (sempre termina)
    - Mas o operador L_E captura a ESTRUTURA TRANSIENTE
    - Tr(L^n) conta caminhos de comprimento n
    - O espectro determina taxas de convergencia
    
    CONEXAO COM COMPLEXIDADE:
    -------------------------
    - Euclides tem complexidade O(log(min(a,b)))
    - Isso corresponde ao decaimento exponencial de Tr(L^n)
    - O gap espectral mede "quao rapido" o algoritmo converge
    
    PROXIMO PASSO:
    --------------
    Stage 32: Formalizar "complexidade = contagem de primos"
    """)
    
    print("=" * 70)


def main():
    demonstrate_euclidean_spectral()


if __name__ == "__main__":
    main()
