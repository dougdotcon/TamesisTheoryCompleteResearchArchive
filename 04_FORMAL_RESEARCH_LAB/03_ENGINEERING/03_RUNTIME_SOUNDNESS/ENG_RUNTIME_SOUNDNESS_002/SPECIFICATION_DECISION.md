---
document_id: ENG-RUNTIME-SOUNDNESS-002-SPECIFICATION-DECISION
work_item_id: ENG-RUNTIME-SOUNDNESS-002
signatures_frozen: true
public_declarations_added: 2
private_helpers_removed: 3
existing_signatures_broken: 0
probe_exit: 0
versioned_tree_touched: false
---

# Decisao de especificacao — pagar a divida na origem

Probe `exit 0`, arvore intocada.

## As duas declaracoes novas, na frente do runtime

```lean
theorem analyzeTransitionTable_reduce {raw} (hRaw : raw.Valid)
    {start} (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start = (match ... detectCycle? ... )

theorem analyzeTransitionTable_rawValid {raw start w}
    (h : analyzeTransitionTable raw start = .ok w) :
    w.baseIndex < raw.next.size ∧ 0 < w.period ∧
      w.baseIndex + w.period ≤ raw.next.size ∧
        raw.run? (w.baseIndex + w.period) start = raw.run? w.baseIndex start
```

A primeira **ja existe** como `analyze_reduce`, privada. A mudanca e de
visibilidade mais renomeacao. A segunda e nova, e subsume
`analyzeTransitionTable_sound` acrescentando as tres clausulas perdidas.

## O que sai

```text
Monovariants/WitnessBounds.lean       analyze_reduce_public   REMOVIDO
ComputabilityBridge/WitnessBound.lean analyze_reduce_cb       REMOVIDO
UniformPrimrec/Analysis.lean          analyze_reduce_u        REMOVIDO
```

Tres auxiliares privados, tres copias da mesma reducao. Os teoremas que
dependiam deles passam a projetar do contrato:

```lean
analyzeTransitionTable_period_pos  := (rawValid h).2.1
analyzeTransitionTable_bound       := (rawValid h).2.2.1
```

## O que NAO muda

```text
analyzeTransitionTable            semantica intacta
analyzeTransitionTable_sound      assinatura intacta, nao removida
ramo internalDetectorFailure       permanece
assinaturas publicas quebradas     0
```

`analyzeTransitionTable_sound` **fica onde esta**. Alargar nao e
substituir: remove-la quebraria consumidores por nada.

## A clausula que ninguem tinha

`w.baseIndex < raw.next.size` nunca foi exposta a consumidor nenhum. Ela
sai de graca junto com as outras, e e a evidencia de que a divida era
maior do que as duas parcelas ja cobradas.

## Recorte

```text
frente encerrada tocada    ENG-FINITE-STATE-RUNTIME-001, so na soundness
autorizado por             PORTFOLIO_REVIEW_COST_MODEL / DEC-046
custo, complexidade        NAO AUTORIZADOS
```
