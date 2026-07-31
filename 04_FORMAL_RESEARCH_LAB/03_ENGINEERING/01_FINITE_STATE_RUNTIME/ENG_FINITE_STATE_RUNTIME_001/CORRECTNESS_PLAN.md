---
document_id: RT-CORRECTNESS-PLAN
---

# Plano de correção

## Validação da tabela

```lean
theorem validateTransitionTable_sound
    {raw : RawTransitionTable} {validated : ValidatedTransitionTable}
    (h : validateTransitionTable raw = .ok validated) :
    validated.toRaw = raw ∧ raw.Valid
```

Rota: `validateTransitionTable` é um `dite`. No ramo `.ok`, a hipótese
`h` só é habitável quando a condição vale, e o valor devolvido é
`⟨raw.next, _⟩`. A conjunção sai por `split` sobre o `dite` e `injection`
sobre a igualdade de `Except`.

A orientação da igualdade — `validated.toRaw = raw` ou o inverso — poderá
ser trocada conforme simplifique a prova. Ambas são equivalentes por
`Eq.symm`, e a escolha é de conveniência.

## Validação do início

```lean
theorem validateStart_sound
    {t : ValidatedTransitionTable} {start : Nat} {s : Fin t.next.size}
    (h : validateStart t start = .ok s) :
    (s : Nat) = start
```

Mesma rota, e é **o teorema anti-clamp**: ele torna impossível que uma
implementação futura ajuste o índice sem quebrar a prova.

## Detector adaptado

```lean
theorem ValidatedTransitionTable.detectCycle?_sound
    (h : t.detectCycle? start = some w) :
    CycleWitness.Valid t.step start w
```

Aplicação direta de `detectCycleWitness?_sound`. `detectCycle?` é
definicionalmente o detector aplicado a `t.step`, de modo que `h` já tem
o tipo esperado — no espírito das três pontes de uma linha de
`Periodicity.lean`.

## Interpretação bruta

```lean
theorem ValidatedTransitionTable.detectCycle?_raw_repeat
    (h : t.detectCycle? start = some w) :
    t.toRaw.run? (w.baseIndex + w.period) (start : Nat) =
      t.toRaw.run? w.baseIndex (start : Nat)
```

Quatro passos, já registrados em `DETECTOR_ADAPTER.md`. O único
ingrediente novo é `run?_eq_iterate_step`, aplicado dos dois lados.

## API dinâmica

```lean
theorem analyzeTransitionTable_sound
    {raw : RawTransitionTable} {start : Nat} {w : CycleWitness}
    (h : analyzeTransitionTable raw start = .ok w) :
    raw.Valid ∧
    start < raw.next.size ∧
    raw.run? (w.baseIndex + w.period) start = raw.run? w.baseIndex start
```

Rota: desmontar o `do` — cada `←` só prossegue no ramo `.ok`, de modo que
`h` fornece simultaneamente as duas validações e a igualdade do detector.
As três conjunções saem, respectivamente, de
`validateTransitionTable_sound`, `validateStart_sound` e
`detectCycle?_raw_repeat`.

Nota sobre a terceira conjunção: ela é enunciada sobre `raw`, não sobre
`validated.toRaw`. A identificação vem da primeira conjunção — e é por
isso que `validateTransitionTable_sound` precisa devolver a igualdade das
tabelas, e não apenas a validade.

```text
NAO incluir minimalidade.
```

## Erros esperados

```lean
theorem analyzeTransitionTable_invalid_table (h : ¬raw.Valid) :
    analyzeTransitionTable raw start = .error .transitionDestinationOutOfBounds

theorem analyzeTransitionTable_invalid_start
    (hRaw : raw.Valid) (hStart : ¬start < raw.next.size) :
    analyzeTransitionTable raw start =
      .error (.initialStateOutOfBounds start raw.next.size)
```

Ambos por redução do `dite` sob a hipótese negativa. O segundo exige a
positiva da tabela para que o `do` chegue ao segundo passo.

Estes dois teoremas são o que impede `internalDetectorFailure` de
mascarar erro de validação: eles fixam **qual** erro sai em cada caso.
