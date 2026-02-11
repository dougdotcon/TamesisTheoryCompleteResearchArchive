
import numpy as np
import matplotlib.pyplot as plt

def mantra_to_yantra_simulation():
    print("--- INICIANDO COMPILAÇÃO DE MANTRA PARA GEOMETRIA ---")
    
    # 1. INPUT (O Código Fonte - Simulação Sintética)
    # Sintetiza o Gayatri Mantra baseada em frequências védicas ideais
    # Om (136.1 Hz - Ano Terrestre), Harmônicos perfeitos
    sr = 22050
    duration = 5
    t = np.linspace(0, duration, sr * duration)
    
    # Frequências Fundamentais (Swaras)
    f_om = 136.1  # Do (Sa)
    f_fifth = f_om * 1.5 # Pa
    f_octave = f_om * 2.0
    
    # Uma mistura harmônica complexa simulando o canto tântrico (Rico em sobretons)
    # A interferência dessas ondas é que cria a geometria
    y = np.sin(2 * np.pi * f_om * t) + \
        0.5 * np.sin(2 * np.pi * f_fifth * t) + \
        0.3 * np.sin(2 * np.pi * f_octave * t)
        
    # Modulação de amplitude para simular a respiração/sílabas (Prana)
    envelope = (0.5 + 0.5 * np.sin(2 * np.pi * 1.5 * t)) 
    y = y * envelope

    # 2. PROCESSAMENTO (O Compilador Pânini/Fourier)
    # Usando numpy.fft para simular a análise espectral sem librosa
    n_fft = 2048
    
    # Short-Time Fourier Transform manual simples ou apenas FFT da janela central
    # Para o Yantra (Plot Polar), precisamos da estrutura harmônica média ou instantânea
    
    # Vamos pegar uma janela no meio onde o som é estável
    center_idx = len(y) // 2
    window = y[center_idx : center_idx + n_fft] * np.hanning(n_fft)
    spectrum = np.fft.rfft(window)
    magnitude = np.abs(spectrum)
    
    # 3. RENDERIZAÇÃO (A Interface Yantra)
    fig = plt.figure(figsize=(12, 6))
    
    # Plot 1: Waveform (O Som no Tempo)
    ax1 = plt.subplot(1, 2, 1)
    ax1.plot(t[:1000], y[:1000], color='c')
    ax1.set_title('Input: Mantra Waveform (Time Domain)')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: A Projeção Polar (Yantra Geométrico)
    ax2 = plt.subplot(1, 2, 2, projection='polar')
    
    # Mapeamento: Frequência -> Raio, Fase/Tempo -> Ângulo?
    # O conceito de Cymatics é que a frequência cria nós em posições geométricas.
    # Vamos visualizar a Magnitude da FFT distribuída circularmente para simular a simetria.
    
    # Normalização
    magnitude = magnitude / np.max(magnitude)
    
    # Espelhamento para criar simetria (A geometria sagrada é simétrica)
    # "Dobramos" o espectro ao redor do círculo
    num_petals = 12 # Simbolizando o Lótus do Coração (Anahata)
    
    theta = np.linspace(0, 2*np.pi, len(magnitude) * num_petals)
    # Repetimos o espectro para criar as "pétalas"
    radial_pattern = np.tile(magnitude, num_petals)
    
    # Corte para caber no theta se necessário, ou ajuste theta
    radial_pattern = radial_pattern[:len(theta)]
    
    # Plot
    ax2.plot(theta, radial_pattern, color='gold', linewidth=1.5)
    ax2.fill(theta, radial_pattern, alpha=0.5, color='orange')
    
    ax2.set_title(f'Output: Geometric Yantra\n(Om Frequency {f_om}Hz - {num_petals} Petals)')
    ax2.set_axis_off()
    ax2.set_facecolor('black')
    
    plt.suptitle("Tamesis Simulation: The Gayatri Mantra as Code", fontsize=16)
    fig.patch.set_facecolor('black')
    ax1.set_facecolor('black')
    ax1.title.set_color('white')
    ax2.title.set_color('white')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.xaxis.label.set_color('white')
    ax1.yaxis.label.set_color('white')

    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\mantra_spectogram_yantra.png"
    plt.savefig(output_path, facecolor='black')
    print(f"Gráfico salvo em: {output_path}")

if __name__ == "__main__":
    mantra_to_yantra_simulation()
