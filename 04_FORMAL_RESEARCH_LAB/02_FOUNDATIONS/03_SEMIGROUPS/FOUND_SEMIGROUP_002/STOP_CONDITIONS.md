---
document_id: FSG2-STOP-CONDITIONS
status: BINDING
---

# FOUND-SEMIGROUP-002 — Condições de parada

Se qualquer condição abaixo ocorrer durante a execução, **parar** e
reclassificar como `NEEDS_REFINEMENT`.

```yaml
- id: STOP-001
  condition: >
    A especificacao ou a formalizacao confundir acao completa do monoide
    com iteracao de um elemento fixo.
  detection: >
    Um teorema da Camada C carregar hipotese [Monoid M]; ou um enunciado
    sobre Reachable ser provado por inducao em potencias de um unico a.

- id: STOP-002
  condition: "O teorema exigir que alcancabilidade seja simetrica."
  detection: "Aparecer Reachable y x como hipotese ou passo de prova."
  counterexample: CE-001

- id: STOP-003
  condition: "A prova depender de qualquer claim Tamesis."
  detection: >
    Mencao a TRI, TDTR, Omega, TOE, massa critica, Braid, ou a qualquer
    documento legado nao auditado como premissa.

- id: STOP-004
  condition: "Os limitantes de cardinalidade estiverem incorretos."
  detection: >
    mu >= Fintype.card X, ou mu + lam > Fintype.card X, ou lam = 0.
    Verificar contra a analise de THEOREM_CANDIDATES.md, que derivou
    i < j <= card X a partir de Fin (card X + 1).

- id: STOP-005
  condition: >
    A API Mathlib necessaria nao for localizada E a alternativa local ficar
    excessivamente grande.
  threshold: >
    Se a definicao local de periodicidade eventual exigir mais de ~40 linhas
    ou teoria auxiliar nova, parar e reavaliar o alvo.

- id: STOP-006
  condition: "A primeira execucao tentar incluir decomposicao unica de orbitas."
  detection: >
    Aparecer minimalidade de mu ou lam, Nat.find sobre pre-periodos, ou
    unicidade do par (mu, lam).
  rationale: "Excluido da meta C por analise de custo; ver FSG2-GAP-004b."

- id: STOP-007
  condition: >
    O escopo comecar a incluir probabilidade, fisica, caos continuo, PDE ou
    sistemas infinitos.
  detection: >
    Remocao da hipotese Fintype X; aparecimento de medida, topologia,
    espaco metrico, ou tempo continuo.

- id: STOP-008
  condition: "A especificacao transformar um exemplo em lei universal."
  detection: >
    Uma propriedade de C3 (fidelidade, transitividade, ausencia de cauda)
    ser enunciada sem hipotese explicita.
  counterexamples: [CE-001, CE-002, CE-003, CE-004]
```

## Condições adicionais deste laboratório

```yaml
- id: STOP-009
  condition: "Uso de minimalPeriod como se fosse periodo eventual."
  detection: >
    Function.minimalPeriod ou MulAction.period aparecer no enunciado do
    alvo. Ambos devolvem 0 fora de periodicPts.
  counterexample: CE-003
  gap: FSG2-GAP-002b

- id: STOP-010
  condition: "Criacao de uma instancia global Preorder X para alcancabilidade."
  rationale: >
    A relacao depende de M, que nao aparece no tipo X. Duas acoes sobre o
    mesmo X dariam instancias incompativeis.
  gap: FSG2-GAP-006

- id: STOP-011
  condition: "Manutencao de hipotese matematicamente ociosa."
  detection: >
    [DecidableEq X] ou [Fintype M] permanecerem numa assinatura sem serem
    usados na prova.
  gap: FSG2-GAP-004c
  precedent: >
    Politica ja aplicada em COUNTING-LAW-BRIDGE, onde 0 < c foi removida
    do teorema tecnico.

- id: STOP-012
  condition: "Qualquer token proibido em Lean."
  detection: "sorry, admit, axiom, unsafe"
  action: "parar imediatamente; nao ha excecao"
```

## O que **não** é condição de parada

```text
Descobrir que um lema esperado nao existe na Mathlib.
  -> registrar em LEAN_FEASIBILITY.md e escrever a versao local, se curta.

Descobrir que um limitante eh mais fraco do que o previsto.
  -> enfraquecer o enunciado e registrar, em vez de forcar o limitante.

Um contraexemplo revelar que uma negativa esperada era falsa.
  -> corrigir ASSUMPTIONS.md; isso eh o mecanismo funcionando.
```
