---
document_id: FCD-FINAL-DATA-MODEL
frozen: true
---

# Modelo de dados final — congelado

```lean
structure CycleWitness where
  baseIndex : ℕ
  period : ℕ
```

## Semântica

```text
baseIndex : indice-base da igualdade
            f^[baseIndex + period] x = f^[baseIndex] x

period    : periodo POSITIVO TESTEMUNHADO
```

`period` **pode ser múltiplo do período mínimo**. Toda documentação
pública desta frente repete essa frase, por decisão do gate de revisão.

## Nomes proibidos

```text
prefixIndex    superado pelo gate de revisao
entryIndex     proibido — sugere o ponto onde a cauda termina
tailLength     proibido — afirma minimalidade
cycleEntry     proibido — idem
minimalPeriod  proibido para o campo period — eh outro objeto da Mathlib
```

## Campos rejeitados

```text
entryPoint      derivavel por f^[baseIndex] x
lista do ciclo  diferida
isMinimal       minimalidade nao autorizada
provas          devem permanecer separadas do dado executavel
Fintype.card    pertence ao predicado, nao ao dado
a funcao f      idem
o estado x      idem
```

A estrutura é, portanto, **independente do tipo de estados**. Isso é
deliberado: `CycleWitness` é um par de naturais e pode ser comparado,
impresso e testado sem qualquer hipótese sobre `X`.

## Instâncias

```lean
deriving DecidableEq, Repr, BEq
```

Confirmadas úteis no probe: `Repr` para `#eval` legível, `DecidableEq` e
`BEq` para os testes de regressão. **Nenhuma outra instância** será
adicionada ao núcleo — em particular, nada de `Setoid`, `Ord`, `Hashable`
ou coerções.

## Predicado de validade — congelado

```lean
def CycleWitness.Valid
    {X : Type*}
    [Fintype X]
    (f : X → X)
    (x : X)
    (w : CycleWitness) : Prop :=
  w.baseIndex < Fintype.card X ∧
  0 < w.period ∧
  w.baseIndex + w.period ≤ Fintype.card X ∧
  f^[w.baseIndex + w.period] x =
    f^[w.baseIndex] x
```

Confirmado na revisão:

```text
Valid NAO exige DecidableEq X;
Valid coincide TERMO A TERMO com a conclusao de
  exists_bounded_iterate_collision;
Valid NAO afirma minimalidade.
```

Conferência contra o fonte, lido neste gate:

```lean
theorem exists_bounded_iterate_collision {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧ 0 < lam ∧ mu + lam ≤ Fintype.card X ∧
        f^[mu + lam] x = f^[mu] x
```

Mesma ordem, mesmas cotas, mesma igualdade.

## Instância de decidibilidade

O probe confirmou que a instância **não** é encontrada automaticamente a
partir de `Valid` — `Valid` é um `def`, e a resolução de instâncias não o
desdobra. Foi necessário declará-la:

```lean
instance CycleWitness.decidableValid {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) (w : CycleWitness) :
    Decidable (CycleWitness.Valid f x w) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))
```

Isso funcionou no probe. **A formalização deve declarar essa instância**;
sem ela, `decide (Valid f x w)` não elabora. Achado do gate de revisão,
ausente da especificação inicial.

## `ValidAt`

```yaml
ValidAt: DEFERRED
```

Não será mantido em paralelo a `Valid`. Ver `SPECIFICATION_REVIEW.md`
para a razão medida.
