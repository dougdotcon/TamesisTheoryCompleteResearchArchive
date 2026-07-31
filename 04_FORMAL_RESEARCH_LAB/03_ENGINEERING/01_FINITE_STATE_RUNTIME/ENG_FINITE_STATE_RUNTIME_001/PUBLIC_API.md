---
document_id: RT-PUBLIC-API
declarations: 29
---

# API pública

Vinte e nove declarações, classificadas.

## `PUBLIC_EXECUTABLE_CORE` — dez

```yaml
- declaration: RawTransitionTable
  module: RawTable.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  role: "dado recebido; pode conter destinos invalidos"
  dependencies: [Array]
  axioms: nenhum
  recommended_for_reuse: true

- declaration: ValidatedTransitionTable
  module: RawTable.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  role: "dado com fechamento provado; campo Prop apagado na execucao"
  dependencies: [Array, Fin]
  axioms: nenhum
  recommended_for_reuse: true

- declaration: RuntimeCycleError
  module: Validation.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  role: "tres construtores; tabela, consulta e defesa"
  dependencies: []
  axioms: nenhum
  recommended_for_reuse: true

- declaration: validateTransitionTable
  module: Validation.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  role: "rejeita destinos invalidos, nunca corrige"
  dependencies: [RawTransitionTable.decidableValid]
  axioms: "[propext, Quot.sound]"
  recommended_for_reuse: true

- declaration: validateStart
  module: Validation.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  role: "valida a consulta, preservando start exatamente"
  dependencies: [Nat.decLt]
  axioms: "[propext, Quot.sound]"
  recommended_for_reuse: true

- declaration: ValidatedTransitionTable.step
  module: Execution.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  role: "onde o dado dinamico vira sistema formal"
  dependencies: [ValidatedTransitionTable.closed]
  axioms: "[propext, Quot.sound]"
  recommended_for_reuse: true

- declaration: RawTransitionTable.step?
  module: Execution.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  role: "um passo sobre o array; none fora dos limites"
  dependencies: [GetElem?]
  axioms: "does not depend on any axioms"
  recommended_for_reuse: true

- declaration: RawTransitionTable.run?
  module: Execution.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  role: "semantica bruta parcial; run? 0 nao valida"
  dependencies: [RawTransitionTable.step?]
  axioms: "does not depend on any axioms"
  recommended_for_reuse: true

- declaration: ValidatedTransitionTable.detectCycle?
  module: DetectorAdapter.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  role: "detector certificado aplicado a step; Fintype e DecidableEq INFERIDAS"
  dependencies: [detectCycleWitness?]
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true

- declaration: analyzeTransitionTable
  module: DynamicAnalysis.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  role: "API dinamica; Array Nat e Nat como unica entrada"
  dependencies: [validateTransitionTable, validateStart, detectCycle?]
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true
```

## `PUBLIC_SPECIFICATION_CORE` — quinze

```yaml
- declaration: RawTransitionTable.Valid
  module: RawTable.lean
  role: "validade estrutural; nao afirma alcancabilidade nem ciclo unico"
  computable: "proposicional, decidivel"
  axioms: "[propext, Quot.sound]"

- declaration: ValidatedTransitionTable.toRaw
  module: RawTable.lean
  role: "volta ao bruto; torna os teoremas centrais enunciaveis"
  computable: true
  axioms: nenhum

- declaration: ValidatedTransitionTable.toRaw_valid
  module: RawTable.lean
  role: "a tabela convertida eh valida"
  axioms: "[propext, Quot.sound]"

- declaration: validateTransitionTable_sound
  role: "validated.toRaw = raw ∧ raw.Valid — forca a tabela a ser A MESMA"
  axioms: "[propext, Quot.sound]"

- declaration: validateTransitionTable_complete
  role: "toda tabela valida eh aceita"
  axioms: "[propext, Quot.sound]"

- declaration: validateStart_sound
  role: "(typedStart : Nat) = start — teorema ANTI-CLAMP"
  axioms: "[propext, Quot.sound]"

- declaration: validateStart_complete
  role: "todo indice no dominio eh aceito"
  axioms: "[propext, Quot.sound]"

- declaration: valid_empty
  role: "a tabela vazia eh estruturalmente valida"
  axioms: "[propext, Quot.sound]"

- declaration: ValidatedTransitionTable.step_val
  role: "@[simp]; a transicao tipada eh o lookup"
  axioms: "[propext, Quot.sound]"

- declaration: ValidatedTransitionTable.step?_eq_some_step
  role: "lookup opcional = step total"
  axioms: "[propext, Quot.sound]"

- declaration: ValidatedTransitionTable.run?_eq_iterate_step
  role: "execucao bruta = iteracao tipada — resultado central"
  axioms: "[propext, Quot.sound]"

- declaration: ValidatedTransitionTable.detectCycle?_sound
  role: "herdado do detector, termo de uma linha"
  axioms: "[propext, Classical.choice, Quot.sound]"

- declaration: ValidatedTransitionTable.detectCycle?_complete
  role: "herdado do detector, termo de uma linha"
  axioms: "[propext, Classical.choice, Quot.sound]"

- declaration: ValidatedTransitionTable.detectCycle?_raw_repeat
  role: "o certificado, reinterpretado sobre a tabela original"
  axioms: "[propext, Classical.choice, Quot.sound]"

- declaration: analyzeTransitionTable_sound
  role: "validade, dominio e repeticao sobre o array original"
  axioms: "[propext, Classical.choice, Quot.sound]"

- declaration: analyzeTransitionTable_complete
  role: "toda entrada valida produz certificado"
  axioms: "[propext, Classical.choice, Quot.sound]"
```

## `PUBLIC_COROLLARY` — três

```text
analyzeTransitionTable_invalid_table
analyzeTransitionTable_invalid_start
analyzeTransitionTable_ne_internalFailure
```

Os dois primeiros **congelam a precedência dos erros**; o terceiro prova
a impossibilidade do ramo defensivo. Todos com pegada herdada do
detector.

## `INSTANCE_SUPPORT` — um

```yaml
- declaration: RawTransitionTable.decidableValid
  module: RawTable.lean
  category: INSTANCE_SUPPORT
  hypotheses: []
  computable: true
  role: "torna Valid decidivel; sem ela o dite nao elabora"
  dependencies: [Fintype.decidableForallFintype, Nat.decLt]
  axioms: "[propext, Quot.sound]"
  recommended_for_reuse: "sim, implicitamente — encontrada por sintese"
```

## `INTERNAL_HELPER` — um

```yaml
- declaration: analyze_reduce
  module: DynamicAnalysis.lean
  category: INTERNAL_HELPER
  visibility: private
  role: "encapsula as duas reducoes que a notacao do esconde"
  adds_mathematical_hypothesis: false
```

## `TEST_ONLY`

Os modelos concretos dos testes — `#[]`, `#[0]`, `#[1]`, `#[1,0]`,
`#[1,2,2]`, `#[1,2,3,2]`, `#[0,2,1]` — definidos nos arquivos de teste e
não exportados.

## Ausências confirmadas

```text
stateCount                       NAO existe
Subtype RawTransitionTable.Valid NAO existe como API publica
CLI, parser, JSON, rede          NAO existem
diagnostico detalhado            NAO existe
qualquer teorema de minimalidade NAO existe
```
