---
document_id: ENC-CLOSURE-RECORD
work_item_id: ENG-FINITE-STATE-ENCODING-001
closed_at: 2026-08-01
closed_at_commit: 2a05887463d44bc3da1ca1c4ac4ea21c6b68390a
result_review: APPROVED
extension_status: NOT_AUTHORIZED
---

# Registro de encerramento

## O que a frente entregou

**A primeira cadeia do laboratório que começa em um objeto Lean tipado e
termina em um certificado interpretado nesse mesmo objeto.**

```text
S, com stepS : S -> S
    |
CertifiedFiniteEncoding S n, FORNECIDA
    |
Array.ofFn, tabela validada por construcao
    |
runtime adapter verificado, sem copia
    |
CycleWitness
    |
stepS^[b + p] start = stepS^[b] start,  em S
```

O consumidor fornece a codificação, `stepS` e `start`. **Zero
typeclasses.**

## Números

```text
estruturas          1
definicoes          4
teoremas           11   (1 privado)
instancias          0
linhas Lean       450   + 298 de testes
modulos             5   + agregador
declaracoes publicas   15
auxiliares internos     1
pontos de transporte    2
testes                  4 arquivos, 6 execucoes isoladas
lake build           PASS, 8757 jobs
documentos             65
lacunas                20: 15 resolvidas, 5 abertas
claims                  1, a vigesima segunda do ledger
```

## O que **não** foi entregue

```text
toEquiv;
consequencias opcionais de bijetividade;
invariancia do witness concreto sob recodificacao;
minimalidade, unicidade;
modelo de custo, benchmark;
extracao, CLI, parser, JSON, rede, integracao;
correcao de um sistema externo especifico;
novidade matematica ou algoritmica.
```

## As três garantias que definem a frente

```text
1. a codificacao eh dado FORNECIDO, nunca derivada por escolha;
2. o transporte NAO altera o indice natural;
3. a soundness termina em igualdade no tipo S.
```

A primeira é sustentada pela estrutura de quatro campos e pela ausência
de `Fintype`. A segunda, por `tableIndex_val`, que é `rfl`. A terceira,
por `encode_injective`, a última seta do DAG.

## Correções de metadados deste ciclo

```text
META-ENC-001  contagem da API alinhada a lista: 14 -> 15
META-ENC-002  chaves duplicadas do item normalizadas, valores identicos
META-ENC-003  ACHADO NOVO, fora da frente, nao alterado
```

`META-ENC-003` registra que `ENG-FINITE-STATE-RUNTIME-001.tests_planned`
tem duas ocorrências com valores **divergentes** (`9` e `8`) na fila. É
frente encerrada; nada foi tocado, e o caso aguarda gate corretivo.

## Estado de encerramento

```yaml
work_status: VERIFIED
specification_status: APPROVED
specification_review: APPROVED
formalization_status: VERIFIED
result_review: APPROVED
extension_status: NOT_AUTHORIZED

reencoding_invariance_status: NOT_AUTHORIZED
extraction_status: NOT_AUTHORIZED
cli_status: NOT_AUTHORIZED
parser_status: NOT_AUTHORIZED
integration_status: NOT_AUTHORIZED
external_abstraction_correctness: DEFERRED
```

## Condições de reabertura

A frente só volta a ser tocada por gate explícito. **Nada** do seguinte
está autorizado por consequência deste encerramento:

```text
extracao; CLI; parser; JSON; rede; integracao;
invariancia sob recodificacao;
ENG-FINITE-STATE-ENCODING-002;
extracao do runtime adapter; Floyd.
```

## A separação que não pode ser apagada

```text
a frente certifica a correspondencia entre um SISTEMA FORMAL TIPADO e
sua tabela construida.

ela NAO certifica a origem externa desse sistema.
```

## Valor registrado

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
```

Codificar um tipo finito como `Fin n` é rotina desde os anos 1950. O que
a frente acrescenta é a prova de que a codificação **preserva a
dinâmica** ao longo de uma cadeia cujas duas pontas já eram teoremas.
