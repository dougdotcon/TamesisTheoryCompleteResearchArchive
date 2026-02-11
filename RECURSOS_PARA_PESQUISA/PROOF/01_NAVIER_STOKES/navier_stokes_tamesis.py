"""
Navier-Stokes Tamesis Simulation v3.0
=====================================
DESIGN SIMPLIFICADO PARA EMERGÊNCIA REAL

Lições aprendidas:
1. Supressão (1 + (E/E0)²)⁻¹ é fraca demais
2. Redistribuição via Laplaciano pode desestabilizar
3. Parâmetros precisam ser calibrados para competição real

NOVA ABORDAGEM:
- Fonte com supressão EXPONENCIAL (não quadrática)
- Redistribuição simples: apenas difusão AUMENTADA quando E > threshold
- Sem termos complexos que podem desestabilizar

OUTPUT: energia_maxima_vs_tempo.png (fundo claro)
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

GRID_SIZE = 25
TIMESTEPS = 300
DT = 0.01

# Fonte
SOURCE_RATE = 2.0       # Intensidade base
GROWTH_RATE = 1.03      # Crescimento temporal

# Difusão
DIFFUSION_BASE = 0.1    # Difusão base (igual para ambos)

# Tamesis
THRESHOLD = 30.0        # Escala de saturação
ENHANCED_DIFFUSION = 0.5  # Difusão extra quando E > threshold

# ============================================================================
# SIMULAÇÃO CLÁSSICA
# ============================================================================

def simulate_classical():
    """Difusão constante + fonte crescente"""
    grid = np.ones((GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    max_E = []
    total_E = []
    var_E = []
    
    center = GRID_SIZE // 2
    r = 2
    
    for t in range(TIMESTEPS):
        # Laplaciano
        lap = np.zeros_like(grid)
        lap[1:-1, 1:-1, 1:-1] = DIFFUSION_BASE * (
            grid[:-2, 1:-1, 1:-1] + grid[2:, 1:-1, 1:-1] +
            grid[1:-1, :-2, 1:-1] + grid[1:-1, 2:, 1:-1] +
            grid[1:-1, 1:-1, :-2] + grid[1:-1, 1:-1, 2:] -
            6 * grid[1:-1, 1:-1, 1:-1]
        )
        
        # Fonte crescente
        source = np.zeros_like(grid)
        intensity = SOURCE_RATE * (GROWTH_RATE ** t) * DT
        source[center-r:center+r, center-r:center+r, center-r:center+r] = intensity
        
        # Update
        grid = grid + lap + source
        grid = np.maximum(grid, 0)
        
        # Métricas
        max_E.append(np.max(grid))
        total_E.append(np.sum(grid))
        var_E.append(np.var(grid))
        
        if np.max(grid) > 1e6:
            remaining = TIMESTEPS - t - 1
            max_E.extend([np.inf] * remaining)
            total_E.extend([np.inf] * remaining)
            var_E.extend([np.inf] * remaining)
            break
    
    return {'max': max_E, 'total': total_E, 'var': var_E}

# ============================================================================
# SIMULAÇÃO TAMESIS v3.0
# ============================================================================

def simulate_tamesis():
    """
    MECANISMOS TAMESIS v3.0:
    
    1. FONTE COM SUPRESSÃO EXPONENCIAL:
       S(E) = S0 × exp(-E / threshold)
       Quando E >> threshold, fonte → 0 muito rapidamente
    
    2. DIFUSÃO ADAPTATIVA:
       D(E) = D_base + D_extra × sigmoid(E - threshold)
       Regiões saturadas difundem mais rápido
    
    NÃO HÁ CLAMP. A estabilidade emerge de:
    - Fonte que se esgota onde energia é alta
    - Difusão que aumenta para espalhar concentrações
    """
    grid = np.ones((GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    max_E = []
    total_E = []
    var_E = []
    center_E = []
    
    center = GRID_SIZE // 2
    r = 2
    region = (slice(center-r, center+r), slice(center-r, center+r), slice(center-r, center+r))
    
    for t in range(TIMESTEPS):
        # =====================================================================
        # 1. DIFUSÃO ADAPTATIVA
        # =====================================================================
        # Coeficiente de difusão local: maior onde E é alto
        sigmoid = 1.0 / (1.0 + np.exp(-(grid - THRESHOLD)))
        local_D = DIFFUSION_BASE + ENHANCED_DIFFUSION * sigmoid
        
        # Laplaciano com difusão variável
        lap = np.zeros_like(grid)
        lap[1:-1, 1:-1, 1:-1] = local_D[1:-1, 1:-1, 1:-1] * (
            grid[:-2, 1:-1, 1:-1] + grid[2:, 1:-1, 1:-1] +
            grid[1:-1, :-2, 1:-1] + grid[1:-1, 2:, 1:-1] +
            grid[1:-1, 1:-1, :-2] + grid[1:-1, 1:-1, 2:] -
            6 * grid[1:-1, 1:-1, 1:-1]
        )
        
        # =====================================================================
        # 2. FONTE COM SUPRESSÃO EXPONENCIAL
        # =====================================================================
        local_energy = grid[region]
        
        # Supressão exponencial: decai rapidamente quando E > threshold
        suppression = np.exp(-local_energy / THRESHOLD)
        
        base_intensity = SOURCE_RATE * (GROWTH_RATE ** t) * DT
        source = np.zeros_like(grid)
        source[region] = base_intensity * suppression
        
        # =====================================================================
        # UPDATE
        # =====================================================================
        grid = grid + lap + source
        grid = np.maximum(grid, 0)
        
        # Métricas
        max_E.append(np.max(grid))
        total_E.append(np.sum(grid))
        var_E.append(np.var(grid))
        center_E.append(grid[center, center, center])
    
    return {'max': max_E, 'total': total_E, 'var': var_E, 'center': center_E}

# ============================================================================
# VISUALIZAÇÃO
# ============================================================================

def plot_results(classical, tamesis, output_path):
    """Gráfico com fundo claro"""
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.patch.set_facecolor('white')
    
    t = np.arange(TIMESTEPS)
    
    # Cores
    C_CLASSIC = '#c0392b'
    C_TAMESIS = '#2980b9'
    C_THRESH = '#f39c12'
    
    # =========================================================================
    # 1. Energia Máxima
    # =========================================================================
    ax = axes[0, 0]
    ax.set_facecolor('#f8f8f8')
    
    c_max = np.array(classical['max'])
    valid = np.isfinite(c_max)
    
    ax.semilogy(t[valid], c_max[valid], color=C_CLASSIC, linewidth=2, label='Clássico')
    
    if not np.all(valid):
        blow_t = np.argmax(~valid)
        ax.axvline(x=blow_t, color=C_CLASSIC, linestyle='--', alpha=0.4)
        ax.text(blow_t + 5, c_max[blow_t-1] * 0.5, 'BLOW-UP', color=C_CLASSIC, fontsize=9)
    
    ax.semilogy(t, tamesis['max'], color=C_TAMESIS, linewidth=2.5, label='Tamesis')
    ax.axhline(y=THRESHOLD, color=C_THRESH, linestyle=':', label=f'Threshold={THRESHOLD}')
    
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Energia Máxima (log)')
    ax.set_title('Energia Máxima', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # =========================================================================
    # 2. Energia Total
    # =========================================================================
    ax = axes[0, 1]
    ax.set_facecolor('#f8f8f8')
    
    c_tot = np.array(classical['total'])
    valid = np.isfinite(c_tot)
    
    ax.semilogy(t[valid], c_tot[valid], color=C_CLASSIC, linewidth=2, label='Clássico')
    ax.semilogy(t, tamesis['total'], color=C_TAMESIS, linewidth=2, label='Tamesis')
    
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Energia Total (log)')
    ax.set_title('Energia Total', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # =========================================================================
    # 3. Variância
    # =========================================================================
    ax = axes[1, 0]
    ax.set_facecolor('#f8f8f8')
    
    c_var = np.array(classical['var'])
    valid = np.isfinite(c_var)
    
    ax.semilogy(t[valid], c_var[valid], color=C_CLASSIC, linewidth=2, label='Clássico')
    ax.semilogy(t, tamesis['var'], color=C_TAMESIS, linewidth=2, label='Tamesis')
    
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Variância (log)')
    ax.set_title('Concentração Espacial', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # =========================================================================
    # 4. Energia Centro vs Média
    # =========================================================================
    ax = axes[1, 1]
    ax.set_facecolor('#f8f8f8')
    
    # Tamesis: centro vs média
    t_center = np.array(tamesis['center'])
    t_mean = np.array(tamesis['total']) / (GRID_SIZE ** 3)
    
    ax.plot(t, t_center, color=C_TAMESIS, linewidth=2, label='Centro (ponto de injeção)')
    ax.plot(t, t_mean, color=C_TAMESIS, linewidth=2, linestyle='--', label='Média do grid')
    ax.axhline(y=THRESHOLD, color=C_THRESH, linestyle=':', label='Threshold')
    
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Energia')
    ax.set_title('Tamesis: Centro vs Média\n(Dispersão da Energia)', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Anotação
    fig.text(0.5, 0.01,
             'v3.0: Fonte exp(-E/T) + Difusão adaptativa. Sem clamp.\n'
             'Estabilização emerge de: (1) Fonte se esgota, (2) Difusão aumentada dispersa picos.',
             ha='center', fontsize=9, style='italic', color='#555')
    
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(output_path, dpi=150, facecolor='white')
    plt.close()
    
    print(f"✓ Gráfico: {output_path}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 65)
    print("NAVIER-STOKES TAMESIS v3.0 - DESIGN SIMPLIFICADO")
    print("=" * 65)
    print(f"\nConfig: Grid {GRID_SIZE}³, {TIMESTEPS} steps")
    print(f"Threshold: {THRESHOLD}, Growth: {GROWTH_RATE}")
    print(f"\nMecanismos: (1) Fonte exp(-E/T), (2) Difusão adaptativa")
    print("Sem clamp. Esperando estabilização emergente.\n")
    
    print("[1/3] Simulando CLÁSSICO...")
    classical = simulate_classical()
    
    print("[2/3] Simulando TAMESIS...")
    tamesis = simulate_tamesis()
    
    print("[3/3] Gerando gráfico...\n")
    output = os.path.join(os.path.dirname(__file__), 'energia_maxima_vs_tempo.png')
    plot_results(classical, tamesis, output)
    
    # Análise
    c_blow = not np.isfinite(classical['max'][-1])
    t_max = max(tamesis['max'])
    t_final = tamesis['max'][-1]
    
    print("=" * 65)
    print("RESULTADO:")
    print("=" * 65)
    c_final_str = 'BLOW-UP' if c_blow else f"{classical['max'][-1]:.1f}"
    print(f"  Clássico: {c_final_str}")
    print(f"  Tamesis:  final={t_final:.2f}, pico={t_max:.2f}")
    print(f"  Threshold: {THRESHOLD}")
    
    if t_final < t_max * 0.9:
        print(f"\n  ✓ Pico seguido de estabilização/decaimento")
    if t_final < THRESHOLD * 3:
        print(f"  ✓ Energia final ~{t_final:.0f} (< 3× threshold)")
    
    # Flutuação
    last = tamesis['max'][-30:]
    cv = np.std(last) / np.mean(last) * 100
    print(f"\n  Coef. Variação (últimos 30 steps): {cv:.1f}%")
    
    print("=" * 65)

if __name__ == "__main__":
    main()
