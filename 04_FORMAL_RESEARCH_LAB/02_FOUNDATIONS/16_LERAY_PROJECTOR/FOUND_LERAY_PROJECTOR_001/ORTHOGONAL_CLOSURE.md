---
document_id: FOUND-LERAY-PROJECTOR-001-ORTHOGONAL-CLOSURE
work_item_id: FOUND-LERAY-PROJECTOR-001
closes_gaps:
  - LP-GAP-001
  - LP-GAP-002
probe_exit: 0
---

# `P` e projecao ORTOGONAL, e a cota e exatamente 1

`379` linhas, `24` declaracoes, `lake build` exit `0`, `0` `sorry`,
`23` `#print axioms` todos `[propext, Classical.choice, Quot.sound]`.

## LP-GAP-002 — autoadjuncao, na forma forte

```lean
inner_lerayOpL2_symm (b) (f g) : ⟪lerayOpL2 b f, g⟫ = ⟪f, lerayOpL2 b g⟫
adjoint_lerayOpL2 (b) : adjoint (lerayOpL2 b) = lerayOpL2 b
isSelfAdjoint_lerayOpL2 (b) : IsSelfAdjoint (lerayOpL2 b)
```

Eu previa que `adjoint` talvez nao estivesse disponivel e que a forma
fraca `⟪Pf,g⟫ = ⟪f,Pg⟫` fosse o maximo. **Estava errado**: `Lp F 2` e
Hilbert, `CompleteSpace` sai por `infer_instance`, e as tres formas
fecham. Sem hipotese `[Nontrivial E]`.

A cadeia: entrada real implica multiplicacao por `L∞` simetrica;
Plancherel **em forma de produto interno ja existe no Mathlib**
(`MeasureTheory.Lp.inner_fourier_eq`); `coordIncl` e `coordProj` sao
mutuamente adjuntos; e a troca `j↔k` fecha por `lerayEntryL2_symm`.

## LP-GAP-001 — a cota nao so melhorou, e ATINGIDA

```lean
norm_lerayOpL2_le_one [Nontrivial E] (b) : ‖lerayOpL2 b‖ ≤ 1
norm_lerayOpL2_eq_one_of_two_le [Nontrivial E] (b) (hn : 2 ≤ n) :
    ‖lerayOpL2 b‖ = 1
```

```text
antes   2n^2      para n = 3:  18
agora   1         e IGUAL a 1, nao apenas <= 1
```

**A rota de Plancherel operador-valorado nao foi necessaria** — e ainda
bem, porque ela **nao existe no Mathlib**. A cota otima cai de graca de
GAP-002 mais idempotencia:

```text
‖Pf‖^2 = <Pf, Pf> = <f, P^2 f> = <f, Pf> <= ‖f‖ ‖Pf‖
```

Cauchy-Schwarz, e pronto. Eu tinha registrado que a cota otima
"exigiria Plancherel matricial" — **isso tambem estava errado**.

## Projecao ortogonal completa

```lean
inner_lerayOpL2_sub (b) (f) : ⟪lerayOpL2 b f, f - lerayOpL2 b f⟫ = 0
norm_sq_lerayOpL2_pythagoras (b) (f) :
    ‖f‖^2 = ‖lerayOpL2 b f‖^2 + ‖f - lerayOpL2 b f‖^2
```

Autoadjunta, idempotente, contracao, e decomposicao de Pitagoras. **`P` e
projecao ortogonal.** A proibicao registrada em `DEC-053` — *nao chamar
`lerayOpL2` de projecao ortogonal* — fica **revogada por prova**.

## Nao-vacuidade, exigida pela regra e nao pedida no gate

`adjoint P = P` seria vacuo se `P = 0`. Nao e:

```lean
lerayOpL2_ne_zero [Nontrivial E] (b) (hn : 2 ≤ n) : lerayOpL2 b ≠ 0
```

O argumento e bonito e vale registrar: se `P = 0`, cada
`fourierMulL2 (lerayEntryL2 b q j) = 0`; conjugando pela isometria de
Plancherel, o simbolo `L∞` aniquila **todo** `L²`; testando com
indicadores de `closedBall 0 R` para `R : ℕ`, o simbolo e a.e. nulo; mas
o **traco** do simbolo e `n − 1` em todo `ξ ≠ 0` — extraindo um ponto por
`NeBot (ae volume)` sai `n = 1`, contra `2 ≤ n`.

Instanciado: `lerayOpL2 b3 ≠ 0 ∧ ‖lerayOpL2 b3‖ = 1` em `ℝ³`.

## Armadilhas registradas

```text
volume_tac para Lp (α := E) F 2  falha de forma INTERMITENTE — o mesmo
    binder passa numa declaracao e falha na seguinte. Solucao: abbrev.
local notation "VF" E n => ...   quebra o parser em (VF E n). Usar abbrev.
inner_self_eq_norm_sq_to_K       produz RCLike.ofReal, que NAO e
    sintaticamente Complex.ofReal; rw nao fecha por rfl, precisa simp.
```

## Duas previsoes minhas, ambas erradas

```text
previ   adjoint pode nao estar disponivel; forma fraca e o maximo
saiu    as tres formas fecham

previ   cota otima exige Plancherel matricial, que nao existe
saiu    cai de Cauchy-Schwarz em tres linhas
```

## O que ainda NAO e afirmado

```text
Id - P = grad (Laplace)^-1 div explicitamente   LP-GAP-003, aberta
a versao H^s matricial                          LP-GAP-004, em execucao
que Navier-Stokes tenha ficado alcancavel
```

**Nenhum problema de milenio foi atacado.**
