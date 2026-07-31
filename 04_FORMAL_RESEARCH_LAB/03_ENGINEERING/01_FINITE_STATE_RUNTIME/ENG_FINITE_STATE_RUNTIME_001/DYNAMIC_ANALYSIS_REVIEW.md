---
document_id: RT-DYNAMIC-ANALYSIS-REVIEW
soundness_audited: true
completeness_audited: true
---

# Revisão da análise dinâmica

## Fluxo confirmado

```text
validateTransitionTable
    -> validateStart
    -> detectCycle?
    -> ok witness  ou  internalDetectorFailure
```

Ausentes: certificado padrão, `Option.getD`, `Classical.choose`, `panic`,
fallback. **A função não totaliza o detector anterior** —
`FOUND-CYCLE-DETECTION-001.totalization_status` permanece `DEFERRED`.

## Soundness — auditada integralmente

```lean
theorem analyzeTransitionTable_sound
    (h : analyzeTransitionTable raw start = .ok w) :
    raw.Valid ∧ start < raw.next.size ∧
    raw.run? (w.baseIndex + w.period) start = raw.run? w.baseIndex start
```

| Exigência | Verificado |
|---|---|
| nenhum `cast` | zero |
| nenhum `Eq.ndrec` explícito | zero |
| nenhum transporte dependente manual | zero |
| nenhuma hipótese adicional do consumidor | a assinatura só tem `h` |
| nenhum enfraquecimento para tabela intermediária | a terceira conjunção é sobre `raw`, não sobre `validated.toRaw` |

**Por que não houve transporte.** A tabela concreta usada é
`⟨raw.next, hRaw⟩`, cujo campo `next` é **sintaticamente** `raw.next`.
Logo `Fin validated.next.size` e `Fin raw.next.size` são o mesmo tipo, e
`(⟨raw.next, hRaw⟩).toRaw` é definicionalmente `raw` por eta de
estruturas. O problema que a especificação temia simplesmente não
ocorre — porque o desenho o evitou.

## O auxiliar privado

```yaml
declaration: analyze_reduce
category: INTERNAL_HELPER
visibility: private
role: >
  encapsula as duas reducoes que a notacao do esconde, devolvendo a
  analise na forma de um match sobre detectCycle?
adds_mathematical_hypothesis: false
```

Auditado: ele **não** adiciona hipótese matemática. Suas duas hipóteses,
`hRaw` e `hStart`, são exatamente as que os dois validadores consomem, e
o enunciado é uma **igualdade de definições** — nenhuma afirmação nova.

É usado por `analyzeTransitionTable_sound` e por
`analyzeTransitionTable_complete`, e é a razão de a primeira ter sete
linhas e a segunda, quatro.

## Completeness — auditada

```lean
theorem analyzeTransitionTable_complete (hRaw : raw.Valid)
    (hStart : start < raw.next.size) :
    ∃ w, analyzeTransitionTable raw start = .ok w := by
  obtain ⟨w, hw⟩ := ValidatedTransitionTable.detectCycle?_complete ⟨raw.next, hRaw⟩ ⟨start, hStart⟩
  refine ⟨w, ?_⟩
  rw [analyze_reduce hRaw hStart, hw]
```

| Exigência | Verificado |
|---|---|
| o witness vem de `detectCycle?_complete` | sim, por `obtain` |
| sem `Classical.choose` | zero |
| sem `Option.get` | zero |
| sem projeção computacional do existencial | o `obtain` ocorre **dentro da prova**, em nível `Prop` |
| sem repetição da colisão limitada | `exists_bounded_iterate_collision`: zero ocorrências |

### O que a completeness **não** afirma

```text
qual witness;
minimalidade;
unicidade;
resultado independente da ordem;
ausencia do construtor internalDetectorFailure na funcao.
```

O último merece ênfase: a completude prova que o ramo `none` **não
ocorre**; ela não o remove do código, e nada nesta frente o remove.
