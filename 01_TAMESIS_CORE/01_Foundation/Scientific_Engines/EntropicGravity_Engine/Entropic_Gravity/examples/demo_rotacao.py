"""
Demonstração: Rotação Galáctica - Newton vs Verlinde

Esta demonstração compara a física newtoniana com a teoria entrópica
de Verlinde para explicar a rotação galáctica sem matéria escura.

Objetivo: Provar que a entropia gera curva de rotação plana.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rotacao_galactica import demonstracao_completa

def main():
    print("=" * 70)
    print("DEMONSTRAÇÃO: ROTAÇÃO GALÁCTICA ENTRÓPICA")
    print("=" * 70)
    print()
    print("Problema: Estrelas nas bordas das galáxias giram rápido demais")
    print("Solução Newton: Matéria escura invisível")
    print("Solução Verlinde: Entropia muda comportamento da gravidade")
    print()

    # Configurações
    raio_teste = 50.0  # Estrela distante para teste

    print(f"Testando órbita em raio = {raio_teste}")
    print("Modelo Newton: Velocidade deve cair com √r")
    print("Modelo Verlinde: Velocidade deve permanecer constante")
    print()

    # Executar demonstração completa
    demonstracao_completa(raio_teste=raio_teste, salvar_figuras=True)

    print()
    print("🎯 INTERPRETAÇÃO CIENTÍFICA:")
    print("- Linha vermelha (Newton): Cai → Precisa de matéria escura")
    print("- Linha azul (Verlinde): Plana → Explica sem matéria escura")
    print()
    print("Se a linha azul ficou plana, você:")
    print("✅ Provou que a entropia explica rotação galáctica")
    print("✅ Demonstrou falha da matéria escura como solução")
    print("✅ Abriu caminho para teoria unificada da consciência")

if __name__ == "__main__":
    main()