---
document_id: ENC-SPECIFICATION-DECISION
stage: SPECIFICATION
frozen: true
---

# Decisões congeladas

## 1. A codificação é dado, não derivação

```lean
structure CertifiedFiniteEncoding (S : Type*) (n : Nat) where
  encode : S → Fin n
  decode : Fin n → S
  decode_encode : ∀ s : S, decode (encode s) = s
  encode_decode : ∀ i : Fin n, encode (decode i) = i
```

Quatro campos nomeados. **Congelado.**

Motivo vinculante, medido no gate de portfólio:

```text
Fintype.equivFin eh noncomputable.
```

Derivar a codificação da mera existência de `[Fintype S]` tornaria a
tabela não computável. A codificação é **dado executável fornecido pelo
consumidor**.

Proibido como representação primária: `[Fintype S]`, `Fintype.equivFin`,
`Fintype.truncEquivFin`, escolha clássica, `Trunc.out`, enumeração
derivada automaticamente.

## 2. Nenhuma typeclass exigida

```text
DecidableEq S   NAO exigida
Fintype S       NAO exigida
Finite S        NAO exigida
Nonempty S      NAO exigida
Inhabited S     NAO exigida
```

O tamanho é o **parâmetro `n`**. Não existe campo `stateCount`, nem
`Array`, nem `stepS`, nem estado inicial, nem `CycleWitness`, nem prova
sobre ciclos dentro da estrutura.

## 3. `Equiv` é vista derivada opcional

```yaml
primary_public_representation: CertifiedFiniteEncoding com quatro campos
Equiv:
  status: OPTIONAL_DERIVED_VIEW
```

`CertifiedFiniteEncoding.toEquiv : S ≃ Fin n` pode existir como
adaptador. Ele **não** pode entrar na cadeia computacional principal.
`Fintype.equivFin` **nunca** cria a codificação.

## 4. Uma única construção pública

```lean
def buildTransitionTable
    (e : CertifiedFiniteEncoding S n) (stepS : S → S) :
    ValidatedTransitionTable
```

A tabela bruta pública é obtida por `(buildTransitionTable e stepS).toRaw`.
**Não** existirão `buildRawTransitionTable` e
`buildValidatedTransitionTable` como construções concorrentes.

## 5. Validade por construção, não por revalidação

A tabela nasce `ValidatedTransitionTable`. `validateTransitionTable`
**não** é chamada — ela permanece na frente anterior, para dados não
confiáveis. Esta frente não produz dado não confiável.

## 6. Uma única orientação para o tamanho

```lean
theorem buildTransitionTable_size :
  (buildTransitionTable e stepS).next.size = n
```

Orientação `size = n`, e não `n = size`. **Congelada.** Todo transporte
usa esta igualdade, invertendo-a onde necessário com `.symm`.

Não existirão `table_size_eq`, `size_table_eq` nem `stateCount`.

## 7. Um único ponto de transporte

```lean
def CertifiedFiniteEncoding.tableIndex
    (e : CertifiedFiniteEncoding S n) (stepS : S → S) (s : S) :
    Fin (buildTransitionTable e stepS).next.size :=
  Fin.cast (buildTransitionTable_size e stepS).symm (e.encode s)
```

**Toda** travessia `Fin n → Fin table.next.size` passa por aqui.
Proibido: `cast` avulso em prova, `Eq.ndrec` manual, `Classical.choice`,
módulo, `clamp`, fallback.

## 8. O teorema anti-correção

```lean
theorem tableIndex_val :
  ((e.tableIndex stepS s) : Nat) = ((e.encode s) : Nat)
```

Provado por `rfl`. O transporte **não modifica o índice natural**. É o
análogo, nesta frente, do `validateStart_sound` da frente anterior.

## 9. `tableIndex_semiconj` é o núcleo; a comutação de um passo é o meio

```yaml
table_step_commutes: PUBLIC_SPECIFICATION_CORE
tableIndex_semiconj: PUBLIC_SPECIFICATION_CORE
```

Ambos são públicos, com papéis distintos e declarados: a comutação é o
enunciado legível e o que se prova; a semiconjugação é a forma que
alimenta `Function.Semiconj.iterate_right`. Não são redundantes — a
segunda é a primeira `.symm`, e é essa `.symm` que a API de Mathlib
exige.

## 10. A soundness termina em `S`

```lean
theorem analyzeEncodedSystem_sound
    (h : analyzeEncodedSystem e stepS start = Except.ok w) :
  stepS^[w.baseIndex + w.period] start = stepS^[w.baseIndex] start
```

Igualdade **no tipo de estados**, não sobre `Nat`, não sobre a tabela.
`STOP-ENC-018` dispara se o enunciado falar apenas da tabela.

## 11. Erros preservados

`analyzeEncodedSystem` devolve `Except RuntimeCycleError CycleWitness`.
Nenhum construtor é removido, nenhum erro novo é criado, nenhum witness
padrão existe, o detector **não** é totalizado.

## 12. Um único corolário de erro

```yaml
analyzeEncodedSystem_complete: PUBLIC_SPECIFICATION_CORE
analyzeEncodedSystem_ne_error: PUBLIC_COROLLARY
```

Um teorema `≠ Except.error err` **quantificado sobre `err`** substitui os
três teoremas de exclusão individual. Os três permanecem
`DEFERRED_OPTIONAL`.
