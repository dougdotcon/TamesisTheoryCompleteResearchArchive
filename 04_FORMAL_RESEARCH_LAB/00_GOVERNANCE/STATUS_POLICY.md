# Política de status

## Work status

```text
UNSCOPED
SCOPED
READY
IN_PROGRESS
BLOCKED
FAILED
REFUTED
PARTIAL_RESULT
VERIFIED
EXTERNALLY_REVIEWED
RETRACTED
ARCHIVED
```

## Evidence level

```text
H = histórico
F = formalizado internamente
C = computacional
O = observacional retrospectivo
P = pré-registrado
E = evidência física prospectiva
I = independente
T = teorema aceito
N = negativo ou inconclusivo
```

## Regras de promoção

Nenhuma ferramenta pode promover automaticamente:

```text
C → T
F → T
P → E
manuscrito → I
```

`VERIFIED` é reservado à verificação do artefato no gate definido, não à
verdade universal da hipótese.

