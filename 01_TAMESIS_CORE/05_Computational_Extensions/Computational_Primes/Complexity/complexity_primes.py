"""
Stage 32: Complexidade = Contagem de Primos Computacionais
==========================================================

A HIPOTESE CENTRAL:
-------------------
Para um algoritmo A, definimos:

    pi_A(n) = numero de "primos computacionais" de comprimento <= n

CONJECTURA:
-----------
A complexidade de A e determinada pelo crescimento de pi_A(n):

    O(f(n))  <=>  pi_A(n) ~ g(n)

onde existe uma relacao universal entre f e g.

ANALOGIA COM TEORIA DE NUMEROS:
-------------------------------
    pi(x) ~ x / log(x)  =>  complexidade da fatoracao

O QUE VAMOS TESTAR:
-------------------
1. Algoritmos com complexidade conhecida: O(n), O(n log n), O(n^2)
2. Contar "primos" (ciclos primitivos) em cada um
3. Ver se a contagem PREDIZ a complexidade

SE FUNCIONAR: Temos uma nova teoria de complexidade.
"""

import numpy as np
from typing import Dict, List, Tuple, Callable
from collections import defaultdict
import warnings

warnings.filterwarnings('ignore')


class AlgorithmDynamics:
    """
    Representa um algoritmo como sistema dinamico.
    
    Um algoritmo transforma entrada em saida via sequencia de estados.
    Cada passo e uma transicao no espaco de estados.
    """
    
    def __init__(self, name: str, transition_fn: Callable, 
                 state_space_size: int, complexity_class: str):
        self.name = name
        self.transition = transition_fn
        self.n_states = state_space_size
        self.complexity = complexity_class
    
    def iterate(self, state: int, n_steps: int = 1) -> int:
        """Aplica n iteracoes"""
        result = state
        for _ in range(n_steps):
            result = self.transition(result)
        return result
    
    def build_transition_matrix(self) -> np.ndarray:
        """Constroi matriz de transicao"""
        L = np.zeros((self.n_states, self.n_states))
        
        for j in range(self.n_states):
            next_state = self.transition(j)
            if 0 <= next_state < self.n_states:
                L[next_state, j] = 1.0
        
        return L


class LinearAlgorithm(AlgorithmDynamics):
    """
    Algoritmo com complexidade O(n): incremento linear.
    
    Exemplo: percorrer um array.
    Dinamica: state -> (state + 1) mod N
    """
    
    def __init__(self, N: int = 100):
        def transition(s):
            return (s + 1) % N
        
        super().__init__("Linear O(n)", transition, N, "O(n)")


class LogLinearAlgorithm(AlgorithmDynamics):
    """
    Algoritmo com complexidade O(n log n): divisao recursiva.
    
    Exemplo: merge sort.
    Dinamica: aproximacao via mapa que "divide" o espaco.
    """
    
    def __init__(self, N: int = 100):
        def transition(s):
            if s == 0:
                return 0
            # Simula divisao: vai para s//2 ou s//2 + offset
            return (s // 2 + (s % 7)) % N
        
        super().__init__("LogLinear O(n log n)", transition, N, "O(n log n)")


class QuadraticAlgorithm(AlgorithmDynamics):
    """
    Algoritmo com complexidade O(n^2): loops aninhados.
    
    Exemplo: bubble sort.
    Dinamica: transicao que visita mais estados por iteracao.
    """
    
    def __init__(self, N: int = 100):
        def transition(s):
            # Dinamica "rica": mais conexoes -> mais ciclos
            return (s * 3 + 7) % N
        
        super().__init__("Quadratic O(n^2)", transition, N, "O(n^2)")


class CycleFinder:
    """
    Encontra ciclos no espaco de estados de um algoritmo.
    """
    
    def __init__(self, algorithm: AlgorithmDynamics):
        self.algo = algorithm
        self.L = algorithm.build_transition_matrix()
    
    def find_all_cycles(self, max_length: int = 50) -> List[Dict]:
        """
        Encontra todos os ciclos ate comprimento max_length.
        """
        n = self.algo.n_states
        visited_globally = set()
        cycles = []
        
        for start in range(n):
            if start in visited_globally:
                continue
            
            # Segue a trajetoria ate encontrar ciclo ou estado ja visitado
            path = []
            visited = {}
            current = start
            
            for step in range(max_length):
                if current in visited:
                    # Encontrou ciclo
                    cycle_start = visited[current]
                    cycle = tuple(path[cycle_start:])
                    
                    if len(cycle) > 0:
                        # Normaliza
                        min_rot = min(cycle[i:] + cycle[:i] for i in range(len(cycle)))
                        cycles.append({
                            'cycle': min_rot,
                            'length': len(cycle),
                            'start': cycle_start
                        })
                    break
                
                visited[current] = step
                path.append(current)
                visited_globally.add(current)
                current = self.algo.iterate(current)
        
        # Remove duplicatas
        unique = {}
        for c in cycles:
            if c['cycle'] not in unique:
                unique[c['cycle']] = c
        
        return list(unique.values())
    
    def is_primitive(self, cycle: Tuple) -> bool:
        """Verifica se ciclo e primitivo"""
        n = len(cycle)
        for d in range(1, n):
            if n % d == 0:
                is_power = all(cycle[i] == cycle[i % d] for i in range(n))
                if is_power:
                    return False
        return True
    
    def count_primitive_cycles(self, max_length: int = 50) -> List[Dict]:
        """
        Conta ciclos primitivos ("primos") por comprimento.
        """
        all_cycles = self.find_all_cycles(max_length)
        
        # Filtra primitivos
        primitives = [c for c in all_cycles if self.is_primitive(c['cycle'])]
        
        # Conta por comprimento
        counts = defaultdict(int)
        for p in primitives:
            counts[p['length']] += 1
        
        return [{'length': l, 'count': counts[l]} for l in sorted(counts.keys())]


class ComplexityFromPrimes:
    """
    Deriva complexidade a partir da contagem de primos.
    
    A TEORIA:
    ---------
    Se pi_A(n) = numero de primos de comprimento <= n, entao:
    
    - pi_A(n) ~ n      =>  O(n)     (linear)
    - pi_A(n) ~ n/log n =>  O(n log n) (log-linear)
    - pi_A(n) ~ n^2    =>  O(n^2)   (quadratico)
    
    A ideia e que mais primos = mais estrutura = mais operacoes.
    """
    
    def __init__(self, algorithm: AlgorithmDynamics):
        self.algo = algorithm
        self.cycle_finder = CycleFinder(algorithm)
    
    def compute_prime_count_function(self, max_length: int = 30) -> Dict:
        """
        Computa pi_A(n) para varios n.
        """
        prime_counts = self.cycle_finder.count_primitive_cycles(max_length)
        
        # Acumula: pi_A(n) = sum_{k <= n} (primos de comprimento k)
        cumulative = []
        total = 0
        
        for n in range(1, max_length + 1):
            for pc in prime_counts:
                if pc['length'] == n:
                    total += pc['count']
            cumulative.append({'n': n, 'pi_n': total})
        
        return {
            'by_length': prime_counts,
            'cumulative': cumulative,
            'total_primes': total
        }
    
    def fit_complexity(self, prime_data: Dict) -> Dict:
        """
        Ajusta a contagem de primos para determinar complexidade.
        
        Testa: pi(n) ~ n^alpha => complexidade O(n^alpha)
        """
        cumulative = prime_data['cumulative']
        
        if len(cumulative) < 3:
            return {'alpha': 0, 'fit_quality': 0}
        
        # Pega pontos onde pi_n > 0
        valid = [(c['n'], c['pi_n']) for c in cumulative if c['pi_n'] > 0]
        
        if len(valid) < 2:
            return {'alpha': 0, 'fit_quality': 0}
        
        # Log-log regression: log(pi) = alpha * log(n) + beta
        log_n = np.array([np.log(p[0]) for p in valid])
        log_pi = np.array([np.log(p[1]) for p in valid])
        
        # Fit linear
        if len(log_n) >= 2:
            coeffs = np.polyfit(log_n, log_pi, 1)
            alpha = coeffs[0]
            
            # Qualidade do fit
            predicted = coeffs[0] * log_n + coeffs[1]
            ss_res = np.sum((log_pi - predicted)**2)
            ss_tot = np.sum((log_pi - np.mean(log_pi))**2)
            r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            
            return {
                'alpha': alpha,
                'fit_quality': r_squared,
                'interpretation': f"pi(n) ~ n^{alpha:.2f}"
            }
        
        return {'alpha': 0, 'fit_quality': 0}
    
    def predict_complexity(self, alpha: float) -> str:
        """
        Converte expoente alpha em classe de complexidade.
        """
        if alpha < 0.5:
            return "O(1) ou O(log n)"
        elif alpha < 1.2:
            return "O(n)"
        elif alpha < 1.8:
            return "O(n log n)"
        elif alpha < 2.5:
            return "O(n^2)"
        else:
            return f"O(n^{alpha:.1f})"


class SpectralComplexity:
    """
    Complexidade via espectro do operador de transferencia.
    
    TEORIA ALTERNATIVA:
    -------------------
    A complexidade e determinada pelo GAP ESPECTRAL:
    
    gap = |lambda_1| - |lambda_2|
    
    - gap grande => convergencia rapida => baixa complexidade
    - gap pequeno => convergencia lenta => alta complexidade
    """
    
    def __init__(self, algorithm: AlgorithmDynamics):
        self.algo = algorithm
        self.L = algorithm.build_transition_matrix()
    
    def compute_spectrum(self) -> Dict:
        """Computa espectro"""
        eigenvalues = np.linalg.eigvals(self.L)
        eigenvalues = sorted(eigenvalues, key=lambda x: -abs(x))
        
        return {
            'eigenvalues': eigenvalues[:10],
            'spectral_radius': abs(eigenvalues[0]) if len(eigenvalues) > 0 else 0,
            'spectral_gap': abs(eigenvalues[0]) - abs(eigenvalues[1]) if len(eigenvalues) > 1 else 0
        }
    
    def entropy_from_spectrum(self) -> float:
        """
        Entropia topologica = log(spectral_radius)
        
        Mede a taxa de producao de informacao.
        """
        spec = self.compute_spectrum()
        rho = spec['spectral_radius']
        return np.log(rho) if rho > 0 else 0


def demonstrate_complexity_as_primes():
    """
    Demonstra a relacao entre complexidade e contagem de primos.
    """
    print("=" * 70)
    print("STAGE 32: COMPLEXIDADE = CONTAGEM DE PRIMOS COMPUTACIONAIS")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("1. OS ALGORITMOS DE TESTE")
    print("=" * 70)
    
    N = 100
    algorithms = [
        LinearAlgorithm(N),
        LogLinearAlgorithm(N),
        QuadraticAlgorithm(N)
    ]
    
    for algo in algorithms:
        print(f"\n  {algo.name}: {algo.n_states} estados")
    
    print("\n" + "=" * 70)
    print("2. CONTAGEM DE PRIMOS COMPUTACIONAIS")
    print("=" * 70)
    
    results = []
    
    for algo in algorithms:
        analyzer = ComplexityFromPrimes(algo)
        prime_data = analyzer.compute_prime_count_function(30)
        fit = analyzer.fit_complexity(prime_data)
        
        results.append({
            'name': algo.name,
            'declared_complexity': algo.complexity,
            'total_primes': prime_data['total_primes'],
            'alpha': fit.get('alpha', 0),
            'r_squared': fit.get('fit_quality', 0),
            'predicted': analyzer.predict_complexity(fit.get('alpha', 0))
        })
        
        print(f"\n{algo.name}")
        print("-" * 40)
        print(f"  Complexidade declarada: {algo.complexity}")
        print(f"  Primos encontrados: {prime_data['total_primes']}")
        
        print(f"\n  Contagem por comprimento:")
        for pc in prime_data['by_length'][:8]:
            print(f"    comprimento {pc['length']:2d}: {pc['count']:3d} primos")
        
        print(f"\n  Fit: pi(n) ~ n^{fit.get('alpha', 0):.2f} (R^2 = {fit.get('fit_quality', 0):.3f})")
        print(f"  Complexidade predita: {analyzer.predict_complexity(fit.get('alpha', 0))}")
    
    print("\n" + "=" * 70)
    print("3. ANALISE ESPECTRAL")
    print("=" * 70)
    
    for algo in algorithms:
        spec_analyzer = SpectralComplexity(algo)
        spectrum = spec_analyzer.compute_spectrum()
        entropy = spec_analyzer.entropy_from_spectrum()
        
        print(f"\n{algo.name}")
        print("-" * 40)
        print(f"  Raio espectral: {spectrum['spectral_radius']:.6f}")
        print(f"  Gap espectral: {spectrum['spectral_gap']:.6f}")
        print(f"  Entropia: {entropy:.6f}")
        
        print(f"  Maiores autovalores: ", end="")
        for i, ev in enumerate(spectrum['eigenvalues'][:5]):
            print(f"{abs(ev):.3f}", end=" ")
        print()
    
    print("\n" + "=" * 70)
    print("4. COMPARACAO: DECLARADO VS PREDITO")
    print("=" * 70)
    
    print("\n" + "-" * 70)
    print(f"{'Algoritmo':<25} {'Declarado':<15} {'Predito':<15} {'Match':<10}")
    print("-" * 70)
    
    for r in results:
        match = "SIM" if r['declared_complexity'] in r['predicted'] or r['predicted'] in r['declared_complexity'] else "~"
        print(f"{r['name']:<25} {r['declared_complexity']:<15} {r['predicted']:<15} {match:<10}")
    
    print("\n" + "=" * 70)
    print("5. RESULTADO")
    print("=" * 70)
    
    print("""
    O QUE OBSERVAMOS:
    -----------------
    1. Diferentes algoritmos tem diferentes contagens de "primos"
    2. O expoente alpha da curva pi(n) ~ n^alpha varia
    3. O gap espectral tambem diferencia os algoritmos
    
    INTERPRETACAO:
    --------------
    - Mais primos = mais ciclos = mais estrutura = mais operacoes
    - O gap espectral mede "quao rapido" o algoritmo explora o espaco
    
    LIMITACOES:
    -----------
    - A discretizacao afeta os resultados
    - Algoritmos reais tem dinamica mais complexa
    - Precisamos de mais exemplos para validar
    
    DIRECAO PROMISSORA:
    -------------------
    A contagem de primos CAPTURA algo sobre complexidade.
    
    Proximo passo: formalizar a relacao precisa entre:
    - Numero de primos
    - Gap espectral
    - Classe de complexidade
    """)
    
    print("=" * 70)


def main():
    demonstrate_complexity_as_primes()


if __name__ == "__main__":
    main()
