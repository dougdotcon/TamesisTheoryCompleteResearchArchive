---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-ABSTRACT-COMPLETENESS
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
category: PUBLIC_SPECIFICATION_CORE
semantic_strength: ABSTRACT_EXISTENCE
---

# Completeness abstrata

## Assinatura congelada

```lean
theorem analyzeAbstractSystem_complete
    (abstraction :
      CertifiedFiniteAbstraction C A stepC stepA)
    (encoding : CertifiedFiniteEncoding A n)
    (start : C) :
    ∃ witness,
      analyzeAbstractSystem abstraction encoding start =
        .ok witness
```

## DAG da prova

```text
analyzeEncodedSystem_complete
→ estado abstrato abstraction.abstract start
→ mesmo witness existencial
```

Um termo:

```lean
analyzeEncodedSystem_complete encoding stepA (abstraction.abstract start)
```

## O que ela garante, e o que não garante

```text
GARANTE   a analise abstrata nunca falha, para qualquer entrada
GARANTE   existe um witness observacional

NAO garante repeticao concreta
NAO garante minimalidade
NAO garante unicidade
NAO depende de OrbitSeparating
```

Descrever este teorema como completeness **concreta** dispararia
`STOP-ABS-018`. A recorrência concreta exige
`analyzeAbstractSystem_reflected_sound` e sua hipótese.

## Sem pré-condição

O consumidor não precisa provar validade de tabela nem domínio de
índice: a construção já garantia ambos na frente anterior, e a ponte não
introduz nova obrigação. Também não há hipótese sobre `C`.

## Witness permanece existencial

```text
a conclusao vive em Prop
nenhuma escolha classica extrai o witness
```

O witness executável continua a ser produzido por
`analyzeAbstractSystem`, que é computável. `Classical.choose` não é
usado para produzir dado — isso dispararia proibição explícita do
laboratório.
