---
document_id: ENC-REVIEW-CHECKLIST
---

# Checklist para o gate de revisão

## Representação

```text
[ ] a codificacao eh dado fornecido, nao derivado
[ ] quatro campos nomeados, e nao um Equiv
[ ] nenhuma typeclass exigida
[ ] nenhum campo redundante
[ ] n eh parametro, e nao Fintype.card
```

## Construção

```text
[ ] uma unica construcao publica
[ ] Array.ofFn, e nada de List.toArray, Fintype.elems ou Finset.univ
[ ] validade por construcao, sem revalidar
[ ] o show na prova de closed foi preservado
```

## Casts — o ponto decisivo

```text
[ ] orientacao unica: size = n
[ ] exatamente dois pontos de transporte
[ ] tableIndex_val por rfl
[ ] nenhum cast avulso, nenhum Eq.ndrec, nenhum heq
[ ] o contraste termo/tatica esta registrado
```

## Comutação

```text
[ ] decode_encode, e nao encode_decode
[ ] a igualdade eh em Fin, e nao apenas entre naturais
[ ] a inversao de orientacao da semiconjugacao esta explicita
[ ] as iteradas vem de Semiconj.iterate_right, sem inducao manual
```

## Resultados centrais

```text
[ ] a soundness termina em igualdade sobre S
[ ] a completeness nao exige pre-condicoes do consumidor
[ ] nenhuma repeticao da casa dos pombos
[ ] o witness permanece em Prop
[ ] um unico corolario de erro, quantificado
```

## Fronteiras

```text
[ ] RT-GAP-017 nao foi alterado retroativamente
[ ] nenhuma afirmacao sobre sistema externo real
[ ] mathematical_novelty e algorithmic_novelty seguem NONE
[ ] 21 claims, nenhuma promovida
[ ] extracao, CLI, parser e integracao seguem NOT_AUTHORIZED
```

## Higiene

```text
[ ] zero arquivos Lean permanentes criados
[ ] zero provas permanentes
[ ] lake build nao executado
[ ] probes removidos
[ ] runtime adapter e detector intactos
[ ] legado intacto
```

## Perguntas que a revisão deve responder

1. `encodedStep` precisa mesmo ser público, ou o lema central de leitura
   pode ser reescrito para escondê-lo?
2. Manter `table_step_commutes` **e** `tableIndex_semiconj` como
   `PUBLIC_SPECIFICATION_CORE` é justificado, ou um deles deve virar
   corolário?
3. `buildTransitionTable_getElem` deve ser público, ou é auxiliar
   interno? Ele é o segundo ponto de transporte, o que argumenta a favor
   de expô-lo.
4. A pegada `Classical.choice` desde `buildTransitionTable` — herdada de
   `Array.getElem_ofFn` — é aceitável, ou vale procurar uma prova de
   `closed` mais leve?
