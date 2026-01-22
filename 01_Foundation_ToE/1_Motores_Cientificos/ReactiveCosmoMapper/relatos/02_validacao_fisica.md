# Relatório 02: Validação Física do Modelo Reativo

**Data:** 29/12/2025
**Módulo:** `src/reactive_gravity.py`, `src/reactive_cosmo_mapper.py`

## Objetivo
Validar computacionalmente se a **Gravidade Entrópica** (sem Matéria Escura) consegue reproduzir as curvas de rotação planas observadas em galáxias espirais.

## Fundamentação Teórica
O modelo baseia-se na equação de interpolação de Verlinde/MOND, onde a aceleração efetiva $g_{obs}$ emerge da aceleração Newtoniana $g_N$ e de uma escala de aceleração fundamental $a_0$:

$$ g_{obs} = \frac{g_N + \sqrt{g_N^2 + 4 g_N a_0}}{2} $$

Onde $a_0 \approx 1.2 \times 10^{-10} m/s^2$ (aceleração crítica relacionada à constante de Hubble).

## Metodologia de Teste
1. **Classe `ReactiveGravity`:** Implementação pura da matemática vetorial e escalar da teoria.
2. **Testes Unitários:**
    - Regime Newtoniano ($g_N \gg a_0$): Confirmado erro relativo $< 0.1\%$.
    - Regime Entrópico ($g_N \ll a_0$): Confirmado comportamento $1/r$ na força (velocidade constante).
3. **Simulação da Galáxia NGC0024:**
    - Dados de entrada: Massa Bariônica (Estrelas + Gás).
    - Comparação: Velocidade Newtoniana vs. Velocidade Reativa vs. Observação.

## Resultados e Evidências
- **Gráfico Gerado:** `NGC0024_rotation.png`
- **Análise:**
    - A curva Newtoniana (azul) decai conforme esperado ($v \propto r^{-1/2}$), falhando em explicar a rotação nas bordas.
    - A curva Reativa (laranja) **permanece plana** nas bordas, alinhando-se com o valor observado ($V_{flat} \approx 106 km/s$).
- **Conclusão:** O "Kernel de Gravidade Reativa" reproduz com sucesso os efeitos dinâmicos atribuídos à Matéria Escura, utilizando apenas massa visível.
