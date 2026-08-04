---
document_id: FOUND-SPECTRAL-COUNTING-001-CLOSURE-RECORD
work_item_id: FOUND-SPECTRAL-COUNTING-001
work_status: VERIFIED
result_review: APPROVED
gate_combination_declared: true
---

# Registro de encerramento

## Desvio de protocolo, declarado

Os gates de especificacao, revisao de especificacao, formalizacao e
revisao de resultado foram **combinados num commit**. O motivo e
registrado em vez de escondido: a sondagem ja havia produzido a prova
inteira com `exit 0`, e o material entrou na arvore sem alteracao de
enunciado.

O que **nao** foi pulado: probe com `exit 0`, `lake build` com `exit 0`,
pegada medida, instancia positiva verificada, e ausencia de `sorry`
conferida por grep. O que foi pulado e a **separacao em quatro commits**.

## O resultado

```lean
theorem finite_eigenvalues_above
    (hc : IsCompactOperator T) (hs : (T : H →ₗ[𝕜] H).IsSymmetric)
    (hlam : 0 < lam) :
    {μ : ℝ | lam ≤ |μ| ∧ HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜)}.Finite
```

**Mais forte que o alvo**: `CompleteSpace H` **nao e necessario**. O
alvo verbatim fica como corolario, `finite_eigenvalues_above_target`.

## A prova evita Pitagoras

O argumento classico usa `‖Tv - Tw‖² = μ² + ν²`. Aqui usa-se
Cauchy-Schwarz contra o proprio autovetor:

```text
<v, Tv - Tw> = μ‖v‖² - ν<v,w> = μ
logo  |μ| <= ‖v‖ ‖Tv - Tw‖ = ‖Tv - Tw‖
```

Separacao `lam` em vez de `sqrt 2 · lam`, e **sem `Real.sqrt`**. Uma
linha de `rw` fecha a estimativa.

## N(lambda) deixou de ser junk

```text
eigCount_eq_finset_card    existe Finset F com F.card = eigCount
eigCount_eq_zero_iff       <- o ponto: so vale porque a finitude veio antes
exists_of_eigCount_pos     contagem positiva exibe autovalor de verdade
eigCount_antitone          FALSO para o valor junk
eigCount_eq_natCard        bate com Nat.card do subtipo
```

`Set.ncard` devolve `0` tambem para conjunto infinito. Sem a finitude,
`eigCount T lam = 0` seria demonstravel e vazio.

## Instancia positiva

`rankOne v := (innerSL 𝕜 v).smulRight v`, projecao de posto 1, com
compacidade **provada a mao** — o Mathlib nao tem "posto finito implica
compacto". Mais `positive_instance_concrete` em
`EuclideanSpace ℝ (Fin 1)`, fechada.

## Numeros

```text
linhas                      257
declaracoes                 14
lake build                  exit 0, 8812 jobs
sorry / admit / axiom       0
pegada                      propext, Classical.choice, Quot.sound
CompleteSpace necessario    NAO
```

## Frente nova, nao colagem

O Mathlib **nao tem** lema de espectro discreto fora de 0. Em
`Compact/FredholmAlternative.lean` ha so
`antilipschitz_of_not_hasEigenvalue`,
`hasEigenvalue_or_mem_resolventSet` e `hasEigenvalue_iff_mem_spectrum`.

`ContinuousLinearMap.finite_dimensional_eigenspace` e
`orthogonalComplement_iSup_eigenspaces_eq_bot`, que a especificacao
previa usar, **nao foram necessarios**.

## O que fica aberto

```text
SC-GAP-001  instancia positiva em dimensao INFINITA concreta.
            Nontrivial (lp ...) nao sintetiza no v4.33.0-rc1.
            O positive_instance parametrico vale para qualquer H com
            vetor unitario, inclusive infinito-dimensional; falta o
            testemunho concreto.
SC-GAP-002  enumeracao Nat -> R monotona e HilbertBasis de autovetores.
            DELIBERADAMENTE ABERTA: ~500+ linhas e NAO e necessaria
            para N(lambda).
SC-GAP-003  imports estreitos. O probe usava import Mathlib; a promocao
            estreitou para 4 modulos, mas nao foi minimizada.
```

## O que NAO e afirmado

```text
que a lei de Weyl esteja provada
que RH tenha ficado alcancavel
que N(lambda) sozinho valha algo para RH
```

**Nenhum problema de milenio foi atacado.**
