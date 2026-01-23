"""
Academic-Quality Visualizations for The Tamesis Action
=======================================================

Professional figures suitable for journal publication.
White background, clean typography, publication-ready.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

# Academic style
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 0.8,
    'axes.grid': False,
    'text.usetex': False,
})


def create_action_structure_diagram():
    """
    Clean diagram showing the structure of the Tamesis Action.
    Academic style with boxes and arrows.
    """
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    ax.set_facecolor('white')
    
    # Title
    ax.text(0.5, 0.95, 'THE TAMESIS ACTION', fontsize=14, fontweight='bold',
            ha='center', va='top', transform=ax.transAxes)
    ax.text(0.5, 0.88, r'$S = \int d^4x \sqrt{-g} \left[ \frac{R}{16\pi G} + \mathcal{L}_m + \mathcal{L}_\Omega + \mathcal{L}_{M_c} \right] + S_\partial$',
            fontsize=11, ha='center', va='top', transform=ax.transAxes)
    
    # Define terms with positions
    terms = [
        {'name': 'Einstein-Hilbert\n$R/16\\pi G$', 'x': 0.10, 'desc': 'GR'},
        {'name': 'Matter\n$\\mathcal{L}_m$', 'x': 0.30, 'desc': 'SM'},
        {'name': 'Reactive\n$\\mathcal{L}_\\Omega$', 'x': 0.50, 'desc': 'MOND'},
        {'name': 'Collapse\n$\\mathcal{L}_{M_c}$', 'x': 0.70, 'desc': 'QM→CL'},
        {'name': 'Boundary\n$S_\\partial$', 'x': 0.90, 'desc': 'Holography'},
    ]
    
    # Draw term boxes
    box_width = 0.15
    box_height = 0.18
    
    for term in terms:
        # Box
        rect = FancyBboxPatch((term['x'] - box_width/2, 0.52), box_width, box_height,
                              boxstyle="round,pad=0.01,rounding_size=0.02",
                              facecolor='white', edgecolor='black', linewidth=1.5,
                              transform=ax.transAxes)
        ax.add_patch(rect)
        
        # Term name
        ax.text(term['x'], 0.64, term['name'], fontsize=9, ha='center', va='center',
                transform=ax.transAxes)
        
        # Description
        ax.text(term['x'], 0.49, f"({term['desc']})", fontsize=8, ha='center', va='top',
                style='italic', color='#444444', transform=ax.transAxes)
    
    # Arrows connecting terms
    for i in range(len(terms)-1):
        ax.annotate('', xy=(terms[i+1]['x'] - box_width/2 - 0.01, 0.61),
                   xytext=(terms[i]['x'] + box_width/2 + 0.01, 0.61),
                   arrowprops=dict(arrowstyle='->', color='black', lw=1),
                   transform=ax.transAxes)
    
    # Lower section: What emerges
    ax.text(0.5, 0.38, 'EMERGENT PHYSICS', fontsize=11, fontweight='bold',
            ha='center', transform=ax.transAxes)
    
    # Horizontal line (draw as plot instead of axhline)
    ax.plot([0.1, 0.9], [0.35, 0.35], color='black', lw=0.5, transform=ax.transAxes)
    
    emergent = [
        {'regime': 'Classical', 'cond': '$M \\gg M_c$, $g \\gg a_0$', 'result': 'GR', 'x': 0.15},
        {'regime': 'Quantum', 'cond': '$M \\ll M_c$', 'result': 'QM', 'x': 0.38},
        {'regime': 'MOND', 'cond': '$g \\ll a_0$', 'result': '$v^4=GMa_0$', 'x': 0.62},
        {'regime': 'Transition', 'cond': '$M \\approx M_c$', 'result': 'Collapse', 'x': 0.85},
    ]
    
    for em in emergent:
        ax.text(em['x'], 0.28, em['regime'], fontsize=10, fontweight='bold',
                ha='center', transform=ax.transAxes)
        ax.text(em['x'], 0.21, em['cond'], fontsize=8, ha='center',
                transform=ax.transAxes)
        ax.text(em['x'], 0.14, f"→ {em['result']}", fontsize=9, ha='center',
                style='italic', transform=ax.transAxes)
    
    # Footer
    ax.text(0.5, 0.04, r'$\delta S = 0$ generates all physics',
            fontsize=10, ha='center', style='italic', transform=ax.transAxes)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('tamesis_action_diagram.png', dpi=300, facecolor='white',
                edgecolor='none', bbox_inches='tight')
    plt.close()
    print("✅ Saved: tamesis_action_diagram.png (academic style)")


def create_unification_diagram():
    """
    Clean diagram showing how four theories emerge from one action.
    """
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
    ax.set_facecolor('white')
    
    # Title
    ax.text(0.5, 0.96, 'UNIFIED PHYSICS FROM ONE ACTION', fontsize=13, fontweight='bold',
            ha='center', transform=ax.transAxes)
    
    # Central circle: Tamesis Action
    center_circle = Circle((0.5, 0.5), 0.12, facecolor='#f0f0f0',
                           edgecolor='black', linewidth=2, transform=ax.transAxes)
    ax.add_patch(center_circle)
    ax.text(0.5, 0.52, 'TAMESIS', fontsize=11, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)
    ax.text(0.5, 0.47, 'ACTION', fontsize=11, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)
    
    # Four emergent theories
    theories = [
        {'name': 'General\nRelativity', 'eq': r'$G_{\mu\nu} = 8\pi G T_{\mu\nu}$', 
         'angle': 45, 'cond': r'$M \gg M_c$'},
        {'name': 'Quantum\nMechanics', 'eq': r'$i\hbar\partial_t|\psi\rangle = H|\psi\rangle$', 
         'angle': 135, 'cond': r'$M \ll M_c$'},
        {'name': 'MOND\nGravity', 'eq': r'$g = \sqrt{g_N a_0}$', 
         'angle': 225, 'cond': r'$g \ll a_0$'},
        {'name': 'Objective\nCollapse', 'eq': r'$M > M_c \rightarrow$ classical', 
         'angle': 315, 'cond': r'$M \approx M_c$'},
    ]
    
    radius = 0.32
    theory_radius = 0.10
    
    for th in theories:
        angle_rad = np.radians(th['angle'])
        x = 0.5 + radius * np.cos(angle_rad)
        y = 0.5 + radius * np.sin(angle_rad)
        
        # Theory circle
        theory_circle = Circle((x, y), theory_radius, facecolor='white',
                               edgecolor='black', linewidth=1.5, transform=ax.transAxes)
        ax.add_patch(theory_circle)
        
        # Theory name
        ax.text(x, y + 0.02, th['name'], fontsize=9, fontweight='bold',
                ha='center', va='center', transform=ax.transAxes)
        
        # Arrow from center to theory
        arrow_start_x = 0.5 + 0.13 * np.cos(angle_rad)
        arrow_start_y = 0.5 + 0.13 * np.sin(angle_rad)
        arrow_end_x = x - theory_radius * np.cos(angle_rad)
        arrow_end_y = y - theory_radius * np.sin(angle_rad)
        
        ax.annotate('', xy=(arrow_end_x, arrow_end_y), xytext=(arrow_start_x, arrow_start_y),
                   arrowprops=dict(arrowstyle='->', color='black', lw=1.2),
                   transform=ax.transAxes)
        
        # Condition label (outside the circle)
        label_x = 0.5 + (radius + theory_radius + 0.06) * np.cos(angle_rad)
        label_y = 0.5 + (radius + theory_radius + 0.06) * np.sin(angle_rad)
        ax.text(label_x, label_y, th['cond'], fontsize=8, ha='center', va='center',
                transform=ax.transAxes, style='italic')
    
    # Footer with key parameters
    ax.text(0.5, 0.08, r'$M_c = 2.2 \times 10^{-14}$ kg   |   $a_0 = cH_0 \approx 1.2 \times 10^{-10}$ m/s²',
            fontsize=9, ha='center', transform=ax.transAxes)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('unification_diagram.png', dpi=300, facecolor='white',
                edgecolor='none', bbox_inches='tight')
    plt.close()
    print("✅ Saved: unification_diagram.png (academic style)")


def create_mc_transition_academic():
    """
    Publication-quality plot of the quantum-classical transition.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), facecolor='white')
    
    # Parameters
    M = np.logspace(-16, -12, 500)
    M_c = 2.2e-14
    
    # Visibility
    visibility_smooth = np.exp(-(M / M_c)**2)  # Smooth (mainstream)
    width = 0.05 * M_c
    visibility_step = 0.5 * (1 - np.tanh((M - M_c) / width))  # Step (Tamesis)
    
    # Plot 1: Comparison
    ax1 = axes[0]
    ax1.semilogx(M * 1e15, visibility_smooth, 'b--', lw=1.5, 
                 label='CSL/GRW (smooth)')
    ax1.semilogx(M * 1e15, visibility_step, 'r-', lw=2,
                 label='Tamesis (step)')
    ax1.axvline(M_c * 1e15, color='gray', ls=':', lw=1, label=f'$M_c$ = {M_c*1e15:.0f} fg')
    
    ax1.set_xlabel('Mass (femtograms)')
    ax1.set_ylabel('Interference Visibility')
    ax1.set_title('Quantum-Classical Transition', fontweight='bold')
    ax1.legend(loc='upper right', frameon=True, edgecolor='black')
    ax1.set_ylim(-0.05, 1.05)
    ax1.set_xlim(M[0]*1e15, M[-1]*1e15)
    
    # Plot 2: Holographic saturation
    ax2 = axes[1]
    
    m_atom = 1.67e-27
    hbar = 1.055e-34
    c = 3e8
    l_P = 1.616e-35
    
    S_required = M / m_atom
    lambda_C = hbar / (M * c)
    A = lambda_C**2
    S_max = A / (4 * l_P**2)
    
    ax2.loglog(M * 1e15, S_required, 'b-', lw=1.5, label='$S_{required}$')
    ax2.loglog(M * 1e15, S_max, 'r-', lw=1.5, label='$S_{max}$ (holographic)')
    ax2.axvline(M_c * 1e15, color='gray', ls=':', lw=1)
    
    # Find intersection for annotation
    ax2.annotate('Collapse\nTriggered', xy=(M_c*1e15, 1e12), fontsize=8,
                ha='center', style='italic')
    
    ax2.set_xlabel('Mass (femtograms)')
    ax2.set_ylabel('Entropy (bits)')
    ax2.set_title('Holographic Saturation', fontweight='bold')
    ax2.legend(loc='upper right', frameon=True, edgecolor='black')
    
    plt.tight_layout()
    plt.savefig('mc_transition.png', dpi=300, facecolor='white',
                edgecolor='none', bbox_inches='tight')
    plt.close()
    print("✅ Saved: mc_transition.png (academic style)")


def create_mond_plot_academic():
    """
    Publication-quality MOND rotation curve.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), facecolor='white')
    
    # Parameters
    a0 = 1.2e-10
    G = 6.674e-11
    M = 1e11 * 1.989e30
    
    r = np.linspace(1, 80, 200)
    r_m = r * 3.086e19
    
    g_N = G * M / r_m**2
    x = g_N / a0
    nu = 0.5 + 0.5 * np.sqrt(1 + 4/x)
    g_MOND = g_N * nu
    
    v_N = np.sqrt(g_N * r_m) / 1000
    v_MOND = np.sqrt(g_MOND * r_m) / 1000
    
    # Plot 1: Rotation curve
    ax1 = axes[0]
    ax1.plot(r, v_N, 'b--', lw=1.5, label='Newton')
    ax1.plot(r, v_MOND, 'r-', lw=2, label='MOND/Tamesis')
    ax1.axhline(220, color='gray', ls=':', lw=1, label='Observed')
    
    ax1.set_xlabel('Radius (kpc)')
    ax1.set_ylabel('Velocity (km/s)')
    ax1.set_title('Galaxy Rotation Curve', fontweight='bold')
    ax1.legend(loc='lower right', frameon=True, edgecolor='black')
    ax1.set_xlim(0, 80)
    ax1.set_ylim(0, 350)
    
    # Plot 2: Interpolation function
    ax2 = axes[1]
    
    x_plot = np.logspace(-2, 2, 200)
    nu_plot = 0.5 + 0.5 * np.sqrt(1 + 4/x_plot)
    
    ax2.loglog(x_plot, nu_plot, 'k-', lw=2)
    ax2.axhline(1, color='gray', ls='--', lw=1)
    ax2.axvline(1, color='gray', ls=':', lw=1)
    
    ax2.text(10, 1.05, 'Newton', fontsize=9, style='italic')
    ax2.text(0.05, 4, 'MOND', fontsize=9, style='italic')
    
    ax2.set_xlabel('$x = g_N / a_0$')
    ax2.set_ylabel(r'$\nu(x)$')
    ax2.set_title('Interpolation Function', fontweight='bold')
    ax2.set_xlim(0.01, 100)
    ax2.set_ylim(0.9, 20)
    
    plt.tight_layout()
    plt.savefig('mond_emergence.png', dpi=300, facecolor='white',
                edgecolor='none', bbox_inches='tight')
    plt.close()
    print("✅ Saved: mond_emergence.png (academic style)")


if __name__ == "__main__":
    print("Generating publication-quality figures...")
    print()
    
    create_action_structure_diagram()
    create_unification_diagram()
    create_mc_transition_academic()
    create_mond_plot_academic()
    
    print()
    print("All academic-quality figures generated!")
