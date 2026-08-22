# Veredito adversarial — frente u12-limit-characterization (wave 2, DISC-DEC-014)

**Agente:** verificação ADVERSARIAL independente. **Data:** 2026-08-21.
**Disciplina cumprida:** plano + seeds pré-registrados em
`ADVERSARIAL_NOTE.md`; derivação analítica própria feita À MÃO e gravada
na nota ANTES de qualquer execução; todos os números próprios travados em
JSON ANTES da leitura de `DERIVATION.md` / `limit_sim.py` /
`RESULTS_SUMMARY.md` / `METHODOLOGY_NOTE.md` da frente (ordem verificável
nos timestamps). Implementações 100% próprias, seeds próprias, valores de
c frescos (0.37, e=2.71828, 7.5, 23 — fora de qualquer grade anterior).

## Alegação atacada

φ_∞(c) = ∫₀¹ e^{−ct²} dt = (1/2)√(π/c)·erf(√c); série Σ(−c)^k/(k!(2k+1))
(a₁ = 1/3); cauda (√π/2)c^{−1/2}; condicional φ_K = 4^K(K!)²/(2K+1)!;
conexão com Hansen & Jaworski, EJC 21(1) (2014) #P1.18, Teorema 7(ii).

## VEREDITOS POR SUPERFÍCIE

### (a) Força bruta exata em n pequeno — **CONFIRMADO**

Enumeração EXATA (sem amostragem) sobre todos os n^n mapas com peso
analítico sobre π (validada por dupla implementação: soma tripla direta
permutações×subconjuntos×destinos em n=4, concordância < 3e−16; e
reproduz os exatos da wave 1: c=0.5 → 0.862638/0.859539/0.857945 em
n=4/5/6). n ∈ {4,5,6,7}, c ∈ {0.5,1,2,3} (`adv2_exact.py/.json`):

| c | exato n=7 | extrap. A+B/n+C/n² | forma alegada | extrap − alegada |
|---|---|---|---|---|
| 0.5 | 0.857038 | 0.855653 | 0.855624 | +0.000029 |
| 1.0 | 0.748352 | 0.746895 | 0.746824 | +0.000071 |
| 2.0 | 0.603609 | 0.598553 | 0.598144 | +0.000409 |
| 3.0 | 0.520855 | 0.506009 | 0.504344 | +0.001666 |

Desvios exatos estritamente decrescentes em n em todas as c; a
extrapolação de 4 pontos aterrissa na forma alegada (resíduo cresce com
c porque o alcance n≤7 é curto para c grande — direção e magnitude
coerentes, critério pré-declarado < 0.005 satisfeito em c ≤ 2).

**Bônus discriminante (a₁):** com exatos em c ∈ {0.0625, 0.125, 0.25}
(`adv2_extrap.py`), o coeficiente linear a₁(n) extrapola para
**0.333325** (alvo 1/3 = 0.333333; forma antiga do arquivo daria 1/2).
Os valores exatos seguem o padrão limpo **a₁(n) = (n²−1)/(3n²)**
(desvios de 1/3: 1/48, 1/75, 1/108, 1/147 em n=4..7 — batem em ≥5
dígitos), o que por si só já aponta a₁ = 1/3 exato.

### (b) Monte Carlo em n grande, c frescos — **CONFIRMADO**

Simulador próprio vetorizado (composição iterada f^(2^17) + contagem de
imagem distinta; validado: c=0 ⇒ φ=1; c=n ⇒ mapa aleatório puro com
E[#cíclicos] = √(πn/2), z=−1.34; 50/50 concordâncias exatas com detector
independente por pilha). n = 65536, N = 6000/célula, seed 77003917
(`adv2_mc.py/.json`):

| c | φ_MC ± SEM | forma alegada | z |
|---|---|---|---|
| 0.37 | 0.890802 ± 0.002743 | 0.889232 | +0.57 |
| 2.71828 | 0.523678 ± 0.003290 | 0.526924 | −0.99 |
| 7.5 | 0.325531 ± 0.002182 | 0.323570 | +0.90 |
| 23 | 0.185774 ± 0.001238 | 0.184791 | +0.79 |

Todas |z| < 1; χ²₄ = 2.73, p ≈ 0.60. Nenhum desvio detectável já em
n = 65536 com esta precisão.

### (b2) Objeto-limite contínuo, construção direta — **CONFIRMADO**

Construção estrutural própria (GEM(1) stick-breaking + K~Poisson(c)
marcas + grafo marca→marca; massa cíclica exata por realização),
N = 400.000/célula, seed 55510123 (`adv2_continuum.py/.json`):
7 células c ∈ {0.37, 0.5, 1, 2.71828, 7.5, 23, 50}; maior desvio
|z| = 2.26 (c=7.5, +0.0006), sinais mistos, **χ²₇ = 12.82, p = 0.077**
— sem estrutura sistemática (em c=7.5 o MC finito independente de (b)
dá z=+0.90; em c=0.37 os sinais de (b) e (b2) são opostos). Em c=0.5 a
concordância é de 1e−6 (0.855626 ± 0.000371 vs 0.855624).

### (c) Re-derivação analítica própria — **CONFIRMADO** (derivação reproduzida)

Feita antes de qualquer execução e antes de ler a derivação da frente
(registrada em `ADVERSARIAL_NOTE.md`):

1. **a₁ = 1/3 exato** por argumento direto (1 marca, ciclo size-biased
   ℓ~U(0,1), perda ℓ − ℓ²/2 ⇒ E = 1/3) — refuta analiticamente a forma
   antiga (1+c)^{−1/2} (a₁ = 1/2) e dá **φ₁ = 2/3** exato.
2. **Cauda (√π/2)c^{−1/2}** por assintótica própria (arcos Exp(c), arco
   visitado size-biased de média 2/c ⇒ Σe^{−t²/c} = √(πc)/2, E[D] = 1/c).
   Nota: esquecer o size-biasing dos arcos visitados daria √(π/2)c^{−1/2}
   (fator √2 errado) — o valor alegado é o correto.
3. **Derivação completa própria** via processo de exploração: hazards
   1/(1−s) por cabeça de arco, marca a taxa c com morte prob. s; o
   produto telescopa e P_J = ∫₀¹ e^{−cs}c^J(1−s)^J s^J/J! ds ⇒
   **φ = ∫₀¹ e^{−cs²} ds** — exatamente a forma alegada.

Lida DEPOIS a `DERIVATION.md` da frente: é passo a passo o MESMO
argumento (mesmos hazards, mesmo cancelamento no PGFL §3 — que no meu
cálculo aparece como telescópio; conferi F(s) = (1−t), E[S(t)] =
(1−t)e^{−ct²} e a identidade (2.1)). **Nenhum erro de lógica
encontrado.** A ressalva honesta deles (§6: passagem finita-n→contínuo
sem rigor Stein/coupling completo) é a mesma da minha derivação — e é
exatamente o elo que as superfícies (a) e (b) controlam empiricamente.
Identidades internas verificadas numericamente à parte: erf = integral =
série (≤1e−15); Wallis; cauda (`scratchpad`).

### (d) Lei condicional φ_K — **CONFIRMADO**

MC próprio do objeto contínuo com K determinístico, N = 400.000, seed
90210777 (`adv2_continuum.py`), mais teste distribucional KS
(`adv2_ks.py`, N = 200.000, seed 90210999):

| K | φ_K MC ± SEM | alvo 4^K(K!)²/(2K+1)! | z | KS vs F(x)=1−(1−x²)^K |
|---|---|---|---|---|
| 1 | 0.666394 ± 0.000372 | 2/3 | −0.73 | D=0.0016, p=0.70 |
| 2 | 0.533167 ± 0.000349 | 8/15 | −0.48 | D=0.0024, p=0.19 |
| 3 | 0.457537 ± 0.000320 | 16/35 | +1.23 | D=0.0028, p=0.09 |

K=1 também é exato pela minha rota analítica (item c.1). O teste KS
confirma inclusive a LEI DISTRIBUCIONAL completa 2Kx(1−x²)^{K−1}
(a parte que a frente declara conjectura para K≥2 — sai reforçada,
continua conjectura como prova).

### Citação Hansen–Jaworski — **CONFIRMADA**

PDF baixado da fonte (combinatorics.org, EJC 21(1) #P1.18): o artigo é
"Structural transition in random mappings", Jennie C. Hansen & Jerzy
Jaworski, 2014; modelo T̂ʳₙ = "corrupted permutation" com a = n−r
vértices de in-degree ≤ 2. **Teorema 7(ii) verbatim:** para a fixo e
k = ⌊xn⌋, P{X̂ʳₙ = k} ∼ (1/n)·2ax(1−x²)^{a−1} — exatamente a densidade
condicional (com a=K) cuja média é ∫₀¹(1−x²)^a dx = 4^a(a!)²/(2a+1)!.
A qualificação da frente ("modelo microscopicamente diferente, mesmo
limite; mistura de Poisson possivelmente nova") é honesta e correta:
o modelo H-J é uniforme sob restrição de in-degree, não o reroteamento
Bernoulli — a equivalência do limite condicional é exatamente o que meu
teste KS de (d) verifica de forma independente para o ensemble u12.

## Comparação direta com a frente (após travamento)

| Quantidade | Frente (limit_sim) | Adversarial (este) | Concorda? |
|---|---|---|---|
| c=0.5 contínuo | 0.855501 ± 0.000523 | 0.855626 ± 0.000371 | sim (0.2σ; ambos ~forma) |
| c=50 contínuo | (T2, z pequeno) | 0.125473 ± 0.000104 vs 0.125331 (z=+1.37) | sim |
| φ_K K=1..3 | z ≤ 1.25 (T3) | z ∈ {−0.73, −0.48, +1.23} | sim |
| held-out | p=0.163 (10 células) | c frescos: p≈0.60 (4 células, n finito) + p=0.077 (7 células contínuo) | sim |
| Código | inspecionado PÓS-travamento | — | **nenhum bug encontrado** (bisect com contiguidade das marcas por ciclo, wrap, coloração de caminhos: corretos) |

## VEREDITO GERAL: **CONFIRMADO** (todas as superfícies)

A tentativa honesta de refutação FALHOU em todas as quatro superfícies.
Mais forte que isso: a minha re-derivação independente, feita às cegas,
produz a MESMA forma fechada ∫₀¹e^{−ct²}dt, e a enumeração exata
finita-n (que não depende de nenhuma simulação) extrapola para ela com
resíduo ~3e−5 em c=0.5 e fixa a₁ = 1/3 com o padrão exato
a₁(n) = (n²−1)/(3n²). A forma fechada, a série, a cauda, a lei
condicional-K e a citação Hansen–Jaworski estão corretas como alegadas.

Ressalvas de escopo (idênticas às da frente, mantidas): (i) a passagem
finita-n → contínuo é controlada empiricamente (n ≤ 65536 aqui), não
formalizada em rigor total; (ii) a lei distribucional completa
min(1,√(E/c)) segue conjectura (reforçada pelos meus KS) para K≥2 como
prova; (iii) nada aqui toca extrapolações Primes/Quantum Chaos/ToE.

## Arquivos desta verificação

- `ADVERSARIAL_NOTE.md` — pré-registro (plano, seeds, derivação própria).
- `adv2_exact.py/.json/.log` — superfície (a), enumeração exata n=4..7.
- `adv2_extrap.py/.json/.log` — extrapolações + a₁ exato.
- `adv2_mc.py/.json/.log` — superfície (b), MC n=65536, c frescos.
- `adv2_continuum.py/.json/.log` — superfícies (b2) e (d).
- `adv2_ks.py/.json/.log` — teste distribucional KS condicional.
