"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RESTAURADOR DE QR CODES DE ISING                          ║
║                        Tamesis Theory - Kernel v3                            ║
║                                                                              ║
║  Aplicação do Modelo de Ising e Censura Termodinâmica para restauração      ║
║  de QR Codes danificados por ruído "sal e pimenta".                         ║
║                                                                              ║
║  Física: Cada pixel é um spin (+1 branco, -1 preto). O sistema relaxa       ║
║  para o estado de menor energia através do algoritmo Metropolis-Hastings.   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import qrcode
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# ═══════════════════════════════════════════════════════════════════════════════
# PARÂMETROS FÍSICOS DO MODELO DE ISING
# ═══════════════════════════════════════════════════════════════════════════════

J = 0.8          # Coupling constant: suaviza ruído isolado
h = 1.5          # External field: fidelidade forte à imagem ruidosa
T_initial = 4.0  # Temperatura inicial (alta entropia)
T_final = 0.01   # Temperatura final (cristalização)
cooling_rate = 0.98   # Taxa de resfriamento

# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES PRINCIPAIS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_qr_code(data: str = "https://tamesis-theory.org", size: int = 100) -> np.ndarray:
    """
    Gera um QR Code válido como matriz de spins.
    
    Returns:
        np.ndarray: Matriz com valores +1 (branco) e -1 (preto)
    """
    # Criar QR Code
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Converter para imagem e redimensionar
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size), Image.Resampling.NEAREST)
    
    # Converter para matriz de spins: branco=+1, preto=-1
    spin_matrix = np.array(img.convert('L'))
    spin_matrix = np.where(spin_matrix > 128, 1, -1).astype(np.int8)
    
    return spin_matrix


def add_noise(spins: np.ndarray, noise_level: float = 0.30) -> np.ndarray:
    """
    Adiciona ruído "sal e pimenta" à imagem.
    Inverte uma fração dos pixels aleatoriamente.
    
    Args:
        spins: Matriz de spins original
        noise_level: Fração de pixels a inverter (0.3 = 30%)
    
    Returns:
        np.ndarray: Matriz com ruído aplicado
    """
    noisy = spins.copy()
    mask = np.random.random(spins.shape) < noise_level
    noisy[mask] = -noisy[mask]  # Inverte os spins selecionados
    return noisy


def calculate_local_energy(spins: np.ndarray, original: np.ndarray, i: int, j: int) -> float:
    """
    Calcula a energia local do Hamiltoniano de Ising para um pixel específico.
    
    H = -J × Σ(Sᵢ·Sⱼ) - h × Σ(Sᵢ·Sᵢ_original)
    
    Args:
        spins: Estado atual do sistema
        original: Imagem original (ruidosa) - campo externo
        i, j: Coordenadas do pixel
    
    Returns:
        float: Energia local do pixel
    """
    rows, cols = spins.shape
    s = spins[i, j]
    
    # Soma dos vizinhos (condições de contorno periódicas)
    neighbors_sum = (
        spins[(i - 1) % rows, j] +
        spins[(i + 1) % rows, j] +
        spins[i, (j - 1) % cols] +
        spins[i, (j + 1) % cols]
    )
    
    # Energia de interação (vizinhos querem ser iguais)
    E_interaction = -J * s * neighbors_sum
    
    # Energia de campo externo (fidelidade à imagem original)
    E_field = -h * s * original[i, j]
    
    return E_interaction + E_field


def metropolis_step(spins: np.ndarray, original: np.ndarray, temperature: float) -> tuple:
    """
    Executa um passo do algoritmo Metropolis-Hastings.
    
    O algoritmo tenta inverter um spin aleatório e aceita a mudança
    baseado na variação de energia (critério de Boltzmann).
    
    Args:
        spins: Estado atual do sistema
        original: Imagem original (campo externo)
        temperature: Temperatura atual do sistema
    
    Returns:
        tuple: (spins atualizados, delta_E, aceito)
    """
    rows, cols = spins.shape
    
    # Escolhe um pixel aleatório
    i = np.random.randint(0, rows)
    j = np.random.randint(0, cols)
    
    # Calcula a energia antes
    E_before = calculate_local_energy(spins, original, i, j)
    
    # Inverte o spin temporariamente
    spins[i, j] = -spins[i, j]
    
    # Calcula a energia depois
    E_after = calculate_local_energy(spins, original, i, j)
    
    # Variação de energia
    delta_E = E_after - E_before
    
    # Critério de Metropolis (Aceitação de Boltzmann)
    if delta_E <= 0:
        # Aceita sempre se a energia diminuiu
        accepted = True
    else:
        # Aceita com probabilidade exp(-ΔE/kT)
        probability = np.exp(-delta_E / temperature)
        if np.random.random() < probability:
            accepted = True
        else:
            # Rejeita: reverte a mudança
            spins[i, j] = -spins[i, j]
            accepted = False
    
    return spins, delta_E, accepted


def calculate_total_energy(spins: np.ndarray, original: np.ndarray) -> float:
    """
    Calcula a energia total do sistema.
    
    Returns:
        float: Energia total do Hamiltoniano
    """
    rows, cols = spins.shape
    
    # Energia de interação (vizinhos)
    E_interaction = 0
    for i in range(rows):
        for j in range(cols):
            # Apenas vizinhos à direita e abaixo para evitar contagem dupla
            E_interaction -= J * spins[i, j] * spins[(i + 1) % rows, j]
            E_interaction -= J * spins[i, j] * spins[i, (j + 1) % cols]
    
    # Energia de campo externo
    E_field = -h * np.sum(spins * original)
    
    return E_interaction + E_field


def calculate_accuracy(restored: np.ndarray, original: np.ndarray) -> float:
    """
    Calcula a porcentagem de pixels corretamente restaurados.
    """
    return 100 * np.mean(restored == original)


def simulate_annealing(noisy: np.ndarray, original_clean: np.ndarray, 
                       steps_per_temp: int = 5000, 
                       visualize: bool = True) -> np.ndarray:
    """
    Executa a simulação de Simulated Annealing (Resfriamento Simulado).
    
    O sistema "ferve" em alta temperatura e gradualmente "esfria",
    permitindo que a estrutura ordenada cristalize.
    
    Args:
        noisy: Imagem ruidosa (estado inicial)
        original_clean: Imagem original limpa (para métricas)
        steps_per_temp: Número de passos Metropolis por temperatura
        visualize: Se True, mostra animação em tempo real
    
    Returns:
        np.ndarray: Imagem restaurada
    """
    spins = noisy.copy()
    original_noisy = noisy.copy()  # Campo externo é a imagem ruidosa
    
    T = T_initial
    
    # Histórico para visualização
    energy_history = []
    accuracy_history = []
    temp_history = []
    
    print("\n" + "═" * 60)
    print("   🔥 INICIANDO SIMULAÇÃO DE ISING (Metropolis-Hastings)")
    print("═" * 60)
    print(f"   Temperatura inicial: {T_initial}")
    print(f"   Temperatura final:   {T_final}")
    print(f"   Taxa de resfriamento: {cooling_rate}")
    print(f"   Passos por temperatura: {steps_per_temp}")
    print("═" * 60 + "\n")
    
    iteration = 0
    
    while T > T_final:
        accepted_count = 0
        
        for _ in range(steps_per_temp):
            spins, delta_E, accepted = metropolis_step(spins, original_noisy, T)
            if accepted:
                accepted_count += 1
        
        # Calcular métricas
        current_energy = calculate_total_energy(spins, original_noisy)
        current_accuracy = calculate_accuracy(spins, original_clean)
        
        energy_history.append(current_energy)
        accuracy_history.append(current_accuracy)
        temp_history.append(T)
        
        # Log de progresso
        acceptance_rate = 100 * accepted_count / steps_per_temp
        print(f"   T={T:.4f} | Energia={current_energy:,.0f} | "
              f"Acurácia={current_accuracy:.1f}% | "
              f"Taxa aceite={acceptance_rate:.1f}%")
        
        # Resfriar o sistema
        T *= cooling_rate
        iteration += 1
    
    print("\n" + "═" * 60)
    print("   ❄️ CRISTALIZAÇÃO COMPLETA!")
    print(f"   Acurácia final: {current_accuracy:.1f}%")
    print("═" * 60 + "\n")
    
    return spins, energy_history, accuracy_history, temp_history


def visualize_results(original: np.ndarray, noisy: np.ndarray, restored: np.ndarray,
                      energy_history: list, accuracy_history: list, temp_history: list):
    """
    Visualiza os resultados: comparação de imagens e gráficos de convergência.
    """
    fig = plt.figure(figsize=(14, 8))
    fig.suptitle('🔬 Restaurador de QR Codes de Ising - Tamesis Kernel v3', 
                 fontsize=14, fontweight='bold')
    
    # ═══════════════════════════════════════════════════════════════════════
    # LINHA SUPERIOR: Imagens
    # ═══════════════════════════════════════════════════════════════════════
    
    # QR Code Original
    ax1 = fig.add_subplot(2, 3, 1)
    ax1.imshow(original, cmap='gray', vmin=-1, vmax=1)
    ax1.set_title('✅ QR Code Original', fontweight='bold')
    ax1.axis('off')
    
    # QR Code com Ruído
    ax2 = fig.add_subplot(2, 3, 2)
    ax2.imshow(noisy, cmap='gray', vmin=-1, vmax=1)
    noise_level = 100 * np.mean(original != noisy)
    ax2.set_title(f'💥 Com Ruído ({noise_level:.0f}% danificado)', fontweight='bold')
    ax2.axis('off')
    
    # QR Code Restaurado
    ax3 = fig.add_subplot(2, 3, 3)
    ax3.imshow(restored, cmap='gray', vmin=-1, vmax=1)
    accuracy = calculate_accuracy(restored, original)
    ax3.set_title(f'🧊 Restaurado ({accuracy:.1f}% correto)', fontweight='bold')
    ax3.axis('off')
    
    # ═══════════════════════════════════════════════════════════════════════
    # LINHA INFERIOR: Gráficos de Convergência
    # ═══════════════════════════════════════════════════════════════════════
    
    # Gráfico de Energia
    ax4 = fig.add_subplot(2, 3, 4)
    ax4.plot(energy_history, 'b-', linewidth=1.5)
    ax4.set_xlabel('Iteração (Temperatura ↓)')
    ax4.set_ylabel('Energia Total')
    ax4.set_title('📉 Relaxamento de Energia', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # Gráfico de Acurácia
    ax5 = fig.add_subplot(2, 3, 5)
    ax5.plot(accuracy_history, 'g-', linewidth=1.5)
    ax5.set_xlabel('Iteração (Temperatura ↓)')
    ax5.set_ylabel('Acurácia (%)')
    ax5.set_title('📈 Recuperação da Informação', fontweight='bold')
    ax5.set_ylim(0, 105)
    ax5.grid(True, alpha=0.3)
    
    # Gráfico de Temperatura
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.semilogy(temp_history, 'r-', linewidth=1.5)
    ax6.set_xlabel('Iteração')
    ax6.set_ylabel('Temperatura (log)')
    ax6.set_title('🌡️ Resfriamento Termodinâmico', fontweight='bold')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('resultado_ising.png', dpi=150, bbox_inches='tight')
    print("   💾 Resultado salvo em 'resultado_ising.png'")
    plt.show()


def save_qr_image(spins: np.ndarray, filename: str):
    """Salva a matriz de spins como imagem PNG."""
    img_array = np.where(spins == 1, 255, 0).astype(np.uint8)
    img = Image.fromarray(img_array, mode='L')
    img.save(filename)
    print(f"   💾 Imagem salva: {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN: EXECUÇÃO DA PROVA DE CONCEITO
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ████████╗ █████╗ ███╗   ███╗███████╗███████╗██╗███████╗                 ║
║     ╚══██╔══╝██╔══██╗████╗ ████║██╔════╝██╔════╝██║██╔════╝                 ║
║        ██║   ███████║██╔████╔██║█████╗  ███████╗██║███████╗                 ║
║        ██║   ██╔══██║██║╚██╔╝██║██╔══╝  ╚════██║██║╚════██║                 ║
║        ██║   ██║  ██║██║ ╚═╝ ██║███████╗███████║██║███████║                 ║
║        ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚═╝╚══════╝                 ║
║                                                                              ║
║              RESTAURADOR DE QR CODES DE ISING - Kernel v3                    ║
║                   Processador Entrópico Termodinâmico                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # ═══════════════════════════════════════════════════════════════════════
    # FASE 1: GERAÇÃO
    # ═══════════════════════════════════════════════════════════════════════
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│  FASE 1: GERAÇÃO DO QR CODE                                 │")
    print("└─────────────────────────────────────────────────────────────┘")
    
    qr_data = "Tamesis Theory - A ordem emerge do caos termodinâmico!"
    original = generate_qr_code(qr_data, size=100)
    print(f"   ✓ QR Code gerado com {original.shape[0]}x{original.shape[1]} pixels")
    print(f"   ✓ Conteúdo: '{qr_data}'")
    save_qr_image(original, 'qr_original.png')
    
    # ═══════════════════════════════════════════════════════════════════════
    # FASE 2: DESTRUIÇÃO
    # ═══════════════════════════════════════════════════════════════════════
    print("\n┌─────────────────────────────────────────────────────────────┐")
    print("│  FASE 2: DESTRUIÇÃO (Adição de Ruído)                       │")
    print("└─────────────────────────────────────────────────────────────┘")
    
    noise_level = 0.20  # 20% de ruído (mais fácil de restaurar)
    noisy = add_noise(original, noise_level)
    damaged_pixels = np.sum(original != noisy)
    print(f"   💥 {damaged_pixels:,} pixels danificados ({100*noise_level:.0f}% do total)")
    print(f"   ⚠️  A imagem agora está ilegível para câmeras!")
    save_qr_image(noisy, 'qr_noisy.png')
    
    # ═══════════════════════════════════════════════════════════════════════
    # FASE 3: CURA FÍSICA (Simulação de Ising)
    # ═══════════════════════════════════════════════════════════════════════
    print("\n┌─────────────────────────────────────────────────────────────┐")
    print("│  FASE 3: CURA FÍSICA (Simulação de Ising)                   │")
    print("└─────────────────────────────────────────────────────────────┘")
    
    start_time = time.time()
    
    restored, energy_hist, accuracy_hist, temp_hist = simulate_annealing(
        noisy, 
        original,
        steps_per_temp=5000,
        visualize=True
    )
    
    elapsed_time = time.time() - start_time
    save_qr_image(restored, 'qr_restored.png')
    
    # ═══════════════════════════════════════════════════════════════════════
    # FASE 4: PROVA (Resultados)
    # ═══════════════════════════════════════════════════════════════════════
    print("\n┌─────────────────────────────────────────────────────────────┐")
    print("│  FASE 4: PROVA - RESULTADOS FINAIS                          │")
    print("└─────────────────────────────────────────────────────────────┘")
    
    final_accuracy = calculate_accuracy(restored, original)
    print(f"""
   📊 MÉTRICAS FINAIS:
   ──────────────────────────────────────────────────────────
   • Pixels originais:     {original.size:,}
   • Pixels danificados:   {damaged_pixels:,} ({100*noise_level:.0f}%)
   • Pixels recuperados:   {int(final_accuracy/100 * original.size):,}
   • Acurácia final:       {final_accuracy:.2f}%
   • Tempo de execução:    {elapsed_time:.1f} segundos
   ──────────────────────────────────────────────────────────
   
   🎯 TESTE DE PROVA:
   Aponte a câmera do seu celular para 'qr_restored.png'
   Se a física funcionou, o QR Code será lido!
   
   ══════════════════════════════════════════════════════════
   "A ordem emerge da minimização de energia livre,
    não de regras lógicas rígidas." - Pilar 3 (TDTR)
   ══════════════════════════════════════════════════════════
    """)
    
    # Visualização final
    visualize_results(original, noisy, restored, energy_hist, accuracy_hist, temp_hist)


if __name__ == "__main__":
    main()
