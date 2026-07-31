---
document_id: RT-FINAL-EXECUTION-SEMANTICS
frozen: true
central_result_verified: true
---

# Semântica de execução — congelada

## Função tipada

```lean
def ValidatedTransitionTable.step (t : ValidatedTransitionTable) :
    Fin t.next.size → Fin t.next.size :=
  fun i => ⟨t.next[i], t.closed i⟩

@[simp]
theorem ValidatedTransitionTable.step_val (t : ValidatedTransitionTable)
    (i : Fin t.next.size) :
    (t.step i : Nat) = t.next[i] :=
  rfl
```

`rfl` confirmado no probe. Coerção `Fin → Nat` **explícita** no enunciado.

## Semântica bruta

```lean
def RawTransitionTable.step? (t : RawTransitionTable) (state : Nat) :
    Option Nat :=
  t.next[state]?

def RawTransitionTable.run? (t : RawTransitionTable) :
    Nat → Nat → Option Nat
  | 0, state => some state
  | steps + 1, state => do
      let nextState ← t.step? state
      t.run? steps nextState
```

Semântica vinculante, **medida**:

```text
run? 0 999 = some 999      tabela vazia, estado fora dos limites
run? 1 999 = none          primeiro lookup invalido
```

O caso zero devolve `some state` **mesmo quando `state ≥ size`**. Isso
**não** valida o estado; a validade do início pertence a `validateStart`.
A semântica de zero passos **não** será alterada para devolver `none`.

```text
run? eh semantica bruta PARCIAL;
validateStart eh a barreira de seguranca da API dinamica.
```

## Ponte de uma transição

```lean
theorem ValidatedTransitionTable.step?_eq_some_step
    (t : ValidatedTransitionTable) (i : Fin t.next.size) :
    t.toRaw.step? (i : Nat) = some ((t.step i : Fin t.next.size) : Nat) := by
  show t.next[(i : Nat)]? = some (t.next[i])
  exact getElem?_pos t.next (i : Nat) i.isLt
```

**Compila.** Usa apenas: lookup válido pelo índice `Fin` (via `i.isLt`),
`step_val` implicitamente na redução, e a redução de `step?`. Nenhum
fallback. Classificado **`CORE`**.

## Ponte de iterações — a obrigação técnica principal

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

**Compila. Pegada: `[propext, Quot.sound]`.**

### Os três detalhes congelados

```text
1. o quantificador ∀ start vem DEPOIS de k, DENTRO do enunciado;
   nao se usa `generalizing`;

2. dois `show` sao necessarios — o primeiro expoe o bind escondido pela
   notacao do, o segundo forca a reducao de Option.bind (some a) f;

3. a variante correta eh Function.iterate_succ_apply, e nao a linha.
```

Fluxo efetivo do caso sucessor:

```text
run? (k+1) start
= (step? start).bind (run? k)
= (some (step start)).bind (run? k)      por step?_eq_some_step
= run? k (step start)                    por reducao do bind
= some (step^[k] (step start))           por ih
= some (step^[k+1] start)                por iterate_succ_apply
```

## Coerções `Fin`/`Nat` — congeladas

Todas explícitas nos enunciados:

```text
step_val               (t.step i : Nat) = t.next[i]
step?_eq_some_step     t.toRaw.step? (i : Nat) = some ((t.step i : ...) : Nat)
run?_eq_iterate_step   t.toRaw.run? k (start : Nat) = some (((...) : Fin ...) : Nat)
```

Nenhuma coerção implícita é deixada ao elaborador nos enunciados públicos.
Isso foi exigido pela revisão e verificado no probe.
