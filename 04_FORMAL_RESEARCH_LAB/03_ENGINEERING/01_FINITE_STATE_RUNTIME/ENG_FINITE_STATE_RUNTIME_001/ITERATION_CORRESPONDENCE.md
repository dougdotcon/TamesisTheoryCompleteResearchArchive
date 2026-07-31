---
document_id: RT-ITERATION-CORRESPONDENCE
central_result: true
---

# Correspondência de iterações

Este é o **resultado central** do adaptador. Sem ele, o certificado fala
de um objeto Lean que ninguém consegue relacionar com o dado de entrada.

## Correspondência de uma transição

```lean
theorem ValidatedTransitionTable.step?_eq_some_step
    (t : ValidatedTransitionTable) (i : Fin t.next.size) :
    t.toRaw.step? (i : Nat) = some ((t.step i : Fin t.next.size) : Nat)
```

Conecta o **lookup opcional** na tabela bruta à **função total** no
domínio validado. A prova reduz a `t.next[i]? = some t.next[i]`, que vale
porque `i.isLt` garante o índice dentro do array, mais `step_val`.

## Correspondência de iterações

```lean
theorem ValidatedTransitionTable.run?_eq_iterate_step
    (t : ValidatedTransitionTable) (start : Fin t.next.size) (k : Nat) :
    t.toRaw.run? k (start : Nat) =
      some (((t.step)^[k] start : Fin t.next.size) : Nat)
```

## Estratégia de prova

```text
inducao em k;
caso zero por rfl — run? 0 s = some s e f^[0] s = s;
caso sucessor usando step?_eq_some_step;
relacao entre Nat.iterate no sucessor e aplicacao de step.
```

### A orientação, auditada e não presumida

O checkout oferece **duas** variantes, ambas confirmadas:

```text
Function.iterate_succ_apply  : f^[n+1] x = f^[n] (f x)
Function.iterate_succ_apply' : f^[n+1] x = f (f^[n] x)
```

`run?` aplica **um passo e recorre sobre o resto**:

```text
run? (k+1) state = step? state >>= run? k
```

Portanto a variante que casa é a **primeira**, `iterate_succ_apply`, com a
contagem externa consumindo o passo **interno** primeiro. A generalização
da indução deve ser sobre o **estado inicial**, não sobre `k` fixo: o
enunciado é provado para todo `start` simultaneamente.

Este é exatamente o tipo de detalhe que a frente anterior errou uma vez —
a orientação de `Function.iterate_add_apply` — e que aqui foi auditado
**antes** de especificar.

## O que este teorema **não** diz

```text
NAO diz que a tabela representa corretamente um sistema real;
NAO diz nada sobre minimalidade;
NAO enumera componentes;
NAO fala de estados inalcancaveis.
```

Ele diz uma coisa só, e é a coisa certa: **executar a tabela bruta `k`
vezes a partir de um estado validado dá o mesmo resultado que iterar a
função tipada `k` vezes.**
