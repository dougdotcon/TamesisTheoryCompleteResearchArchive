---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-EXECUTION-TEST-RESULT
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
tests_executed: 12
test_files: 4
native_evaluation_used: false
---

# Resultado dos testes

Todos executados dentro de `lake build`, exceto a auditoria umbrella,
executada explicitamente.

## Testes formais — `FoundFiniteStateAbstraction001.lean`

```text
ABS-TEST-001  orientacao por Iff.rfl                        PASS
ABS-TEST-002  iterate_commutes instanciado                  PASS
ABS-TEST-003  soundness observacional instanciada           PASS
ABS-TEST-004  OrbitSeparating por abstracao injetiva        PASS
ABS-TEST-005  reflexao concreta sob OrbitSeparating         PASS
ABS-TEST-006  cadeia central sem typeclass alguma           PASS
```

## Testes executáveis — `FoundFiniteStateAbstraction001Execution.lean`

```text
ABS-TEST-007  BOOL_TO_UNIT devolve .ok ⟨0,1⟩ de false       PASS
              BOOL_TO_UNIT devolve .ok ⟨0,1⟩ de true        PASS
ABS-TEST-008  identidade sobre Fin 4 devolve .ok ⟨2,2⟩      PASS
ABS-TEST-009  recorrencia abstrata, por rfl                 PASS
              recorrencia observacional pelo teorema        PASS
ABS-TEST-010  concreteStep false ≠ false                    PASS
              concreteStep true ≠ true                      PASS
ABS-TEST-011  falha de OrbitSeparating                      PASS
              reflexao ingenua falsa                        PASS
```

Todos por `decide` e `rfl`. A avaliação nativa **não** é usada.

## Auditoria de pegada — `FoundFiniteStateAbstraction001Axioms.lean`

```text
ABS-TEST-012  #print axioms de 16 declaracoes               PASS
```

## Auditoria umbrella — executada explicitamente

```text
alcance das 7 declaracoes publicas pela raiz     PASS
alcance do contraexemplo pela raiz               PASS
frentes anteriores ainda alcancadas              PASS
cadeia completa com abstracao muitos-para-um     PASS
REAL_EXIT_CODE                                   0
error_lines                                      0
```

### O teste mais informativo da frente

A auditoria umbrella instancia uma abstração **genuinamente
muitos-para-um**:

```text
C = Fin 4    stepC = rotacao +1
A = Fin 2    stepA = rotacao +1
abstract     paridade, dois-para-um
```

Resultado:

```text
a analise abstrata devolve   .ok ⟨0, 2⟩
a recorrencia OBSERVACIONAL  VALE      as paridades coincidem
a recorrencia CONCRETA       FALHA     rotate4 so volta em 4 passos
OrbitSeparating              FALHA
```

Este é o caso central da frente exibido em um único exemplo: um ciclo
abstrato de período `2` que **não** é ciclo concreto, com a soundness
observacional valendo e a reflexão corretamente indisponível.

`BOOL_TO_UNIT` mostra o mesmo com a abstração mais degenerada possível;
o exemplo da paridade mostra que o fenômeno não depende da
degenerescência.

## Contagem

```text
casos planejados em TEST_PLAN.md   12
casos executados                   12
arquivos de teste                   4
```
