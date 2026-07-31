---
document_id: RT-SPECIFICATION-REVIEW
gate: ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_REVIEW
reviewed_commit: 4d9e2488accc8d6a952e46b1d995c5e47c498a4f
decision: A_SPECIFICATION_REVIEW_APPROVED
probe: /tmp/FiniteStateRuntimeReviewProbe.lean (removido)
permanent_lean_files: 0
---

# Revisão da especificação

## O que esta revisão demonstrou

```text
O probe descartavel compilou com ZERO erros, incluindo
run?_eq_iterate_step, detectCycle?_raw_repeat e os dois teoremas de
precedencia de erro.
```

Esta era a condição de aprovação: o agente devia demonstrar, em ambiente
descartável, que o principal teorema de correspondência entre `run?` e
`Nat.iterate` realmente fecha no Lean fixado. **Fecha.**

## `run?_eq_iterate_step` — resolvido

A forma que compila:

```lean
theorem ValidT.run?_eq_iterate_step (t : ValidT) (k : Nat) :
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

### Três detalhes que a revisão congela

1. **A generalização é feita pelo enunciado, não pela tática.** O `∀ start`
   vem **depois** de `k`, dentro do tipo. `induction k generalizing start`
   não foi usado. Com o quantificador no enunciado, `ih` já vem na forma
   `∀ start, ...` e se aplica a `t.step start` diretamente.
2. **Dois `show` são necessários**, e são o coração da prova. O primeiro
   expõe o `bind` que a notação `do` esconde; o segundo força a redução de
   `Option.bind (some a) f` para `f a`. Sem eles, nem `rw` nem `simp`
   encontram o padrão.
3. **A orientação auditada estava certa.** `Function.iterate_succ_apply`
   (`f^[n+1] x = f^[n] (f x)`) é a que casa; a variante linha teria
   exigido comutar a indução.

Pegada axiomática do teorema: `[propext, Quot.sound]` — **sem**
`Classical.choice`.

## Confirmações item a item

| Item | Verdito |
|---|---|
| `RawTransitionTable` mínima | **CONFIRMADO** — um campo; `size`, `stateCount`, `proof`, `start`, `fallback` ausentes |
| `Valid` decidível | **CONFIRMADO** — `#synth` resolve em tabela vazia, válida e inválida |
| tabela vazia separada da consulta | **CONFIRMADO** — `validateT ⟨#[]⟩` é `ok`; `analyzeT ⟨#[]⟩ 0` é `initialStateOutOfBounds 0 0` |
| `ValidatedTransitionTable` garante fechamento | **CONFIRMADO** — `closed` é campo |
| `step` total por construção | **CONFIRMADO** — `step_val` fecha por `rfl` |
| `run?` sem fallback | **CONFIRMADO** — `run? 1 999 = none` |
| `run?_eq_iterate_step` viável | **DEMONSTRADO** — compila |
| detector apenas reutilizado | **CONFIRMADO** — `detectCycle?` é uma linha |
| witness interpretado na tabela bruta | **CONFIRMADO** — `detectCycle?_raw_repeat` compila |
| precedência dos erros congelada | **CONFIRMADO** — ver abaixo |
| `internalDetectorFailure` defensivo | **CONFIRMADO** — ramo mantido, impossibilidade derivável |
| soundness e completeness coerentes | **CONFIRMADO** — planos revisados |
| nenhuma entrada corrigida | **CONFIRMADO** — sem `mod`, `clamp`, `getD`, fallback |
| nenhum parsing externo | **CONFIRMADO** |
| novidade zero | **CONFIRMADO** |

## Precedência dos erros — congelada e medida

```text
1. tabela invalida
2. estado inicial invalido
3. falha interna impossivel
4. sucesso
```

O teste decisivo, exigido pelo gate e executado:

```text
analyzeT ⟨#[1]⟩ 100  ->  transitionDestinationOutOfBounds
```

A tabela é inválida **e** o início é inválido; o erro de **tabela**
vence. A ordem do `do` é a garantia, e os dois teoremas de erro a fixam.

## Achado técnico: as provas de precedência exigem `show`

Nem `simp` nem `split` conseguem reduzir o `do` sobre `Except`:

```text
simp [analyzeT, validateT, dif_neg h, Except.bind]   -> unsolved goals
split                                                 -> "Could not split"
simp only [...] ; simp [hStart]                       -> "made no progress"
```

O que funciona:

```lean
theorem analyzeT_invalid_table (raw) (start) (h : ¬raw.Valid) :
    analyzeT raw start = .error .transitionDestinationOutOfBounds := by
  unfold analyzeT validateT
  rw [dif_neg h]
  rfl

theorem analyzeT_invalid_start (raw) (start) (hRaw : raw.Valid)
    (hStart : ¬start < raw.next.size) :
    analyzeT raw start = .error (.initialStateOutOfBounds start raw.next.size) := by
  unfold analyzeT validateT
  rw [dif_pos hRaw]
  show (validateStartT ⟨raw.next, hRaw⟩ start).bind _ = _
  rw [show validateStartT ⟨raw.next, hRaw⟩ start
        = .error (.initialStateOutOfBounds start raw.next.size) from dif_neg hStart]
  rfl
```

O motivo do fracasso do `rw` direto: depois de `dif_pos hRaw`, a condição
interna é `start < validated.next.size` com `validated` ainda **ligado
pelo `do`**; `(⟨raw.next, hRaw⟩ : ValidT).next.size` é *defeq* a
`raw.next.size`, mas não *sintaticamente* igual. O `show` resolve porque
opera a menos de definicional.

**Este é o padrão que a formalização deve seguir.** Registrado para que o
gate seguinte não repita as três tentativas fracassadas.

## Correção à auditoria de API anterior

A especificação registrou `Array.getElem?` como `NOT_FOUND`. Preciso
qualificar:

```text
Array.getElem?              nao existe como CONSTANTE  (confirmado)
Array.getElem?_eq_getElem   EXISTE como lema           (novo)
getElem?_pos                EXISTE, e eh o usado       (novo)
```

`getElem?_pos (c) (i) (h : dom c i) : c[i]? = some c[i]` foi o lema que
fechou `step?_eq_some_step`. A entrada da auditoria foi corrigida.

## Numeração de diretório

```yaml
directory_numbering_issue:
  status: ACKNOWLEDGED_COSMETIC
  rename_authorized: false
```

`03_ENGINEERING/` e `03_MILLENNIUM/` coexistem. Nenhum diretório foi
renomeado neste gate.

## Decisão

```text
A. ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_REVIEW_APPROVED
```
