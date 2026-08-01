---
document_id: ENC-FINAL-DYNAMIC-ANALYSIS-BRIDGE
supersedes: [ENC-DYNAMIC-ANALYSIS-BRIDGE, ENC-SOUNDNESS-PLAN, ENC-COMPLETENESS-PLAN]
stage: SPECIFICATION_REVIEW
frozen: true
---

# Ponte dinâmica final

## A API

```lean
def analyzeEncodedSystem (e : CertifiedFiniteEncoding S n) (stepS : S → S) (start : S) :
    Except RuntimeCycleError CycleWitness :=
  analyzeTransitionTable (buildTransitionTable e stepS).toRaw
    ((e.encode start : Fin n) : Nat)
```

Verificado no probe:

```text
typeclasses exigidas          0
witness padrao                nenhum
Option.get                    ausente
tipo de erro novo             nenhum
parser                        ausente
totalizacao do detector       nao ocorre
runtime adapter modificado    nao
```

## Soundness tipada

```lean
theorem analyzeEncodedSystem_sound {e} {stepS} {start} {witness}
    (h : analyzeEncodedSystem e stepS start = Except.ok witness) :
    stepS^[witness.baseIndex + witness.period] start = stepS^[witness.baseIndex] start := by
  have hrun := (analyzeTransitionTable_sound h).2.2
  rw [e.run?_corresponds_to_typed_iterate stepS (witness.baseIndex + witness.period) start,
      e.run?_corresponds_to_typed_iterate stepS witness.baseIndex start] at hrun
  exact e.encode_injective (Fin.ext (Option.some.inj hrun))
```

Quatro linhas. Compilou.

### DAG completo, verificado

```text
analyzeTransitionTable_sound
  -> a terceira conjuncao: igualdade entre run? sobre o Array construido
      -> run?_corresponds_to_typed_iterate, lado esquerdo
      -> run?_corresponds_to_typed_iterate, lado direito
          -> Option.some.inj          (sem axiomas)
              -> Fin.ext              (sem axiomas)
                  -> encode_injective (sem axiomas)
                      -> IGUALDADE EM S
```

A conclusão é uma igualdade em `S`. **Não** é
`encode lhs = encode rhs`; a injetividade é aplicada, e a última seta do
DAG é justamente ela. `STOP-ENC-018` não disparou.

Nenhum `DecidableEq S`, nenhum `Fintype S`, nenhuma hipótese extra: a
assinatura tem apenas `h`.

### O que a soundness não afirma

```text
minimalidade de baseIndex ou period;
unicidade do witness;
canonicidade da entrada;
minimalPeriod;
independencia da ordem de busca.
```

## Completeness tipada

```lean
theorem analyzeEncodedSystem_complete (e) (stepS) (start : S) :
    ∃ witness, analyzeEncodedSystem e stepS start = Except.ok witness :=
  analyzeTransitionTable_complete _ _ (buildTransitionTable e stepS).toRaw_valid
    (by
      show ((e.encode start : Fin n) : Nat) < (buildTransitionTable e stepS).next.size
      rw [buildTransitionTable_size]
      exact (e.encode start).isLt)
```

**Sem pré-condições do consumidor.** As duas que a frente anterior exigia
são agora consequências da construção.

### DAG completo, verificado

```text
buildTransitionTable.toRaw_valid
  -> validade estrutural
      -> buildTransitionTable_size
          -> encode start possui limite, por Fin.isLt
              -> analyzeTransitionTable_complete
```

Não são repetidos: pigeonhole, `exists_bounded_iterate_collision`,
`cycleCandidates`, `detectCycleWitness?`. A reutilização é indireta, já
encapsulada no runtime adapter. Nenhum `Classical.choose`; o witness
permanece existencial em `Prop`.

## Exclusão universal de erros

```lean
theorem analyzeEncodedSystem_ne_error (e) (stepS) (start : S) (err : RuntimeCycleError) :
    analyzeEncodedSystem e stepS start ≠ Except.error err := by
  obtain ⟨witness, hw⟩ := analyzeEncodedSystem_complete e stepS start
  rw [hw]
  simp
```

**Um** corolário público, quantificado sobre `err`. As três exclusões
específicas ficam `DEFERRED_OPTIONAL`.

Os construtores de erro **permanecem** no tipo executável, porque a
função reutilizada continua baseada em `Except` — e porque a
impossibilidade é teorema, não motivo de remoção.

Medido no probe, nas duas formas exigidas:

```lean
example : analyzeEncodedSystem permEnc tailStep ⟨0,_⟩
    ≠ Except.error RuntimeCycleError.internalDetectorFailure := ...
example (err) : analyzeEncodedSystem boolEnc not true ≠ Except.error err := ...
```

## Caso vazio

```yaml
empty_state_type_policy:
  encoding_structure: ALLOWED
  table_construction: ALLOWED
  table_structural_validity: VALID
  analysis_call: UNINHABITED
```

`CertifiedFiniteEncoding Empty 0` foi construída; a tabela avaliou para
`#[]`. Nenhum `0 < n`, `Nonempty S` ou `Inhabited S` foi adicionado.
`analyzeEncodedSystem` exige `start : S`, e com `S` vazio **não existe
chamada bem tipada** — a ausência é garantida pelo sistema de tipos.
