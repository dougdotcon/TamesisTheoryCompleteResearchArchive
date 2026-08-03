---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-ITERATION-CORRESPONDENCE
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
---

# Correspondência de iteradas

## Assinatura congelada

```lean
theorem CertifiedFiniteAbstraction.iterate_commutes
    (abstraction :
      CertifiedFiniteAbstraction C A stepC stepA)
    (k : Nat)
    (start : C) :
    abstraction.abstract ((stepC^[k]) start) =
      (stepA^[k]) (abstraction.abstract start)
```

## Rota obrigatória

```lean
abstraction.commutes.iterate_right k start
```

Um termo. Nenhuma tática, nenhuma indução.

## O que o teorema NÃO exige

```text
finitude de C          nao
finitude de A          nao
igualdade decidivel    nao
encoding               nao
estado inicial fixo    nao
k limitado             nao
```

O teorema pertence **somente** à abstração. Ele é anterior à codificação
e independente dela — por isso vive no módulo da abstração, e não no da
análise.

## Por que indução manual está proibida

O laboratório já registrou, em frente anterior:

```text
"Nao reprovar a comutacao de iteradas por inducao manual:
 Semiconj.iterate_right resolve"
```

Esta é a terceira frente consecutiva a consumir `iterate_right`. Uma
indução manual seria uma quarta reimplementação de um lema de Mathlib.

## Pegada medida

```text
CertifiedFiniteAbstraction.iterate_commutes    [propext]
```

`propext` é herdado de `Function.Semiconj.iterate_right`. Nenhuma
escolha clássica participa, e nada aqui produz dado.
