---
document_id: ENC-COMPLETENESS-PLAN
probe_status: PROBE_PROVED
---

# Plano de completeness

## Enunciado congelado

```lean
theorem analyzeEncodedSystem_complete (e) (stepS) (start : S) :
    ∃ w, analyzeEncodedSystem e stepS start = Except.ok w
```

**Sem pré-condições.** A frente anterior exigia `raw.Valid` e
`start < raw.next.size` do chamador; aqui as duas são consequências da
construção, e o consumidor não precisa provar nada.

## Prova congelada

```lean
  analyzeTransitionTable_complete _ _ (buildTransitionTable e stepS).toRaw_valid
    (by
      show ((e.encode start : Fin n) : Nat) < (buildTransitionTable e stepS).next.size
      rw [buildTransitionTable_size]
      exact (e.encode start).isLt)
```

Termo com uma obrigação lateral de três linhas. Compilou no probe.

## DAG obrigatório

```text
ValidatedTransitionTable.toRaw_valid       (frente anterior, uma linha)
    -> validade da tabela construida
buildTransitionTable_size
    -> encode start esta dentro dos limites, por Fin.isLt
        -> analyzeTransitionTable_complete
```

## O que NÃO é repetido

```text
pigeonhole;
exists_bounded_iterate_collision;
detector de ciclos;
completude do runtime adapter;
cycleCandidates.
```

Zero ocorrências planejadas. A completude vem inteira de
`analyzeTransitionTable_complete`, que por sua vez vem de
`detectCycle?_complete`. Três frentes de reutilização, nenhuma cópia.

## O witness permanece em `Prop`

```text
sem Classical.choose;
sem Option.get;
sem projecao computacional do existencial.
```

O existencial é consumido por `obtain` **dentro** das provas que
precisam dele, como no corolário de erro. Ele nunca vira dado.

## Corolário de erro

```lean
theorem analyzeEncodedSystem_ne_error (e) (stepS) (start : S) (err : RuntimeCycleError) :
    analyzeEncodedSystem e stepS start ≠ Except.error err
```

Quantificado sobre `err`, **um** teorema cobre os três construtores.
Compilou no probe.

```yaml
analyzeEncodedSystem_complete: PUBLIC_SPECIFICATION_CORE
analyzeEncodedSystem_ne_error: PUBLIC_COROLLARY
exclusoes individuais dos tres erros: DEFERRED_OPTIONAL
```

Três teoremas públicos onde um basta seria inflar a API. Os erros
**permanecem** no tipo executável.
