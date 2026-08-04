---
document_id: FOUND-SPECTRAL-COUNTING-001-INFINITE-INSTANCE
work_item_id: FOUND-SPECTRAL-COUNTING-001
closes_gap: SC-GAP-001
probe_exit: 0
---

# SC-GAP-001 fechada — e a divida era real

## Por que esta lacuna importava

A instancia positiva de `FOUND-SPECTRAL-COUNTING-001` estava em
`EuclideanSpace ℝ (Fin 1)` — **dimensao finita**. Mas o conteudo do
teorema e justamente *espectro infinito, cada faixa acima de lambda
finita*. Em dimensao finita isso e quase trivial.

Sem a instancia infinita, o laboratorio nao sabia se tinha provado algo
com conteudo ou uma forma que so se realiza no caso degenerado.

## O que fechou

`463` linhas, `17` `#print axioms` todos limpos, `lake build` exit `0`,
`0` `sorry`. Espaco: `H2 := lp (fun _ : ℕ => ℂ) 2`, operador diagonal `T`
com `dseq i = 1/(i+1)`.

```lean
positive_instance_infinite_dimensional :
    ¬ FiniteDimensional ℂ H2 ∧ IsCompactOperator T ∧ IsSymmetric T ∧
    {μ | HasEigenvalue T μ}.Infinite ∧
    (∀ lam, 0 < lam → {μ | lam ≤ |μ| ∧ HasEigenvalue T μ}.Finite) ∧
    (∀ lam, 0 < lam → lam ≤ 1 → … .Nonempty) ∧
    (∀ lam, 0 < lam → lam ≤ 1 → 0 < eigCount T lam) ∧
    (∀ lam, 0 < lam → eigCount T lam = ⌊(1:ℝ)/lam⌋₊) ∧
    eigCount T (1/3) = 3
```

## A lei de contagem saiu EXATA

Foi pedido o caso `lam = 1/3`. Saiu a lei geral:

```lean
eigCount_eq_floor {lam : ℝ} (hlam : 0 < lam) :
    eigCount T lam = ⌊(1 : ℝ) / lam⌋₊
```

**Lei tipo Weyl exata, nao assintotica.** Via
`{μ | …} = dseq '' ↑(Finset.range ⌊1/lam⌋₊)` mais injetividade de `dseq`.

Instancias fechadas: `eigCount T 1 = 1`, `eigCount T (1/3) = 3`,
`eigCount T (1/10) = 10`, e o conjunto explicito
`{μ | 1/3 ≤ |μ| ∧ …} = {1, 1/2, 1/3}`.

## A peca que faltava era a RECIPROCA

```lean
eigenvalue_mem_range {μ : ℂ} (h : HasEigenvalue T μ) : ∃ i, (dseq i : ℂ) = μ
```

Sem ela o conjunto acima de `lam` e so limitado por cima, e o calculo
explicito e **impossivel**. A prova: `T f = μ • f` coordenada a
coordenada da `dseq i * f i = μ * f i`; `f ≠ 0` fornece `i` com
`f i ≠ 0`; `mul_right_cancel₀`.

Corolario: `0` **nao** e autovalor, e o espectro e exatamente
`range dseq`.

## Cross-check contra vacuidade

`eigCount_third_cross_check` recalcula o mesmo `3` por rota
**independente** — conjunto explicito com `ncard_insert_of_notMem` em vez
de `Finset.card_range`. Os dois batem.

E o zero e o zero **de verdade**, nao o junk do `ncard`:
`eigCount T 2 = 0` alimenta `eigCount_eq_zero_iff` e produz
`no_eigenvalue_above_two`.

`eigCount_antitone` deixa de ser vacuo por
`eigCount_strict_example : eigCount T (1/3) < eigCount T (1/10)`.

## O beco sem saida do agente anterior era desnecessario

A tentativa anterior parou em `Nontrivial (lp …)` nao sintetizar. **A
infinito-dimensionalidade nao sai de `Nontrivial`** — sai de autovetores
linearmente independentes:

```text
Module.End.eigenvectors_linearIndependent'
Module.Finite.not_linearIndependent_of_infinite
```

Nenhum `Nontrivial (lp …)` foi necessario em ponto algum.

## Armadilhas de nome registradas (Mathlib v4.33.0-rc1)

```text
Set.ncard_coe_Finset   NAO EXISTE. E Set.ncard_coe_finset, f minusculo.
push_neg               DEPRECIADO. A forma corrente e  push Not at h.
```

## Consequencia

A instancia de dimensao finita `positive_instance_concrete` fica
**estritamente subsumida**. O teorema tem conteudo onde importa.
