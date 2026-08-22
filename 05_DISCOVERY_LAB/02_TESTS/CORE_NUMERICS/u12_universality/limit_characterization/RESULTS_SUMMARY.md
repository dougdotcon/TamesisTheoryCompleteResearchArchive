# Resultados — frente `u12-limit-characterization` (onda 2, DISC-DEC-014)

**Data:** 2026-08-21. Pré-registro em `METHODOLOGY_NOTE.md` (gravado antes
de qualquer execução desta frente); derivação em `DERIVATION.md`;
execução única dos testes T1–T4 (`limit_sim.py`, `limit_sim.log`,
`limit_results.json`).

## VEREDITO

> **Forma fechada IDENTIFICADA e DERIVADA (não ajustada):**
>
> **φ_∞(c) = ∫₀¹ e^{−c t²} dt = (1/2)·√(π/c)·erf(√c)**
>
> Zero parâmetros livres. Derivada por argumento probabilístico exato
> (processo de exploração da trajetória + PGFL de Poisson, com um
> cancelamento exato que é a razão de existir forma fechada), verificada
> em ordem baixa por rota analítica independente, e aprovada em TODOS os
> critérios numéricos pré-registrados, incluindo grade held-out nunca
> medida pela onda 1. **Sinalizada para verificação adversarial em nível
> de orquestrador (obrigatória antes de catalogar).**

Corolário analítico: o "teorema" do arquivo `(1+c)^{−1/2}` fica refutado
também ANALITICAMENTE (não só numericamente): a série correta é
1 − c/3 + c²/10 − …, enquanto (1+c)^{−1/2} = 1 − c/2 + 3c²/8 − …
(primeira ordem já difere: 1/3 ≠ 1/2); a cauda correta é
(√π/2)·c^{−1/2} ≈ 0.8862·c^{−1/2} (correções apenas exponencialmente
pequenas), não 1·c^{−1/2}.

## O que é DERIVADO (categoria a)

1. **Forma fechada** φ_∞(c) = ∫₀¹e^{−ct²}dt (DERIVATION.md §1–4):
   P(ponto típico cíclico) via processo de exploração; taxas por unidade
   de massa percorrida t: fechamento-π em cada início de arco 1/(1−t),
   reroteamento c (terminal com prob. t); E[S(t)] = (1−t)e^{−ct²} pelo
   PGFL — o fator de cada reroteamento é (1−t) independente do instante
   (sobrevivência (1−s) cancela exatamente o hazard extra (1−t)/(1−s)).
2. **Série (inteira):** φ_∞(c) = Σ_k (−c)^k/(k!(2k+1))
   = 1 − c/3 + c²/10 − c³/42 + c⁴/216 − …
3. **Assintótica exata:** φ_∞(c) = (√π/2)c^{−1/2} − e^{−c}[1/(2c) − …];
   coeficiente da cauda A = √π/2 = 0.8862269255 (a onda 1 só sabia
   "~c^{−1/2}").
4. **Condicionais por-K:** φ_K = ∫₀¹(1−t²)^K dt = 4^K(K!)²/(2K+1)!
   (Wallis): 1, 2/3, 8/15, 16/35, 128/315, 256/693, …
5. **Checagem independente de 1ª ordem** (rota separada, via objeto
   PD(1) com 1 reroteamento, sem processo de exploração): φ₁ = 2/3 e
   a₁ = 1/3 exatos; e a densidade completa do caso K=1 é 2x em (0,1)
   (cálculo fechado em DERIVATION.md §5 + verificação manual da
   densidade), coincidindo com a predição do item 4.
6. **Massa livre:** E[massa de ciclos sem reroteamento] = (1−e^{−c})/c
   (size-biasing de PD(1)).

Ressalva honesta (DERIVATION.md §6): a passagem finita-n → contínuo do
processo de exploração é argumento de convergência de taxas padrão, não
formalizado em rigor total; é exatamente o elo controlado pelos dados
finitos da onda 1 (desvios estáveis até n = 64.000, χ² p = 0.09/0.58
contra o objeto contínuo).

## Validação numérica pré-registrada (execução única; tudo PASSOU)

| Teste | O quê | Resultado |
|---|---|---|
| T1 held-out (10 valores de c NUNCA medidos na onda 1: 0.05…100; N=200k/célula; seed 20260821) | χ²₁₀ = 14.22, **p = 0.163**, max\|z\| = 2.66 | **PASS** |
| T2 cross-check (grade da onda 1, sementes novas 31337) | χ²₇ = 5.68, **p = 0.578**, max\|z\| = 1.71 | **PASS** |
| T3 por-K (K=1..5, N=400k, seed 64206) | χ²₅ = 4.54, **p = 0.475**, max\|z\| = 1.25 | **PASS** |
| T4 decomposição (massa livre vs (1−e^{−c})/c) | max\|z\| = 2.11 | **PASS** |
| Global T1+T2 (17 células, 0 parâmetros ajustados) | χ²₁₇ = 19.90, **p = 0.279** | **PASS** |

Exemplos (MC vs forma): c=0.5: 0.855501±0.000523 vs 0.855624;
c=3: 0.504733±0.000558 vs 0.504344; c=100: 0.088775±0.000104 vs
0.088623. Consistência externa: os φ_∞ adversariais da onda 1
(`adv_continuum.json`, sementes/código independentes) também batem
célula a célula (max ~1.3σ em c=0.5).

## O que é CONJECTURA numericamente suportada (categoria b)

**Lei distribucional completa** da massa cíclica no limite:
M(c) =^d min(1, √(E/c)), E ~ Exp(1), i.e. P(M ≤ x) = 1 − e^{−cx²}
(x<1) com átomo e^{−c} em 1; condicional a K reroteamentos, densidade
2Kx(1−x²)^{K−1}. A MÉDIA disso é a forma derivada; a lei completa está
provada aqui só para K=1 e é conjectura para K≥2, suportada por testes
KS suplementares (pós-hoc, declarados: `supplementary_distribution.py`):
K=1: p=0.455; K=2: p=0.770; K=3: p=0.357; caso Poisson c=1: átomo
z=+0.33, KS contínuo p=0.171.

Nada nesta frente é "ajuste" (categoria c): não houve fitting de
parâmetros em momento algum.

## Identificação na literatura (checagem obrigatória — resultado)

O ensemble u12 pertence à família de "permutações corrompidas"
estudada por **Hansen & Jaworski, "Structural transition in random
mappings", Electronic Journal of Combinatorics 21(1) (2014), #P1.18**:
para o modelo deles com a defeitos fixos, o Teorema 7(ii) dá a densidade
limite 2ax(1−x²)^{a−1} para a fração cíclica — exatamente a nossa lei
condicional por-K (com a=K), cuja média ∫₀¹(1−t²)^a dt coincide com o
nosso φ_K (integração por partes; verificado). Ou seja: **a lei
condicional-K do limite u12 já era conhecida** (para um modelo
microscopicamente diferente — restrição de in-degree ≤ 2, modelo
anti-preferencial — mas com o mesmo limite), e o nosso resultado
identifica o limite u12 como a **mistura de Poisson(c)** dessa lei.
A forma erf/∫₀¹e^{−ct²}dt da mistura, a série, a cauda (√π/2)c^{−1/2} e
a caracterização M = min(1,√(E/c)) **não foram encontradas** publicadas
nas buscas realizadas (WebSearch, 5 consultas; termos e fontes no log da
sessão) — mas a busca não é exaustiva; a atribuição correta é: "caso
particular/mistura de Hansen–Jaworski 2014; forma fechada da mistura
possivelmente nova". O modelo relacionado de in-degrees intercambiáveis:
Hansen & Jaworski, Random Structures & Algorithms 33 (2008) 105–126.

Fontes: [EJC 21(1) #P1.18 (PDF)](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i1p18/pdf/),
[registro Heriot-Watt](https://researchportal.hw.ac.uk/en/publications/structural-transition-in-random-mappings/),
[RSA 2008 (exchangeable in-degrees)](https://onlinelibrary.wiley.com/doi/abs/10.1002/rsa.20187).

## Tabulação

`tabulation.json`: 70 valores de c ∈ [0.01, 1000] em precisão dupla
(erro relativo ≲1e−15 via erf), coeficientes exatos da série (frações),
φ_K exatos, assintótica. Valores-chave:
φ_∞(0.5)=0.855624391892; φ_∞(1)=0.746824132812; φ_∞(2)=0.598144006661;
φ_∞(5)=0.395712309611; φ_∞(10)=0.280247390507; φ_∞(20)=0.198166364830;
φ_∞(50)=0.125331413732; φ_∞(100)=0.088622692545.

## Escopo e limites

- Vale para o ensemble u12 e o observável fração cíclica no limite
  n→∞; nada aqui reabilita extrapolações do arquivo (Primes/Quantum
  Chaos/ToE), que permanecem fora de escopo/refutadas.
- Correções finitas-n (taxa de convergência) não foram caracterizadas
  nesta frente.
- **FLAG ADVERSARIAL: SIM** — forma fechada passou todos os critérios
  pré-declarados; verificação adversarial independente em nível de
  orquestrador é obrigatória antes de qualquer catalogação (sugestões
  para o adversário: re-derivar o cancelamento do §3 da DERIVATION.md;
  testar c intermediários novos, e.g. c∈{0.35, 4, 11, 45}; testar a
  predição distribucional min(1,√(E/c)) com sementes próprias; atacar a
  passagem finita-n→contínuo com n grande em c pequeno).

## Arquivos (todos nesta pasta)

- `METHODOLOGY_NOTE.md` — pré-registro (programa analítico/numérico +
  critérios de aceitação, antes de rodar).
- `DERIVATION.md` — derivação completa, passo a passo verificável.
- `limit_sim.py`, `limit_sim.log`, `limit_results.json` — T1–T4.
- `supplementary_distribution.py`, `.log`, `.json` — testes KS
  distribucionais (suplementares, pós-hoc declarados).
- `tabulation.json` — tabulação de alta precisão + série + assintótica.
