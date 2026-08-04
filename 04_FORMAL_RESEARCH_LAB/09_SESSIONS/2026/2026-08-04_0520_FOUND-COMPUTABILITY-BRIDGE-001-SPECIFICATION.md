---
session_id: 2026-08-04_0520_FOUND-COMPUTABILITY-BRIDGE-001-SPECIFICATION
started_at: 2026-08-04T05:20:30-03:00
ended_at: 2026-08-04T05:20:30-03:00
agent: claude-opus-5
git_commit_before: 909f7e06d52c172b49f908c22c3d32492c50bd7d
git_commit_after: PENDING
active_work_item: FOUND-COMPUTABILITY-BRIDGE-001
authorized_action: FOUND_COMPUTABILITY_BRIDGE_001_SPECIFICATION_PREPARATION_AUTHORIZED
result_status: SPECIFICATION_READY_FOR_REVIEW
claims_changed: []
gaps_opened: 9
gaps_closed: 0
---

## Objetivo autorizado

Especificar `FOUND-COMPUTABILITY-BRIDGE-001` — responder, com assinaturas
que compilem, as cinco perguntas registradas em `ATTACK_READINESS.md`.

## Estado inicial

```text
HEAD                 909f7e06d52c172b49f908c22c3d32492c50bd7d
canonical_commit     f46568d2e61d3fcce03dab5d923d2c808a80eecc
active_work_item     FOUND-COMPUTABILITY-BRIDGE-001
work_status          SCOPED
specification        inexistente
arvore de trabalho   limpa
```

## Trabalho executado

Um probe descartável, `/tmp/ProbeCB1.lean`, com 28 declarações. Nenhum
arquivo da árvore versionada foi tocado durante a elaboração
(`git_dirty=0` conferido no mesmo script que capturou o código de saída).

### As cinco respostas

```text
2. CertifiedFiniteEncoding induz Primcodable?   SIM, direto
1. analyzeEncodedSystem e Computable?           SIM, por FINITUDE
3. o detector e Primrec, nao so Computable?     SIM, por FINITUDE
4. baseIndex + period <= n e cota de recursos?  NAO, e cota do CERTIFICADO
5. custo formalizavel sem modelo de maquina?    NAO neste nivel
```

### O resultado central, que é negativo

`Primrec.dom_finite` prova que **toda** função que sai de um tipo finito
codificável é primitiva recursiva, sem consultar a função. Logo:

```text
primrec_analyzeEncodedSystem   corolario de UMA LINHA
```

A classificação `Primrec`/`Computable` é **constante** sobre o domínio do
laboratório. Ela não distingue a busca limitada de uma tabela de
consulta, e não pode servir de degrau para classe de complexidade
nenhuma.

Isto é entrega, não fracasso: era exatamente o que precisava ser sabido
antes de qualquer conversa sobre `PVSNP-PHYS-001`.

### Onde a pergunta tem conteúdo

`UniformPrimrecStatement : Prop := Primrec₂ analyzeTransitionTable`
elabora. Sobre `RawTransitionTable × Nat` o domínio é infinito e
`dom_finite` não se aplica. A prova **não foi tentada** — `CB-GAP-001`,
deliberadamente aberta.

Optou-se por `def : Prop` em vez de `sorry` ou axioma local: o enunciado
fica verificadamente escrevível sem que nada seja afirmado.

### A instância positiva

Regra `positive_instance_required`, nascida do defeito de vacuidade de
`FOUND-MONOVARIANT-DESCENT-001`:

```text
tipo             Bool          habitado
n                2             > 0
verificacao      decide        avaliacao, nao hipotese
caso vacuo       isEmpty_of_encoding_zero, teorema publico
```

`CertifiedFiniteEncoding S 0` força `IsEmpty S`. A armadilha está
nomeada em teorema público em vez de descoberta por revisão posterior.

## Correções de método registradas

### Varredura de axiomas incompleta, corrigida antes do commit

A primeira medição de pegada cobriu **20** das 28 declarações e seria
publicada em `STATUS.yaml` como se fosse integral. Refeita para 28,
cobertura `FULL`. É o mesmo padrão de defeito — contagem agregada
publicada sem cobrir todas as entradas — que a regra `aggregate_counts`
já existia para impedir; desta vez foi pego antes do commit.

### Relatório de sessão ausente em oito gates

`AGENTS.md` passo 7 exige relatório em `09_SESSIONS/`. O último existente
é `2026-08-03_2210`. Os gates de invariantes, monovariantes, a revisão de
portfólio, a correção de vacuidade e a avaliação de prontidão não
produziram um. Registrado como observação; **nada é reescrito
retroativamente**, o que está proibido.

## Verificações

```text
probe exit                      0
linhas error:                   0
linhas warning:                 0
arvore versionada tocada        nao  (git_dirty=0)
declaracoes                     28   derivadas por script, PARTITION_OK
pegada axiomatica               28/28 medida, cobertura FULL
frentes encerradas modificadas  0
```

## Estado final

```text
work_status          READY
specification        READY_FOR_REVIEW
authorized_action    FOUND_COMPUTABILITY_BRIDGE_001_SPECIFICATION_REVIEW_AUTHORIZED
lacunas abertas      9
condicoes de parada  12 declaradas, 0 disparadas
claims promovidas    0
```

## O que NÃO foi feito

```text
0 arquivos Lean permanentes
0 lake build
0 classes de complexidade
0 afirmacoes de custo
0 problemas de milenio atacados
```
