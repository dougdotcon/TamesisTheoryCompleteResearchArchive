---
document_id: FOUND-BISIMULATION-BOUNDARY-001-TEST-PLAN
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
tests_planned: 8
test_files: 2
---

# Plano de testes

## `FoundBisimulationBoundary001.lean` — testes formais

```text
BIS-TEST-001  simulates_iff_semiconj por Iff.rfl
BIS-TEST-002  reflects_iff_simulates instanciado
BIS-TEST-003  bisimulation_iff_semiconj instanciado
BIS-TEST-004  BOOL_TO_UNIT e bissimulacao
BIS-TEST-005  forgetBool e sobrejetiva
BIS-TEST-006  bissimulacao NAO reflete ciclos
BIS-TEST-007  bissimulacao sobrejetiva NAO reflete ciclos
BIS-TEST-008  cadeia central sem typeclass alguma
```

## `FoundBisimulationBoundary001Axioms.lean` — auditoria

Somente `#print axioms` das oito declarações públicas mais as duas
`TEST_ONLY`. Nenhum experimento negativo compartilha arquivo com probe
obrigatório.

Resultado esperado: **nenhuma** declaração da frente depende de axioma.

## O teste que mede a fronteira

`BIS-TEST-004` mais `BIS-TEST-006` juntos são o produto da frente:

```text
BOOL_TO_UNIT E bissimulacao          e
bissimulacao NAO reflete ciclos
```

Se algum dia `BIS-TEST-004` deixar de compilar, o colapso quebrou. Se
`BIS-TEST-006` deixar de compilar, alguém provou algo falso.

## Contagem

```text
testes planejados   8
arquivos de teste   2
```

Não há testes executáveis: a frente é inteiramente proposicional, não
introduz função computável e não avalia nada. Inventar um `#eval` aqui
seria teatro.
