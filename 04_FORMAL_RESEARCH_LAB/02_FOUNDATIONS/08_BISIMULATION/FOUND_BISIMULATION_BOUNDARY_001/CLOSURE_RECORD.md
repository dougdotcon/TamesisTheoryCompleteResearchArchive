---
document_id: FOUND-BISIMULATION-BOUNDARY-001-CLOSURE-RECORD
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
work_status: VERIFIED
result_review: APPROVED
extension_status: NOT_AUTHORIZED
---

# Registro de encerramento

## Estado final

```yaml
active_work_item: FOUND-BISIMULATION-BOUNDARY-001
work_status: VERIFIED
specification_status: APPROVED
specification_review: APPROVED
formalization_status: VERIFIED
result_review: APPROVED
extension_status: NOT_AUTHORIZED

relational_bisimulation_status: NOT_AUTHORIZED
nondeterministic_systems_status: NOT_AUTHORIZED
labelled_actions_status: NOT_AUTHORIZED
coinduction_status: NOT_AUTHORIZED
quotient_status: NOT_AUTHORIZED
extraction_status: NOT_AUTHORIZED

authorized_action: PORTFOLIO_REVIEW_REQUIRED
```

## Os quatro gates

```text
6163bd5  lab: select deterministic bisimulation boundary
a51fc14  lab: specify deterministic bisimulation boundary
c2247d6  lab: review deterministic bisimulation specification
25e85ff  lab: formalize deterministic bisimulation boundary
(este)   lab: review deterministic bisimulation result
```

Um commit por gate, mais o commit de seleção.

## A força exata do que foi provado

```text
Para sistemas deterministicos TOTAIS e bissimulacao FUNCIONAL,
o zag e consequencia do zig, porque stepC sendo funcao total
impoe a testemunha.

Logo BOOL_TO_UNIT ja e uma bissimulacao, e sobrejetiva, e o
ciclo abstrato continua espurio.
```

## O que **não** foi provado

```text
que bissimulacao seja semiconjugacao EM GERAL
que bissimulacao seja inutil
que sistemas nao deterministicos se comportem assim
qualquer coisa sobre bissimulacao relacional, rotulos ou coinducao
```

## O quadro que a frente completa

```text
semiconjugacao             NAO reflete
bissimulacao funcional     NAO reflete   (e a mesma coisa)
bissimulacao sobrejetiva   NAO reflete
OrbitSeparating            REFLETE
injetividade global        REFLETE  (forte demais)
```

Reforçar a **relação de simulação** não atravessa a fronteira entre
observar e refletir. O que atravessa é **separação de estados**.

## Números finais, derivados

```text
arquivos Lean criados            8
agregadores modificados          2  (apenas imports)
declaracoes publicas             8  (3 definicoes, 5 teoremas)
declaracoes TEST_ONLY            2
declaracoes sem pegada          10 de 10
testes                           8
gaps fechados                    5 de 10
stop conditions declaradas      10
stop conditions disparadas       0
claims promovidas                1
ledger de claims                24
lake build                       exit 0, 8775 jobs
duplicatas YAML                  0 em 413 arquivos
frentes encerradas modificadas   0
```

## Próxima ação

```text
PORTFOLIO_REVIEW_REQUIRED
```

Nenhuma frente nova está escolhida. Os candidatos herdados são
quocientes (`ABS-GAP-016`, `BIS-GAP-009` correlato) e a bibliografia de
semântica de concorrência (`BIS-GAP-010`), que ficou **deliberadamente
aberta**.
