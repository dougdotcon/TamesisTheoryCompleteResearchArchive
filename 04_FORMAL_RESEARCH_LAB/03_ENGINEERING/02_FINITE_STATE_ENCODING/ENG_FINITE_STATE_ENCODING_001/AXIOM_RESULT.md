---
document_id: ENC-AXIOM-RESULT
sorryAx: 0
local_axioms: 0
---

# Resultado da auditoria de axiomas

Medido por `TamesisLab/Tests/EngFiniteStateEncoding001Axioms.lean`,
`exit 0`.

```text
CertifiedFiniteEncoding.encode_injective            NENHUM
CertifiedFiniteEncoding.encodedStep                 NENHUM

buildTransitionTable                                propext, Classical.choice, Quot.sound
buildTransitionTable_size                           propext, Classical.choice, Quot.sound
CertifiedFiniteEncoding.tableIndex                  propext, Classical.choice, Quot.sound
CertifiedFiniteEncoding.tableIndex_val              propext, Classical.choice, Quot.sound
CertifiedFiniteEncoding.tableIndex_semiconj         propext, Classical.choice, Quot.sound
CertifiedFiniteEncoding.table_step_commutes         propext, Classical.choice, Quot.sound
CertifiedFiniteEncoding.table_iterate_commutes      propext, Classical.choice, Quot.sound
CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate
                                                    propext, Classical.choice, Quot.sound
analyzeEncodedSystem                                propext, Classical.choice, Quot.sound
analyzeEncodedSystem_sound                          propext, Classical.choice, Quot.sound
analyzeEncodedSystem_complete                       propext, Classical.choice, Quot.sound
analyzeEncodedSystem_ne_error                       propext, Classical.choice, Quot.sound
```

```text
sorryAx          0
axiomas locais   0
```

## Onde a pegada entra, e por quê

```text
PRIMEIRA declaracao a carregar os tres:  buildTransitionTable
CAUSA:                                   campo closed, via Array.getElem_ofFn
```

Toda a camada de codificação — `encode_injective` e `encodedStep` — é
**livre de axiomas**. A pegada propaga daí em diante pelo **tipo**, e não
pela prova: `buildTransitionTable_size`, cujo próprio argumento é
`Array.size_ofFn` (`[propext]`), a herda porque seu enunciado menciona
`buildTransitionTable`.

## A decisão, mantida

```yaml
decision: ACCEPT_INFRASTRUCTURAL_AXIOM_FOOTPRINT
```

Medida na revisão e não reaberta aqui: a rota definicional leve é
**inviável para `n` genérico** — `(Array.ofFn f).size` não é
definicionalmente `n` —, e a definição reutilizada
`analyzeTransitionTable` já carrega os três axiomas, de modo que nada a
jusante melhoraria.

Nenhum experimento destinado a falhar entrou em arquivo Lean permanente,
conforme a regra que `ENC-VAL-001` deixou.

## A regra do laboratório, pela sexta vez

```text
a presenca infraestrutural de propext, Classical.choice e Quot.sound
nao bloqueia se:
  nenhuma definicao for noncomputable;
  a avaliacao funcionar;
  nenhuma escolha classica produzir dado.
```

Os três verificados por execução.
