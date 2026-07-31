---
artifact_id: FOUND-SEMIGROUP-002
audit_status: PASS
lean_file: "05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics/Counterexamples.lean"
---

# FOUND-SEMIGROUP-002 — Auditoria de contraexemplos

Cinco modelos, todos verificados em Lean. **Nenhum experimento Python.**
Nenhum `native_decide`.

## Correção obrigatória aplicada em CE-001

A especificação original propunha refutar a simetria de `Reachable` com o
grafo de uma função `f : X → X` — `0 → 1`, `1 → 1`. **Isso estava errado**:
`Reachable` foi definida pela **ação completa** do monoide, e o grafo de uma
função isolada refuta apenas a alcançabilidade por iterações **daquele
gerador**.

`CE-001` foi reconstruído como **ação genuína de monoide**, com todas as
leis verificadas antes da instanciação.

## CE-001 — alcançabilidade não é simétrica

```text
Tr = { idT, collapse }        monoide, comp associativa, idT bilateral
St = { zero, one }
act idT s      = s
act collapse s = one
```

Leis provadas **antes** das instâncias, na ordem do laboratório:

| Lei | Lean | Método |
|---|---|---|
| associatividade | `CE001.comp_assoc` | `decide` (8 casos) |
| identidade à esquerda | `CE001.idT_comp` | `rfl` |
| identidade à direita | `CE001.comp_idT` | `cases` + `rfl` |
| compatibilidade da ação | `CE001.act_comp` | `decide` (8 casos) |

Só então: `instance : Monoid Tr`, `instance : MulAction Tr St`.

Resultado:

```lean
CE001.reachable_zero_one     : Reachable (M := Tr) zero one
CE001.not_reachable_one_zero : ¬ Reachable (M := Tr) one zero
CE001.reachable_not_symmetric : ambos
```

A negativa é sobre **todo o monoide**: `act_one` mostra que *nenhuma* das
duas transformações move `one`.

## CE-002 — uma ação finita não precisa ser transitiva

Monoide trivial `{idT}` agindo pela identidade sobre `{a, b}`. Duas órbitas
disjuntas.

```lean
CE002.not_reachable_a_b : ¬ Reachable (M := Tr) a b
CE002.not_transitive    : ∃ x y, ¬ Reachable (M := Tr) x y
```

## CE-003 — cauda antes do ciclo

Camada C pura: `f : St → St`, `s0 ↦ s1 ↦ s2 ↦ s2`. **Sem monoide** — e é
correto que não haja, porque o enunciado refutado é sobre iteração de
função.

```lean
CE003.not_fixed          : f s0 ≠ s0
CE003.iterate_one        : f^[1] s0 = s1
CE003.iterate_two        : f^[2] s0 = s2
CE003.eventually_fixed   : f^[2+1] s0 = f^[2] s0        (mu = 2, lam = 1)
CE003.iterate_ge_two     : ∀ n, 2 ≤ n → f^[n] s0 = s2
CE003.s0_not_periodic    : ¬ ∃ n, 0 < n ∧ f^[n] s0 = s0
CE003.periodic_point_is_tail : IsPeriodicPt f 1 (f^[2] s0)
```

`s0_not_periodic` é a forma **forte** — para *todo* período positivo, não
apenas para os pequenos. O gate a tratava como opcional; ela saiu barata
via `iterate_ge_two`, provada por indução com
`Function.iterate_succ_apply'`, e vale a pena porque é ela que sustenta a
afirmação sobre `minimalPeriod`.

Consequência registrada: `Function.minimalPeriod f s0 = 0`, pois
`s0 ∉ periodicPts f`. Usá-lo como "período eventual" daria `λ = 0`,
contradizendo `0 < λ`. O ponto periódico é `f^[2] s0`.

O teorema principal foi instanciado neste modelo no teste isolado.

## CE-004 — uma ação finita não precisa ser fiel

O **mesmo** monoide de `CE-001` agindo sobre um tipo de um único estado.

```lean
CE004.not_faithful : ∃ a b : CE001.Tr, a ≠ b ∧ ∀ s : CE004.St, a • s = b • s
```

Testemunhas: `idT` e `collapse`. Sobre um único ponto, ambas são a
identidade. Consequência: **a Camada B não determina a Camada A** — ações
distintas podem induzir a mesma função.

Nota de disciplina de instâncias: reutilizar `CE001.Tr` com um `X`
diferente **não** cria conflito, porque a instância é
`MulAction CE001.Tr CE004.St`, distinta de `MulAction CE001.Tr CE001.St`.

## CE-005 — um invariante não separa órbitas

Reutiliza o modelo de `CE-002`, com `I : St → PUnit` constante.

```lean
CE005.I_isInvariant : IsInvariant (M := CE002.Tr) I
CE005.invariant_does_not_separate_orbits :
  IsInvariant I ∧ I a = I b ∧ ¬ Reachable a b
```

Consequência: a **recíproca** de `IsInvariant.of_reachable` é falsa. Um
invariante **refuta** alcançabilidade quando difere; nunca a demonstra.

## Cobertura das negativas

| Negativa | Contraexemplo | Estado |
|---|---|---|
| alcançabilidade não é simétrica | `CE-001` | verificado |
| ação finita não precisa ser transitiva | `CE-002` | verificado |
| órbita pode ter cauda | `CE-003` | verificado |
| eventual ≠ periódico desde `n = 0` | `CE-003` | verificado |
| ação finita não precisa ser fiel | `CE-004` | verificado |
| ações distintas, mesma função em `X` | `CE-004` | verificado |
| invariante constante em duas órbitas | `CE-005` | verificado |
| invariante não separa órbitas | `CE-005` | verificado |
| **o período depende do estado inicial** | — | **ainda sem modelo** |

A última permanece registrada em `FSG2-GAP-007` e **não é afirmada** em
lugar algum. O modelo é trivial de construir, mas o gate especificou cinco
contraexemplos e nenhum a cobre; preferiu-se manter a pendência a afirmar
uma negativa sem exemplo.

## Método

Todas as leis finitas foram provadas por `decide` sobre termos pequenos e
transparentes (no máximo 8 casos), ou por `rfl`/`cases`. **Nenhum
`native_decide`.** Cada modelo vive em namespace próprio.
