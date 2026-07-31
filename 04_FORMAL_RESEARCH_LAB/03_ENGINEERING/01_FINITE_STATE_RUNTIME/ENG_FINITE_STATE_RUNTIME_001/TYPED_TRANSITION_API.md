---
document_id: RT-TYPED-TRANSITION-API
frozen: true
---

# Função de transição tipada

```lean
def ValidatedTransitionTable.step (t : ValidatedTransitionTable) :
    Fin t.next.size → Fin t.next.size :=
  fun i => ⟨t.next[i], t.closed i⟩
```

Uma linha. O valor é o lookup; a prova de que ele está no domínio é
exatamente o campo `closed` aplicado ao índice.

**É aqui que o dado dinâmico vira sistema formal.** Antes desta linha há
um `Array Nat` que pode conter qualquer coisa; depois dela há uma função
**total** sobre um tipo finito com igualdade decidível — precisamente a
interface que `detectCycleWitness?` exige.

## Proibições

```text
Classical.choose
fallback
mod
clamp
getD
```

Nenhuma é necessária: `t.closed i` já fornece a prova. Qualquer uma delas
seria sintoma de que a validação foi contornada.

## Correspondência com o lookup

```lean
@[simp] theorem ValidatedTransitionTable.step_val
    (t : ValidatedTransitionTable) (i : Fin t.next.size) :
    (t.step i : Nat) = t.next[i]
```

**Verificado no probe: fecha por `rfl`.** A projeção `Fin.val` do
anônimo `⟨t.next[i], _⟩` é definicionalmente `t.next[i]`.

Marcado `@[simp]` porque toda ponte com a camada bruta passa por ele —
`step?_eq_some_step`, `run?_eq_iterate_step` e a interpretação final do
witness.

## Totalidade

`step` é total **por construção**, não por convenção. O tipo
`Fin t.next.size → Fin t.next.size` não admite valor de escape, e a
validação garantiu que nenhum é necessário. É essa totalidade que permite
aplicar `Function.iterate` sem qualquer hipótese adicional.
