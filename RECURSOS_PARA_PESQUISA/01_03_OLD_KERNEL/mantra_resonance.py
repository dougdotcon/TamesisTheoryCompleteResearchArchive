
import numpy as np
import matplotlib.pyplot as plt

def simulate_chladni_patterns():
    """
    Simula Padrões de Chladni (Cymatics) como prova de conceito da Interface Mantra-Yantra.
    
    Tamesis Theory Interpretation:
    - Input: Mantra (Frequência/Vibração)
    - Medium: Mercúrio ou Cristal (Placa Vibratória)
    - Output: Yantra (Geometria Sagrada / Circuito)
    
    Demonstra que o SOM pode programar a MATÉRIA.
    """
    
    print("--- INICIANDO SIMULAÇÃO DE RESSONÂNCIA BIO-ACÚSTICA (MANTRA -> YANTRA) ---")
    
    # Grid resolution
    N = 200
    x = np.linspace(0, 1, N)
    y = np.linspace(0, 1, N)
    X, Y = np.meshgrid(x, y)
    
    # Chladni Plate Equation for a constrained square plate
    # A * cos(n*pi*x)*cos(m*pi*y) - B * cos(m*pi*x)*cos(n*pi*y) = 0
    # Onde (n,m) são os modos de vibração (Frequências do Mantra)
    
    def chladni_function(n, m, A=1, B=1):
        return A * np.sin(n * np.pi * X) * np.sin(m * np.pi * Y) + \
               B * np.sin(m * np.pi * X) * np.sin(n * np.pi * Y)

    # Mantras (Frequencies n, m)
    mantras = [
        {"name": "OM (Primordial Sound)", "modes": (1, 1), "desc": "Unity / Base State"},
        {"name": "YAM (Heart / Air)", "modes": (2, 2), "desc": "Quadrants / Stability"},
        {"name": "RAM (Fire / Action)", "modes": (3, 5), "desc": "Complex Geometry / Activation"},
        {"name": "VIMANA LAUNCH CODE", "modes": (7, 9), "desc": "High Frequency / Grid Override"}
    ]
    
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    
    for i, mantra in enumerate(mantras):
        n, m = mantra["modes"]
        Z = chladni_function(n, m)
        
        # O padrão é formado onde a vibração é ZERO (Nodal Lines)
        # É onde a "areia" (ou mercúrio) se acumula.
        
        axes[i].contour(X, Y, Z, levels=[0], colors='white', linewidths=3)
        axes[i].imshow(np.abs(Z), cmap='magma', extent=[0, 1, 0, 1], vmin=0, vmax=2)
        
        axes[i].set_title(f"{mantra['name']}\nModes (n={n}, m={m})")
        axes[i].axis('off')
        
        print(f"  > Executing Mantra '{mantra['name']}'...")
        print(f"    - Frequency Modes: n={n}, m={m}")
        print(f"    - Yantra Pattern Generated: {mantra['desc']}")

    plt.suptitle("Tamesis Bio-Interface: Sound (Mantra) programming Geometry (Yantra)", fontsize=16, color='white', backgroundcolor='black')
    fig.patch.set_facecolor('black')
    
    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\mantra_cymatics.png"
    plt.savefig(output_path, facecolor='black')
    print(f"Gráfico salvo em: {output_path}")

if __name__ == "__main__":
    simulate_chladni_patterns()
