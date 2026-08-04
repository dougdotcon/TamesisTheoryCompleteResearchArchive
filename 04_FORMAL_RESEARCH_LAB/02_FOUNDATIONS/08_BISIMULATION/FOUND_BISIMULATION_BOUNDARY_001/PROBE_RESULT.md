---
document_id: FOUND-BISIMULATION-BOUNDARY-001-PROBE-RESULT
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
probe_exit: 0
probe_removed: true
---

# Resultado do probe descartável

## Execução

```text
arquivo   /tmp/BisimulationProbe.lean
comando   lake env lean, via script com captura de codigo de saida
error_lines        0
REAL_EXIT_CODE     0
removido           SIM
```

O código de saída foi capturado por **arquivo de script**, não por
`echo $?` atravessando fronteira de shell — regra incorporada no gate de
formalização da frente anterior.

## Declarações compiladas

```text
Simulates
Reflects
Bisimulation
simulates_iff_semiconj
reflects_iff_simulates
bisimulation_iff_semiconj
boolToUnit_bisimulation
forgetBool_surjective
bisimulation_does_not_reflect_cycles
surjective_bisimulation_does_not_reflect_cycles
bisimulation_not_orbitSeparating
injective_bisimulation_reflects
```

## Pegada medida

```text
bisimulation_iff_semiconj                          NENHUM
reflects_iff_simulates                             NENHUM
boolToUnit_bisimulation                            NENHUM
bisimulation_does_not_reflect_cycles               NENHUM
surjective_bisimulation_does_not_reflect_cycles    NENHUM
```

**A frente inteira é livre de pegada axiomática.** Diferente da frente
anterior, nada aqui atravessa `analyzeEncodedSystem`, de modo que
`propext`, `Classical.choice` e `Quot.sound` não entram.

## Aviso do linter observado

```text
warning: Variable name `stepA` is not explicitly referenced
```

Em `injective_bisimulation_reflects`, que não depende de `stepA`. Será
corrigido na formalização permanente — a variável sai da assinatura, já
que a conclusão é sobre `OrbitSeparating`, que não menciona o sistema
abstrato.

Registrado aqui para que a correção não pareça uma mudança silenciosa
de assinatura.

## Tokens proibidos

```text
sorry, admit, unsafe, noncomputable   0
Classical.choose, Classical.decEq     0
avaliacao nativa                      0
declaracoes destinadas a falhar       0
```
