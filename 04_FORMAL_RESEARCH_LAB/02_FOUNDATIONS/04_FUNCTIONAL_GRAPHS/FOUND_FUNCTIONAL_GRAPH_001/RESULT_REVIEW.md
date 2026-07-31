---
document_id: FFG-RESULT-REVIEW
gate: FOUND_FUNCTIONAL_GRAPH_001_RESULT_REVIEW
reviewed_commit: 3f6d7e785ba8bd90a35f33f7dc889f1234a7b650
decision: A_RESULT_REVIEW_APPROVED
new_theorems: 0
math_modules_modified: 0
---

# FOUND-FUNCTIONAL-GRAPH-001 — Revisão de resultado

Revisão do que já está verificado. **Nenhum teorema novo, nenhum módulo
matemático alterado.**

## Confirmação item a item

### FGR-001 — alcance por iteração `CONFIRMADO`

```text
@iterReachable_refl  : ∀ {X} (f : X → X) (x : X), IterReachable f x x
@iterReachable_trans : ∀ {X} {f : X → X} {x y z : X},
  IterReachable f x y → IterReachable f y z → IterReachable f x z
```

Testemunhas `0` e **`b + a`**. Nenhuma finitude, nenhum `DecidableEq` —
visível nas assinaturas impressas: os binders são apenas `{X : Type u_1}`
e `{f : X → X}`.

### FGR-002 — encontro eventual `CONFIRMADO`

`eventuallyMeets_refl`, `_symm`, `_trans`, todos com o mesmo perfil de
binders. **Nenhuma finitude.**

### FGR-003 — componente funcional `CONFIRMADO`

A relação de componente usada em `exists_component_cycle_with_entry_bound`
é `EventuallyMeets`. `MutuallyReachable` existe como definição pública mas
**não aparece** em nenhum enunciado do núcleo — apenas em `CE-004`, onde é
refutada como candidata.

Nenhuma definição pública concorrente: `SameFunctionalComponent` e
`componentSet` **não foram criados**.

### FGR-004 — alcance implica encontro `CONFIRMADO`

`IterReachable.eventuallyMeets`, testemunhas `(n, 0)`, pois
`f^[0] y ≡ y` definicionalmente.

### FGR-005 — igualdade da órbita periódica `CONFIRMADO`

```text
@periodicOrbit_eq_of_eventuallyMeets : ∀ {X} {f : X → X} {p q : X},
  p ∈ Function.periodicPts f → q ∈ Function.periodicPts f →
  EventuallyMeets f p q →
  Function.periodicOrbit f p = Function.periodicOrbit f q
```

Ausentes: `Fintype`, `DecidableEq`, `minimalPeriod`, aritmética modular.
A prova é um `calc` de três passos sobre
`Function.periodicOrbit_apply_iterate_eq`.

### FGR-006 — resultado inverso `CONFIRMADO`

```text
@eventuallyMeets_of_periodicOrbit_eq : ∀ {X} {f : X → X} {p q : X},
  p ∈ Function.periodicPts f → q ∈ Function.periodicPts f →
  Function.periodicOrbit f p = Function.periodicOrbit f q →
  EventuallyMeets f p q
```

### 12 — A limitação a pontos periódicos é **essencial**

```text
NAO vale:  periodicOrbit f p = periodicOrbit f q ↔ EventuallyMeets f p q
           para pontos arbitrarios.
```

Razão, e é a ressalva mais importante desta revisão:

```text
Se p ∉ periodicPts f, entao periodicOrbit f p = Cycle.nil.

Dois pontos NAO periodicos tem, ambos, a orbita VAZIA. As orbitas sao
iguais — trivialmente — sem que as trajetorias se encontrem.
```

O fenômeno foi **verificado concretamente** no teste de auditoria, com
`CE-002`:

```lean
example : Function.periodicOrbit CE002.f CE002.St.a = Cycle.nil :=
  Function.periodicOrbit_eq_nil_iff_not_periodic_pt.mpr CE002.a_not_periodic
```

As duas hipóteses `hp` e `hq` permanecem **visíveis** na assinatura, e o
teste de auditoria contém um exemplo que só typecheck fornecendo-as.

#### O que **não** foi formalizado

Um contraexemplo explícito — dois pontos **não** periódicos com órbitas
(vazias) iguais que **não** se encontram — **não existe** entre os seis
modelos. Em `CE-002` e `CE-004` os pontos transitórios **se encontram**.
Construir tal modelo (duas caudas disjuntas para dois ciclos disjuntos)
exigiria um sétimo contraexemplo, isto é, matemática nova, que este gate
proíbe. Registrado como observação estrutural, **não** como fato
formalizado.

### FGR-007 — existência limitada `CONFIRMADO`

```text
@exists_cyclePoint_reachable_with_bound : ∀ {X} [inst : Fintype X]
  (f : X → X) (x : X), ∃ mu < Fintype.card X, f^[mu] x ∈ Function.periodicPts f
```

Reutiliza `TamesisLab.Foundations.FiniteDynamics.exists_eventual_period`
via `Function.mk_mem_periodicPts`.

### 14 — Casa dos pombos

`Fintype.exists_ne_map_eq_of_card_lt` **não aparece** em nenhum arquivo
desta frente. O princípio foi consumido uma única vez em
`FOUND-SEMIGROUP-002`. **Não foi repetido.**

### FGR-008 — teorema principal `CONFIRMADO`

```text
@exists_component_cycle_with_entry_bound : ∀ {X} [inst : Fintype X]
  (f : X → X) (x : X),
  ∃ mu < Fintype.card X,
    f^[mu] x ∈ Function.periodicPts f ∧
    ∀ q ∈ Function.periodicPts f,
      EventuallyMeets f x q →
      Function.periodicOrbit f (f^[mu] x) = Function.periodicOrbit f q
```

### 16 — Interpretação da unicidade

```text
E:      unicidade da ORBITA PERIODICA.

NAO E:  unicidade de ponto        — CE-005 exibe dois, distintos
        unicidade de mu           — minimalidade nao provada
        minimalidade de periodo   — nao afirmada no principal
        representante canonico    — f^[mu] x eh UM, nao O
```

`∃!` **não aparece** em nenhum enunciado.

## 17 — Auditoria da transitividade

Revisada linha a linha.

```text
hxy: f^[mx] x = f^[ny] y
hyz: f^[my] y = f^[nz] z
```

Separação por `Nat.le_total ny my`.

### 18 — Caso `ny ≤ my`

```text
d = my - ny            hd : (my - ny) + ny = my   por omega
testemunhas            (d + mx, nz)

calc f^[(my-ny) + mx] x = f^[my-ny] (f^[mx] x)   iterate_add_apply f _ _ _
                        = f^[my-ny] (f^[ny] y)   rw [hxy']
                        = f^[(my-ny) + ny] y     (iterate_add_apply _ _ _).symm
                        = f^[my] y               rw [hd]
                        = f^[nz] z               hyz'
```

### 19 — Caso `my ≤ ny`

```text
d = ny - my            hd : (ny - my) + my = ny   por omega
testemunhas            (mx, d + nz)

calc f^[mx] x = f^[ny] y                 hxy'
              = f^[(ny-my) + my] y       rw [hd]
              = f^[ny-my] (f^[my] y)     iterate_add_apply f _ _ _
              = f^[ny-my] (f^[nz] z)     rw [hyz']
              = f^[(ny-my) + nz] z       (iterate_add_apply _ _ _).symm
```

### Orientação

```text
Function.iterate_add_apply (f) (m n) (x) : f^[m + n] x = f^[m] (f^[n] x)
```

Contagem **externa** à esquerda. Todas as chamadas usam a forma
`Function.iterate_add_apply f _ _ _` com o `f` explícito, evitando
ambiguidade de reescrita.

## 20 — Caso infinito

```text
EventuallyMeets continua sendo relacao de equivalencia para funcoes sobre
tipos INFINITOS: os tres teoremas nao usam finitude.

A existencia de ponto periodico alcancavel eh FALSA em geral para tipos
infinitos.

Exemplo documental: X = N, f(n) = n + 1 — sem ponto periodico algum.
```

Nenhum teorema Lean foi criado para esse exemplo. `[Fintype X]` aparece
**somente** em `ComponentCycle.lean`, na camada de existência.

## 21 — Caso do tipo vazio

```text
Os teoremas de existencia recebem x : X. Se X for vazio, nao existe termo
x : X e o teorema nao pode ser invocado.
```

Nenhuma hipótese global `Nonempty X` é necessária, e nenhuma existe.
Verificado: zero ocorrências de `Nonempty`, `Inhabited`, `Finite` e
`DecidableEq` nas assinaturas públicas.

## Decisão

```text
A. FOUND_FUNCTIONAL_GRAPH_001_RESULT_REVIEW_APPROVED
```

| Critério | Estado |
|---|---|
| teoremas compilam | `lake build` PASS, 8.727 jobs |
| hipóteses mínimas | sem `DecidableEq`; `Fintype` só na existência |
| transitividade correta | revisada linha a linha |
| inverso limitado a periódicos | hipóteses visíveis e indispensáveis |
| instâncias isoladas | 5, todas em contraexemplos; **0 no núcleo** |
| contraexemplos válidos | seis, alvos distintos |
| claim corresponde ao resultado | revisada |
| não computabilidade documentada | `PROOF_AUDIT.md`, `RESULT_BOUNDARY.md` |
| sem dependência de `SimpleGraph` | 0 imports |
| sem dependência oculta de legado | imports auditados |
