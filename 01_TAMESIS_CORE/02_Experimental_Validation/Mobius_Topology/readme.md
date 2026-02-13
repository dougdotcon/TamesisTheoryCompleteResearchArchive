# Experimento de Topologia de Möbius — Validação TAMESIS

[![Status](https://img.shields.io/badge/Status-Active_Research-00C853?style=for-the-badge)](.)
[![Type](https://img.shields.io/badge/Type-Topological_Validation-8B5CF6?style=for-the-badge)](.)
[![Pillar](https://img.shields.io/badge/Pillar-TRI_+_TDTR_+_Kernel_v3-FF6B6B?style=for-the-badge)](.)

> *"A não-orientabilidade não é uma curiosidade geométrica — é a assinatura topológica de um regime quântico encapsulado dentro do regime clássico."*

---

## 1. Motivação

A Fita de Möbius é a superfície não-orientável mais simples que existe. Ela possui:

- **1 lado** (percorra com o dedo — você cobre toda a superfície sem levantar)
- **1 borda** (1 contorno único)
- **Característica de Euler:** $\chi = 0$

Quando **cortada**, ela revela fenômenos topológicos que são análogos diretos aos pilares da Teoria TAMESIS:

- Transições de regime irreversíveis (TDTR)
- Regimes aninhados e incompatíveis (TRI)
- Transições de fase no grafo entrópico (Kernel v3)

---

## 2. Protocolo Experimental (Papel)

### Material Necessário

| Item | Quantidade | Observação |
|:-----|:-----------|:-----------|
| Papel A4 | 3 folhas | Cortar tiras de ~30cm × 3cm |
| Tesoura | 1 | Fina, para cortes precisos |
| Fita adesiva | 1 rolo | Para unir as extremidades |
| Caneta/lápis | 1 | Para marcar linhas de corte |
| Régua | 1 | Para marcar 1/2 e 1/3 da largura |

---

### Experimento A: Corte no Centro (1/2 da largura)

![Priority](https://img.shields.io/badge/Dificuldade-Fácil-00C853?style=flat-square)

**Construção:**

1. Corte uma tira de papel de ~30cm × 3cm
2. Segure as duas extremidades
3. Dê **meia torção** (180°) em uma extremidade
4. Cole as extremidades com fita adesiva → **Fita de Möbius**
5. Verifique: percorra com o dedo — deve cobrir "ambos os lados" sem levantar

**Corte:**

1. Com a caneta, trace uma linha no **centro exato** da largura (1.5cm de cada borda)
2. A linha deve percorrer toda a fita — quando você completar, a linha se fecha sozinha
3. Corte ao longo dessa linha com a tesoura

**Resultado Esperado:**

| Propriedade | Antes do Corte | Depois do Corte |
|:------------|:---------------|:----------------|
| Número de peças | 1 | **1 (NÃO separa!)** |
| Comprimento | L | **2L** (dobro!) |
| Largura | W | W/2 |
| Torções | 1 meia-torção | **4 meias-torções (2 torções completas)** |
| Orientabilidade | Não-orientável | **Orientável (2 lados)** |
| Bordas | 1 | **2** |

> **Surpresa:** A fita não se divide! Ela se torna uma fita única MAIOR com 2 torções completas. Isso acontece porque a linha central percorre a fita DUAS VEZES antes de se fechar (devido à meia-torção).

---

### Experimento B: Corte Fora do Centro (1/3 da largura)

![Priority](https://img.shields.io/badge/Dificuldade-Médio-FFC107?style=flat-square)

**Construção:**

1. Construa uma NOVA fita de Möbius (mesma técnica do Experimento A)

**Corte:**

1. Com a régua, marque uma linha a **1/3 da largura** (1cm da borda, se a largura é 3cm)
2. A linha deve percorrer toda a fita
3. Corte ao longo dessa linha

**Resultado Esperado:**

| Propriedade | Fita Estreita | Fita Larga |
|:------------|:--------------|:-----------|
| Tipo | **Fita de Möbius** | **Fita com 2 torções** |
| Largura | W/3 | 2W/3 (reduzido) |
| Comprimento | L (original) | **2L** (dobro!) |
| Orientabilidade | **Não-orientável** | **Orientável** |
| Torções | 1 meia-torção | 4 meias-torções |

> **Surpresa Maior:** As duas fitas estão **ENTRELAÇADAS** — uma dentro da outra! Elas são topologicamente inseparáveis sem cortar. A fita estreita é uma nova Fita de Möbius (não-orientável), e a fita larga é orientável com 2 torções completas.

---

### Experimento C: Cortes Recursivos (Avançado)

![Priority](https://img.shields.io/badge/Dificuldade-Avançado-FF6B6B?style=flat-square)

**Protocolo:**

1. Após o Experimento A, pegue a fita resultante (2 torções completas)
2. Corte-a novamente no centro
3. **Resultado:** Duas fitas com 2 torções, entrelaçadas

**Questão TAMESIS:** A recursão de cortes é uma **cascata de transições de regime**. Cada corte produz mais estrutura — análogo ao aumento de entropia durante a expansão do universo.

---

## 3. Análise Topológica Formal

### Teorema de Möbius (Corte Central)

Seja $M$ uma fita de Möbius com $n$ meias-torções (onde $n$ é ímpar para ser não-orientável).

**Corte no centro:**

$$M_{n} \xrightarrow{\text{corte}_{1/2}} S_{2n}$$

Onde $S_{2n}$ é uma fita única com $2n$ meias-torções.

- Se $n = 1$: $M_1 \to S_2$ (1 Möbius → 1 fita com 2 meias-torções)
- Se $n = 3$: $M_3 \to S_6$ (3 meias-torções → 6 meias-torções)

**Corte fora do centro ($p/q$ da largura, $p < q$):**

$$M_{n} \xrightarrow{\text{corte}_{p/q}} M_{n} \sqcup S_{2n}$$

Produz a **união disjunta** de uma Möbius com $n$ meias-torções e uma fita orientável com $2n$ meias-torções, **conectadas por linking number** $|Lk| = 1$.

### Invariantes Topológicos

| Invariante | Möbius Original | Corte Central | Corte 1/3 (estreita) | Corte 1/3 (larga) |
|:-----------|:----------------|:--------------|:----------------------|:-------------------|
| $\chi$ (Euler) | 0 | 0 | 0 | 0 |
| Orientável? | Não | **Sim** | **Não** | **Sim** |
| Bordas | 1 | 2 | 1 | 2 |
| Gênero | — | 0 | — | 0 |
| Meias-torções | 1 | 4 | 1 | 4 |
| Linking Number | — | — | 1 (com a outra) | 1 (com a outra) |

---

## 4. Interpretação TAMESIS: Cinco Insights Fundamentais

### Insight 1: Aninhamento de Regimes (TRI)

![Pillar](https://img.shields.io/badge/Pilar-TRI-FF6B6B?style=flat-square)

O corte fora do centro (1/3) revela uma **estrutura de regimes aninhados**:

- A fita estreita (Möbius) = **Regime Quântico** (não-orientável, sem "acima/abaixo" definido)
- A fita larga (2 torções) = **Regime Clássico** (orientável, com direção definida)
- Elas estão **topologicamente ligadas** — inseparáveis, mas **incompatíveis**

> **Leitura TRI:** Os regimes quântico e clássico coexistem no universo como a fita de Möbius e a fita orientável — conectados pela mesma fronteira, mas com propriedades topológicas mutuamente exclusivas. Você não pode "alisar" a fita de Möbius em uma fita orientável sem cortá-la — assim como não pode unificar QM e GR sem uma transição de regime.

### Insight 2: Irreversibilidade Estrutural (TDTR)

![Pillar](https://img.shields.io/badge/Pilar-TDTR-2196F3?style=flat-square)

O ato de cortar é uma **operação de semigrupo**: irreversível.

$$\text{Cortar}: M \to S \quad \text{(existe)}$$
$$\text{Descortar}: S \to M \quad \text{(NÃO existe)}$$

Isso é formalmente análogo ao **Teorema da Irreversibilidade Estrutural** de TDTR: transições de regime formam um semigrupo, não um grupo. Você não pode "dequantizar" um sistema clássico de volta ao regime quântico.

> **A Flecha do Tempo Topológica:** Antes do corte, o sistema tem 1 borda e 1 lado. Depois, tem 2 bordas e 2 lados. A informação topológica aumentou (mais estrutura), mas a não-orientabilidade original foi destruída de forma irreversível no componente cortado. Isso espelha o aumento de entropia.

### Insight 3: Transição de Fase (Kernel v3)

![Pillar](https://img.shields.io/badge/Pilar-Kernel_v3-8B5CF6?style=flat-square)

No modelo Kernel v3, o universo é um **Grafo Causal** que sofre transições de fase. O corte da fita de Möbius é uma transição de fase topológica:

| Propriedade | Antes (Fase I) | Depois (Fase II) |
|:------------|:---------------|:-----------------|
| Topologia | Não-orientável | Orientável |
| Conectividade | 1 componente | 1 ou 2 componentes |
| Simetria | Alta (Z₂) | Quebrada |
| Entropia | Baixa (simples) | Alta (complexa) |

> **Analogia ao Big Bounce:** O corte é como o instante $t = 0$. A transição de fase não destrói a informação — ela a **reorganiza** em uma topologia diferente. A fita resultante "lembra" a torção original (carrega 2 torções como memória da Möbius original).

### Insight 4: Quebra de Simetria

![Pillar](https://img.shields.io/badge/Pilar-Simetria-FFC107?style=flat-square)

- **Corte no centro:** Preserva a simetria Z₂ da fita (ambos os lados do corte são equivalentes) → resultado simétrico (1 fita)
- **Corte fora do centro:** **Quebra a simetria Z₂** → resultado assimétrico (2 fitas com propriedades diferentes)

> **Leitura TAMESIS:** A quebra de simetria gera MAIS estrutura. Isso é análogo à quebra espontânea de simetria eletrofraca: quando a simetria SU(2) × U(1) é quebrada, surgem partículas com massas diferentes (W, Z, fóton). O corte assimétrico da Möbius produz dois objetos topologicamente distintos onde antes havia um.

### Insight 5: Emaranhamento Topológico

![Pillar](https://img.shields.io/badge/Pilar-Entrelaçamento-00BCD4?style=flat-square)

As duas fitas produzidas pelo corte fora do centro estão **topologicamente entrelaçadas** com Linking Number = 1. Isso significa:

- Elas **não podem ser separadas** sem cortar
- Cada uma "sabe" da existência da outra
- A informação sobre o vínculo está **não-localmente distribuída**

> **Analogia ao Emaranhamento Quântico:** Assim como dois qubits emaranhados são inseparáveis no estado $|\Psi\rangle = \frac{1}{\sqrt{2}}(|01\rangle + |10\rangle)$, as duas fitas compartilham informação topológica que não pode ser localizada em nenhuma delas individualmente. O linking number é o "invariante de emaranhamento" topológico.

---

## 5. Conexão com Trabalho Existente

Este experimento estende o trabalho já realizado em:

| Arquivo | Conexão |
|:--------|:--------|
| `mobius_spinor.py` | Demonstra spin-1/2 como vetor percorrendo a Möbius (720° para retorno). O corte mostra o que acontece quando essa topologia é "quebrada" |
| `dirac_belt_trick.py` | O truque do cinto de Dirac mostra a mesma topologia SO(3) vs SU(2). O corte revela a estrutura interna |
| `topology_comparison.png` | Esfera (escalar) vs Toro (spinor). O corte da Möbius demonstra a transição entre esses regimes |

---

## 6. Previsões e Questões Abertas

### Previsão 1: Cascata de Cortes

Cortes recursivos no centro produzem uma **cascata exponencial**:

| Geração | N° de fitas | Meias-torções | Entrelaçadas? |
|:---------|:-----------|:--------------|:-------------|
| 0 | 1 (Möbius) | 1 | — |
| 1 (centro) | 1 | 4 | — |
| 2 (centro) | 2 | 4 cada | Sim |
| 3 (centro) | 4 | 4 cada | Sim (complexo) |

**Questão:** A complexidade do entrelaçamento segue uma lei de escala? Isso poderia mapear para o crescimento de entropia no Kernel v3.

### Previsão 2: Corte com N Meias-Torções

| Meias-torções | Corte Central | Resultado |
|:-------------|:-------------|:---------|
| 1 (Möbius) | Centro | 1 fita, 4 meias-torções |
| 2 (cilindro torcido) | Centro | 2 fitas separadas, 2 meias-torções cada |
| 3 | Centro | 1 fita, 6 meias-torções |
| 4 | Centro | 2 fitas separadas, 4 meias-torções cada |

**Padrão:** Torções ÍMPARES → 1 fita (não separa). Torções PARES → 2 fitas separadas.

> **Leitura TAMESIS:** Sistemas com topologia ímpar (fermions, spin 1/2) são **resistentes à fragmentação** — mantêm-se conectados sob perturbação. Sistemas com topologia par (bosons, spin inteiro) se fragmentam. Isso é exatamente a diferença entre férmions e bósons!

### Questão Aberta

> **Pergunta de Pesquisa:** Se construirmos uma "Garrafa de Klein" (Möbius em 2D fechada) e cortarmos, o que acontece? Existem análogos tridimensionais que mapeiam para as transições de regime?

---

## 7. Simulação Computacional

Execute o script Python para visualização:

```bash
python mobius_cutting_simulation.py
```

**Outputs:**

- `mobius_original.png` — Fita de Möbius original com linhas de corte
- `mobius_center_cut.png` — Resultado do corte central
- `mobius_offcenter_cut.png` — Resultado do corte fora do centro
- `mobius_topology_summary.png` — Resumo comparativo

---

## 8. Referências

1. Fulber, D.H.M. *Topological Origin of Spin* (TAMESIS Research, 2026)
2. Listing, J.B. *Vorstudien zur Topologie* (1847) — Primeira descrição da fita de Möbius
3. Möbius, A.F. *Über die Bestimmung des Inhaltes eines Polyeders* (1858)
4. Starostin, E.L. & van der Heijden, G.H.M. *The shape of a Möbius strip* (Nature Materials, 2007)
5. Tanda, S. et al. *A Möbius strip of single crystals* (Nature, 2002)

---

*Programa de Pesquisa Tamesis*
*"O corte é a transição. A topologia é memória."*
