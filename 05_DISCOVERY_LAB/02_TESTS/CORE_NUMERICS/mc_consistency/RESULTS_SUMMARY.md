# Resultado — `mc_consistency` (consistência interna do valor congelado de M_c)

**Frente:** `mc-internal-consistency`, linha `DISC-CORE-NUMERICS-001`
(DISC-DEC-013, 2026-08-21). Critérios fixados a priori em
`METHODOLOGY_NOTE.md`; execução única e determinística de
`analysis/compute_mc_consistency.py` (saída integral em
`analysis/compute_mc_consistency.log`, números em
`analysis/results.json`). Nenhuma correção ou reexecução foi necessária.

## VEREDITO: **INCONSISTENTE COMO FORMULADO**

O valor congelado `M_c = 5.292674126388712e-16 kg` (contrato
`tamesis-mc-v1.0`) é **aritmeticamente correto sob suas próprias
premissas** (C1 aprovado), mas **não é internamente consistente com o
restante do núcleo** em dois critérios independentes:

- **C2 REPROVADO** — o contrato usa o ramo `a0 = cH0`, exatamente o ramo
  que o teste pré-registrado do próprio laboratório
  (`DISC-COSMOLOGY-MOND-SPARC-002`, dados reais SPARC,
  `05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_A0_DERIVATION/analysis/result_primary.json`,
  veredito `H_A_SURVIVES_H_B_FALSIFIED`) **falsificou**; o ramo
  sobrevivente do próprio núcleo é `a0 = cH0/2π`. Sob o ramo
  sobrevivente, a mesma fórmula dá
  `M_c = 4.206323510621529e-16 kg` — o valor congelado excede-o pelo
  fator exato `(2π)^(1/8) = 1.258266063710756` (**+25,83%**).
- **C3 REPROVADO** — as formulações de M_c espalhadas pelo núcleo
  diferem entre si por até **189,7×** (2,28 ordens de grandeza); 6 pares
  excedem o limiar de inconsistência (fator 10) fixado a priori.

Máxima força do veredito, conforme a nota: nenhuma inferência sobre
física — apenas sobre a coerência interna do número.

## Critérios (fixados antes de computar) e resultados

| Critério | Definição resumida | Resultado |
|---|---|---|
| C1 | recálculo reproduz o valor congelado (tol. rel. 1e-9) e o `si_value` de H0 (tol. 1e-6) | **APROVADO** (desvios 2,8e-12 e 2,3e-11) |
| C2 | ramo de a0 do contrato = ramo sobrevivente de SPARC-002, ou diferença ≤ 1% | **REPROVADO** (ramo falsificado; +25,83%) |
| C3 | todos os pares de valores de M_c dentro de fator 2; reprova se algum par > fator 10 | **REPROVADO** (máx. 189,7×) |
| C4 | fidelidade aritmética das derivações alternativas (informativo) | 1 fiel, 2 infiéis e dimensionalmente inconsistentes (abaixo) |

## Inventário de M_c no núcleo (tarefa a)

| Valor (kg) | Fórmula/derivação | Arquivo:linha (canônico + ocorrências) | Contexto |
|---|---|---|---|
| 5.292674126388712e-16 | `M_c = m_P (a0/a_P)^(1/8)`, `a0 = cH0`, H0=70 km/s/Mpc | `…/tamesis_mc_v1/config/tamesis_mc_v1.yaml:63` (canônico); `config.py:223`; `mc_model.py:11-21`; `STATUS.md:28`; `reports/MODEL_CONTRACT_V1_0.md:23`; `data/model_summary.json:8` e demais sidecars | Contrato congelado 2026-07-26; raiz oitava classificada `modelling_assumption` no próprio YAML (linha 35: "not a derived theorem") |
| 5.29e-16 / 5.2926e-16 (mesma escala) | idem (`m_P·Ξ^{1/8}`, Ξ=a0/a_P) | `massa_critica/README.md:16,26,178`; `ResearchStrategy.md:15`; `simulations/constants.py` (docstring); `hipotese_colapso_quantico/PROPOSTA_MC.md` (§2, "≈5,3e-16"); `01_Foundation/roadmap.md:90`; `01_Foundation/Core_Papers/roadmap.md:56` | Mesmo ramo `a0=cH0`; `calculo_mc.py:36-66` documenta que o expoente 1/8 saiu de VARREDURA de frações {1/2…3/4} contra janela-alvo 1e-17–1e-14 kg (o próprio script chega a sugerir 1/6 para alvo 1e-15) |
| 2.2e-14 | (i) `(ħ²/(Gc))^{1/4}`; (ii) `(ħ·m_atom·c³/4G)^{1/3}`; (iii) valor "observado"/alvo sem fórmula | (i) `08_…/prl_submission.html:239`; (ii) `03_Axiomatic_Closure/Universe_Equation/01_Mc_Derivation/index.html:255`; (iii) `Killer_Prediction/interference_sim.py:10`; `Tabletop_Experiment/experiment_design.py:9`; `05_Falsification_Criteria/falsify.py:99`; `Universe_Equation/roadmap.md:49`; `04_Transition_Sim/transition_simulation.py:26`; `08_…/generate_figures.py:30`; `ToE_Refutation/mc_investigation.py:25`, `unified_constants.py:64` | "Killer prediction"/manuscrito 08 e rascunho PRL; `STATUS.md:39-41` do módulo v1 já registrava o conflito "sem explicar a mudança de duas ordens de magnitude" |
| ~1e-14 | `(ħ²/(Gc))^{1/4}` como ordem de grandeza | `08_…/paper.html:410` | O próprio arquivo declara incerteza de 1–2 ordens de grandeza e que "the exact value of M_c is an experimental question" |
| 1.16e-16 | `M_c ≈ M_P·Ω^{-4}`, Ω=117.038 | `01_Foundation/README.md:97` (Ω definido nas linhas 17 e 46) | Rotulado "Prediction" na tabela de escalas do Ω-postulado |

**Admissões do próprio núcleo, registradas no inventário:**

- `tamesis_mc_v1/STATUS.md:31-32`: *"O valor não é uma constante medida
  nem uma derivação concluída."*
- `tamesis_mc_v1/STATUS.md:34-41`: lista os conflitos legados (mistura
  de estados "derivado/calibrado/hipótese" em `constants.py`; o
  2,2e-14 do `Killer_Prediction` "sem explicar a mudança de duas ordens
  de magnitude").
- `ToE_Refutation/mc_investigation.py` (seções 3–4): conclui que "M_c
  NÃO pode ser derivado de holografia cosmológica" e que Λ, a0 e M_c são
  "TRÊS fenômenos INDEPENDENTES" — ou seja, o próprio núcleo, no Estágio
  de auto-refutação, já desautorizou a ponte cosmológica que o contrato
  v1.0 congela.
- `tamesis_mc_v1/reports/STRUCTURAL_PARAMETER_SEARCH_EVIDENCE.md` é um
  inventário interno anterior que já classificava as ocorrências de
  2,2e-14 como `expected_legacy`.

## Números (tarefas b e c)

Constantes: congeladas do contrato para A1–A3; CODATA 2022/IAU (fetch
2026-08-21, proveniência na nota de metodologia) para checagens de
sanidade e A4. Sanidade: `m_P` do contrato vs CODATA difere 1,6e-7
(dentro de 2,2e-5). `l_P = 1.616255023929e-35 m`,
`a_P = 5.560726280388e+51 m/s²`.

**A1 — aritmética do contrato.** Recalculado
`M_c = 5.292674126403759e-16 kg` vs congelado
`5.292674126388712e-16` → desvio relativo **2,84e-12** (a diferença é o
próprio `si_value` de H0 congelado com Mpc ligeiramente diferente do IAU
exato: 2.268545502662652e-18 vs 2.268545502611056e-18 s⁻¹, desvio
2,3e-11). **A aritmética congelada é correta.**

**A2 — os dois ramos de a0 (H0=70).**

| Ramo | a0 (m/s²) | M_c (kg) |
|---|---|---|
| `a0 = cH0` (contrato; **falsificado** por SPARC-002) | 6.800928e-10 | 5.292674126403759e-16 |
| `a0 = cH0/2π` (**sobrevivente** em SPARC-002) | 1.082401e-10 | 4.206323510621529e-16 |

Fator de deslocamento: `(2π)^(1/8) = 1.258266063710756` → o valor
congelado está **25,83% acima** do que a própria fórmula dá no ramo que
o núcleo deixou sobreviver.

**A3 — sensibilidade a H0** (`M_c ∝ H0^{1/8}`): H0=67,4 → −0,472%;
H0=73 → +0,526% (ambos os ramos escalam igualmente). A escolha de H0 é
numericamente irrelevante perto do fator de ramo de ~26%.

**A4 — aritmética das derivações alternativas.**

- `M_P·Ω^{-4}` (Ω=117,038): recomputado `1.159946e-16 kg` vs alegado
  1,16e-16 → desvio 0,005%, **fiel**. Mas difere do valor congelado por
  fator 4,56 (tensão, faixa 2×–10×).
- `(ħ²/(Gc))^{1/4}` (rascunho PRL): **dimensionalmente inconsistente** —
  a combinação tem dimensão `kg^(3/4)·s^(1/4)`, não massa. O valor
  numérico da expressão como escrita é `2.730433e-17` (unidades SI
  mistas); a alegação "≈2,2e-14 kg" é **805,7× maior** que a expressão
  escrita. **Infiel.**
- `(ħ·m_atom·c³/4G)^{1/3}` (01_Mc_Derivation): **dimensionalmente
  inconsistente** (`kg·m^{2/3}·s^{-2/3}`). Com m_atom = 1 u dá
  `2.605e-9` (mistas); para reproduzir 2,2e-14 seria preciso
  `m_atom = 1,0e-42 kg` (6e-16 u — nenhum átomo físico). Além disso o
  mesmo arquivo alega que 2,2e-14 kg ≈ "320 million amu", quando
  2,2e-14 kg = 1,325e13 u (erro interno de 4,1e4×; "320 bilhões de u" é
  na verdade o valor CONGELADO 5,29e-16 kg = 3,19e11 u — indício de
  conflação entre os dois valores dentro do próprio arquivo). **Infiel.**

**A5 — matriz de razões** (inclui o ramo sobrevivente):

| | congelado | 2,2e-14 | 1e-14 | Ω⁻⁴ (1,16e-16) | sobreviv. (4,21e-16) |
|---|---|---|---|---|---|
| congelado 5,29e-16 | 1 | 0,024 | 0,053 | 4,56 | 1,258 |
| 2,2e-14 | 41,6 | 1 | 2,2 | 189,7 | 52,3 |
| 1e-14 | 18,9 | 0,455 | 1 | 86,2 | 23,8 |
| 1,16e-16 | 0,219 | 0,0053 | 0,0116 | 1 | 0,276 |
| 4,21e-16 | 0,795 | 0,019 | 0,042 | 3,63 | 1 |

Maior razão par-a-par: **189,7× (2,28 ordens de grandeza)**. Seis pares
acima de 10×; três pares na faixa de tensão 2×–10× (inclusive
congelado vs Ω⁻⁴: 4,56×; congelado vs ramo sobrevivente: 1,26×).

## Limitações (declaradas)

1. **Auditoria de consistência interna, não teste experimental.** Não
   existe dado de laboratório na escala de M_c: o próprio
   `reports/BOHR_LEVEL_GAP.md` registra que o melhor ponto observado de
   interferência de centro de massa está em `M/M_c = 5,33e-7` (~1,9
   milhão de vezes abaixo do limiar), com zero registros perto/acima do
   limiar. Nada aqui valida ou refuta M_c fisicamente.
2. **SPARC-002 adjudica a0 em dinâmica galáctica**; transferir esse a0
   para colapso quântico é uma escolha do próprio núcleo. C2 cobra
   somente coerência com a escolha sobrevivente do próprio corpo teórico
   — aliás, o próprio `ToE_Refutation` do núcleo já concluíra que essa
   ponte não se sustenta.
3. Os limiares de C3 (fator 2 / fator 10) são convenções fixadas a
   priori na nota; os pares na faixa intermediária foram reportados como
   tensão, não adjudicados.
4. Os papers 08 declaram explicitamente que 2,2e-14/1e-14 é estimativa
   de ordem de grandeza com incerteza de 1–2 ordens — mesmo sob essa
   leitura caridosa, a fórmula escrita não reproduz o próprio número
   alegado (805,7×) e não tem dimensão de massa, o que é um defeito
   aritmético/dimensional interno, não uma questão de precisão.
5. O veredito global foi negativo, logo a regra "recomputar por segunda
   rota + reprodução adversarial obrigatória antes de catalogar" para
   achados POSITIVOS não foi acionada. Ainda assim, como C1 (subalegação
   aprovada) é um resultado que o contrato usa a seu favor, recomenda-se
   reprodução adversarial barata em nível de orquestrador do A1 antes de
   catalogar (é uma linha de aritmética; o custo é trivial).

## Arquivos desta frente

- `METHODOLOGY_NOTE.md` — critérios fixados antes de computar (sem adendos).
- `analysis/compute_mc_consistency.py` — script determinístico único.
- `analysis/compute_mc_consistency.log` — saída integral da execução única.
- `analysis/results.json` — todos os números em forma estruturada.
- `RESULTS_SUMMARY.md` — este arquivo.
