"""
Simulação de Gravidade Emergente baseada na Teoria de Entropia de Erik Verlinde

Este módulo implementa a simulação básica 1D onde a gravidade emerge
da maximização de entropia, sem programar forças diretamente.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO DO UNIVERSO ENTRÓPICO ---
# Não existe constante G. Não existe Lei de Newton aqui.
# Apenas Probabilidade.

POSICAO_MASSA = 0.0  # O centro do universo (Onde a informação é densa)
POSICAO_INICIAL = 50.0  # Onde soltamos a partícula
PASSOS = 2000  # Número de passos da simulação

def densidade_informacao(x):
    """
    Segundo Verlinde, a entropia muda com a distância.
    Perto da massa, a densidade de bits holográficos é maior.
    Isso cria um 'gradiente de entropia'.

    Parameters:
    -----------
    x : float
        Posição da partícula

    Returns:
    --------
    float
        Densidade de informação (proporcional à entropia)
    """
    # Evitar divisão por zero
    distancia = abs(x - POSICAO_MASSA)
    if distancia < 1.0:
        return 10000.0  # Aumentado para gradiente mais forte

    # Modelo melhorado: A Entropia (S) é proporcional a 1/r^2
    # Simulando força gravitacional ~1/r^2
    return 1.0 / (distancia ** 2)

def simular_queda_entropica(posicao_inicial=None, passos=None, temperatura=0.1):
    """
    Simula a queda entrópica de uma partícula em direção ao centro de massa.

    Parameters:
    -----------
    posicao_inicial : float, optional
        Posição inicial da partícula (padrão: POSICAO_INICIAL)
    passos : int, optional
        Número de passos da simulação (padrão: PASSOS)
    temperatura : float, optional
        Temperatura do sistema (agitação térmica)

    Returns:
    --------
    list
        Trajetória da partícula ao longo do tempo
    """
    if posicao_inicial is None:
        posicao_inicial = POSICAO_INICIAL
    if passos is None:
        passos = PASSOS

    posicao = posicao_inicial
    trajetoria = [posicao]

    for _ in range(passos):
        # 1. Propor um movimento aleatório (Random Walk puro)
        passo = np.random.choice([-1, 1]) * 0.5
        nova_posicao_proposta = posicao + passo

        # 2. Calcular a Variação de Entropia (Delta S)
        # S_atual vs S_nova
        S_atual = densidade_informacao(posicao)
        S_nova = densidade_informacao(nova_posicao_proposta)

        diferenca_S = S_nova - S_atual

        # 3. A Regra Termodinâmica (Força Entrópica)
        # O sistema prefere ir para onde a Entropia é maior (perto da massa).
        # Usamos Metropolis para aceitar o movimento

        # Se a entropia aumenta (diferenca_S > 0), aceitamos sempre.
        # Se diminui, aceitamos com uma probabilidade pequena.
        if diferenca_S > 0 or np.random.rand() < np.exp(diferenca_S / temperatura):
            posicao = nova_posicao_proposta

        trajetoria.append(posicao)

        # Se tocou na massa, para
        if abs(posicao - POSICAO_MASSA) < 1.0:
            break

    return trajetoria

def plotar_simulacao(trajetoria, salvar_figura=False, nome_arquivo='simulacao_gravidade.png'):
    """
    Plota a trajetória da simulação.

    Parameters:
    -----------
    trajetoria : list
        Trajetória da partícula
    salvar_figura : bool, optional
        Se True, salva a figura em arquivo
    nome_arquivo : str, optional
        Nome do arquivo para salvar a figura
    """
    plt.figure(figsize=(10, 6))
    plt.plot(trajetoria, label='Trajetória da Partícula')
    plt.axhline(y=POSICAO_MASSA, color='r', linestyle='--', label='Centro de Massa (Alta Entropia)')
    plt.title('Simulação de Gravidade Entrópica (Verlinde)\nSem Força G, apenas Maximização de Entropia')
    plt.xlabel('Tempo (Passos)')
    plt.ylabel('Distância')
    plt.legend()
    plt.grid(True, alpha=0.3)

    if salvar_figura:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
        print(f"Figura salva como {nome_arquivo}")

    plt.show()

if __name__ == "__main__":
    # --- EXECUÇÃO E PROVA ---
    print("Executando simulação de gravidade emergente...")
    historico = simular_queda_entropica()

    print(f"Simulação concluída. Trajetória final: {len(historico)} passos")
    print(".2f")

    plotar_simulacao(historico, salvar_figura=True)