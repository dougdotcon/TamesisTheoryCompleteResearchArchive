---
document_id: ENC-COMPUTABILITY-REVIEW
supersedes: ENC-COMPUTABILITY-BOUNDARY
stage: SPECIFICATION_REVIEW
verdict: COMPUTABLE
---

# Revisão de computabilidade

## Confirmado por `#eval`

```text
encodedStep              via buildTransitionTable
buildTransitionTable     sete modelos
tableIndex               via decide, sob codificacao permutada
analyzeEncodedSystem     nove avaliacoes
```

Saídas medidas:

```text
buildTransitionTable boolEnc id      #[0, 1]
buildTransitionTable boolEnc not     #[1, 0]
buildTransitionTable idEnc3 fixStep  #[1, 2, 2]
buildTransitionTable idEnc4 tailStep #[1, 2, 3, 2]
buildTransitionTable permEnc tailStep #[1, 0, 1, 2]
buildTransitionTable emptyEnc id     #[]
```

## Proibições verificadas por `grep` antes da execução

```text
sorry              0
admit              0
axiom              0
unsafe             0
noncomputable      0
Classical.choose   0
Classical.decEq    0
Fintype.equivFin   0
Trunc.out          0
Option.get         0
getD               0
modulo             0
clamp              0
fallback           0
```

O `grep` sobre o probe de revisão saiu com código `1` — nenhuma
ocorrência.

## Escolha clássica produzindo dado

```text
nenhuma.
```

A distinção que o gate pediu, feita explicitamente:

```yaml
axioma_usado_por_prova:
  onde: campo closed de buildTransitionTable, via Array.getElem_ofFn
  onde: analyzeTransitionTable e seus teoremas, via Fintype.card
  efeito_na_execucao: nenhum — sao campos e enunciados Prop, apagados

escolha_classica_produzindo_dado_executavel:
  ocorrencias: 0
  evidencia: "#eval devolve arrays e witnesses concretos em sete modelos"
```

## Casts manuais

```text
Eq.ndrec manual   0
cast_heq          0
HEq               0
```

Dois pontos de transporte, ambos declarados; nada mais.

## `#eval` não é extração

```yaml
extraction_status: NOT_AUTHORIZED
cli_status: NOT_AUTHORIZED
parser_status: NOT_AUTHORIZED
integration_status: NOT_AUTHORIZED
```

Nenhum binário, alvo Lake, `main`, `IO`, arquivo, JSON, servidor, rede ou
banco. `lake build` **não** foi executado neste gate.
