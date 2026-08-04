---
document_id: FOUND-MONOVARIANT-DESCENT-001-STOP-CONDITIONS
work_item_id: FOUND-MONOVARIANT-DESCENT-001
stop_conditions_declared: 11
tested_by_anticipation: 11
triggered: 0
---

# Condições de parada

Todas testadas por antecipação no probe. Nenhuma disparou.

| # | Condição | Testada |
|---|---|---|
| STOP-MON-001 | A medida usar ordem que não `Nat` | sim |
| STOP-MON-002 | Afirmar necessidade do monovariante | sim |
| STOP-MON-003 | Afirmar que boa fundação basta | sim |
| STOP-MON-004 | `0 < period` virar hipótese do consumidor | sim |
| STOP-MON-005 | A recuperação tocar arquivo de frente encerrada | sim |
| STOP-MON-006 | Reimplementar o detector ou a casa dos pombos | sim |
| STOP-MON-007 | Exigir `Fintype` ou `DecidableEq` | sim |
| STOP-MON-008 | Abrir terminação de programas ou ordinais | sim |
| STOP-MON-009 | Conectar a Clay, TOE, física ou Riemann | sim |
| STOP-MON-010 | Tentar remover pegada infraestrutural | sim |
| STOP-MON-011 | Novidade ≠ `NONE` | sim |

## STOP-MON-003, que é a armadilha real

`Nat` é bem fundado. Isso **não** faz de toda função `C → Nat` um
monovariante: `k - 1` é a função óbvia e falha em zero, onde a subtração
trunca. `strictDown_not_monovariant` existe para que essa distinção fique
escrita em Lean.

## STOP-MON-005 e STOP-MON-006, que andam juntas

A recuperação de `0 < period` reproduz, em namespace novo, uma redução
que a frente encerrada mantém privada. A linha é: **reproduzir uma
redução curta a partir de API pública é permitido; reimplementar o
detector não é.** A duplicação está declarada em
`SPECIFICATION_DECISION.md`.
