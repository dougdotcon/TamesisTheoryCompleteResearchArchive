---
document_id: RT-METADATA-CORRECTION-RECORD
mathematical_impact: NONE
lean_impact: NONE
claim_impact: NONE
---

# Registro de correção de metadados

```yaml
issue:
  aggregate gap counts inconsistent with individual entries

mathematical_impact:
  NONE

lean_impact:
  NONE

claim_impact:
  NONE

correction:
  resolved_formally 10 → 11
  open_deferred 8 → 7
```

## Como o defeito foi detectado

O relatório do gate de formalização já o identificou, comparando a
contagem declarada no cabeçalho de `GAP_REGISTER.yaml` com a contagem
real das entradas. Um segundo commit era proibido naquele gate, e a
correção ficou explicitamente registrada como pendente.

## Verificação antes da correção

```text
cabecalho declarado    resolved_formally: 10   open_deferred: 8
entradas reais         RESOLVED_FORMALLY: 11   OPEN_DEFERRED: 7
total                  22   (consistente nos dois)
```

As onze entradas `RESOLVED_FORMALLY` são `RT-GAP-002` a `RT-GAP-010`,
`RT-GAP-012` e `RT-GAP-016`. As sete `OPEN_DEFERRED` são `RT-GAP-013`,
`-014`, `-015`, `-017`, `-018`, `-019` e `-022`.

## O que a correção **não** faz

```text
nao altera status individuais;
nao fecha nenhum gap;
nao modifica modulo Lean algum;
nao cria claim;
nao altera a forca de nenhum resultado.
```

É estritamente documental: dois inteiros num cabeçalho de agregação
passaram a coincidir com o que as entradas sempre disseram.

## Verificação depois da correção

```text
resolved_by_design: 1
resolved_formally: 11
resolved_by_boundary: 2
open_deferred: 7
open_bibliographic: 1
total: 22
```

Soma: `1 + 11 + 2 + 7 + 1 = 22`. Consistente.

## Causa raiz

O cabeçalho foi escrito à mão junto com as entradas, e não derivado
delas. Duas reclassificações de última hora — `RT-GAP-016` para
`RESOLVED_FORMALLY` — não foram propagadas ao agregado.

A lição é a mesma que já apareceu duas vezes neste laboratório sob outra
forma: **contagem escrita à mão diverge; contagem derivada não.** A
verificação de consistência entre cabeçalho e entradas passou a ser feita
por script neste gate, e o resultado é reportado.
