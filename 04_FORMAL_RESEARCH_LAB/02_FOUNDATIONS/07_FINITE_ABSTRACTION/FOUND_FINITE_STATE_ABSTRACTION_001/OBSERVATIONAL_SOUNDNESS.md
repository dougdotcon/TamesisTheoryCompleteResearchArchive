---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-OBSERVATIONAL-SOUNDNESS
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
category: PUBLIC_SPECIFICATION_CORE
semantic_strength: OBSERVATIONAL_RECURRENCE
---

# Soundness observacional — o resultado central

## Assinatura congelada

```lean
theorem analyzeAbstractSystem_observational_sound
    {abstraction :
      CertifiedFiniteAbstraction C A stepC stepA}
    {encoding : CertifiedFiniteEncoding A n}
    {start : C}
    {witness : CycleWitness}
    (h :
      analyzeAbstractSystem abstraction encoding start =
        .ok witness) :
    abstraction.abstract
        ((stepC^[witness.baseIndex + witness.period]) start)
      =
    abstraction.abstract
        ((stepC^[witness.baseIndex]) start)
```

## DAG da prova

```text
analyzeEncodedSystem_sound no sistema A
→ igualdade entre iteradas de stepA
→ iterate_commutes para os dois indices
→ igualdade entre observacoes de estados concretos
```

Duas reescritas por `iterate_commutes` e um `exact`. A prova não repete
a casa dos pombos, não repete o detector e não reabre a tabela.

## Onde a conclusão termina, e por quê

```text
a conclusao vive em A, depois de aplicar abstract
```

A igualdade afirma que os **dois estados concretos têm a mesma
observação**. Ela não afirma que os estados concretos são iguais. Essa
distinção é a frente inteira.

Concluir em `C` aqui dispararia `STOP-ABS-004`.

Adicionar `OrbitSeparating` a este teorema seria enfraquecê-lo: o
resultado observacional vale **sem hipótese alguma além da
semiconjugação**, e é essa gratuidade que o torna útil.

## O que o teorema não afirma

```text
que baseIndex seja minimo
que period seja o periodo minimo
que o witness seja unico
que o witness seja invariante sob recodificacao
que o ciclo abstrato seja concreto
que a abstracao externa esteja correta
```

## Classificação

```yaml
category: PUBLIC_SPECIFICATION_CORE
semantic_strength: OBSERVATIONAL_RECURRENCE
requires_orbit_separating: false
concludes_in: A
```
