---
document_id: RT-START-STATE-VALIDATION
frozen: true
---

# Validação do estado inicial

```lean
def validateStart (t : ValidatedTransitionTable) (start : Nat) :
    Except RuntimeCycleError (Fin t.next.size) :=
  if h : start < t.next.size then
    .ok ⟨start, h⟩
  else
    .error (.initialStateOutOfBounds start t.next.size)
```

## Exigências

```text
preservar EXATAMENTE start;
nao aplicar modulo;
nao aplicar clamp;
nao escolher zero;
nao exigir tabela nao vazia como hipotese separada.
```

A última é consequência da política da tabela vazia: com
`next.size = 0`, nenhum `start` satisfaz `start < 0`, e o erro sai
naturalmente, sem hipótese adicional. Verificado no probe:
`analyzeT ⟨#[]⟩ 0` devolveu `error (initialStateOutOfBounds 0 0)`.

## Teoremas

```lean
theorem validateStart_sound {t : ValidatedTransitionTable} {start : Nat}
    {s : Fin t.next.size} (h : validateStart t start = .ok s) :
    (s : Nat) = start

theorem validateStart_complete (t : ValidatedTransitionTable) {start : Nat}
    (h : start < t.next.size) :
    ∃ s, validateStart t start = .ok s
```

`validateStart_sound` é a garantia de **não corrigir**: o índice tipado
devolvido tem exatamente o valor pedido. É o teorema que torna
impossível um `clamp` silencioso passar despercebido.

Uma equivalência completa — `validateStart t start = .ok s ↔ ...` — fica
como corolário **opcional**, e só se algum consumidor precisar.

## Separação de responsabilidades

```text
validateTransitionTable   valida o DADO
validateStart             valida a CONSULTA
detectCycle?              EXECUTA
```

Três funções, três erros, três teoremas. O gate proíbe explicitamente
combiná-las em um único `Bool`, e a razão é prática: para quem chama, a
informação de **qual** validação falhou é o produto principal.
