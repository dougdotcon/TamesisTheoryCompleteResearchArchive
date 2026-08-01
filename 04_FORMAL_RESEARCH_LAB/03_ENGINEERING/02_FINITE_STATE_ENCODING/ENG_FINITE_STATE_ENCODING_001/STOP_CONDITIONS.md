---
document_id: ENC-STOP-CONDITIONS
count: 18
triggered: 0
---

# Stop conditions

```text
STOP-ENC-001  codificacao usa fallback silencioso
STOP-ENC-002  encode/decode sem leis inversas suficientes
STOP-ENC-003  Array sem tamanho demonstravel
STOP-ENC-004  validade da tabela nao demonstravel
STOP-ENC-005  casts nao controlados
STOP-ENC-006  escolha classica produz dado executavel
STOP-ENC-007  detector anterior copiado
STOP-ENC-008  runtime adapter modificado
STOP-ENC-009  parser, CLI ou IO entra no nucleo
STOP-ENC-010  equivalencia assumida, nao fornecida
STOP-ENC-011  sistema externo declarado correto
STOP-ENC-012  novidade inflada
STOP-ENC-013  frente duplica item existente
STOP-ENC-014  PoC nao cabe em 30 dias
STOP-ENC-015  DecidableEq S exigida sem necessidade
STOP-ENC-016  Fintype S exigida sem necessidade
STOP-ENC-017  n > 0 adicionado a estrutura sem necessidade
STOP-ENC-018  soundness fala apenas da tabela, nao do sistema tipado
```

## Estado neste gate

```text
disparadas: 0
```

As quatro mais próximas de disparar, e por que não dispararam:

- **`STOP-ENC-005`** era o risco central declarado pelo portfólio. Não
  disparou: existem **exatamente dois** pontos de transporte, ambos
  auditados, e o probe compilou. Se a formalização precisar de um
  terceiro, a frente para.
- **`STOP-ENC-006`** era o risco identificado na auditoria de
  `Fintype.equivFin`. Não disparou porque a codificação é campo, não
  derivação. É a condição que mais restringe o desenho.
- **`STOP-ENC-018`** é o critério de sucesso da frente inteira. Não
  disparou: a soundness termina em `stepS^[b+p] start = stepS^[b] start`,
  igualdade em `S`.
- **`STOP-ENC-015`** e **`STOP-ENC-016`** não dispararam: nenhuma
  typeclass aparece em nenhuma das dezesseis declarações.

## Se qualquer uma ocorrer

```text
ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_BLOCKED
e parar.
```


---

## Revisão — `2066edc`

Acrescentada:

```text
STOP-ENC-019  witness concreto declarado invariavel sob recodificacao
              sem prova
```

Total: **19** stop conditions, **zero** disparadas na revisão.
