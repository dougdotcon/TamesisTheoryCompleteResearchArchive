---
document_id: RT-RAW-EXECUTION-SEMANTICS
frozen: true
---

# Semântica bruta de execução

Para interpretar o certificado sobre a tabela **original**, é preciso uma
semântica que fale de `Nat` e de `Array`, não de `Fin`.

```lean
def RawTransitionTable.step? (t : RawTransitionTable) (state : Nat) :
    Option Nat :=
  t.next[state]?

def RawTransitionTable.run? (t : RawTransitionTable) :
    Nat → Nat → Option Nat
  | 0, state => some state
  | steps + 1, state => do
      let nextState ← t.step? state
      t.run? steps nextState
```

A notação `t.next[state]?` é a forma correta no checkout: `Array.getElem?`
**não** existe como constante nesta revisão — ver `LEAN_API_AUDIT.md`.

## Semântica vinculante

```text
run? k start tenta executar EXATAMENTE k transicoes;
run? 0 start = some start, mesmo ANTES da validacao;
para k > 0, qualquer acesso fora do array produz none.
```

O caso zero é deliberado e importante: `run? 0` é a identidade sobre
`Nat`, **sem** checar nada. Isso mantém `run?` uma função sobre dados
brutos, cuja única obrigação é ser fiel ao array. A validade do estado
inicial permanece responsabilidade da camada de consulta — que é
exatamente onde `validateStart` está.

Verificado no probe:

```text
#[1,2,3,2].run? 0 0   ->  some 0
#[1,2,3,2].run? 2 0   ->  some 2
#[1,2,3,2].run? 4 0   ->  some 2
#[0].run? 3 0         ->  some 0
#[0].run? 1 5         ->  none        (indice fora do array)
```

O último caso mostra `run?` fazendo o que deve: nenhum fallback, nenhum
zero silencioso — `none`.

## Ordem da recursão

O caso sucessor aplica **um** passo e recorre sobre o resto:

```text
run? (k+1) state  =  step? state >>= run? k
```

Isso é o **passo externo primeiro**. A consequência aparece em
`ITERATION_CORRESPONDENCE.md`: a indução casa com
`Function.iterate_succ_apply`, não com a variante linha.

## Proibições

```text
sem fallback;
sem valor padrao;
sem modulo no indice;
sem clamp.
```

`run?` é total como função (sempre devolve um `Option`), mas **parcial**
como semântica — e o `none` é informação, não falha a ser escondida.
