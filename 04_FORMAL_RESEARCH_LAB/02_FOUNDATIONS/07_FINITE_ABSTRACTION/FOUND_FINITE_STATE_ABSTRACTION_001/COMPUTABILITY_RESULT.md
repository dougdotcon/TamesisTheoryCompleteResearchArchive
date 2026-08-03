---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-COMPUTABILITY-RESULT
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
noncomputable_declarations: 0
---

# Computabilidade

## O que executa

```text
CertifiedFiniteAbstraction    estrutura de dado
analyzeAbstractSystem         funcao computavel
```

Nenhuma declaração da frente é `noncomputable`.

## Evidência operacional

Quatro avaliações concretas reduzem por `decide`:

```text
analyzeAbstractSystem boolToUnitAbstraction unitEncoding false = .ok ⟨0,1⟩
analyzeAbstractSystem boolToUnitAbstraction unitEncoding true  = .ok ⟨0,1⟩
analyzeAbstractSystem idAbstraction idEnc4 ⟨0,_⟩               = .ok ⟨2,2⟩
analyzeAbstractSystem parityAbstraction idEnc2 ⟨0,_⟩           = .ok ⟨0,2⟩
```

Uma definição bloqueada por escolha clássica não reduziria. A pegada
`Classical.choice` que aparece no `#print axioms` vive em proposições,
não no caminho de execução.

## O que permanece proposicional

```text
iterate_commutes                            Prop
analyzeAbstractSystem_observational_sound   Prop
OrbitSeparating                             Prop
analyzeAbstractSystem_reflected_sound       Prop
analyzeAbstractSystem_complete              Prop, existencial
```

`analyzeAbstractSystem_complete` afirma **existência** de certificado. O
certificado utilizável continua vindo da função computável, nunca de
`Classical.choose`.

## APIs não computáveis, deliberadamente evitadas

```text
Fintype.equivFin        rejeitada ja na frente da codificacao
Function.periodicOrbit  nao usada
Classical.choose        nao usada
```

## Fronteira honesta

```text
A frente nao afirma custo, complexidade ou desempenho.

Nenhum modelo de custo foi definido, e por isso nenhuma
afirmacao de complexidade e permitida — ABS-GAP-020.
```

A execução de `analyzeAbstractSystem` herda inteiramente o custo de
`analyzeEncodedSystem`, que também não tem modelo de custo declarado. A
única diferença é uma aplicação de `abstract` ao estado inicial.
