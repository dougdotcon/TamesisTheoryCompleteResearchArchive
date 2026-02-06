import numpy as np
import matplotlib.pyplot as plt
from src.physics_models.black_hole_universe import UniversosBuracoNegro
from src.physics_models.relativity import CamposEscalarAcoplados

def run_reheating_demo():
    print("=== REHEATING PHYSICS DEMO (Low Xi for Speed) ===")
    
    # 1. Physics Parameters
    # Use Xi=1.0 to ensure inflation ends quickly and we can see Reheating
    xi = 1.0 
    gamma = 0.1 # High decay for visibility
    M_parent = 5e22
    
    print(f"Parameters: Xi={xi}, Gamma={gamma}")
    
    # 2. Initial Conditions
    bhu = UniversosBuracoNegro(M_parent)
    condicoes = bhu.gerar_condicoes_iniciais_rebote()
    
    condicoes['a_inicial'] = 1.0 
    condicoes['pi_phi_inicial'] = 0.0
    condicoes['phi_inicial'] = 1.5 # Start higher to get some inflation
    condicoes['rho_r_inicial'] = 0.0 
    
    # 3. Model Setup
    modelo = CamposEscalarAcoplados(xi=xi, gamma=gamma)
    
    # 4. Run Simulation
    # Inflation should end around t=500 for Xi=1
    # Reheating follows.
    t_span = (0.0, 2000.0)
    print(f"Running simulation for t={t_span}...")
    
    evol = modelo.evolucao_campo_bounce(t_span=t_span, n_pontos=2000, initial_conditions=condicoes)
    
    if not evol['sucesso']:
        print(f"❌ Simulation Failed: {evol.get('mensagem', 'Unknown error')}")
        return
        
    # 5. Analysis
    t = evol['t']
    rho_r = evol['rho_r']
    rho_phi = evol['rho_phi']
    a = evol['a']
    H = evol['H']
    
    # Find crossover point
    idx_cross = np.where(rho_r > rho_phi)[0]
    if len(idx_cross) > 0:
        t_cross = t[idx_cross[0]]
        print(f"✅ RADIATION DOMINATION ACHIEVED at t = {t_cross:.1f}")
    else:
        print("⚠️ No crossover detected yet.")

    final_rho_r = rho_r[-1]
    final_rho_phi = rho_phi[-1]
    
    print(f"Final State (t={t[-1]:.1f}):")
    print(f"  Scale Factor a = {a[-1]:.4e}")
    print(f"  Radio rho_r    = {final_rho_r:.4e}")
    print(f"  Field rho_phi  = {final_rho_phi:.4e}")
    
    # 6. Save Plot
    try:
        plt.figure(figsize=(10, 6))
        plt.semilogy(t, rho_phi, label=r'$\rho_\phi$ (Inflaton)', color='blue', linewidth=2)
        plt.semilogy(t, rho_r, label=r'$\rho_r$ (Radiation)', color='orange', linewidth=2, linestyle='--')
        
        if len(idx_cross) > 0:
            plt.axvline(x=t_cross, color='green', linestyle=':', label='Reheating Complete')
            
        plt.xlabel('Time (Planck units)')
        plt.ylabel('Energy Density')
        plt.title(f'Reheating Demonstration ($\Gamma={gamma}, \\xi={xi}$)')
        plt.legend()
        plt.grid(True, which="both", ls="-", alpha=0.2)
        plt.savefig('reheating_demo.png')
        print("Plot saved to reheating_demo.png")
    except Exception as e:
        print(f"Could not save plot: {e}")

if __name__ == "__main__":
    run_reheating_demo()
