---
document_id: ENC-COMPUTABILITY-BOUNDARY
verdict: COMPUTABLE
---

# Fronteira de computabilidade

## Exigido e confirmado

```text
CertifiedFiniteEncoding    dado executavel fornecido
encodedStep                computavel
buildTransitionTable       computavel
tableIndex                 computavel
analyzeEncodedSystem       computavel
```

Confirmado por `#eval` no probe, em sete modelos concretos, incluindo o
tipo vazio.

## Proibido no código executável

```text
noncomputable
Classical.choose
Classical.decEq
Trunc.out
Fintype.equivFin
Option.get
getD
fallback
modulo
clamp
```

Nenhum foi usado no probe. `STOP-ENC-001` e `STOP-ENC-006` cobrem
violações.

## Por que a codificação é fornecida

```text
Fintype.equivFin (a) [Fintype a] : a ≃ Fin (Fintype.card a)
declarado noncomputable em Mathlib/Data/Fintype/EquivFin.lean:80
axiomas [propext, Classical.choice, Quot.sound]
```

`Fintype.truncEquivFin` devolve `Trunc`, que só elimina para
`Subsingleton` — não produz dado utilizável. **A única rota computável é
receber `encode` e `decode` como campos.**

Essa decisão não é uma preferência de estilo: é o que separa uma tabela
que pode ser avaliada de uma tabela que só existe no papel.

## O que a computabilidade **não** é

```text
#eval NAO eh extracao.
```

```yaml
extraction_status: NOT_AUTHORIZED
cli_status: NOT_AUTHORIZED
parser_status: NOT_AUTHORIZED
integration_status: NOT_AUTHORIZED
```

Nenhum binário, alvo Lake, `main`, `IO`, arquivo, JSON, servidor ou API
externa. A computabilidade interna é **pré-condição** para uma futura
extração; ela não é extração, e não a autoriza.
