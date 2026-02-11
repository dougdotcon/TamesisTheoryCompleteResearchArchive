# PESQUISAS.MD: Análise Tática para o Roadmap Hodge

## 🧭 Visão Geral: O Que Estamos Buscando

Nosso objetivo no `ROADMAP_HODGE.md` é estabelecer a **Realizabilidade Estrutural de Ciclos Algébricos**. A Conjectura de Hodge não é apenas sobre a existência de subvariedades, mas sobre a consistência entre dois mundos de informação: o **Analítico (Hodge Classes)** que detecta topologia via integração, e o **Algébrico (Ciclos)** que constrói topologia via polinômios.

A tese do Roadmap é que classes de Hodge Racionais do tipo $(p,p)$ são **Estruturalmente Rígidas** o suficiente para forçar a existência de um "corpo" algébrico.

Filtragem estratégica da literatura:

1. **Cemitério (Tentativas Falhas):** A Conjectura de Hodge Integral (IHC), onde a torção aritmética destrói a ponte analítico-algébrica.
2. **Espelhos (Abordagens Adjacentes):** O Teorema (1,1) de Lefschetz (o caso que funciona) e a Teoria de Hodge Absoluta/Motivos (a generalização necessária).
3. **Arsenal (Ferramentas Locais):** Transversalidade de Griffiths e Loci de Hodge (Cattani-Deligne-Kaplan) como provas de rigidez.

---

## 💀 TIPO 1: Tentativas Sérias que Falharam (E Onde Exatamente Quebraram)

*Onde a "Analiticidade" falhou em capturar a "Aritmética".*

### 1.1 A Falha Integral (Atiyah-Hirzebruch, 1961)

* **A Tentativa:** Provar que toda classe de Hodge inteira vem de um ciclo algébrico.
* **Onde Quebrou:**
  * **Obstruções de Torção:** Atiyah e Hirzebruch usaram a K-Teoria Topológica e operações de Steenrod para mostrar que existem classes analíticas "fantasmas" que falham em testes de integridade aritmética módulo $p$.
  * A estrutura de Hodge (linear, espaços vetoriais sobre $\mathbb{C}$) é "cega" para a torção (aritmética finita).
* **Lição para o Roadmap:**
  * ❌ **Não tentar:** Resolver a conjectura para coeficientes inteiros ($\mathbb{Z}$). Isso é falso.
  * ✅ **Fazer:** Focar estritamente em coeficientes Racionais ($\mathbb{Q}$). A racionalidade elimina a torção e é o requisito mínimo para a "Rigidez" que buscamos.

### 1.2 O Contra-Exemplo de Kollár (1990)

* **A Tentativa:** Salvar a conjectura integral em dimensão baixa ou para classes sem torção.
* **Onde Quebrou:**
  * Kollár usou degenerações de hipersuperfícies para mostrar que mesmo classes livres de torção podem falhar em ser algébricas se a "geometria local" na singularidade exigir coeficientes fracionários.
* **Lição Tática:**
  * A algebricidade é uma propriedade global rígida. O "Compiler" analítico-algébrico falha se não tivermos a precisão infinita dos racionais.

### 1.3 Variedades Abelianas e Enriques (Benoist-Ottem, Engel)

* **A Falha Recente (2020-2025):** Demonstrações de que a IHC falha até em variedades Abelianas muito gerais. Isso confirma que a estrutura analítica sozinha é insuficiente para capturar toda a nuance aritmética, reforçando a necessidade de Motivos/Galois para uma descrição completa.

---

## 🌌 TIPO 2: Abordagens Estruturais Adjacentes (O Mesmo Espírito)

*Onde a ponte funciona ou é generalizada.*

### 2.1 O Teorema de Lefschetz (1,1)

* **Conceito:** Para $p=1$ (divisores), a Conjectura de Hodge é verdadeira.
* **Conexão com o Roadmap:**
  * Funciona porque temos a exponencial $H^1(X, \mathcal{O}^*) \to H^2(X, \mathbb{Z})$. Isso nos dá a ferramenta de construção (Fibrados Lineares).
  * Para $p > 1$, não existe essa ferramenta direta. Nosso roadmap tenta substituir essa falta de ferramenta construtiva por um argumento de **Rigidez Deformacional**.

### 2.2 Algebraidade do Locus de Hodge (Cattani-Deligne-Kaplan, 1995)

* **Conceito:** O subconjunto do espaço de moduli onde uma classe de cohomologia se torna uma classe de Hodge é uma subvariedade algébrica.
* **Conexão com o Roadmap:**
  * **Prova da Rigidez:** Este é o teorema mais forte a nosso favor. Ele diz que "ser Hodge" é uma condição algébrica, não apenas analítica transcendental arbitrária.
  * Se o lugar onde a classe "vive" é algébrico, isso sugere que a classe em si tem natureza algébrica. Usaremos isso para argumentar que classes de Hodge racionais não podem ser "fantasmas" transcendentais.

### 2.3 Teoria dos Motivos (Grothendieck / Voevodsky)

* **Conceito:** Uma categoria universal de "peças geométricas" que unifica Betti, de Rham e l-ádico.
* **Conexão com o Roadmap:**
  * Reinterpreta a Conjectura de Hodge como a "sobrejetividade do mapa de realização".
  * Embora abstrata, a teoria fornece a estrutura (Conjecturas Padrão) onde a nossa "Realizabilidade Estrutural" deve habitar.

---

## 🛠️ TIPO 3: Ferramentas Técnicas Locais (O Arsenal)

*Componentes para o `PAPER_B`.*

### 3.1 Transversalidade de Griffiths

* **Origem:** Variação de Estruturas de Hodge (VHS).
* **Uso Tático:**
  * A filtração de Hodge $F^p$ satisfaz $\nabla F^p \subset F^{p-1} \otimes \Omega^1$.
  * Isso impõe uma **restrição diferencial** severa sobre como as classes de Hodge podem se mover.
  * Argumento de Censura: Classes "fantasmas" (não algébricas) violariam essa transversalidade ao serem deformadas, ou teriam que ser localmente constantes (o que contradiz a geometria de variedades gerais). A transversalidade é o "policial" que força a algebricidade.

### 3.2 Funções Normais e Singularidades (Green-Griffiths)

* **Origem:** Estudo do Jacobiano Intermediário $J^k(X)$.
* **Uso Tático:**
  * Uma classe de Hodge induz uma "Função Normal" $\nu$.
  * Se a classe é algébrica, $\nu$ tem singularidades específicas e controladas.
  * Podemos usar isso como um teste de detecção: "Se tem cara de algébrico e cheiro de algébrico (singularidades corretas), então é algébrico".

### 3.3 Spread e Ciclos Absolutos

* **Origem:** Voisin, Deligne.
* **Uso Tático:**
  * O conceito de "Spread": estender uma classe de Hodge definida em uma variedade complexa para uma variedade definida sobre um corpo numérico.
  * Se uma classe $(p,p)$ é consistente sob a ação do grupo de Galois (Hodge Absoluto), ela é uma candidata forte a ser Motívica (algébrica).

---

## 📉 Síntese para o Roadmap

O `GUN-HODGE` reestruturado clarifica a estratégia do **Structural Realizability**:

1. **Fugir da Aritmética:** A falha da IHC (Tipo 1) nos ensina a ignorar coeficientes inteiros. A batalha é sobre $\mathbb{Q}$.
2. **Apostar na Rigidez:** O Teorema de Cattani-Deligne-Kaplan (Tipo 2.2) e a Transversalidade de Griffiths (Tipo 3.1) são as evidências de que classes de Hodge não são objetos suaves arbitrários; elas estão "travadas" em estruturas algébricas.
3. **O Salto de Fé Lógico:** O gap final é provar que essa Rigidez Analítica implica Existência Geométrica. O Roadmap propõe fechar isso tratando a "Não-Algebraicidade" como uma instabilidade estrutural proibida para classes racionais.

**Próxima Ação:** Utilizar a noção de **Transversalidade** como o mecanismo principal de "Censura" para classes fantasmas no `PAPER_B`.

---

### Referências Selecionadas

* **Hodge (1950):** *The Topological Invariant...* (A Origem)
* **Atiyah, Hirzebruch (1961):** *Vector bundles and homogeneous spaces.* (O Cemitério Integral)
* **Griffiths (1968):** *Periods of integrals...* (A Transversalidade)
* **Deligne (1971):** *Théorie de Hodge I, II, III.* (A Estrutura de Pesos)
* **Cattani, Deligne, Kaplan (1995):** *On the locus of Hodge classes.* (A Prova de Rigidez)
* **Voisin (2002+):** *Hodge Theory and Complex Algebraic Geometry.* (A Bíblia Moderna)
* **Totaro (1997):** *Torsion algebraic cycles.* (Refinamento da Falha)
