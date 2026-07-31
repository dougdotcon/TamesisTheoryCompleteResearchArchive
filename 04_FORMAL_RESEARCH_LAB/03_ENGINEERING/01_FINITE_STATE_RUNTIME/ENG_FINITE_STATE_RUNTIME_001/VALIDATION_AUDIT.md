---
document_id: RT-VALIDATION-AUDIT
silent_corrections: 0
---

# Auditoria da validação

## Nenhuma correção silenciosa

Busca por padrões suspeitos nos módulos da frente:

```bash
grep -RInE '%|mod|getD|clamp|fallback|min .*size|max .*size'
```

Três ocorrências, **todas em documentação**, revisadas manualmente:

| Linha | Contexto |
|---|---|
| `Validation.lean:60` | "…é entre duas tabelas brutas com o mesmo array" — a palavra casada é parte de *proposicional* |
| `Validation.lean:84` | "Nenhum **módulo**, nenhum **clamp**, nenhum zero padrão" — a própria proibição |
| `Validation.lean:96` | "teorema **anti-clamp**" |

```text
correcoes silenciosas no CODIGO: 0
```

O array é preservado byte a byte: `validateTransitionTable` devolve
`⟨raw.next, h⟩`, e `raw.next` aparece literalmente.

## Os dois teoremas que tornam a correção impossível de esconder

```lean
theorem validateTransitionTable_sound ... : validated.toRaw = raw ∧ raw.Valid
theorem validateStart_sound ... : (typedStart : Nat) = start
```

O primeiro força a tabela devolvida a ser **a mesma**; o segundo força o
índice devolvido a ter **o valor pedido**. Qualquer `%`, `clamp` ou
`getD` introduzido no futuro quebraria uma das duas provas.

## Tabela vazia

```lean
theorem valid_empty : RawTransitionTable.Valid ⟨#[]⟩
```

Provado por vacuidade: `Fin (#[]).size` é `Fin 0` e não tem habitantes.
Medido em execução:

```text
(validateTransitionTable ⟨#[]⟩).isOk = true
analyzeTransitionTable ⟨#[]⟩ 0 = error (initialStateOutOfBounds 0 0)
```

A validade é **estrutural**; a existência de estado inicial pertence à
consulta. Nenhum erro `emptyTable` foi criado; nenhum `Nonempty`,
`Inhabited` ou `0 < size` entrou no predicado.

## Separação das duas validações

```text
validateTransitionTable   -> transitionDestinationOutOfBounds
validateStart             -> initialStateOutOfBounds (start, stateCount)
```

Erros distintos, teoremas distintos, testes distintos. Nunca um único
booleano.

## Axiomas da camada de validação

```text
RawTransitionTable.Valid          [propext, Quot.sound]
validateTransitionTable           [propext, Quot.sound]
validateTransitionTable_sound     [propext, Quot.sound]
validateTransitionTable_complete  [propext, Quot.sound]
validateStart                     [propext, Quot.sound]
validateStart_sound               [propext, Quot.sound]
validateStart_complete            [propext, Quot.sound]
valid_empty                       [propext, Quot.sound]
```

**Nenhum `Classical.choice`.** A camada de validação inteira é
axiomaticamente mais leve que o detector que ela alimenta.
