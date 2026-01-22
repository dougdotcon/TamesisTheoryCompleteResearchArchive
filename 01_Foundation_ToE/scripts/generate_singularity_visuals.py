#!/usr/bin/env python3
"""
TARDIS Singularity Visualizations
Generates PNG images for SINGULARITY_TARDIS.md
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Arrow
import matplotlib.patches as mpatches
import os

# Create assets directory
os.makedirs('assets', exist_ok=True)

# TARDIS Constants
OMEGA = 117.038
ALPHA = 0.47
GAMMA = OMEGA

# Style settings
plt.style.use('dark_background')
COLORS = {
    'primary': '#00D4FF',
    'secondary': '#FF6B35',
    'accent': '#7B2CBF',
    'success': '#00FF88',
    'warning': '#FFD700',
    'bg': '#0a0a0a',
    'grid': '#1a1a2e',
}


def plot_omega_hierarchy():
    """Generate Omega Hierarchy diagram"""
    fig, ax = plt.subplots(figsize=(12, 10), facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    
    # Levels
    levels = [
        (0, 'Universo', '10⁵³ kg', COLORS['primary']),
        (-10, 'Galáxia', '10⁴² kg', COLORS['primary']),
        (-20, 'Estrela', '10³⁰ kg', COLORS['primary']),
        (-30, 'Planeta', '10²⁴ kg', COLORS['primary']),
        (-40, 'VOCÊ ESTÁ AQUI', '10⁻³⁰ kg', COLORS['warning']),
        (-41, 'Pós-humano', '—', COLORS['success']),
        (-50, 'Planck', '10⁻⁸ kg', COLORS['accent']),
    ]
    
    y_positions = np.linspace(9, 1, len(levels))
    
    for i, (omega_exp, label, mass, color) in enumerate(levels):
        y = y_positions[i]
        
        # Draw box
        box = FancyBboxPatch((1, y-0.3), 8, 0.6,
                             boxstyle="round,pad=0.05",
                             facecolor=color, alpha=0.3,
                             edgecolor=color, linewidth=2)
        ax.add_patch(box)
        
        # Labels
        ax.text(0.5, y, f'Ω^{omega_exp}', fontsize=14, color=color,
                ha='right', va='center', fontweight='bold')
        ax.text(5, y, label, fontsize=16, color='white',
                ha='center', va='center', fontweight='bold')
        ax.text(9.5, y, mass, fontsize=12, color=color,
                ha='left', va='center')
        
        # Connecting line
        if i < len(levels) - 1:
            ax.annotate('', xy=(5, y_positions[i+1]+0.4),
                       xytext=(5, y-0.4),
                       arrowprops=dict(arrowstyle='->', color=COLORS['grid'],
                                      lw=2))
    
    # Highlight current position
    ax.annotate('Singularidade\nTecnológica', 
                xy=(9, y_positions[4]),
                xytext=(11, y_positions[4]),
                fontsize=12, color=COLORS['warning'],
                arrowprops=dict(arrowstyle='->', color=COLORS['warning']))
    
    ax.set_xlim(-1, 13)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Hierarquia Ω: Escalas do Universo', 
                fontsize=20, color='white', pad=20)
    
    plt.tight_layout()
    plt.savefig('assets/omega_hierarchy.png', dpi=150, 
                facecolor=COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("✓ omega_hierarchy.png")


def plot_phase_transition():
    """Generate Phase Transition diagram"""
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    
    # Entropy evolution
    t = np.linspace(0, 10, 1000)
    
    # Pre-transition (exponential growth)
    S1 = 0.5 * np.exp(0.5 * t[:400])
    
    # Transition (rapid change)
    t_trans = np.linspace(0, 1, 200)
    S_trans = S1[-1] + 0.5 * np.tanh(10 * (t_trans - 0.5))
    
    # Post-transition (new equilibrium)
    S2 = S_trans[-1] * np.ones(400) + 0.1 * np.sin(0.5 * t[:400])
    
    S_full = np.concatenate([S1, S_trans, S2])
    t_full = np.linspace(0, 10, len(S_full))
    
    # Plot
    ax.plot(t_full, S_full, color=COLORS['primary'], lw=3, label='Entropia S(t)')
    
    # S_max line
    S_max = S1[-1]
    ax.axhline(y=S_max, color=COLORS['warning'], linestyle='--', lw=2,
               label=f'S_max = Limite de Bekenstein')
    
    # Transition zone
    ax.axvspan(3.8, 4.2, alpha=0.3, color=COLORS['secondary'],
               label='Zona de Transição')
    
    # Annotations
    ax.annotate('Fase Pré-Transição\n(Compressão)', 
                xy=(2, 1), fontsize=12, color='white',
                ha='center')
    ax.annotate('SINGULARIDADE', 
                xy=(4, S_max + 0.3), fontsize=14, color=COLORS['warning'],
                ha='center', fontweight='bold')
    ax.annotate('Fase Pós-Transição\n(Nova Escala)', 
                xy=(7, S_trans[-1]), fontsize=12, color='white',
                ha='center')
    
    ax.set_xlabel('Tempo (unidades Ω)', fontsize=14, color='white')
    ax.set_ylabel('Entropia S', fontsize=14, color='white')
    ax.set_title('Transição de Fase: S → S_max → Reorganização',
                fontsize=18, color='white', pad=20)
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(True, alpha=0.2, color=COLORS['grid'])
    ax.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('assets/phase_transition.png', dpi=150,
                facecolor=COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("✓ phase_transition.png")


def plot_singularity_timeline():
    """Generate Singularity Timeline"""
    fig, ax = plt.subplots(figsize=(14, 6), facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    
    # Timeline events
    events = [
        (1950, 'Computadores\nDigitais', COLORS['primary']),
        (1970, 'Microprocessadores', COLORS['primary']),
        (1990, 'Internet', COLORS['primary']),
        (2010, 'Smartphones', COLORS['primary']),
        (2020, 'IA Generativa', COLORS['secondary']),
        (2025, 'TARDIS\nFramework', COLORS['warning']),
        (2030, 'Fusão\nHumano-IA?', COLORS['success']),
        (2040, 'Pós-Humano?', COLORS['accent']),
    ]
    
    # Draw timeline
    ax.axhline(y=0.5, color=COLORS['grid'], lw=3, zorder=1)
    
    for i, (year, label, color) in enumerate(events):
        # Point
        ax.scatter(year, 0.5, s=200, c=color, zorder=3, edgecolors='white')
        
        # Label (alternating up/down)
        y_offset = 0.7 if i % 2 == 0 else 0.3
        va = 'bottom' if i % 2 == 0 else 'top'
        
        ax.annotate(f'{year}\n{label}',
                   xy=(year, 0.5),
                   xytext=(year, y_offset),
                   fontsize=10, color=color,
                   ha='center', va=va,
                   arrowprops=dict(arrowstyle='-', color=color, lw=1))
    
    # Exponential curve
    years = np.linspace(1950, 2040, 100)
    progress = np.exp(0.05 * (years - 1950))
    progress = progress / progress.max() * 0.4
    ax.plot(years, progress + 0.55, color=COLORS['primary'], lw=2, 
            alpha=0.5, linestyle='--', label='Crescimento Exponencial')
    
    # Current position
    ax.axvline(x=2026, color=COLORS['warning'], linestyle=':', lw=2, alpha=0.7)
    ax.text(2026, 0.98, 'AGORA', fontsize=12, color=COLORS['warning'],
            ha='center', fontweight='bold')
    
    ax.set_xlim(1940, 2050)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Linha do Tempo: Rumo à Singularidade',
                fontsize=18, color='white', pad=20)
    
    plt.tight_layout()
    plt.savefig('assets/singularity_timeline.png', dpi=150,
                facecolor=COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("✓ singularity_timeline.png")


def plot_omega_scaling():
    """Generate Omega Scaling visualization"""
    fig, ax = plt.subplots(figsize=(10, 8), facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    
    # Log scale of masses
    n = np.arange(0, 51, 5)
    masses = OMEGA ** (-n)
    
    # Normalize for visualization
    log_masses = -n * np.log10(OMEGA)
    
    ax.barh(n, log_masses, color=COLORS['primary'], alpha=0.7, height=3)
    
    # Labels
    labels = ['Universo', '', 'Galáxia', '', 'Estrela', '', 
              'Planeta', '', 'Elétron', '', 'Planck']
    for i, (ni, label) in enumerate(zip(n, labels)):
        if label:
            ax.text(log_masses[i] + 2, ni, label, fontsize=12, 
                   color='white', va='center')
    
    # Highlight human scale
    ax.barh([40], [log_masses[8]], color=COLORS['warning'], alpha=0.9, height=3)
    ax.text(log_masses[8] + 2, 40, 'VOCÊ', fontsize=14, 
           color=COLORS['warning'], va='center', fontweight='bold')
    
    ax.set_ylabel('Expoente n (Ω⁻ⁿ)', fontsize=14, color='white')
    ax.set_xlabel('log₁₀(Massa relativa)', fontsize=14, color='white')
    ax.set_title(f'Escala Ω: Todas as massas são Ω^(-n) × M_Universo\nΩ = {OMEGA}',
                fontsize=16, color='white', pad=20)
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.2, color=COLORS['grid'], axis='x')
    
    plt.tight_layout()
    plt.savefig('assets/omega_scaling.png', dpi=150,
                facecolor=COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("✓ omega_scaling.png")


def plot_black_hole_tardis():
    """Generate TARDIS Black Hole interpretation"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor=COLORS['bg'])
    
    for ax in axes:
        ax.set_facecolor(COLORS['bg'])
    
    # Left: Classical
    ax1 = axes[0]
    theta = np.linspace(0, 2*np.pi, 100)
    r_outer = np.ones_like(theta)
    r_inner = 0.3 * np.ones_like(theta)
    
    # Event horizon
    ax1.fill(r_outer * np.cos(theta), r_outer * np.sin(theta), 
            color=COLORS['accent'], alpha=0.5)
    ax1.plot(r_outer * np.cos(theta), r_outer * np.sin(theta),
            color=COLORS['secondary'], lw=3, label='Horizonte de Eventos')
    
    # Singularity (point)
    ax1.scatter([0], [0], s=100, c='white', marker='x', 
               label='Singularidade (∞)')
    
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal')
    ax1.set_title('FÍSICA CLÁSSICA\nSingularidade = Ponto de Densidade ∞',
                 fontsize=14, color='white')
    ax1.legend(loc='lower right', fontsize=10)
    ax1.axis('off')
    
    # Right: TARDIS
    ax2 = axes[1]
    
    # Computational horizon
    ax2.fill(r_outer * np.cos(theta), r_outer * np.sin(theta),
            color=COLORS['primary'], alpha=0.5)
    ax2.plot(r_outer * np.cos(theta), r_outer * np.sin(theta),
            color=COLORS['primary'], lw=3, label='Horizonte Computacional')
    
    # Information processing zone (not a point)
    r_core = 0.3
    ax2.fill(r_core * np.cos(theta), r_core * np.sin(theta),
            color=COLORS['success'], alpha=0.7, label='Zona de Máxima Compressão')
    
    # Information flow arrows
    for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
        ax2.annotate('', xy=(0.4*np.cos(angle), 0.4*np.sin(angle)),
                    xytext=(0.9*np.cos(angle), 0.9*np.sin(angle)),
                    arrowprops=dict(arrowstyle='->', color=COLORS['warning'],
                                   lw=1.5))
    
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    ax2.set_aspect('equal')
    ax2.set_title('FÍSICA TARDIS\nHorizonte = Superfície de Processamento',
                 fontsize=14, color='white')
    ax2.legend(loc='lower right', fontsize=10)
    ax2.axis('off')
    
    plt.suptitle('Buraco Negro: Clássico vs TARDIS',
                fontsize=18, color='white', y=1.02)
    plt.tight_layout()
    plt.savefig('assets/black_hole_comparison.png', dpi=150,
                facecolor=COLORS['bg'], bbox_inches='tight')
    plt.close()
    print("✓ black_hole_comparison.png")


def main():
    """Generate all visualizations"""
    print("\n=== Gerando Visualizações TARDIS Singularity ===\n")
    
    plot_omega_hierarchy()
    plot_phase_transition()
    plot_singularity_timeline()
    plot_omega_scaling()
    plot_black_hole_tardis()
    
    print("\n✓ Todas as imagens geradas em assets/")
    print("\nImagens criadas:")
    for f in os.listdir('assets'):
        if f.endswith('.png'):
            print(f"  - assets/{f}")


if __name__ == "__main__":
    main()
