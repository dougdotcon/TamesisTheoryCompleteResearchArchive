---
document_id: FSG2-CLOSURE-RECORD
work_item_id: FOUND-SEMIGROUP-002
closed_at: 2026-07-31
reviewed_commit: b4ce2551cd9f3588030fc7281d7f8c7aa624bac3
decision: A_FOUND_SEMIGROUP_002_RESULT_REVIEW_APPROVED
extension_status: NOT_AUTHORIZED
---

# FOUND-SEMIGROUP-002 — Registro de encerramento

## Estado final

```yaml
active_work_item: FOUND-SEMIGROUP-002
work_status: VERIFIED
result_review: APPROVED
extension_status: NOT_AUTHORIZED
current_blocker: null
authorized_action: NO_ACTION_AUTHORIZED
```

`NO_ACTION_AUTHORIZED` é uma **trava**, não uma autorização de execução.
Nenhum gate pode agir sob ela.

## O que fica como fundação reutilizável

```text
05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics/
  Reachability.lean          Camada A: alcancabilidade
  Invariants.lean            Camada A: invariantes
  EventualPeriodicity.lean   Camada C: funcao sobre tipo finito
  MonoidIteration.lean       Camada B: corolario derivado
  Counterexamples.lean       CE-001..CE-005
  Audit.lean                 registro de assinaturas
FiniteDynamics.lean          agregador

Tests/FoundSemigroup002.lean
Tests/FoundSemigroup002Counterexamples.lean
Tests/FoundSemigroup002InstanceAudit.lean
```

**17 declarações públicas**, 1 auxiliar `private`, 11 instâncias — todas
confinadas a contraexemplos.

## Propriedades verificadas na revisão

```text
casa dos pombos usada UMA unica vez;
minimalPeriod NUNCA usado (4 mencoes, todas em comentario);
nenhuma instancia global de Preorder;
zero instancias no nucleo matematico;
nenhum conflito de instancia; umbrella nao ambiguo;
assinaturas minimas: sem DecidableEq X, Fintype M, Group M;
card X = 0 nao produz contradicao escondida (x : X eh premissa);
nenhuma dependencia de Nonempty ou Inhabited;
nenhuma dependencia de legado.
```

## Limites que permanecem vinculantes

```yaml
mathematical_novelty: NONE
```

Três documentos vinculantes:

| Documento | Trava |
|---|---|
| `RESULT_BOUNDARY.md` | o que foi e o que não foi provado |
| `C3_BOUNDARY.md` | leitura correta de "propriedades de C3 falham em geral" |
| `NOVELTY_BOUNDARY.md` | proibições de vocabulário |

### A leitura de C3, repetida por ser a mais fácil de perder

```text
CORRETO:
Para CADA UMA das quatro propriedades existe uma acao finita na qual
ela falha.

ERRADO:
As quatro falham SIMULTANEAMENTE em toda acao finita.
```

### Independência dos contraexemplos

```text
Nao foi provado que todas essas falhas ocorrem simultaneamente em uma
unica acao.

Nao foi provado que todas as acoes finitas exibem essas falhas.
```

Os cinco modelos são independentes entre si: `CE-003` sequer tem monoide,
e `CE-004` reutiliza o monoide de `CE-001` sobre outro espaço de estados.

## O que **não** está autorizado

```text
FOUND_SEMIGROUP_003
FOUND_SEMIGROUP_002_EXTENSION
TRI_BRIDGE
TDTR_BRIDGE
PHYSICS_EXECUTION
UNIVERSAL_DYNAMICS
```

Nenhuma dessas entradas foi adicionada ao allowlist, e nenhuma pode ser
adicionada sem gate próprio.

## Gaps que permanecem abertos

```text
FSG2-GAP-004b   decomposicao canonica         OPEN_DEFERRED
FSG2-GAP-007    negativa sem contraexemplo    OPEN_DEFERRED
FSG2-GAP-009    bibliografia primaria         OPEN_BIBLIOGRAPHIC
```

Encerrar a frente **não fecha** nenhum deles.

## Próximo passo

```text
Aguardar um gate separado de revisao de portfolio para selecionar o
proximo work item. Nenhuma extensao de FOUND-SEMIGROUP-002 esta
autorizada.
```

## Situação das duas frentes do laboratório

```text
FOUND-SEMIGROUP-002   VERIFIED / APPROVED   fundacao formal reutilizavel
RH-NOGO-001           FROZEN_PARTIAL_RESULT congelado, NAO descartado
```

Nenhum arquivo de `RH-NOGO-001` foi tocado nesta revisão.
