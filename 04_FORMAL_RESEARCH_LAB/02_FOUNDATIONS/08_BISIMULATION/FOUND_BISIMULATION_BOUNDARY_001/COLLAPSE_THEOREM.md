---
document_id: FOUND-BISIMULATION-BOUNDARY-001-COLLAPSE-THEOREM
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
category: PUBLIC_SPECIFICATION_CORE
---

# O teorema de colapso

## Assinatura congelada

```lean
theorem bisimulation_iff_semiconj
    (abstract : C → A) (stepC : C → C) (stepA : A → A) :
    Bisimulation abstract stepC stepA
      ↔ Function.Semiconj abstract stepC stepA
```

## O lema que faz o trabalho

```lean
theorem reflects_iff_simulates
    (abstract : C → A) (stepC : C → C) (stepA : A → A) :
    Reflects abstract stepC stepA ↔ Simulates abstract stepC stepA
```

### Direção `→`

```text
h c  devolve  ⟨c', hstep : stepC c = c', hobs : abstract c' = stepA (abstract c)⟩
reescrever hobs por hstep  ⟹  abstract (stepC c) = stepA (abstract c)
```

### Direção `←`

```text
testemunha  c' := stepC c
stepC c = stepC c        por rfl
abstract (stepC c) = …   e exatamente a hipotese
```

A segunda direção é onde o colapso fica visível: **a testemunha não é
escolhida, é imposta**.

## DAG

```text
reflects_iff_simulates
        │
simulates_iff_semiconj  (Iff.rfl)
        │
        └─ bisimulation_iff_semiconj
```

## Pegada medida

```text
reflects_iff_simulates      nenhum axioma
simulates_iff_semiconj      nenhum axioma
bisimulation_iff_semiconj   nenhum axioma
```

## O que o teorema NÃO diz

```text
que bissimulacao seja igual a semiconjugacao em geral
que bissimulacao seja inutil
que sistemas nao deterministicos se comportem assim
que exista quociente, representante canonico ou coinducao
```

Ver [`SCOPE_BOUNDARY.md`](SCOPE_BOUNDARY.md).

## Por que o resultado é útil, sendo negativo

Ele fecha uma rota de pesquisa. Depois da frente anterior, a pergunta
natural era "e se exigirmos bissimulação?". A resposta é que, neste
recorte, **já se tem bissimulação de graça**, e ela não ajuda.

Isso redireciona o esforço para a condição que de fato funciona:
`OrbitSeparating`, injetividade sobre a órbita alcançada.
