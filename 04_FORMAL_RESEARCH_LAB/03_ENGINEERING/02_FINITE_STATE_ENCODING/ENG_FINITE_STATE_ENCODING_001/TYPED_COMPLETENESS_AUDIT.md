---
document_id: ENC-TYPED-COMPLETENESS-AUDIT
preconditions: 0
---

# Auditoria da completeness tipada

## Enunciado implementado

```lean
theorem analyzeEncodedSystem_complete (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (start : S) :
    ∃ witness, analyzeEncodedSystem encoding stepS start = .ok witness
```

**Zero pré-condições.** A frente anterior exigia do chamador
`raw.Valid` e `start < raw.next.size`; aqui as duas são consequências da
construção.

## Prova implementada

```lean
  have hStart : ((encoding.encode start : Fin n) : Nat)
      < (buildTransitionTable encoding stepS).next.size := by
    rw [buildTransitionTable_size]
    exact (encoding.encode start).isLt
  exact analyzeTransitionTable_complete _ _
    (buildTransitionTable encoding stepS).toRaw_valid hStart
```

Cinco linhas.

### Nota de implementação

A especificação recomendava `simpa using (encoding.tableIndex stepS start).isLt`.
Ela funciona, mas o linter de Lean apontou o `using` como desnecessário —
`buildTransitionTable_size` e `tableIndex_val` são ambos `@[simp]`, de
modo que `simp` sozinho fecharia o objetivo. Trocamos pela rota explícita
`rw` + `exact`, que não depende do conjunto `simp` e não emite aviso.

## DAG

```text
buildTransitionTable.toRaw_valid            (frente anterior, 1 linha)
  -> validade estrutural da tabela construida
buildTransitionTable_size
  -> Fin.isLt de encode start
      -> hStart
          -> analyzeTransitionTable_complete
```

## Ausências verificadas por busca

```text
pigeonhole                          0
exists_bounded_iterate_collision    0
exists_ne_map_eq_of_card_lt         0
cycleCandidates                     0
detectCycleWitness?                 0
Classical.choose                    0
```

A reutilização é **indireta**, encapsulada no runtime adapter. O witness
permanece existencial em `Prop`: o `obtain` só ocorre dentro da prova do
corolário de erro, e nunca produz dado.

## Teste imediato

```text
lake env lean TamesisLab/Engineering/FiniteStateEncoding/DynamicAnalysis.lean
exit 0
```

`ENG_FINITE_STATE_ENCODING_001_TYPED_COMPLETENESS_FAILED` não disparou.

## Exclusão universal de erros

```lean
theorem analyzeEncodedSystem_ne_error (encoding) (stepS) (start) (err) :
    analyzeEncodedSystem encoding stepS start ≠ .error err := by
  intro hError
  obtain ⟨witness, hOk⟩ := analyzeEncodedSystem_complete encoding stepS start
  rw [hOk] at hError
  cases hError
```

**Um** corolário público, quantificado sobre `err`. As três exclusões
específicas permanecem `DEFERRED_OPTIONAL`, e os construtores continuam
no tipo executável — a impossibilidade é teorema, não motivo de remoção.

Instanciado nos testes para dois erros concretos e na forma universal.
