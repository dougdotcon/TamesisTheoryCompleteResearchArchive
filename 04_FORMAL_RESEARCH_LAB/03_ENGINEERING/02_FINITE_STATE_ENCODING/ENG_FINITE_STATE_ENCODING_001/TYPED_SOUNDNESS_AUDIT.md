---
document_id: ENC-TYPED-SOUNDNESS-AUDIT
conclusion_type: S
---

# Auditoria da soundness tipada

## Enunciado implementado

```lean
theorem analyzeEncodedSystem_sound {encoding : CertifiedFiniteEncoding S n}
    {stepS : S → S} {start : S} {witness : CycleWitness}
    (h : analyzeEncodedSystem encoding stepS start = .ok witness) :
    stepS^[witness.baseIndex + witness.period] start = stepS^[witness.baseIndex] start
```

**A conclusão é uma igualdade em `S`.** Não sobre `Nat`, não sobre
`Fin n`, não sobre o `Array`. `STOP-ENC-018` não disparou.

A assinatura tem **apenas** `h`. Nenhuma hipótese adicional é imposta ao
consumidor.

## Prova implementada

```lean
  have hrun := (analyzeTransitionTable_sound h).2.2
  rw [encoding.run?_corresponds_to_typed_iterate stepS
        (witness.baseIndex + witness.period) start,
      encoding.run?_corresponds_to_typed_iterate stepS witness.baseIndex start] at hrun
  exact encoding.encode_injective (Fin.ext (Option.some.inj hrun))
```

Quatro linhas.

## DAG, seta a seta

```text
analyzeTransitionTable_sound                (frente anterior)
  -> .2.2 : run? (b+p) start = run? b start, sobre o Array construido
      -> run?_corresponds_to_typed_iterate, lado esquerdo
      -> run?_corresponds_to_typed_iterate, lado direito
          -> some (encode (stepS^[b+p] start)) = some (encode (stepS^[b] start))
              -> Option.some.inj              [sem axiomas]
                  -> Fin.ext                  [sem axiomas]
                      -> encode_injective     [sem axiomas]
                          -> IGUALDADE EM S
```

As três últimas setas não dependem de axioma nenhum — medido.

## Ausências verificadas

```text
cast                       0
Eq.ndrec                   0
transporte dependente      0
DecidableEq S              0
Fintype S                  0
hipoteses extras           0
```

Não houve transporte porque a expressão do enunciado é **sintaticamente**
a expressão da prova: `run?_corresponds_to_typed_iterate` fala de
`(buildTransitionTable encoding stepS).toRaw.run?`, exatamente o que
`analyzeTransitionTable_sound` produz. Mesma técnica que a frente
anterior usou ao escolher a tabela concreta.

## O que a soundness NÃO afirma

```text
minimalidade de baseIndex ou period;
unicidade do witness;
canonicidade da entrada;
minimalPeriod;
independencia da ordem de busca;
invariancia sob recodificacao.
```

## Teste imediato

```text
lake env lean TamesisLab/Engineering/FiniteStateEncoding/DynamicAnalysis.lean
exit 0
```

`ENG_FINITE_STATE_ENCODING_001_TYPED_SOUNDNESS_FAILED` não disparou.

## Interpretação semântica, medida

Três exemplos concluem igualdades **no tipo original**, obtendo o witness
por `decide`:

```lean
example : tailStep^[2 + 2] ⟨0, _⟩ = tailStep^[2] ⟨0, _⟩ := ...   -- idEnc4
example : tailStep^[2 + 2] ⟨0, _⟩ = tailStep^[2] ⟨0, _⟩ := ...   -- permEnc
example : not^[0 + 2] true = not^[0] true := ...                 -- boolEnc
```

Os dois primeiros usam **codificações diferentes** e chegam à **mesma
conclusão semântica**. É isso que a frente prova; a coincidência dos
witnesses concretos, não.
