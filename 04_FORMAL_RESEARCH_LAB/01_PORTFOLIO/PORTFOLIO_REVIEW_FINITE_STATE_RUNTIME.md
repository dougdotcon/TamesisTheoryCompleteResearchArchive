---
document_id: PORTFOLIO-REVIEW-FINITE-STATE-RUNTIME
gate: PORTFOLIO_REVIEW
reviewed_at: 2026-08-01
reviewed_commit: a4907b7cb2b421ccb52fc0262bf276ef2d94f8a9
decision: A_PORTFOLIO_REVIEW_APPROVED_FINITE_STATE_RUNTIME_SELECTED
selected_work_item: ENG-FINITE-STATE-RUNTIME-001
duplicate_found: false
lean_files_created: 0
---

# Revisão de portfólio — ponte para sistemas finitos reais

Revisão após o encerramento de `FOUND-CYCLE-DETECTION-001`. **Nenhum
arquivo Lean, nenhuma prova, nenhum adaptador, nenhum executável, nenhum
`lake build`.**

## O que já existe, com precisão

```text
EXECUTAVEL dentro do Lean
  CycleWitness, cycleCandidates, detectCycleWitness?
  avaliados por #eval em cinco modelos

PROPOSICIONAL
  CycleWitness.Valid e os quatro teoremas de correcao
  Function.periodicPts, EventuallyMeets, periodicOrbit
  toda a camada de FOUND-SEMIGROUP-002 e FOUND-FUNCTIONAL-GRAPH-001

DEPENDE DE TIPOS DEFINIDOS EM COMPILACAO
  o detector inteiro: X : Type*, [Fintype X], [DecidableEq X], f : X -> X
  os cinco modelos de teste sao definidos NO FONTE

FALTA PARA RECEBER DADOS EXTERNOS
  tudo
```

O laboratório tem um programa verificado que **não consegue receber uma
entrada**. Essa é a lacuna que este gate ataca.

## Frentes encerradas — confirmadas

```yaml
FOUND-CYCLE-DETECTION-001:
  work_status: VERIFIED
  specification_status: APPROVED
  formalization_status: VERIFIED
  result_review: APPROVED
  extension_status: NOT_AUTHORIZED
  totalization_status: DEFERRED
  extraction_status: NOT_AUTHORIZED
  optimization_status: NOT_AUTHORIZED
  minimality_status: NOT_AUTHORIZED
  mathematical_novelty: NONE
  algorithmic_novelty: NONE

FOUND-FUNCTIONAL-GRAPH-001: VERIFIED / APPROVED / NOT_AUTHORIZED
FOUND-SEMIGROUP-002:        VERIFIED / APPROVED / NOT_AUTHORIZED
RH-NOGO-001:                FROZEN_PARTIAL_RESULT / NOT_AUTHORIZED /
                            NO_EXECUTION / DEFERRED
```

Nenhum `extension_status` foi alterado. Nenhum módulo matemático foi
tocado. O novo item é **independente** e apenas consome APIs verificadas.

## As seis alternativas

### A — totalização do detector

```yaml
candidate: totalizar detectCycleWitness?
formal_cost: baixo a moderado
engineering_value: BAIXO
software_reuse: baixo
scientific_risk: baixo
dependency_readiness: alta
poc_30_day: sim
classification: DEFERRED_LOW_INCREMENTAL_VALUE
reason: >
  A completeness ja prova que none eh impossivel. A remocao de Option
  melhora pouco a integracao pratica e NAO resolve a entrada de dados
  externos. Trocar Option CycleWitness por CycleWitness nao aproxima o
  detector de uma tabela carregada em runtime — e um consumidor externo
  vai precisar de Except de qualquer modo, para reportar entrada
  invalida.
```

Observação adicional: em uma camada dinâmica, `Option` é o **menor** dos
problemas; o erro real a reportar é "esta tabela é inválida", que a
totalização não endereça.

### B — Floyd

```yaml
candidate: Floyd como otimizacao
formal_cost: alto — invariantes de duas velocidades, terminacao
engineering_value: nulo hoje
software_reuse: nenhum sem runtime
scientific_risk: baixo
dependency_readiness: alta
poc_30_day: incerto
classification: DEFERRED_PREMATURE_OPTIMIZATION
reason: >
  Ainda nao existe adaptador nem baseline executavel sobre dados
  recebidos em tempo de execucao. Otimizar antes de ter uma carga real
  eh otimizar contra uma suposicao.
```

### C — Brent

```yaml
candidate: Brent como otimizacao
formal_cost: alto — invariantes de bloco e dobramento
engineering_value: nulo hoje
classification: DEFERRED_PREMATURE_OPTIMIZATION
reason: idem, com risco formal ainda maior que Floyd
```

### D — extração isolada

```yaml
candidate: Lake executable sobre exemplos definidos no fonte
formal_cost: baixo
engineering_value: APARENTE, nao real
software_reuse: nenhum
classification: INSUFFICIENT_RUNTIME_VALUE
reason: >
  Compilar uma funcao fechada ou um modelo fixo NAO permite analisar
  sistemas fornecidos por usuarios ou por outros softwares. O binario
  saberia responder apenas sobre os cinco modelos ja escritos no fonte,
  que ja sabemos responder por #eval.
```

Este é o ponto que o gate anterior deixou explícito e que esta revisão
confirma: **executar dentro do elaborador não é o gargalo; receber a
entrada é.**

### E — infraestrutura de testes

```yaml
candidate: resolver o padrao "teste que importa a raiz"
formal_cost: nulo
engineering_value: medio, interno
scientific_risk: nulo
classification: P2_LAB_INFRASTRUCTURE
reason: >
  Os dois testes de auditoria de FOUND-CYCLE-DETECTION-001 importam
  TamesisLab e por isso nao podem ser registrados na raiz — seria import
  circular. Eles funcionam, e sao executados explicitamente. Nao ha
  bloqueio real no build.
```

Registrado como item futuro em `RT-GAP-018`. **Não** selecionado como
frente principal: nenhum bloqueio real foi encontrado no `lake build`,
que passa com 8737 jobs.

### F — adaptador de sistema finito em tempo de execução

```yaml
candidate: ENG-FINITE-STATE-RUNTIME-001
formal_cost: MODERADO
engineering_value: ALTO
software_reuse: MUITO ALTO
scientific_risk: baixo — engenharia formal padrao
dependency_readiness: ALTA — detector VERIFIED e result_review APPROVED
poc_30_day: SIM
classification: SELECTED
reason: >
  Transforma uma API formal fechada em uma interface para dados
  dinamicos validados. Eh a unica das seis que muda o que o laboratorio
  CONSEGUE FAZER, e nao apenas quao rapido ou quao elegante ele faz.
```

## Comparação de retorno

| Candidato | Custo formal | Valor de engenharia | Reuso | Risco | Prontidão | PoC 30d |
|---|---|---|---|---|---|---|
| A totalização | baixo | **baixo** | baixo | baixo | alta | sim |
| B Floyd | alto | nulo hoje | nulo | baixo | alta | incerto |
| C Brent | alto | nulo hoje | nulo | baixo | alta | não |
| D extração isolada | baixo | **aparente** | nenhum | baixo | alta | sim |
| E infra de testes | nulo | médio interno | interno | nulo | alta | sim |
| **F adaptador** | **moderado** | **alto** | **muito alto** | baixo | **alta** | **sim** |

```text
ENG-FINITE-STATE-RUNTIME-001 possui maior retorno imediato porque
transforma uma API formal fechada em uma interface para dados
dinamicos validados.
```

## Verificação de duplicata

```text
ENG- como track ou prefixo de item      0 ocorrencias na fila
RawTransitionTable / TransitionTable    0 ocorrencias no repositorio
RUNTIME-001 / RUNTIME_001               0 ocorrencias
Array no nucleo Foundations             0 ocorrencias
```

As menções a "adaptador" no laboratório são de dois tipos, e **nenhuma**
é o alvo desta frente:

| Onde | O que é |
|---|---|
| `CD-GAP-012`, `RESULT_BOUNDARY.md`, `REVIEW_DECISION.md` | o **adaptador de componente**, ponte proposicional com `FOUND-FUNCTIONAL-GRAPH-001` |
| `REUSE_MATRIX.md` das três frentes | a classificação `REQUIRES_ADAPTER`, que **descreve** a lacuna que esta frente vai fechar |

```text
duplicata: NAO ENCONTRADA
```

O item novo executa exatamente o que as matrizes de reutilização das três
fundações registraram como faltante.

## Critérios de rejeição do alvo

Nenhum ocorreu.

| Critério | Verificado |
|---|---|
| resultado equivalente encerrado | não existe |
| Lean fixado não suportar `Array` ou `Fin` executáveis | `Array` e `Fin` são core; `Fin n` já foi usado nos cinco modelos de teste |
| não haver representação total possível | `Fin n → Fin n` a partir de tabela fechada é total por construção |
| exigir escolha não computável para produzir dados | a prova de fechamento entra como argumento `Prop`; o dado vem do `Array` |
| escopo não separável de parsing externo | o núcleo recebe `Array Nat`, não texto — o parsing fica fora |
| custo exceder PoC de 30 dias | `MODERADO`; sete resultados candidatos, nenhum com teoria nova |

## Decisão

```text
A. PORTFOLIO_REVIEW_APPROVED_FINITE_STATE_RUNTIME_SELECTED
```

Item criado como `SCOPED`. Autorizada **apenas** a preparação da
especificação.
