"""
Stage 34.4: Operador que Captura a Recursao
===========================================

O PROBLEMA DOS STAGES ANTERIORES:
---------------------------------
O operador L (uma particao) nao captura o fato de que o quicksort
REDUZ o tamanho do problema a cada iteracao.

No quicksort real:
- Primeira particao: problema de tamanho n
- Segunda particao: 2 problemas de tamanho ~n/2
- ...
- Total: O(n log n) comparacoes

O operador L^k ainda trata o problema como se fosse tamanho n sempre.

A SOLUCAO:
----------
Modelar o quicksort como processo em ARVORE DE RECURSAO.

Estado = configuracao da arvore (quais elementos estao fixados)
Transicao = uma particao fixa mais um elemento

O OPERADOR CORRETO:
-------------------
Definir estado como: conjunto de elementos ja "fixados" (na posicao final).

Espaco de estados: 2^{1,...,n} (conjuntos de elementos fixados)
Tamanho: 2^n (muito menor que n! para n grande)

Transicao: de S (fixados) para S U {pivot}

ALTERNATIVA MAIS SIMPLES:
-------------------------
Estado = numero de elementos fixados (0, 1, ..., n)
Espaco: n+1 estados
Transicao: de k fixados para k+1 fixados (sempre fixa o pivot)

Esta e uma cadeia de Markov ABSORVENTE.
Estado n (todos fixados) e absorvente.

A ZETA AQUI:
------------
Com esta visao, o operador nao e mais estocastico no sentido usual.
E um operador de ABSORCAO.

O tempo de absorcao = complexidade do algoritmo.
"""

import numpy as np
from typing import List, Tuple, Dict, Set
import math
from collections import defaultdict
from itertools import combinations


class FixedElementsMarkovChain:
    """
    Cadeia de Markov no espaco de "numero de elementos fixados".
    
    Estado k = k elementos estao na posicao final.
    Estado 0 = nenhum fixado (inicial)
    Estado n = todos fixados (absorvente)
    
    Transicao: cada particao fixa EXATAMENTE 1 elemento (o pivot).
    """
    
    def __init__(self, n: int):
        self.n = n
        self.n_states = n + 1  # 0, 1, ..., n
        
        # A matriz de transicao e trivial neste modelo:
        # P[k+1, k] = 1 para k < n
        # P[n, n] = 1 (absorvente)
        
        self.P = np.zeros((self.n_states, self.n_states))
        for k in range(n):
            self.P[k + 1, k] = 1.0
        self.P[n, n] = 1.0
    
    def expected_steps(self) -> float:
        """
        Numero esperado de passos para absorver.
        
        Como cada passo avanca exatamente 1, sao exatamente n passos.
        Mas isso nao captura a COMPLEXIDADE (numero de comparacoes)!
        """
        return self.n


class ComparisonCountOperator:
    """
    Operador que conta COMPARACOES, nao particoes.
    
    Estado = (elementos_fixados, comparacoes_feitas)
    
    Mas isso explode... Vamos simplificar.
    
    ALTERNATIVA:
    Estado = nivel na arvore de recursao (profundidade)
    Cada nivel contribui ~n comparacoes (no total de todos os nos)
    
    Profundidade esperada = O(log n)
    Comparacoes por nivel = O(n)
    Total = O(n log n)
    """
    
    def __init__(self, n: int):
        self.n = n
    
    def expected_comparisons_analytic(self) -> float:
        """
        Formula analitica para comparacoes esperadas do quicksort.
        
        E[C_n] = 2(n+1)H_n - 4n
        
        onde H_n = 1 + 1/2 + ... + 1/n (numero harmonico)
        
        ~ 2n ln n + O(n)
        ~ 1.39 n log_2 n
        """
        H_n = sum(1.0/k for k in range(1, self.n + 1))
        return 2 * (self.n + 1) * H_n - 4 * self.n


class RecursionTreeOperator:
    """
    Operador na arvore de recursao.
    
    MODELO:
    -------
    Cada no da arvore representa um subproblema.
    O estado e o TAMANHO do subproblema.
    
    Raiz: tamanho n
    Apos particao: dois filhos de tamanhos k e n-k-1 (pivot removido)
    
    O operador descreve a DISTRIBUICAO de tamanhos apos uma particao.
    
    SIMPLIFICACAO:
    --------------
    Em vez de rastrear a arvore inteira, rastreamos a DISTRIBUICAO
    de tamanhos de subproblemas.
    
    Estado = vetor (c_0, c_1, ..., c_n) onde c_k = numero de subproblemas de tamanho k
    """
    
    def __init__(self, n: int):
        self.n = n
        # Estados: configuracoes (c_0, ..., c_n)
        # Mas isso explode... precisamos de outra abordagem
    
    def partition_distribution(self, size: int) -> List[Tuple[int, int, float]]:
        """
        Distribuicao dos tamanhos dos filhos apos particao.
        
        Se pivot e escolhido uniformemente em subproblema de tamanho size:
        - Filho esquerdo: tamanho k
        - Filho direito: tamanho size - k - 1
        - Probabilidade: 1/size para cada k em {0, ..., size-1}
        
        Retorna lista de (tamanho_esq, tamanho_dir, probabilidade).
        """
        if size <= 1:
            return [(0, 0, 1.0)]  # Caso base: nada a fazer
        
        transitions = []
        for k in range(size):
            left_size = k
            right_size = size - k - 1
            prob = 1.0 / size
            transitions.append((left_size, right_size, prob))
        
        return transitions


class SubproblemSizeOperator:
    """
    Operador no espaco de TAMANHOS DE SUBPROBLEMA.
    
    Este e o operador mais natural para quicksort!
    
    Estado = tamanho do subproblema atual
    Espaco: {0, 1, ..., n}
    
    Transicao de tamanho k:
    - Gera dois filhos de tamanhos i e k-i-1 (para i aleatorio)
    - Custo: k-1 comparacoes
    
    O operador L[j, k] = P(filho de tamanho j | pai de tamanho k)
    
    FORMULA:
    --------
    L[j, k] = 2/k se 0 <= j <= k-1 (cada filho)
              0   caso contrario
    
    (Fator 2 porque cada particao gera DOIS filhos)
    
    AJUSTE:
    -------
    Na verdade, para tamanho k, temos 2 filhos: um de tamanho j, outro de tamanho k-j-1.
    Se contamos subproblemas (nao comparacoes), a transicao e:
    
    L[j, k] = 1/k  para cada j em {0, ..., k-1}  (filho esquerdo)
            + 1/k  para cada j em {0, ..., k-1}  (filho direito)
    
    Simplificando: cada tamanho j < k tem probabilidade 2/k de ser gerado.
    """
    
    def __init__(self, n: int):
        self.n = n
        self.n_states = n + 1  # 0, 1, ..., n
        
        self.L = np.zeros((self.n_states, self.n_states))
        self._build_operator()
    
    def _build_operator(self):
        """
        Constroi operador de transicao.
        
        L[j, k] = probabilidade de gerar subproblema de tamanho j
                  a partir de subproblema de tamanho k
        """
        for k in range(2, self.n + 1):  # k >= 2 tem transicoes nao-triviais
            # Cada pivot divide em (i, k-i-1) com prob 1/k
            # Precisamos contar quantas vezes cada j aparece
            
            count = np.zeros(self.n_states)
            for pivot_pos in range(k):
                left_size = pivot_pos
                right_size = k - pivot_pos - 1
                count[left_size] += 1
                count[right_size] += 1
            
            # Normaliza pela probabilidade 1/k de cada pivot
            # E pelo fato de que geramos 2 filhos
            self.L[:, k] = count / k
        
        # k = 0, 1 sao absorventes (nao geram novos subproblemas)
        self.L[0, 0] = 1.0
        self.L[1, 1] = 1.0  # Ou L[0, 1] = 1 se quisermos que tamanho 1 gere tamanho 0
    
    def spectrum(self) -> np.ndarray:
        """Autovalores do operador"""
        eigenvalues = np.linalg.eigvals(self.L)
        return np.sort(np.abs(eigenvalues))[::-1]
    
    def expected_work_from_size(self, k: int) -> float:
        """
        Trabalho esperado (comparacoes) para resolver subproblema de tamanho k.
        
        Recorrencia: W(k) = k - 1 + (2/k) * sum_{j=0}^{k-1} W(j)
        
        Solucao: W(k) = 2(k+1)H_k - 4k (formula conhecida)
        """
        if k <= 1:
            return 0.0
        
        H_k = sum(1.0/i for i in range(1, k + 1))
        return 2 * (k + 1) * H_k - 4 * k


class DepthOperator:
    """
    Operador que rastreia PROFUNDIDADE na arvore de recursao.
    
    Profundidade esperada do quicksort: ~2 ln n
    
    Estado = profundidade atual
    Transicao: profundidade d -> profundidade d+1 (sempre)
    
    O interessante e: qual e a DISTRIBUICAO de profundidades
    quando o algoritmo termina?
    """
    
    def __init__(self, n: int, max_depth: int = 50):
        self.n = n
        self.max_depth = max_depth
        
    def expected_depth(self) -> float:
        """
        Profundidade esperada da arvore de recursao.
        
        E[D_n] ~ 2 ln n (para quicksort aleatorio)
        """
        return 2 * np.log(self.n)
    
    def max_depth_expected(self) -> float:
        """
        Profundidade maxima esperada.
        
        E[max D_n] ~ 4.31 ln n (Devroye 1986)
        """
        return 4.31 * np.log(self.n)


def demonstrate_recursive_operators():
    """
    Demonstra operadores que capturam a recursao.
    """
    print("=" * 70)
    print("STAGE 34.4: OPERADORES QUE CAPTURAM A RECURSAO")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("1. OPERADOR DE TAMANHO DE SUBPROBLEMA")
    print("=" * 70)
    
    for n in [5, 8, 10, 15]:
        op = SubproblemSizeOperator(n)
        
        print(f"\n--- n = {n} ---")
        print(f"Espaco de estados: {op.n_states}")
        
        spectrum = op.spectrum()
        print(f"Autovalores (top 5): {spectrum[:5]}")
        
        # Trabalho esperado
        W_n = op.expected_work_from_size(n)
        n_log_n = 1.39 * n * np.log2(n)
        
        print(f"Trabalho esperado: {W_n:.2f}")
        print(f"1.39 n log_2 n:    {n_log_n:.2f}")
    
    print("\n" + "=" * 70)
    print("2. MATRIZ DE TRANSICAO (n=5)")
    print("=" * 70)
    
    n = 5
    op = SubproblemSizeOperator(n)
    
    print(f"\nMatriz L (tamanho -> tamanho):")
    print("     " + "".join(f"{j:>6}" for j in range(n + 1)))
    for k in range(n + 1):
        row = "".join(f"{op.L[j, k]:>6.2f}" for j in range(n + 1))
        print(f" {k}:  {row}")
    
    print("\n" + "=" * 70)
    print("3. ESPECTRO DO OPERADOR DE TAMANHO")
    print("=" * 70)
    
    print("\n" + "-" * 60)
    print(f"{'n':>4} {'|S|':>6} {'lambda_1':>10} {'lambda_2':>10} {'gap':>10}")
    print("-" * 60)
    
    for n in [5, 8, 10, 15, 20]:
        op = SubproblemSizeOperator(n)
        spectrum = op.spectrum()
        
        gap = spectrum[0] - spectrum[1] if len(spectrum) > 1 else 0
        
        print(f"{n:>4} {op.n_states:>6} {spectrum[0]:>10.4f} {spectrum[1]:>10.4f} {gap:>10.4f}")
    
    print("\n" + "=" * 70)
    print("4. COMPARACAO: TRABALHO ESPERADO vs n log n")
    print("=" * 70)
    
    print("\n" + "-" * 70)
    print(f"{'n':>4} {'W(n)':>12} {'2n ln n':>12} {'1.39n log2 n':>14} {'Ratio':>10}")
    print("-" * 70)
    
    for n in [5, 10, 20, 50, 100]:
        op = SubproblemSizeOperator(min(n, 50))  # Limita para nao explodir
        
        W_n = op.expected_work_from_size(n)
        two_n_ln_n = 2 * n * np.log(n)
        n_log_n = 1.39 * n * np.log2(n)
        ratio = W_n / n_log_n if n_log_n > 0 else 0
        
        print(f"{n:>4} {W_n:>12.2f} {two_n_ln_n:>12.2f} {n_log_n:>14.2f} {ratio:>10.4f}")
    
    print("\n" + "=" * 70)
    print("5. PROFUNDIDADE DA ARVORE")
    print("=" * 70)
    
    print("\n" + "-" * 50)
    print(f"{'n':>4} {'E[depth]':>12} {'2 ln n':>12} {'E[max depth]':>14}")
    print("-" * 50)
    
    for n in [5, 10, 20, 50, 100]:
        depth_op = DepthOperator(n)
        
        exp_depth = depth_op.expected_depth()
        two_ln_n = 2 * np.log(n)
        max_depth = depth_op.max_depth_expected()
        
        print(f"{n:>4} {exp_depth:>12.2f} {two_ln_n:>12.2f} {max_depth:>14.2f}")
    
    print("\n" + "=" * 70)
    print("6. RESULTADO")
    print("=" * 70)
    
    print("""
    DESCOBERTAS:
    ------------
    1. O OPERADOR DE TAMANHO DE SUBPROBLEMA e o correto!
       - Estado = tamanho do subproblema
       - Transicao = distribuicao de tamanhos dos filhos
       
    2. O espectro deste operador tem estrutura clara:
       - Autovalor 1 com multiplicidade alta (estados absorventes)
       - Outros autovalores < 1
       
    3. O trabalho esperado W(n) = 2(n+1)H_n - 4n
       - Isso e EXATAMENTE 2n ln n + O(n)
       - Confirma complexidade O(n log n)
       
    4. A profundidade esperada e O(log n):
       - E[depth] ~ 2 ln n
       - Cada nivel processa ~n comparacoes (no total)
       - Total: O(n) * O(log n) = O(n log n)
    
    INSIGHT CRITICO:
    ----------------
    O operador CERTO nao e em S_n (permutacoes).
    O operador CERTO e no espaco de TAMANHOS.
    
    A complexidade O(n log n) emerge DIRETAMENTE da formula:
    
        W(n) = n - 1 + (2/n) * sum_{k=0}^{n-1} W(k)
    
    Esta recorrencia TEM SOLUCAO EXATA:
    
        W(n) = 2n ln n + O(n)
    
    CONCLUSAO:
    ----------
    NAO precisamos de teoria espectral elaborada para obter n log n.
    A recorrencia classica ja da a resposta.
    
    MAS: a teoria espectral PODE dar informacoes adicionais:
    - Variancia da complexidade
    - Distribuicao de profundidades
    - Transicoes de fase (para variantes do quicksort)
    
    PROXIMO PASSO:
    --------------
    Stage 34.5: Conectar espectro com VARIANCIA da complexidade.
    
    Hipotese: segundo autovalor determina variancia.
    """)
    
    print("=" * 70)


def main():
    demonstrate_recursive_operators()


if __name__ == "__main__":
    main()
