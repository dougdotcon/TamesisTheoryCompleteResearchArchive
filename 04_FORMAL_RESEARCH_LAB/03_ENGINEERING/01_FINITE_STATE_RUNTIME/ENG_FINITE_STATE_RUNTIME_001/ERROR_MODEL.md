---
document_id: RT-ERROR-MODEL
frozen: true
---

# Modelo de erros — congelado

```lean
inductive RuntimeCycleError
  | transitionDestinationOutOfBounds
  | initialStateOutOfBounds (start : Nat) (stateCount : Nat)
  | internalDetectorFailure
deriving DecidableEq, Repr, BEq
```

## Os três construtores

| Construtor | Quando | Carga |
|---|---|---|
| `transitionDestinationOutOfBounds` | a tabela tem ao menos um destino fora do domínio | **nenhuma**, na v1 |
| `initialStateOutOfBounds` | a tabela é válida, mas `start ≥ next.size` | `start` e `stateCount` |
| `internalDetectorFailure` | o detector devolveu `none` | nenhuma |

```text
NAO usar um unico erro generico para tabela invalida e inicio invalido.
```

Os dois são falhas de naturezas diferentes: a primeira é do **dado**, a
segunda é da **consulta**. Colapsá-las destruiria a informação mais útil
para quem chama.

## Por que o primeiro erro é genérico na v1

`transitionDestinationOutOfBounds` **não** carrega `source`,
`destination`, o primeiro índice inválido nem a lista de todos os
inválidos.

```text
localizar detalhadamente o primeiro destino invalido exigiria uma
segunda busca e uma prova adicional, sem ser necessaria para garantir
seguranca ou correcao do adaptador inicial.
```

A validação é feita por `if h : t.Valid`, que decide a proposição inteira;
extrair a testemunha do `¬∀` exigiria reconstruí-la por uma busca
separada, com seu próprio lema de correção. É trabalho real, e não muda
uma linha da garantia.

```yaml
RT-GAP-022:
  title: detailed invalid-transition diagnostics
  status: OPEN_DEFERRED
```

## `internalDetectorFailure`

Permanece na função executável, **por decisão**, embora
`detectCycleWitness?_complete` prove que o `none` é impossível para
entradas válidas.

Três condições para que isso seja legítimo, todas satisfeitas:

```text
eh defesa operacional;
esta documentado como proposicionalmente impossivel;
NAO eh usado para mascarar erro de validacao.
```

A terceira é garantida pela ordem do `do`: a validação da tabela e a do
início ocorrem **antes**, e cada uma tem seu próprio erro. Quando o
`match` sobre `Option` é alcançado, a tabela já é válida e o índice já
está no domínio.

`analyzeTransitionTable_ne_internalFailure` tornará essa impossibilidade
um teorema.

## Instâncias

`DecidableEq`, `Repr` e `BEq` derivadas — necessárias para os testes de
regressão compararem erros esperados por `decide`.
