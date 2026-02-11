
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def simulate_mercury_vortex():
    print("--- INICIANDO SIMULAÇÃO DE VÓRTICE DE MERCÚRIO (MHD VIMANA) ---")
    
    # 1. O VÁCUO (Grid de Nós Entrópicos)
    # Representa a densidade do espaço-tempo. 1.0 = Vácuo Padrão.
    grid_size = 50
    vacuum_density = np.ones((grid_size, grid_size))
    
    # 2. A GRAVIDADE (Gradiente de Densidade)
    # A Terra cria um poço de alta densidade no fundo (y crescendo)
    for y in range(grid_size):
        # Gradiente linear simulando campo gravitacional planetário
        vacuum_density[y, :] += (y / grid_size) * 0.5  
    
    # 3. O VIMANA (O Agente de Rajas)
    vimana_pos = (grid_size // 2, grid_size // 2)
    
    def apply_mercury_vortex(density_grid, pos, strength):
        """
        Simula o efeito do Motor de Mercúrio.
        A injeção de energia (vórtice/Rajas) 'evapora' a densidade local (quebra conexões).
        Converte Tamas (Densidade) em Sattva (Espaço Diluído).
        """
        y, x = np.ogrid[:grid_size, :grid_size]
        dist_sq = (x - pos[1])**2 + (y - pos[0])**2
        
        # O Vórtice cria uma bolha de BAIXA densidade (entropia máxima local)
        # Fator de blindagem: quanto maior a força, menor a densidade efetiva
        shield_radius = 5.0
        # Gaussian distribution for the vortex effect
        shield_mask = np.exp(-dist_sq / (2 * shield_radius**2))
        
        # APLICANDO LAGHIMA: Reduz a densidade local inversamente à força
        # Strength = Rajas input
        current_grid = density_grid.copy()
        current_grid -= shield_mask * strength
        
        # Clip para evitar densidade negativa (buracos na realidade, vacuum decay)
        # Mantemos 0.1 como "éter residual"
        return np.clip(current_grid, 0.1, None)
    
    # 4. LOOP DE SIMULAÇÃO
    forces = [0.0, 0.5, 1.0, 2.0] # Níveis de potência do motor (Rajas)
    
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    
    print("Simulando níveis de potência...")
    
    for i, f in enumerate(forces):
        current_grid = apply_mercury_vortex(vacuum_density, vimana_pos, f)
        
        # ANÁLISE: Calcular o Gradiente Local no centro (Gravidade Efetiva)
        # Gradiente positivo = Gravidade puxando para baixo
        # Gradiente zero = Flutuação
        # Gradiente negativo (invertido) = Propulsão
        grad_y, grad_x = np.gradient(current_grid)
        
        # A gravidade local é o gradiente em Y no ponto do Vimana
        local_gravity = grad_y[vimana_pos[0], vimana_pos[1]]
        
        print(f"  > Vortex Strength {f}: Gravidade Local Efetiva = {local_gravity:.4f}")
        if local_gravity <= 0.001 and local_gravity >= -0.001:
             print("    [STATUS: FLUTUAÇÃO/LEVITAÇÃO ALCANÇADA]")
        elif local_gravity < -0.001:
             print("    [STATUS: PROPULSÃO ANTIGRAVITACIONAL]")

        
        # Visualização
        im = axes[i].imshow(current_grid, cmap='inferno', vmin=0, vmax=1.5)
        axes[i].set_title(f"Vortex Strength (Rajas): {f}\nEffective Gravity: {local_gravity:.3f}")
        axes[i].axis('off')
        
        # Mark Vimana position
        axes[i].plot(vimana_pos[1], vimana_pos[0], 'cx', markersize=10, markeredgewidth=2)
    
    plt.suptitle("Vimanika Shastra Simulation: Mercury Vortex Density Reduction (Laghima Effect)", fontsize=16)
    plt.tight_layout()
    
    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\mercury_vortex_mhd.png"
    plt.savefig(output_path)
    print(f"Gráfico salvo em: {output_path}")

if __name__ == "__main__":
    simulate_mercury_vortex()
