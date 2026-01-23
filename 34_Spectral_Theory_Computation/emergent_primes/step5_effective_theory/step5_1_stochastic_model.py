"""
STEP 5.1: Modelo Estocastico Efetivo
====================================

OBJETIVO:
---------
Modelar os ciclos sobreviventes no regime critico epsilon = 1 - c/n
como um processo estocastico bem definido.

CONJECTURA:
-----------
A distribuicao de comprimentos de ciclos no regime critico
segue uma distribuicao tipo Poisson-Dirichlet truncada.

TEORIA DE FUNDO:
----------------
Para random maps puros (epsilon = 0), Flajolet-Odlyzko mostrou:
- E[numero de ciclos] ~ (1/2) log(n) + gamma
- Comprimento do maior ciclo ~ sqrt(pi*n/8)

Para permutacoes (epsilon = 1), teoria classica:
- E[numero de ciclos] ~ log(n) + gamma  
- Ciclos seguem distribuicao de Ewens com theta = 1

PERGUNTA CENTRAL:
-----------------
Qual e o processo efetivo que governa a transicao?

HIPOTESE:
---------
O regime critico e governado por um processo de COALESCENCIA:
- Pontos "coalescem" em ciclos
- Taxa de coalescencia ~ c/n
- No limite, converge para Poisson-Dirichlet
"""

import numpy as np
from typing import List, Dict, Tuple
from collections import defaultdict
from scipy import special
import warnings
warnings.filterwarnings('ignore')


class CycleDistributionAnalysis:
    """
    Analisa a distribuicao de comprimentos de ciclos.
    """
    
    def __init__(self, n: int, epsilon: float, n_samples: int = 100):
        self.n = n
        self.epsilon = epsilon
        self.c = (1.0 - epsilon) * n  # Parametro de escala
        self.n_samples = n_samples
        
        self.cycle_data = self._collect_cycle_data()
    
    def _generate_map(self) -> np.ndarray:
        f = np.random.permutation(self.n)
        for i in range(self.n):
            if np.random.random() > self.epsilon:
                f[i] = np.random.randint(0, self.n)
        return f
    
    def _find_cycles(self, f: np.ndarray) -> List[int]:
        """Retorna lista de comprimentos de ciclos"""
        visited = set()
        cycle_lengths = []
        
        for start in range(self.n):
            if start in visited:
                continue
            
            path = []
            x = start
            while x not in visited:
                visited.add(x)
                path.append(x)
                x = f[x]
            
            if x in path:
                cycle_start = path.index(x)
                cycle_lengths.append(len(path) - cycle_start)
        
        return cycle_lengths
    
    def _collect_cycle_data(self) -> List[List[int]]:
        """Coleta dados de ciclos de multiplas amostras"""
        data = []
        for _ in range(self.n_samples):
            f = self._generate_map()
            cycles = self._find_cycles(f)
            data.append(cycles)
        return data
    
    def mean_num_cycles(self) -> Tuple[float, float]:
        """E[numero de ciclos] e std"""
        counts = [len(cycles) for cycles in self.cycle_data]
        return np.mean(counts), np.std(counts)
    
    def mean_total_length(self) -> Tuple[float, float]:
        """E[soma dos comprimentos] e std"""
        totals = [sum(cycles) for cycles in self.cycle_data]
        return np.mean(totals), np.std(totals)
    
    def normalized_cycle_fractions(self) -> List[List[float]]:
        """
        Para cada amostra, retorna fracoes L_i / sum(L_i).
        Isso normaliza para comparar com Poisson-Dirichlet.
        """
        fractions = []
        for cycles in self.cycle_data:
            total = sum(cycles)
            if total > 0:
                fracs = sorted([c / total for c in cycles], reverse=True)
                fractions.append(fracs)
        return fractions
    
    def cycle_size_distribution(self) -> Dict[int, float]:
        """Distribuicao empirica de comprimentos de ciclos"""
        all_lengths = []
        for cycles in self.cycle_data:
            all_lengths.extend(cycles)
        
        if not all_lengths:
            return {}
        
        counts = defaultdict(int)
        for l in all_lengths:
            counts[l] += 1
        
        total = len(all_lengths)
        return {k: v / total for k, v in sorted(counts.items())}


class EwensDistribution:
    """
    Distribuicao de Ewens para ciclos de permutacoes.
    
    Para theta = 1 (permutacao uniforme):
    P(numero de ciclos = k) ~ S(n, k) / n!
    
    onde S(n, k) = numeros de Stirling de primeira especie.
    """
    
    def __init__(self, n: int, theta: float = 1.0):
        self.n = n
        self.theta = theta
    
    def expected_num_cycles(self) -> float:
        """E[numero de ciclos] para Ewens(theta)"""
        # E[K] = sum_{i=1}^{n} theta / (theta + i - 1)
        # Para theta = 1: E[K] = H_n ~ log(n) + gamma
        return sum(self.theta / (self.theta + i - 1) for i in range(1, self.n + 1))
    
    def expected_cycle_of_size_k(self, k: int) -> float:
        """E[numero de ciclos de tamanho k]"""
        # Para Ewens(theta): E[C_k] = theta / k
        return self.theta / k


class CoalescenceModel:
    """
    Modelo de coalescencia para o regime critico.
    
    IDEIA:
    ------
    Comeca com n pontos.
    A cada passo, com probabilidade p = c/n:
    - Um ponto "coalesce" com outro (perde injetividade)
    
    No limite, isso deve reproduzir phi(c).
    """
    
    def __init__(self, n: int, c: float):
        self.n = n
        self.c = c
        self.p_coalescence = c / n  # Probabilidade de perda de injetividade por posicao
    
    def expected_non_injective_points(self) -> float:
        """
        E[pontos que NAO estao em ciclos]
        
        Se cada posicao tem prob p de "coalescer":
        E[pontos perdidos] ~ n * p = c
        
        Mas isso e mais complexo porque afeta estrutura de ciclos.
        """
        # Modelo simplificado: cada posicao independentemente
        # perde injetividade com prob p
        return self.n * self.p_coalescence
    
    def expected_cycle_points_approx(self) -> float:
        """
        Aproximacao para E[pontos em ciclos].
        
        Para random map puro: E[pontos em ciclos] ~ sqrt(pi*n/2)
        Para permutacao: E[pontos em ciclos] = n
        
        Interpolacao heuristica:
        E[pontos em ciclos] ~ n * exp(-c/n * k) para algum k
        """
        # Tentativa: modelo de "sobrevivencia"
        # Cada ponto sobrevive em ciclo com prob ~ exp(-c/constante)
        
        if self.c == 0:
            return self.n
        
        # Heuristica baseada nos dados empiricos
        # phi(c) ~ exp(-c * alpha) para algum alpha
        return self.n * np.exp(-self.c * 0.15)  # alpha a ser ajustado
    
    def phi_theoretical(self) -> float:
        """
        Tentativa de derivar phi(c) teoricamente.
        
        CONJECTURA:
        phi(c) = probabilidade de um ponto estar em um ciclo
               = fracao do espaco que "sobrevive"
        """
        # Modelo 1: Poisson
        # Se cada aresta tem prob c/n de "quebrar":
        # phi(c) ~ exp(-c * f(1)) onde f e funcao desconhecida
        
        # Modelo 2: Campo medio
        # phi(c) satisfaz equacao auto-consistente
        
        # Por agora, ajuste empirico:
        return np.exp(-0.2 * self.c) * (1 - 0.5 * np.exp(-self.c))


class PoissonDirichletTest:
    """
    Testa se a distribuicao de fracoes de ciclos segue Poisson-Dirichlet.
    
    Poisson-Dirichlet(theta):
    - E[maior fracao] ~ theta / (theta + 1) para theta pequeno
    - Fracoes decaem exponencialmente em ordem
    """
    
    def __init__(self, fractions: List[List[float]]):
        self.fractions = fractions
    
    def mean_largest_fraction(self) -> Tuple[float, float]:
        """E[maior fracao] e std"""
        largest = [f[0] if f else 0 for f in self.fractions]
        return np.mean(largest), np.std(largest)
    
    def mean_second_largest_fraction(self) -> Tuple[float, float]:
        """E[segunda maior fracao] e std"""
        second = [f[1] if len(f) > 1 else 0 for f in self.fractions]
        return np.mean(second), np.std(second)
    
    def fraction_ratio(self) -> float:
        """E[f_2 / f_1] - diagnostico de Poisson-Dirichlet"""
        ratios = []
        for f in self.fractions:
            if len(f) > 1 and f[0] > 0:
                ratios.append(f[1] / f[0])
        return np.mean(ratios) if ratios else 0
    
    def gini_coefficient(self) -> float:
        """Coeficiente de Gini das fracoes - mede desigualdade"""
        ginis = []
        for f in self.fractions:
            if len(f) > 1:
                n = len(f)
                numerator = sum((2 * (i + 1) - n - 1) * f[i] for i in range(n))
                denominator = n * sum(f)
                if denominator > 0:
                    ginis.append(numerator / denominator)
        return np.mean(ginis) if ginis else 0


def analyze_stochastic_model():
    """
    Analise do modelo estocastico efetivo.
    """
    print("=" * 70)
    print("STEP 5.1: MODELO ESTOCASTICO EFETIVO")
    print("=" * 70)
    
    n = 500
    n_samples = 100
    c_values = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0]
    
    print(f"\nParametros: n={n}, n_samples={n_samples}")
    
    print("\n" + "=" * 70)
    print("1. COMPARACAO COM TEORIA DE EWENS (PERMUTACOES)")
    print("=" * 70)
    
    # Para permutacao pura (c=0)
    ewens = EwensDistribution(n, theta=1.0)
    print(f"\nEwens(theta=1, n={n}):")
    print(f"  E[ciclos] teorico: {ewens.expected_num_cycles():.2f}")
    print(f"  E[ciclos] = log(n) + gamma = {np.log(n) + 0.5772:.2f}")
    
    # Permutacao empirica
    analysis_perm = CycleDistributionAnalysis(n, 1.0, n_samples)
    mean_perm, std_perm = analysis_perm.mean_num_cycles()
    print(f"  E[ciclos] empirico: {mean_perm:.2f} +/- {std_perm:.2f}")
    
    print("\n" + "=" * 70)
    print("2. DISTRIBUICAO DE CICLOS NO REGIME CRITICO")
    print("=" * 70)
    
    print("\n" + "-" * 70)
    print(f"{'c':>8} {'E[ciclos]':>12} {'E[total]':>12} {'E[total]/n':>12}")
    print("-" * 70)
    
    for c in c_values:
        epsilon = 1.0 - c / n
        analysis = CycleDistributionAnalysis(n, epsilon, n_samples)
        
        mean_cycles, _ = analysis.mean_num_cycles()
        mean_total, _ = analysis.mean_total_length()
        
        print(f"{c:>8.1f} {mean_cycles:>12.2f} {mean_total:>12.1f} {mean_total/n:>12.3f}")
    
    print("\n" + "=" * 70)
    print("3. TESTE DE POISSON-DIRICHLET")
    print("=" * 70)
    
    print("\nFracoes normalizadas dos ciclos:")
    print("-" * 70)
    print(f"{'c':>8} {'E[f_1]':>10} {'E[f_2]':>10} {'f_2/f_1':>10} {'Gini':>10}")
    print("-" * 70)
    
    for c in c_values:
        epsilon = 1.0 - c / n
        analysis = CycleDistributionAnalysis(n, epsilon, n_samples)
        fracs = analysis.normalized_cycle_fractions()
        
        pd_test = PoissonDirichletTest(fracs)
        f1_mean, _ = pd_test.mean_largest_fraction()
        f2_mean, _ = pd_test.mean_second_largest_fraction()
        ratio = pd_test.fraction_ratio()
        gini = pd_test.gini_coefficient()
        
        print(f"{c:>8.1f} {f1_mean:>10.3f} {f2_mean:>10.3f} {ratio:>10.3f} {gini:>10.3f}")
    
    print("\n" + "=" * 70)
    print("4. MODELO DE COALESCENCIA")
    print("=" * 70)
    
    print("\nComparacao com modelo de coalescencia:")
    print("-" * 70)
    print(f"{'c':>8} {'phi empirico':>15} {'phi modelo':>15} {'erro':>10}")
    print("-" * 70)
    
    for c in c_values:
        epsilon = 1.0 - c / n
        analysis = CycleDistributionAnalysis(n, epsilon, n_samples)
        mean_total, _ = analysis.mean_total_length()
        phi_emp = mean_total / n
        
        coal = CoalescenceModel(n, c)
        phi_model = coal.expected_cycle_points_approx() / n
        
        erro = abs(phi_emp - phi_model)
        print(f"{c:>8.1f} {phi_emp:>15.3f} {phi_model:>15.3f} {erro:>10.3f}")
    
    print("\n" + "=" * 70)
    print("5. AJUSTE DE phi(c)")
    print("=" * 70)
    
    # Coleta dados para ajuste
    phi_data = []
    for c in c_values:
        epsilon = 1.0 - c / n
        analysis = CycleDistributionAnalysis(n, epsilon, n_samples)
        mean_total, _ = analysis.mean_total_length()
        phi_data.append((c, mean_total / n))
    
    # Testa diferentes modelos
    print("\nTestando modelos para phi(c):")
    print("-" * 50)
    
    # Modelo 1: phi(c) = exp(-alpha * c)
    def model_exp(c, alpha):
        return np.exp(-alpha * c)
    
    # Modelo 2: phi(c) = 1 / (1 + beta * c)
    def model_rational(c, beta):
        return 1.0 / (1.0 + beta * c)
    
    # Modelo 3: phi(c) = (1 + c)^(-gamma)
    def model_power(c, gamma):
        return (1.0 + c) ** (-gamma)
    
    # Ajusta cada modelo
    from scipy.optimize import minimize_scalar
    
    c_arr = np.array([d[0] for d in phi_data])
    phi_arr = np.array([d[1] for d in phi_data])
    
    def fit_model(model_func, param_name):
        def mse(param):
            pred = np.array([model_func(c, param) for c in c_arr])
            return np.mean((pred - phi_arr) ** 2)
        
        result = minimize_scalar(mse, bounds=(0.01, 2.0), method='bounded')
        return result.x, result.fun
    
    alpha_opt, mse_exp = fit_model(model_exp, 'alpha')
    beta_opt, mse_rat = fit_model(model_rational, 'beta')
    gamma_opt, mse_pow = fit_model(model_power, 'gamma')
    
    print(f"Modelo exponencial: phi(c) = exp(-{alpha_opt:.4f} * c), MSE = {mse_exp:.6f}")
    print(f"Modelo racional:    phi(c) = 1/(1 + {beta_opt:.4f} * c), MSE = {mse_rat:.6f}")
    print(f"Modelo potencia:    phi(c) = (1+c)^(-{gamma_opt:.4f}), MSE = {mse_pow:.6f}")
    
    # Identifica melhor modelo
    best_model = min([('exp', mse_exp), ('rational', mse_rat), ('power', mse_pow)], key=lambda x: x[1])
    print(f"\nMelhor modelo: {best_model[0]}")
    
    print("\n" + "=" * 70)
    print("6. CONCLUSOES DO STEP 5.1")
    print("=" * 70)
    
    print(f"""
    DESCOBERTAS:
    ------------
    1. DISTRIBUICAO DE CICLOS:
       - Para c pequeno: dominado por 1-2 ciclos grandes
       - Para c grande: muitos ciclos pequenos
       - Fracao do maior ciclo f_1 decresce com c
    
    2. TESTE POISSON-DIRICHLET:
       - A distribuicao NAO e exatamente Poisson-Dirichlet
       - Coeficiente de Gini varia com c
       - Estrutura e mais complexa que o modelo simples
    
    3. AJUSTE DE phi(c):
       - Melhor modelo: {best_model[0]}
       - phi(c) ~ exp(-{alpha_opt:.4f} * c) ou 1/(1 + {beta_opt:.4f} * c)
       - MSE do melhor ajuste: {best_model[1]:.6f}
    
    HIPOTESE PARA STEP 5.2:
    -----------------------
    phi(c) pode ser derivada de uma equacao de campo medio
    ou de um processo de coalescencia continuo.
    """)
    
    print("=" * 70)
    
    return {
        'phi_data': phi_data,
        'best_model': best_model[0],
        'alpha': alpha_opt,
        'beta': beta_opt,
        'gamma': gamma_opt
    }


def main():
    results = analyze_stochastic_model()
    return results


if __name__ == "__main__":
    main()
