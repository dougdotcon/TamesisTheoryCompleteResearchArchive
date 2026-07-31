---
session_id: 2026-07-31-PORTFOLIO-REVIEW-CYCLE-DETECTION
date: 2026-07-31
gate: PORTFOLIO_REVIEW
authorized_action: PORTFOLIO_REVIEW_AUTHORIZED
agent: claude-opus-5
commit_before: 49924c3fe9b5cc2eab0cdea12c3554fc537c051d
decision: A_PORTFOLIO_REVIEW_APPROVED_CYCLE_DETECTION_SELECTED
selected_work_item: FOUND-CYCLE-DETECTION-001
lean_files_created: 0
---

# Sessão — Revisão de portfólio · detecção executável de ciclos

Seleção da próxima fundação formal após o encerramento de
`FOUND-FUNCTIONAL-GRAPH-001`. **Nenhum arquivo Lean. Nenhuma prova.
Nenhum algoritmo implementado. Nenhum `lake build`.**

## Preflight

```text
HEAD                  49924c3fe9b5cc2eab0cdea12c3554fc537c051d
árvore                limpa
processos Lean/Lake   nenhum
cat-file -e           0
merge-base ancestor   0   (igualdade aceita)
canonical_commit      3f6d7e7 -> 49924c3
```

Entrada com `authorized_action: PORTFOLIO_REVIEW_REQUIRED` — trava, não
autorização. A emissão do gate abriu, temporariamente,
`PORTFOLIO_REVIEW_AUTHORIZED`, que já constava do allowlist; nenhuma
entrada nova foi necessária para isso.

## Frentes encerradas

`FOUND-FUNCTIONAL-GRAPH-001` e `FOUND-SEMIGROUP-002` seguem `VERIFIED`,
com revisão aprovada e `extension_status: NOT_AUTHORIZED`; `RH-NOGO-001`
segue `FROZEN_PARTIAL_RESULT`, não autorizada, sem execução, camada
concreta diferida. Nenhum `extension_status` foi alterado, nenhum módulo
matemático foi tocado.

## Auditoria do portfólio

Seis itens não executados foram reavaliados com os nove campos exigidos.
Todos rejeitados; nenhuma pesquisa matemática das frentes rejeitadas foi
iniciada.

| Item | PoC 30 dias | Motivo |
|---|---|---|
| `NS-PRESSURE-001` | NÃO | Clay; Mathlib não sustenta a camada de EDP |
| `PVSNP-PHYS-001` | NÃO | vizinho de Clay; valor em definições não verificáveis |
| `YM-LIMIT-001` | NÃO | custo `very_high`; QFT construtiva ausente |
| `HODGE-CDK-001` | NÃO | custo bibliográfico `very_high`; sem produto formal pequeno |
| `BSD-HYP-MATRIX-001` | NÃO | produto essencialmente bibliográfico |
| `TOE-INTERFACE-001` | NÃO | depende de `RH-NOGO-001`, congelada — dependência **bloqueante** |

## Alvo selecionado

```yaml
work_item: FOUND-CYCLE-DETECTION-001
title: "Executable Cycle Detection for Finite Deterministic Systems"
track: FOUNDATIONS
work_status: SCOPED
mathematical_novelty: NONE
research_role: FORMAL_ALGORITHM_FOUNDATION
```

**Duplicata: não encontrada.** Zero ocorrências de `CYCLE-DETECTION` ou
`detectCycle` como work item ou definição. Floyd e Brent aparecem em três
documentos — e nos três como material **declarado fora de escopo**:
`KNOWN_RESULTS_MATRIX.md` e `REUSE_MATRIX.md` de `FOUND-SEMIGROUP-002`, e
`REUSE_MATRIX.md` de `FOUND-FUNCTIONAL-GRAPH-001`. O novo item executa
exatamente o que as duas frentes anteriores registraram como não feito.

Nenhum dos cinco critérios de rejeição do alvo ocorreu.

## A lacuna atacada

O fechamento anterior provou que o ciclo existe. Não entregou algoritmo
executável, nem `μ`, nem `λ`, nem ponto de entrada, nem lista do ciclo,
nem certificado computável — porque `Function.periodicOrbit` é
**noncomputável**. Essa distância é o escopo da nova frente.

## Planejamento preliminar

Estrutura candidata `CycleDetectionResult` com `entryIndex`, `period` e
`entryPoint`, e seis invariantes candidatos. **Não congelada** — a
especificação decidirá se armazena também a lista do ciclo ou
certificados (`CD-GAP-002`).

Algoritmos comparados: Floyd, Brent e tabela visitada.

```text
PRIMARY:            FLOYD_WITH_FUEL
REFERENCE_BASELINE: VISITED_TABLE
DEFERRED:           BRENT
```

O baseline por tabela visitada tem papel duplo: correção mais fácil de
provar e **oráculo** para comparar contra Floyd nos casos de teste.
Nenhum dos três foi implementado.

Risco principal registrado: **terminação**. Cinco estratégias a avaliar, e
quatro camadas que a especificação deve manter separadas — terminação do
programa, correção matemática, limites de complexidade e equivalência com
a API proposicional.

## Distinção que evita erro de categoria

`DecidableEq X` é sobre **estados**. `periodicOrbit` vive em `Cycle X`, e
nenhuma decidibilidade sobre `Cycle X` é assumida, requerida ou
construída. A ponte com os resultados anteriores é **proposicional**: o
`entryPoint` calculado pertence a `periodicPts`, e sua `periodicOrbit` é
a órbita única do componente.

Registrado também que `FOUND-FUNCTIONAL-GRAPH-001` demonstrou que
`DecidableEq X` **não** é necessária na camada proposicional. Aqui a
situação muda de natureza, mas continua sendo hipótese a **confirmar**,
não a presumir (`CD-GAP-004`).

## Minimalidade — não autorizada

Minimalidade de `μ`, minimalidade de `λ`, complexidade assintótica
formal, lista completa da bacia e enumeração de componentes globais
permanecem **não autorizadas**. Floyd *tende* a produzir valores mínimos;
tender não é provar.

## Casos de teste e lacunas

Seis casos de teste preliminares (`CD-CE-001` a `CD-CE-006`), com valores
declarados **candidatos** — nenhum contrato de minimalidade foi escolhido
ainda. Dezesseis lacunas abertas (`CD-GAP-001` a `CD-GAP-016`), nenhuma
fechada.

## Desvios de governança

Três edições mínimas e literais em `10_TOOLS/labctl.py`, sem wildcard:

- `DEC-014` — `FOUND-CYCLE-DETECTION-001` no conjunto de
  `active_work_item` permitidos;
- `DEC-015` — nova checagem: o item não pode ficar ativo antes de
  `FOUND-FUNCTIONAL-GRAPH-001` estar `VERIFIED`;
- `DEC-016` — entrada literal
  `FOUND_CYCLE_DETECTION_001_SPECIFICATION_PREPARATION_AUTHORIZED` no
  allowlist.

`PORTFOLIO_REVIEW_AUTHORIZED` já existia — nenhuma entrada foi criada
para ele.

## Validação

```text
pytest                  PASS
labctl validate         PASS
canonical_commit_check  PASS
Lean files created      0
Lean proofs created     0
lake build executed     NO
algorithm implemented   NO
claims promoted         0
physics claims          0
legacy files modified   0
RH-NOGO-001 touched     0
FOUND-SEMIGROUP-002     0 arquivos matemáticos
FOUND-FUNCTIONAL-GRAPH-001  0 arquivos matemáticos
whitespace              WHITESPACE_EOF_AUDIT_PASS
```

A auditoria de whitespace rodou sob `set -euo pipefail`, de modo que uma
falha interromperia o gate antes do commit. Nenhum `commit --amend` foi
usado.

## Estado final

```text
active_work_item    FOUND-CYCLE-DETECTION-001
work_status         SCOPED
current_blocker     null
authorized_action   FOUND_CYCLE_DETECTION_001_SPECIFICATION_PREPARATION_AUTHORIZED
```

Formalização, extração de código e integração com sistemas reais
permanecem **não autorizadas**.

## Próxima ação única

Preparar a especificação de um algoritmo executável e formalmente correto
para detectar a cauda e o ciclo de uma trajetória determinística finita.
