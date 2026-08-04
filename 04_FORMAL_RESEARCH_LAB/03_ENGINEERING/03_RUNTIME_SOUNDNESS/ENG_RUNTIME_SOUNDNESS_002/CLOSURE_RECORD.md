---
document_id: ENG-RUNTIME-SOUNDNESS-002-CLOSURE-RECORD
work_item_id: ENG-RUNTIME-SOUNDNESS-002
work_status: VERIFIED
result_review: APPROVED
extension_status: NOT_AUTHORIZED
---

# Registro de encerramento

## Numeros finais, derivados

```text
declaracoes publicas acrescentadas    2
mudancas de visibilidade              1  (analyze_reduce -> publica)
auxiliares privados removidos         3
copias da reducao restantes           0   <- eram 4
assinaturas publicas quebradas        0
mudancas de semantica                 0
lake build                            exit 0, 8811 jobs, 0 error
```

## O que foi feito

```lean
theorem analyzeTransitionTable_reduce   -- era private analyze_reduce
theorem analyzeTransitionTable_rawValid -- novo, contrato inteiro
```

E as tres copias privadas sairam:

```text
Monovariants/WitnessBounds.lean        analyze_reduce_public   REMOVIDO
ComputabilityBridge/WitnessBound.lean  analyze_reduce_cb       REMOVIDO
UniformPrimrec/Analysis.lean           analyze_reduce_u        REMOVIDO
```

Os teoremas que dependiam delas passaram a **projetar do contrato**:

```lean
analyzeTransitionTable_period_pos := (analyzeTransitionTable_rawValid h).2.1
analyzeTransitionTable_bound      := (analyzeTransitionTable_rawValid h).2.2.1
```

Duas provas de dez linhas viraram uma projecao cada.

## A verificacao que importa

```text
grep private theorem analyze_reduce   ->  0
grep analyze_reduce_{public,cb,u}     ->  0
```

A divida esta paga na origem, e nao contornada.

## O que NAO mudou

```text
analyzeTransitionTable            semantica intacta
analyzeTransitionTable_sound      assinatura intacta, nao removida
ramo internalDetectorFailure       permanece
```

## Fecha

```text
CB-GAP-004   FECHADA
UP-GAP-002   FECHADA
```

## Proxima acao

```text
PORTFOLIO_REVIEW_REQUIRED
```

**Nenhum problema de milenio foi atacado.** Isto e manutencao.
