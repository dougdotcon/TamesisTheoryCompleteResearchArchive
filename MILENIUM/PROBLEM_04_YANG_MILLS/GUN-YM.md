# PESQUISAS.MD: Análise Tática para o Roadmap Yang-Mills

## 🧭 Visão Geral: O Que Estamos Buscando

Nosso objetivo no `ROADMAP_YANG_MILLS.md` é estabelecer a **Estabilidade Estrutural de Teorias de Calibre**. Não se trata apenas de provar que a equação existe, mas de mostrar que a fase "sem gap" (gapless) é **estruturalmente instável** em 4D. A massa do glúon não é um acidente, é uma necessidade para a consistência termodinâmica da teoria.

Filtragem estratégica da literatura:

1. **Cemitério (Tentativas Falhas):** Onde a intuição perturbativa e a análise funcional clássica colidiram com o muro do infravermelho.
2. **Espelhos (Abordagens Adjacentes):** Modelos (3D, Lattice) onde o gap já foi provado ou é manifesto.
3. **Arsenal (Ferramentas Locais):** As técnicas específicas que usaremos para construir o argumento de "Seleção de Fase".

---

## 💀 TIPO 1: Tentativas Sérias que Falharam (E Onde Exatamente Quebraram)

*Análise de "No-Go Zones". Por que não conseguimos construir isso "na mão" até agora?*

### 1.1 O Programa de Balaban (1980s)

* **A Tentativa:** Construção rigorosa via Grupo de Renormalização no reticulado, integrando escala por escala.
* **Onde Quebrou:**
  * **Hiato UV-IR:** Balaban provou a Estabilidade Ultravioleta (a teoria não explode para $a \to 0$). Mas não conseguiu conectar isso ao Confinamento (IR).
  * **Perda de Controle:** Ao chegar nas escalas de baixa energia (acoplamento forte), a expansão de cluster deixa de convergir. A ferramenta analítica "quebra" justamente onde a massa surge.
* **Lição para o Roadmap:**
  * ❌ **Não tentar:** Estender a prova de Balaban analiticamente para o IR.
  * ✅ **Fazer:** Usar a **Anomalia de Rastro** como critério de seleção macroscópica. Se Balaban garante o UV, nós só precisamos mostrar que o único IR consistente com esse UV é o que tem Gap.

### 1.2 Instantons Diluídos ('t Hooft)

* **A Tentativa:** Explicar a massa/confinamento via tunelamento entre vácuos.
* **Onde Quebrou:**
  * **Catástrofe Infravermelha:** A integral sobre o tamanho $\rho$ dos instantons diverge ($\int d\rho \rho^{\beta_0 - 5}$). Instantons grandes proliferam e o gás deixa de ser diluído.
* **Lição para o Roadmap:**
  * Objetos semiclássicos isolados não explicam o vácuo 4D denso. O vácuo é um "líquido", não um gás. Precisamos de **argumentos de medida estatística** (Track A3), não apenas de soluções clássicas.

### 1.3 Teoria de Perturbação Ressomada

* **A Tentativa:** Somar a série perturbativa (Borel) para encontrar efeitos não-perturbativos.
* **Onde Quebrou:**
  * **Ambiguidades de Renormalon:** A série é assintótica e possui polos no plano de Borel que tornam a soma ambígua. Sem informações extras (trans-séries), a teoria é incompleta.
* **Lição para o Roadmap:**
  * A série perturbativa **não contém** a informação do Gap. O Gap é um fenômeno singular ($e^{-1/g^2}$).

---

## 🌌 TIPO 2: Abordagens Estruturais Adjacentes (O Mesmo Espírito)

*Modelos que provam que "Gap é o estado natural de sistemas de calibre confinados".*

### 2.1 Osterwalder-Seiler (Lattice Strong Coupling)

* **Conceito:** Teorema rigoroso que prova o Gap e o Confinamento para Yang-Mills no reticulado quando $g \gg 1$.
* **Conexão com o Roadmap:**
  * Mostra que a fase confinada/massiva **existe** matematicamente. O problema é apenas conectá-la ao limite contínuo ($g \to 0, a \to 0$).
  * Nosso argumento será de **continuidade de fase**: se não há transição de fase (crítica) entre acoplamento forte e fraco, o Gap de Osterwalder-Seiler persiste.

### 2.2 Mecanismo de Polyakov (QED Compacta em 3D)

* **Conceito:** Geração de massa via plasma de monopolos.
* **Conexão com o Roadmap:**
  * Um exemplo perfeito de como a topologia gera massa sem Higgs.
  * Em 4D, os monopolos viram loops. A condensação desses loops ("supercondutor dual") é o mecanismo físico por trás da nossa "Seleção de Fase".

### 2.3 Gribov-Zwanziger (Restrição Geométrica)

* **Conceito:** O espaço de configurações tem um horizonte físico (Horizonte de Gribov).
* **Conexão com o Roadmap:**
  * O horizonte corta os graus de liberdade de baixa energia (suprime infravermelho). Isso gera uma massa efetiva (Parâmetro de Gribov $\gamma_G$).
  * Isso valida nossa tese de **Censura**: o espaço de fase "livre" é uma ilusão matemática. A geometria real censura o propagador livre.

---

## 🛠️ TIPO 3: Ferramentas Técnicas Locais (O Arsenal)

*Componentes para a construção dos Papers no Track B.*

### 3.1 Quantização Estocástica (Parisi-Wu)

* **Origem:** TQC / Probabilidade.
* **Uso Tático:**
  * Permite definir a teoria sem fixação de calibre algébrica (evita Gribov na formulação).
  * A evolução em um "tempo fictício" $\tau$ relaxa para a distribuição de equilíbrio.
  * Resultados recentes (2025) de Hairer e outros dão base rigorosa a isso. Podemos usar a estabilidade da equação estocástica como proxy para a estabilidade do vácuo.

### 3.2 Anomalia de Rastro (Trace Anomaly)

* **Origem:** Renormalização.
* **Uso Tático:**
  * A equação $T^\mu_\mu \propto \beta(g) F^2 \neq 0$.
  * Isso prova que a invariância de escala **é quebrada quanticamente**.
  * Argumento central do Roadmap: **Uma teoria sem escala (gapless) é incompatível com a Anomalia de Rastro.** Se a escala é quebrada, deve surgir uma escala de massa ($M_{gap}$).

### 3.3 Trans-séries e Ressurgência

* **Origem:** Dunne, Ünsal.
* **Uso Tático:**
  * Formalismo para conectar perturbative e não-perturbativo.
  * Nos permite argumentar que o "mundo perturbativo" (sem massa) conhece suas próprias falhas e aponta para a existência de termos não-perturbativos (massa).

---

## 📉 Síntese para o Roadmap

O `GUN-YM` reestruturado confirma a estratégia do **Track A - The Exclusion Mechanism**:

1. **Não procurar o campo escalar:** (A Trivialidade de $\phi^4$ mata isso).
2. **Apostar na Instabilidade de Escala:** A Anomalia de Rastro (3.2) é o dado fundamental que força o surgimento de uma escala.
3. **Usar a Geometria como Prova:** O Horizonte de Gribov (2.3) e os resultados de Reticulado (2.1) mostram que o espaço de configurações "gosta" de ter Gap. A fase sem gap é instável.

**Próxima Ação:** Focar o `PAPER_B_STRUCTURAL_SUPPRESSION` em transformar a Anomalia de Rastro em uma obstrução topológica formal para a existência de um espectro contínuo começando em zero.

---

### Referências Selecionadas

* **Osterwalder-Seiler (1978):** *Lattice Yang-Mills at Strong Coupling.* (A Base de Existência)
* **Balaban (1980s):** *UV Stability of Yang-Mills.* (O Teto de Existência)
* **Gribov (1978) / Zwanziger:** *Quantization of Non-Abelian Gauge Theories.* (A Restrição Geométrica)
* **Parisi-Wu (1981):** *Perturbation Theory Without Gauge Fixing.* (A Ferramenta Estocástica)
* **Dunne/Ünsal (2012+):** *Resurgence and Trans-series in QFT.* (A Conexão Matemática)
* **Hairer et al. (2025):** *Stochastic Quantization Rigor.* (A Nova Esperança Rigorosa)
