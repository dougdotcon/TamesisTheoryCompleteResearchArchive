# Nota de metodologia — frente `u12-universality` (linha DISC-CORE-NUMERICS-001, DISC-DEC-013)

**Status:** decisões metodológicas fixadas ANTES de qualquer computação
de reprodução. Nenhum número desta frente foi calculado antes da data e
hora de gravação deste arquivo (2026-08-21). Implementação de reprodução
é INDEPENDENTE (do zero); o código do arquivo (`final_verification.py`,
`step1_random_map_family.py`, `stage_34_2/34_3`) foi LIDO para fixar a
definição operacional, mas NÃO será reutilizado na computação primária.
Comparação posterior contra o código do arquivo é permitida apenas como
diagnóstico, nunca como resultado primário.

## 1. A alegação sob teste (SOURCES — citações literais com file:line)

A alegação "classe de universalidade U_1/2" tem três componentes
quantitativos e um componente de distinção de classes:

### (A) Lei de escala φ(c) = (1+c)^(-1/2)

`01_TAMESIS_CORE/06_Universality_Discovery/Closure_Paper/paper.html:315-322`:

> "Theorem (U_1/2 Universality) — For the family of perturbed
> permutations with $\epsilon = 1 - c/n$, the expected fraction of
> elements in cycles satisfies:
> $$\lim_{n \to \infty} \mathbb{E}\left[\frac{\text{elements in
> cycles}}{n}\right] = (1 + c)^{-1/2}$$"

`01_TAMESIS_CORE/RESEARCH_RESULTS.md:628`:

> `$$\boxed{\phi(c) = (1 + c)^{-1/2}}$$`

`01_TAMESIS_CORE/06_Universality_Discovery/U12_Discovery/DISCOVERY_SUMMARY.md:553-557`:

> "Para qualquer familia de funcoes f_epsilon: [n] -> [n] que interpola
> entre permutacao (epsilon=1) e random map (epsilon=0) com
> epsilon = 1 - c/n, vale no limite n -> infinito:
> phi(c) = lim_{n->inf} E[pontos em ciclos] / n = (1 + c)^{-1/2}"

### (B) Expoente medido α = 0.508 ± 0.033

`01_TAMESIS_CORE/RESEARCH_RESULTS.md:634`:

> `| Exponent α | **0.508 ± 0.033** (consistent with 0.5) |`

`01_TAMESIS_CORE/06_Universality_Discovery/Closure_Paper/paper.html:374`:

> "Fitted exponent: $\alpha = 0.508 \pm 0.033$ (expected: 0.500)"

Protocolo de medição do arquivo (para espelhamento):
`01_TAMESIS_CORE/06_Universality_Discovery/Regime_Transitions/Physical_Tests/final_verification.py:108-141`
— grade `n ∈ {500,1000,2000}`, `c ∈ {0.5,1,2,5,10,20,50}`, 30 amostras
por célula, ajuste `curve_fit` NÃO ponderado do modelo
`(1+c)**(-alpha)` usando SOMENTE as células n=2000. (Nota de auditoria:
o arquivo `final_verification.py` contém um `e` solto na linha 25, que
levanta `NameError` na execução do módulo — o script como está gravado
NÃO executa sem edição; e nenhum script da cadeia U_1/2 fixa seed.
Logo o número 0.508±0.033 não é regenerável bit a bit a partir do
repositório; só é testável estatisticamente, como feito aqui.)

### (C) Gap espectral gap(n) = 2/n

`01_TAMESIS_CORE/RESEARCH_RESULTS.md:637`:

> `$$gap(n) = \frac{2}{n}, \quad \lambda_2 = \frac{n-2}{n}$$`

`01_TAMESIS_CORE/06_Universality_Discovery/U12_Discovery/DISCOVERY_SUMMARY.md:22-25`:

> "Stage 34.3: Analise Espectral — Descoberta principal:
> gap(n) = 2/n (EXATO), lambda_2 = (n-2)/n"

Objeto: operador de transferência de UMA partição de quicksort com
pivô uniforme em S_n
(`01_TAMESIS_CORE/06_Universality_Discovery/U12_Discovery/stages/stage_34_2_operator.py:296-349`:
"L[i, j] = P(obter permutacao i | comecando com permutacao j, uma
particao)"; pivô escolhido uniformemente entre as n posições,
`prob = 1.0 / self.n`, linha 345). Gap definido como
`|lambda_1| - |lambda_2|` com autovalores ordenados por módulo
(`stage_34_3_spectral_analysis.py:70-72`). Hipótese enunciada em
`stage_34_3_spectral_analysis.py:11-17`.

### (D) Distinção das classes concorrentes do Atlas

`01_TAMESIS_CORE/RESEARCH_RESULTS.md:662-668` (Universality Atlas):

> `| U₀ | Θ(c - c*) | Threshold/percolation | Phase transitions |`
> `| U₁/₂ | (1 + c)⁻¹/² | Discrete-to-random | Randomized algorithms |`
> `| U₁ | e⁻ᶜ | Exponential decay | Radioactive decay |`
> `| U₂ | (1 + c)⁻² | Lindblad decoherence | Quantum systems |`
> `| U_∞ | 1/(1 + cⁿ) | Multi-threshold | Complex systems |`

Também `01_TAMESIS_CORE/06_Universality_Discovery/Universality_Atlas/atlas.py:8-12`.

### Menções correlatas (contexto, não objeto primário)

- `RECURSOS_PARA_PESQUISA/REAL_DISCOVERIES.md:63-64`: "The $U_{1/2}$
  Universality Class: Identified a new universality class with exponent
  $\alpha = 1/2$ governing systems at the threshold of randomization
  (Primes, Quantum Chaos)." — NOTA: a extensão a "Primes, Quantum
  Chaos" NÃO é suportada pelos próprios arquivos primários (que
  restringem a classe a perturbações Bernoulli(c/n) uniformes e
  independentes, axiomas U1-U3 em `DISCOVERY_SUMMARY.md:705-732`);
  esta extensão NÃO está sob teste aqui.
- `RELATORIO_LEIS_DE_POTENCIA_E_CLASSIFICACAO_DE_SISTEMAS.md:16,50,56`:
  usa U12 como exemplo metodológico (`~(1/2)log(n)+γ` ciclos de random
  maps vs `n/log(n)` primos). A lei `E[ciclos] ~ (1/2)log n + γ` para
  random maps puros é resultado CLÁSSICO da literatura (o próprio
  arquivo cita Flajolet–Odlyzko em `DISCOVERY_SUMMARY.md:195-197`), não
  descoberta do arquivo; será verificada apenas como sanity check
  secundário.

## 2. Definição operacional pinada (o que será simulado)

O objeto matemático está SUFICIENTEMENTE especificado nas fontes para
reprodução. Definição operacional (extraída de
`final_verification.py:36-57` e `step1_random_map_family.py:53-69`,
ambas construções idênticas):

1. `π` = permutação uniforme de `{0,...,n-1}`.
2. Para cada `i` independentemente: com probabilidade `p = c/n`,
   `f(i) = Uniform{0,...,n-1}` (com reposição, pode inclusive
   coincidir com `π(i)`); caso contrário `f(i) = π(i)`.
3. Observável: `φ = (número de pontos cíclicos do grafo funcional de
   f)/n`, onde ponto cíclico = pertence a um ciclo (equivalente:
   sobrevive à remoção iterada de nós sem pré-imagem).

Alegação (A): `E[φ] → (1+c)^{-1/2}` quando `n → ∞`, com `c` fixo.

## 3. Plano de reprodução (implementação própria, do zero)

Linguagem: Python 3 + numpy (algoritmo de contagem de pontos cíclicos:
peeling de Kahn por grau de entrada, O(n) por amostra — implementação
própria, diferente da caminhada com `path.index` do arquivo).

### Protocolo A1 — grade primária

- RNG: `numpy.random.default_rng` com `SeedSequence(20260821)`,
  substreams derivados por `spawn` — um substream por célula `(n, c)`.
- Grade: `n ∈ {500, 1000, 2000, 4000}`, `c ∈ {0.5, 1, 2, 5, 10, 20,
  50}` (mesma grade de c do arquivo, + n=4000 para limite maior),
  `N = 200` amostras por célula (vs 30 do arquivo — SEM menor).
- Registrar `φ̄(n,c)`, desvio padrão e SEM por célula (JSON).

### Protocolo A2 — ajuste do expoente

- **Fit-espelho:** mínimos quadrados não ponderados de
  `φ = (1+c)^{-α}` sobre as 7 células `n=2000` (espelha exatamente o
  protocolo de `final_verification.py:134-141` que gerou 0.508±0.033).
  Incerteza: σ do `curve_fit` E bootstrap não paramétrico sobre as 200
  amostras por célula (B=2000 réplicas de ajuste); reporta-se o IC 95%
  bootstrap (percentil).
- **Fit-limite:** idem sobre as células `n=4000`, ponderado por SEM.

### Protocolo C — gap espectral (independente)

- Implementação própria do operador de uma partição com pivô uniforme
  em S_n (matriz n!×n!, estocástica por coluna), `n ∈ {3,4,5,6,7}`.
- Autovalores por `numpy.linalg.eig`; ordenar por módulo;
  `gap = |λ_1| - |λ_2|`.

## 4. Critérios de decisão (PRÉ-DECLARADOS)

### R1 — "reproduzido" (componentes A e B)

Declara-se **reproduzido** se e somente se TODAS as condições:

- **R1a:** IC 95% do Fit-espelho contém 0.5 OU o ajuste central desvia
  de 0.5 por menos de 0.05 (o próprio critério declarado do arquivo em
  `final_verification.py:147-152`); E o IC 95% do Fit-espelho tem
  interseção não vazia com [0.475, 0.541] (= 0.508 ± 0.033).
- **R1b:** erro absoluto médio `|φ̄ − (1+c)^{-1/2}|` sobre todas as 28
  células da grade A1 é < 0.05 (limiar que o próprio arquivo usa,
  `final_verification.py:172`).
- **R1c (limite):** no Fit-limite (n=4000), IC 95% contém 0.5.

Se R1a/R1b passam mas R1c falha, o veredito é "reproduzido no
protocolo do arquivo, mas o limite n→∞ é questionável" (documentar).

### R2 — "distinto das classes concorrentes" (componente D)

Dados: as 7 células `n=4000` (φ̄ ± SEM). Modelos ajustados aos MESMOS
dados por mínimos quadrados ponderados (1/SEM²):

| Classe | Forma pré-declarada | Parâmetros livres |
|---|---|---|
| U_1/2 (fixa) | `(1+c)^{-1/2}` | 0 |
| U_1/2 (livre) | `(1+c)^{-α}` | 1 (α) |
| U_0 threshold | `1` se `c<c*`, `b` se `c≥c*` | 2 (c*, b) |
| U_1 exponencial | `exp(-λc)` | 1 (λ) |
| U_2 Lindblad | `(1+βc)^{-2}` | 1 (β) |
| U_∞ multi-threshold | `1/(1+c^m)` | 1 (m) |

(As versões com parâmetro livre são GENEROSAS com as concorrentes: as
formas literais do Atlas, `e^{-c}` e `(1+c)^{-2}`, também serão
reportadas, mas o critério usa as versões com escala livre.)

Estatística: `χ² = Σ ((φ̄ − modelo)/SEM)²`; `AIC = χ² + 2k`.

Declara-se **distinto** se e somente se `AIC(U_1/2 fixa)` é MENOR que
o AIC de CADA forma concorrente (U_0, U_1, U_2, U_∞, nas versões
livres) por `ΔAIC ≥ 10`. Concorrente com `ΔAIC < 10` ⇒ "não distinto
dessa classe como formulado" (nomeando-a).

### R3 — gap(n) = 2/n (componente C)

Declara-se **reproduzido (exato)** se, para todos `n ∈ {3,...,7}`:
`| |λ_2| − (n−2)/n | < 1e−8` e `|gap − 2/n| < 1e−8`.
(Alegação é de identidade algébrica exata; tolerância só cobre erro de
ponto flutuante.)

### Regra de sobrevivência (item 4 da disciplina)

Se R1 E R2 passam: recomputar com **segundo conjunto de seeds**
(`SeedSequence(777)`) e **grades diferentes** — `n ∈ {300, 800, 3000}`,
`c ∈ {0.3, 0.7, 1.5, 3, 7, 15, 30}`, `N = 300` — repetindo R1b/R1c/R2
na nova grade; e SINALIZAR reprodução adversarial de nível
orquestrador no relatório final.

### Limites do veredito

Veredito máximo possível: "reproduzido / não reproduzido; distinto /
não distinto das classes concorrentes como formulado" — para ESTE
ensemble (permutação perturbada Bernoulli(c/n) uniforme) e ESTE
observável (fração de pontos cíclicos). Nada aqui valida ou refuta as
extrapolações do arquivo a "Primes, Quantum Chaos", física de
Lindblad, ou qualquer conexão Tamesis/ToE (a ToE já está refutada pelo
próprio arquivo, `ToE_Refutation/FINAL_VERDICT.md`).

Máximo de um adendo datado a esta nota, se correção for necessária.

*Frente u12-universality — 2026-08-21 — gravado antes de qualquer
computação de reprodução.*
