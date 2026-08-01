---
document_id: ENC-PUBLIC-API-SPECIFICATION
declarations: 16
---

# API pública planejada

Dezesseis declarações. A frente anterior tinha vinte e nove; esta é
menor de propósito, porque reutiliza em vez de reconstruir.

## `PUBLIC_EXECUTABLE_CORE` — cinco

```yaml
- declaration: CertifiedFiniteEncoding
  module: Encoding.lean
  hypotheses: []
  computable: true
  role: "bijecao FORNECIDA entre S e Fin n; dois campos de dado, dois Prop"
  dependencies: [Fin]
  recommended_for_reuse: true

- declaration: CertifiedFiniteEncoding.encodedStep
  module: Encoding.lean
  hypotheses: []
  computable: true
  role: "encode ∘ stepS ∘ decode; total por construcao"
  dependencies: [CertifiedFiniteEncoding]
  recommended_for_reuse: true

- declaration: buildTransitionTable
  module: TableConstruction.lean
  hypotheses: []
  computable: true
  role: "unica construcao publica; devolve ValidatedTransitionTable"
  dependencies: [Array.ofFn, encodedStep]
  recommended_for_reuse: true

- declaration: CertifiedFiniteEncoding.tableIndex
  module: TableIndex.lean
  hypotheses: []
  computable: true
  role: "UNICO ponto de transporte Fin n -> Fin table.next.size"
  dependencies: [Fin.cast, buildTransitionTable_size]
  recommended_for_reuse: true

- declaration: analyzeEncodedSystem
  module: TypedAnalysis.lean
  hypotheses: []
  computable: true
  role: "API tipada; entrada eh a codificacao, o passo e o estado inicial"
  dependencies: [buildTransitionTable, analyzeTransitionTable]
  recommended_for_reuse: true
```

## `PUBLIC_SPECIFICATION_CORE` — oito

```yaml
- declaration: CertifiedFiniteEncoding.encode_injective
  role: "fecha a soundness em S"

- declaration: buildTransitionTable_size
  role: "UNICA ponte publica entre Fin n e Fin table.next.size; orientacao size = n"

- declaration: buildTransitionTable_getElem
  role: "lema central de leitura; segundo e ultimo ponto de transporte"

- declaration: tableIndex_val
  role: "ANTI-CORRECAO: o cast nao modifica o indice natural; por rfl"

- declaration: table_step_commutes
  role: "comutacao de um passo; enunciado legivel"

- declaration: tableIndex_semiconj
  role: "a mesma comutacao na forma que Semiconj.iterate_right consome"

- declaration: table_iterate_commutes
  role: "comutacao de iteradas; corolario de uma linha"

- declaration: run?_corresponds_to_typed_iterate
  role: "execucao bruta da tabela construida = trajetoria tipada"

- declaration: analyzeEncodedSystem_sound
  role: "repeticao PROVADA em S"

- declaration: analyzeEncodedSystem_complete
  role: "toda entrada tipada produz certificado; SEM pre-condicoes"
```

## `PUBLIC_COROLLARY` — um

```text
analyzeEncodedSystem_ne_error
```

Quantificado sobre o erro; substitui três exclusões individuais.

## `OPTIONAL_ADAPTER` — dois

```text
CertifiedFiniteEncoding.toEquiv        S ≃ Fin n
positive_size_of_state                 0 < n a partir de um estado
CertifiedFiniteEncoding.decode_surjective
```

Nenhum entra na cadeia computacional. `toEquiv` **não** pode ser criado
por `Fintype.equivFin`.

## `DEFERRED`

```text
exclusoes individuais dos tres construtores de erro;
decode injetiva, encode sobrejetiva;
qualquer teorema de minimalidade;
qualquer modelo de custo.
```

## Ausências confirmadas

```text
stateCount                      NAO existe
buildRawTransitionTable         NAO existe
buildValidatedTransitionTable   NAO existe
table_size_eq / size_table_eq   NAO existem
segunda funcao de execucao      NAO existe
novo tipo de erro               NAO existe
CLI, parser, JSON, IO           NAO existem
```


---

## Revisão — `2066edc`

Este documento é **superado** por `FINAL_PUBLIC_API.md`. Registro
preservado para histórico.

Mudanças da revisão: `tableIndex_semiconj` passa a teorema semântico
principal; `table_step_commutes` passa a `PUBLIC_COROLLARY`;
`buildTransitionTable_getElem` passa a `INTERNAL_HELPER`; `tableIndex_val`
recebe `@[simp]`. Declarações públicas: `16 → 14`.
