---
document_id: RT-PROOF-AUDIT
forbidden_tokens: 0
silent_corrections: 0
detector_internals: 0
---

# Auditoria das provas

## Contagens

```text
estruturas       2     RawTransitionTable, ValidatedTransitionTable
indutivos        1     RuntimeCycleError
definicoes       9
instancias       1     RawTransitionTable.decidableValid
teoremas        18     (1 privado: analyze_reduce)
arquivos         6 + 1 agregador da frente + 1 de trilha + 3 testes
linhas         869
```

## Auditorias de contagem zero

```text
tokens de prova incompleta                    0
marca de nao-computabilidade                  0
escolha classica extraindo dado               0
igualdade decidivel classica                  0
correcoes silenciosas de indice no CODIGO     0
lema de contagem do pigeonhole                0
teorema de colisao limitada                   0
enumeracao de candidatos do detector          0
imports proibidos                             0
objeto de orbita quociente                    0
sorryAx                                       0
```

Duas observações sobre falsos positivos, ambas revisadas manualmente:

* a busca por correções silenciosas casou **três linhas de
  documentação** em `Validation.lean` — as próprias proibições e o nome
  "anti-clamp". Nenhuma é código.
* a busca por imports proibidos casou o nome do módulo
  `DynamicAnalysis`, que contém a substring `Analysis`. A lista de
  imports declarados confirma que só existem três imports externos.

## O que compilou de primeira

Todos os cinco módulos do núcleo compilaram na primeira tentativa,
incluindo `analyzeTransitionTable_sound` e `_complete` — as duas
obrigações que a revisão da especificação apontava como as únicas sem
evidência executável.

Isso não é sorte: a revisão já havia demonstrado
`run?_eq_iterate_step`, `step?_eq_some_step`,
`detectCycle?_raw_repeat` e os dois teoremas de erro em ambiente
descartável, e registrado os padrões de prova que funcionam — incluindo
as três abordagens que **não** funcionam para reduzir o `do` sobre
`Except`.

## Reutilização, não reimplementação

```text
detectCycleWitness?           -> detectCycle?              uma linha
detectCycleWitness?_sound     -> detectCycle?_sound        termo de uma linha
detectCycleWitness?_complete  -> detectCycle?_complete     termo de uma linha
```

E, indiretamente e sem mencioná-los: `exists_bounded_iterate_collision`,
a casa dos pombos e a enumeração de candidatos. **Quinta frente** a
consumir o pigeonhole através do teorema original.

## O auxiliar privado

`analyze_reduce` é o único auxiliar privado da frente. Ele isola as duas
reduções que a notação `do` esconde e é usado por soundness e por
completeness. Sem ele, cada uma repetiria o mesmo bloco de `unfold`,
`rw [show ... from dif_pos]` e `show`.

## O que as provas **não** estabelecem

```text
que baseIndex ou period sejam minimos;
qualquer limite de complexidade;
que a tabela represente corretamente um sistema externo real;
enumeracao global de componentes;
totalizacao do detector.
```
