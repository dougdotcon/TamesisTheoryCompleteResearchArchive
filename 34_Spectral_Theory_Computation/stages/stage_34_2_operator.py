"""
Stage 34.2: Operador de Transferencia para Quicksort
====================================================

O PROBLEMA CONCEITUAL:
----------------------
Quicksort NAO e um mapa T: S_n -> S_n.
Ele e um algoritmo que ORDENA, ou seja:
    T(sigma) = identidade  para TODO sigma

Isso daria um operador trivial!

A SOLUCAO:
----------
Estudar a EVOLUCAO PARCIAL do algoritmo.

Em vez de ver quicksort como "entrada -> saida",
ver como "distribuicao de estados internos apos k passos".

ALTERNATIVA 1: Operador de Reducao de Inversoes
-----------------------------------------------
Definir T como "aplicar uma particao parcial que reduz inversoes".

ALTERNATIVA 2: Operador de Transicao de Arvore
----------------------------------------------
Modelar o espaco de estados como arvore de recursao.
O operador descreve transicoes entre niveis.

ALTERNATIVA 3: Operador de Entropia
-----------------------------------
Modelar como a "entropia da permutacao" decai.
O operador atua na distribuicao de permutacoes parcialmente ordenadas.

ABORDAGEM ESCOLHIDA:
--------------------
Vamos usar uma ideia mais natural:

O OPERADOR DE COMPARACAO
------------------------
Cada comparacao no quicksort PARTICIONA o espaco de permutacoes.
Se comparamos elementos i e j:
    - Metade das permutacoes tem arr[i] < arr[j]
    - Metade tem arr[i] > arr[j]

O operador L_cmp descreve essa particao.

Apos uma sequencia de comparacoes, a entropia diminui.
A taxa de reducao de entropia = complexidade.

FORMALIZACAO:
-------------
Estado = subconjunto de S_n (permutacoes consistentes com comparacoes feitas)
Inicial = S_n inteiro
Final = {identidade} (uma unica permutacao)

O operador L atua em 2^{S_n} (conjunto de partes de S_n).
Mas isso e exponencial demais!

SIMPLIFICACAO PRATICA:
----------------------
Estudar o operador MEDIO:

L_{avg}[i,j] = P(permutacao j se torna "mais ordenada" para posicao i)

Ou melhor: estudar o operador no espaco de INVERSOES.
"""

import numpy as np
from typing import List, Tuple, Dict, Set
from itertools import permutations
import math
from collections import defaultdict

# Importa do stage anterior
import sys
sys.path.insert(0, '.')
from stage_34_1_input_space import PermutationSpace, QuicksortDynamics


class InversionOperator:
    """
    Operador no espaco de inversoes.
    
    IDEIA:
    ------
    Em vez de trabalhar em S_n (n! elementos),
    trabalhar no espaco de "numero de inversoes" (n(n-1)/2 + 1 elementos).
    
    O estado e o numero de inversoes.
    A transicao e: quantas inversoes sao removidas por comparacao.
    
    OPERADOR:
    ---------
    L[i, j] = P(passar de j inversoes para i inversoes | uma comparacao)
    """
    
    def __init__(self, n: int):
        self.n = n
        self.max_inv = n * (n - 1) // 2
        self.n_states = self.max_inv + 1  # 0, 1, ..., max_inv
        
        self.space = PermutationSpace(n)
        self.L = None
        
        self._build_operator()
    
    def _build_operator(self):
        """
        Constroi operador de transicao no espaco de inversoes.
        
        Para cada permutacao com k inversoes:
        - Escolhe uma comparacao aleatoria (i, j) uniformemente
        - Se estao na ordem errada, troca (remove 1 inversao)
        - Se estao na ordem certa, mantem (0 inversoes removidas)
        
        L[k-1, k] = P(remover 1 inversao | comecando com k inversoes)
        L[k, k] = P(manter k inversoes | comecando com k inversoes)
        """
        self.L = np.zeros((self.n_states, self.n_states))
        
        # Para cada numero de inversoes, calcula transicao media
        inv_perms = defaultdict(list)
        for perm in self.space:
            inv = self.space.inversions(perm)
            inv_perms[inv].append(perm)
        
        # Para cada nivel de inversoes
        for k in range(self.n_states):
            if k not in inv_perms or len(inv_perms[k]) == 0:
                self.L[k, k] = 1.0  # Estado absorvente
                continue
            
            perms_at_k = inv_perms[k]
            n_perms = len(perms_at_k)
            
            # Para cada permutacao com k inversoes
            # Calcula transicao media sobre todas as comparacoes possiveis
            transition_counts = defaultdict(float)
            
            for perm in perms_at_k:
                # Todas as comparacoes possiveis
                n_comparisons = self.n * (self.n - 1) // 2
                
                for i in range(self.n):
                    for j in range(i + 1, self.n):
                        # Se perm[i] > perm[j], ha uma inversao
                        # Uma comparacao pode "consertar" isso
                        new_perm = list(perm)
                        if perm[i] > perm[j]:
                            # Troca remove essa inversao
                            new_perm[i], new_perm[j] = new_perm[j], new_perm[i]
                        new_inv = self.space.inversions(tuple(new_perm))
                        
                        # Peso uniforme sobre comparacoes
                        transition_counts[new_inv] += 1.0 / (n_perms * n_comparisons)
            
            # Normaliza
            for new_k, count in transition_counts.items():
                self.L[new_k, k] = count
    
    def spectrum(self) -> np.ndarray:
        """Calcula autovalores do operador"""
        eigenvalues = np.linalg.eigvals(self.L)
        return np.sort(np.abs(eigenvalues))[::-1]
    
    def stationary_distribution(self) -> np.ndarray:
        """Distribuicao estacionaria (autovetor com autovalor 1)"""
        eigenvalues, eigenvectors = np.linalg.eig(self.L.T)
        idx = np.argmax(np.abs(eigenvalues))
        stationary = np.abs(eigenvectors[:, idx])
        return stationary / stationary.sum()
    
    def expected_steps_to_zero(self) -> np.ndarray:
        """
        Numero esperado de passos para chegar a 0 inversoes.
        
        Resolve: E[k] = 1 + sum_j L[j,k] * E[j]  para k > 0
                 E[0] = 0
        """
        E = np.zeros(self.n_states)
        
        # Resolve iterativamente (backward induction)
        for k in range(1, self.n_states):
            # E[k] = 1 + sum_{j < k} L[j, k] * E[j] + L[k, k] * E[k]
            # E[k] * (1 - L[k, k]) = 1 + sum_{j < k} L[j, k] * E[j]
            
            denom = 1 - self.L[k, k]
            if denom < 1e-10:
                E[k] = float('inf')
            else:
                numer = 1.0
                for j in range(k):
                    numer += self.L[j, k] * E[j]
                E[k] = numer / denom
        
        return E


class PartitionOperator:
    """
    Operador baseado em particoes do quicksort.
    
    IDEIA:
    ------
    Uma particao com pivot p divide S_n em:
    - Permutacoes onde p esta "resolvido"
    
    O operador descreve como a distribuicao evolui apos uma particao.
    
    SIMPLIFICACAO:
    --------------
    Trabalhar no espaco de "perfis de particao":
    - Quantos elementos estao no lugar certo
    - Estrutura de blocos parcialmente ordenados
    """
    
    def __init__(self, n: int):
        self.n = n
        self.space = PermutationSpace(n)
        
        # Estado = numero de elementos "fixados" (no lugar final)
        self.n_states = n + 1  # 0, 1, ..., n elementos fixados
        self.L = None
        
        self._build_operator()
    
    def _count_fixed_points(self, perm: Tuple[int, ...]) -> int:
        """Conta quantos elementos estao no lugar certo"""
        return sum(1 for i, p in enumerate(perm) if p == i)
    
    def _apply_partition(self, perm: Tuple[int, ...], pivot_idx: int) -> Tuple[int, ...]:
        """
        Aplica uma particao com pivot no indice dado.
        
        Elementos menores que o pivot vao para a esquerda.
        Elementos maiores vao para a direita.
        O pivot vai para a posicao correta.
        """
        arr = list(perm)
        pivot = arr[pivot_idx]
        
        # Remove pivot temporariamente
        arr.pop(pivot_idx)
        
        # Particiona
        left = [x for x in arr if x < pivot]
        right = [x for x in arr if x > pivot]
        
        # Reconstroi
        result = left + [pivot] + right
        return tuple(result)
    
    def _build_operator(self):
        """
        Constroi operador de transicao no espaco de pontos fixos.
        
        L[i, j] = P(ter i pontos fixos | tinha j pontos fixos, apos uma particao)
        """
        self.L = np.zeros((self.n_states, self.n_states))
        
        # Agrupa permutacoes por numero de pontos fixos
        fixed_perms = defaultdict(list)
        for perm in self.space:
            fp = self._count_fixed_points(perm)
            fixed_perms[fp].append(perm)
        
        # Para cada nivel de pontos fixos
        for j in range(self.n_states):
            if j not in fixed_perms or len(fixed_perms[j]) == 0:
                self.L[j, j] = 1.0  # Estado absorvente
                continue
            
            perms_at_j = fixed_perms[j]
            n_perms = len(perms_at_j)
            
            transition_counts = defaultdict(float)
            
            for perm in perms_at_j:
                # Tenta cada posicao como pivot
                for pivot_idx in range(self.n):
                    new_perm = self._apply_partition(perm, pivot_idx)
                    new_fp = self._count_fixed_points(new_perm)
                    
                    transition_counts[new_fp] += 1.0 / (n_perms * self.n)
            
            # Normaliza
            for i, count in transition_counts.items():
                self.L[i, j] = count
    
    def spectrum(self) -> np.ndarray:
        """Calcula autovalores do operador"""
        eigenvalues = np.linalg.eigvals(self.L)
        return np.sort(np.abs(eigenvalues))[::-1]


class QuicksortTransferOperator:
    """
    Operador de transferencia COMPLETO para quicksort.
    
    Atua diretamente em S_n.
    
    DEFINICAO:
    ----------
    Para cada permutacao sigma:
    - Aplica uma particao (escolhe pivot uniformemente)
    - Conta em qual permutacao resulta
    
    L[i, j] = P(obter permutacao i | comecando com permutacao j, uma particao)
    
    NOTA:
    -----
    Esta e a matriz completa n! x n!
    So funciona para n pequeno (n <= 6 pratico)
    """
    
    def __init__(self, n: int):
        if n > 6:
            raise ValueError(f"n={n} muito grande. Use n <= 6.")
        
        self.n = n
        self.space = PermutationSpace(n)
        self.matrix_size = self.space.size
        self.L = None
        
        self._build_operator()
    
    def _apply_one_partition(self, perm: Tuple[int, ...]) -> List[Tuple[Tuple[int, ...], float]]:
        """
        Aplica uma particao com pivot aleatorio.
        
        Retorna lista de (nova_permutacao, probabilidade).
        """
        results = []
        
        for pivot_idx in range(self.n):
            arr = list(perm)
            pivot = arr[pivot_idx]
            
            # Remove e particiona
            arr.pop(pivot_idx)
            left = [x for x in arr if x < pivot]
            right = [x for x in arr if x > pivot]
            
            new_perm = tuple(left + [pivot] + right)
            prob = 1.0 / self.n
            
            results.append((new_perm, prob))
        
        return results
    
    def _build_operator(self):
        """Constroi a matriz de transferencia completa"""
        self.L = np.zeros((self.matrix_size, self.matrix_size))
        
        for j, perm_j in enumerate(self.space):
            transitions = self._apply_one_partition(perm_j)
            
            for new_perm, prob in transitions:
                i = self.space.index(new_perm)
                self.L[i, j] += prob
    
    def spectrum(self, n_eigenvalues: int = 20) -> np.ndarray:
        """Calcula autovalores"""
        eigenvalues = np.linalg.eigvals(self.L)
        eigenvalues = sorted(eigenvalues, key=lambda x: -abs(x))
        return np.array(eigenvalues[:n_eigenvalues])
    
    def spectral_radius(self) -> float:
        """Raio espectral = maior autovalor em modulo"""
        eigs = self.spectrum(5)
        return abs(eigs[0])
    
    def spectral_gap(self) -> float:
        """Gap espectral"""
        eigs = self.spectrum(5)
        if len(eigs) < 2:
            return 0.0
        return abs(eigs[0]) - abs(eigs[1])


def demonstrate_operators():
    """
    Demonstra os operadores construidos.
    """
    print("=" * 70)
    print("STAGE 34.2: OPERADOR DE TRANSFERENCIA PARA QUICKSORT")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("1. OPERADOR NO ESPACO DE INVERSOES")
    print("=" * 70)
    
    for n in [4, 5, 6]:
        print(f"\n--- n = {n} ---")
        inv_op = InversionOperator(n)
        
        print(f"Espaco de estados: {inv_op.n_states} (inversoes de 0 a {inv_op.max_inv})")
        
        spectrum = inv_op.spectrum()
        print(f"Autovalores (top 5): {spectrum[:5]}")
        print(f"Raio espectral: {spectrum[0]:.6f}")
        
        E = inv_op.expected_steps_to_zero()
        print(f"Passos esperados para ordenar (partindo de max inversoes): {E[-1]:.2f}")
    
    print("\n" + "=" * 70)
    print("2. OPERADOR NO ESPACO DE PONTOS FIXOS")
    print("=" * 70)
    
    for n in [4, 5, 6]:
        print(f"\n--- n = {n} ---")
        part_op = PartitionOperator(n)
        
        print(f"Espaco de estados: {part_op.n_states} (pontos fixos de 0 a {n})")
        
        spectrum = part_op.spectrum()
        print(f"Autovalores: {spectrum}")
        print(f"Raio espectral: {spectrum[0]:.6f}")
    
    print("\n" + "=" * 70)
    print("3. OPERADOR COMPLETO EM S_n")
    print("=" * 70)
    
    for n in [4, 5, 6]:
        print(f"\n--- n = {n} ---")
        full_op = QuicksortTransferOperator(n)
        
        print(f"Matriz: {full_op.matrix_size} x {full_op.matrix_size}")
        
        spectrum = full_op.spectrum(10)
        print(f"Autovalores (top 10 em modulo):")
        for i, eig in enumerate(spectrum[:10]):
            print(f"  lambda_{i}: |{abs(eig):.6f}| (fase: {np.angle(eig):.4f})")
        
        print(f"Raio espectral: {full_op.spectral_radius():.6f}")
        print(f"Gap espectral: {full_op.spectral_gap():.6f}")
    
    print("\n" + "=" * 70)
    print("4. COMPARACAO DOS RAIOS ESPECTRAIS")
    print("=" * 70)
    
    print("\n" + "-" * 50)
    print(f"{'n':>4} {'|S_n|':>8} {'rho(L)':>10} {'n log n':>10} {'n^2':>8}")
    print("-" * 50)
    
    for n in [4, 5, 6]:
        full_op = QuicksortTransferOperator(n)
        rho = full_op.spectral_radius()
        n_log_n = n * np.log(n)
        n_sq = n * n
        
        print(f"{n:>4} {math.factorial(n):>8} {rho:>10.6f} {n_log_n:>10.2f} {n_sq:>8}")
    
    print("\n" + "=" * 70)
    print("5. RESULTADO DO STAGE 34.2")
    print("=" * 70)
    
    print("""
    O QUE CONSTRUIMOS:
    ------------------
    1. InversionOperator: atua no espaco de inversoes (O(n^2) estados)
    2. PartitionOperator: atua no espaco de pontos fixos (O(n) estados)
    3. QuicksortTransferOperator: atua em S_n completo (n! estados)
    
    OBSERVACOES IMPORTANTES:
    ------------------------
    - O raio espectral do operador completo e SEMPRE 1
      (porque e uma matriz estocastica)
    
    - Isso significa que o raio espectral NAO e a medida certa!
    
    - O que importa e o GAP ESPECTRAL:
      gap = |lambda_1| - |lambda_2|
      
    - Gap grande = convergencia rapida = algoritmo eficiente
    - Gap pequeno = convergencia lenta = algoritmo ineficiente
    
    INSIGHT CRITICO:
    ----------------
    Complexidade NAO emerge do raio espectral.
    Complexidade emerge da TAXA DE DECAIMENTO do segundo autovalor.
    
    Tempo para convergir ~ 1 / gap
    
    PROXIMO PASSO:
    --------------
    Stage 34.3: Estudar o GAP ESPECTRAL como funcao de n
    
    Hipotese: gap(n) ~ 1 / (n log n)
    
    Isso daria: tempo ~ n log n
    """)
    
    print("=" * 70)


def main():
    demonstrate_operators()


if __name__ == "__main__":
    main()
