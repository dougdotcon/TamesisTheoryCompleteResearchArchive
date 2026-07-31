---
document_id: RT-VALIDATION-API
frozen: true
---

# API de validação da tabela

```lean
def validateTransitionTable (t : RawTransitionTable) :
    Except RuntimeCycleError ValidatedTransitionTable :=
  if h : t.Valid then
    .ok ⟨t.next, h⟩
  else
    .error .transitionDestinationOutOfBounds
```

O `if h :` é o `dite` dependente: no ramo positivo, `h : t.Valid` é
exatamente o campo `closed` exigido pela estrutura. Nenhuma construção
intermediária, nenhum lema.

## Exigências confirmadas no probe

```text
computavel                       #eval devolveu true/false nos quatro casos
sem fallback                     o ramo negativo eh erro, nao valor
sem modulo                       o array nao eh tocado
sem clamp                        idem
sem alteracao do array           .ok carrega t.next literalmente
sem Classical.choose explicito   #print axioms: [propext, Quot.sound]
sem marca de nao-computabilidade
```

Avaliações do probe:

```text
validateT #[]           isOk = true
validateT #[1]          isOk = false
validateT #[0]          isOk = true
validateT #[1,2,3,2]    isOk = true
```

A primeira é a política da tabela vazia em ação.

## O que está proibido

```text
destination % size
min destination (size - 1)
getD 0
qualquer reescrita do array
```

```text
NAO transformar destinos invalidos em destinos validos.
```

Esta é a proibição central da frente. Um destino corrigido produz um
sistema **diferente** daquele que o chamador descreveu, e o certificado
seria correto sobre esse outro sistema — falha silenciosa, e portanto a
pior possível.

## Política da tabela vazia — congelada

```yaml
empty_table:
  structural_validity: VALID
  executable_query: REJECTED_WITH_INVALID_START
```

Justificativa:

```text
RawTransitionTable.Valid eh universal sobre Fin 0 e, portanto, vale
vacuamente para a tabela vazia.

Entretanto, nao existe estado inicial pertencente a Fin 0.
```

Consequências, todas verificadas no probe:

```text
validateTransitionTable #[]   ->  ok
validateStart _ qualquer      ->  error
analyzeTransitionTable #[] 0  ->  error (initialStateOutOfBounds 0 0)
```

**Não** adicionar `Nonempty`, `Inhabited` nem `0 < next.size` ao
predicado de validade estrutural. Fazê-lo confundiria duas perguntas
distintas: "esta tabela é coerente?" e "esta consulta faz sentido?".
