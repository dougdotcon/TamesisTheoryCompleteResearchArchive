---
document_id: FCD-CANDIDATE-ENUMERATION
---

# Enumeração dos candidatos

## Assinatura

```lean
def cycleCandidates
    (n : ℕ) :
    List CycleWitness
```

Sem hipótese alguma sobre `X` — a função nem menciona `X`.

## Domínio

```text
baseIndex < n
0 < period
baseIndex + period <= n
```

## Ordem

```text
baseIndex crescente;
para cada baseIndex, period crescente.
```

A ordem é determinística e serve a **testes de regressão**. Ela **não** é
promovida a afirmação de minimalidade matemática. Que o primeiro candidato
aceito seja frequentemente o de menor `μ` é uma consequência da ordem, não
um teorema — e não será enunciado como tal.

## Construção candidata

```text
para mu em [0, n):
  para lam em [1, n - mu]:
    emitir <mu, lam>
```

Em termos das APIs auditadas:

```text
(List.range n).flatMap (fun m =>
  (List.range (n - m)).map (fun k => <m, k + 1>))
```

`List.range n` dá `m < n`; `List.range (n - m)` dá `k < n - m`, e com
`λ = k + 1` obtém-se `1 ≤ λ ≤ n - m`, isto é, `m + λ ≤ n`.

## Caso de fronteira `μ + λ = n`

**Incluído.** Verificado por avaliação na sonda temporária:

```text
n = 3  ->  [(0,1), (0,2), (0,3), (1,1), (1,2), (2,1)]
n = 4  ->  [(0,1), (0,2), (0,3), (0,4), (1,1), (1,2), (1,3),
            (2,1), (2,2), (3,1)]
n = 1  ->  [(0,1)]
```

Os pares `(0,3)`, `(1,2)`, `(2,1)` em `n = 3` são exatamente os de soma
`3 = n`. A fronteira está presente, e o caso `n = 1` produz o único
candidato possível.

Observação **não provada**: o comprimento parece ser `n(n+1)/2` — medido
como `6` para `n = 3` e `10` elementos listados para `n = 4`. Registrado
como observação de sonda, não como lema.

## Caso `n = 0`

```text
n = 0  ->  []
```

`List.range 0 = []`, logo a lista é vazia. Isso é **correto e desejado**:
com `card X = 0` o tipo é vazio e não existe `x : X` para iniciar. Nenhuma
hipótese `Nonempty` é necessária, exatamente como em
`FOUND-FUNCTIONAL-GRAPH-001`.

## Propriedade central

```lean
theorem mem_cycleCandidates_iff {n : ℕ} {w : CycleWitness} :
    w ∈ cycleCandidates n ↔
      w.baseIndex < n ∧
      0 < w.period ∧
      w.baseIndex + w.period ≤ n
```

Enunciado para `n` arbitrário, **sem** `Fintype` e **sem** `DecidableEq`.

Decomposição da prova, se necessária:

| Componente | Papel | API |
|---|---|---|
| soundness | todo membro satisfaz as três cotas | `List.mem_flatMap`, `List.mem_map`, `List.mem_range` |
| completude | toda tripla que satisfaz as cotas é membro | as mesmas, na direção inversa |
| duplicatas | **irrelevante** | ver abaixo |
| ordem | não é parte do `iff` | testes de regressão |

## Duplicatas

A construção `flatMap`/`map` sobre `List.range` **não** produz duplicatas,
porque `m` percorre valores distintos e, para cada `m`, `k` também. Mas
**nenhuma prova de ausência de duplicatas será exigida**: ela não afeta a
correção nem a completude do detector — `List.find?` devolve o primeiro
elemento que satisfaz o predicado, e a presença de repetições no fim da
lista seria inócua. Registrado em `CD-GAP-018`.
