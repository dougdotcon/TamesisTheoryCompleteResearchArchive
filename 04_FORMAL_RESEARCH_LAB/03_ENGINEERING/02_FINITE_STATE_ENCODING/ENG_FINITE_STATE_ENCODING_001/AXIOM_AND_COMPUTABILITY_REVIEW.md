---
document_id: ENC-AXIOM-AND-COMPUTABILITY-REVIEW
sorryAx: 0
local_axioms: 0
---

# Revisão de axiomas e computabilidade

## Medido no teste de axiomas, `exit 0`

```text
encode_injective                    NENHUM
encodedStep                         NENHUM

buildTransitionTable                propext, Classical.choice, Quot.sound
buildTransitionTable_size           propext, Classical.choice, Quot.sound
tableIndex                          propext, Classical.choice, Quot.sound
tableIndex_val                      propext, Classical.choice, Quot.sound
tableIndex_semiconj                 propext, Classical.choice, Quot.sound
table_step_commutes                 propext, Classical.choice, Quot.sound
table_iterate_commutes              propext, Classical.choice, Quot.sound
run?_corresponds_to_typed_iterate   propext, Classical.choice, Quot.sound
analyzeEncodedSystem                propext, Classical.choice, Quot.sound
analyzeEncodedSystem_sound          propext, Classical.choice, Quot.sound
analyzeEncodedSystem_complete       propext, Classical.choice, Quot.sound
analyzeEncodedSystem_ne_error       propext, Classical.choice, Quot.sound
```

```text
sorryAx          0
axiomas locais   0
```

## Primeira aparição

```text
buildTransitionTable — pelo campo closed, via Array.getElem_ofFn
```

Toda a camada de codificação é **livre de axiomas**. A pegada propaga
daí em diante pelo **tipo**: `buildTransitionTable_size`, cujo argumento
`Array.size_ofFn` é `[propext]`, a herda porque seu enunciado menciona
`buildTransitionTable`.

## Computabilidade

```text
CertifiedFiniteEncoding   dados fornecidos
encodedStep               computavel
buildTransitionTable      computavel
tableIndex                computavel
analyzeEncodedSystem      computavel
```

Sete tabelas concretas verificadas por `decide`, incluindo o tipo vazio.

## A distinção, reafirmada

```yaml
axioma_usado_por_prova:
  onde: campo closed; e analyzeTransitionTable, via Fintype.card
  efeito_na_execucao: nenhum — sao Prop, apagados

escolha_classica_produzindo_dado:
  encode: 0
  decode: 0
  Array: 0
  witness executavel: 0
```

## Tokens proibidos

```text
sorry, admit, axiom, unsafe, noncomputable,
Classical.choose, Classical.decEq, Fintype.equivFin,
Trunc.out, Option.get, getD
```

Busca sobre os cinco módulos, o agregador e os quatro testes: saída
vazia, código `1`. **Zero.**

## Correções silenciosas

```text
%, mod, clamp, fallback, min, max   0
```

Saída vazia, código `1`. Nenhuma ocorrência sequer textual. `Fin.cast` é
transporte de tipo, e `tableIndex_val` prova que preserva o valor.
