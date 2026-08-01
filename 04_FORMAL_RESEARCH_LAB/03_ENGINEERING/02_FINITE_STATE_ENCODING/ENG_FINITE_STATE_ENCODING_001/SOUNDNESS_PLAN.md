---
document_id: ENC-SOUNDNESS-PLAN
probe_status: PROBE_PROVED
central_result: true
---

# Plano de soundness

## Enunciado congelado

```lean
theorem analyzeEncodedSystem_sound
    {e : CertifiedFiniteEncoding S n} {stepS : S → S} {start : S} {w : CycleWitness}
    (h : analyzeEncodedSystem e stepS start = Except.ok w) :
    stepS^[w.baseIndex + w.period] start = stepS^[w.baseIndex] start
```

**A igualdade é em `S`.** Não sobre `Nat`, não sobre `Fin n`, não sobre a
tabela. Este é o resultado semântico central da frente, e `STOP-ENC-018`
existe exatamente para impedir que ele degenere num enunciado sobre a
tabela.

## Prova congelada

```lean
  have hrun := (analyzeTransitionTable_sound h).2.2
  rw [run?_corresponds_to_typed_iterate, run?_corresponds_to_typed_iterate] at hrun
  exact e.encode_injective (Fin.ext (Option.some.inj hrun))
```

Três linhas. Compilou no probe, na primeira tentativa.

## DAG obrigatório

```text
analyzeTransitionTable_sound                    (frente anterior)
    -> a terceira conjuncao: igualdade entre run? sobre a tabela
        -> run?_corresponds_to_typed_iterate, lado esquerdo
        -> run?_corresponds_to_typed_iterate, lado direito
            -> Option.some.inj
                -> Fin.ext
                    -> CertifiedFiniteEncoding.encode_injective
                        -> igualdade no tipo S
```

Cada seta é um passo de prova real, e nenhuma delas é uma hipótese
adicional imposta ao consumidor: a assinatura tem **apenas** `h`.

## Por que não há transporte dependente

`analyzeTransitionTable_sound` fala de `raw.run?`, e
`run?_corresponds_to_typed_iterate` está enunciado sobre
`(buildTransitionTable e stepS).toRaw.run?` — a mesma expressão,
sintaticamente. A reescrita casa sem `cast`, sem `Eq.ndrec`, sem `heq`.

É a mesma técnica que a frente anterior usou ao escolher a tabela
concreta `⟨raw.next, hRaw⟩`: **fazer o objeto do enunciado ser
sintaticamente o objeto da prova.**

## O que a soundness NÃO afirma

```text
baseIndex minimo;
period minimo;
entrada canonica;
minimalPeriod;
unicidade do witness;
enumeracao do componente;
independencia da ordem de busca.
```

O witness é *um* certificado de repetição, não *o* certificado. Mesma
fronteira das duas frentes anteriores, preservada literalmente.
