---
document_id: RT-ITERATION-BRIDGE-AUDIT
central_result: true
compiled: true
---

# Auditoria da ponte de iterações

Era a obrigação técnica principal da frente. **Compilou de primeira**, na
forma exata congelada na revisão.

## Uma transição

```lean
theorem ValidatedTransitionTable.step?_eq_some_step
    (t : ValidatedTransitionTable) (i : Fin t.next.size) :
    t.toRaw.step? (i : Nat) = some ((t.step i : Fin t.next.size) : Nat) := by
  show t.next[(i : Nat)]? = some (t.next[i])
  exact getElem?_pos t.next (i : Nat) i.isLt
```

Duas linhas. Usa apenas o lookup válido pelo índice `Fin`, via `i.isLt`.
Nenhum `getD`, nenhum fallback.

## Iterações

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

## Os três detalhes, confirmados na prática

```text
1. o quantificador ∀ start vem DEPOIS de k, DENTRO do enunciado;
   `generalizing` NAO eh usado, e a hipotese de inducao ja vem na forma
   ∀ start, aplicavel a t.step start;

2. dois `show` sao necessarios — o primeiro expoe o bind que a notacao
   do esconde, o segundo forca a reducao de Option.bind (some a) f;

3. a variante correta eh Function.iterate_succ_apply, cuja contagem
   externa consome o passo INTERNO — exatamente a ordem de recursao de
   run?.
```

## Fluxo do caso sucessor

```text
run? (k+1) start
= (step? start).bind (run? k)                    primeiro show
= (some (step start)).bind (run? k)              step?_eq_some_step
= run? k (step start)                            segundo show
= some (step^[k] (step start))                   hipotese de inducao
= some (step^[k+1] start)                        iterate_succ_apply
```

## Axiomas

```text
step?               does not depend on any axioms
run?                does not depend on any axioms
step?_eq_some_step  [propext, Quot.sound]
run?_eq_iterate_step [propext, Quot.sound]
```

As duas **definições** de execução bruta não dependem de axioma algum.
O teorema central não usa `Classical.choice`.

## Semântica de zero passos — preservada

```text
run? 0 999 = some 999      inclusive para tabela vazia
run? 1 999 = none          primeiro lookup invalido
```

Ambos provados por `rfl` nos testes. A semântica **não** foi alterada
para devolver `none` em zero passos: `run?` é fiel ao array, e
`validateStart` é a barreira de segurança da API.
