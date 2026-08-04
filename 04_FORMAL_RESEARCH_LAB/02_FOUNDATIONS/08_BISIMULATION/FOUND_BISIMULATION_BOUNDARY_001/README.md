---
document_id: FOUND-BISIMULATION-BOUNDARY-001-README
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
status: READY
specification_status: READY_FOR_REVIEW
formalization_status: NOT_STARTED
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SEMANTIC_FOUNDATION
---

# FOUND-BISIMULATION-BOUNDARY-001

**Deterministic Bisimulation and the Limits of Cycle Reflection**

## A pergunta herdada

`ABS-GAP-015` ficou aberto com uma suspeita explícita: bissimulação
seria mais forte que semiconjugação e talvez refletisse ciclos.

## A resposta

```text
Em sistemas deterministicos totais, a bissimulacao funcional
COINCIDE com a semiconjugacao.

Logo BOOL_TO_UNIT ja e uma bissimulacao — e sobrejetiva — e
mesmo assim nao reflete ciclos.

O que separa nao e bissimulacao. E injetividade sobre a orbita.
```

## Por que zig e zag colapsam

```text
zag:  dado c, exibir c' com stepC c = c' e abstract c' = stepA (abstract c)

testemunha obrigatoria: c' = stepC c

obrigacao restante:     abstract (stepC c) = stepA (abstract c)
                        que e exatamente o zig
```

Determinismo e totalidade não deixam escolha de testemunha. Sem escolha,
não há informação nova.

## Documentos

```text
SPECIFICATION_DECISION.md      decisoes congeladas
DATA_MODEL.md                  Simulates, Reflects, Bisimulation
COLLAPSE_THEOREM.md            bisimulation_iff_semiconj
COUNTEREXAMPLE_CONSEQUENCE.md  BOOL_TO_UNIT ja e bissimulacao
SCOPE_BOUNDARY.md              onde o colapso NAO vale
PUBLIC_API_SPECIFICATION.md    API publica candidata
PROBE_RESULT.md                evidencia do probe
TEST_PLAN.md                   testes planejados
GAP_REGISTER.yaml              gaps
STOP_CONDITIONS.md             stop conditions
CLAIM_BOUNDARY.md              wording permitido e proibido
STATUS.yaml                    estado da frente
```

## O documento mais importante

[`SCOPE_BOUNDARY.md`](SCOPE_BOUNDARY.md). O resultado é um **colapso**, e
colapsos são exatamente o tipo de teorema que se generaliza
indevidamente. Fora do recorte determinístico total e funcional, zig e
zag não colapsam e nada aqui se aplica.
