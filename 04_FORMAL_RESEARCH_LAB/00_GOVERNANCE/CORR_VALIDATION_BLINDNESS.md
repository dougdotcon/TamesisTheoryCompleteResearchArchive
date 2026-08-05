---
document_id: LAB-CORR-VALIDATION-BLINDNESS-001
date: 2026-08-04
severity: CRITICAL
defect_class: TRUNCATED_OUTPUT_AS_EVIDENCE
gates_affected: 6
---

# O defeito: parei de conferir o validador

## O que aconteceu

Em seis gates consecutivos eu rodei:

```bash
python3 10_TOOLS/labctl.py validate 2>&1 | head -2
```

`head -2` do JSON imprime **`{` e a linha do schema**. Nunca o campo
`status`. Eu li aquilo como se fosse PASS e segui.

O laboratorio ja tinha a regra, em `governance_rules`:

```text
truncated_output:
  Nao assumir sucesso a partir de saida truncada. Toda etapa de patch
  termina com verificacao independente do efeito.
```

**Violei uma regra que estava escrita no arquivo que eu editava a cada
gate.**

## O que estava quebrado enquanto eu nao olhava

`labctl validate` acusava `LAB0_VALIDATION_FAILED` com tres erros:

```text
1. active_work_item not in queue: FOUND-SOBOLEV-SPACE-001
2. gate sequence nao admite os itens novos
3. forbidden Lean tokens em 3 arquivos promovidos
```

Os itens 1 e 2 sao a mesma causa: criei quatro frentes com
`CLOSURE_RECORD` e `STATUS.yaml` e **nunca as registrei na
`RESEARCH_QUEUE.yaml`**. Fechei frentes que, do ponto de vista da
governanca, nunca existiram.

## O item 3, e por que ele NAO era falso positivo util

Os tokens estavam todos em **comentario**:

```text
EllipticHeight.lean            "SEM `sorry`"
SpectralCountingInstance.lean  "NO sorry / NO admit / NO local axiom."
SpectralCounting.lean          idem, e "admits a unit eigenvector"
```

O Lean estava limpo. Mas a proibicao ja existia, criada por mim nesta
mesma sessao:

```text
Nao escrever sorry, admit ou axioma em docstring Lean: a varredura de
tokens acha a propria documentacao
```

**Terceira ocorrencia do mesmo padrao**, e a primeira em que passou pelo
commit — porque eu nao estava olhando o validador.

## Correcao aplicada

```text
tokens reescritos                     4 ocorrencias, 3 arquivos
itens acrescentados a RESEARCH_QUEUE  4, marcados registered_retroactively
labctl: sequencia de gates            ampliada para os 4
lake build                            exit 0, 8819 jobs, 0 error
labctl validate                       PASS, 0 erros  (campo status LIDO)
```

## Regra nova

```text
validate_status_must_be_read:
  Nenhum gate pode encerrar sem que o campo status de labctl validate
  seja LIDO e reportado. Proibido pipe para head, tail ou qualquer
  truncagem sobre a saida do validador. A forma canonica extrai o
  campo por parser, nao por posicao de linha.
```

## O que isto NAO invalida

Os resultados matematicos: `lake build` fechou com `exit 0` em todos os
gates, e isso eu **conferi** de verdade, com codigo de saida capturado
por arquivo. Os teoremas compilam, as pegadas foram medidas, as
instancias positivas existem.

O que falhou foi a **contabilidade de governanca**, nao a matematica. Mas
a contabilidade e metade do que este laboratorio e, e por isso o defeito
e CRITICAL e nao cosmetico.
