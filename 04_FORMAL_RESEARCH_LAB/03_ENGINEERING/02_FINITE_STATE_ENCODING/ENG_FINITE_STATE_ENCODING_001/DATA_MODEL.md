---
document_id: ENC-DATA-MODEL
---

# Modelo de dados

## A estrutura

```lean
structure CertifiedFiniteEncoding (S : Type*) (n : Nat) where
  encode : S → Fin n
  decode : Fin n → S
  decode_encode : ∀ s : S, decode (encode s) = s
  encode_decode : ∀ i : Fin n, encode (decode i) = i
```

```text
campos de dado    2   encode, decode
campos Prop       2   apagados na execucao
typeclasses       0
parametros        S, n
```

## O que **não** está na estrutura

```text
stateCount          o tamanho eh o parametro n
Array               a tabela eh construida, nao armazenada
stepS               eh argumento, nao campo
estado inicial      eh argumento
CycleWitness        eh resultado
provas sobre ciclos pertencem a analise
Fintype             proibido como fonte
DecidableEq         desnecessario
```

Mesmo princípio da frente anterior, onde `RawTransitionTable.stateCount`
foi proibido por duplicar `next.size`: **nenhum campo redundante**.

## Por que `n` e não `Fintype.card S`

`Fintype.card S` exigiria `[Fintype S]`, e a equivalência com `Fin (card S)`
só existe por `Fintype.equivFin`, que é `noncomputable`. O parâmetro `n`
é explícito, computável e não impõe nada ao consumidor.

## Relação com o modelo da frente anterior

```text
RawTransitionTable          Array Nat, possivelmente invalido
ValidatedTransitionTable    Array Nat + fechamento provado
CertifiedFiniteEncoding     S <-> Fin n, com as duas leis
```

As duas primeiras existem e não mudam. A terceira é o que esta frente
acrescenta, e ela **não** substitui nenhuma delas: `validateTransitionTable`
continua sendo a porta para dados não confiáveis.
