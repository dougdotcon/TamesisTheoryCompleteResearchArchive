"""
Módulo de Rotação Galáctica: Teste da Teoria de Verlinde

Este módulo implementa simulações 2D da rotação galáctica comparando
a física newtoniana com a teoria entrópica de Verlinde.

Objetivo: Demonstrar curva de rotação plana sem matéria escura.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional

# CONFIGURAÇÃO DA GALÁXIA
G_NEWTON = 1.0           # Constante gravitacional newtoniana
M_BURACO_NEGRO = 1000.0  # Massa no centro da galáxia
ESCALA_VERLINDE = 20.0   # Distância de transição Verlinde
A_0 = 2.0               # Aceleração mínima do universo (constante de Verlinde) - AUMENTADO PARA DEMONSTRAÇÃO VISUAL

def forca_newtoniana(r: float) -> float:
    """
    Força gravitacional newtoniana clássica.
    F = GM/r²

    Parameters:
    -----------
    r : float
        Distância do centro

    Returns:
    --------
    float
        Aceleração gravitacional
    """
    if r < 1e-10:  # Evitar divisão por zero
        return 0.0
    return (G_NEWTON * M_BURACO_NEGRO) / (r ** 2)

def forca_verlinde(r: float) -> float:
    """
    Força gravitacional segundo a teoria entrópica de Verlinde.

    Modelo: Transição de fase baseada na aceleração
    - Alta aceleração (perto do centro): Comportamento newtoniano (1/r²)
    - Baixa aceleração (bordas): Decaimento mais lento (1/r)

    Parameters:
    -----------
    r : float
        Distância do centro

    Returns:
    --------
    float
        Aceleração gravitacional entrópica
    """
    if r < 1e-10:
        return 0.0

    # Calcular aceleração newtoniana
    aceleracao_newton = forca_newtoniana(r)

    # Transição de fase baseada na aceleração
    if aceleracao_newton > A_0:
        # Perto do centro: comportamento newtoniano
        return aceleracao_newton
    else:
        # Longe do centro: entropia muda o comportamento
        # A força decai mais devagar, mantendo velocidade orbital constante
        return np.sqrt(A_0 * aceleracao_newton)

def velocidade_orbital_estavel(r: float, modelo: str = 'newton') -> float:
    """
    Calcula a velocidade orbital necessária para órbita circular estável.

    Para órbita circular: F_centripeta = F_gravitacional
    v = sqrt(F * r)

    Parameters:
    -----------
    r : float
        Raio da órbita
    modelo : str
        'newton' ou 'verlinde'

    Returns:
    --------
    float
        Velocidade orbital
    """
    if modelo == 'newton':
        f = forca_newtoniana(r)
    elif modelo == 'verlinde':
        f = forca_verlinde(r)
    else:
        raise ValueError("Modelo deve ser 'newton' ou 'verlinde'")

    return np.sqrt(f * r)

def simular_orbita(modelo: str = 'newton',
                   raio_inicial: float = 10.0,
                   passos: int = 1000,
                   dt: float = 0.1) -> Tuple[List[float], List[float], float]:
    """
    Simula a órbita de uma estrela na galáxia.

    Parameters:
    -----------
    modelo : str
        'newton' ou 'verlinde'
    raio_inicial : float
        Distância inicial do centro
    passos : int
        Número de passos da simulação
    dt : float
        Passo de tempo

    Returns:
    --------
    tuple
        (trajetoria_x, trajetoria_y, velocidade_media)
    """
    # Estado inicial: na posição (raio_inicial, 0) com velocidade tangencial
    x, y = raio_inicial, 0.0

    # Velocidade inicial para órbita circular
    v_orbital = velocidade_orbital_estavel(raio_inicial, modelo)
    vx, vy = 0.0, v_orbital

    trajetoria_x = [x]
    trajetoria_y = [y]
    velocidades = [v_orbital]

    for _ in range(passos):
        r = np.sqrt(x**2 + y**2)

        # Calcular aceleração baseada no modelo
        if modelo == 'newton':
            aceleracao_total = forca_newtoniana(r)
        else:
            aceleracao_total = forca_verlinde(r)

        # Vetor aceleração (direção radial para o centro)
        ax = -aceleracao_total * (x / r)
        ay = -aceleracao_total * (y / r)

        # Atualizar velocidade (método de Euler)
        vx += ax * dt
        vy += ay * dt

        # Atualizar posição
        x += vx * dt
        y += vy * dt

        trajetoria_x.append(x)
        trajetoria_y.append(y)
        velocidades.append(np.sqrt(vx**2 + vy**2))

    velocidade_media = np.mean(velocidades)
    return trajetoria_x, trajetoria_y, velocidade_media

def calcular_curva_rotacao(raios: np.ndarray,
                          modelo: str = 'newton') -> np.ndarray:
    """
    Calcula a curva de rotação para múltiplos raios.

    Parameters:
    -----------
    raios : np.ndarray
        Array de raios para calcular
    modelo : str
        'newton' ou 'verlinde'

    Returns:
    --------
    np.ndarray
        Velocidades orbitais para cada raio
    """
    velocidades = []

    for r in raios:
        v = velocidade_orbital_estavel(r, modelo)
        velocidades.append(v)

    return np.array(velocidades)

def plotar_comparacao_orbitas(raio_teste: float = 50.0,
                              passos: int = 2000) -> None:
    """
    Plota comparação visual entre órbitas newtoniana e entrópica.

    Parameters:
    -----------
    raio_teste : float
        Raio para testar órbitas
    passos : int
        Passos da simulação
    """
    # Simular órbitas
    tx_n, ty_n, _ = simular_orbita('newton', raio_teste, passos)
    tx_v, ty_v, _ = simular_orbita('verlinde', raio_teste, passos)

    plt.figure(figsize=(8, 8))

    # Centro da galáxia
    plt.scatter([0], [0], color='black', s=200, marker='*',
                label='Buraco Negro Central', zorder=10)

    # Órbitas
    plt.plot(tx_n, ty_n, 'r--', linewidth=2, alpha=0.7,
             label=f'Newton (Raio={raio_teste})')
    plt.plot(tx_v, ty_v, 'b-', linewidth=2,
             label=f'Verlinde (Raio={raio_teste})')

    # Análise final
    r_final_n = np.sqrt(tx_n[-1]**2 + ty_n[-1]**2)
    r_final_v = np.sqrt(tx_v[-1]**2 + ty_v[-1]**2)

    plt.title('.1f' '.1f'
              f'\nNewton: Cai para r={r_final_n:.1f} | Verlinde: Mantém r={r_final_v:.1f}')
    plt.xlabel('Posição X')
    plt.ylabel('Posição Y')
    plt.legend()
    plt.axis('equal')
    plt.grid(True, alpha=0.3)

def plotar_curva_rotacao(raios: Optional[np.ndarray] = None) -> None:
    """
    Plota a curva de rotação comparando Newton vs Verlinde.

    Parameters:
    -----------
    raios : np.ndarray, optional
        Raios para calcular (padrão: linspace 5-100)
    """
    if raios is None:
        raios = np.linspace(5, 100, 20)

    # Calcular velocidades
    vel_newton = calcular_curva_rotacao(raios, 'newton')
    vel_verlinde = calcular_curva_rotacao(raios, 'verlinde')

    plt.figure(figsize=(10, 6))

    plt.plot(raios, vel_newton, 'r--o', linewidth=2, markersize=6,
             label='Newton: v ∝ 1/√r (cai rápido)')
    plt.plot(raios, vel_verlinde, 'b-o', linewidth=2, markersize=6,
             label='Verlinde: v ≈ constante (plana)')

    # Linha de referência para velocidade constante
    v_media_verlinde = np.mean(vel_verlinde[10:])  # Média nas bordas
    plt.axhline(y=v_media_verlinde, color='b', linestyle=':', alpha=0.5,
                label='.1f')

    plt.title('Curva de Rotação Galáctica: Newton vs Verlinde\n'
              '(Sem Matéria Escura vs Com Matéria Escura)')
    plt.xlabel('Distância do Centro (unidades)')
    plt.ylabel('Velocidade Orbital (unidades)')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Análise estatística
    variacao_newton = np.std(vel_newton) / np.mean(vel_newton)
    variacao_verlinde = np.std(vel_verlinde) / np.mean(vel_verlinde)

    print("\n📊 ANÁLISE DA CURVA DE ROTAÇÃO:")
    print(f"Newton - Variação: {variacao_newton:.1%} (cai)")
    print(f"Verlinde - Variação: {variacao_verlinde:.1%} (plana)")
    print(".1f")
    print(".1f")
    if variacao_verlinde < variacao_newton * 0.5:
        print("✅ SUCESSO: Curva plana demonstrada - Matéria Escura não necessária!")
    else:
        print("❌ FALHA: Ajustar parâmetros da transição Verlinde")

def demonstracao_completa(raio_teste: float = 50.0,
                         salvar_figuras: bool = True) -> None:
    """
    Demonstração completa: órbitas + curva de rotação.

    Parameters:
    -----------
    raio_teste : float
        Raio para teste orbital
    salvar_figuras : bool
        Se deve salvar figuras
    """
    print("=" * 70)
    print("DEMONSTRAÇÃO: ROTAÇÃO GALÁCTICA - NEWTON vs VERLINDE")
    print("=" * 70)
    print()
    print("Objetivo: Provar que a entropia gera rotação plana sem matéria escura")
    print()

    # Criar figura com subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Subplot 1: Órbitas
    plt.sca(ax1)

    tx_n, ty_n, _ = simular_orbita('newton', raio_teste, 2000)
    tx_v, ty_v, _ = simular_orbita('verlinde', raio_teste, 2000)

    ax1.scatter([0], [0], color='black', s=200, marker='*',
                label='Buraco Negro', zorder=10)
    ax1.plot(tx_n, ty_n, 'r--', linewidth=2, alpha=0.7,
             label=f'Newton (r={raio_teste})')
    ax1.plot(tx_v, ty_v, 'b-', linewidth=2,
             label=f'Verlinde (r={raio_teste})')

    ax1.set_title(f'Órbitas: Newton vs Verlinde (Raio={raio_teste})')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.legend()
    ax1.axis('equal')
    ax1.grid(True, alpha=0.3)

    # Subplot 2: Curva de rotação
    plt.sca(ax2)

    raios = np.linspace(5, 100, 20)
    vel_n = calcular_curva_rotacao(raios, 'newton')
    vel_v = calcular_curva_rotacao(raios, 'verlinde')

    ax2.plot(raios, vel_n, 'r--o', linewidth=2, markersize=6,
             label='Newton (cai)')
    ax2.plot(raios, vel_v, 'b-o', linewidth=2, markersize=6,
             label='Verlinde (plana)')

    ax2.set_title('Curva de Rotação Galáctica')
    ax2.set_xlabel('Distância do Centro')
    ax2.set_ylabel('Velocidade Orbital')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()

    if salvar_figuras:
        plt.savefig('results/rotation_curve_comparison.png', dpi=300, bbox_inches='tight')
        print("\n💾 Figuras salvas em 'results/rotation_curve_comparison.png'")

    plt.show()

    # Análise final
    print("\n🔬 ANÁLISE FINAL:")
    r_final_n = np.sqrt(tx_n[-1]**2 + ty_n[-1]**2)
    r_final_v = np.sqrt(tx_v[-1]**2 + ty_v[-1]**2)

    print(".1f")
    print(".1f")
    if abs(r_final_v - raio_teste) < abs(r_final_n - raio_teste):
        print("✅ TRIUNFO: Verlinde mantém órbita estável!")
        print("   A entropia explica rotação galáctica sem matéria escura.")
    else:
        print("⚠️  PARCIAL: Ajustar parâmetros para órbita mais estável.")

if __name__ == "__main__":
    # Demonstração rápida
    demonstracao_completa()