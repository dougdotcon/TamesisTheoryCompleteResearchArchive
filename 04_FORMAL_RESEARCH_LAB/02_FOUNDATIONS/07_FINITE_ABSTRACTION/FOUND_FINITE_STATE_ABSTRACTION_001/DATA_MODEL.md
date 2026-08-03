---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-DATA-MODEL
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
---

# Modelo de dados

## A estrutura

```lean
structure CertifiedFiniteAbstraction
    (C A : Type*)
    (stepC : C → C)
    (stepA : A → A) where
  abstract : C → A
  commutes :
    Function.Semiconj abstract stepC stepA
```

Um campo de dado, uma lei. `stepC` e `stepA` são **parâmetros** da
estrutura, não campos: eles pertencem aos sistemas, não à abstração.

## O que a estrutura deliberadamente NÃO armazena

| Rejeitado | Por quê |
|---|---|
| `CertifiedFiniteEncoding A n` | fundiria abstração muitos-para-um com codificação exata |
| estado inicial | a abstração não conhece de onde a análise parte |
| `CycleWitness` | resultado de execução, não dado da abstração |
| resultado da análise | idem |
| `Array` / tabela | a tabela pertence à frente de codificação |
| prova de `OrbitSeparating` | é obrigação do consumidor, por órbita |
| concretização `A → C` | exigiria uma teoria que a frente não tem |

## O significado de "Certified"

```text
"Certified" significa que a comutação entre stepC, abstract e
stepA é fornecida como prova formal.

Não significa que um sistema externo real foi corretamente
traduzido para C.

Não significa que abstract seja injetiva.

Não significa que recorrências abstratas sejam concretas.
```

O adjetivo qualifica **um campo da estrutura**, e nada além dele. Ver
[`RESULT_BOUNDARY.md`](RESULT_BOUNDARY.md).

## Separação em relação à codificação

```text
abstracao          C → A     possivelmente muitos-para-um
codificacao        A ≃ Fin n exata, com duas leis
```

`CertifiedFiniteEncoding A n` entra como argumento de
`analyzeAbstractSystem`, nunca como campo. É essa separação que torna a
fronteira observacional visível: a perda de informação vive em
`abstract`, e a codificação não perde nada.

## Typeclasses

```text
sobre C   nenhuma
sobre A   nenhuma
```

Verificado por compilação: o probe declara `C A : Type*` sem instância
alguma e a cadeia central inteira elabora.
