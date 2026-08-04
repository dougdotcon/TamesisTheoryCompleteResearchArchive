---
document_id: FOUND-ELLIPTIC-HEIGHT-001-CLOSURE-RECORD
work_item_id: FOUND-ELLIPTIC-HEIGHT-001
work_status: VERIFIED
result_review: APPROVED
gate_combination_declared: true
discharges_mathlib_todo: true
---

# Registro de encerramento

## O que fechou

A obrigacao **D** da Peca C, **todos os ramos**:

```lean
addSubMap_eval_sym2x (P Q : W.Point) :
    ∃ c : F, c ≠ 0 ∧
      (fun i ↦ (addSubMap W i).eval (P.sym2x Q)) = c • ((P+Q).sym2x (P-Q))
```

| ramo | testemunha `c` |
|---|---|
| `(0,0)`, `(0,P)`, `(P,0)` | `1` |
| `x₁ = x₂` (P=Q e Q=−P colapsam) | via `dupMain` |
| 2-torcao, `ψ = 0` | `f₀` |
| duplicacao, `ψ ≠ 0` | `f₁ = ψ²` |
| secante generica, `x₁ ≠ x₂` | `(x₁ − x₂)²` |

**Nada ficou em aberto.**

## Os corolarios, agora INCONDICIONAIS

```lean
parallelogram (W) [W.IsElliptic] :
    ∃ C, ∀ P Q, |h(P+Q) + h(P−Q) − 2*(h P + h Q)| ≤ C

torsion_finite (W) [W.IsElliptic] [Northcott ...] :
    Finite (AddCommGroup.torsion W.toAffine.Point)
```

**A finitude da torcao de `E(K)` sai SEM qualquer forma de Mordell-Weil
fraco.** Era a previsao da medicao, e confirmou-se.

E `pecaC_conditional_on_F` isola **F como a unica hipotese restante**
para `AddGroup.FG`.

## Descarrega TODO do Mathlib

O TODO de `Mathlib/NumberTheory/Height/EllipticCurve.lean` tem tres
itens, e os tres estao cobertos:

```text
Define the naive height                              FEITO
Add the further ingredients needed for the
  approximate parallelogram law                      FEITO
Add the statement and proof of the approximate
  parallelogram law                                  FEITO
```

E o TODO de `Affine/AddSubMap.lean` — *"Show that the map really does
what it is claimed to do"* — esta provado **no nivel de x-coordenadas**,
que e exatamente o enunciado do docstring.

## A previsao de metodo que ESTAVA ERRADA

Eu previ `field_simp; ring` sobre funcoes racionais grandes. **Falha** —
rebenta num termo com `(4y² + 4a₁xy + …)⁻¹` espalhado.

A rota que funciona:

```text
1. limpar denominadores UM FATOR DE CADA VEZ
   hx₃ : (x₁−x₂)^2 * addX … = N₃    (so ai field_simp; ring)
2. tratar addX como ATOMO e fechar com linear_combination,
   usando as duas equacoes de Weierstrass como certificados
   de pertinencia ao ideal
3. mul_left_cancel₀ (pow_ne_zero 2 hd) para dividir por (x₁−x₂)²
   sem field_simp
```

## O custo real nao estava no Lean

Nao havia CAS no ambiente. Os quatro certificados de ideal foram obtidos
com um **redutor polinomial multivariado escrito em Python puro** (~90
linhas, divisao por `E₁` monico em `y₁` e `E₂` monico em `y₂`), todos com
resto `0`:

```text
soma        N₃ + N₄ − f₁       = 2E₁ + 2E₂
produto     N₃N₄ − f₀·d²       = q₁E₁ + q₂E₂   (q grau 3)
duplicacao  f₁ᴰ − ψ²           = −4E₁
            f₀ᴰ − (ν² + a₁νψ − (a₂+2x)ψ²) = (4a₂+a₁²+8x)·E₁
```

**O gargalo era encontrar os multiplicadores, nao prova-los.**

## Armadilha registrada

`rw [sub_eq_add_neg]` reescreve primeiro o **escalar** `(x₁−x₂)`, nao a
subtracao de **pontos**. E preciso fazer o `rw` **antes** do
`refine ⟨(x₁−x₂)^2, …⟩`.

## Numeros

```text
linhas                361
lake build            exit 0, 8814 jobs
sorry / axioma local    0
pegada                propext, Classical.choice, Quot.sound
teorema D               ~120 linhas + ~45 de plumbing
compilacao              6.7 s
```

## Estimativa revista

```text
antes   moderate-high, 300-600 linhas, dias a semana
agora   pequeno: 120 linhas, uma sessao
```

## Instancia positiva

`Wq : WeierstrassCurve ℚ := ⟨0,0,0,0,1⟩` (`y² = x³ + 1`), pontos
`Pa = (2,3)` e `Pb = (0,1)` com `Pa ≠ 0`, `Pb ≠ 0`, `Pa ≠ Pb` provados.
`D_lhs_at_Pa_Pb` computa o lado esquerdo como `![-8, 4, 4] ≠ 0` — **a
igualdade de D nao e degenerada**.

## Ressalva honesta

Isto e um probe promovido em estilo e namespace de laboratorio, **nao um
PR ao Mathlib**. Portar exigiria mover `naiveH`/`xC` para namespaces
corretos, reduzir os `linear_combination` gigantes a formato aceitavel, e
acrescentar as variantes `map` e `baseChange`.

## O que NAO e afirmado

```text
que BSD tenha ficado alcancavel
que Mordell-Weil esteja provado    -- falta F, escala de meses
que isto seja contribuicao aceita no Mathlib
```

**Nenhum problema de milenio foi atacado.**
