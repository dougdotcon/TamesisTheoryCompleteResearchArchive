---
artifact_id: FOUND-FUNCTIONAL-GRAPH-001
audit_status: PASS
lean_file: "05_FORMAL/lean/TamesisLab/Foundations/FunctionalGraphs/Counterexamples.lean"
---

# FOUND-FUNCTIONAL-GRAPH-001 — Auditoria de contraexemplos

Seis modelos, seis afirmações refutadas **distintas**. Todos em Lean,
nenhum experimento Python, nenhum `native_decide`.

## FFG-CE-001 — dois ciclos globais distintos

```text
a → a
b → b
```

```text
CE001.a_periodic : a ∈ periodicPts f
CE001.b_periodic : b ∈ periodicPts f
CE001.not_meets  : ¬ EventuallyMeets f a b
```

A negativa usa `iterate_a`/`iterate_b`, provados por indução: cada
trajetória é constante. Refuta a existência de um ciclo global único.

## FFG-CE-002 — cauda antes do ciclo

```text
a → b → c → c
```

```text
CE002.c_periodic     : c ∈ periodicPts f
CE002.reach_a_c      : IterReachable f a c        testemunha 2
CE002.meets_a_c      : EventuallyMeets f a c
CE002.iterate_ge_two : ∀ n, 2 ≤ n → f^[n] a = c
CE002.a_not_periodic : a ∉ periodicPts f
```

`a_not_periodic` é a forma **forte**: para período positivo algum. O caso
`n = 1` sai por `decide`; `n ≥ 2` por `iterate_ge_two`.

O teorema principal foi instanciado neste modelo, no teste isolado.

## FFG-CE-003 — ciclo de comprimento maior que um

```text
a ↔ b
```

```text
CE003.a_periodic : a ∈ periodicPts f       testemunha (2, _, rfl)
CE003.b_periodic : b ∈ periodicPts f
CE003.a_ne_b     : a ≠ b
CE003.not_fixed  : f a ≠ a
CE003.orbit_eq   : periodicOrbit f b = periodicOrbit f a
```

**`orbit_eq` não usa `decide`** — `periodicOrbit` é noncomputável. A prova
é `Function.periodicOrbit_apply_iterate_eq a_periodic 1`, aproveitando que
`b` é definicionalmente `f^[1] a`.

## FFG-CE-004 — mesmo componente sem alcance mútuo

```text
a → c ← b,  c → c
```

```text
CE004.meets_a_b              : EventuallyMeets f a b   testemunhas ⟨1, 1, rfl⟩
CE004.not_reach_a_b          : ¬ IterReachable f a b
CE004.not_reach_b_a          : ¬ IterReachable f b a
CE004.not_mutually_reachable : ¬ MutuallyReachable f a b
```

**Contraexemplo decisivo da frente.** É ele que sustenta a rejeição de
`MutuallyReachable` como definição de componente, decidida em
`COMPONENT_NOTIONS.md` e congelada em `FINAL_DEFINITIONS.md`.

As duas negativas usam `iterate_a_ge_one`/`iterate_b_ge_one`: a partir do
primeiro passo, ambas as trajetórias são constantes iguais a `c`.

## FFG-CE-005 — vários pontos cíclicos, uma única órbita

Reutiliza o modelo de `CE-003`, com pergunta diferente.

```text
CE005.distinct_points_same_orbit :
  a ≠ b ∧ a ∈ periodicPts f ∧ b ∈ periodicPts f ∧
  periodicOrbit f b = periodicOrbit f a
```

Refuta "um ponto periódico por componente" e **confirma** que o objeto
único é a órbita, não o representante.

## FFG-CE-006 — mesmo período mínimo, componentes distintos

```text
a0 ↔ a1     b0 ↔ b1
```

```text
CE006.a0_minimalPeriod : minimalPeriod f a0 = 2
CE006.b0_minimalPeriod : minimalPeriod f b0 = 2
CE006.same_period_different_component :
  minimalPeriod f a0 = minimalPeriod f b0 ∧ ¬ EventuallyMeets f a0 b0
```

### Versão forte formalizada — sem rebaixamento

O gate permitia a versão fraca com `igualdade dos períodos mínimos:
DEFERRED`. **Não foi necessário rebaixar.** A igualdade dos períodos
mínimos foi provada, pelo auxiliar `private minimalPeriod_eq_two`:

```text
1. IsPeriodicPt f 2 s                      por rfl
2. minimalPeriod f s ∣ 2                   IsPeriodicPt.minimalPeriod_dvd
3. 0 < minimalPeriod f s                   minimalPeriod_pos_of_mem_periodicPts
4. minimalPeriod f s ≤ 2                   Nat.le_of_dvd
5. minimalPeriod f s ≠ 1                   minimalPeriod_eq_one_iff_isFixedPt
                                           mais ¬ IsFixedPt f s por decide
6. minimalPeriod f s = 2                   omega
```

```yaml
minimal_period_equality: FORMALIZED
deferred: false
```

A distinção exigida pelo gate está explícita: `minimalPeriod f a0 =
minimalPeriod f b0` é **verdadeiro**, enquanto
`periodicOrbit f a0 = periodicOrbit f b0` é **falso** — é justamente o que
`¬ EventuallyMeets` mais `FFG-CYCLE-002` implicariam.

## Independência

```text
NAO foi provado que todas essas falhas ocorrem simultaneamente numa unica
funcao.

NAO foi provado que toda funcao finita exibe essas falhas.
```

`CE-003` e `CE-005` usam o mesmo sistema com perguntas diferentes, e isso
está declarado.

## Disciplina

Cinco namespaces com instância `Fintype` própria; `CE005` sem instância.
Nenhuma instância no namespace principal. Nenhum `native_decide`.
