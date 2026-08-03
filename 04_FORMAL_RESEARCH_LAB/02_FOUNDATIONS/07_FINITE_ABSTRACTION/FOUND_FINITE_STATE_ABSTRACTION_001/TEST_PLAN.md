---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-TEST-PLAN
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
tests_planned: 12
---

# Plano de testes

Três arquivos, com contratos distintos. Todos terminam com código de
saída zero; nenhum contém declaração destinada a falhar.

## `FoundFiniteStateAbstraction001.lean` — testes formais

```text
ABS-TEST-001  orientacao de Semiconj por Iff.rfl
ABS-TEST-002  iterate_commutes instanciado
ABS-TEST-003  soundness observacional instanciada
ABS-TEST-004  OrbitSeparating satisfeita por abstracao injetiva
ABS-TEST-005  soundness refletida sob OrbitSeparating
ABS-TEST-006  completeness abstrata generica, sem typeclass
```

## `FoundFiniteStateAbstraction001Execution.lean` — testes executáveis

```text
ABS-TEST-007  analise abstrata de BOOL_TO_UNIT devolve witness
ABS-TEST-008  analise abstrata com abstracao identidade sobre Fin 4
ABS-TEST-009  recorrencia abstrata do contraexemplo, por rfl
ABS-TEST-010  ausencia de recorrencia concreta, por decide
ABS-TEST-011  falha de OrbitSeparating no contraexemplo
```

Por `decide` e `rfl`. `native_decide` é proibido.

## `FoundFiniteStateAbstraction001Axioms.lean` — auditoria

```text
ABS-TEST-012  #print axioms das sete declaracoes publicas
```

Somente `#print axioms`. Nenhum experimento negativo compartilha
arquivo com um probe obrigatório — regra `mandatory_probe_exit_code` do
laboratório.

## Auditoria pela raiz

`FoundFiniteStateAbstraction001UmbrellaAudit.lean` importa `TamesisLab`
e confirma que os nomes públicos resolvem sem ambiguidade a partir da
raiz. Ele **não** é registrado em `TamesisLab.lean` — isso criaria
import circular, proibição já registrada no laboratório.

## Contagem

```text
testes planejados   12
arquivos de teste    4
```

Derivada das listas acima; conferida por script no gate de
formalização.
