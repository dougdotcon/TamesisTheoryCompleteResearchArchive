---
document_id: RT-DYNAMIC-ANALYSIS-API
frozen: true
---

# API dinâmica de análise

```lean
def analyzeTransitionTable (raw : RawTransitionTable) (start : Nat) :
    Except RuntimeCycleError CycleWitness := do
  let validated ← validateTransitionTable raw
  let typedStart ← validateStart validated start
  match validated.detectCycle? typedStart with
  | some witness => .ok witness
  | none => .error .internalDetectorFailure
```

## O que esta função faz e não faz

```text
NAO totaliza detectCycleWitness?;
preserva explicitamente o ramo Option impossivel;
converte esse ramo em erro defensivo;
NAO utiliza certificado padrao;
NAO utiliza escolha classica;
NAO esconde erro de tabela ou de estado inicial.
```

A notação `do` sobre `Except` propaga o primeiro erro e para — de modo
que uma tabela inválida **nunca** chega à validação do início, e um
início inválido **nunca** chega ao detector. A ordem é a garantia.

## O ramo `internalDetectorFailure`

Proposicionalmente impossível para entradas válidas, e mesmo assim
presente na função executável.

```text
Manter o ramo eh uma decisao, nao um esquecimento.
```

Três razões:

1. **Não totalizar.** Eliminar o `none` exigiria carregar a prova de
   completude para dentro da definição executável, o que é exatamente a
   totalização que a frente anterior deixou `DEFERRED`.
2. **Honestidade da API.** O tipo `Except` já existe por causa das duas
   validações; acrescentar um terceiro construtor custa nada e documenta
   a fronteira.
3. **Robustez a mudanças.** Se um dia o detector for trocado por Floyd, o
   ramo continua correto sem alteração da assinatura.

E a impossibilidade vira teorema:

```lean
theorem analyzeTransitionTable_ne_internalFailure
    (hRaw : raw.Valid) (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start ≠ .error .internalDetectorFailure
```

derivável da completude.

## Verificado no probe

A versão descartável avaliou nos treze casos previstos:

```text
#[]        start 0   ->  error (initialStateOutOfBounds 0 0)
#[1]       start 0   ->  error transitionDestinationOutOfBounds
#[0]       start 1   ->  error (initialStateOutOfBounds 1 1)
#[0]       start 0   ->  ok <0,1>
#[1,0]     start 0   ->  ok <0,2>
#[1,2,2]   start 0   ->  ok <2,1>
#[1,2,3,2] start 0   ->  ok <2,2>
#[1,2,3,2] start 1   ->  ok <1,2>
#[1,2,3,2] start 2   ->  ok <0,2>
#[1,2,3,2] start 3   ->  ok <0,2>
#[0,2,1]   start 0   ->  ok <0,1>
#[0,2,1]   start 1   ->  ok <0,2>
#[0,2,1]   start 2   ->  ok <0,2>
```

Os quatro que produzem certificado a partir de `#[0]`, `#[1,0]`,
`#[1,2,2]` e `#[1,2,3,2]` reproduzem **exatamente** os resultados dos
modelos `Fin 1`, `Bool`, `Fin 3` e `Fin 4` já verificados no detector —
o que dá à frente um **oráculo** independente.

## Hipóteses do consumidor

```text
o consumidor fornece Array Nat e Nat.
```

Nada mais. Sem `Fintype`, sem `DecidableEq`, sem `Fin`, sem provas, sem
funções Lean. Esse é o ganho central da frente, e a assinatura de
`analyzeTransitionTable` é a sua expressão.
