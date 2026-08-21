# Resultados — frente `u12-universality` (DISC-CORE-NUMERICS-001 / DISC-DEC-013)

**Data:** 2026-08-21. Critérios de decisão fixados ANTES da computação
em `METHODOLOGY_NOTE.md` (mesmo diretório). Implementação independente,
do zero (`analysis/u12_reproduction.py`, `analysis/gap_spectral_test.py`),
validada internamente (`analysis/validation_checks.py`: 0/100
divergências entre dois contadores de pontos cíclicos independentes;
benchmark Flajolet–Odlyzko `E[cíclicos] ≈ sqrt(πn/2)` reproduzido com
razão 0.986–1.013; `c=0 ⇒ φ=1` exato).

## Veredito (máximo permitido pela disciplina da linha)

> **Reproduzido no protocolo do arquivo; distinto das classes
> concorrentes do Atlas como formulado. PORÉM: a forma forte da
> alegação — limite exato `φ(c) = (1+c)^{-1/2}` quando `n→∞`
> ("Theorem", Closure_Paper/paper.html:315-322) — NÃO é suportada:
> há desvios sistemáticos pequenos (~2–4% absolutos, até 7.8 σ
> agrupados) que NÃO diminuem de n=1.000 a n=64.000.**

Detalhe por critério pré-declarado:

| Critério | Resultado | Números |
|---|---|---|
| R1a (expoente do arquivo) | **PASS** | Fit-espelho (n=2000, protocolo de `final_verification.py`): α = 0.506, IC95 bootstrap [0.490, 0.522] — contém 0.5 e intersecta 0.508±0.033 |
| R1b (erro médio < 0.05) | **PASS** (2×) | 0.0203 (grade primária, 28 células), 0.0261 (grade adversarial) |
| R1c (limite: IC de α em n máx contém 0.5) | **FAIL** (2×) | n=4000: α = 0.512, IC95 [0.5003, 0.5241]; n=3000 (2º seed set): α = 0.520, IC95 [0.5075, 0.5311] |
| R2 (distinção das classes do Atlas, ΔAIC ≥ 10) | **PASS** (2×) | menor ΔAIC vs U_1/2 fixa: 582.8 (U_2 livre, primária) e 374.0 (U_2 livre, adversarial); U_0, U_1, U_∞ ainda piores |
| R3 (gap(n)=2/n, λ₂=(n−2)/n) | **PASS (exato)** | n=3..7: desvios < 1e−8 (operador de 1 partição de quicksort, pivô uniforme, reimplementado) |

## O que foi testado (definição operacional)

Ensemble (idêntico ao do arquivo, `final_verification.py:36-57`,
`step9_2_discrete_convergence.py:76-89`): permutação uniforme de `[n]`;
cada ponto independentemente rerroteado com prob. `c/n` para destino
uniforme. Observável: fração de pontos cíclicos do grafo funcional.

## Números principais

### Grade primária (seed base 20260821, N=200/célula, n ∈ {500,1000,2000,4000}, c ∈ {0.5,...,50})

- Fit-espelho n=2000 não ponderado: **α = 0.5057 ± 0.0188** — reproduz
  o **0.508 ± 0.033** do arquivo (RESEARCH_RESULTS.md:634) dentro do
  ruído. O protocolo do arquivo (7 pontos, 30 amostras, sem pesos,
  sem seed) é estatisticamente frouxo, e o próprio script gravado não
  executa (NameError na linha 25 de `final_verification.py`); o valor
  específico 0.508±0.033 não é regenerável bit a bit, apenas
  estatisticamente — e É reproduzido nesse sentido.
- α não ponderado por n: 0.506 (n=500), 0.495 (n=1000), 0.506 (n=2000),
  0.499 (n=4000) — todos consistentes com 0.5 nesse nível de precisão.
- Com precisão maior (ajuste ponderado por SEM): α = 0.5117 ± 0.0058
  (n=4000) e α = 0.5195 ± 0.0056 (n=3000, grade e seeds independentes)
  — ambos excluem 0.500 marginal-mas-consistentemente (R1c FAIL).

### Ajuste de qualidade da forma fixa `(1+c)^{-1/2}`

- χ² (7 pontos, n=4000): 24.6 → p ≈ 9×10⁻⁴.
- χ² (7 pontos, n=3000, grade adversarial): 77.6 → p ≈ 4×10⁻¹⁴.
- A forma é uma aproximação excelente (~2% absoluto), mas os resíduos
  não são ruído.

### Diagnóstico PÓS-HOC de tamanho finito (`analysis/finite_size_diagnostic.py`, seed 99001122, N=400/célula, n até 64.000)

Desvio `φ_medido − (1+c)^{-1/2}` agrupado sobre n ∈ {1000, 4000,
16000, 64000} (estável em n, sem tendência de queda ao longo de 64×):

| c | desvio agrupado | significância |
|---|---|---|
| 0.5 | +0.0355 ± 0.0060 | +5.9 σ |
| 2.0 | +0.0186 ± 0.0068 | +2.7 σ |
| 10.0 | −0.0229 ± 0.0037 | −6.2 σ |
| 50.0 | −0.0127 ± 0.0016 | −7.8 σ |

Estrutura de sinal (positivo em c pequeno, negativo em c grande) é
exatamente o que infla o α ajustado para ~0.51–0.52 em alta precisão.
Interpretação honesta: **o limite `φ(c)` existe empiricamente (valores
estáveis em n), mas difere da forma fechada `(1+c)^{-1/2}` por ~2–4%
absolutos**; uma correção de decaimento muito lento (ex.: `1/log n`)
não pode ser 100% excluída com n ≤ 64.000, mas nada nos dados a
sugere. Observação: a própria verificação do arquivo
(DISCOVERY_SUMMARY.md:1015-1027) mostra erros relativos de até 9.6% e
mesmo assim declara "TEOREMA VERIFICADO" — os desvios que medimos já
eram visíveis nos dados do próprio arquivo.

### Distinção de classes (pré-declarada, AIC = χ² + 2k, células de n máximo)

| Modelo | forma | AIC (primária) | AIC (adversarial) |
|---|---|---|---|
| **U_1/2 fixa** | `(1+c)^{-1/2}` | **24.6** | **77.6** |
| U_1/2 livre | `(1+c)^{-α}` | 22.3 | — |
| U_2 livre | `(1+βc)^{-2}` | 607.3 | 451.6 |
| U_∞ livre | `1/(1+c^m)` | 644.7 | 1420.0 |
| U_1 livre | `exp(-λc)` | 1278.6 | 1154.0 |
| U_0 threshold | degrau | 1143.9 | 1357.4 |

Todas as concorrentes nomeadas no Atlas (RESEARCH_RESULTS.md:662-668)
são rejeitadas com ΔAIC ≥ 374 nos dois conjuntos de seeds — a lei é
**distinta** das classes U_0, U_1, U_2 e U_∞ como formuladas.

### Gap espectral (componente C)

`gap(n) = 2/n` e `λ₂ = (n−2)/n` verificados EXATOS (desvio < 1e−8,
ponto flutuante) para n = 3..7 com reimplementação independente do
operador de uma partição de quicksort com pivô uniforme
(`analysis/gap_spectral_test.py`, `result_gap_spectral.json`). Nota de
escopo: esta é uma identidade algébrica de um operador específico
pequeno; o próprio arquivo reconhece que ela NÃO fornece a
complexidade do quicksort (DISCOVERY_SUMMARY.md:47-51) — é resultado
correto porém modesto.

## Escopo e limites

- Nada aqui valida as extrapolações do arquivo da classe U_1/2 a
  "Primes, Quantum Chaos" (REAL_DISCOVERIES.md:63-64) — essa extensão
  não decorre das fontes primárias e não foi testada.
- Nenhuma inferência Tamesis/ToE: a ToE permanece refutada pelo
  próprio arquivo (ToE_Refutation/FINAL_VERDICT.md).
- Reprodução adversarial em nível de orquestrador: **SINALIZADA**
  (critérios R1a+R1b+R2 sobreviveram a dois conjuntos independentes de
  seeds e grades; o achado novo — desvio sistemático estável que
  contradiz a forma exata do "teorema" — merece re-derivação/re-medição
  por agente independente antes de qualquer atualização do arquivo).

## Arquivos

- `METHODOLOGY_NOTE.md` — pré-registro (fontes verbatim + critérios).
- `analysis/u12_reproduction.py` — reprodução independente (grades
  primária e adversarial), `result_primary.json`,
  `result_adversarial.json`, `primary.log`, `adversarial.log`.
- `analysis/gap_spectral_test.py` — teste R3, `result_gap_spectral.json`,
  `gap_spectral.log`.
- `analysis/validation_checks.py` — validação interna,
  `result_validation_checks.json`, `validation_checks.log`.
- `analysis/finite_size_diagnostic.py` — diagnóstico pós-hoc,
  `result_finite_size_diagnostic.json`, `finite_size_diagnostic.log`.
