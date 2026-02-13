"""
=============================================================================
  TAMESIS RESEARCH — Mobius Strip Cutting: Animated GIF Simulations
=============================================================================

  Generates animated GIFs demonstrating:
  1. Rotating Mobius strip with anatomy labels
  2. Center cut animation (strip separating into 1 piece with 2 twists)
  3. Off-center cut showing two interlocked strips
  4. Symmetry breaking comparison (Z2 preserved vs broken)
  5. Regime nesting (TRI insight) — orientable vs non-orientable

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-12

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ==========================================================================
# PARAMETRIC HELPERS
# ==========================================================================

def mobius_surface(u, v, R=2.0):
    """Standard Mobius strip parametrization."""
    x = (R + v * np.cos(u / 2)) * np.cos(u)
    y = (R + v * np.cos(u / 2)) * np.sin(u)
    z = v * np.sin(u / 2)
    return x, y, z


def twisted_surface(u, v, R=2.0, n_half=4):
    """Strip with n half-twists (center-cut result when n_half=4)."""
    x = (R + v * np.cos(n_half * u / 2)) * np.cos(u)
    y = (R + v * np.cos(n_half * u / 2)) * np.sin(u)
    z = v * np.sin(n_half * u / 2)
    return x, y, z


def setup_ax(ax, title="", elev=25, azim=45):
    """Standard axis configuration."""
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-1.5, 1.5)
    if title:
        ax.set_title(title, fontsize=13, fontweight='bold', pad=10)
    ax.set_xlabel('X', fontsize=8, labelpad=1)
    ax.set_ylabel('Y', fontsize=8, labelpad=1)
    ax.set_zlabel('Z', fontsize=8, labelpad=1)
    ax.view_init(elev=elev, azim=azim)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('lightgray')
    ax.yaxis.pane.set_edgecolor('lightgray')
    ax.zaxis.pane.set_edgecolor('lightgray')
    ax.tick_params(labelsize=6)


# ==========================================================================
# GIF 1: Rotating Mobius Strip with finger trace
# ==========================================================================

def generate_gif_mobius_rotation():
    """
    Rotating Mobius strip showing its single-sided, single-edge topology.
    A moving point traces the surface, demonstrating you cover both
    'sides' without lifting — proving non-orientability.
    """
    print("[GIF 1/5] Generating: Mobius strip rotation with tracer...")

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')

    # Static mesh
    u_mesh = np.linspace(0, 2 * np.pi, 80)
    v_mesh = np.linspace(-0.5, 0.5, 20)
    U, V = np.meshgrid(u_mesh, v_mesh)
    X, Y, Z = mobius_surface(U, V)

    total_frames = 120
    tracer_trail_len = 30

    status_text = ax.text2D(0.03, 0.93, "", transform=ax.transAxes,
                            fontsize=10, fontweight='bold',
                            bbox=dict(boxstyle='round,pad=0.3',
                                      facecolor='lightyellow', alpha=0.9))

    def update(frame):
        ax.cla()
        setup_ax(ax, 'Fita de Mobius: 1 Lado, 1 Borda')

        # Rotate view
        azim = 30 + frame * 3
        ax.view_init(elev=25, azim=azim)

        # Color based on v-parameter position
        colors = cm.viridis((V - V.min()) / (V.max() - V.min()))
        ax.plot_surface(X, Y, Z, facecolors=colors, alpha=0.5,
                        edgecolor='gray', linewidth=0.05)

        # Tracer point — traverses the center line
        # Goes from 0 to 4pi (two full loops = 720 degrees)
        theta = frame * (4 * np.pi / total_frames)
        u_t = theta % (2 * np.pi)

        # Position on center of strip (v=0)
        px = 2 * np.cos(u_t)
        py = 2 * np.sin(u_t)
        pz = 0.0

        # Normal vector (shows which "side" we're on)
        alpha = theta / 2.0
        nx = np.cos(u_t) * np.sin(alpha)
        ny = np.sin(u_t) * np.sin(alpha)
        nz = np.cos(alpha)
        scale = 0.6

        # Draw tracer point
        ax.scatter([px], [py], [pz], color='red', s=80, zorder=10)

        # Draw normal vector
        ax.plot([px, px + nx * scale],
                [py, py + ny * scale],
                [pz, pz + nz * scale],
                'r-', linewidth=3, zorder=10)

        # Trail
        trail_thetas = np.linspace(max(0, theta - 2), theta, tracer_trail_len)
        trail_x = 2 * np.cos(trail_thetas % (2 * np.pi))
        trail_y = 2 * np.sin(trail_thetas % (2 * np.pi))
        trail_z = np.zeros_like(trail_thetas)
        ax.plot(trail_x, trail_y, trail_z, 'r-', linewidth=1.5, alpha=0.4)

        deg = np.degrees(theta)
        loop_num = int(deg // 360) + 1
        if deg <= 360:
            state = "Loop 1: Cobrindo o 'lado A'"
        else:
            state = "Loop 2: Cobrindo o 'lado B' (mesmo lado!)"

        ax.text2D(0.03, 0.93,
                  f"Angulo: {deg:.0f} / 720\nLoop {loop_num} | {state}",
                  transform=ax.transAxes, fontsize=9, fontweight='bold',
                  bbox=dict(boxstyle='round,pad=0.3',
                            facecolor='lightyellow', alpha=0.9))

        return []

    ani = animation.FuncAnimation(fig, update, frames=total_frames, blit=False)
    path = os.path.join(OUTPUT_DIR, 'mobius_rotation.gif')
    ani.save(path, writer='pillow', fps=20)
    plt.close(fig)
    print(f"    Saved: {path}")


# ==========================================================================
# GIF 2: Center Cut Animation
# ==========================================================================

def generate_gif_center_cut():
    """
    Animates the center cut: shows the Mobius strip 'opening up' into
    a single longer strip with 2 full twists.
    Phase 1: Show original with cut line
    Phase 2: Transition to the result
    """
    print("[GIF 2/5] Generating: Center cut animation...")

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')

    total_frames = 100

    def update(frame):
        ax.cla()
        setup_ax(ax, '', elev=25, azim=45)
        ax.view_init(elev=25, azim=30 + frame * 1.5)

        t = frame / total_frames  # 0 to 1

        if t < 0.4:
            # Phase 1: Show original Mobius with cut line
            phase_t = t / 0.4
            ax.set_title('Corte Central: Antes', fontsize=13, fontweight='bold')

            u = np.linspace(0, 2 * np.pi, 80)
            v = np.linspace(-0.5, 0.5, 20)
            U, V = np.meshgrid(u, v)
            X, Y, Z = mobius_surface(U, V)
            colors = cm.viridis((V - V.min()) / (V.max() - V.min()))
            ax.plot_surface(X, Y, Z, facecolors=colors, alpha=0.5,
                            edgecolor='gray', linewidth=0.05)

            # Animated cut line growing
            u_cut = np.linspace(0, 2 * np.pi * phase_t, 100)
            x_cut = 2 * np.cos(u_cut)
            y_cut = 2 * np.sin(u_cut)
            z_cut = np.zeros_like(u_cut)
            ax.plot(x_cut, y_cut, z_cut, 'r-', linewidth=3)

            # Scissors indicator
            if len(u_cut) > 0:
                ax.scatter([x_cut[-1]], [y_cut[-1]], [z_cut[-1]],
                           color='red', s=120, marker='x', linewidths=3)

            ax.text2D(0.03, 0.93,
                      f"Cortando... {phase_t * 100:.0f}%",
                      transform=ax.transAxes, fontsize=10, fontweight='bold',
                      bbox=dict(boxstyle='round,pad=0.3',
                                facecolor='#FFE0E0', alpha=0.9))

        elif t < 0.5:
            # Phase 2: Flash / transition
            ax.set_title('CORTADO!', fontsize=16, fontweight='bold', color='red')
            ax.text2D(0.5, 0.5, "1 peca!\nNAO separou!",
                      transform=ax.transAxes, fontsize=18, fontweight='bold',
                      ha='center', va='center', color='red',
                      bbox=dict(boxstyle='round,pad=0.5',
                                facecolor='lightyellow', alpha=0.95))

        else:
            # Phase 3: Show result — single strip with 2 full twists
            phase_t = (t - 0.5) / 0.5
            ax.set_title('Resultado: 1 Fita com 2 Torcoes Completas',
                          fontsize=12, fontweight='bold')

            u = np.linspace(0, 4 * np.pi, 200)
            v = np.linspace(-0.22, 0.22, 12)
            U, V = np.meshgrid(u, v)

            X = (2 + V * np.cos(U)) * np.cos(U)
            Y = (2 + V * np.cos(U)) * np.sin(U)
            Z = V * np.sin(U)

            colors = cm.plasma((U - U.min()) / (U.max() - U.min()))
            ax.plot_surface(X, Y, Z, facecolors=colors, alpha=0.6,
                            edgecolor='gray', linewidth=0.05)

            # Trace center line
            u_line = np.linspace(0, 4 * np.pi, 300)
            x_l = 2 * np.cos(u_line)
            y_l = 2 * np.sin(u_line)
            z_l = np.zeros_like(u_line)
            ax.plot(x_l, y_l, z_l, 'white', linewidth=1, alpha=0.6)

            ax.text2D(0.03, 0.93,
                      "Comprimento: 2x original\n"
                      "Largura: 1/2 original\n"
                      "Torcoes: 4 meias-torcoes\n"
                      "Orientavel: SIM",
                      transform=ax.transAxes, fontsize=8, fontweight='bold',
                      bbox=dict(boxstyle='round,pad=0.3',
                                facecolor='#E8D5FF', alpha=0.9))

        return []

    ani = animation.FuncAnimation(fig, update, frames=total_frames, blit=False)
    path = os.path.join(OUTPUT_DIR, 'mobius_center_cut.gif')
    ani.save(path, writer='pillow', fps=20)
    plt.close(fig)
    print(f"    Saved: {path}")


# ==========================================================================
# GIF 3: Off-center Cut — Two Interlocked Strips
# ==========================================================================

def generate_gif_offcenter_cut():
    """
    Animates the off-center (1/3) cut showing emergence of 
    two topologically interlocked strips.
    """
    print("[GIF 3/5] Generating: Off-center cut animation...")

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')

    total_frames = 100

    def update(frame):
        ax.cla()
        setup_ax(ax, '', elev=25, azim=45)
        ax.view_init(elev=25, azim=30 + frame * 2)

        t = frame / total_frames

        if t < 0.35:
            # Phase 1: Show original with off-center cut line
            phase_t = t / 0.35
            ax.set_title('Corte 1/3: Fora do Centro', fontsize=13, fontweight='bold')

            u = np.linspace(0, 2 * np.pi, 80)
            v = np.linspace(-0.5, 0.5, 20)
            U, V = np.meshgrid(u, v)
            X, Y, Z = mobius_surface(U, V)
            colors = cm.viridis((V - V.min()) / (V.max() - V.min()))
            ax.plot_surface(X, Y, Z, facecolors=colors, alpha=0.5,
                            edgecolor='gray', linewidth=0.05)

            # Off-center cut line
            u_cut = np.linspace(0, 2 * np.pi * phase_t, 100)
            v_off = 0.17 * np.ones_like(u_cut)
            x_c, y_c, z_c = mobius_surface(u_cut, v_off)
            ax.plot(x_c, y_c, z_c, color='orange', linewidth=3, linestyle='--')

            if len(u_cut) > 0:
                ax.scatter([x_c[-1]], [y_c[-1]], [z_c[-1]],
                           color='orange', s=120, marker='x', linewidths=3)

            ax.text2D(0.03, 0.93,
                      f"Cortando a 1/3... {phase_t * 100:.0f}%",
                      transform=ax.transAxes, fontsize=10, fontweight='bold',
                      bbox=dict(boxstyle='round,pad=0.3',
                                facecolor='#FFF0E0', alpha=0.9))

        elif t < 0.45:
            # Transition
            ax.set_title('CORTADO!', fontsize=16, fontweight='bold', color='darkorange')
            ax.text2D(0.5, 0.5, "2 pecas!\nENTRELACADAS!",
                      transform=ax.transAxes, fontsize=18, fontweight='bold',
                      ha='center', va='center', color='darkorange',
                      bbox=dict(boxstyle='round,pad=0.5',
                                facecolor='lightyellow', alpha=0.95))

        else:
            # Phase 2: Show two interlocked strips
            phase_t = (t - 0.45) / 0.55
            ax.set_title('Resultado: 2 Fitas Entrelacadas',
                          fontsize=12, fontweight='bold')

            # Strip 1: Narrow Mobius (non-orientable) — red
            u1 = np.linspace(0, 2 * np.pi, 80)
            v1 = np.linspace(-1, 1, 10)
            U1, V1 = np.meshgrid(u1, v1)
            v_actual = 0.35 + V1 * 0.12
            X1 = (2 + v_actual * np.cos(U1 / 2)) * np.cos(U1)
            Y1 = (2 + v_actual * np.cos(U1 / 2)) * np.sin(U1)
            Z1 = v_actual * np.sin(U1 / 2)
            ax.plot_surface(X1, Y1, Z1, alpha=0.7, color='#FF6B6B',
                            edgecolor='darkred', linewidth=0.15)

            # Strip 2: Larger orientable strip — teal
            u2 = np.linspace(0, 4 * np.pi, 200)
            v2 = np.linspace(-1, 1, 10)
            U2, V2 = np.meshgrid(u2, v2)
            v_act2 = -0.1 + V2 * 0.15
            X2 = (2 + v_act2 * np.cos(U2)) * np.cos(U2)
            Y2 = (2 + v_act2 * np.cos(U2)) * np.sin(U2)
            Z2 = v_act2 * np.sin(U2)
            ax.plot_surface(X2, Y2, Z2, alpha=0.45, color='#4ECDC4',
                            edgecolor='teal', linewidth=0.08)

            # Legend
            from matplotlib.patches import Patch
            ax.legend(handles=[
                Patch(facecolor='#FF6B6B', label='Mobius (nao-orientavel)'),
                Patch(facecolor='#4ECDC4', label='2 torcoes (orientavel)')
            ], loc='upper left', fontsize=7, framealpha=0.9)

            ax.text2D(0.03, 0.93,
                      "Estreita: Mobius (1 meia-torcao)\n"
                      "Larga: 2 torcoes completas\n"
                      "Linking Number: |Lk| = 1\n"
                      "INSEPARAVEIS!",
                      transform=ax.transAxes, fontsize=8, fontweight='bold',
                      bbox=dict(boxstyle='round,pad=0.3',
                                facecolor='#E0FFF5', alpha=0.9))

        return []

    ani = animation.FuncAnimation(fig, update, frames=total_frames, blit=False)
    path = os.path.join(OUTPUT_DIR, 'mobius_offcenter_cut.gif')
    ani.save(path, writer='pillow', fps=20)
    plt.close(fig)
    print(f"    Saved: {path}")


# ==========================================================================
# GIF 4: Symmetry Breaking Comparison
# ==========================================================================

def generate_gif_symmetry():
    """
    Side-by-side comparison showing Z2 symmetry preservation (center cut)
    vs symmetry breaking (off-center cut).
    """
    print("[GIF 4/5] Generating: Symmetry breaking comparison...")

    fig = plt.figure(figsize=(14, 6))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')
    ax1.set_facecolor('white')
    ax2.set_facecolor('white')

    total_frames = 80

    def update(frame):
        ax1.cla()
        ax2.cla()

        azim = 30 + frame * 3
        setup_ax(ax1, 'Corte Central: Simetria Z2 PRESERVADA', elev=25, azim=azim)
        setup_ax(ax2, 'Corte 1/3: Simetria Z2 QUEBRADA', elev=25, azim=azim)

        # Left: Center cut result (single strip, 2 twists)
        u = np.linspace(0, 4 * np.pi, 160)
        v = np.linspace(-0.22, 0.22, 10)
        U, V = np.meshgrid(u, v)
        X = (2 + V * np.cos(U)) * np.cos(U)
        Y = (2 + V * np.cos(U)) * np.sin(U)
        Z = V * np.sin(U)
        colors = cm.plasma((U - U.min()) / (U.max() - U.min()))
        ax1.plot_surface(X, Y, Z, facecolors=colors, alpha=0.6,
                         edgecolor='gray', linewidth=0.05)

        ax1.text2D(0.05, 0.9, "1 peca\nSimetrica",
                   transform=ax1.transAxes, fontsize=9, fontweight='bold',
                   color='#8B5CF6',
                   bbox=dict(boxstyle='round,pad=0.3',
                             facecolor='#F0E0FF', alpha=0.9))

        # Right: Off-center result (two strips)
        # Narrow Mobius
        u1 = np.linspace(0, 2 * np.pi, 60)
        v1 = np.linspace(-1, 1, 8)
        U1, V1 = np.meshgrid(u1, v1)
        va = 0.35 + V1 * 0.12
        X1 = (2 + va * np.cos(U1 / 2)) * np.cos(U1)
        Y1 = (2 + va * np.cos(U1 / 2)) * np.sin(U1)
        Z1 = va * np.sin(U1 / 2)
        ax2.plot_surface(X1, Y1, Z1, alpha=0.7, color='#FF6B6B',
                         edgecolor='darkred', linewidth=0.15)

        # Larger strip
        u2 = np.linspace(0, 4 * np.pi, 160)
        v2 = np.linspace(-1, 1, 8)
        U2, V2 = np.meshgrid(u2, v2)
        va2 = -0.1 + V2 * 0.15
        X2 = (2 + va2 * np.cos(U2)) * np.cos(U2)
        Y2 = (2 + va2 * np.cos(U2)) * np.sin(U2)
        Z2 = va2 * np.sin(U2)
        ax2.plot_surface(X2, Y2, Z2, alpha=0.45, color='#4ECDC4',
                         edgecolor='teal', linewidth=0.08)

        ax2.text2D(0.05, 0.9, "2 pecas\nAssimetricas",
                   transform=ax2.transAxes, fontsize=9, fontweight='bold',
                   color='#FF6B6B',
                   bbox=dict(boxstyle='round,pad=0.3',
                             facecolor='#FFE0E0', alpha=0.9))

        return []

    ani = animation.FuncAnimation(fig, update, frames=total_frames, blit=False)
    path = os.path.join(OUTPUT_DIR, 'mobius_symmetry.gif')
    ani.save(path, writer='pillow', fps=15)
    plt.close(fig)
    print(f"    Saved: {path}")


# ==========================================================================
# GIF 5: Regime Nesting (TRI) — Orientable inside Non-Orientable
# ==========================================================================

def generate_gif_regime_nesting():
    """
    Highlights the TRI insight: non-orientable regime (Mobius) 
    nested inside orientable regime (2-twist strip), rotating to 
    show the interlocking from all angles.
    """
    print("[GIF 5/5] Generating: TRI regime nesting...")

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')

    total_frames = 100

    def update(frame):
        ax.cla()
        setup_ax(ax, 'TRI: Regimes Aninhados', elev=20, azim=45)

        azim = frame * 3.6
        elev = 20 + 15 * np.sin(frame * np.pi / total_frames)
        ax.view_init(elev=elev, azim=azim)

        # Regime 1: Non-orientable (Quantum) — Mobius, red
        u1 = np.linspace(0, 2 * np.pi, 80)
        v1 = np.linspace(-1, 1, 12)
        U1, V1 = np.meshgrid(u1, v1)
        va = 0.35 + V1 * 0.13
        X1 = (2 + va * np.cos(U1 / 2)) * np.cos(U1)
        Y1 = (2 + va * np.cos(U1 / 2)) * np.sin(U1)
        Z1 = va * np.sin(U1 / 2)

        # Pulse effect
        pulse = 0.7 + 0.3 * np.sin(frame * 2 * np.pi / 30)
        ax.plot_surface(X1, Y1, Z1, alpha=pulse * 0.8, color='#FF6B6B',
                        edgecolor='darkred', linewidth=0.2)

        # Regime 2: Orientable (Classical) — 2 twists, teal
        u2 = np.linspace(0, 4 * np.pi, 200)
        v2 = np.linspace(-1, 1, 12)
        U2, V2 = np.meshgrid(u2, v2)
        va2 = -0.1 + V2 * 0.17
        X2 = (2 + va2 * np.cos(U2)) * np.cos(U2)
        Y2 = (2 + va2 * np.cos(U2)) * np.sin(U2)
        Z2 = va2 * np.sin(U2)
        ax.plot_surface(X2, Y2, Z2, alpha=0.35, color='#4ECDC4',
                        edgecolor='teal', linewidth=0.08)

        # Labels
        ax.text2D(0.03, 0.93,
                  "REGIME QUANTICO\n"
                  "Nao-orientavel (Mobius)\n"
                  "Spin 1/2, fermions",
                  transform=ax.transAxes, fontsize=8, fontweight='bold',
                  color='darkred',
                  bbox=dict(boxstyle='round,pad=0.3',
                            facecolor='#FFE0E0', alpha=0.9))

        ax.text2D(0.03, 0.05,
                  "REGIME CLASSICO\n"
                  "Orientavel (2 torcoes)\n"
                  "Spin inteiro, bosons",
                  transform=ax.transAxes, fontsize=8, fontweight='bold',
                  color='teal',
                  bbox=dict(boxstyle='round,pad=0.3',
                            facecolor='#E0FFF5', alpha=0.9))

        ax.text2D(0.65, 0.5,
                  "INSEPARAVEIS\n|Lk| = 1",
                  transform=ax.transAxes, fontsize=10, fontweight='bold',
                  ha='center', color='#2C3E50',
                  bbox=dict(boxstyle='round,pad=0.4',
                            facecolor='lightyellow', alpha=0.9))

        return []

    ani = animation.FuncAnimation(fig, update, frames=total_frames, blit=False)
    path = os.path.join(OUTPUT_DIR, 'mobius_regime_nesting.gif')
    ani.save(path, writer='pillow', fps=20)
    plt.close(fig)
    print(f"    Saved: {path}")


# ==========================================================================
# MAIN
# ==========================================================================

def main():
    print("=" * 60)
    print("  TAMESIS — Mobius Topology GIF Generator")
    print("=" * 60)
    print()

    generate_gif_mobius_rotation()
    generate_gif_center_cut()
    generate_gif_offcenter_cut()
    generate_gif_symmetry()
    generate_gif_regime_nesting()

    print()
    print("=" * 60)
    print("  All GIFs generated successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()
