---
document_id: RT-VALIDATED-DATA-MODEL
frozen: true
---

# Modelo de dados validado — congelado

```lean
structure ValidatedTransitionTable where
  next : Array Nat
  closed : ∀ i : Fin next.size, next[i] < next.size
```

O campo de prova é apagado durante a execução.

## Campos rejeitados

```text
stateCount               derivavel
step como campo          eh funcao derivada, nao dado
RawTransitionTable       duplicada — o array ja esta aqui
estado inicial           pertence a CONSULTA
CycleWitness             eh resultado, nao entrada
```

## Conversão para bruto

```lean
def ValidatedTransitionTable.toRaw (t : ValidatedTransitionTable) :
    RawTransitionTable :=
  ⟨t.next⟩

theorem ValidatedTransitionTable.toRaw_valid
    (t : ValidatedTransitionTable) : t.toRaw.Valid
```

`toRaw` será **público**. Razão: ele é a única forma de enunciar
`detectCycle?_raw_repeat` e `run?_eq_iterate_step`, que falam da execução
sobre a tabela **original**. Um `toRaw` interno tornaria os dois teoremas
centrais inenunciáveis fora do módulo.

`toRaw_valid` é imediato: o campo `closed` é exatamente `Valid` da tabela
convertida, por definição de `toRaw`.

## `Subtype` versus estrutura nomeada

Comparados `Subtype RawTransitionTable.Valid` e
`ValidatedTransitionTable`.

```text
Decisao: estrutura nomeada.
```

| Motivo | Consequência prática |
|---|---|
| API mais legível | `t.next` e `t.closed` em vez de `t.1.next` e `t.2` |
| namespace próprio | `ValidatedTransitionTable.step`, `.detectCycle?` |
| campos diretos | `step` acessa `t.closed i` sem desempacotar |
| melhor superfície para execução | o `Repr` derivado do `Subtype` carregaria a prova |
| menos projeções `.1` e `.2` | provas mais curtas |
| representação trocável | trocar `Array` por outro contêiner não muda a API |

```text
NAO manter ambas como APIs publicas equivalentes.
```

Nota: `ValidatedTransitionTable` **não** deriva `DecidableEq`, `Repr` nem
`BEq` — ela contém um campo `Prop`, e derivá-las exigiria irrelevância de
prova explícita. Comparação e impressão acontecem sobre `toRaw`.
