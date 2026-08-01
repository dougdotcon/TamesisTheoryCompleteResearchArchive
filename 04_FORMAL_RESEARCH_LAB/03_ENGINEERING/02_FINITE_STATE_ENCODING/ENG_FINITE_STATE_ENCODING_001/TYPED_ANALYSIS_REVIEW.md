---
document_id: ENC-TYPED-ANALYSIS-REVIEW
soundness_conclusion_type: S
completeness_preconditions: 0
---

# Revisão da análise tipada

## `analyzeEncodedSystem`

```lean
def analyzeEncodedSystem (encoding) (stepS) (start : S) :
    Except RuntimeCycleError CycleWitness :=
  analyzeTransitionTable (buildTransitionTable encoding stepS).toRaw
    ((encoding.encode start : Fin n) : Nat)
```

```text
typeclasses publicas    0
Except preservado       sim
witness padrao          nenhum
Option.get, getD        ausentes
erro novo               nenhum
totalizacao             nao ocorre
runtime adapter         intacto
```

## Soundness

```lean
theorem analyzeEncodedSystem_sound {encoding} {stepS} {start} {witness}
    (h : analyzeEncodedSystem encoding stepS start = .ok witness) :
    stepS^[witness.baseIndex + witness.period] start = stepS^[witness.baseIndex] start
```

Conclusão **no tipo `S`**. A assinatura tem apenas `h`.

### DAG real, conferido na prova

```text
analyzeTransitionTable_sound
  -> .2.2, terceira conjuncao sobre RawTransitionTable.run?
      -> run?_corresponds_to_typed_iterate, duas vezes
          -> Option.some.inj
              -> Fin.ext
                  -> encode_injective
                      -> igualdade em S
```

Ausências verificadas:

```text
cast manual          0
Eq.ndrec explicito   0
Fintype S            0
DecidableEq S        0
conclusao so em Nat  nao
conclusao so em Fin  nao
```

Nada é afirmado sobre minimalidade ou unicidade.

## Completeness

```lean
theorem analyzeEncodedSystem_complete (encoding) (stepS) (start : S) :
    ∃ witness, analyzeEncodedSystem encoding stepS start = .ok witness
```

**Sem pré-condições.**

```text
toRaw_valid
  -> buildTransitionTable_size
      -> limite de encode start, por Fin.isLt
          -> analyzeTransitionTable_complete
```

```text
witness em Prop            sim
Classical.choose           0
repeticao do detector      0
repeticao do pigeonhole    0
detectCycleWitness? direto 0
```

### O ajuste do linter

```yaml
implementation_adjustment:
  from: "simpa using (tableIndex stepS start).isLt"
  to: "rw [buildTransitionTable_size]; exact (encode start).isLt"
  classification: NON_MATERIAL_LINTER_CLEANUP
  theorem_strength_changed: false
  hypotheses_changed: false
```

O enunciado e as hipóteses são os mesmos; mudou apenas a tática. Com
`buildTransitionTable_size` e `tableIndex_val` ambos `@[simp]`, o `using`
era supérfluo e o linter apontou. A rota explícita não depende do
conjunto `simp`.

## Exclusão universal de erros

```lean
theorem analyzeEncodedSystem_ne_error (encoding) (stepS) (start) (err : RuntimeCycleError) :
    analyzeEncodedSystem encoding stepS start ≠ .error err
```

Quantificado sobre **qualquer** `err`, derivado da completeness. Os três
construtores **permanecem** no tipo executável. Não existem três
corolários redundantes.

## Tipo vazio

```text
CertifiedFiniteEncoding Empty 0    construida no teste
tabela                             #[]
0 < n, Nonempty S, Inhabited S     ausentes da API
chamada artificial de analise      nenhuma
```

`analyzeEncodedSystem` exige `start : S`; com `S` vazio não existe
chamada bem tipada. A ausência é garantida pelo **sistema de tipos**.
