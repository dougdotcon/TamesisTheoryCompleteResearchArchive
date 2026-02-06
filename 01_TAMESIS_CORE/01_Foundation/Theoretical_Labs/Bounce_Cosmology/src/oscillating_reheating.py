import numpy as np
import matplotlib.pyplot as plt
from src.physics_models.relativity import CamposEscalarAcoplados

def run_oscillating_reheating():
    """
    Demonstrate Reheating by starting with an OSCILLATING inflaton.
    This skips the slow-roll phase and goes directly to the coherent oscillations
    that drive particle production.
    """
    print("=== OSCILLATING INFLATON REHEATING DEMO ===")
    print("Initial Conditions: Post-Inflation (Field oscillating at minimum)\n")
    
    # Physics Setup
    xi = 1.0  # Low coupling for computational speed
    gamma = 0.05  # Decay rate
    
    # Post-Inflation Initial Conditions
    # - Scale factor already expanded (a >> 1)
    # - Field near minimum of potential (phi ~ 0)
    # - Field has kinetic energy (oscillating)
    condicoes = {
        'a_inicial': 100.0,  # Post-inflation universe
        'H_inicial': 0.01,   # Hubble rate decreasing
        'phi_inicial': 0.3,  # Near minimum (V = 0.5 * m^2 * phi^2)
        'pi_phi_inicial': 0.0,  # Will be converted to v_phi
        'rho_r_inicial': 0.0,   # Cold start
    }
    
    # Give the field initial velocity to start oscillations
    # This simulates the field rolling down and bouncing
    v_phi_initial = 0.1  # Oscillating amplitude
    
   # Manually override to inject velocity
    # (pi_phi would be a^3 * v_phi, but we convert in the code)
    
    print(f"Parameters:")
    print(f"  Xi (coupling)    = {xi}")
    print(f"  Gamma (decay)    = {gamma}")
    print(f"  phi_initial      = {condicoes['phi_inicial']}")
    print(f"  v_phi_initial    = {v_phi_initial}")
    print(f"  a_initial        = {condicoes['a_inicial']}\n")
    
    # Override pi_phi to inject velocity
    condicoes['pi_phi_inicial'] = v_phi_initial * condicoes['a_inicial']**3
    
    # Model
    modelo = CamposEscalarAcoplados(xi=xi, gamma=gamma)
    
    # Run Simulation
    # Short time span since oscillations are fast
    t_span = (0.0, 1000.0)
    print(f"Running simulation for t={t_span}...\n")
    
    evol = modelo.evolucao_campo_bounce(t_span=t_span, n_pontos=5000, initial_conditions=condicoes)
    
    if not evol['sucesso']:
        print(f"❌ Failed: {evol.get('mensagem', 'Unknown')}")
        return
    
    # Extract Results
    t = evol['t']
    phi = evol['phi']
    v_phi = evol['v_phi']
    rho_r = evol['rho_r']
    rho_phi = evol['rho_phi']
    a = evol['a']
    
    # Analysis
    idx_cross = np.where(rho_r > rho_phi)[0]
    
    print("=" * 50)
    if len(idx_cross) > 0:
        t_reheat = t[idx_cross[0]]
        print(f"✅ REHEATING SUCCESSFUL!")
        print(f"   Radiation dominates at t = {t_reheat:.2f}")
        T_reheat_planck = (rho_r[idx_cross[0]])**0.25
        print(f"   Reheating Temperature ~ {T_reheat_planck:.2e} (Planck units)")
    else:
        print(f"⚠️  Radiation growing but not yet dominant")
        ratio_final = rho_r[-1] / (rho_phi[-1] + 1e-50)
        print(f"   Final ratio rho_r/rho_phi = {ratio_final:.4f}")
    
    print(f"\nFinal State (t={t[-1]:.1f}):")
    print(f"  Field phi        = {phi[-1]:.4e}")
    print(f"  Radiation rho_r  = {rho_r[-1]:.4e}")
    print(f"  Inflaton rho_phi = {rho_phi[-1]:.4e}")
    print(f"  Scale factor a   = {a[-1]:.4e}")
    
    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Subplot 1: Field Oscillations
    axes[0, 0].plot(t, phi, color='purple', linewidth=1.5)
    axes[0, 0].set_xlabel('Time')
    axes[0, 0].set_ylabel(r'$\phi$ (Inflaton Field)')
    axes[0, 0].set_title('Inflaton Oscillations')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Subplot 2: Energy Densities
    axes[0, 1].semilogy(t, rho_phi, label=r'$\rho_\phi$ (Field)', linewidth=2)
    axes[0, 1].semilogy(t, rho_r, label=r'$\rho_r$ (Radiation)', linewidth=2, linestyle='--')
    if len(idx_cross) > 0:
        axes[0, 1].axvline(t_reheat, color='green', linestyle=':', label='Reheating')
    axes[0, 1].set_xlabel('Time')
    axes[0, 1].set_ylabel('Energy Density')
    axes[0, 1].set_title('Energy Transfer (Decay)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, which='both', alpha=0.3)
    
    # Subplot 3: Velocity (shows damping)
    axes[1, 0].plot(t, v_phi, color='red', linewidth=1)
    axes[1, 0].set_xlabel('Time')
    axes[1, 0].set_ylabel(r'$\dot{\phi}$ (Field Velocity)')
    axes[1, 0].set_title('Oscillation Damping')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Subplot 4: Ratio
    ratio = rho_r / (rho_phi + 1e-50)
    axes[1, 1].plot(t, ratio, color='orange', linewidth=2)
    axes[1, 1].axhline(1.0, color='black', linestyle='--', label='Equipartition')
    axes[1, 1].set_xlabel('Time')
    axes[1, 1].set_ylabel(r'$\rho_r / \rho_\phi$')
    axes[1, 1].set_title('Radiation Fraction')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('oscillating_reheating.png', dpi=150)
    print(f"\n📊 Plot saved: oscillating_reheating.png")

if __name__ == "__main__":
    run_oscillating_reheating()
