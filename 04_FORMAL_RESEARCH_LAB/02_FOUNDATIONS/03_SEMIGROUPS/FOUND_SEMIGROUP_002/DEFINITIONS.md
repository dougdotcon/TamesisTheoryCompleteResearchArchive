# FOUND-SEMIGROUP-002 — Definições

## Separação obrigatória das três camadas

O erro que esta especificação existe para evitar é tratar como um só objeto
três coisas distintas.

| Camada | Objeto | Quantificação | Pertence a |
|---|---|---|---|
| **A** | ação completa de `M` sobre `X` | `∃ m : M` | alcançabilidade, órbita, invariante |
| **B** | dinâmica de um `a : M` fixo | `∃ n : ℕ`, sobre `a ^ n` | periodicidade da ação |
| **C** | sistema funcional `(X, f)` | `∃ n : ℕ`, sobre `f^[n]` | periodicidade eventual |

Regra de decisão adotada: **todo teorema vai para a camada mais fraca em
que seu enunciado ainda faz sentido.** Consequência direta e não negociável:

```text
A periodicidade eventual eh um teorema da CAMADA C.
Ela nao menciona monoide, nao menciona acao, e nao precisa de nenhum dos
dois. Enuncia-la na camada A seria importar hipotese ociosa.
```

O resultado para ações (Camada B) é obtido como **corolário** do resultado
funcional, via `smul_iterate_apply`, e não reprovado por enumeração.

## Camada A — ação de monoide

Dados:

```text
M : tipo finito
X : tipo finito
Monoid M
MulAction M X
```

### Alcançabilidade

```lean
def Reachable
    {M X : Type*}
    [Monoid M]
    [MulAction M X]
    (x y : X) : Prop :=
  ∃ m : M, m • x = y
```

Leitura: *existe uma transformação do monoide que leva `x` a `y`*.

Observação registrada: a definição quantifica sobre **todo** o monoide, não
sobre potências de um gerador. `Reachable x y` **não** significa que `y`
apareça na órbita de `x` sob um elemento específico.

### Órbita — decisão de representação

`MulAction.orbit` já existe no checkout fixado
(`Mathlib/GroupTheory/GroupAction/Defs.lean:49`):

```lean
def orbit (a : α) := Set.range fun m : γ => m • a
```

com

```lean
theorem mem_orbit_iff {a₁ a₂ : α} : a₂ ∈ orbit γ a₁ ↔ ∃ x : γ, x • a₁ = a₂ :=
  Iff.rfl
```

**Decisão: usar `MulAction.orbit` e `Set X`, não `Finset X`.**

Justificativa:

1. `mem_orbit_iff` é `Iff.rfl`, logo `Reachable x y ↔ y ∈ orbit M x` é
   **definicional** — a ponte custa zero.
2. `Finset X` exigiria `DecidableEq X` e `Fintype M` e uma construção por
   imagem; nenhuma dessas hipóteses é necessária para os teoremas
   estruturais.
3. A finitude só é necessária no alvo da Camada C, onde entra via
   `Fintype X` diretamente, sem passar pela órbita.

Se um gate futuro precisar contar elementos da órbita, aí sim `Finset` ou
`Set.ncard` entram — como refinamento, não como representação base.

### Invariante

```lean
def IsInvariant
    {M X A : Type*}
    [Monoid M]
    [MulAction M X]
    (I : X → A) : Prop :=
  ∀ m x, I (m • x) = I x
```

Três noções distintas, que **não** devem receber o mesmo nome:

```text
INVARIANTE SOB A ACAO COMPLETA
  forall m x, I (m . x) = I x
  (a definicao acima)

INVARIANTE SOB UM GERADOR a
  forall x, I (a . x) = I x
  estritamente mais fraco: nada diz sobre outros elementos de M

INVARIANTE AO LONGO DE UMA ORBITA
  forall y in orbit M x, I y = I x
  consequencia do primeiro, mas NAO equivalente:
  eh uma afirmacao sobre um x fixo
```

A especificação prevê nomes separados: `IsInvariant`,
`IsInvariantUnder a`, e a forma "ao longo da órbita" como *teorema*
(`FSG2-INV-001`), não como definição concorrente.

## Camada B — dinâmica de um elemento

Fixados `a : M` e `x : X`, a sequência é

```text
x, a . x, a^2 . x, a^3 . x, ...
```

que é a iteração de

```lean
f_a : X → X := fun y => a • y
```

### Identidade iteração ↔ potência

**Já existe na Mathlib fixada**
(`Mathlib/Algebra/Group/Action/Defs.lean:432,437`):

```lean
theorem smul_iterate (a : M) : ∀ n : ℕ, (a • · : α → α)^[n] = (a ^ n • ·)
lemma smul_iterate_apply (a : M) (n : ℕ) (x : α) : (a • ·)^[n] x = a ^ n • x
```

Portanto a relação que a especificação previa como possivelmente ausente

```text
Function.iterate (fun y => a • y) n x = a^n • x
```

é exatamente `smul_iterate_apply`. `FSG2-GAP-003` está **resolvido pela
API existente** e não requer lema local. Isto foi verificado por leitura da
fonte, não presumido.

## Camada C — sistema funcional finito

Dados abstratos:

```text
X : tipo finito
f : X → X
```

Nenhuma estrutura algébrica. A periodicidade eventual vive aqui.

### Vocabulário

```text
CAUDA (preperiodo) mu   numero de passos antes de entrar no ciclo
PERIODO lambda          comprimento do ciclo, com lambda > 0
COLISAO                 par de indices i < j com f^[i] x = f^[j] x
```

## Armadilha registrada: `minimalPeriod` não é o que se procura

`Function.minimalPeriod f x` e `MulAction.period m a` existem na Mathlib,
mas ambos devolvem **0** quando `x` **não** é periódico:

```lean
def minimalPeriod (f : α → α) (x : α) :=
  if h : x ∈ periodicPts f then Nat.find h else 0
```

E `Function.IsPeriodicPt f n x := IsFixedPt f^[n] x`, isto é
`f^[n] x = x` — retorno ao ponto **inicial**, periodicidade desde `n = 0`.

Num sistema com cauda (ver `CE-003`: `0 → 1 → 2 → 2`) o estado `0` é
eventualmente periódico mas **não** é periódico, logo
`minimalPeriod f 0 = 0`. Usar `minimalPeriod` como se fosse o período
eventual produziria um enunciado falso.

Registrado como `FSG2-GAP-002b`. A conexão correta é indireta e é ela
mesma um teorema-alvo: **o ponto `f^[μ] x` é periódico no sentido da
Mathlib**, com período `λ`.
