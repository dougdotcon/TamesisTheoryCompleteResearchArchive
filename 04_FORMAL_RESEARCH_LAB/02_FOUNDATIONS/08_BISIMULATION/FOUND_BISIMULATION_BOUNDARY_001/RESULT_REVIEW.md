---
document_id: FOUND-BISIMULATION-BOUNDARY-001-RESULT-REVIEW
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
review_start_head: 25e85ff9f9386a658d01ec3aba0b45c1d115526b
decision: FOUND_BISIMULATION_BOUNDARY_001_RESULT_REVIEW_APPROVED
---

# Revisão de resultado

## Reexecução independente

Nada foi herdado do gate anterior:

```text
lake build            REAL_BUILD_EXIT=0, 8775 jobs, 0 erros reais
modulos isolados      8 de 8, exit 0, errors 0
contagem derivada     8 publicas, 2 TEST_ONLY
tokens proibidos      0
typeclasses no nucleo 0
frentes encerradas    NO_CLOSED_FRONT_FILES_CHANGED
pytest                34 passed
labctl validate       PASS
varredura YAML        413 arquivos, 0 duplicatas
```

## Os doze itens

| # | Item | Verdito |
|---|---|---|
| 1 | `Reflects` não trivializado | CONFIRMADO |
| 2 | `simulates_iff_semiconj` é `Iff.rfl` | CONFIRMADO |
| 3 | `reflects_iff_simulates` não é `Iff.rfl` | CONFIRMADO |
| 4 | colapso provado | CONFIRMADO |
| 5 | contraexemplo é bissimulação | CONFIRMADO |
| 6 | abstração é sobrejetiva | CONFIRMADO |
| 7 | as duas negações compilam | CONFIRMADO |
| 8 | pegada axiomática nula | CONFIRMADO |
| 9 | nenhuma typeclass | CONFIRMADO |
| 10 | recorte documentado e respeitado | CONFIRMADO |
| 11 | contagem derivada = declarada | CONFIRMADO |
| 12 | frentes encerradas intocadas | CONFIRMADO |

## O item 11, que exigiu correção

A primeira organização derivava `10` contra `8` congeladas. Corrigida
**movendo o código**, não a contagem: `boolToUnit_bisimulation` e
`forgetBool_surjective` foram para `CounterexampleInstance.lean`.

Registro honesto: elas continuam **residentes na biblioteca**, e não nos
testes, porque as negações públicas as consomem. Isso segue o precedente
de `FiniteStateAbstraction/Counterexample.lean`, e está declarado em
[`PUBLIC_API.md`](PUBLIC_API.md) em vez de escondido na contagem.

## Dois incidentes de medição, ambos registrados

1. **Falso negativo de elaboração isolada.** Dois módulos reportaram
   `exit=1` enquanto o build passava. Causa verificada: `lake env lean`
   não constrói dependências, e o `.olean` do módulo recém-criado ainda
   não existia. Reexecutados após o build: `exit=0` nos oito.

2. **Duas chaves YAML duplicadas, introduzidas por mim.** Um patch
   anterior órfãou duas linhas do bloco `probe:` do `STATUS.yaml`, que
   caíram dentro de `formalization:` e colidiram; e um
   `formalization_status` obsoleto sobreviveu na fila.

   Foram **detectadas pelo scanner ampliado em
   `LAB-GOV-FRONTMATTER-SCAN-001`**, antes do commit, e corrigidas. O
   gate de correção do instrumento pagou por si mesmo dois gates depois.

## Pegada

```text
10 de 10 declaracoes: does not depend on any axioms
```

A frente não atravessa `analyzeEncodedSystem`, então nem `propext` entra.

## Claim

Uma única claim, `DETERMINISTIC-BISIMULATION-COLLAPSE-FORMAL-001`,
`evidence_level: F`, novidade `NONE`. Wording conferida contra as listas
permitida e proibida, com atenção ao qualificador obrigatório.

```text
ledger antes   23
ledger depois  24
```

## Decisão

```text
FOUND_BISIMULATION_BOUNDARY_001_RESULT_REVIEW_APPROVED
```

## Ressalva de independência

Os quatro gates da frente foram executados pelo mesmo agente em sessões
consecutivas. Nenhum substitui revisão externa. O que sustenta o
resultado é o que foi medido e reexecutado — e, neste caso, também o que
uma ferramenta independente do agente recusou.
