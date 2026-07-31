---
document_id: RT-ITERATION-BRIDGE-REVIEW
audited_line_by_line: true
---

# Revisão da ponte de iterações

## Uma transição

```lean
theorem ValidatedTransitionTable.step?_eq_some_step
    (t : ValidatedTransitionTable) (i : Fin t.next.size) :
    t.toRaw.step? (i : Nat) = some ((t.step i : Fin t.next.size) : Nat) := by
  show t.next[(i : Nat)]? = some (t.next[i])
  exact getElem?_pos t.next (i : Nat) i.isLt
```

Relaciona o **lookup opcional sobre `Nat`** com o **`step` total sobre
`Fin n`**. Usa `getElem?_pos`, a API local auditada, com o limite vindo
de `i.isLt`. **Nenhum fallback.**

## Iterações — auditado linha por linha

```lean
theorem ValidatedTransitionTable.run?_eq_iterate_step
    (t : ValidatedTransitionTable) (k : Nat) :
    ∀ start : Fin t.next.size,
      t.toRaw.run? k (start : Nat) =
        some (((t.step)^[k] start : Fin t.next.size) : Nat) := by
  induction k with
  | zero => intro start; rfl
  | succ k ih =>
      intro start
      show (t.toRaw.step? (start : Nat)).bind (t.toRaw.run? k) = _
      rw [t.step?_eq_some_step start]
      show t.toRaw.run? k ((t.step start : Fin t.next.size) : Nat) = _
      rw [ih (t.step start), Function.iterate_succ_apply]
```

| Exigência | Verificado |
|---|---|
| indução em `k` | `induction k with` |
| hipótese válida para todo `start` | o `∀ start` está **no enunciado**, depois de `k`; `ih` vem na forma `∀ start` e é aplicada a `t.step start` |
| passo externo executado primeiro | o primeiro `show` expõe `(step? start).bind (run? k)` — o passo é consumido antes da recursão |
| `Function.iterate_succ_apply` | usado literalmente |
| nenhuma orientação inversa | `iterate_succ_apply'` **não** aparece |

### Coerções `Fin`/`Nat`

Todas explícitas no enunciado: `(start : Nat)` no lado esquerdo, e
`(((t.step)^[k] start : Fin t.next.size) : Nat)` no direito. Nenhuma é
deixada ao elaborador.

### Os dois `show`

São o coração da prova e não são cosméticos:

```text
o primeiro expõe o bind que a notação do esconde;
o segundo força a redução de Option.bind (some a) f para f a.
```

Sem eles, nem `rw` nem `simp` encontram o padrão — fato estabelecido no
gate de revisão da especificação e reconfirmado aqui.

## Axiomas

```text
RawTransitionTable.step?              does not depend on any axioms
RawTransitionTable.run?               does not depend on any axioms
step?_eq_some_step                    [propext, Quot.sound]
run?_eq_iterate_step                  [propext, Quot.sound]
```

Dentro do subconjunto permitido, e **sem `Classical.choice`**.

## Nenhuma segunda semântica

Existe **uma** semântica bruta (`step?`/`run?`) e **uma** função tipada
(`step`). A ponte as relaciona; ela não introduz um terceiro modelo de
execução. Confirmado por leitura integral dos seis módulos.
