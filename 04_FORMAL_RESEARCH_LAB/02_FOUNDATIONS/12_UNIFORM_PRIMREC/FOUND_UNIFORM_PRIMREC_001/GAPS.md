---
document_id: FOUND-UNIFORM-PRIMREC-001-GAPS
work_item_id: FOUND-UNIFORM-PRIMREC-001
gaps_opened: 5
gaps_closed_at_specification: 0
closes_gap_from_other_front: CB-GAP-001
---

# Lacunas

| id | conteudo | estado |
|---|---|---|
| `UP-GAP-001` | modelo de custo — herdada de `CB-GAP-002` | **DELIBERADAMENTE ABERTA** |
| `UP-GAP-002` | quarta reproducao da reducao do bloco `do` | ABERTA |
| `UP-GAP-003` | cota primitiva recursiva explicita no numero de passos | ABERTA |
| `UP-GAP-004` | `analyzeEncodedSystem` uniforme sobre a codificacao | ABERTA |
| `UP-GAP-005` | classes de complexidade sobre a maquina do laboratorio | ABERTA |

## O que esta frente FECHA

```text
CB-GAP-001   Primrec2 analyzeTransitionTable   FECHADA
```

E a unica lacuna da ponte com conteudo algoritmico, e fecha com prova, nao
com declaracao.

## `UP-GAP-003`, a que separa esta frente de custo

Provar `Primrec` e exibir **alguma** derivacao primitiva recursiva. Nao e
exibir uma **cota**. A frente nao enuncia quantos passos a analise gasta,
e enunciar isso exigiria um modelo de maquina — `UP-GAP-001`.

## `UP-GAP-002`, a divida que agora tem quatro parcelas

```text
FiniteStateRuntime/DynamicAnalysis.lean   original, privada
Monovariants/WitnessBounds.lean           segunda
ComputabilityBridge/WitnessBound.lean     terceira
UniformPrimrec/Analysis.lean              quarta
```

A correcao propria continua sendo alargar `analyzeTransitionTable_sound`,
o que toca frente encerrada e exige gate proprio.
