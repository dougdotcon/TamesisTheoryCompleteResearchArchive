---
document_id: FOUND-INVARIANT-UNREACHABILITY-001-STOP-CONDITIONS
work_item_id: FOUND-INVARIANT-UNREACHABILITY-001
stop_conditions_declared: 12
tested_by_anticipation: 12
triggered: 0
---

# Condições de parada

Todas testadas **por antecipação** no probe do gate de portfólio. Nenhuma
disparou.

| # | Condição | Testada |
|---|---|---|
| STOP-INV-001 | `Invariant` não ser definicionalmente `Semiconj ... id` | sim |
| STOP-INV-002 | A ferramenta afirmar necessidade, não suficiência | sim |
| STOP-INV-003 | `constant_invariant_proves_nothing` não compilar | sim |
| STOP-INV-004 | Alguma declaração exigir `Fintype C` ou `Fintype A` | sim |
| STOP-INV-005 | Alguma declaração exigir `DecidableEq` | sim |
| STOP-INV-006 | O teorema negativo exigir hipótese além de `Invariant` | sim |
| STOP-INV-007 | A instância usar tipo finito | sim |
| STOP-INV-008 | Abrir monovariante, boa ordem ou terminação | sim |
| STOP-INV-009 | Modificar arquivo de frente encerrada | sim |
| STOP-INV-010 | Afirmar reticulado, álgebra ou invariante completo | sim |
| STOP-INV-011 | Conectar a Clay, TOE, física ou Riemann | sim |
| STOP-INV-012 | `mathematical_novelty` ou `algorithmic_novelty` ≠ `NONE` | sim |

## As duas que exigiram cuidado real

**STOP-INV-002.** A leitura errada é sedutora: "invariante separa, logo
inalcançável" convida a ler "inalcançável, logo existe invariante que
separa". A recíproca é vacuamente verdadeira pelo invariante mais fino
— a própria relação de alcançabilidade — e portanto **não diz nada**.
`constant_invariant_proves_nothing` está na frente para que a assimetria
fique escrita em Lean, não só em prosa.

**STOP-INV-006.** O teorema negativo poderia degenerar se exigisse
finitude, decidibilidade ou hipótese sobre a órbita. Ele exige apenas
`Invariant`. Verificado no probe: a assinatura tem uma hipótese e um
`start`.

## Registro honesto

A frente é barata **porque** a observação central é uma igualdade
definicional. Barateza não é mérito e não é novidade: invariantes são
material clássico, e o que a frente faz é dar-lhes lugar no frame formal
que já existia.
