# Veredito adversarial — frente u12-universality

**Agente:** reprodução ADVERSARIAL (DISC-CORE-NUMERICS-001 / DISC-DEC-013).
**Data:** 2026-08-21. Plano e seeds pré-registrados em `ADVERSARIAL_NOTE.md`
(gravado antes de qualquer execução). Implementação 100% independente e
estruturalmente distinta (reroteamento Binomial+posições sem reposição;
detecção de pontos cíclicos por *pointer doubling* / imagem de f^N; rota
analítica extra pela simulação direta do objeto-limite n→∞). O código e os
resultados da frente primária (`analysis/`) só foram lidos DEPOIS de todos
os números adversariais estarem gravados em JSON (ordem verificável nos
timestamps dos arquivos).

## Validação do simulador (pré-requisito, ANTES de medir)

- Enumeração exata (soma sobre TODOS os n^n mapas com peso analítico
  sobre π), n ∈ {4,5,6}, c ∈ {0.5, 2}; fórmula cross-checada por força
  bruta sobre todas as n! permutações (n=4,5; concordância < 1e−10).
  MC vs exato: 6 células, |z| máx = 2.48. (`adv_validate.log`)
- Benchmarks clássicos: c=0 ⇒ φ=1 exato; c=n ⇒ random map uniforme
  puro, P(cíclico) exato em n=1000: z = −0.54.
- Já na enumeração exata: E[φ] em c=0.5 cai 0.8626 → 0.8595 → 0.8579
  (n=4,5,6), tendendo a ~0.855 — LONGE do "teorema" 0.8165.

## VEREDITOS POR ITEM

### Item 1 — expoente α ≈ 0.506, IC95 [0.490, 0.522], consistente com 1/2: **CONFIRMADO**

Protocolo-espelho do arquivo (n=2000, c ∈ {0.5,…,50}, ajuste não
ponderado de `(1+c)^{-α}`; meus dados: N=300/célula, seed 424242):

- **α = 0.4992 ± 0.0187** (curve_fit), IC95 bootstrap **[0.4865, 0.5124]**
  (B=4000). Contém 0.5; intersecta o IC da frente primária [0.490,
  0.522] e o 0.508±0.033 do arquivo. Não refutável. (`adv_fits.log`)

### Item 2 — U_1/2 decisivamente preferida sobre U_0/U_1/U_2/U_∞: **CONFIRMADO** (com margens ainda maiores)

n=4000, N=1000/célula (seed 8675309), χ² ponderado por SEM, AIC = χ²+2k:

| Modelo | χ² | AIC | ΔAIC vs U_1/2 fixa |
|---|---|---|---|
| U_1/2 fixa `(1+c)^{-1/2}` | 160.6 | 160.6 | 0 |
| U_1/2 livre `(1+c)^{-α}` (α=0.520) | 100.5 | 102.5 | −58.1 |
| U_∞ livre `1/(1+c^m)` | 2806.2 | 2808.2 | **+2647.6** |
| U_2 livre `(1+βc)^{-2}` | 2923.6 | 2925.6 | +2765.0 |
| U_0 degrau | 5696.3 | 5700.3 | +5539.7 |
| U_1 livre `e^{-λc}` | 6222.0 | 6224.0 | +6063.4 |

Pior margem adversarial: **+2648** (U_∞) ≫ 10. A frente primária
reportou pior margem 374 (U_2, grade n=3000) — a diferença de magnitude
é esperada (meus SEMs são menores por N maior); a ORDENAÇÃO e o
critério pré-declarado (ΔAIC ≥ 10 para todas) confirmam-se. Nota
honesta: α livre bate a forma fixa por ΔAIC = −58 e o χ² da forma fixa
tem p ≈ 2.4×10⁻³¹ — coerente com o Item 3: a lei é da "família 1/2",
mas a forma fechada exata não é o limite verdadeiro.

### Item 3 — anti-alegação (teorema exato contradito): **CONFIRMADO E REFORÇADO**

(a) Desvios finitos NÃO encolhem (seed 31415926; N=8000…3000/célula):

| c | n=2000 | 4000 | 8000 | 16000 | 32000 | 64000 | agrupado |
|---|---|---|---|---|---|---|---|
| 0.5 (dev vs teorema) | +0.0387 | +0.0329 | +0.0436 | +0.0421 | +0.0371 | +0.0429 | **+0.0394±0.0012 (+32.5σ)** |
| 50 (dev vs teorema) | −0.0154 | −0.0142 | −0.0153 | −0.0157 | −0.0162 | −0.0148 | **−0.0152±0.0003 (−44.6σ)** |

Razão (média dos 3 maiores n)/(3 menores): 1.06 (c=0.5) e 1.05 (c=50)
— sem qualquer encolhimento (correção O(n^{-1/2}) preveria razão ~0.4).
χ² agrupado contra o teorema: p ≈ 5×10⁻²²⁷ (c=0.5) e p < 1×10⁻³⁰⁰
(c=50) — muito além dos p ≈ 9×10⁻⁴ / 4×10⁻¹⁴ da frente primária,
porque usei N maior.

(b) **Rota analítica independente — simulação exata do objeto-limite**
(`adv_continuum.py`, seed 271828): no limite n→∞ o ensemble converge
para: ciclos ~ Poisson–Dirichlet(1), K ~ Poisson(c) pontos reroteados
com destinos uniformes; a massa cíclica é a massa dos ciclos sem
reroteamento MAIS os segmentos percorridos ao longo dos ciclos do mapa
de saltos g (derivação na nota; estimador não viesado, sem n finito):

| c | φ_∞ (contínuo) | teorema `(1+c)^{-1/2}` | desvio | signif. |
|---|---|---|---|---|
| 0.5 | 0.85493 ± 0.00053 | 0.81650 | **+0.03843** | +73σ |
| 1 | 0.74688 ± 0.00122 | 0.70711 | +0.03977 | +33σ |
| 2 | 0.59837 ± 0.00122 | 0.57735 | +0.02102 | +17σ |
| 5 | 0.39570 ± 0.00092 | 0.40825 | −0.01254 | −14σ |
| 10 | 0.28015 ± 0.00065 | 0.30151 | −0.02136 | −33σ |
| 20 | 0.19853 ± 0.00046 | 0.21822 | −0.01968 | −42σ |
| 50 | 0.12524 ± 0.00015 | 0.14003 | **−0.01479** | −101σ |

(c) Consistência cruzada: os dados finitos (item a) são TOTALMENTE
explicados pelo limite contínuo — χ² dos 6 pontos de n contra φ_∞:
p = 0.093 (c=0.5) e p = 0.577 (c=50). Ou seja: o limite φ(c) EXISTE,
é o que a simulação do contínuo dá, e NÃO é `(1+c)^{-1/2}`. A forma
fechada é apenas uma boa aproximação (~2–4% absolutos) com o
comportamento assintótico correto ~c^{-1/2}.

O "Theorem (U_1/2 Universality)" do arquivo
(`Closure_Paper/paper.html:315-322`) está portanto **refutado como
identidade exata** por DUAS rotas independentes entre si e independentes
da frente primária. Não consegui refutar a anti-alegação — ela sai
FORTALECIDA (de ~6–8σ para >30σ por célula agrupada, mais o limite
contínuo).

## Comparação direta com a frente primária

| Quantidade | Frente primária | Adversarial (este) | Concordância |
|---|---|---|---|
| α (espelho n=2000) | 0.506, IC [0.490, 0.522] | 0.499, IC [0.487, 0.512] | sim (sobreposição ampla) |
| Pior ΔAIC concorrente | +374 (U_2, n=3000) | +2648 (U_∞, n=4000) | sim (mesma ordenação; margem maior por N maior) |
| dev c=0.5 (agrupado) | +0.0355 ± 0.0060 | +0.0394 ± 0.0012; contínuo +0.0384 ± 0.0005 | sim (0.6σ) |
| dev c=50 (agrupado) | −0.0127 ± 0.0016 | −0.0152 ± 0.0003; contínuo −0.0148 ± 0.0001 | sim (1.5σ) |
| p do χ² vs teorema | 9×10⁻⁴ (n=4000) / 4×10⁻¹⁴ | 5×10⁻²²⁷ (c=0.5) / <10⁻³⁰⁰ (c=50) | mesmo sentido, muito mais forte |
| Encolhe com n? | não (até 64.000) | não (até 64.000; razão 1.05–1.06) | sim |

Bugs: **nenhum encontrado** — nem no meu código (validado por
enumeração exata e benchmarks) nem no da frente primária
(`analysis/u12_reproduction.py`: peeling de Kahn e máscara Bernoulli
corretos por inspeção pós-travamento; nossos números batem célula a
célula dentro do ruído). A explicação mundana para o conjunto todo é
que o "teorema" do arquivo nunca foi um teorema: o limite verdadeiro é
o do objeto contínuo acima, e `(1+c)^{-1/2}` é um ansatz aproximado que
os dados de baixa estatística do arquivo (30 amostras/célula, sem seed)
não conseguiam distinguir.

## Escopo e ressalvas

- Vale para ESTE ensemble e ESTE observável; nada aqui toca
  extrapolações a "Primes/Quantum Chaos", Lindblad ou Tamesis/ToE.
- Correções ultra-lentas (ex.: 1/log n) não são 100% excluíveis com
  n ≤ 64.000, mas a coincidência quantitativa dos dados finitos com o
  limite contínuo independente (p = 0.09 / 0.58) torna essa hipótese
  supérflua.
- Custo total ≈ 6 min de CPU; nenhuma célula planejada foi cortada.

## Arquivos desta reprodução

- `ADVERSARIAL_NOTE.md` — plano + seeds (pré-registro).
- `adv_sim.py`, `adv_validate.py`, `adv_main.py`, `adv_continuum.py`,
  `adv_fits.py` — código próprio.
- `adv_validation.json`, `adv_results.json`, `adv_continuum.json`,
  `adv_fits.json` — dados; logs: `adv_validate.log`, `adv_M1.log`,
  `adv_M2.log`, `adv_M3.log`, `adv_M4.log`, `adv_fits.log`.

**Resumo executivo: itens 1, 2 e 3 CONFIRMADOS. A tentativa honesta de
refutação falhou em todos; o item 3 (refutação do "teorema exato") sai
mais forte do que a frente primária o deixou.**
