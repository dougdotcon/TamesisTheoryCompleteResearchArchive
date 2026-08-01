---
document_id: ENC-PUBLIC-API
public_declarations: 15
internal_helpers: 1
---

# API pública formalizada

**Quinze** declarações públicas e **um** auxiliar interno.

`FINAL_PUBLIC_API.md` declarava `14` no cabeçalho, mas listava quinze
itens. O número medido nos módulos é `15`; a correção está registrada em
`FORMALIZATION_RESULT.md`.

## `PUBLIC_EXECUTABLE_CORE` — cinco

```yaml
- declaration: CertifiedFiniteEncoding
  module: Encoding.lean
  hypotheses: []
  computable: true
  axioms: nenhum
  role: "bijecao FORNECIDA; dois campos de dado, duas leis"

- declaration: CertifiedFiniteEncoding.encodedStep
  module: Encoding.lean
  hypotheses: []
  computable: true
  axioms: nenhum
  role: "unico nome publico do conteudo da tabela"

- declaration: buildTransitionTable
  module: TableConstruction.lean
  hypotheses: []
  computable: true
  axioms: "[propext, Classical.choice, Quot.sound]"
  role: "unica construcao publica; devolve ValidatedTransitionTable"

- declaration: CertifiedFiniteEncoding.tableIndex
  module: TableConstruction.lean
  hypotheses: []
  computable: true
  role: "UNICO transporte publico Fin n -> Fin table.next.size"

- declaration: analyzeEncodedSystem
  module: DynamicAnalysis.lean
  hypotheses: []
  computable: true
  role: "API tipada; codificacao, passo e estado inicial"
```

## `PUBLIC_SPECIFICATION_CORE` — oito

```yaml
- CertifiedFiniteEncoding.encode_injective      # fecha a soundness em S
- buildTransitionTable_size                     # @[simp]; orientacao size = n
- CertifiedFiniteEncoding.tableIndex_val        # @[simp]; ANTI-CORRECAO, por rfl
- CertifiedFiniteEncoding.tableIndex_semiconj   # resultado semantico PRINCIPAL
- CertifiedFiniteEncoding.table_iterate_commutes
- CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate
- analyzeEncodedSystem_sound                    # igualdade em S
- analyzeEncodedSystem_complete                 # sem pre-condicoes
```

## `PUBLIC_COROLLARY` — dois

```yaml
- CertifiedFiniteEncoding.table_step_commutes   # (semiconj s).symm
- analyzeEncodedSystem_ne_error                 # quantificado sobre err
```

## `INTERNAL_HELPER` — um

```yaml
- declaration: buildTransitionTable_getElem
  module: Commutation.lean
  visibility: private
  adds_mathematical_hypothesis: false
```

Ele vive em `Commutation.lean`, e não em `TableConstruction.lean`, por
uma razão concreta: `private` em Lean 4 é escopo de **módulo**, e o único
consumidor é `tableIndex_semiconj`. Colocá-lo junto da construção o
obrigaria a ser público.

## Ausências confirmadas por busca

```text
stateCount                      0
buildRawTransitionTable         0
buildValidatedTransitionTable   0
transitionArray                 0
segunda orientacao do tamanho   0
segundo tableIndex              0
segunda funcao de execucao      0
novo construtor de erro         0
toEquiv                         0
CLI, parser, JSON, IO           0
```

## Imports

```text
Encoding.lean          TamesisLab.Engineering.FiniteStateRuntime
TableConstruction.lean ...FiniteStateEncoding.Encoding
Commutation.lean       ...FiniteStateEncoding.TableConstruction
DynamicAnalysis.lean   ...FiniteStateEncoding.Commutation
```

**Um import por módulo.** Nenhum import de Mathlib foi acrescentado:
`Array.ofFn`, `Array.size_ofFn`, `Array.getElem_ofFn`, `Fin.cast`,
`Fin.ext`, `Function.LeftInverse.injective`, `Function.Semiconj` e
`Function.Semiconj.iterate_right` já eram alcançados pela frente anterior.

`Mathlib.Data.Fintype.EquivFin` **não** é importado — e essa ausência é
uma barreira, não uma economia.
