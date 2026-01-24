#!/usr/bin/env python3
"""
Demonstração da Simulação de Gravidade Emergente

Este script executa a simulação básica 1D e mostra os resultados.
"""

import sys
import os

# Adicionar o diretório src ao path para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from simulacao_1d import simular_queda_entropica, plotar_simulacao, POSICAO_INICIAL, POSICAO_MASSA

def main():
    """Função principal da demonstração."""
    print("=" * 60)
    print("DEMONSTRAÇÃO: Gravidade Emergente via Entropia")
    print("=" * 60)
    print()
    print("Conceito: A gravidade surge da maximização de entropia,")
    print("não de forças fundamentais programadas.")
    print()
    print("Executando simulação...")

    # Executar simulação com parâmetros padrão
    trajetoria = simular_queda_entropica()

    print(f"Simulacao concluida com {len(trajetoria)} passos")
    print(".2f")
    print()

    # Análise básica
    posicao_final = trajetoria[-1]
    distancia_inicial = abs(POSICAO_INICIAL)
    distancia_final = abs(posicao_final)

    print("ANÁLISE DOS RESULTADOS:")
    print(".2f")
    print(".2f")
    print(".1f")
    print()

    if distancia_final < distancia_inicial * 0.1:
        print("✅ SUCESSO: A partícula foi atraída para o centro!")
        print("   Isso demonstra que a gravidade emerge da entropia.")
    else:
        print("⚠️  RESULTADO NEUTRO: A partícula não convergiu fortemente.")
        print("   Tente aumentar o número de passos ou ajustar parâmetros.")

    print()
    print("Gerando visualização...")

    # Plotar resultados
    plotar_simulacao(trajetoria, salvar_figura=True, nome_arquivo='demo_gravidade.png')

    print("Visualizacao salva como 'demo_gravidade.png'")
    print()
    print("Próximos passos sugeridos:")
    print("1. Experimente diferentes temperaturas")
    print("2. Aumente o número de passos para convergência")
    print("3. Explore a extensão 2D para rotação galáctica")

if __name__ == "__main__":
    main()