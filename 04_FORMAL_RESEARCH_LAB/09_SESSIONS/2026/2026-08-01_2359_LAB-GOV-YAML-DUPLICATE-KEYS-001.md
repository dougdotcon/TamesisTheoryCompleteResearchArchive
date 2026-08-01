---
session_id: 2026-08-01-LAB-GOV-YAML-DUPLICATE-KEYS-001
date: 2026-08-01
gate: LAB_GOV_YAML_DUPLICATE_KEYS_001
authorized_action: LAB_GOV_YAML_DUPLICATE_KEYS_CORRECTION_AUTHORIZED
agent: claude-opus-5
commit_before: e9e2ce7e3ba589425942efd5b551cf03570334bc
decision: LAB_GOV_YAML_DUPLICATE_KEYS_CORRECTION_VERIFIED
lean_files_created: 0
lean_files_modified: 0
---

# Sessão — rejeição e normalização de chaves YAML duplicadas

## O problema, dito com precisão

Não era o valor `8` estar possivelmente errado. Era isto:

```python
yaml.safe_load("a: 1\na: 2\n")   ->   {"a": 2}
```

Sem erro, sem aviso, sem rastro. Enquanto um mapa puder ter duas
definições da mesma chave, **a representação textual da governança não
tem semântica unívoca** — e nenhuma revisão de portfólio pode se apoiar
nela.

## O que a varredura integral achou

O relatório anterior falava em três itens, todos na fila. A varredura
completa dos `55` arquivos YAML achou **oito ocorrências em três
arquivos**:

```text
5 identicas, 3 divergentes
```

E as duas divergências novas estavam **fora** da fila, que era o único
lugar onde eu havia olhado:

```text
FOUND_CYCLE_DETECTION_001/STATUS.yaml   extraction_status
    NOT_AUTHORIZED  contra  READY_FOR_FEASIBILITY_AUDIT
ENG_FINITE_STATE_ENCODING_001/STATUS.yaml   documents
    39  contra  65
```

A primeira é a mais séria de todas: o `STATUS.yaml` de uma frente
**encerrada** vinha sendo lido com uma trava **mais fraca** do que a que
a governança de fato mantém. `CLOSURE_RECORD.md` e `LAB_STATE.md` dizem
`NOT_AUTHORIZED`; o parser dizia `READY_FOR_FEASIBILITY_AUDIT`.

Isso não é anedota sobre este gate. É a demonstração de que "auditei os
campos que eu suspeitava" não é auditoria.

## `tests_planned`, resolvido por fonte de verdade

```text
TEST_PLAN.md, front matter    tests: 9
TEST_PLAN.md, secoes          RT-TEST-001 .. RT-TEST-009
STATUS.yaml da frente         tests_planned: 9
fila, linha 505               9    escrita na especificacao
fila, linha 518               8    escrita na formalizacao
portfolio result.json         lista de 8 nomes, ate RT-TEST-008
```

O `8` é a contagem da **seleção**, anterior ao congelamento da
especificação, que acrescentou o nono caso. Valor final: **`9`**.

A frente vizinha confirma a semântica do campo: em
`FOUND-CYCLE-DETECTION-001`, fila, `TEST_PLAN` e `STATUS` dizem `7`, os
três de acordo.

E as contagens que **não** são a mesma coisa, agora separadas por escrito:

```text
selecao                8
especificacao          9    <- tests_planned
formalizacao          10    <- tests_formalized
arquivos .lean         4
teoremas de regressao 22
```

O valor final difere do que o parser usava. Isso é
`NON_MATHEMATICAL_GOVERNANCE_SEMANTIC_CORRECTION` — não cosmética.

## O detector

Percorre a **árvore sintática**, por `yaml.compose_all`. O objeto
carregado não serve: nele a duplicata já morreu.

```text
funcao       detect_duplicate_yaml_keys(path)
varredura    scan_duplicate_yaml_keys(root)
integrado    labctl validate, ANTES do carregamento normal
codigo       DUPLICATE_YAML_KEY
severidade   FAIL, inclusive para valores identicos
escopo       todo .yaml e .yml versionado sob o laboratorio
```

Duplicata idêntica também reprova, e a razão está na política: a
proibição não é sobre o valor, é sobre a ambiguidade da fonte. Que hoje
coincidam não impede que a próxima edição toque só uma das duas — foi
exatamente assim que `META-ENC-003` nasceu.

## Demonstração antes de corrigir

O detector novo foi rodado **contra o repositório sujo**:

```text
duplicate_count_before = 8
META-ENC-003_detected  = YES
```

Só depois os arquivos foram normalizados.

## Depois

```text
55 arquivos, 470 mapas, 320 sequencias
duplicate_occurrences: 0
files_with_duplicates: 0
labctl validate: PASS
pytest: 21 testes   (eram 9)
```

## O que não mudou

```text
claims          22
work items      15
arquivos Lean   0 criados, 0 modificados
teoremas        0 tocados
lake build      nao executado
estados cientificos  0 alterados
```

As três mudanças de valor efetivo são todas de governança:
`tests_planned` `8 → 9`, `extraction_status`
`READY_FOR_FEASIBILITY_AUDIT → NOT_AUTHORIZED`, e `documents` sem
mudança efetiva (`65` já era o valor lido).

## A regra que fica

```text
Uma chave por mapa. Duplicatas identicas tambem proibidas.
"Ultimo valor vence" nao eh semantica de governanca.
A ausencia de erro no parser nao demonstra integridade.

Auditoria declarada integral deve percorrer o conjunto completo.
Uma auditoria parcial nao pode ser descrita como completa.
```

A segunda parte é a que me diz respeito diretamente: foi a terceira vez
que uma verificação minha foi mais estreita do que a afirmação que ela
sustentava.

## Estado final

```text
current_blocker             null
authorized_action           PORTFOLIO_REVIEW_REQUIRED
portfolio_review_status     READY
yaml_duplicate_key_status   VERIFIED_CLEAN
consumed_authorizations     [LAB_GOV_YAML_DUPLICATE_KEYS_CORRECTION_AUTHORIZED]
```

## Próxima ação única

Aguardar o gate de revisão de portfólio. A fila agora tem uma única
leitura possível.
