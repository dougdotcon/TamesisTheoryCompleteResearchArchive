---
document_id: FCD-TEST-PLAN
tests_planned: 7
---

# Plano de testes

Os valores abaixo são **testes de regressão para a ordem da enumeração**.
**Não** são teoremas gerais de minimalidade.

## CD-TEST-001 — ponto fixo imediato

```text
a -> a
card X = 1
```

```yaml
expected_prefixIndex: 0
expected_period: 1
property_tested: caso degenerado; primeiro candidato da lista
```

## CD-TEST-002 — cauda para ponto fixo

```text
a -> b -> c -> c
card X = 3
```

```yaml
expected_prefixIndex: 2
expected_period: 1
property_tested: cauda nao trivial com ciclo trivial
```

Observação: a ordem visita `(0,1), (0,2), (0,3), (1,1), (1,2), (2,1)`. Os
cinco primeiros falham; `(2,1)` é o primeiro aceito.

## CD-TEST-003 — ciclo desde o início

```text
a -> b -> c -> a
card X = 3
```

```yaml
expected_prefixIndex: 0
expected_period: 3
property_tested: ciclo nao trivial sem cauda
```

Observação: `(0,1)` e `(0,2)` falham; `(0,3)` é aceito — e é o caso de
fronteira `μ + λ = card X`, o que torna este teste **também** um teste de
que a fronteira está na lista.

## CD-TEST-004 — cauda e ciclo de dois

```text
a -> b -> c -> d -> c
card X = 4
```

```yaml
expected_prefixIndex: 2
expected_period: 2
property_tested: caso geral, as duas fases nao triviais
```

## CD-TEST-005 — dois estados entrando no mesmo ciclo

Executar o detector **separadamente** a partir de cada estado.

```yaml
expected_period: pode coincidir entre os dois
expected_prefixIndex: depende do estado inicial
property_tested: >
  o periodo testemunhado eh propriedade do componente; o prefixIndex
  NAO eh. Liga-se a exists_component_cycle_with_entry_bound
```

## CD-TEST-006 — `Bool`

```yaml
property_tested: genericidade da API em tipo da biblioteca, nao inventado aqui
note: >
  os valores dependem da funcao escolhida; para f = not espera-se
  prefixIndex 0 e period 2, para f = id espera-se period 1
```

## CD-TEST-007 — tipo unitário

```yaml
card_X: 1
expected_prefixIndex: 0
expected_period: 1
property_tested: menor caso possivel; cycleCandidates 1 = [<0,1>]
```

Verificado na sonda que `(List.range 1).flatMap ...` produz exatamente
`[(0, 1)]`.

## O que os testes **não** estabelecem

```text
NAO estabelecem minimalidade de mu;
NAO estabelecem minimalidade de lambda;
NAO estabelecem complexidade;
NAO estabelecem equivalencia com Floyd.
```

Se a ordem da enumeração mudar, os valores esperados mudam — e é
exatamente para detectar isso que os testes existem.
