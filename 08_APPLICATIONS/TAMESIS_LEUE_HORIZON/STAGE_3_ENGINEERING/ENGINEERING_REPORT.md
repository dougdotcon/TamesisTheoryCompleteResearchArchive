# RELATÓRIO DE ENGENHARIA (V4): FINAL ROBUSTNESS VERIFICATION

**Status:** Validado Statisticamente (N=5 Seeds)
**Data:** 26/01/2026

## 1. Protocolo Experimental Rigoroso

Para garantir a validade científica, testamos o modelo Tamesis contra um **Baseline Forte** (ReLU + Regularização L2) e usamos a técnica de **Surrogate Gradient** (STE) para lidar com a saturação do horizonte, conforme padrão em quantização de redes neurais.

* **Métrica:** Erro de Rollout (MSE acumulado em 50 passos futuros recursivos).
* **Controle:** 5 Inicializações aleatórias (Seeds).
* **Baseline:** Redes com mesma topologia usando ReLU e Weight Decay (L2).

## 2. Resultados Finais

| Configuração | Erro de Rollout (Média) | Desvio Padrão | Desempenho Relativo |
|:--- |:--- |:--- |:--- |
| **ReLU + L2 (Baseline Forte)** | 0.5198 | ± 0.1681 | (Referência) |
| **Tamesis (LMC + AMRD)** | **0.1168** | ± 0.0643 | **+77.5% Melhor** |

## 3. Análise Técnica

O modelo Tamesis superou radicalmente a regularização L2 tradicional.

* **Interpretação:** Enquanto o L2 simplesmente "encolhe" os pesos para zero, a Gravidade AMRD "compacta" os pesos em torno da média da camada, preservando a estrutura da informação.
* **Surrogate Gradient:** O uso de gradientes substitutos ($1 - \tanh^2$) permitiu que a rede aprendesse eficientemente mesmo com ativações saturadas ("Horizontes"), confirmando a hipótese de *Transfer of Principle*.

## 4. Conclusão Final

A arquitetura inspirada na física não é apenas estável; ela é **superior** às técnicas padrão de regularização para dinâmica caótica.

### Evidência de Robustez

![Robustness V4](./final_recovery_benchmark.png)
*Fig 1. Comparação de Estabilidade. O erro acumulado do Tamesis (Direita) é drasticamente menor que o Baseline L2 (Esquerda).*
