---
document_id: FCD-CORRECTNESS-PLAN
---

# Plano de correção — soundness

## Enunciado

```lean
theorem detectCycleWitness?_sound
    {X : Type*}
    [Fintype X]
    [DecidableEq X]
    {f : X → X}
    {x : X}
    {w : CycleWitness}
    (h : detectCycleWitness? f x = some w) :
    CycleWitness.Valid f x w
```

## Rota

```text
h : List.find? p (cycleCandidates (card X)) = some w
        |
List.find?_some
        |
p w = true, isto eh, decide (Valid f x w) = true
        |
decide_eq_true_eq  (ou of_decide_eq_true)
        |
Valid f x w
```

Duas APIs, ambas confirmadas no checkout:

```text
List.find?_some : List.find? p l = some a -> p a = true
decide_eq_true_eq : (decide p = true) = p
```

## Observação sobre a dependência de `mem_cycleCandidates_iff`

O gate sugeriu que a prova dependesse de três coisas: correção de
`List.find?`, correção do predicado executável e `mem_cycleCandidates_iff`.

Auditoria: **`mem_cycleCandidates_iff` não é necessária para a
soundness.** As três cotas (`baseIndex < card X`, `0 < period`,
`baseIndex + period ≤ card X`) estão **dentro** de `Valid`, e portanto
são entregues pelo próprio predicado decidido, sem consultar a lista.

Isso é uma **fortificação**, não uma lacuna: a soundness fica independente
da construção da lista. Se a enumeração fosse trocada — por Floyd, por
tabela visitada — a soundness continuaria válida sem alteração, desde que
o predicado permaneça o mesmo.

`mem_cycleCandidates_iff` é indispensável na **completude**, onde a
direção é a inversa: dado um par válido, mostrar que ele está na lista.
Registrado como desvio deliberado do plano sugerido.

`List.mem_of_find?_eq_some` está disponível caso a pertinência à lista
venha a ser necessária por outro motivo; não é usada no plano atual.

## O que a soundness **não** afirma

```text
NAO afirma que w eh o unico certificado;
NAO afirma que w.baseIndex eh minimo;
NAO afirma que w.period eh minimo;
NAO afirma nada sobre a ordem da enumeracao.
```
