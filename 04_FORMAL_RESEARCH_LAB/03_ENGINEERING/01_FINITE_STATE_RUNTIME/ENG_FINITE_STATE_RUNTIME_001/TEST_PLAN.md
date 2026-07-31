---
document_id: RT-TEST-PLAN
tests: 9
---

# Plano de testes

Todos os nove foram **pré-verificados** na versão descartável do probe.
Os valores de `CycleWitness` dependem da ordem do detector e **não** são
afirmações de minimalidade geral.

## RT-TEST-001 — tabela vazia

```yaml
input_table: "#[]"
start: 0
validation_result: ok
analysis_result: "error (initialStateOutOfBounds 0 0)"
raw_execution_trace: "run? 0 0 = some 0; nenhum passo possivel"
property_tested: "tabela vazia eh ESTRUTURALMENTE valida, mas nao admite consulta"
expected_error_or_witness: initialStateOutOfBounds
```

## RT-TEST-002 — destino inválido

```yaml
input_table: "#[1]"
start: 0
validation_result: "error transitionDestinationOutOfBounds"
analysis_result: "error transitionDestinationOutOfBounds"
raw_execution_trace: "run? 1 0 = none — o destino 1 nao existe"
property_tested: "destino fora dos limites eh REJEITADO, nunca corrigido"
expected_error_or_witness: transitionDestinationOutOfBounds
```

## RT-TEST-003 — início inválido

```yaml
input_table: "#[0]"
start: 1
validation_result: ok
analysis_result: "error (initialStateOutOfBounds 1 1)"
property_tested: "a consulta eh validada SEPARADAMENTE da tabela"
expected_error_or_witness: initialStateOutOfBounds
```

## RT-TEST-004 — ponto fixo

```yaml
input_table: "#[0]"
start: 0
analysis_result: "ok <0,1>"
raw_execution_trace: "0 -> 0 -> 0"
property_tested: "caso minimo; reproduz o modelo Fin 1 identidade"
```

## RT-TEST-005 — ciclo de dois

```yaml
input_table: "#[1,0]"
start: 0
analysis_result: "ok <0,2>"
raw_execution_trace: "0 -> 1 -> 0"
property_tested: "reproduz o modelo Bool com not"
```

## RT-TEST-006 — cauda para ponto fixo

```yaml
input_table: "#[1,2,2]"
start: 0
analysis_result: "ok <2,1>"
raw_execution_trace: "0 -> 1 -> 2 -> 2"
property_tested: "reproduz o modelo Fin 3"
```

## RT-TEST-007 — cauda para ciclo de dois

```yaml
input_table: "#[1,2,3,2]"
start: 0
analysis_result: "ok <2,2>"
raw_execution_trace: "0 -> 1 -> 2 -> 3 -> 2"
property_tested: "reproduz o modelo Fin 4; caso geral"
```

## RT-TEST-008 — outros estados

```yaml
input_table: "#[1,2,3,2]"
start: "1, 2, 3"
analysis_result: "ok <1,2>, ok <0,2>, ok <0,2>"
property_tested: >
  o period testemunhado coincide dentro do componente; o baseIndex NAO —
  depende do estado inicial
```

## RT-TEST-009 — dois componentes

```yaml
input_table: "#[0,2,1]"
start: "0, 1, 2"
analysis_result: "ok <0,1>, ok <0,2>, ok <0,2>"
raw_execution_trace: "0 -> 0 (fixo);  1 -> 2 -> 1 (ciclo de dois)"
property_tested: "a tabela tem DOIS componentes; cada consulta ve o seu"
```

```text
NAO interpretar como enumeracao global dos componentes.
```

O adaptador responde sobre **a trajetória do estado consultado**. Que a
tabela tenha dois componentes é observável executando três consultas —
não é um resultado que a frente produza.

## O oráculo

Os quatro casos `004` a `007` reproduzem, em forma de tabela, exatamente
os modelos `Fin 1`, `Bool`, `Fin 3` e `Fin 4` já verificados em
`FOUND-CYCLE-DETECTION-001`. A coincidência dos certificados é **evidência
independente** de que a ponte `Array Nat → Fin n` preserva a dinâmica.
