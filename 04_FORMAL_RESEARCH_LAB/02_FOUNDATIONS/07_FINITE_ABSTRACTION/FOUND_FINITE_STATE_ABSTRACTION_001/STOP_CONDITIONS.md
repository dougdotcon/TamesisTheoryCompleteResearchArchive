---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-STOP-CONDITIONS
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
stop_conditions_declared: 18
stop_conditions_triggered: 0
---

# Stop conditions

## As dezoito

```text
STOP-ABS-001  igualdade abstrata tratada como concreta
STOP-ABS-002  BOOL_TO_UNIT nao compila
STOP-ABS-003  Semiconj orientada incorretamente
STOP-ABS-004  soundness observacional termina em C
STOP-ABS-005  reflexao nao exige hipotese adicional
STOP-ABS-006  OrbitSeparating e tautologica
STOP-ABS-007  Fintype C exigida
STOP-ABS-008  DecidableEq C exigida
STOP-ABS-009  encoding anterior modificado
STOP-ABS-010  runtime adapter modificado
STOP-ABS-011  detector copiado
STOP-ABS-012  bissimulacao assumida
STOP-ABS-013  abstracao externa declarada correta
STOP-ABS-014  parser, CLI ou IO no nucleo
STOP-ABS-015  novidade inflada
STOP-ABS-016  probe obrigatorio com exit diferente de zero
STOP-ABS-017  identificadores concorrentes para o mesmo item
STOP-ABS-018  completeness abstrata descrita como completeness concreta
```

## As duas novas

`STOP-ABS-017` e `STOP-ABS-018` foram acrescentadas neste gate.

`STOP-ABS-017` responde a um risco **real e já materializado**: as
formas `FOUND-FINITE-ABSTRACTION-001` e
`FOUND-FINITE-STATE-ABSTRACTION-001` circularam ao mesmo tempo. Ver
[`IDENTIFIER_CANONICALIZATION_RECORD.md`](IDENTIFIER_CANONICALIZATION_RECORD.md).

`STOP-ABS-018` fecha a confusão mais provável da frente: a completeness
garante existência de witness **abstrato**, e alguém poderia lê-la como
garantia de recorrência concreta.

## Testadas por antecipação

```text
STOP-ABS-002  o contraexemplo compila
STOP-ABS-006  a condicao falha em BOOL_TO_UNIT, logo nao e tautologica
STOP-ABS-016  probe terminou com exit 0
STOP-ABS-017  identificador unificado neste gate
```

## Estado

```text
stop conditions declaradas   18
stop conditions disparadas    0
```
