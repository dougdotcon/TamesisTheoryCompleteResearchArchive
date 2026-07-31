---
document_id: RT-VALIDATION-REVIEW
silent_corrections_in_code: 0
---

# Revisão da validação

## Comportamento confirmado

```text
raw.Valid   ->  ok ⟨raw.next, prova⟩
¬raw.Valid  ->  error transitionDestinationOutOfBounds
```

O array é passado adiante **literalmente**: `⟨raw.next, h⟩`. Nenhuma
cópia, nenhuma reescrita, nenhum elemento tocado.

## Busca por correções silenciosas

```bash
grep -RInE '%|\bmod\b|getD|clamp|fallback|min .*size|max .*size'
```

Duas ocorrências, **ambas em documentação**, revisadas manualmente:

| Linha | Texto |
|---|---|
| `Validation.lean:84` | "Nenhum **módulo**, nenhum **clamp**, nenhum zero padrão" |
| `Validation.lean:96` | "Este é o teorema **anti-clamp**" |

```text
correcoes silenciosas no CODIGO EXECUTAVEL: 0
```

## Os dois teoremas que tornam a correção impossível de esconder

```lean
validateTransitionTable_sound : validated.toRaw = raw ∧ raw.Valid
validateStart_sound           : (typedStart : Nat) = start
```

O primeiro força a tabela devolvida a ser **a mesma**; o segundo força o
índice a ter **o valor pedido**. Qualquer `%`, `clamp` ou `getD`
introduzido no futuro quebraria uma das duas provas — não é uma
convenção, é uma obrigação verificada pelo kernel.

## Completude

`validateTransitionTable_complete` e `validateStart_complete` são
**termos de uma linha** cada, com testemunhas explícitas
`⟨raw.next, h⟩` e `⟨start, h⟩`.

## A separação que a revisão reafirma

```text
validateTransitionTable   valida o DADO      -> transitionDestinationOutOfBounds
validateStart             valida a CONSULTA  -> initialStateOutOfBounds
```

Nunca um único booleano. Para quem chama, **qual** validação falhou é o
produto principal.

## Tabela vazia

```text
estruturalmente valida    por vacuidade sobre Fin 0
consulta rejeitada        initialStateOutOfBounds start 0, para todo start
erro emptyTable           NAO existe
```

Nenhum `Nonempty`, `Inhabited` ou `0 < size` entrou no predicado de
validade.

## Axiomas

```text
RawTransitionTable.Valid          [propext, Quot.sound]
validateTransitionTable           [propext, Quot.sound]
validateTransitionTable_sound     [propext, Quot.sound]
validateTransitionTable_complete  [propext, Quot.sound]
validateStart                     [propext, Quot.sound]
validateStart_sound               [propext, Quot.sound]
validateStart_complete            [propext, Quot.sound]
```

**Sem `Classical.choice`.** A camada de validação inteira é
axiomaticamente mais leve que o detector que ela alimenta.
