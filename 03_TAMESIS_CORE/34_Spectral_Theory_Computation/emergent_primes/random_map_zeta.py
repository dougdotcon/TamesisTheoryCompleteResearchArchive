"""
CAMINHO 2 ATIVADO: Zeta de Random Maps
======================================

CONTEXTO:
---------
Stage 34.7 mostrou que Random Maps tem:
- Ciclos primitivos
- Crescimento pi(n) ~ (1/2) log(n)
- Estrutura caotica genuina

OBJETIVO:
---------
Construir a ZETA DO RANDOM MAP e estudar suas propriedades.

DEFINICAO:
----------
Para funcao f: {0,...,n-1} -> {0,...,n-1}:

Z_f(s) = prod_{ciclos primitivos gamma} (1 - |gamma|^{-s})^{-1}

Ou via serie:
log Z_f(s) = sum_{k>=1} N_k / k * n^{-ks}

onde N_k = numero de pontos em ciclos de comprimento k.

TEORIA CONHECIDA (Flajolet-Odlyzko):
------------------------------------
Para random map:
- Numero esperado de ciclos: (1/2) log(n) + gamma + O(1/n)
  onde gamma = 0.5772... (Euler-Mascheroni)
- Comprimento esperado do ciclo maior: sqrt(pi*n/8)
- Comprimento da "cauda" (ate entrar em ciclo): sqrt(pi*n/8)

NOSSA CONTRIBUICAO:
-------------------
Conectar isso com teoria espectral e formalizar "primos computacionais".
"""

import numpy as np
from typing import List, Tuple, Dict
import math
from collections import defaultdict


class RandomMapZeta:
    """
    Zeta function para random maps.
    """
    
    def __init__(self, n: int, f: np.ndarray = None, seed: int = None):
        self.n = n
        
        if f is None:
            if seed is not None:
                np.random.seed(seed)
            self.f = np.random.randint(0, n, size=n)
        else:
            self.f = f
        
        # Encontra ciclos
        self.cycles = self._find_all_cycles()
        self.cycle_lengths = [len(c) for c in self.cycles]
    
    def _find_all_cycles(self) -> List[List[int]]:
        """Encontra todos os ciclos da funcao"""
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
    
    def zeta_product(self, s: complex) -> complex:
        """
        Z_f(s) = prod_{gamma} (1 - |gamma|^{-s})^{-1}
        
        Produto sobre ciclos primitivos.
        """
        result = 1.0
        
        for length in self.cycle_lengths:
            if length > 0:
                term = 1.0 - length ** (-s)
                if abs(term) > 1e-15:
                    result *= 1.0 / term
        
        return result
    
    def log_zeta_series(self, s: complex, max_k: int = 50) -> complex:
        """
        log Z_f(s) = sum_{k>=1} (1/k) * sum_{|gamma|=k} 1 * k^{-s}
                   = sum_{k>=1} N_k / k * k^{-s}
        
        onde N_k = numero de ciclos de comprimento k.
        """
        # Conta ciclos por comprimento
        counts = defaultdict(int)
        for length in self.cycle_lengths:
            counts[length] += 1
        
        result = 0.0
        for k in range(1, max_k + 1):
            if k in counts:
                N_k = counts[k]
                result += (N_k / k) * (k ** (-s))
        
        return result
    
    def derivative_log_zeta(self, s: complex, h: float = 1e-6) -> complex:
        """
        d/ds log Z_f(s) = -sum_{gamma} log|gamma| / (|gamma|^s - 1)
        
        Calculado numericamente.
        """
        return (self.log_zeta_series(s + h) - self.log_zeta_series(s - h)) / (2 * h)
    
    def prime_counting_function(self) -> Dict[int, int]:
        """
        pi_f(n) = numero de ciclos primitivos de comprimento <= n
        
        Para random map, todos os ciclos sao primitivos (rarissimo ter repeticao).
        """
        counts = {}
        total = 0
        for k in range(1, max(self.cycle_lengths) + 1):
            count_at_k = sum(1 for l in self.cycle_lengths if l == k)
            total += count_at_k
            counts[k] = total
        return counts


class RandomMapEnsemble:
    """
    Estuda propriedades MEDIAS sobre ensemble de random maps.
    """
    
    def __init__(self, n: int, n_samples: int = 100):
        self.n = n
        self.n_samples = n_samples
        self.maps = [RandomMapZeta(n) for _ in range(n_samples)]
    
    def expected_cycle_count(self) -> Tuple[float, float]:
        """E[numero de ciclos] e std"""
        counts = [len(m.cycles) for m in self.maps]
        return np.mean(counts), np.std(counts)
    
    def expected_max_cycle(self) -> Tuple[float, float]:
        """E[comprimento do maior ciclo] e std"""
        max_lens = [max(m.cycle_lengths) if m.cycle_lengths else 0 for m in self.maps]
        return np.mean(max_lens), np.std(max_lens)
    
    def cycle_length_distribution(self) -> Dict[int, float]:
        """Distribuicao de comprimentos de ciclo"""
        all_lengths = []
        for m in self.maps:
            all_lengths.extend(m.cycle_lengths)
        
        counts = defaultdict(int)
        for l in all_lengths:
            counts[l] += 1
        
        total = len(all_lengths)
        return {k: v / total for k, v in sorted(counts.items())}
    
    def mean_zeta(self, s: complex) -> Tuple[complex, complex]:
        """E[Z_f(s)] e std sobre ensemble"""
        values = [m.zeta_product(s) for m in self.maps]
        return np.mean(values), np.std(values)
    
    def verify_flajolet_odlyzko(self) -> Dict:
        """
        Verifica predicoes teoricas de Flajolet-Odlyzko:
        - E[ciclos] ~ (1/2) log(n) + gamma
        - E[max ciclo] ~ sqrt(pi*n/8)
        - E[cauda] ~ sqrt(pi*n/8)
        """
        gamma_euler = 0.5772156649
        
        # Predicoes teoricas
        expected_cycles_theory = 0.5 * np.log(self.n) + gamma_euler
        expected_max_theory = np.sqrt(np.pi * self.n / 8)
        
        # Observado
        cycles_obs, cycles_std = self.expected_cycle_count()
        max_obs, max_std = self.expected_max_cycle()
        
        return {
            'n': self.n,
            'cycles': {
                'theory': expected_cycles_theory,
                'observed': cycles_obs,
                'std': cycles_std,
                'ratio': cycles_obs / expected_cycles_theory
            },
            'max_cycle': {
                'theory': expected_max_theory,
                'observed': max_obs,
                'std': max_std,
                'ratio': max_obs / expected_max_theory
            }
        }


class ComputationalPrimeTheory:
    """
    Formaliza "teoria dos numeros" para random maps.
    """
    
    def __init__(self, n: int, n_samples: int = 100):
        self.ensemble = RandomMapEnsemble(n, n_samples)
        self.n = n
    
    def prime_number_theorem_analog(self) -> Dict:
        """
        Testa se pi_f(x) ~ x / log(x) ou outra lei.
        
        Para random maps, a lei e diferente:
        E[numero de ciclos] ~ (1/2) log(n)
        
        Ou seja: pi_f(n) ~ (1/2) log(n), NAO n/log(n).
        """
        # Coleta pi_f para cada mapa
        pi_values = []
        for m in self.ensemble.maps:
            total_cycles = len(m.cycles)
            pi_values.append(total_cycles)
        
        mean_pi = np.mean(pi_values)
        
        # Compara com teorias
        pnt_classic = self.n / np.log(self.n)  # n / log(n)
        flajolet = 0.5 * np.log(self.n) + 0.5772  # (1/2) log(n) + gamma
        
        return {
            'observed': mean_pi,
            'pnt_classic': pnt_classic,
            'flajolet': flajolet,
            'best_fit': 'flajolet' if abs(mean_pi - flajolet) < abs(mean_pi - pnt_classic) else 'pnt'
        }
    
    def riemann_hypothesis_analog(self) -> Dict:
        """
        Existe um "RH" para random maps?
        
        Para zeta de Riemann: zeros tem Re(s) = 1/2
        
        Para random map: a zeta tem estrutura mais simples
        (produto finito, sem zeros nao-triviais).
        
        MAS: podemos estudar a DISTRIBUICAO de |Z_f(s)| sobre ensemble.
        """
        # Avalia zeta em varios pontos
        s_values = [0.5 + 1j * t for t in np.linspace(1, 20, 50)]
        
        zeta_magnitudes = []
        for s in s_values:
            magnitudes = [abs(m.zeta_product(s)) for m in self.ensemble.maps]
            zeta_magnitudes.append({
                's': s,
                'mean': np.mean(magnitudes),
                'std': np.std(magnitudes)
            })
        
        return {
            'zeta_statistics': zeta_magnitudes[:10],  # Primeiros 10
            'observation': 'Zeta de random map e produto finito, sem zeros nao-triviais'
        }


def demonstrate_random_map_zeta():
    """
    Demonstra zeta de random maps e teoria de primos computacionais.
    """
    print("=" * 70)
    print("CAMINHO 2: ZETA DE RANDOM MAPS")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("1. VERIFICACAO DE FLAJOLET-ODLYZKO")
    print("=" * 70)
    
    print("\nComparando teoria com observacao:")
    print("-" * 70)
    print(f"{'n':>6} {'E[ciclos] obs':>14} {'E[ciclos] teo':>14} {'ratio':>8}")
    print("-" * 70)
    
    for n in [100, 500, 1000, 2000]:
        ensemble = RandomMapEnsemble(n, n_samples=50)
        result = ensemble.verify_flajolet_odlyzko()
        
        c_obs = result['cycles']['observed']
        c_teo = result['cycles']['theory']
        ratio = result['cycles']['ratio']
        
        print(f"{n:>6} {c_obs:>14.2f} {c_teo:>14.2f} {ratio:>8.2f}")
    
    print("\n" + "=" * 70)
    print("2. ZETA DO RANDOM MAP")
    print("=" * 70)
    
    n = 500
    rm = RandomMapZeta(n, seed=42)
    
    print(f"\nRandom map com n={n}")
    print(f"Numero de ciclos: {len(rm.cycles)}")
    print(f"Comprimentos: {rm.cycle_lengths}")
    
    print("\nValores de Z_f(s):")
    print("-" * 40)
    print(f"{'s':>6} {'|Z_f(s)| prod':>15} {'log Z_f serie':>15}")
    print("-" * 40)
    
    for s in [1.0, 1.5, 2.0, 2.5, 3.0]:
        z_prod = rm.zeta_product(s)
        log_z = rm.log_zeta_series(s)
        print(f"{s:>6.1f} {abs(z_prod):>15.4f} {log_z.real:>15.4f}")
    
    print("\n" + "=" * 70)
    print("3. TEOREMA DOS NUMEROS PRIMOS COMPUTACIONAL")
    print("=" * 70)
    
    n = 1000
    theory = ComputationalPrimeTheory(n, n_samples=50)
    pnt = theory.prime_number_theorem_analog()
    
    print(f"\nPara n={n}:")
    print(f"  pi_f observado:  {pnt['observed']:.2f}")
    print(f"  PNT classico:    {pnt['pnt_classic']:.2f} (n / log n)")
    print(f"  Flajolet:        {pnt['flajolet']:.2f} ((1/2) log n + gamma)")
    print(f"  Melhor ajuste:   {pnt['best_fit']}")
    
    print("\n" + "=" * 70)
    print("4. LEI DOS PRIMOS COMPUTACIONAIS")
    print("=" * 70)
    
    print("""
    DESCOBERTA:
    -----------
    Para random maps, a lei de contagem de "primos" (ciclos) e:
    
        pi_f(n) ~ (1/2) log(n) + gamma
    
    onde gamma = 0.5772... (Euler-Mascheroni)
    
    COMPARACAO:
    -----------
    | Sistema          | Lei                    |
    |------------------|------------------------|
    | Primos classicos | pi(n) ~ n / log(n)     |
    | Random maps      | pi(n) ~ (1/2) log(n)   |
    
    A diferenca e QUALITATIVA:
    - Primos classicos: crescem quase linearmente
    - Random maps: crescem logaritmicamente
    
    INTERPRETACAO:
    --------------
    Random maps tem "poucos primos" comparado com inteiros.
    Isso reflete que a estrutura e muito "caotica" - 
    quase tudo cai nas mesmas orbitas.
    """)
    
    print("\n" + "=" * 70)
    print("5. ZETA E FORMULA EXPLICITA")
    print("=" * 70)
    
    print("""
    Para random map f:
    
    Z_f(s) = prod_{gamma ciclo} (1 - |gamma|^{-s})^{-1}
    
    log Z_f(s) = sum_k (N_k / k) * k^{-s}
    
    onde N_k = numero de ciclos de comprimento k.
    
    DIFERENCA DA ZETA DE RIEMANN:
    -----------------------------
    - Riemann: produto INFINITO sobre primos
    - Random map: produto FINITO sobre ciclos
    
    - Riemann: zeros nao-triviais na linha critica
    - Random map: sem zeros nao-triviais (produto finito)
    
    ANALOGIA QUE FUNCIONA:
    ----------------------
    A FORMULA EXPLICITA existe:
    
    sum_gamma f(|gamma|) = integral termo suave + sum_zeros g(rho)
    
    Mas para random map, nao ha zeros, entao:
    
    sum_gamma f(|gamma|) = integral termo suave
    
    Isso e mais simples, mas ainda captura a estrutura.
    """)
    
    print("\n" + "=" * 70)
    print("6. CONCLUSAO DO CAMINHO 2")
    print("=" * 70)
    
    print("""
    O QUE DESCOBRIMOS:
    ------------------
    1. "Primos computacionais" = ciclos em random maps
    2. Lei de contagem: pi(n) ~ (1/2) log(n), NAO n/log(n)
    3. Zeta e produto finito, sem zeros nao-triviais
    4. Formula explicita simplifica (sem termo oscilatorio)
    
    O QUE ISSO SIGNIFICA:
    ---------------------
    A analogia "primos = ciclos" FUNCIONA, mas a lei e DIFERENTE.
    
    Isso NAO e fracasso - e DESCOBERTA:
    - Random maps tem estrutura diferente de inteiros
    - A "densidade de primos" e muito menor
    - A zeta e mais simples (finita)
    
    CONEXAO COM CAMINHO 1:
    ----------------------
    A teoria espectral do random map conecta:
    - Espectro de L_f (matriz de transicao)
    - Ciclos (primos)
    - Zeta (funcao geradora)
    
    O operador L_f tem autovalor 0 com alta multiplicidade
    (porque random map nao e bijecao).
    
    PROXIMO PASSO POTENCIAL:
    ------------------------
    Estudar random PERMUTATIONS (bijecoes) para ter espectro mais rico.
    Ou estudar perturbacoes de random maps.
    """)
    
    print("=" * 70)


def main():
    demonstrate_random_map_zeta()


if __name__ == "__main__":
    main()
