---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-RESULT-REVIEW
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
review_start_head: de1b8a9e8a57fb48f11a229e8ea96d747889a2a5
decision: FOUND_FINITE_STATE_ABSTRACTION_001_RESULT_REVIEW_APPROVED
---

# Revisão de resultado

Auditoria da implementação existente, **sem ampliar a matemática**.

## Reexecução independente no commit revisado

```text
lake build                REAL_BUILD_EXIT=0, 8767 jobs, 0 erros reais
auditoria umbrella        REAL_EXIT_CODE=0, 0 erros
contagem derivada         7 declaracoes publicas
tokens proibidos          0
typeclasses no nucleo     0
pytest                    21 passed
labctl validate           PASS
duplicatas YAML           0 em 57 arquivos
```

Nada foi aceito por herança do gate anterior: build, auditoria e
contagens foram reexecutados aqui.

## Os quatorze itens de conferência

| # | Item | Verdito |
|---|---|---|
| 1 | identificador único | CONFIRMADO |
| 2 | API pública correta | CONFIRMADO |
| 3 | `Semiconj` orientada corretamente | CONFIRMADO |
| 4 | soundness observacional termina em `A` | CONFIRMADO |
| 5 | soundness refletida exige `OrbitSeparating` | CONFIRMADO |
| 6 | completeness abstrata não promete reflexão | CONFIRMADO |
| 7 | `BOOL_TO_UNIT` correto | CONFIRMADO |
| 8 | falha de `OrbitSeparating` provada | CONFIRMADO |
| 9 | nenhuma typeclass desnecessária | CONFIRMADO |
| 10 | nenhum código anterior modificado | CONFIRMADO |
| 11 | claim limitada | CONFIRMADO |
| 12 | gaps honestos | CONFIRMADO |
| 13 | zero duplicatas YAML | CONFIRMADO |
| 14 | zero contagens manuais divergentes | CONFIRMADO |

## Detalhe dos itens não triviais

### 2 — API pública

Contagem **derivada do código** por varredura dos quatro módulos
centrais: `1` estrutura, `2` definições, `4` teoremas. Total `7`, igual
ao congelado. Nenhuma declaração pública extra escapou para a
biblioteca.

### 4 e 5 — a fronteira

```text
observational_sound   conclui  abstraction.abstract (…) = abstraction.abstract (…)
reflected_sound       recebe   OrbitSeparating …    conclui  stepC^[…] start = stepC^[…] start
```

A diferença entre as duas linhas é o resultado da frente. Ambas lidas
por `#check` no `Audit.lean`, dentro do build.

### 10 — frentes encerradas

```text
arquivos alterados sob:
  Engineering/FiniteStateEncoding/   0
  Engineering/FiniteStateRuntime/    0
  Foundations/CycleDetection/        0
  Foundations/FunctionalGraphs/      0
  Foundations/Semigroups/            0
  Foundations/FiniteDynamics/        0
  RHNogo/                            0
```

Verificado por script sobre o índice do git nos três commits da frente.
Os únicos arquivos preexistentes tocados são `TamesisLab.lean` e
`TamesisLab/Foundations.lean`, e apenas com linhas de `import`.

### 12 — gaps honestos

`15` fechados, `5` abertos. Dois merecem registro explícito:

- `ABS-GAP-019` foi fechado **por delimitação de escopo**, não por
  revisão bibliográfica. Está marcado para reabertura se alguma
  reivindicação de prioridade aparecer.
- `ABS-GAP-017` é **permanentemente aberto**: nenhuma frente formal
  decide se um sistema externo real foi corretamente modelado.

## Auditoria umbrella

Criada e executada explicitamente, fora de `TamesisLab.lean` para não
criar ciclo. Ela alcança as sete declarações pela raiz e instancia uma
abstração **muitos-para-um** (`Fin 4 → Fin 2` pela paridade) na qual a
recorrência observacional vale e a concreta falha.

## Claim

Uma única claim promovida,
`CERTIFIED-FINITE-STATE-ABSTRACTION-FORMAL-001`, com
`evidence_level: F`, `mathematical_novelty: NONE`,
`algorithmic_novelty: NONE`. Wording conferida contra a lista permitida
e contra a lista proibida.

```text
ledger antes   22
ledger depois  23
```

## Decisão

```text
FOUND_FINITE_STATE_ABSTRACTION_001_RESULT_REVIEW_APPROVED
```

## Ressalva de independência

Especificação, revisão, formalização e esta revisão de resultado foram
executadas pelo mesmo agente, em sessões consecutivas. Nenhuma delas
substitui revisão externa. O que sustenta o resultado é o que foi
**medido e reexecutado**: `lake build` com código de saída confiável,
`#print axioms`, contagens derivadas por script e testes que compilam.
