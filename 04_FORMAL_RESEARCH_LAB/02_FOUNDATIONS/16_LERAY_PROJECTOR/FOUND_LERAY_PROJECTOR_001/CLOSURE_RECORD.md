---
document_id: FOUND-LERAY-PROJECTOR-001-CLOSURE-RECORD
work_item_id: FOUND-LERAY-PROJECTOR-001
work_status: VERIFIED
result_review: APPROVED
gate_combination_declared: true
closes_gap: FM-GAP-002
---

# Registro de encerramento

## O projetor de Leray esta construido em L2

```lean
lerayOpL2 b : Lp E (EuclideanSpace ℂ (Fin n)) 2 →L[ℂ] Lp E (EuclideanSpace ℂ (Fin n)) 2
norm_lerayOpL2_le : ‖lerayOpL2 b‖ ≤ 2 * (n : ℝ)^2
lerayOpL2_idem [Nontrivial E] : lerayOpL2 b ∘L lerayOpL2 b = lerayOpL2 b
```

`561` linhas, `42` declaracoes, `lake build` exit `0`, `0` `sorry`,
`29` `#print axioms` todos `[propext, Classical.choice, Quot.sound]`.

## A forma escolhida, e por que

Familia finita indexada por base ortonormal, **nao** `Lp (F →L[ℂ] F) ∞`:

```lean
lerayMatrixR b x j k : ℝ :=
  (if j = k then 1 else 0) - ⟪x, b j⟫_ℝ * ⟪x, b k⟫_ℝ / ‖x‖^2
```

Tres razoes, todas medidas:

```text
1. reusa literalmente norm_lerayComponent_le da arvore, via
   lerayMatrix b x j k = delta_jk - lerayComponent (b j) (b k) x
2. o operador vira SOMA FINITA de fourierMulL2 escalares, e nao
   existe Lp.norm_smul_le operador-valorado no Mathlib
3. a soma sum_k xi_k^2 = ‖xi‖^2 sai de
   OrthonormalBasis.sum_inner_mul_inner, que e exatamente o que a
   idempotencia precisa
```

**Custo declarado da escolha**: a cota sai `2n²` em vez da otima `1`.

## A idempotencia fechou em TRES niveis

```text
1. pontual do simbolo      P(xi)^2 = P(xi)   para xi != 0
2. do simbolo em L-infinito                  q.t.p.
3. DO OPERADOR em L2       lerayOpL2 ∘L lerayOpL2 = lerayOpL2
```

Foi pedido o nivel 1. Fecharam os tres.

## O calculo de multiplicadores virou algebra

```lean
fourierMulL2_comp : fourierMulL2 F g ∘L fourierMulL2 F h = fourierMulL2 F (g • h)
fourierMulL2_add, fourierMulL2_sum, fourierMulL2_zero
```

E **homomorfismo de algebra**, nao so um operador solto.

## As propriedades do projetor

```lean
lerayMatrixR_idem          P^2 = P
lerayMatrixR_apply_inner   soma_k P_jk <x, b k> = 0   -- MATA GRADIENTES
lerayMatrixR_symm          simetrico
trace_lerayMatrixR         traco = n - 1
norm_lerayMatrix_le        entradas limitadas por 2
measurable_lerayMatrix
```

O traco `n − 1` e a assinatura do projetor sobre campos solenoidais:
retira exatamente **uma** dimensao, a longitudinal.

## Instancia positiva NAO TRIVIAL

`nonvacuous_leray_R3` em `EuclideanSpace ℝ (Fin 3)` com
`b3 = EuclideanSpace.basisFun`:

```text
P ∘ P = P             ‖P‖ ≤ 18
em xi = b3 0 != 0:    P_00 = 0,  P_11 = 1,  traco = 2
logo                  P != 0  e  P != Id
```

**Projecao nao trivial.** Sem isso o resultado seria forma sem
satisfazibilidade — a quarta vez que essa checagem importa nesta sessao.

E o simbolo **nao e temperado**, logo o operador do Mathlib colapsa em
`0` nele: `not_hasTemperateGrowth_lerayComponent`, ja na arvore.

## O que falta e refinamento, NAO existencia

```text
LP-GAP-001  cota otima ‖P‖ <= 1. Tenho 2n^2. Exigiria Plancherel
            matricial em vez de soma triangular.
LP-GAP-002  P como projecao ORTOGONAL. lerayEntryL2 e real-valorada,
            logo conjugacao-invariante, mas P* = P NAO foi provado.
LP-GAP-003  Id - P = grad (Laplace)^-1 div, explicitamente.
LP-GAP-004  a versao em H^s do operador MATRICIAL. O escalar ja esta
            na arvore via MemSobolev.existsUnique_fourierMulL2, e o
            bloqueio e FM-GAP-001: nao ha TIPO de espaco de Sobolev.
```

## O que NAO e afirmado

```text
que Navier-Stokes tenha ficado alcancavel
que a pressao esteja recuperada
que P seja projecao ortogonal      -- LP-GAP-002
que a cota seja otima              -- LP-GAP-001
```

**Nenhum problema de milenio foi atacado.** O que existe e um operador
limitado idempotente em L2 com o simbolo certo.
