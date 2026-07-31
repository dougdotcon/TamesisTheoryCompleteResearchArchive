---
document_id: RT-FINAL-SIGNATURES
frozen: true
public_declarations: 25
---

# Assinaturas congeladas

Desviar de qualquer uma exige gate próprio. Todas foram verificadas em
versão descartável.

## `PUBLIC_EXECUTABLE_CORE`

```lean
structure RawTransitionTable where
  next : Array Nat
deriving DecidableEq, Repr, BEq

structure ValidatedTransitionTable where
  next : Array Nat
  closed : ∀ i : Fin next.size, next[i] < next.size

inductive RuntimeCycleError
  | transitionDestinationOutOfBounds
  | initialStateOutOfBounds (start : Nat) (stateCount : Nat)
  | internalDetectorFailure
deriving DecidableEq, Repr, BEq

def validateTransitionTable (raw : RawTransitionTable) :
    Except RuntimeCycleError ValidatedTransitionTable

def validateStart (t : ValidatedTransitionTable) (start : Nat) :
    Except RuntimeCycleError (Fin t.next.size)

def ValidatedTransitionTable.step (t : ValidatedTransitionTable) :
    Fin t.next.size → Fin t.next.size

def RawTransitionTable.step? (t : RawTransitionTable) (state : Nat) : Option Nat

def RawTransitionTable.run? (t : RawTransitionTable) : Nat → Nat → Option Nat

def ValidatedTransitionTable.detectCycle? (t : ValidatedTransitionTable)
    (start : Fin t.next.size) : Option CycleWitness

def analyzeTransitionTable (raw : RawTransitionTable) (start : Nat) :
    Except RuntimeCycleError CycleWitness
```

## `PUBLIC_SPECIFICATION_CORE`

```lean
def RawTransitionTable.Valid (t : RawTransitionTable) : Prop

instance RawTransitionTable.decidableValid (t : RawTransitionTable) :
    Decidable t.Valid

def ValidatedTransitionTable.toRaw (t : ValidatedTransitionTable) :
    RawTransitionTable

theorem ValidatedTransitionTable.toRaw_valid
    (t : ValidatedTransitionTable) : t.toRaw.Valid

theorem validateTransitionTable_sound
    {raw : RawTransitionTable} {validated : ValidatedTransitionTable}
    (h : validateTransitionTable raw = .ok validated) :
    validated.toRaw = raw ∧ raw.Valid

theorem validateTransitionTable_complete (raw : RawTransitionTable)
    (h : raw.Valid) :
    ∃ validated, validateTransitionTable raw = .ok validated

theorem validateStart_sound
    {t : ValidatedTransitionTable} {start : Nat}
    {typedStart : Fin t.next.size}
    (h : validateStart t start = .ok typedStart) :
    (typedStart : Nat) = start

theorem validateStart_complete (t : ValidatedTransitionTable) (start : Nat)
    (h : start < t.next.size) :
    ∃ typedStart, validateStart t start = .ok typedStart

@[simp] theorem ValidatedTransitionTable.step_val
    (t : ValidatedTransitionTable) (i : Fin t.next.size) :
    (t.step i : Nat) = t.next[i]

theorem ValidatedTransitionTable.step?_eq_some_step
    (t : ValidatedTransitionTable) (i : Fin t.next.size) :
    t.toRaw.step? (i : Nat) = some ((t.step i : Fin t.next.size) : Nat)

theorem ValidatedTransitionTable.run?_eq_iterate_step
    (t : ValidatedTransitionTable) (k : Nat) :
    ∀ start : Fin t.next.size,
      t.toRaw.run? k (start : Nat) =
        some (((t.step)^[k] start : Fin t.next.size) : Nat)

theorem ValidatedTransitionTable.detectCycle?_sound
    {t : ValidatedTransitionTable} {start : Fin t.next.size}
    {w : CycleWitness} (h : t.detectCycle? start = some w) :
    CycleWitness.Valid t.step start w

theorem ValidatedTransitionTable.detectCycle?_complete
    (t : ValidatedTransitionTable) (start : Fin t.next.size) :
    ∃ w, t.detectCycle? start = some w

theorem ValidatedTransitionTable.detectCycle?_raw_repeat
    {t : ValidatedTransitionTable} {start : Fin t.next.size}
    {w : CycleWitness} (h : t.detectCycle? start = some w) :
    t.toRaw.run? (w.baseIndex + w.period) (start : Nat) =
      t.toRaw.run? w.baseIndex (start : Nat)

theorem analyzeTransitionTable_sound
    {raw : RawTransitionTable} {start : Nat} {w : CycleWitness}
    (h : analyzeTransitionTable raw start = .ok w) :
    raw.Valid ∧ start < raw.next.size ∧
    raw.run? (w.baseIndex + w.period) start = raw.run? w.baseIndex start

theorem analyzeTransitionTable_complete (raw : RawTransitionTable)
    (start : Nat) (hRaw : raw.Valid) (hStart : start < raw.next.size) :
    ∃ w, analyzeTransitionTable raw start = .ok w
```

## `PUBLIC_COROLLARY`

```lean
theorem analyzeTransitionTable_invalid_table (raw : RawTransitionTable)
    (start : Nat) (h : ¬raw.Valid) :
    analyzeTransitionTable raw start =
      .error .transitionDestinationOutOfBounds

theorem analyzeTransitionTable_invalid_start (raw : RawTransitionTable)
    (start : Nat) (hRaw : raw.Valid) (hStart : ¬start < raw.next.size) :
    analyzeTransitionTable raw start =
      .error (.initialStateOutOfBounds start raw.next.size)

theorem analyzeTransitionTable_ne_internalFailure
    (raw : RawTransitionTable) (start : Nat) (hRaw : raw.Valid)
    (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start ≠ .error .internalDetectorFailure
```

## `DEFERRED`

```text
diagnostico detalhado; CLI; JSON; CSV; arquivo; rede; integracao;
extracao de produto; Floyd; Brent; tabela visitada; minimalidade;
complexidade; benchmark; correcao da abstracao externa.
```

## Contagem

```text
PUBLIC_EXECUTABLE_CORE      10
PUBLIC_SPECIFICATION_CORE   14  (1 def, 1 instancia, 1 def, 11 teoremas)
PUBLIC_COROLLARY             3
```

## Provas já demonstradas em ambiente descartável

```text
toRaw_valid                 t.closed
step_val                    rfl
step?_eq_some_step          getElem?_pos t.next i i.isLt
run?_eq_iterate_step        inducao + dois show + iterate_succ_apply
detectCycle?_raw_repeat     sound + run?_eq_iterate_step x2 + hv.2.2.2
analyzeTransitionTable_invalid_table    unfold + dif_neg + rfl
analyzeTransitionTable_invalid_start    unfold + dif_pos + show + rw + rfl
```
