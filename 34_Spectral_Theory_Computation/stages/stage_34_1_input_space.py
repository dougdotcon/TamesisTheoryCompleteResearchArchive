"""
Stage 34.1: Espaco de Inputs para Algoritmos de Ordenacao
=========================================================

OBJETIVO:
---------
Definir rigorosamente o espaco de inputs I = S_n (permutacoes de n elementos)
sobre o qual o operador L_A vai atuar.

POR QUE PERMUTACOES:
--------------------
- Quicksort, mergesort, heapsort operam sobre listas
- Uma lista de n elementos distintos E uma permutacao
- O espaco de permutacoes S_n e finito, bem estruturado
- Medida natural: uniforme (todas permutacoes equiprovaveis)

O ESPACO:
---------
S_n = grupo simetrico de n elementos
|S_n| = n!

Estrutura adicional:
- Distancia: numero minimo de trocas para ir de sigma a tau
- Vizinhanca: permutacoes que diferem por uma transposicao
- Grafo de Cayley: S_n com geradores = transposicoes adjacentes

IMPORTANTE:
-----------
Este NAO e o espaco de estados do algoritmo.
Este e o espaco de ENTRADAS possiveis.
O operador L_A vai descrever como a "distribuicao de inputs" evolui.
"""

import numpy as np
from typing import List, Tuple, Set, Dict, Iterator
from itertools import permutations
from collections import defaultdict
import math


class PermutationSpace:
    """
    O espaco S_n de permutacoes de n elementos.
    
    Representacao:
    - Permutacao = tupla (a_0, a_1, ..., a_{n-1})
    - Significa: posicao i contem elemento a_i
    - Identidade: (0, 1, 2, ..., n-1)
    """
    
    def __init__(self, n: int):
        if n > 8:
            raise ValueError(f"n={n} muito grande. n! = {math.factorial(n)}. Use n <= 8.")
        
        self.n = n
        self.size = math.factorial(n)
        
        # Gera todas as permutacoes
        self._all_perms = list(permutations(range(n)))
        
        # Indexacao: permutacao -> indice
        self._perm_to_idx = {p: i for i, p in enumerate(self._all_perms)}
        
        # Identidade
        self.identity = tuple(range(n))
    
    def __len__(self) -> int:
        return self.size
    
    def __iter__(self) -> Iterator[Tuple[int, ...]]:
        return iter(self._all_perms)
    
    def index(self, perm: Tuple[int, ...]) -> int:
        """Retorna indice da permutacao"""
        return self._perm_to_idx[perm]
    
    def perm(self, idx: int) -> Tuple[int, ...]:
        """Retorna permutacao dado indice"""
        return self._all_perms[idx]
    
    def compose(self, sigma: Tuple[int, ...], tau: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Composicao: (sigma o tau)(i) = sigma(tau(i))
        
        Aplica tau primeiro, depois sigma.
        """
        return tuple(sigma[tau[i]] for i in range(self.n))
    
    def inverse(self, sigma: Tuple[int, ...]) -> Tuple[int, ...]:
        """Inversa da permutacao"""
        inv = [0] * self.n
        for i, s in enumerate(sigma):
            inv[s] = i
        return tuple(inv)
    
    def transpose(self, sigma: Tuple[int, ...], i: int, j: int) -> Tuple[int, ...]:
        """Aplica transposicao (i j) a sigma"""
        result = list(sigma)
        result[i], result[j] = result[j], result[i]
        return tuple(result)
    
    def adjacent_transposition(self, sigma: Tuple[int, ...], i: int) -> Tuple[int, ...]:
        """Aplica transposicao adjacente (i i+1)"""
        return self.transpose(sigma, i, i + 1)
    
    def inversions(self, sigma: Tuple[int, ...]) -> int:
        """
        Numero de inversoes: pares (i,j) com i < j mas sigma[i] > sigma[j].
        
        Mede "desordem" da permutacao.
        Distancia ate a identidade no grafo de transposicoes adjacentes.
        """
        count = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if sigma[i] > sigma[j]:
                    count += 1
        return count
    
    def kendall_tau_distance(self, sigma: Tuple[int, ...], tau: Tuple[int, ...]) -> int:
        """
        Distancia de Kendall-Tau entre duas permutacoes.
        
        = numero de transposicoes adjacentes para ir de sigma a tau
        = inversoes(sigma^{-1} o tau)
        """
        sigma_inv = self.inverse(sigma)
        composed = self.compose(sigma_inv, tau)
        return self.inversions(composed)
    
    def neighbors_by_adjacent_transposition(self, sigma: Tuple[int, ...]) -> List[Tuple[int, ...]]:
        """
        Vizinhos de sigma no grafo de Cayley com geradores = transposicoes adjacentes.
        
        Cada permutacao tem n-1 vizinhos.
        """
        neighbors = []
        for i in range(self.n - 1):
            neighbors.append(self.adjacent_transposition(sigma, i))
        return neighbors
    
    def neighbors_by_any_transposition(self, sigma: Tuple[int, ...]) -> List[Tuple[int, ...]]:
        """
        Vizinhos de sigma no grafo com geradores = todas as transposicoes.
        
        Cada permutacao tem C(n,2) = n(n-1)/2 vizinhos.
        """
        neighbors = []
        for i in range(self.n):
            for j in range(i + 1, self.n):
                neighbors.append(self.transpose(sigma, i, j))
        return neighbors
    
    def uniform_measure(self) -> np.ndarray:
        """Medida uniforme: cada permutacao tem probabilidade 1/n!"""
        return np.ones(self.size) / self.size
    
    def sorted_measure(self) -> np.ndarray:
        """Medida concentrada na identidade (lista ordenada)"""
        measure = np.zeros(self.size)
        measure[self.index(self.identity)] = 1.0
        return measure
    
    def inversion_distribution(self) -> Dict[int, int]:
        """Distribuicao do numero de inversoes"""
        dist = defaultdict(int)
        for perm in self._all_perms:
            inv = self.inversions(perm)
            dist[inv] += 1
        return dict(sorted(dist.items()))


class QuicksortDynamics:
    """
    A dinamica do Quicksort no espaco de permutacoes.
    
    IDEIA CHAVE:
    ------------
    Quicksort NAO e um mapa determinístico de permutacao -> permutacao.
    Ele e um processo PROBABILISTICO (escolha do pivot).
    
    Mas podemos estudar:
    1. Versao deterministica (pivot = primeiro elemento)
    2. Versao randomizada (pivot uniforme)
    
    COMO MODELAR "UM PASSO":
    ------------------------
    Uma iteracao do quicksort e uma PARTICAO:
    - Escolhe pivot p
    - Elementos < p vao para esquerda
    - Elementos > p vao para direita
    - Isso gera uma "permutacao parcialmente ordenada"
    
    O OPERADOR:
    -----------
    Nao atua diretamente em permutacoes.
    Atua na DISTRIBUICAO de permutacoes.
    
    Se comecamos com distribuicao uniforme:
    - Apos uma particao, algumas permutacoes "convergem"
    - A entropia diminui
    - No final, tudo converge para a identidade
    """
    
    def __init__(self, n: int):
        self.n = n
        self.space = PermutationSpace(n)
    
    def partition_deterministic(self, arr: List[int]) -> Tuple[List[int], int]:
        """
        Uma particao com pivot = primeiro elemento.
        
        Retorna:
        - Array particionado
        - Posicao final do pivot
        """
        if len(arr) <= 1:
            return arr, 0
        
        pivot = arr[0]
        left = [x for x in arr[1:] if x < pivot]
        right = [x for x in arr[1:] if x > pivot]
        
        result = left + [pivot] + right
        pivot_pos = len(left)
        
        return result, pivot_pos
    
    def one_partition_step(self, perm: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Aplica UMA particao global ao array.
        
        Isso NAO e exatamente o quicksort (que e recursivo),
        mas captura a essencia de "uma iteracao".
        """
        arr = list(perm)
        result, _ = self.partition_deterministic(arr)
        return tuple(result)
    
    def recursive_partition_depth(self, perm: Tuple[int, ...], max_depth: int = 10) -> int:
        """
        Quantas particoes recursivas ate ordenar completamente.
        
        Isso e uma medida de "complexidade" para esta permutacao especifica.
        """
        if perm == self.space.identity:
            return 0
        
        arr = list(perm)
        depth = self._quicksort_depth(arr, 0, len(arr) - 1, 0, max_depth)
        return depth
    
    def _quicksort_depth(self, arr: List[int], low: int, high: int, 
                         current_depth: int, max_depth: int) -> int:
        """Conta profundidade maxima da recursao"""
        if low >= high or current_depth >= max_depth:
            return current_depth
        
        # Particao
        pivot = arr[low]
        i = low + 1
        j = high
        
        while True:
            while i <= j and arr[i] < pivot:
                i += 1
            while i <= j and arr[j] > pivot:
                j -= 1
            if i > j:
                break
            arr[i], arr[j] = arr[j], arr[i]
        
        arr[low], arr[j] = arr[j], arr[low]
        
        # Recursao
        left_depth = self._quicksort_depth(arr, low, j - 1, current_depth + 1, max_depth)
        right_depth = self._quicksort_depth(arr, j + 1, high, current_depth + 1, max_depth)
        
        return max(left_depth, right_depth)
    
    def comparison_count(self, perm: Tuple[int, ...]) -> int:
        """
        Numero de comparacoes para ordenar esta permutacao.
        
        Esta e a medida classica de complexidade.
        """
        arr = list(perm)
        count = [0]  # Usa lista para permitir modificacao em closure
        self._quicksort_count(arr, 0, len(arr) - 1, count)
        return count[0]
    
    def _quicksort_count(self, arr: List[int], low: int, high: int, count: List[int]):
        """Quicksort contando comparacoes"""
        if low >= high:
            return
        
        pivot = arr[low]
        i = low + 1
        j = high
        
        while True:
            while i <= j:
                count[0] += 1
                if arr[i] >= pivot:
                    break
                i += 1
            while i <= j:
                count[0] += 1
                if arr[j] <= pivot:
                    break
                j -= 1
            if i > j:
                break
            arr[i], arr[j] = arr[j], arr[i]
        
        arr[low], arr[j] = arr[j], arr[low]
        
        self._quicksort_count(arr, low, j - 1, count)
        self._quicksort_count(arr, j + 1, high, count)


def demonstrate_input_space():
    """
    Demonstra o espaco de inputs S_n.
    """
    print("=" * 70)
    print("STAGE 34.1: ESPACO DE INPUTS PARA QUICKSORT")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("1. O ESPACO S_n")
    print("=" * 70)
    
    for n in range(3, 8):
        space = PermutationSpace(n)
        print(f"  S_{n}: {space.size:>6} permutacoes ({n}! = {math.factorial(n)})")
    
    print("\n" + "=" * 70)
    print("2. ESTRUTURA DE S_5")
    print("=" * 70)
    
    n = 5
    space = PermutationSpace(n)
    
    print(f"\nEspaco: S_{n} com {space.size} elementos")
    print(f"Identidade: {space.identity}")
    
    # Algumas permutacoes
    print("\nExemplos de permutacoes:")
    for i in [0, 1, 10, 50, 100, 119]:
        perm = space.perm(i)
        inv = space.inversions(perm)
        print(f"  [{i:3d}] {perm}  inversoes={inv}")
    
    print("\n" + "=" * 70)
    print("3. DISTRIBUICAO DE INVERSOES")
    print("=" * 70)
    
    inv_dist = space.inversion_distribution()
    max_inv = max(inv_dist.keys())
    
    print(f"\nNumero maximo de inversoes: {max_inv} (= C({n},2) = {n*(n-1)//2})")
    print("\nDistribuicao:")
    print("-" * 40)
    print(f"{'Inversoes':>10} {'Count':>10} {'Frequencia':>12}")
    print("-" * 40)
    
    for inv, count in inv_dist.items():
        freq = count / space.size
        bar = '#' * int(freq * 50)
        print(f"{inv:10d} {count:10d} {freq:12.4f}  {bar}")
    
    print("\n" + "=" * 70)
    print("4. VIZINHANCA NO GRAFO DE CAYLEY")
    print("=" * 70)
    
    perm = (4, 2, 0, 3, 1)  # Uma permutacao qualquer
    print(f"\nPermutacao: {perm}")
    print(f"Inversoes: {space.inversions(perm)}")
    
    print("\nVizinhos por transposicao adjacente:")
    for neighbor in space.neighbors_by_adjacent_transposition(perm):
        inv = space.inversions(neighbor)
        print(f"  {neighbor}  inversoes={inv}")
    
    print("\n" + "=" * 70)
    print("5. QUICKSORT COMO DINAMICA")
    print("=" * 70)
    
    qs = QuicksortDynamics(n)
    
    print("\nComplexidade do quicksort para algumas permutacoes:")
    print("-" * 50)
    print(f"{'Permutacao':>20} {'Inversoes':>10} {'Comparacoes':>12}")
    print("-" * 50)
    
    test_perms = [
        space.identity,                    # Ja ordenada
        tuple(reversed(range(n))),         # Reversa (pior caso)
        (2, 4, 1, 3, 0),                   # Aleatoria
        (1, 0, 3, 2, 4),                   # Quase ordenada
        (4, 0, 1, 2, 3),                   # Um elemento fora
    ]
    
    for perm in test_perms:
        inv = space.inversions(perm)
        comp = qs.comparison_count(perm)
        print(f"{str(perm):>20} {inv:>10} {comp:>12}")
    
    print("\n" + "=" * 70)
    print("6. ESTATISTICAS DE COMPLEXIDADE")
    print("=" * 70)
    
    # Calcula comparacoes para todas as permutacoes
    comparisons = []
    for perm in space:
        comp = qs.comparison_count(perm)
        comparisons.append(comp)
    
    comparisons = np.array(comparisons)
    
    print(f"\nEstatisticas de comparacoes (n={n}):")
    print(f"  Minimo:  {comparisons.min()}")
    print(f"  Maximo:  {comparisons.max()}")
    print(f"  Media:   {comparisons.mean():.2f}")
    print(f"  Std:     {comparisons.std():.2f}")
    
    # Complexidade teorica
    print(f"\nComparacao com teoria:")
    print(f"  Melhor caso teorico: O(n log n) ~ {n * np.log2(n):.1f}")
    print(f"  Caso medio teorico:  ~1.39 n log n ~ {1.39 * n * np.log2(n):.1f}")
    print(f"  Pior caso teorico:   O(n^2) ~ {n * (n-1) / 2:.1f}")
    
    print("\n" + "=" * 70)
    print("7. RESULTADO DO STAGE 34.1")
    print("=" * 70)
    
    print("""
    O QUE CONSTRUIMOS:
    ------------------
    1. Espaco de inputs S_n com n! elementos
    2. Estrutura de grupo (composicao, inversa)
    3. Distancia de Kendall-Tau (inversoes)
    4. Grafo de Cayley (vizinhanca por transposicoes)
    5. Medida uniforme
    
    OBSERVACOES:
    ------------
    - Para n=5: 120 permutacoes
    - Para n=6: 720 permutacoes
    - Para n=7: 5040 permutacoes
    - Para n=8: 40320 permutacoes (limite pratico)
    
    - Numero de inversoes vai de 0 (ordenada) a C(n,2) (reversa)
    - Distribuicao de inversoes e SIMETRICA (propriedade de S_n)
    
    PROXIMO PASSO:
    --------------
    Stage 34.2: Construir o operador L_quicksort
    
    A ideia:
    - L_A[i,j] = probabilidade de ir do input j para o input i
    - Mas quicksort NAO preserva permutacao (ele ORDENA)
    - Precisamos definir o operador de forma que capture a ESTRUTURA
    """)
    
    print("=" * 70)
    
    return space, qs


def main():
    space, dynamics = demonstrate_input_space()
    return space, dynamics


if __name__ == "__main__":
    main()
