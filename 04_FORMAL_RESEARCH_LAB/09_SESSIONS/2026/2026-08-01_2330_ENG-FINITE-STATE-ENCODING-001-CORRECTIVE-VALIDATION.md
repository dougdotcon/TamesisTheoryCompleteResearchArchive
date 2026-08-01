---
session_id: 2026-08-01-ENG-FINITE-STATE-ENCODING-001-CORRECTIVE-VALIDATION
date: 2026-08-01
gate: ENG_FINITE_STATE_ENCODING_001_CORRECTIVE_REVIEW_VALIDATION
authorized_action: ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW_AUTHORIZED
agent: claude-opus-5
commit_before: 751cef8d0280c8d07643a7d5d9d1bdbd9f849f8d
deviation_id: ENC-VAL-001
decision: A_ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW_APPROVED
lean_files_created: 0
---

# Sessão — correção da validação da revisão

## O defeito

```text
Exigencia:  probe de axiomas: PASS; probes compilarem integralmente
Reportado:  FiniteStateEncodingAxiomProbe.lean -> exit 1
```

As três falhas eram experimentos negativos intencionais sobre a rota
definicional descartada. A medição estava certa; o **lugar** estava
errado.

```text
um experimento negativo nao pode compartilhar arquivo com uma
validacao obrigatoria cujo contrato exige exit 0.
```

Um relatório que declara `PASS` sobre um processo com `exit 1` não é
auditável — e isso vale mesmo quando se sabe exatamente por que ele
falhou. A classificação correta do evento não é "erro matemático", e sim
`NON_MATHEMATICAL_VALIDATION_FAILURE`.

## Preflight

```text
HEAD                      751cef8d0280c8d07643a7d5d9d1bdbd9f849f8d
commits desde 2066edc     1
arvore                    limpa
processos                 nenhum
canonical_commit          2066edc, PRESERVADO
```

`751cef8` **não** foi promovido a canônico neste gate: o commit da
revisão não estava integralmente encerrado enquanto o desvio existisse.

## Suspensão explícita

Durante o gate, o estado foi movido para:

```text
specification_status              READY_FOR_REVIEW_CORRECTION
specification_review              CORRECTIVE_VALIDATION_REQUIRED
current_blocker                   ENC-VAL-001
authorized_action                 ..._SPECIFICATION_REVIEW_AUTHORIZED
formalization_authorization_state SUSPENDED_PENDING_ENC_VAL_001
```

A autorização de formalização **não** foi removida do allowlist. Ela foi
tratada como suspensa — presente, não executável. A transição foi
aplicada e **verificada por script** antes de qualquer outra coisa.

## Os dois probes limpos

```text
FiniteStateEncodingReviewProbe.lean   exit 0, 30 s, 0 erros
FiniteStateEncodingAxiomProbe.lean    exit 0,  3 s, 0 erros
```

O probe de axiomas passou a conter **somente** declarações que compilam,
dezesseis `#check` e trinta `#print axioms`. Zero declarações destinadas
a falhar — e o próprio `exit 0` é a prova disso.

`grep` de tokens proibidos nos dois arquivos: saída vazia, código `1`.
`sorryAx`: ausente. Axiomas locais: ausentes.

## Nada mudou na matemática

```text
estrutura de quatro campos          inalterada
decode_encode / encode_decode       papeis inalterados
dois pontos de transporte           inalterados
tableIndex_val por rfl              inalterado
tableIndex_semiconj principal       inalterado
soundness terminando em S           inalterada
completeness sem pre-condicoes      inalterada
20 lacunas, 21 claims               inalteradas
```

A pegada axiomática foi reconfirmada e é **idêntica**:

```text
encode_injective   does not depend on any axioms
encodedStep        does not depend on any axioms
buildTransitionTable   primeira a carregar os tres, pelo campo closed
```

## A regra que fica

```text
Experimentos negativos, provas exploratorias destinadas a falhar e
testes de impossibilidade nao podem compartilhar arquivo com probes
obrigatorios cujo contrato exige exit 0.

Validacoes obrigatorias terminam com codigo de saida zero.

Resultados negativos sao preservados em documentacao, nunca
reexecutados como validacao.

Um processo Lean com exit 1 nunca eh evidencia de PASS.
```

Entrou em `governance_rules` e nas proibições vivas do `LAB_STATE.md`.
Os experimentos negativos permanecem em `AXIOM_FOOTPRINT_REVIEW.md`,
como evidência histórica, e nenhum arquivo Lean deliberadamente inválido
foi criado.

## Estado final

```text
work_status                       READY
specification_status              APPROVED
specification_review              APPROVED
formalization_status              NOT_STARTED
current_blocker                   null
authorized_action                 ..._FORMALIZATION_AUTHORIZED
formalization_authorization_state RESTORED_AFTER_ENC_VAL_001
entradas novas no allowlist       0
```

## Próxima ação única

Formalizar. Uma única tabela pública, dois pontos controlados de
transporte, zero escolha clássica produzindo dado executável — agora sem
carregar uma inconsistência de governança para a próxima etapa.
