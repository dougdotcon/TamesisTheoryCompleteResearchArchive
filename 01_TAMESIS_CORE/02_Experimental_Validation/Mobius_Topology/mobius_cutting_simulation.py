"""
=============================================================================
  TAMESIS RESEARCH PROGRAM — Möbius Strip Cutting Simulation
=============================================================================

  Demonstrates the topological consequences of cutting a Möbius strip:
  1. Center cut (1/2 width) → Single larger strip with 2 full twists
  2. Off-center cut (1/3 width) → Two interlocked strips

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-12
  Connection: TRI (Regime Nesting) + TDTR (Irreversibility) + Kernel v3

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import os

# ============================================================================
# PARAMETRIC SURFACE DEFINITIONS
# ============================================================================

def mobius_strip(u, v, R=2.0, w=0.5):
    """
    Parametric equations for a Möbius strip.
    
    u : angle along the strip [0, 2π]
    v : width parameter [-w, w]
    R : radius of central circle
    w : half-width of the strip
    """
    x = (R + v * np.cos(u / 2)) * np.cos(u)
    y = (R + v * np.cos(u / 2)) * np.sin(u)
    z = v * np.sin(u / 2)
    return x, y, z


def twisted_strip(u, v, R=2.0, w=0.5, n_half_twists=4):
    """
    Parametric equations for a strip with n half-twists (orientable if n is even).
    
    For the center-cut result: n_half_twists=4 (2 full twists)
    The strip traverses from u=0 to u=4π (double the circumference).
    """
    # For a strip with n half-twists, the twist rate is n/2 per 2π
    x = (R + v * np.cos(n_half_twists * u / 2)) * np.cos(u)
    y = (R + v * np.cos(n_half_twists * u / 2)) * np.sin(u)
    z = v * np.sin(n_half_twists * u / 2)
    return x, y, z


def center_cut_result(u, v, R=2.0, w=0.25):
    """
    The result of cutting a Möbius strip at the center:
    A single strip with 4 half-twists (2 full twists), double the length.
    Parametrize over u in [0, 4π] (goes around twice).
    """
    # The center line of the original Möbius traverses from 0 to 4π to close
    x = (R + v * np.cos(u)) * np.cos(u)
    y = (R + v * np.cos(u)) * np.sin(u)
    z = v * np.sin(u)
    return x, y, z


def offcenter_mobius_narrow(u, v, R=2.0, v_offset=0.3):
    """
    The narrow strip from off-center cut: still a Möbius strip.
    v ranges around v_offset (1/3 from one edge).
    """
    v_actual = v_offset + v * 0.15  # narrow strip near one edge
    x = (R + v_actual * np.cos(u / 2)) * np.cos(u)
    y = (R + v_actual * np.cos(u / 2)) * np.sin(u)
    z = v_actual * np.sin(u / 2)
    return x, y, z


def offcenter_large_strip(u, v, R=2.0, v_center=-0.05):
    """
    The larger strip from off-center cut: orientable with 2 full twists.
    This strip winds around twice (u in [0, 4π]).
    """
    v_actual = v_center + v * 0.2
    x = (R + v_actual * np.cos(u)) * np.cos(u)
    y = (R + v_actual * np.cos(u)) * np.sin(u)
    z = v_actual * np.sin(u)
    return x, y, z


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def setup_3d_axis(ax, title, elev=25, azim=45):
    """Configure a 3D axis with clean styling."""
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-1.5, 1.5)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('X', fontsize=9, labelpad=2)
    ax.set_ylabel('Y', fontsize=9, labelpad=2)
    ax.set_zlabel('Z', fontsize=9, labelpad=2)
    ax.view_init(elev=elev, azim=azim)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('lightgray')
    ax.yaxis.pane.set_edgecolor('lightgray')
    ax.zaxis.pane.set_edgecolor('lightgray')
    ax.tick_params(labelsize=7)


def plot_original_with_cut_lines(ax):
    """Plot the original Möbius strip with cut lines marked."""
    u = np.linspace(0, 2 * np.pi, 120)
    v = np.linspace(-0.5, 0.5, 30)
    U, V = np.meshgrid(u, v)
    
    X, Y, Z = mobius_strip(U, V, R=2.0, w=0.5)
    
    # Color by position to show the twist
    colors = cm.viridis((V - V.min()) / (V.max() - V.min()))
    
    ax.plot_surface(X, Y, Z, facecolors=colors, alpha=0.6,
                    edgecolor='gray', linewidth=0.1, shade=True)
    
    # Center cut line (red, dashed)
    u_line = np.linspace(0, 2 * np.pi, 200)
    v_center = np.zeros_like(u_line)
    xc, yc, zc = mobius_strip(u_line, v_center, R=2.0, w=0.5)
    ax.plot(xc, yc, zc, 'r-', linewidth=3, label='Corte Central (1/2)')
    
    # Off-center cut line (orange, dashed)
    v_offcenter = np.ones_like(u_line) * 0.17  # ~1/3 from edge
    xo, yo, zo = mobius_strip(u_line, v_offcenter, R=2.0, w=0.5)
    ax.plot(xo, yo, zo, 'orange', linewidth=2.5, linestyle='--', 
            label='Corte 1/3 (fora do centro)')
    
    ax.legend(loc='upper left', fontsize=8, framealpha=0.9)
    setup_3d_axis(ax, 'Fita de Möbius Original\n(com linhas de corte)')


def plot_center_cut_result(ax):
    """Plot the result of center cut: one larger strip with 2 full twists."""
    u = np.linspace(0, 4 * np.pi, 240)
    v = np.linspace(-0.2, 0.2, 15)
    U, V = np.meshgrid(u, v)
    
    X, Y, Z = center_cut_result(U, V, R=2.0, w=0.25)
    
    # Color gradient to show it's a single continuous strip
    colors = cm.plasma((U - U.min()) / (U.max() - U.min()))
    
    ax.plot_surface(X, Y, Z, facecolors=colors, alpha=0.6,
                    edgecolor='gray', linewidth=0.1, shade=True)
    
    # Trace the center line to show it's ONE strip
    u_line = np.linspace(0, 4 * np.pi, 400)
    v_zero = np.zeros_like(u_line)
    xc, yc, zc = center_cut_result(u_line, v_zero, R=2.0, w=0.25)
    ax.plot(xc, yc, zc, 'white', linewidth=1.5, alpha=0.8)
    
    setup_3d_axis(ax, 'Resultado: Corte Central\n1 fita única, 2 torções completas')


def plot_offcenter_cut_result(ax):
    """Plot the result of off-center cut: two interlocked strips."""
    
    # Strip 1: Narrow Möbius strip (non-orientable)
    u1 = np.linspace(0, 2 * np.pi, 120)
    v1 = np.linspace(-1, 1, 12)
    U1, V1 = np.meshgrid(u1, v1)
    X1, Y1, Z1 = offcenter_mobius_narrow(U1, V1, R=2.0, v_offset=0.35)
    
    ax.plot_surface(X1, Y1, Z1, alpha=0.7, color='#FF6B6B',
                    edgecolor='darkred', linewidth=0.2, shade=True)
    
    # Strip 2: Larger orientable strip (2 full twists)
    u2 = np.linspace(0, 4 * np.pi, 240)
    v2 = np.linspace(-1, 1, 12)
    U2, V2 = np.meshgrid(u2, v2)
    X2, Y2, Z2 = offcenter_large_strip(U2, V2, R=2.0, v_center=-0.1)
    
    ax.plot_surface(X2, Y2, Z2, alpha=0.5, color='#4ECDC4',
                    edgecolor='teal', linewidth=0.1, shade=True)
    
    # Legend patches
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FF6B6B', edgecolor='darkred', alpha=0.7,
              label='Möbius (não-orientável)'),
        Patch(facecolor='#4ECDC4', edgecolor='teal', alpha=0.5, 
              label='2 torções (orientável)')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8, framealpha=0.9)
    
    setup_3d_axis(ax, 'Resultado: Corte 1/3\n2 fitas entrelaçadas')


def plot_topology_comparison(ax):
    """
    Summary diagram showing the topological transformation.
    Uses a 2D schematic.
    """
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Resumo Topológico — Fita de Möbius', fontsize=14, fontweight='bold')
    
    # Section 1: Original
    ax.text(1, 7.2, 'ORIGINAL', fontsize=12, fontweight='bold', color='#2C3E50',
            ha='center')
    ax.add_patch(plt.Rectangle((0.2, 6.4), 1.6, 0.5, fill=True, 
                               facecolor='#E8D5B7', edgecolor='#2C3E50', linewidth=2))
    ax.annotate('', xy=(1.8, 6.65), xytext=(0.2, 6.65),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='red'))
    ax.text(1, 6.1, '1 lado, 1 borda\n1 meia-torção', fontsize=7, ha='center',
            color='gray')
    
    # Section 2: Center Cut
    ax.text(5, 7.2, 'CORTE CENTRAL', fontsize=12, fontweight='bold', color='#8B5CF6',
            ha='center')
    ax.add_patch(plt.Rectangle((3.5, 6.2), 3.0, 0.7, fill=True,
                               facecolor='#DDA0DD', edgecolor='#8B5CF6', linewidth=2))
    ax.text(5, 6.55, '1 FITA MAIOR', fontsize=9, fontweight='bold',
            ha='center', color='#8B5CF6')
    ax.text(5, 5.9, '2L comprimento\n4 meias-torções\nOrientável', fontsize=7,
            ha='center', color='gray')
    
    # Arrow from original to center cut
    ax.annotate('', xy=(3.4, 6.65), xytext=(2.0, 6.65),
                arrowprops=dict(arrowstyle='->', lw=2, color='#8B5CF6'))
    ax.text(2.7, 6.85, 'CUT 1/2', fontsize=8, ha='center', color='#8B5CF6')
    
    # Section 3: Off-center Cut
    ax.text(5, 4.5, 'CORTE 1/3', fontsize=12, fontweight='bold', color='#FF6B6B',
            ha='center')
    
    # Narrow Möbius
    ax.add_patch(plt.Rectangle((3.5, 3.5), 1.2, 0.5, fill=True,
                               facecolor='#FF6B6B', edgecolor='darkred', linewidth=2,
                               alpha=0.7))
    ax.text(4.1, 3.75, 'Möbius', fontsize=8, fontweight='bold',
            ha='center', color='white')
    ax.text(4.1, 3.2, 'Não-orientável\n1 meia-torção', fontsize=6, ha='center',
            color='gray')
    
    # Link symbol
    ax.text(5.0, 3.75, '<->', fontsize=14, ha='center', va='center', fontweight='bold', color='#2C3E50')
    
    # Larger strip
    ax.add_patch(plt.Rectangle((5.3, 3.4), 1.5, 0.7, fill=True,
                               facecolor='#4ECDC4', edgecolor='teal', linewidth=2,
                               alpha=0.7))
    ax.text(6.05, 3.75, '2 Torções', fontsize=8, fontweight='bold',
            ha='center', color='white')
    ax.text(6.05, 3.1, 'Orientável\n4 meias-torções', fontsize=6, ha='center',
            color='gray')
    
    # Arrow from original to off-center
    ax.annotate('', xy=(3.4, 3.75), xytext=(2.0, 6.4),
                arrowprops=dict(arrowstyle='->', lw=2, color='#FF6B6B',
                               connectionstyle='arc3,rad=0.3'))
    ax.text(2.0, 5.0, 'CUT 1/3', fontsize=8, ha='center', color='#FF6B6B')
    
    # TAMESIS Insights Box
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((0.3, 0.3), 9.4, 2.5, 
                                boxstyle='round,pad=0.15',
                                facecolor='#F8F9FA', edgecolor='#2C3E50',
                                linewidth=2))
    ax.text(5, 2.5, 'INSIGHTS TAMESIS', fontsize=11, fontweight='bold',
            ha='center', color='#2C3E50')
    
    insights = [
        '[TRI] Regime nao-orientavel aninhado dentro de regime orientavel',
        '[TDTR] O corte e irreversivel (semigrupo) - analogo a transicao de regime',
        '[Kernel v3] Transicao de fase topologica - a informacao e reorganizada',
        '[Simetria] Corte central preserva Z2; corte 1/3 quebra simetria',
        '[Linking] Fitas entrelacadas = emaranhamento topologico'
    ]
    
    for i, insight in enumerate(insights):
        ax.text(0.6, 2.1 - i * 0.38, insight, fontsize=6.5, color='#2C3E50',
                va='center')


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 70)
    print("  TAMESIS RESEARCH — Möbius Strip Cutting Simulation")
    print("=" * 70)
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # ---- Figure 1: Original Möbius with cut lines ----
    print("\n[1/4] Generating: Original Möbius strip with cut lines...")
    fig1 = plt.figure(figsize=(10, 8))
    ax1 = fig1.add_subplot(111, projection='3d')
    plot_original_with_cut_lines(ax1)
    fig1.tight_layout()
    path1 = os.path.join(output_dir, 'mobius_original.png')
    fig1.savefig(path1, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"    Saved: {path1}")
    plt.close(fig1)
    
    # ---- Figure 2: Center cut result ----
    print("[2/4] Generating: Center cut result...")
    fig2 = plt.figure(figsize=(10, 8))
    ax2 = fig2.add_subplot(111, projection='3d')
    plot_center_cut_result(ax2)
    fig2.tight_layout()
    path2 = os.path.join(output_dir, 'mobius_center_cut.png')
    fig2.savefig(path2, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"    Saved: {path2}")
    plt.close(fig2)
    
    # ---- Figure 3: Off-center cut result ----
    print("[3/4] Generating: Off-center cut result...")
    fig3 = plt.figure(figsize=(10, 8))
    ax3 = fig3.add_subplot(111, projection='3d')
    plot_offcenter_cut_result(ax3)
    fig3.tight_layout()
    path3 = os.path.join(output_dir, 'mobius_offcenter_cut.png')
    fig3.savefig(path3, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"    Saved: {path3}")
    plt.close(fig3)
    
    # ---- Figure 4: Topology Summary ----
    print("[4/4] Generating: Topology summary diagram...")
    fig4 = plt.figure(figsize=(12, 9))
    ax4 = fig4.add_subplot(111)
    plot_topology_comparison(ax4)
    fig4.tight_layout()
    path4 = os.path.join(output_dir, 'mobius_topology_summary.png')
    fig4.savefig(path4, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"    Saved: {path4}")
    plt.close(fig4)
    
    # ---- Combined Figure (2x2) ----
    print("\n[BONUS] Generating combined 2x2 figure...")
    fig_all, axes = plt.subplots(2, 2, figsize=(16, 14),
                                  subplot_kw={'projection': '3d'})
    
    # Convert to list for easier handling
    ax_list = axes.flatten()
    
    # Panel 1: Original
    plot_original_with_cut_lines(ax_list[0])
    
    # Panel 2: Center cut
    plot_center_cut_result(ax_list[1])
    
    # Panel 3: Off-center cut
    plot_offcenter_cut_result(ax_list[2])
    
    # Panel 4: Replace with a different view
    # Show the original from different angle
    u = np.linspace(0, 2 * np.pi, 120)
    v = np.linspace(-0.5, 0.5, 30)
    U, V = np.meshgrid(u, v)
    X, Y, Z = mobius_strip(U, V, R=2.0, w=0.5)
    colors = cm.coolwarm((V - V.min()) / (V.max() - V.min()))
    ax_list[3].plot_surface(X, Y, Z, facecolors=colors, alpha=0.6,
                            edgecolor='gray', linewidth=0.1)
    setup_3d_axis(ax_list[3], 'Fita de Möbius\n(vista alternativa)', elev=60, azim=135)
    
    fig_all.suptitle('TAMESIS — Topologia de Möbius: Corte e Transição de Regime',
                     fontsize=16, fontweight='bold', y=0.98)
    fig_all.tight_layout(rect=[0, 0, 1, 0.96])
    path_all = os.path.join(output_dir, 'mobius_combined.png')
    fig_all.savefig(path_all, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"    Saved: {path_all}")
    plt.close(fig_all)
    
    # ---- Print topological analysis ----
    print("\n" + "=" * 70)
    print("  TOPOLOGICAL ANALYSIS SUMMARY")
    print("=" * 70)
    print()
    print("  Original Möbius Strip:")
    print("    - Sides: 1 (non-orientable)")
    print("    - Edges: 1")
    print("    - Half-twists: 1")
    print("    - Euler Characteristic: chi = 0")
    print()
    print("  Center Cut (1/2 width) Result:")
    print("    - Number of pieces: 1 (DOES NOT SEPARATE)")
    print("    - Sides: 2 (orientable)")
    print("    - Edges: 2")  
    print("    - Half-twists: 4 (2 full twists)")
    print("    - Length: 2× original")
    print("    - Width: 1/2 original")
    print()
    print("  Off-Center Cut (1/3 width) Result:")
    print("    - Number of pieces: 2 (INTERLOCKED)")
    print("    - Piece A (narrow): Möbius strip (1 half-twist, non-orientable)")
    print("    - Piece B (wide): Strip with 4 half-twists (orientable)")
    print("    - Linking Number: |Lk| = 1")
    print("    - INSEPARABLE without cutting!")
    print()
    print("  TAMESIS Connection:")
    print("    > TRI: Non-orientable regime nested inside orientable regime")
    print("    > TDTR: Cutting is irreversible (semigroup operation)")
    print("    > Kernel v3: Topological phase transition")
    print("    > Symmetry: Center cut preserves Z2; off-center breaks it")
    print("    > Entanglement: Interlocked strips = topological linking")
    print()
    print("=" * 70)
    print("  All files saved successfully!")
    print("=" * 70)


if __name__ == '__main__':
    main()
