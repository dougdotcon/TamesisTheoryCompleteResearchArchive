---
document_id: RT-CLOSURE-RECORD
work_item_id: ENG-FINITE-STATE-RUNTIME-001
closed_at: 2026-08-01
closed_at_commit: 746102fa458fe7ccda6d8939bb3f8834a8ac0dc4
result_review: APPROVED
extension_status: NOT_AUTHORIZED
---

# Registro de encerramento

## O que a frente entregou

**A primeira cadeia completa do laboratório que começa em um dado de
runtime potencialmente inválido e termina em um certificado formal de
repetição sobre esse mesmo dado.**

```text
Array Nat potencialmente invalido
        |
validacao estrutural, sem correcao silenciosa
        |
ValidatedTransitionTable
        |
Fin n -> Fin n, total por construcao
        |
detector certificado, reutilizado sem copia
        |
CycleWitness
        |
repeticao PROVADA sobre o Array original
```

O consumidor fornece `Array Nat` e `Nat`. **Zero typeclasses.**

## Números

```text
estruturas       2
indutivos        1
definicoes       9
instancias       1
teoremas        18   (1 auxiliar privado)
linhas Lean    869
testes           4, todos exit 0
regressoes      22, por decide e rfl, sem native_decide
documentos      53
lacunas         22: 14 resolvidas, 8 abertas
claims           1, a vigesima primeira do ledger
```

## O que **não** foi entregue

```text
CLI, parser, JSON, CSV, arquivo, rede;
extracao de produto;
integracao com sistemas reais;
prova de correcao da abstracao externa;
diagnostico detalhado do destino invalido;
totalizacao do detector;
Floyd, Brent, tabela visitada;
minimalidade;
modelo formal de custo;
novidade matematica ou algoritmica.
```

## As duas garantias que definem a frente

```text
1. destinos invalidos sao REJEITADOS, nunca corrigidos;
2. o certificado eh interpretado sobre o Array ORIGINAL.
```

A primeira é sustentada por `validateTransitionTable_sound` e
`validateStart_sound` — este último, o teorema **anti-clamp**. A segunda,
por `run?_eq_iterate_step` e `detectCycle?_raw_repeat`.

## Estado de encerramento

```yaml
work_status: VERIFIED
specification_status: APPROVED
formalization_status: VERIFIED
result_review: APPROVED
extension_status: NOT_AUTHORIZED

extraction_status: NOT_AUTHORIZED
cli_status: NOT_AUTHORIZED
external_format_status: NOT_AUTHORIZED
integration_status: NOT_AUTHORIZED
detailed_diagnostics_status: NOT_AUTHORIZED
external_abstraction_correctness: DEFERRED
```

## Correção documental deste gate

```text
GAP_REGISTER.yaml, cabecalho:
  resolved_formally 10 -> 11
  open_deferred      8 -> 7
```

Estritamente documental. Nenhum status individual, nenhum módulo Lean,
nenhuma claim e nenhuma força de resultado foram alterados. Ver
`METADATA_CORRECTION_RECORD.md`.

## Desvio documental declarado

```yaml
deviation_id: DOC-RT-001
classification: NAME_COLLISION_AVOIDED
```

O gate nomeava `COMPUTABILITY_REVIEW.md` entre os documentos a criar. Um
documento com esse nome **já existia**, criado em `6c3b837` no gate de
revisão da especificação, com `stage: SPECIFICATION_REVIEW`.

Escrevê-lo teria **apagado** o registro do gate anterior. O conteúdo de
resultado foi então gravado em `FINAL_COMPUTABILITY_REVIEW.md` — o mesmo
padrão dos seis `FINAL_*` que a frente já usa para documentos sucessores
de estágio — e o original foi restaurado por `git checkout`, verificado
por `git status` vazio e por `grep` do seu `stage`.

```text
documentos criados neste gate    12
documentos da frente             53
documentos preexistentes apagados 0
```

Desvio **apenas de nome de arquivo**. Nenhum conteúdo exigido pelo gate
deixou de ser produzido.

## Condições de reabertura

A frente só volta a ser tocada por um gate explícito. **Nada** do
seguinte está autorizado por consequência deste encerramento:

```text
extracao; CLI; parser; JSON; CSV; rede; integracao;
diagnostico detalhado; ENG-FINITE-STATE-RUNTIME-002;
Floyd; totalizacao de FOUND-CYCLE-DETECTION-001.
```

## A separação que não pode ser apagada

```text
o adaptador prova que A TABELA FORNECIDA eh analisada corretamente;
ele NAO prova que a tabela representa um sistema externo real.
```

## Valor registrado

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
```

Uma tabela de transições é a representação mais banal de um autômato
determinístico. O que a frente acrescenta é conectá-la, com prova, a um
detector cujas correção e completude já eram teoremas — e mostrar que a
conexão preserva a dinâmica.
