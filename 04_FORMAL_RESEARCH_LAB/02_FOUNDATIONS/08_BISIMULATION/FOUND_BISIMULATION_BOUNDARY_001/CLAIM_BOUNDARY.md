---
document_id: FOUND-BISIMULATION-BOUNDARY-001-CLAIM-BOUNDARY
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
claim_candidate: DETERMINISTIC-BISIMULATION-COLLAPSE-FORMAL-001
claims_promoted_in_this_gate: 0
---

# Fronteira da claim

```text
claims promovidas neste gate   0
ledger permanece               23
```

## Claim candidata

```yaml
claim_id: DETERMINISTIC-BISIMULATION-COLLAPSE-FORMAL-001
domain: formal_semantics
work_status: VERIFIED
evidence_level: F
mathematical_novelty: NONE
algorithmic_novelty: NONE
```

## Wording permitida

```text
Foi formalizado em Lean que, para sistemas deterministicos
totais, a bissimulacao funcional dada pelo grafico de uma funcao
de abstracao coincide com a semiconjugacao.

Foi provado que o contraexemplo BOOL_TO_UNIT ja satisfaz essa
bissimulacao, e que a funcao de abstracao e sobrejetiva.

Foi provado que nem bissimulacao nem bissimulacao sobrejetiva
refletem recorrencia abstrata como recorrencia concreta.
```

## Wording proibida

```text
bissimulacao e o mesmo que semiconjugacao        (sem qualificador)
bissimulacao e inutil
bissimulacao foi refutada
sistemas nao deterministicos se comportam assim
resultado novo em semantica de concorrencia
novidade matematica
novo algoritmo
```

## A distinção que a wording precisa carregar

```text
CERTO   "para sistemas deterministicos totais, a bissimulacao
         FUNCIONAL coincide com a semiconjugacao"

ERRADO  "bissimulacao e semiconjugacao"
```

A segunda forma é falsa na teoria de concorrência, que é não
determinística e rotulada. Ver [`SCOPE_BOUNDARY.md`](SCOPE_BOUNDARY.md).

## Evidência exigida antes da promoção

```text
lake build            exit 0
testes formais        PASS
auditoria de axiomas  PASS
labctl validate       PASS
pytest                PASS
scanner YAML          0 duplicatas
```
