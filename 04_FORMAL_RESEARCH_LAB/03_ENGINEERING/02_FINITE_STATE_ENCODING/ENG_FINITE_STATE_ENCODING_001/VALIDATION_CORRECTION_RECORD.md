---
document_id: ENC-VALIDATION-CORRECTION-RECORD
deviation_id: ENC-VAL-001
classification: NON_MATHEMATICAL_VALIDATION_FAILURE
---

# Registro de correção de validação

```yaml
deviation_id: ENC-VAL-001
previous_review_commit: 751cef8d0280c8d07643a7d5d9d1bdbd9f849f8d

problem:
  mandatory axiom probe exited with code 1

cause:
  intentionally failing negative experiments shared the same file

mathematical_impact: NONE
api_impact: NONE
computability_impact: NONE
claim_impact: NONE

correction:
  - clean main probe executed with exit 0
  - clean axiom probe executed with exit 0
  - negative experiments retained only as documentation

governance_rule:
  mandatory validation probes must contain only declarations
  expected to compile successfully
```

## O que aconteceu

O gate de revisão exigia, literalmente:

```text
probe de axiomas: PASS
probes compilarem integralmente
```

e o arquivo `/tmp/FiniteStateEncodingAxiomProbe.lean` terminou com
`exit 1`.

As três falhas eram **experimentos negativos intencionais** sobre a rota
definicional descartada, e a revisão os tratou como medição válida — o
que eles são. O erro não foi a medição: foi tê-la colocado **dentro do
arquivo classificado como auditoria obrigatória bem-sucedida**.

```text
um experimento negativo nao pode compartilhar arquivo com uma
validacao obrigatoria cujo contrato exige exit 0.
```

## O que **não** aconteceu

```text
nenhum contraexemplo matematico foi encontrado;
nenhuma declaracao da especificacao deixou de compilar;
nenhuma decisao de API foi contestada;
nenhuma pegada axiomatica mudou;
nenhuma claim foi afetada.
```

O conteúdo continuava correto. O que estava errado era o **contrato do
artefato de validação**, e um relatório que declara `PASS` sobre um
processo com `exit 1` é um relatório que não pode ser auditado.

## Correção aplicada

```text
probe principal   /tmp/FiniteStateEncodingReviewProbe.lean   exit 0
probe de axiomas  /tmp/FiniteStateEncodingAxiomProbe.lean    exit 0
```

O probe de axiomas passou a conter **somente** declarações que compilam,
`#check` e `#print axioms`. Nenhuma declaração destinada a falhar.

Os experimentos negativos permanecem registrados em
`AXIOM_FOOTPRINT_REVIEW.md`, como **documentação**, e não são
reexecutados.

## Efeito sobre a decisão A

```text
A decisao A da revisao permanece CORRETA no merito, e passou a ser
INTEGRALMENTE VALIDA somente apos este gate corretivo.
```

Entre `751cef8` e o commit deste gate, a autorização de formalização
esteve **suspensa** — presente no allowlist, não executável.
