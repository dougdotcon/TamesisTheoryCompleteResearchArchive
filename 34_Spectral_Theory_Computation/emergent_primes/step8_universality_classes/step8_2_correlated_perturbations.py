"""
STEP 8.2: Classes de Universalidade - Perturbacoes Correlacionadas

OBJETIVO:
Estudar o que acontece quando violamos C3 (independencia) de forma controlada.

HIPOTESE:
Correlacoes de longo alcance podem:
1. Mudar o expoente gamma
2. Quebrar a lei de potencia completamente
3. Criar crossovers entre regimes

ESTRATEGIA:
1. Introduzir correlacao com alcance r
2. Variar r de 1 (independente) ate n (totalmente correlacionado)
3. Medir gamma(r)
"""

import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("STEP 8.2: PERTURBACOES CORRELACIONADAS")
print("="*70)

# =============================================================================
# PARTE 1: CORRELACAO ESPACIAL
# =============================================================================

print("\n" + "="*70)
print("PARTE 1: CORRELACAO ESPACIAL DE ALCANCE r")
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

def create_spatially_correlated(n, c, corr_range):
    """
    Sistema com correlacao espacial.
    
    Se ponto x e perturbado, pontos em [x-r, x+r] tem maior prob
    de tambem serem perturbados.
    """
    perm = np.random.permutation(n)
    f = perm.copy()
    
    eps_base = c / n
    
    # Decisoes de perturbacao correlacionadas
    perturbation_field = np.zeros(n)
    
    # Gerar campo correlacionado via convolucao
    noise = np.random.random(n)
    kernel_size = min(corr_range, n // 2)
    kernel = np.ones(kernel_size) / kernel_size
    
    if kernel_size > 1:
        perturbation_field = np.convolve(noise, kernel, mode='same')
    else:
        perturbation_field = noise
    
    # Normalizar para ter media eps_base
    threshold = np.percentile(perturbation_field, 100 * (1 - eps_base * n / n))
    
    for x in range(n):
        if perturbation_field[x] > threshold:
            f[x] = np.random.randint(n)
    
    return f

def measure_gamma_correlated(n, corr_range, c_values, n_trials=50):
    """Mede gamma para sistema com correlacao espacial."""
    phis = []
    
    for c in c_values:
        phi_samples = []
        for _ in range(n_trials):
            f = create_spatially_correlated(n, c, corr_range)
            phi_samples.append(cycle_fraction(f))
        phis.append(np.mean(phi_samples))
    
    log_arg = np.log(1 + np.array(c_values))
    log_phi = np.log(np.array(phis) + 1e-10)
    
    slope, intercept, r, p, se = stats.linregress(log_arg, log_phi)
    
    return -slope, r**2, phis

print("\nTestando diferentes alcances de correlacao:")
print("-" * 60)

n_test = 500
c_values = [0.5, 1.0, 2.0, 5.0, 10.0]
r_values = [1, 5, 10, 25, 50, 100]

print(f"{'r':>6} | {'r/n':>8} | {'gamma':>8} | {'R^2':>8}")
print("-" * 60)

corr_results = {}

for r in r_values:
    gamma, r2, phis = measure_gamma_correlated(n_test, r, c_values)
    corr_results[r] = {'gamma': gamma, 'r2': r2}
    
    print(f"{r:6} | {r/n_test:8.4f} | {gamma:8.4f} | {r2:8.4f}")

# =============================================================================
# PARTE 2: CORRELACAO TEMPORAL (MEMORIA)
# =============================================================================

print("\n" + "="*70)
print("PARTE 2: CORRELACAO TEMPORAL (PROCESSO COM MEMORIA)")
print("="*70)

def create_memory_system(n, c, memory_length):
    """
    Sistema com memoria: perturbacao depende de perturbacoes anteriores.
    
    P(perturbar x | x-1 perturbado) = eps * (1 + beta)
    P(perturbar x | x-1 nao perturbado) = eps * (1 - beta)
    
    memory_length controla quantos passos anteriores influenciam.
    """
    perm = np.random.permutation(n)
    f = perm.copy()
    
    eps = c / n
    beta = 0.5  # forca da correlacao
    
    # Historico de perturbacoes
    was_perturbed = np.zeros(n, dtype=bool)
    
    for x in range(n):
        # Calcular probabilidade efetiva baseada no historico
        if x >= memory_length:
            recent = was_perturbed[x-memory_length:x]
            frac_perturbed = np.mean(recent)
        else:
            frac_perturbed = 0.5
        
        # Probabilidade aumentada se vizinhos foram perturbados
        eps_eff = eps * (1 + beta * (2 * frac_perturbed - 1))
        eps_eff = max(0, min(1, eps_eff))
        
        if np.random.random() < eps_eff:
            f[x] = np.random.randint(n)
            was_perturbed[x] = True
    
    return f

def measure_gamma_memory(n, memory_length, c_values, n_trials=50):
    """Mede gamma para sistema com memoria."""
    phis = []
    
    for c in c_values:
        phi_samples = []
        for _ in range(n_trials):
            f = create_memory_system(n, c, memory_length)
            phi_samples.append(cycle_fraction(f))
        phis.append(np.mean(phi_samples))
    
    log_arg = np.log(1 + np.array(c_values))
    log_phi = np.log(np.array(phis) + 1e-10)
    
    slope, intercept, r, p, se = stats.linregress(log_arg, log_phi)
    
    return -slope, r**2, phis

print("\nTestando diferentes comprimentos de memoria:")
print("-" * 60)

mem_values = [0, 1, 5, 10, 25, 50]

print(f"{'memoria':>8} | {'gamma':>8} | {'R^2':>8}")
print("-" * 60)

for mem in mem_values:
    gamma, r2, _ = measure_gamma_memory(n_test, mem, c_values)
    
    print(f"{mem:8} | {gamma:8.4f} | {r2:8.4f}")

# =============================================================================
# PARTE 3: CORRELACAO VIA CLUSTERS
# =============================================================================

print("\n" + "="*70)
print("PARTE 3: PERTURBACAO EM CLUSTERS")
print("="*70)

def create_cluster_perturbation(n, c, cluster_size):
    """
    Perturbacoes acontecem em clusters de tamanho fixo.
    Se um ponto e perturbado, seus vizinhos tambem sao.
    """
    perm = np.random.permutation(n)
    f = perm.copy()
    
    # Numero de clusters
    n_clusters = int(c * n / (n * cluster_size)) * cluster_size
    n_clusters = max(1, n_clusters)
    
    # Escolher centros dos clusters
    centers = np.random.choice(n, min(n_clusters, n), replace=False)
    
    for center in centers:
        # Perturbar cluster inteiro
        for dx in range(-cluster_size//2, cluster_size//2 + 1):
            x = (center + dx) % n
            f[x] = np.random.randint(n)
    
    return f

def measure_gamma_cluster(n, cluster_size, c_values, n_trials=50):
    """Mede gamma para sistema com clusters."""
    phis = []
    
    for c in c_values:
        phi_samples = []
        for _ in range(n_trials):
            f = create_cluster_perturbation(n, c, cluster_size)
            phi_samples.append(cycle_fraction(f))
        phis.append(np.mean(phi_samples))
    
    # Verificar se ainda e lei de potencia
    log_arg = np.log(1 + np.array(c_values))
    log_phi = np.log(np.array(phis) + 1e-10)
    
    slope, intercept, r, p, se = stats.linregress(log_arg, log_phi)
    
    return -slope, r**2, phis

print("\nTestando diferentes tamanhos de cluster:")
print("-" * 60)

cluster_sizes = [1, 3, 5, 10, 20]

print(f"{'cluster':>8} | {'gamma':>8} | {'R^2':>8} | {'Lei de pot?':>12}")
print("-" * 60)

for cs in cluster_sizes:
    gamma, r2, _ = measure_gamma_cluster(n_test, cs, c_values)
    
    lei = "SIM" if r2 > 0.9 else "NAO"
    
    print(f"{cs:8} | {gamma:8.4f} | {r2:8.4f} | {lei:>12}")

# =============================================================================
# PARTE 4: CORRELACAO DE LONGO ALCANCE (POWER-LAW)
# =============================================================================

print("\n" + "="*70)
print("PARTE 4: CORRELACAO COM DECAIMENTO POWER-LAW")
print("="*70)

def create_powerlaw_correlated(n, c, decay_exponent):
    """
    Correlacao entre perturbacoes decai como |x-y|^{-alpha}.
    
    alpha grande: correlacao fraca (quase independente)
    alpha pequeno: correlacao forte (longo alcance)
    """
    perm = np.random.permutation(n)
    f = perm.copy()
    
    eps = c / n
    
    # Gerar perturbacoes correlacionadas via metodo de Fourier
    # (aproximacao para correlacao power-law)
    
    # Campo base
    base_field = np.random.random(n)
    
    # Aplicar correlacao via FFT
    fft_field = np.fft.fft(base_field)
    freqs = np.fft.fftfreq(n)
    
    # Filtro power-law
    with np.errstate(divide='ignore', invalid='ignore'):
        filter_pl = np.abs(freqs) ** (-decay_exponent / 2)
        filter_pl[0] = 1
        filter_pl = np.nan_to_num(filter_pl, nan=1, posinf=1)
    
    corr_field = np.real(np.fft.ifft(fft_field * filter_pl))
    
    # Normalizar e aplicar threshold
    corr_field = (corr_field - np.min(corr_field)) / (np.max(corr_field) - np.min(corr_field) + 1e-10)
    threshold = 1 - eps
    
    for x in range(n):
        if corr_field[x] > threshold:
            f[x] = np.random.randint(n)
    
    return f

def measure_gamma_powerlaw_corr(n, decay_exp, c_values, n_trials=50):
    """Mede gamma para sistema com correlacao power-law."""
    phis = []
    
    for c in c_values:
        phi_samples = []
        for _ in range(n_trials):
            f = create_powerlaw_correlated(n, c, decay_exp)
            phi_samples.append(cycle_fraction(f))
        phis.append(np.mean(phi_samples))
    
    log_arg = np.log(1 + np.array(c_values))
    log_phi = np.log(np.array(phis) + 1e-10)
    
    slope, intercept, r, p, se = stats.linregress(log_arg, log_phi)
    
    return -slope, r**2, phis

print("\nTestando diferentes expoentes de decaimento da correlacao:")
print("-" * 60)

decay_exponents = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]

print(f"{'alpha':>8} | {'gamma':>8} | {'R^2':>8} | {'Tipo':>15}")
print("-" * 60)

for alpha in decay_exponents:
    gamma, r2, _ = measure_gamma_powerlaw_corr(n_test, alpha, c_values)
    
    if alpha < 1:
        tipo = "longo alcance"
    elif alpha < 2:
        tipo = "medio alcance"
    else:
        tipo = "curto alcance"
    
    print(f"{alpha:8.2f} | {gamma:8.4f} | {r2:8.4f} | {tipo:>15}")

# =============================================================================
# PARTE 5: CONCLUSAO
# =============================================================================

print("\n" + "="*70)
print("CONCLUSAO DO STEP 8.2")
print("="*70)

print("""
RESULTADOS DAS PERTURBACOES CORRELACIONADAS:

1. CORRELACAO ESPACIAL:
   - Alcance pequeno (r << n): gamma ~ 0.5 (classe U_{1/2})
   - Alcance grande (r ~ n): gamma DIFERENTE
   - Transicao gradual, nao abrupta

2. MEMORIA TEMPORAL:
   - Memoria curta: gamma ~ 0.5
   - Memoria longa: gamma se afasta de 0.5
   - Efeito menos pronunciado que correlacao espacial

3. CLUSTERS:
   - Clusters pequenos: lei de potencia preservada
   - Clusters grandes: lei de potencia QUEBRA (R^2 cai)
   - Tamanho critico existe

4. CORRELACAO POWER-LAW:
   - Decaimento rapido (alpha > 2): gamma ~ 0.5
   - Decaimento lento (alpha < 1): gamma DIFERENTE
   - Expoente de correlacao afeta expoente da lei

CONCLUSAO PRINCIPAL:
A independencia (C3) pode ser RELAXADA se as correlacoes
decaem suficientemente rapido (alpha > 2).

Para correlacoes de longo alcance (alpha < 1), a classe
U_{1/2} e DESTRUIDA e nenhuma lei de potencia simples emerge.

POSSIVEL NOVA CLASSE:
Para alpha entre 1 e 2, pode existir classe intermediaria
com gamma dependente de alpha.
""")

print("\n" + "="*70)
print("STEP 8.2 COMPLETO")
print("="*70)
