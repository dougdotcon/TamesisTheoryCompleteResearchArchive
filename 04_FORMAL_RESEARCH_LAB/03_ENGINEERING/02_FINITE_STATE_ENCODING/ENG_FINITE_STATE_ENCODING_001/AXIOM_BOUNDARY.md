---
document_id: ENC-AXIOM-BOUNDARY
---

# Fronteira axiomática

## Medido no probe

```text
buildTransitionTable                  [propext, Classical.choice, Quot.sound]
buildTransitionTable_size             [propext, Classical.choice, Quot.sound]
buildTransitionTable_getElem          [propext, Classical.choice, Quot.sound]
tableIndex                            [propext, Classical.choice, Quot.sound]
tableIndex_val                        [propext, Classical.choice, Quot.sound]
table_step_commutes                   [propext, Classical.choice, Quot.sound]
tableIndex_semiconj                   [propext, Classical.choice, Quot.sound]
table_iterate_commutes                [propext, Classical.choice, Quot.sound]
run?_corresponds_to_typed_iterate     [propext, Classical.choice, Quot.sound]
analyzeEncodedSystem                  [propext, Classical.choice, Quot.sound]
analyzeEncodedSystem_sound            [propext, Classical.choice, Quot.sound]
analyzeEncodedSystem_complete         [propext, Classical.choice, Quot.sound]
analyzeEncodedSystem_ne_error         [propext, Classical.choice, Quot.sound]
```

Uniforme. Nenhum `sorryAx`, nenhum axioma local.

## De onde vem `Classical.choice`

Duas origens, ambas herdadas e ambas em posição de **prova**:

```text
Array.getElem_ofFn        [propext, Classical.choice, Quot.sound]
Fintype.card, via o detector, exatamente como na frente anterior
```

A primeira entra já em `buildTransitionTable`, porque o campo `closed` —
que é `Prop` e é apagado na execução — usa `getElem_ofFn`. Por isso a
pegada aparece uniforme desde a construção, e não apenas onde o detector
entra.

## A regra do laboratório, reafirmada pela quarta vez

```text
a presenca infraestrutural de propext, Classical.choice e Quot.sound
nao bloqueia a especificacao se:

  nenhuma definicao for noncomputable;
  #eval funcionar;
  nenhum Classical.choose produzir dado.
```

Os três critérios foram verificados por execução, não por leitura:
nenhuma definição marcada, `#eval` produziu `#[1,0]`, `#[1,2,3,2]`,
`#[1,0,1,2]`, `#[]` e os witnesses de sete modelos, e nenhuma escolha
clássica aparece nos corpos executáveis.

## Comparação honesta

Na frente anterior, `step?` e `run?` **não dependiam de axioma nenhum**,
e a camada de validação ficava em `[propext, Quot.sound]`. Aqui a pegada
é mais pesada desde o início, e a causa é única: `Array.getElem_ofFn`.
Não é uma degradação da qualidade da prova; é o custo de trocar uma
verificação de limites por uma construção indexada.


---

## Revisão — `2066edc`

**Superado** por `AXIOM_FOOTPRINT_REVIEW.md`.

Correção material: este documento afirmava pegada uniforme nas treze
declarações. A revisão mediu que `encode_injective`, `encode_surjective`
e `encodedStep` **não dependem de axioma nenhum**, e que a primeira
declaração a carregar `[propext, Classical.choice, Quot.sound]` é
`buildTransitionTable`, pelo campo `closed` via `Array.getElem_ofFn`.

Decisão: `ACCEPT_INFRASTRUCTURAL_AXIOM_FOOTPRINT`.
