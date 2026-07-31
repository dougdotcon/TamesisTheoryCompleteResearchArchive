---
document_id: FCD-COMPLETENESS-PLAN
pigeonhole_repeated: false
---

# Plano de completude

## Enunciado

```lean
theorem detectCycleWitness?_complete
    {X : Type*}
    [Fintype X]
    [DecidableEq X]
    (f : X → X)
    (x : X) :
    ∃ w : CycleWitness,
      detectCycleWitness? f x = some w
```

## Por que isto é um transporte, e não uma prova nova

Assinatura já verificada, lida do arquivo fonte:

```lean
theorem exists_bounded_iterate_collision {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧ 0 < lam ∧ mu + lam ≤ Fintype.card X ∧
        f^[mu + lam] x = f^[mu] x
```

Comparada ao predicado:

```lean
CycleWitness.Valid f x ⟨mu, lam⟩ :=
  mu < Fintype.card X ∧ 0 < lam ∧ mu + lam ≤ Fintype.card X ∧
    f^[mu + lam] x = f^[mu] x
```

São a **mesma conjunção**, na mesma ordem. O modelo de dados foi desenhado
para isso. A construção do `CycleWitness` a partir da colisão é literal.

## Fluxo obrigatório

```text
exists_bounded_iterate_collision
        |
obter mu e lam com as quatro propriedades
        |
construir CycleWitness <mu, lam>
        |
provar que pertence a cycleCandidates (card X)   [mem_cycleCandidates_iff]
        |
provar que o predicado executavel o aceita       [decide_eq_true_eq]
        |
concluir que find? nao retorna none              [List.find?_isSome]
```

## APIs da última etapa

```text
List.find?_isSome :
  (List.find? p xs).isSome = true <-> exists x in xs, p x = true

Option.isSome_iff_exists :
  x.isSome = true <-> exists a, x = some a
```

Ambas confirmadas no checkout. A composição das duas entrega exatamente o
`∃ w, detectCycleWitness? f x = some w` do enunciado.

`List.find?_eq_none` está disponível como rota alternativa por contradição
(`∀ x ∈ l, ¬ p x`), caso a rota por `isSome` produza atrito.

## Pigeonhole

```text
Fintype.exists_ne_map_eq_of_card_lt NAO sera usado nesta frente.
```

A casa dos pombos foi consumida **uma única vez**, dentro de
`exists_bounded_iterate_collision`, em `FOUND-SEMIGROUP-002`. Esta frente
a consome **através** daquele teorema. Repeti-la seria trabalho duplicado
e violaria a regra explícita do gate.

Verificação a exigir na formalização: nenhuma ocorrência de
`Fintype.exists_ne_map_eq_of_card_lt` nos arquivos desta frente.

## Nota sobre o tipo vazio

Se `card X = 0`, então `cycleCandidates 0 = []` e o detector devolveria
`none`. Isso **não** contradiz a completude: com `card X = 0` o tipo é
vazio e não existe `x : X` para passar ao teorema. O enunciado recebe
`x : X` explicitamente, exatamente como em `FOUND-FUNCTIONAL-GRAPH-001`.
Nenhuma hipótese `Nonempty X` é necessária.
