---
document_id: FFG-FINAL-SIGNATURES
status: FROZEN
gate: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW
---

# FOUND-FUNCTIONAL-GRAPH-001 — Assinaturas congeladas

Autorizadas para a formalização. **Nenhum corpo de prova aqui.**

---

## Auditoria de orientação — `Function.iterate_add_apply`

Confirmado por probe:

```lean
Function.iterate_add_apply (f : α → α) (m n : ℕ) (x : α) :
  f^[m + n] x = f^[m] (f^[n] x)
```

```text
`f` eh EXPLICITO e vem primeiro.
A contagem EXTERNA eh `m`, e ela aparece a ESQUERDA da soma.
```

Consequência que corrige a especificação: aplicar `f^[d]` a uma igualdade
já iterada produz `f^[d + k]`, **não** `f^[k + d]`. As testemunhas naturais
são `d + mx` e `d + nz`; a forma `mx + d` da especificação anterior é igual
em valor mas difere sintaticamente e exigiria `Nat.add_comm` para casar com
`rw`.

**As testemunhas abaixo estão na forma natural.**

---

## Alcançabilidade dirigida

```lean
theorem iterReachable_refl (f : X → X) (x : X) :
    IterReachable f x x
```

Testemunha `0`; `f^[0] x = x` é `rfl`.

```lean
theorem iterReachable_trans {f : X → X} {x y z : X}
    (hxy : IterReachable f x y) (hyz : IterReachable f y z) :
    IterReachable f x z
```

De `f^[a] x = y` e `f^[b] y = z`, testemunha **`b + a`**:

```text
f^[b + a] x = f^[b] (f^[a] x) = f^[b] y = z
```

```lean
theorem IterReachable.eventuallyMeets {f : X → X} {x y : X}
    (h : IterReachable f x y) : EventuallyMeets f x y
```

Testemunhas `(n, 0)`, pois `f^[n] x = y = f^[0] y`.

`EventuallyMeets.of_iterReachable_left` **não** será criado: duplicaria a
mesma API. Uma direção basta, e a simetria de `EventuallyMeets` cobre o
resto.

---

## Encontro eventual

```lean
theorem eventuallyMeets_refl (f : X → X) (x : X) :
    EventuallyMeets f x x
```

Testemunhas `(0, 0)`.

```lean
theorem eventuallyMeets_symm {f : X → X} {x y : X}
    (h : EventuallyMeets f x y) : EventuallyMeets f y x
```

Troca das testemunhas e `.symm`.

```lean
theorem eventuallyMeets_trans {f : X → X} {x y z : X}
    (hxy : EventuallyMeets f x y) (hyz : EventuallyMeets f y z) :
    EventuallyMeets f x z
```

### Mapa de índices — nomes inequívocos

```text
hxy da   mx, ny   com   f^[mx] x = f^[ny] y
hyz da   my, nz   com   f^[my] y = f^[nz] z
```

O alinhamento é sobre a trajetória intermediária `y`, comparando `ny` e
`my`.

### Caso `ny ≤ my`, com `d = my - ny`

Aplicar `f^[d]` à **primeira** igualdade:

```text
f^[d + mx] x = f^[d] (f^[mx] x)      iterate_add_apply f d mx x, direita->esquerda
             = f^[d] (f^[ny] y)      por hxy
             = f^[d + ny] y          iterate_add_apply f d ny y
             = f^[my] y              pois d + ny = my   (omega, dado ny ≤ my)
             = f^[nz] z              por hyz
```

```yaml
testemunhas:
  x: "d + mx"
  z: "nz"
```

### Caso `my ≤ ny`, com `d = ny - my`

Aplicar `f^[d]` à **segunda** igualdade:

```text
f^[mx] x = f^[ny] y                  por hxy
         = f^[d + my] y              pois d + my = ny   (omega, dado my ≤ ny)
         = f^[d] (f^[my] y)          iterate_add_apply f d my y
         = f^[d] (f^[nz] z)          por hyz
         = f^[d + nz] z              iterate_add_apply f d nz z
```

```yaml
testemunhas:
  x: "mx"
  z: "d + nz"
```

Separação dos casos por `Nat.le_total ny my`. Subtração truncada
normalizada por `omega`.

**Nenhuma hipótese de finitude em nenhum dos três.**

---

## Igualdade de órbitas

```lean
theorem periodicOrbit_eq_of_eventuallyMeets {f : X → X} {p q : X}
    (hp : p ∈ Function.periodicPts f)
    (hq : q ∈ Function.periodicPts f)
    (hpq : EventuallyMeets f p q) :
    Function.periodicOrbit f p = Function.periodicOrbit f q
```

Orientação congelada: **`p = q`**, com `p` sendo o primeiro argumento de
`EventuallyMeets`.

Rota, com a orientação real do lema
(`periodicOrbit f (f^[n] x) = periodicOrbit f x`):

```text
1. obter mp, nq de hpq, com f^[mp] p = f^[nq] q
2. (periodicOrbit_apply_iterate_eq hp mp).symm
     : periodicOrbit f p = periodicOrbit f (f^[mp] p)
3. reescrever pela igualdade das iteradas
     : periodicOrbit f p = periodicOrbit f (f^[nq] q)
4. periodicOrbit_apply_iterate_eq hq nq
     : periodicOrbit f (f^[nq] q) = periodicOrbit f q
5. concluir
```

Hipóteses ausentes, e devem permanecer ausentes: `DecidableEq X`,
`Fintype X`, `minimalPeriod`, aritmética modular.

### Recíproca — `OPTIONAL_COROLLARY`

```lean
theorem eventuallyMeets_of_periodicOrbit_eq {f : X → X} {p q : X}
    (hp : p ∈ Function.periodicPts f)
    (hq : q ∈ Function.periodicPts f)
    (h : Function.periodicOrbit f p = Function.periodicOrbit f q) :
    EventuallyMeets f p q
```

Autorizada **somente** se a prova for composição curta de
`self_mem_periodicOrbit`, `mem_periodicOrbit_iff` e
`IterReachable.eventuallyMeets`. **Não** é dependência do teorema
principal.

---

## Adaptador de existência

```lean
theorem exists_cyclePoint_reachable_with_bound {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ mu : ℕ,
      mu < Fintype.card X ∧
      f^[mu] x ∈ Function.periodicPts f
```

Derivado de `exists_eventual_period` via `Function.mk_mem_periodicPts`:

```text
exists_eventual_period f x  da  mu, lam  com
  mu < card X, 0 < lam, mu + lam <= card X,
  IsPeriodicPt f lam (f^[mu] x)

mk_mem_periodicPts hlam hper  :  f^[mu] x ∈ periodicPts f
```

**A casa dos pombos não é repetida.** Sem par artificial `ℕ × X`. Sem
`DecidableEq X`.

---

## Teorema principal

```lean
theorem exists_component_cycle_with_entry_bound {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ mu : ℕ,
      mu < Fintype.card X ∧
      f^[mu] x ∈ Function.periodicPts f ∧
      ∀ q : X,
        q ∈ Function.periodicPts f →
        EventuallyMeets f x q →
        Function.periodicOrbit f (f^[mu] x) =
          Function.periodicOrbit f q
```

Rota:

```text
1. exists_cyclePoint_reachable_with_bound da mu e hp
2. dado q ciclico com EventuallyMeets f x q:
     IterReachable f x (f^[mu] x)                 testemunha mu
     EventuallyMeets f x (f^[mu] x)               IterReachable.eventuallyMeets
     EventuallyMeets f (f^[mu] x) x               eventuallyMeets_symm
     EventuallyMeets f (f^[mu] x) q               eventuallyMeets_trans
3. periodicOrbit_eq_of_eventuallyMeets hp hq (passo 2)
     : periodicOrbit f (f^[mu] x) = periodicOrbit f q
```

A orientação da conclusão **casa** com a regra congelada: o primeiro
argumento de `EventuallyMeets` no passo 3 é `f^[mu] x`, e é ele que fica à
esquerda.

### O que a conclusão **não** usa

```text
NAO usa ∃! p : X.
NAO afirma unicidade do representante f^[mu] x.
NAO afirma minimalidade de mu.
NAO afirma minimalidade do periodo.
```

O objeto único é `Function.periodicOrbit f (f^[mu] x)`.

---

## Hipóteses por camada

| Camada | Hipóteses |
|---|---|
| `IterReachable`, `MutuallyReachable`, `EventuallyMeets` e seus teoremas | **nenhuma** |
| `periodicOrbit_eq_of_eventuallyMeets` | **nenhuma** de finitude |
| `exists_cyclePoint_reachable_with_bound` | `[Fintype X]` |
| `exists_component_cycle_with_entry_bound` | `[Fintype X]` |

Proibidas sem necessidade verificada: `DecidableEq X`, `Finite X`,
`Nonempty X`, `Inhabited X`. O parâmetro `x : X` já impede aplicação ao
tipo vazio.
