
import numpy as np
import matplotlib.pyplot as plt

def simulate_mercury_vortex_advanced():
    print("--- SIMULAÇÃO: VÓRTICE DE MERCÚRIO COM PERFIL GRAVITACIONAL ---")
    
    grid_size = 100
    center = grid_size // 2
    vacuum_density = np.ones((grid_size, grid_size))
    
    # Base Gravity (Earth)
    for y in range(grid_size):
        vacuum_density[y, :] += (y / grid_size) * 0.5 
    
    def apply_vortex(grid, strength):
        y, x = np.ogrid[:grid_size, :grid_size]
        dist_sq = (x - center)**2 + (y - center)**2
        shield_mask = np.exp(-dist_sq / (2 * 10**2)) # Radius 10
        
        # Laghima Effect
        grid_modified = grid - (shield_mask * strength)
        return np.clip(grid_modified, 0.0, None), shield_mask

    strengths = [0.0, 1.0, 2.0]
    
    fig, axes = plt.subplots(len(strengths), 2, figsize=(12, 10))
    
    for i, f in enumerate(strengths):
        grid_out, mask = apply_vortex(vacuum_density, f)
        
        # 1. Heatmap
        ax_map = axes[i][0]
        im = ax_map.imshow(grid_out, cmap='inferno', vmin=0, vmax=1.5)
        ax_map.set_title(f"Density Map (Rajas Strength: {f})")
        ax_map.axis('off')
        
        # 2. Gravity Profile (Cross Section at Center X)
        ax_profile = axes[i][1]
        profile = grid_out[:, center]
        ax_profile.plot(profile, color='blue', label='Local Density (Gravity)')
        ax_profile.axhline(y=1.0, color='gray', linestyle='--', label='Standard Vacuum')
        ax_profile.axhline(y=0.0, color='red', linestyle=':', label='Zero Gravity (Levitation)')
        
        # Highlight the "Bubble"
        if f > 0:
            ax_profile.fill_between(range(grid_size), profile, 1.0, 
                                    where=(profile < 1.0), color='cyan', alpha=0.3, label='Laghima Bubble')
        
        ax_profile.set_title(f"Gravity Profile (Cross Section) - Strength {f}")
        ax_profile.set_xlabel('Altitude (Y)')
        ax_profile.set_ylabel('Vacuum Density')
        ax_profile.legend(loc='upper right', fontsize='small')
        ax_profile.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\mercury_vortex_profile.png"
    plt.savefig(output_path)
    print(f"Gráfico de Perfil salvo em: {output_path}")

if __name__ == "__main__":
    simulate_mercury_vortex_advanced()
