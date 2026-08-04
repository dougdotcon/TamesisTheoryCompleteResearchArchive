---
document_id: PORTFOLIO-REVIEW-SPECTRAL-COUNTING-2026-08-04
reviewed_at: 2026-08-04
selected_work_item: FOUND-SPECTRAL-COUNTING-001
probe_exit: 0
positive_instance_built_before_gate: true
---

# Revisao de portfolio — a Peca B, com corte medido

## O que a sondagem achou

`N(lambda)` **elabora hoje**, em quatro variantes. O obstaculo nao e
tipagem — e **vacuidade por junk value**:

```text
Nat.card, Module.finrank e Set.ncard devolvem 0 em conjunto infinito
logo  N(lambda) = 0  e demonstravel e VAZIO sem prova de finitude
```

E o mesmo defeito que derrubou `FOUND-MONOVARIANT-DESCENT-001`, achado
**antes** de custar um gate.

## A instancia positiva ja esta construida

`exit 0`, sem `sorry`, axiomas `[propext, Classical.choice, Quot.sound]`.

```text
operador   diagonal em lp (fun _ : Nat => C) 2, d_i = 1/(i+1)
compacto   PROVADO, ~90 linhas, sem nenhuma API de lp para operadores
autoadj.   PROVADO via lp.inner_eq_tsum
espectro   INFINITO, provado por injetividade de d
```

Nao existe `lp.diagonal` nem acao de `lp infinito` sobre `lp p` no
Mathlib. O operador foi construido do zero com `Memℓp.mono`,
`lp.norm_mono` e `LinearMap.mkContinuous`; a compacidade veio de
truncacoes de posto finito mais `isCompactOperator_of_tendsto`.

**A regra `positive_instance_required` esta satisfeita antes de a frente
abrir.** E a primeira vez que isso acontece neste laboratorio.

## O gargalo e UM teorema

```text
autovalores de operador compacto nao acumulam fora de 0
```

Ingredientes, todos ja no Mathlib:

```text
LinearMap.IsSymmetric.orthogonalFamily_eigenspaces
IsCompactOperator.isCompact_closure_image_closedBall
ContinuousLinearMap.finite_dimensional_eigenspace
ContinuousLinearMap.orthogonalComplement_iSup_eigenspaces_eq_bot
```

Argumento padrao: `‖T e_n - T e_m‖^2 = mu_n^2 + mu_m^2 >= 2 lambda^2`.

## O CORTE, que e a decisao desta revisao

A Peca B divide-se em duas de tamanhos muito diferentes:

```text
(i)  N(lambda) como contagem genuina     ~200-300 linhas   MODERATE
(ii) enumeracao Nat -> R monotona
     e HilbertBasis de autovetores       ~500+ linhas      HIGH
```

**Esta frente cobre so (i).** E (ii) **nao e necessaria** para
`N(lambda)` — a versao finita do Mathlib usa `Tuple.sort` sobre `Fin n`,
que nao tem analogo em `Nat`, e replicar isso seria custo sem retorno
para o alvo.

`(ii)` fica declarada como `SC-GAP-002`, aberta de proposito.

## Evidencia de que e frente nova

```text
17 nomes candidatos sondados   0 existem
 4 buscas exact?                0 fecham
```

Nao e colagem de API existente.

## O que esta selecao NAO afirma

```text
que RH tenha ficado alcancavel
que a lei de Weyl fique provada
que N(lambda) sozinho valha alguma coisa para RH
```

O valor e **upstream e independente de RH**: hoje "lei de contagem de
Weyl" nao tem enunciado tipavel, e esta frente a torna enunciavel sob
hipotese explicita. So isso.
