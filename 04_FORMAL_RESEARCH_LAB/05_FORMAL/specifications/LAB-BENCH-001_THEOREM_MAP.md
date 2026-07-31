---
schema: tamesis-benchmark-theorem-map/1
work_item_id: LAB-BENCH-001
scientific_value: "NONE — INFRASTRUCTURE BENCHMARK"
lean_root: "04_FORMAL_RESEARCH_LAB/05_FORMAL/lean"
toolchain: "leanprover/lean4:v4.33.0-rc1"
mathlib_revision: "79d0395a1825a6264ad5d269e35e60537518955e"
build_status: PASS
---

# LAB-BENCH-001 — Mapa de rastreabilidade

Cada item liga um requisito do benchmark a seu arquivo Lean, sua assinatura e
seu método de prova. Todos os resultados são matemática elementar conhecida.
Nenhum item é uma descoberta do Programa Tamesis; nenhum resultado Tamesis,
Omega ou Braid é usado como premissa.

## BENCH-FUN-001 — identidade e composição de funções

Arquivo: `TamesisLab/Benchmark/Core.lean` (sem imports; testa construção local)

| ID | Enunciado humano | Assinatura Lean | Dependências | Método | Build |
|---|---|---|---|---|---|
| FUN-DEF-1 | composição local de funções | `def fcomp {α β γ} (g : β → γ) (f : α → β) : α → γ` | — | definição | PASS |
| FUN-DEF-2 | identidade local | `def fid {α} : α → α` | — | definição | PASS |
| FUN-THM-1 | associatividade da composição | `theorem fcomp_assoc (h g f) : fcomp (fcomp h g) f = fcomp h (fcomp g f)` | FUN-DEF-1 | `rfl` | PASS |
| FUN-THM-2 | identidade à esquerda | `theorem fcomp_fid_left (f) : fcomp fid f = f` | FUN-DEF-1,2 | `rfl` | PASS |
| FUN-THM-3 | identidade à direita | `theorem fcomp_fid_right (f) : fcomp f fid = f` | FUN-DEF-1,2 | `rfl` | PASS |

## BENCH-DEF-001 — definições e estruturas pequenas

Arquivo: `TamesisLab/Benchmark/Structures.lean`

| ID | Enunciado humano | Assinatura Lean | Dependências | Método | Build |
|---|---|---|---|---|---|
| DEF-TY-1 | tipo enumerado com três regimes, igualdade decidível derivada | `inductive Regime \| alpha \| beta \| gamma deriving DecidableEq, Repr` | — | derivação | PASS |
| DEF-FN-1 | transição cíclica determinística `alpha → beta → gamma → alpha` | `def Regime.step : Regime → Regime` | DEF-TY-1 | definição por casos | PASS |
| DEF-THM-1 | aplicar `step` três vezes retorna ao regime inicial | `theorem Regime.step_cycle (r) : r.step.step.step = r` | DEF-FN-1 | `cases r <;> rfl` (análise finita) | PASS |
| DEF-ST-1 | estrutura pequena de estado | `structure BenchState where regime : Regime; tick : Nat` | DEF-TY-1 | estrutura | PASS |
| DEF-FN-2 | construtor do estado inicial | `def BenchState.init (r : Regime) : BenchState` | DEF-ST-1 | definição | PASS |
| DEF-THM-2 | projeção do regime após construção | `theorem BenchState.init_regime (r) : (BenchState.init r).regime = r` | DEF-FN-2 | `rfl` | PASS |
| DEF-THM-3 | projeção do contador após construção | `theorem BenchState.init_tick (r) : (BenchState.init r).tick = 0` | DEF-FN-2 | `rfl` | PASS |
| DEF-ST-2 | wrapper tipado de transformação | `structure Transition (α) where apply : α → α` | — | estrutura | PASS |
| DEF-FN-3 | transição identidade | `def Transition.id (α) : Transition α` | DEF-ST-2, FUN-DEF-2 | definição | PASS |
| DEF-FN-4 | composição de transições | `def Transition.comp (t s : Transition α) : Transition α` | DEF-ST-2, FUN-DEF-1 | definição | PASS |
| DEF-THM-4 | associatividade da composição de transições | `theorem Transition.comp_assoc (t s r) : (t.comp s).comp r = t.comp (s.comp r)` | DEF-FN-4 | `rfl` (eta definicional) | PASS |
| DEF-THM-5 | identidade à esquerda | `theorem Transition.id_comp (t) : (Transition.id α).comp t = t` | DEF-FN-3,4 | `rfl` (eta definicional) | PASS |
| DEF-THM-6 | identidade à direita | `theorem Transition.comp_id (t) : t.comp (Transition.id α) = t` | DEF-FN-3,4 | `rfl` (eta definicional) | PASS |

## BENCH-REL-001 — relações e composição relacional

Arquivo: `TamesisLab/Benchmark/Relations.lean`

| ID | Enunciado humano | Assinatura Lean | Dependências | Método | Build |
|---|---|---|---|---|---|
| REL-DEF-1 | relação binária local | `def BRel (α) : Type u := α → α → Prop` | — | definição | PASS |
| REL-DEF-2 | composição relacional | `def rcomp (R S : BRel α) : BRel α := fun a c => ∃ b, R a b ∧ S b c` | REL-DEF-1 | definição | PASS |
| REL-DEF-3 | relação identidade (diagonal) | `def rid : BRel α := fun a b => a = b` | REL-DEF-1 | definição | PASS |
| REL-THM-1 | associatividade da composição relacional | `theorem rcomp_assoc (R S T) : rcomp (rcomp R S) T = rcomp R (rcomp S T)` | REL-DEF-2 | `funext`/`propext` + `match`/`exact` | PASS |
| REL-THM-2 | identidade à esquerda | `theorem rcomp_rid_left (R) : rcomp rid R = R` | REL-DEF-2,3 | `funext`/`propext` + `cases`/`exact` | PASS |
| REL-THM-3 | identidade à direita | `theorem rcomp_rid_right (R) : rcomp R rid = R` | REL-DEF-2,3 | `funext`/`propext` + `cases`/`exact` | PASS |
| REL-DEF-4 | relação de adjacência declarada entre regimes, separada de `step` | `inductive Regime.Adj : Regime → Regime → Prop` (3 construtores explícitos) | DEF-TY-1 | indutivo | PASS |
| REL-THM-4 | a transição determinística respeita a relação declarada | `theorem Regime.step_adj (r) : Regime.Adj r r.step` | DEF-FN-1, REL-DEF-4 | `cases r <;> constructor` (análise finita) | PASS |

## BENCH-MATHLIB-001 — uso mínimo e controlado de Mathlib

Arquivo: `TamesisLab/Benchmark/MathlibInterop.lean`
(import único: `Mathlib.Data.Finset.Insert`)

| ID | Enunciado humano | Assinatura Lean | Dependências | Método | Build |
|---|---|---|---|---|---|
| ML-THM-1 | `alpha` pertence ao singleton `{alpha}` de `Finset` | `theorem alpha_mem_singleton : Regime.alpha ∈ ({Regime.alpha} : Finset Regime)` | DEF-TY-1, Mathlib | `Finset.mem_singleton_self` | PASS |
| ML-THM-2 | `beta` não pertence ao singleton `{alpha}` | `theorem beta_not_mem_singleton : Regime.beta ∉ ({Regime.alpha} : Finset Regime)` | DEF-TY-1, Mathlib | `simp` | PASS |

## BENCH-TEST-001 — importação e testes

Arquivo: `TamesisLab/Tests/BenchmarkSmoke.lean`

Importa `TamesisLab.Benchmark` e referencia todos os 15 teoremas acima por
nome, um `example` por teorema, com as mesmas assinaturas. Compila no grafo de
build (`TamesisLab.lean` importa `TamesisLab.Benchmark` e
`TamesisLab.Tests.BenchmarkSmoke`) e individualmente por
`lake env lean TamesisLab/Tests/BenchmarkSmoke.lean`.

Desvio registrado: a especificação previa `Tests/Benchmark.lean` na raiz Lean;
o arquivo foi criado como `TamesisLab/Tests/BenchmarkSmoke.lean` para entrar no
grafo de build da biblioteca `TamesisLab` (a raiz `Tests/` fica fora do alvo
padrão do `lake build`), seguindo o padrão já usado pelos smokes de Mathlib.

## Módulo raiz

`TamesisLab/Benchmark.lean` agrega os quatro módulos. `TamesisLab.lean`
importa o agregador e o teste.

## Totais

| Métrica | Valor |
|---|---|
| definições/estruturas/indutivos | 11 |
| teoremas | 15 |
| exemplos de referência no teste | 15 |
| `sorry` / `admit` / `axiom` / `unsafe` | 0 / 0 / 0 / 0 |
| `lake build` | PASS (8.676 jobs) |
| `lake env lean TamesisLab/Tests/BenchmarkSmoke.lean` | PASS (exit 0) |

Valor científico de todos os itens: NONE — INFRASTRUCTURE BENCHMARK.
