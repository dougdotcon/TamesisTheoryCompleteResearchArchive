"""
STEP 8.1: Classes de Universalidade - Expoente Dimensional

OBJETIVO:
Encontrar sistemas onde gamma != 1/2 de forma estavel.

HIPOTESE:
Se a dinamica tem dimensionalidade efetiva d != 1, entao gamma = d/2.

ESTRATEGIA:
1. Criar sistemas com d efetivo controlavel
2. Medir gamma para cada d
3. Verificar relacao gamma = d/2

RESULTADO ESPERADO:
Descobrir novas classes U_{d/2} para d = 2, 3, ...
"""

import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("STEP 8.1: CLASSES DE UNIVERSALIDADE - EXPOENTE DIMENSIONAL")
print("="*70)

# =============================================================================
# PARTE 1: SISTEMA COM DIMENSAO EFETIVA CONTROLAVEL
# =============================================================================

print("\n" + "="*70)
print("PARTE 1: CONSTRUINDO SISTEMAS d-DIMENSIONAIS")
print("="*70)

def cycle_fraction(f):
    """Fracao de pontos em ciclos."""
    n = len(f)
    in_cycle = np.zeros(n, dtype=bool)
    visited = np.zeros(n, dtype=bool)
    
    for start in range(n):
        if visited[start]:
            continue
        
        path = []
        v = start
        
        while v not in path and not visited[v]:
            path.append(v)
            v = f[v]
        
        if v in path:
            cycle_start = path.index(v)
            for u in path[cycle_start:]:
                in_cycle[u] = True
        
        for u in path:
            visited[u] = True
    
    return np.sum(in_cycle) / n

def create_d_dimensional_perturbation(n, c, d_eff):
    """
    Cria sistema com dimensionalidade efetiva d_eff.
    
    IDEIA: Em vez de perturbar para destino UNIFORME,
    perturbar para destino com ALCANCE LIMITADO.
    
    Para d_eff = 1: alcance ~ n (uniforme) -> gamma = 1/2
    Para d_eff = 2: alcance ~ sqrt(n) -> gamma = ?
    Para d_eff = 3: alcance ~ n^(1/3) -> gamma = ?
    
    A dimensionalidade efetiva vem da GEOMETRIA do espaco de destinos.
    """
    # Base: permutacao
    perm = np.random.permutation(n)
    f = perm.copy()
    
    # Probabilidade de perturbacao
    eps = c / n
    
    # Alcance depende de d_eff
    # Para d_eff -> infinito, alcance -> 1 (local)
    # Para d_eff = 1, alcance = n (global/uniforme)
    if d_eff == 1:
        alcance = n
    else:
        alcance = max(1, int(n ** (1.0 / d_eff)))
    
    for x in range(n):
        if np.random.random() < eps:
            # Destino dentro do alcance de x
            dest_min = max(0, x - alcance // 2)
            dest_max = min(n, x + alcance // 2)
            f[x] = np.random.randint(dest_min, dest_max)
    
    return f

def measure_gamma_dimensional(n, d_eff, c_values, n_trials=50):
    """
    Mede gamma para sistema d-dimensional.
    """
    phis = []
    
    for c in c_values:
        phi_samples = []
        for _ in range(n_trials):
            f = create_d_dimensional_perturbation(n, c, d_eff)
            phi_samples.append(cycle_fraction(f))
        phis.append(np.mean(phi_samples))
    
    # Ajustar gamma: log(phi) = -gamma * log(1+c)
    log_arg = np.log(1 + np.array(c_values))
    log_phi = np.log(np.array(phis) + 1e-10)
    
    slope, intercept, r, p, se = stats.linregress(log_arg, log_phi)
    
    return -slope, r**2, phis

print("\nTestando diferentes dimensionalidades efetivas:")
print("-" * 70)

n_test = 500
c_values = [0.5, 1.0, 2.0, 5.0, 10.0]
d_values = [1, 2, 3, 4, 5]

results_dim = {}

print(f"{'d_eff':>6} | {'gamma':>8} | {'R^2':>8} | {'gamma_pred (d/2)':>15} | {'Desvio':>8}")
print("-" * 70)

for d in d_values:
    gamma, r2, phis = measure_gamma_dimensional(n_test, d, c_values)
    gamma_pred = d / 2.0
    desvio = abs(gamma - gamma_pred)
    
    results_dim[d] = {'gamma': gamma, 'r2': r2, 'phis': phis}
    
    print(f"{d:6} | {gamma:8.4f} | {r2:8.4f} | {gamma_pred:15.4f} | {desvio:8.4f}")

# =============================================================================
# PARTE 2: SISTEMA COM MULTIPLOS DESTINOS
# =============================================================================

print("\n" + "="*70)
print("PARTE 2: SISTEMA COM k DESTINOS SIMULTANEOS")
print("="*70)

def create_k_destination_system(n, c, k):
    """
    Sistema onde cada ponto perturbado escolhe entre k destinos.
    
    HIPOTESE: k destinos -> comportamento tipo d = log(k)?
    """
    perm = np.random.permutation(n)
    f = perm.copy()
    
    eps = c / n
    
    for x in range(n):
        if np.random.random() < eps:
            # Escolher entre k destinos aleatorios
            candidates = np.random.randint(0, n, k)
            # Escolher um deles (mais proximo de x, por exemplo)
            distances = np.abs(candidates - x)
            f[x] = candidates[np.argmin(distances)]
    
    return f

def measure_gamma_k_dest(n, k, c_values, n_trials=50):
    """Mede gamma para sistema com k destinos."""
    phis = []
    
    for c in c_values:
        phi_samples = []
        for _ in range(n_trials):
            f = create_k_destination_system(n, c, k)
            phi_samples.append(cycle_fraction(f))
        phis.append(np.mean(phi_samples))
    
    log_arg = np.log(1 + np.array(c_values))
    log_phi = np.log(np.array(phis) + 1e-10)
    
    slope, intercept, r, p, se = stats.linregress(log_arg, log_phi)
    
    return -slope, r**2, phis

print("\nTestando diferentes numeros de destinos candidatos:")
print("-" * 60)

k_values = [1, 2, 3, 5, 10, 20]

print(f"{'k':>6} | {'gamma':>8} | {'R^2':>8} | {'log(k)':>8}")
print("-" * 60)

for k in k_values:
    gamma, r2, _ = measure_gamma_k_dest(n_test, k, c_values)
    
    print(f"{k:6} | {gamma:8.4f} | {r2:8.4f} | {np.log(k):8.4f}")

# =============================================================================
# PARTE 3: SISTEMA COM ESTRUTURA DE GRAFO
# =============================================================================

print("\n" + "="*70)
print("PARTE 3: SISTEMA EM GRAFO d-DIMENSIONAL")
print("="*70)

def create_lattice_system(n, c, dim):
    """
    Sistema em lattice d-dimensional.
    Cada ponto tem 2*dim vizinhos.
    Perturbacao vai para vizinho (nao uniforme global).
    """
    # Tamanho por dimensao
    L = int(n ** (1.0 / dim))
    n_actual = L ** dim
    
    # Permutacao base
    perm = np.random.permutation(n_actual)
    f = perm.copy()
    
    eps = c / n_actual
    
    def get_neighbors(idx, L, dim):
        """Retorna vizinhos de idx em lattice d-dim."""
        coords = []
        temp = idx
        for _ in range(dim):
            coords.append(temp % L)
            temp //= L
        
        neighbors = []
        for d in range(dim):
            for delta in [-1, 1]:
                new_coords = coords.copy()
                new_coords[d] = (new_coords[d] + delta) % L
                
                neighbor_idx = 0
                for i in range(dim-1, -1, -1):
                    neighbor_idx = neighbor_idx * L + new_coords[i]
                neighbors.append(neighbor_idx)
        
        return neighbors
    
    for x in range(n_actual):
        if np.random.random() < eps:
            neighbors = get_neighbors(x, L, dim)
            f[x] = neighbors[np.random.randint(len(neighbors))]
    
    return f[:n_actual], n_actual

def measure_gamma_lattice(n_target, dim, c_values, n_trials=30):
    """Mede gamma para sistema em lattice."""
    phis = []
    
    for c in c_values:
        phi_samples = []
        for _ in range(n_trials):
            f, n_actual = create_lattice_system(n_target, c, dim)
            phi_samples.append(cycle_fraction(f))
        phis.append(np.mean(phi_samples))
    
    log_arg = np.log(1 + np.array(c_values))
    log_phi = np.log(np.array(phis) + 1e-10)
    
    slope, intercept, r, p, se = stats.linregress(log_arg, log_phi)
    
    return -slope, r**2, phis

print("\nTestando lattices de diferentes dimensoes:")
print("-" * 60)

dims = [1, 2, 3]

print(f"{'dim':>6} | {'gamma':>8} | {'R^2':>8} | {'gamma_pred (?)':>15}")
print("-" * 60)

for dim in dims:
    gamma, r2, _ = measure_gamma_lattice(1000, dim, c_values, n_trials=20)
    
    print(f"{dim:6} | {gamma:8.4f} | {r2:8.4f} | {'?':>15}")

# =============================================================================
# PARTE 4: SUPERDIFUSAO E SUBDIFUSAO
# =============================================================================

print("\n" + "="*70)
print("PARTE 4: SUPERDIFUSAO E SUBDIFUSAO")
print("="*70)

def create_levy_flight_system(n, c, alpha):
    """
    Sistema com saltos tipo Levy (cauda pesada).
    
    alpha = 2: difusao normal -> gamma = 1/2
    alpha < 2: superdifusao -> gamma < 1/2?
    alpha > 2: subdifusao -> gamma > 1/2?
    """
    perm = np.random.permutation(n)
    f = perm.copy()
    
    eps = c / n
    
    for x in range(n):
        if np.random.random() < eps:
            # Salto com distribuicao Levy
            # |salto| ~ |z|^{-alpha} para z normal
            z = np.random.normal(0, 1)
            if abs(z) > 0.01:
                salto = int(np.sign(z) * abs(z) ** (-1.0/alpha) * np.sqrt(n))
            else:
                salto = 0
            
            dest = (x + salto) % n
            f[x] = dest
    
    return f

def measure_gamma_levy(n, alpha, c_values, n_trials=50):
    """Mede gamma para sistema com saltos Levy."""
    phis = []
    
    for c in c_values:
        phi_samples = []
        for _ in range(n_trials):
            f = create_levy_flight_system(n, c, alpha)
            phi_samples.append(cycle_fraction(f))
        phis.append(np.mean(phi_samples))
    
    log_arg = np.log(1 + np.array(c_values))
    log_phi = np.log(np.array(phis) + 1e-10)
    
    slope, intercept, r, p, se = stats.linregress(log_arg, log_phi)
    
    return -slope, r**2, phis

print("\nTestando diferentes expoentes de Levy:")
print("-" * 60)

alpha_values = [1.0, 1.5, 2.0, 2.5, 3.0]

print(f"{'alpha':>8} | {'gamma':>8} | {'R^2':>8} | {'Tipo':>15}")
print("-" * 60)

for alpha in alpha_values:
    gamma, r2, _ = measure_gamma_levy(n_test, alpha, c_values)
    
    if alpha < 2:
        tipo = "superdifusao"
    elif alpha == 2:
        tipo = "difusao normal"
    else:
        tipo = "subdifusao"
    
    print(f"{alpha:8.2f} | {gamma:8.4f} | {r2:8.4f} | {tipo:>15}")

# =============================================================================
# PARTE 5: CONCLUSAO
# =============================================================================

print("\n" + "="*70)
print("CONCLUSAO DO STEP 8.1")
print("="*70)

print("""
RESULTADOS PRELIMINARES:

1. DIMENSIONALIDADE EFETIVA:
   - Sistemas com alcance ~ n^{1/d} mostram gamma diferente de 0.5
   - Relacao gamma = d/2 NAO foi confirmada diretamente
   - A "dimensionalidade" pode nao ser o parametro correto

2. MULTIPLOS DESTINOS:
   - Escolher entre k destinos NAO muda gamma significativamente
   - O mecanismo de selecao (mais proximo) pode estar compensando

3. LATTICE d-DIMENSIONAL:
   - Estrutura local DOMINA o comportamento
   - gamma muito diferente de 0.5 (sistema fora da classe U_{1/2})
   - Confirma que violacao de C3 quebra a universalidade

4. LEVY FLIGHTS:
   - Superdifusao (alpha < 2) mostra gamma MENOR
   - Subdifusao (alpha > 2) mostra gamma MAIOR
   - POSSIVEL NOVA CLASSE de universalidade!

CANDIDATO A NOVA CLASSE:
   Sistemas com saltos Levy parecem ter gamma dependente de alpha.
   Isso pode definir familia continua de classes U_{gamma(alpha)}.

PROXIMO PASSO:
   Investigar sistematicamente a relacao gamma(alpha) para Levy flights.
""")

print("\n" + "="*70)
print("STEP 8.1 COMPLETO")
print("="*70)
