---
document_id: ENC-PUBLIC-API-REVIEW
public_declarations: 15
internal_helpers: 1
derived_from_code: true
---

# Revisão da API pública

## Contagem derivada do código, não dos documentos

```text
publicas   15
privadas    1
por especie: 1 structure, 4 def, 10 theorem, 0 instance
```

## `PUBLIC_EXECUTABLE_CORE` — cinco

```text
CertifiedFiniteEncoding                     Encoding.lean
CertifiedFiniteEncoding.encodedStep         Encoding.lean
buildTransitionTable                        TableConstruction.lean
CertifiedFiniteEncoding.tableIndex          TableConstruction.lean
analyzeEncodedSystem                        DynamicAnalysis.lean
```

## `PUBLIC_SPECIFICATION_CORE` — oito

```text
CertifiedFiniteEncoding.encode_injective    Encoding.lean
buildTransitionTable_size                   TableConstruction.lean
CertifiedFiniteEncoding.tableIndex_val      TableConstruction.lean
CertifiedFiniteEncoding.tableIndex_semiconj Commutation.lean
CertifiedFiniteEncoding.table_iterate_commutes            Commutation.lean
CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate Commutation.lean
analyzeEncodedSystem_sound                  DynamicAnalysis.lean
analyzeEncodedSystem_complete               DynamicAnalysis.lean
```

## `PUBLIC_COROLLARY` — dois

```text
CertifiedFiniteEncoding.table_step_commutes Commutation.lean
analyzeEncodedSystem_ne_error               DynamicAnalysis.lean
```

`5 + 8 + 2 = 15`. Conferido contra a lista extraída do código.

## `INTERNAL_HELPER` — um

```yaml
declaration: buildTransitionTable_getElem
module: Commutation.lean
visibility: private
consumers: [tableIndex_semiconj]
adds_mathematical_hypothesis: false
```

A localização em `Commutation.lean` é consequência do escopo de `private`
em Lean 4 — que é o **módulo** — e do fato de seu único consumidor ser a
semiconjugação. Colocá-lo em `TableConstruction.lean` o obrigaria a ser
público. A revisão **não** exige movê-lo por organização narrativa.

Verificação de que ele é mesmo interno: `EngFiniteStateEncoding001.lean`
importa a frente e não o alcança; o umbrella audit importa a raiz e
tampouco.

## Zero typeclasses

Confirmado por seis exemplos genéricos em `S` e `n` no teste formal, sem
`Fintype`, `DecidableEq`, `Nonempty` ou `Inhabited`. Se qualquer uma fosse
exigida, a elaboração falharia por instância ausente.

## Ausências reconfirmadas

```text
stateCount, buildRawTransitionTable, buildValidatedTransitionTable,
transitionArray, segundo tableIndex, segunda orientacao de tamanho,
segunda execucao, novo construtor de erro, toEquiv,
CLI, parser, JSON, IO                                    todos 0
```
