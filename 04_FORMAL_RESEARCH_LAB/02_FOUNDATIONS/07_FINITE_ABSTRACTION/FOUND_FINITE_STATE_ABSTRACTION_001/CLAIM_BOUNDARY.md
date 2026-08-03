---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-CLAIM-BOUNDARY
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
claim_candidate: CERTIFIED-FINITE-STATE-ABSTRACTION-FORMAL-001
claims_promoted_in_this_gate: 0
---

# Fronteira da claim

## Nenhuma claim é promovida na especificação

```text
claims promovidas neste gate   0
ledger permanece               22 claims
```

A promoção só pode ocorrer depois da formalização permanente e da sua
validação, em gate próprio, e no máximo **uma**.

## Claim candidata

```yaml
claim_id: CERTIFIED-FINITE-STATE-ABSTRACTION-FORMAL-001
domain: formal_semantics
work_status: VERIFIED
evidence_level: F
mathematical_novelty: NONE
algorithmic_novelty: NONE
```

## Wording permitida

```text
Foi formalizada em Lean uma abstração determinística
semiconjugada entre um sistema concreto e um sistema abstrato
finito certificadamente codificado.

Foi provado que um witness abstrato implica recorrência
observacional no sistema concreto.

Sob uma hipótese explícita de separação da órbita, essa
recorrência observacional pode ser refletida como recorrência
concreta.

Também foi formalizado um contraexemplo mostrando que a
semiconjugação isoladamente não reflete ciclos.
```

## Wording proibida

```text
todo ciclo abstrato e concreto;
abstracoes finitas sao sempre corretas;
bissimulacao foi provada;
sistemas externos foram certificados;
algoritmo novo;
novidade matematica;
complexidade otima;
integracao pronta.
```

## Evidência exigida antes da promoção

```text
lake build            exit 0
testes formais        PASS
testes executaveis    PASS
auditoria de axiomas  PASS
labctl validate       PASS
pytest                PASS
scanner YAML          0 duplicatas
```
