---
document_id: ENC-SEMICONJUGATION
probe_status: PROBE_PROVED
---

# Semiconjugação

## Enunciado

```lean
theorem tableIndex_semiconj (e) (stepS) :
    Function.Semiconj (e.tableIndex stepS) stepS (buildTransitionTable e stepS).step :=
  fun s => (table_step_commutes e stepS s).symm
```

Termo de uma linha.

## A orientação, que é fácil de errar

```text
Function.Semiconj f ga gb  significa  ∀ x, f (ga x) = gb (f x)
```

Portanto `Semiconj tableIndex stepS step` significa

```text
∀ s, tableIndex (stepS s) = step (tableIndex s)
```

enquanto `table_step_commutes` afirma

```text
step (tableIndex s) = tableIndex (stepS s)
```

**São uma o `.symm` da outra.** Essa inversão é obrigatória e está
congelada; escrevê-la ao contrário produz um erro de unificação que o
probe já mostrou não ser automático.

## Classificação

```yaml
table_step_commutes:
  category: PUBLIC_SPECIFICATION_CORE
  role: enunciado legivel; eh o que se prova

tableIndex_semiconj:
  category: PUBLIC_SPECIFICATION_CORE
  role: forma exigida por Function.Semiconj.iterate_right
```

Ambos públicos. **Não são redundantes**: o primeiro é o teorema que um
leitor humano confere; o segundo é a forma que a API de Mathlib consome.
Manter apenas um obrigaria a inserir um `.symm` em cada uso — exatamente
o tipo de ruído que a frente anterior eliminou centralizando reduções.

## Por que isso encurta a frente

`Function.Semiconj.iterate_right` existe, com axiomas `[propext]` e a
assinatura

```lean
Semiconj f ga gb → ∀ n, Semiconj f ga^[n] gb^[n]
```

Descoberta no gate de portfólio, ela transforma a comutação de iteradas —
que na frente anterior custou uma indução com dois `show` e uma escolha
delicada entre `iterate_succ_apply` e sua variante — em **um termo de uma
linha**.


---

## Revisão — `2066edc`

**Superado** por `FINAL_COMMUTATION_THEOREMS.md`.

A revisão inverteu os papéis: a semiconjugação passa a ser **provada
diretamente** e a comutação de um passo passa a ser seu `.symm`. O
argumento deste documento — de que as duas devem coexistir — foi mantido;
o que mudou foi qual delas é o teorema e qual é o corolário.
