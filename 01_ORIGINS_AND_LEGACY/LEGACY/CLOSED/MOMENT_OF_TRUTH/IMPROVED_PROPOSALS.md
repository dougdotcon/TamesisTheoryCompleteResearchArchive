# PROPOSTAS DE VALIDAÇÃO (V2): Refinando a Ciência

**Motivação:** Os testes anteriores falharam em capturar a sutileza da teoria. TRI requer restrição energética para modularizar, e TDTR requer topologia para ver a seta do tempo.

---

## 2. TRI v2: O Teste Metabólico (`EXP_02_METABOLIC_TRI`)

**A Falha Anterior:** A rede neural clássica (Exp 02) não se dividiu porque o Backpropagation padrão é "guloso" e espalha o aprendizado por todos os neurônios indiscriminadamente.

**A Nova Hipótese (Tamesis Termodinâmica):**
Modularidade não é grátis; ela é uma estratégia de **Economia de Energia**.
O cérebro só se divide em hemisférios porque manter conexões longas é caro.

**O Experimento:**
Repetimos o teste "Lógica vs Caos", mas adicionamos um **Custo Metabólico** (Regularização L1) à função de perda.
$$ Loss = L_{tarefa} + \lambda \sum |Weights| $$

* **Previsão:** Sob pressão energética ($\lambda > 0$), a rede será forçada a matar conexões redundantes "cruzadas".
* **Critério de Sucesso:** Se a rede com o custo metabólico apresentar um *Modularization Score* alto (> 0.5), provamos que **TRI + Entropia = Inteligência Modular**.

---

## 3. TDTR v2: O Teste Topológico (`EXP_03_TOPOLOGICAL_ARROW`)

**A Falha Anterior:** A compressão `zlib` foi enganada pelo ruído de ponto flutuante. Sistemas caóticos pareciam ruído aleatório em ambas as direções.

**A Nova Hipótese (Grafos de Visibilidade):**
Em vez de olhar para os bits, olhamos para a **Geometria da Série Temporal**.
Transformamos a série temporal em um **Grafo de Visibilidade (HVG)**.

* Cada ponto $t$ é um nó.
* Conecta a $t'$ se houver "linha de visão".

**O Experimento:**

1. Gerar séries (Seno, Caos Logístico, Mercado).
2. Converter para Grafo (HVG).
3. Calcular a **Divergência de Kullback-Leibler (KLD)** entre a distribuição de graus "Olhando para Frente" ($P_{in}$) e "Olhando para Trás" ($P_{out}$).

* **Previsão:**
  * Seno: $KLD \approx 0$ (Grafo simétrico).
  * Caos/Mercado: $KLD \gg 0$ (O grafo tem uma "direção" estrutural).
* **Critério de Sucesso:** Detectar assimetria clara no Caos Logístico onde o `zlib` falhou.
