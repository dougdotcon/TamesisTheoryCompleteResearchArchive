---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-REFLECTED-SOUNDNESS
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
category: PUBLIC_SPECIFICATION_CORE
semantic_strength: CONCRETE_RECURRENCE_UNDER_HYPOTHESIS
---

# Soundness concreta refletida

## Assinatura congelada

```lean
theorem analyzeAbstractSystem_reflected_sound
    {abstraction :
      CertifiedFiniteAbstraction C A stepC stepA}
    {encoding : CertifiedFiniteEncoding A n}
    {start : C}
    {witness : CycleWitness}
    (hSeparating :
      OrbitSeparating
        abstraction.abstract
        stepC
        start)
    (h :
      analyzeAbstractSystem abstraction encoding start =
        .ok witness) :
    (stepC^[witness.baseIndex + witness.period]) start
      =
    (stepC^[witness.baseIndex]) start
```

## DAG da prova

```text
analyzeAbstractSystem_observational_sound
→ hSeparating aplicado aos indices baseIndex + period e baseIndex
→ igualdade concreta
```

Um termo:

```lean
hSeparating (witness.baseIndex + witness.period) witness.baseIndex
  (analyzeAbstractSystem_observational_sound h)
```

## A hipótese está visível, e é obrigatória

`hSeparating` é argumento **explícito** da assinatura. Ela não vive
dentro de `CertifiedFiniteAbstraction`, não é instância, não é
`autoParam` e não é derivada.

Esconder a hipótese dispararia `STOP-ABS-005`. A visibilidade é o
conteúdo científico do teorema: quem quiser a conclusão concreta tem de
exibir a separação.

## Por que separação na órbita, e não injetividade global

Injetividade global é suficiente — `orbitSeparating_of_injective` o
prova — e desnecessariamente forte. A órbita alcançada a partir de
`start` é o único lugar onde os índices do witness vivem. Exigir mais
tornaria o teorema inaplicável a abstrações que perdem informação fora
da órbita, que é o caso normal.

## Onde a conclusão termina

```text
igualdade entre estados CONCRETOS, no tipo C
```

Esta é a única declaração pública da frente que conclui em `C`, e ela
paga por isso com uma hipótese explícita.
