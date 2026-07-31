---
document_id: FFG-STOP-CONDITIONS
status: BINDING
---

# FOUND-FUNCTIONAL-GRAPH-001 — Condições de parada

Se qualquer condição ocorrer, **parar** e classificar como
`NEEDS_REFINEMENT`.

```yaml
- id: STOP-001
  condition: "componente definido como MutuallyReachable"
  detection: "componentSet ou o teorema principal usando MutuallyReachable"
  counterexample: FFG-CE-004

- id: STOP-002
  condition: "unicidade formulada como unico ponto periodico"
  detection: "∃! p, p ∈ periodicPts f  no enunciado"
  counterexample: FFG-CE-005

- id: STOP-003
  condition: "periodicPts usado sem periodo positivo"
  detection: "recorrencia definida como ∃ n, f^[n] x = x"
  note: "com n = 0 todo estado seria recorrente"

- id: STOP-004
  condition: "periodicOrbit substituida sem necessidade por estrutura local"
  detection: "structure Cycle ou def myOrbit no nucleo"

- id: STOP-005
  condition: "teorema principal repetir o pigeonhole"
  detection: "Fintype.exists_ne_map_eq_of_card_lt aparecer nesta frente"

- id: STOP-006
  condition: "SimpleGraph tornar-se dependencia obrigatoria do nucleo"
  detection: "import Mathlib.Combinatorics.SimpleGraph em modulo do nucleo"

- id: STOP-007
  condition: "distancia minima adicionada sem decidir computabilidade"
  detection: "Nat.find sobre pre-periodos, ou minimalidade de mu"

- id: STOP-008
  condition: "DecidableEq adicionada sem necessidade verificada"
  detection: "[DecidableEq X] numa assinatura do nucleo"
  note: "a auditoria mostrou que NAO eh necessaria; ver FFG-GAP-008"

- id: STOP-009
  condition: "componente tornar-se verdadeiro apenas por definicao tautologica"
  detection: >
    o teorema principal provado sem usar Fintype X, ou sem usar
    exists_eventual_period
  note: >
    Teste: se o enunciado continuasse verdadeiro para X infinito, algo esta
    errado. Para f : N -> N, f n = n + 1, ele eh FALSO.

- id: STOP-010
  condition: "resultado forte de arvores autorizado prematuramente"
  detection: "arvores de entrada, decomposicao canonica, unicidade de mu"

- id: STOP-011
  condition: "afirmacao de novidade matematica"

- id: STOP-012
  condition: "conexao com TRI, TDTR, TOE ou fisica"

- id: STOP-013
  condition: "instancia global de Setoid, Preorder ou equivalencia"
  note: "EventuallyMeets depende de f, que nao aparece no tipo X"

- id: STOP-014
  condition: "qualquer token proibido em Lean"
  detection: "sorry, admit, axiom, unsafe"
  action: "parar imediatamente; sem excecao"
```

## O que **não** é condição de parada

```text
Descobrir que um lema esperado nao existe.
  -> registrar em MATHLIB_API_AUDIT.md e escrever a versao local, se curta.

Descobrir que uma previsao da especificacao estava errada.
  -> corrigir e registrar. Ja aconteceu com FFG-GAP-008.

Um contraexemplo revelar que uma negativa esperada era falsa.
  -> corrigir ASSUMPTIONS.md; eh o mecanismo funcionando.
```
