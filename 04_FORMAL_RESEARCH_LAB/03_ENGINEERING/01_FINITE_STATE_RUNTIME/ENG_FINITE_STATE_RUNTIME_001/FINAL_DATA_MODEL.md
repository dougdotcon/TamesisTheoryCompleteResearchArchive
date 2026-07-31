---
document_id: RT-FINAL-DATA-MODEL
frozen: true
---

# Modelo de dados final — congelado

## Bruto

```lean
structure RawTransitionTable where
  next : Array Nat
deriving DecidableEq, Repr, BEq
```

Confirmada a ausência de `size`, `stateCount`, `proof`, `start` e
`fallback`.

```text
raw.next.size eh o UNICO nome publico para o numero de estados.
```

Nenhum accessor `stateCount` será criado. Decisão da especificação,
reafirmada aqui.

## Validade

```lean
def RawTransitionTable.Valid (t : RawTransitionTable) : Prop :=
  ∀ i : Fin t.next.size, t.next[i] < t.next.size
```

Confirmado:

```text
dominio de quantificacao finito
validade decidivel
tabela vazia valida por vacuidade
nenhum requisito de estado inicial
nenhum requisito de alcancabilidade
nenhum requisito de ciclo unico
```

Nenhum predicado público concorrente por `Nat` ou por elementos. Lemas
equivalentes futuros ficam permitidos e documentados, não criados.

## Instância decidível

```lean
instance RawTransitionTable.decidableValid (t : RawTransitionTable) :
    Decidable t.Valid := by
  unfold RawTransitionTable.Valid
  infer_instance
```

**Esta forma foi a testada e compila.** A variante com `inferInstanceAs`
permanece como alternativa registrada, não necessária.

`#synth` auditado em três tabelas:

```text
⟨#[]⟩    -> decValid
⟨#[0]⟩   -> decValid
⟨#[1]⟩   -> decValid
```

Sem `Classical`, sem `Classical.decEq`, sem `Classical.choose`, sem marca
de não-computabilidade.

## Validado

```lean
structure ValidatedTransitionTable where
  next : Array Nat
  closed : ∀ i : Fin next.size, next[i] < next.size
```

**Sem `deriving`** — a estrutura é dependente e contém campo `Prop`.

```lean
def ValidatedTransitionTable.toRaw (t : ValidatedTransitionTable) :
    RawTransitionTable :=
  ⟨t.next⟩

theorem ValidatedTransitionTable.toRaw_valid
    (t : ValidatedTransitionTable) : t.toRaw.Valid :=
  t.closed
```

`toRaw_valid` fecha por `t.closed` **diretamente** — confirmado no probe.
`toRaw` é público. Nenhum `Subtype RawTransitionTable.Valid` público
concorrente.

## Tabela vazia — congelada

```yaml
empty_table:
  structural_validity: VALID
  validation_result: OK
  valid_start_exists: false
  analysis_result_for_any_nat: INITIAL_STATE_OUT_OF_BOUNDS
```

Medido:

```text
(validateT ⟨#[]⟩).isOk   ->  true
analyzeT ⟨#[]⟩ 0         ->  error (initialStateOutOfBounds 0 0)
```

Nenhum erro `emptyTable` foi criado. Nenhum `Nonempty`, `Inhabited` ou
`0 < size` foi acrescentado à validade.

## Erros

```lean
inductive RuntimeCycleError
  | transitionDestinationOutOfBounds
  | initialStateOutOfBounds (start : Nat) (stateCount : Nat)
  | internalDetectorFailure
deriving DecidableEq, Repr, BEq
```

`transitionDestinationOutOfBounds` permanece **genérico na v1**. Nenhum
payload de diagnóstico detalhado. `RT-GAP-022` segue `OPEN_DEFERRED`.

Erro de tabela e erro de início **não** colapsados.
