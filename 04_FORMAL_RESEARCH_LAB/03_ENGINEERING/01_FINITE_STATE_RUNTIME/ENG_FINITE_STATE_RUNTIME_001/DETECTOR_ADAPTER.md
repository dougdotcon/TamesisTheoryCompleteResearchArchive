---
document_id: RT-DETECTOR-ADAPTER
frozen: true
---

# Adaptador do detector

```lean
def ValidatedTransitionTable.detectCycle? (t : ValidatedTransitionTable)
    (start : Fin t.next.size) : Option CycleWitness :=
  detectCycleWitness? t.step start
```

Uma linha. **O corpo de `detectCycleWitness?` não é copiado.**

As instâncias `Fintype (Fin n)` e `DecidableEq (Fin n)` são inferidas —
o chamador não fornece nenhuma.

## Herança direta

```lean
theorem ValidatedTransitionTable.detectCycle?_sound
    {t : ValidatedTransitionTable} {start : Fin t.next.size}
    {w : CycleWitness} (h : t.detectCycle? start = some w) :
    CycleWitness.Valid t.step start w

theorem ValidatedTransitionTable.detectCycle?_complete
    (t : ValidatedTransitionTable) (start : Fin t.next.size) :
    ∃ w, t.detectCycle? start = some w
```

Ambos por **reutilização direta** de `detectCycleWitness?_sound` e
`detectCycleWitness?_complete`. Como `detectCycle?` é definicionalmente a
aplicação do detector, as provas devem ser aplicações imediatas, no
espírito das três pontes de `Periodicity.lean`.

```text
NAO repetir a enumeracao;
NAO repetir o pigeonhole.
```

A casa dos pombos permanece consumida **uma única vez**, em
`FOUND-SEMIGROUP-002`, através de `exists_bounded_iterate_collision`, que
o detector já consome.

## Interpretação do witness na tabela bruta

```lean
theorem ValidatedTransitionTable.detectCycle?_raw_repeat
    {t : ValidatedTransitionTable} {start : Fin t.next.size}
    {w : CycleWitness} (h : t.detectCycle? start = some w) :
    t.toRaw.run? (w.baseIndex + w.period) (start : Nat) =
      t.toRaw.run? w.baseIndex (start : Nat)
```

### Prova futura

```text
1. obter CycleWitness.Valid para t.step, por detectCycle?_sound;
2. extrair a igualdade entre as duas iteradas — a quarta clausula;
3. usar run?_eq_iterate_step nos DOIS lados;
4. reescrever pela igualdade certificada.
```

Este é o teorema que fecha o ciclo da frente: um certificado obtido sobre
`Fin n` volta a ser uma afirmação sobre **a tabela que o usuário
entregou**.

```text
NAO afirmar que baseIndex ou period sao minimos.
```

O que se afirma é que executar `baseIndex + period` passos e executar
`baseIndex` passos levam ao **mesmo estado** — nada mais.
