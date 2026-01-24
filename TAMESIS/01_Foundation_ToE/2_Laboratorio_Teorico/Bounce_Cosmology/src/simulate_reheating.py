import numpy as np
import matplotlib.pyplot as plt
from src.physics_models.black_hole_universe import UniversosBuracoNegro
from src.physics_models.relativity import CamposEscalarAcoplados

def run_reheating_simulation():
    print("=== SIMULATION PHASE 4: REHEATING ===")
    
    # 1. Physics Parameters
    xi = 100.0
    gamma = 2e-3 # Decay rate (tunable)
    M_parent = 5e22
    
    print(f"Parameters: Xi={xi}, Gamma={gamma}")
    
    # 2. Initial Conditions
    bhu = UniversosBuracoNegro(M_parent)
    condicoes = bhu.gerar_condicoes_iniciais_rebote()
    
    # Normalize for simulation stability
    condicoes['a_inicial'] = 1.0 
    condicoes['pi_phi_inicial'] = 0.0
    condicoes['phi_inicial'] = 1.0 # Starting on the slope
    condicoes['rho_r_inicial'] = 0.0 # Cold universe initially
    
    # 3. Model Setup
    modelo = CamposEscalarAcoplados(xi=xi, gamma=gamma)
    
    # Time span: Inflation + Reheating
    # Needs to be long enough for the field to roll down the plateau
    t_span = (0.0, 50000.0)
    print(f"Running simulation for t={t_span}...")
    
    evol = modelo.evolucao_campo_bounce(t_span=t_span, n_pontos=5000, initial_conditions=condicoes)
    
    if not evol['sucesso']:
        print(f"❌ Simulation Failed: {evol.get('mensagem', 'Unknown error')}")
        return
        
    # 5. Analysis
    t = evol['t']
    rho_r = evol['rho_r']
    rho_phi = evol['rho_phi']
    a = evol['a']
    H = evol['H']
    
    # Check dominance
    final_rho_r = rho_r[-1]
    final_rho_phi = rho_phi[-1]
    ratio = final_rho_r / (final_rho_phi + 1e-30)
    
    print(f"Final State (t={t[-1]:.1f}):")
    print(f"  Scale Factor a = {a[-1]:.4e}")
    print(f"  Radio rho_r    = {final_rho_r:.4e}")
    print(f"  Field rho_phi  = {final_rho_phi:.4e}")
    print(f"  Ratio (r/phi)  = {ratio:.4f}")
    
    if ratio > 1.0:
        print("✅ REHEATING SUCCESSFUL: Radiation dominates!")
    else:
        print("⚠️ REHEATING INCOMPLETE: Scalar field still dominates.")
        
    # 6. Save Plot
    try:
        plt.figure(figsize=(10, 6))
        plt.semilogy(t, rho_phi, label=r'$\rho_\phi$ (Inflaton)', color='blue')
        plt.semilogy(t, rho_r, label=r'$\rho_r$ (Radiation)', color='red')
        plt.axhline(y=final_rho_r, color='gray', linestyle='--', alpha=0.5)
        plt.xlabel('Time (Planck units)')
        plt.ylabel('Energy Density')
        plt.title(f'Reheating Dynamics ($\Gamma={gamma}, \\xi={xi}$)')
        plt.legend()
        plt.grid(True, which="both", ls="-", alpha=0.2)
        plt.savefig('reheating_simulation.png')
        print("Plot saved to reheating_simulation.png")
    except Exception as e:
        print(f"Could not save plot: {e}")

if __name__ == "__main__":
    run_reheating_simulation()
