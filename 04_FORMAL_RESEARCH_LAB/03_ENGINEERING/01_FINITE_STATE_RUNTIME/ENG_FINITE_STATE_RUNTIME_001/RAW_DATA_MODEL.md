---
document_id: RT-RAW-DATA-MODEL
frozen: true
---

# Modelo de dados bruto — congelado

```lean
structure RawTransitionTable where
  next : Array Nat
deriving DecidableEq, Repr, BEq
```

Um único campo. A tabela bruta **pode** ser inválida — é isso que a torna
a representação certa para a entrada.

## Campos rejeitados

```text
size          derivavel de next.size
stateCount    idem
proof         a tabela bruta nao carrega garantia alguma
start         eh parametro da CONSULTA, nao da tabela
fallback      nao existe fallback nesta frente
```

Motivo do primeiro, que governa todos:

```text
o numero de estados eh SEMPRE next.size;
armazenar size criaria redundancia e obrigacao de consistencia.
```

Mesma disciplina que rejeitou `entryPoint` em `CycleWitness`.

## O accessor `stateCount`

```lean
def RawTransitionTable.stateCount (t : RawTransitionTable) : Nat :=
  t.next.size
```

**Decisão: não criar.** Ele não melhora a API — apenas duplica
`next.size` sob um segundo nome público, e a regra é explícita:

```text
nao congelar simultaneamente dois nomes publicos para o tamanho.
```

`t.next.size` é curto, é o nome que o Lean já usa nos tipos `Fin`, e
aparece literalmente nas assinaturas de `step`, `validateStart` e do erro
`initialStateOutOfBounds`. Introduzir `stateCount` obrigaria a escolher um
dos dois em cada assinatura, ou a provar `stateCount = next.size` em toda
ponte.

Registrado como decisão de API, não como omissão. Se a revisão discordar,
a alternativa é adotar `stateCount` **em toda parte** e nunca `next.size`
— nunca os dois.

## Semântica

```text
cada POSICAO do array representa um estado;
o VALOR em cada posicao eh o indice do sucessor daquele estado.
```

Portanto o espaço de estados é `Fin next.size`, e o índice `i` denota o
estado `i`.

## Instâncias

`DecidableEq`, `Repr` e `BEq`, todas derivadas. `Repr` é o que torna os
`#eval` de teste legíveis; `DecidableEq` e `BEq` sustentam os testes de
regressão. Nenhuma outra instância será adicionada.
