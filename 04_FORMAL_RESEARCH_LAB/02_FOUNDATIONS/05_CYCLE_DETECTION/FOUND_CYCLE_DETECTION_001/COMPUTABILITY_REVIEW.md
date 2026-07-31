---
document_id: FCD-COMPUTABILITY-REVIEW
verdict: COMPUTABLE
---

# Revisão de computabilidade

## Classificação congelada

```text
CycleWitness         computavel
cycleCandidates      computavel
CycleWitness.Valid   proposicional, DECIDIVEL com DecidableEq X
detectCycleWitness?  computavel
```

Separadamente, e sem confusão possível:

```text
Function.periodicOrbit  noncomputavel e proposicional
Function.periodicPts    interface proposicional (Set X)
EventuallyMeets         proposicional
IterReachable           proposicional
```

**`periodicPts` não foi transformada em detector executável.** O detector
devolve um par de naturais; a pertinência a `periodicPts` é um teorema
sobre esse par, não um cálculo.

## Evidência de execução

Cinco modelos avaliados com `#eval` no probe descartável:

```text
Fin 1, id                      some <0,1>
Bool, id                       some <0,1>   (nos dois estados)
Bool, not                      some <0,2>   (nos dois estados)
Fin 3, 0->1->2->2, de 0        some <2,1>
Fin 4, 0->1->2->3->2, de 0     some <2,2>
```

Nenhuma definição precisou de `noncomputable`. Nenhuma usou
`Classical.choose`.

## O achado sobre a pegada axiomática

```text
#print axioms cycleCandidates      does not depend on any axioms
#print axioms detectCycleWitness?  [propext, Classical.choice, Quot.sound]
```

Localização da origem, com um segundo probe:

| Constante | Pegada |
|---|---|
| `List.range` | nenhuma |
| `List.flatMap` | nenhuma |
| `List.find?` | nenhuma |
| `Nat.iterate` | nenhuma |
| `cycleCandidates` | **nenhuma** |
| `Fintype.card` | `[propext, Classical.choice, Quot.sound]` |
| `Finset.univ` | `[propext, Classical.choice, Quot.sound]` |
| `detectCycleWitness?` | `[propext, Classical.choice, Quot.sound]` |

Uma variante `detectAt? (n : ℕ)` que **recebe** a cota, em vez de
calculá-la, não depende de axioma algum — e avalia normalmente.

## A leitura correta

```text
Pegada axiomatica NAO eh o mesmo que noncomputabilidade.
```

`Fintype.card` é computável — `#eval Fintype.card (Fin 3)` devolve `3` —
e mesmo assim carrega `Classical.choice`, porque a infraestrutura de
`Finset` da Mathlib usa escolha dentro de **provas**, que são apagadas na
compilação.

Portanto, o critério "sem `Classical.choice`" do gate deve ser lido como:

```text
1. a definicao nao eh marcada noncomputable;
2. #eval funciona em exemplos concretos;
3. nenhum Classical.choose produz DADO.
```

Os três estão confirmados. Exigir pegada axiomática vazia seria
inatingível para qualquer definição que use `Fintype.card` — isto é, para
qualquer detector com cota derivada da cardinalidade.

## Consequência para `ValidAt`

A tentação seria adotar `ValidAt n` para conservar o núcleo sem axiomas.
Não resolve: `detectCycleWitness?` precisa **calcular** `Fintype.card X`
para saber onde parar, de modo que a pegada volta pela porta da frente.

```yaml
ValidAt: DEFERRED
```

## Instância de decidibilidade

Achado do probe: a instância `Decidable (CycleWitness.Valid f x w)`
**não** é encontrada automaticamente, porque `Valid` é um `def` e a
resolução de instâncias não o desdobra. É preciso declará-la
explicitamente com `inferInstanceAs`. Isso funcionou.

**A formalização deve incluir essa instância.** Sem ela,
`decide (Valid f x w)` não elabora, e o detector nem sequer compila.
