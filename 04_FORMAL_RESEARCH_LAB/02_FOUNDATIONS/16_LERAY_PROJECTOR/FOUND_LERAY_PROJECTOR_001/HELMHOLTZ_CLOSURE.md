---
document_id: FOUND-LERAY-PROJECTOR-001-HELMHOLTZ-CLOSURE
work_item_id: FOUND-LERAY-PROJECTOR-001
closes_gap: LP-GAP-003
probe_exit: 0
---

# Helmholtz fechou — no simbolo E no operador

`582` linhas, `54` declaracoes, `42` `#print axioms` todos
`[propext, Classical.choice, Quot.sound]`, `lake build` exit `0`,
`0` `sorry`.

## `Id - P = grad (Laplace)^-1 div` e IDENTIDADE PROVADA, nao analogia

```lean
gradSymbol b x j     := I * ⟪x, b j⟫
divSymbol b x k      := I * ⟪x, b k⟫
invLaplaceSymbol x   := -1 / ‖x‖^2

gradInvLapDiv_eq_qMatrix :
    gradSymbol b x j * invLaplaceSymbol x * divSymbol b x k = qMatrix b x j k
```

Provada **em ℂ**, com `i² = −1` cancelando o sinal de `Δ⁻¹`. Era prosa no
registro anterior; agora e teorema.

## O complemento e projecao de posto 1 sobre a direcao longitudinal

```lean
qMatrixR b x j k := ⟪x, b j⟫ * ⟪x, b k⟫ / ‖x‖^2
qMatrixR_rank_one : qMatrixR b x j k = (⟪x,b j⟫/‖x‖) * (⟪x,b k⟫/‖x‖)   -- Q = u ⊗ u
qMatrixR_idem, qMatrixR_symm, trace_qMatrixR = 1
qMatrixR_apply_inner (hx) : ∑ k, qMatrixR b x j k * ⟪x, b k⟫ = ⟪x, b j⟫  -- Q(ξ)ξ = ξ
```

E a decomposicao, sem hipotese sobre `x`:

```lean
helmholtz_symbol :
    (∑ k, lerayMatrixR · ⟪v, b k⟫) + (∑ k, qMatrixR · ⟪v, b k⟫) = ⟪v, b j⟫
lerayMatrixR_mul_qMatrixR (hx) : ∑ k, lerayMatrixR · qMatrixR · = 0
qMatrixR_mul_lerayMatrixR (hx) : ∑ k, qMatrixR · lerayMatrixR · = 0
```

`P` retira a componente longitudinal, `Q` **e** ela, e as duas se
aniquilam nos dois sentidos.

## No operador

```lean
qOpL2 b := id - lerayOpL2 b

lerayOpL2_add_qOpL2  : P f + Q f = f
lerayOpL2_comp_qOpL2 : P ∘L Q = 0        qOpL2_comp_lerayOpL2 : Q ∘L P = 0
qOpL2_idem           : Q ∘L Q = Q
adjoint_qOpL2        : Q* = Q            isSelfAdjoint_qOpL2
norm_qOpL2_le_one    : ‖Q‖ ≤ 1
norm_sq_helmholtz    : ‖f‖^2 = ‖P f‖^2 + ‖Q f‖^2
```

## Bonus nao pedido: `Q` e multiplicador, nao so `1 - P`

```lean
fourierMulL2 ℂ (oneL2 E) = id
lerayEntryL2 + qEntryL2 = (if j = k then oneL2 else 0)     -- em L∞
coordProj_qOpL2 :
    (coordProj E q) (qOpL2 b f)
      = ∑ k, fourierMulL2 ℂ (qEntryL2 b q k) ((coordProj E k) f)
```

`Q` **e** o multiplicador matricial de simbolo `ξ_qξ_k/‖ξ‖²`. Sem isso a
anti-vacuidade abaixo nao sairia.

## Anti-vacuidade nos DOIS lados, no nivel do operador

```lean
qOpL2_ne_zero [Nontrivial E] : qOpL2 b ≠ 0
```

Se `Q = 0`, todo `qEntryL2` seria `0` em `L∞`, logo o traco do simbolo
seria `0` q.t.p.; mas `trace_qMatrixR = 1` em todo `ξ ≠ 0`. Contradicao.

Junto com `lerayOpL2_ne_zero` ja provado, a decomposicao e **nao trivial
dos dois lados**, e nao so no simbolo.

## Instancia positiva concreta

Em `ℝ³`, `ξ = b3 0`, `v = b3 0 + b3 1`:

```text
Q(ξ)v = 1  (componente longitudinal)     nao nula
P(ξ)v = 1  (componente solenoidal)       nao nula
soma = v, aniquilacao mutua, trace Q = 1, Q² = Q
```

## Dois travamentos, ambos triviais

```text
lerayMatrixR_eq_sub        ring dava "No goals" — o simp only ja fechava
lerayEntryL2_add_qEntryL2  Lp.coeFn_zero entrega 0 x em forma Pi.zero;
                           faltava Pi.zero_apply no simp only
```

Nenhum travamento matematico restante.

## O que ainda NAO e afirmado

```text
que Navier-Stokes tenha ficado alcancavel
que a pressao esteja recuperada de uma solucao
que exista teoria de EDP no laboratorio
```

O projetor esta completo como **objeto**: ortogonal, cota `1`, Helmholtz
provada. Isso e a peca que a medicao de NS disse faltar — **peca, nao
solucao**. **Nenhum problema de milenio foi atacado.**
