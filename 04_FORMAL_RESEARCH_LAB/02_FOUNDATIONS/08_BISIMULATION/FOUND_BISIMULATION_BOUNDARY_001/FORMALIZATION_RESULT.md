---
document_id: FOUND-BISIMULATION-BOUNDARY-001-FORMALIZATION-RESULT
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
formalization_status: VERIFIED
lake_build_exit: 0
lake_build_jobs: 8775
axiom_footprint: NONE
---

# Resultado da formalização

## Build

```text
lake build            REAL_BUILD_EXIT=0
jobs                  8775
linhas "error:" reais 0
```

## Módulos permanentes

```text
BisimulationBoundary/Definitions.lean             Simulates, Reflects, Bisimulation
BisimulationBoundary/Collapse.lean                as tres equivalencias
BisimulationBoundary/CounterexampleInstance.lean  BOOL_TO_UNIT ja e bissimulacao
BisimulationBoundary/CycleReflection.lean         as duas negacoes
BisimulationBoundary/Audit.lean                   somente #check
BisimulationBoundary.lean                         agregador

Tests/FoundBisimulationBoundary001.lean
Tests/FoundBisimulationBoundary001Axioms.lean
```

```text
arquivos Lean novos                   8
arquivos preexistentes modificados    2  (somente linhas de import)
```

## Contagem derivada por script — bate com o congelado

```text
def Simulates
def Reflects
def Bisimulation
theorem simulates_iff_semiconj
theorem reflects_iff_simulates
theorem bisimulation_iff_semiconj
theorem bisimulation_does_not_reflect_cycles
theorem surjective_bisimulation_does_not_reflect_cycles

public_defs=3  public_theorems=5  public_total=8
```

```text
declarado em PUBLIC_API_SPECIFICATION.md   8
derivado do codigo                          8
divergencia                                 0
```

### A correção que fez as contagens baterem

A primeira organização colocou `boolToUnit_bisimulation` e
`forgetBool_surjective` no mesmo módulo das negações públicas. O script
então derivava **10** declarações contra as **8** congeladas.

As duas não podiam ir para o arquivo de testes: as negações públicas as
consomem. A solução foi separá-las em
`CounterexampleInstance.lean`, exatamente como a frente anterior separou
`Counterexample.lean`.

```text
TEST_ONLY residentes na biblioteca   2
motivo   consumidas pelas negacoes publicas
precedente   FiniteStateAbstraction/Counterexample.lean
```

A divergência foi resolvida **movendo o código para refletir a
classificação**, e não ajustando a contagem para caber.

## Elaboração isolada

```text
Definitions.lean               exit=0 errors=0
Collapse.lean                  exit=0 errors=0
CounterexampleInstance.lean    exit=0 errors=0
CycleReflection.lean           exit=0 errors=0
Audit.lean                     exit=0 errors=0
BisimulationBoundary.lean      exit=0 errors=0
FoundBisimulationBoundary001.lean        exit=0 errors=0
FoundBisimulationBoundary001Axioms.lean  exit=0 errors=0
```

### Um falso negativo, registrado

Na primeira execução, logo após a criação de
`CounterexampleInstance.lean`, os módulos `CycleReflection.lean` e
`BisimulationBoundary.lean` reportaram `exit=1 errors=1`, enquanto o
`lake build` completo passava com `0` erros.

Causa: os testes isolados rodaram **antes** do build, e o `.olean` do
módulo recém-criado ainda não existia. `lake env lean` não constrói
dependências.

Reexecutados **depois** do build: `exit=0 errors=0` nos oito.

O episódio é registrado porque um `exit=1` acompanhado de um build verde
é exatamente o padrão que não pode ser silenciado. Neste caso a
contradição tinha explicação verificável, e foi verificada.

## Pegada — nenhuma

```text
Simulates                                        nenhum axioma
Reflects                                         nenhum axioma
Bisimulation                                     nenhum axioma
simulates_iff_semiconj                           nenhum axioma
reflects_iff_simulates                           nenhum axioma
bisimulation_iff_semiconj                        nenhum axioma
boolToUnit_bisimulation                          nenhum axioma
forgetBool_surjective                            nenhum axioma
bisimulation_does_not_reflect_cycles             nenhum axioma
surjective_bisimulation_does_not_reflect_cycles  nenhum axioma
```

**Dez de dez.** Nada aqui atravessa `analyzeEncodedSystem`: não há
`Array`, não há tabela, não há execução. Por isso `propext`,
`Classical.choice` e `Quot.sound` não entram em lugar nenhum — ao
contrário da frente anterior.

## Tokens proibidos e typeclasses

```text
FORBIDDEN_TOKENS               0
NO_TYPECLASS_BRACKETS_IN_CORE  confirmado
NO_CLOSED_FRONT_FILES_CHANGED  confirmado
```

## Desvios da especificação

```text
nenhum desvio de assinatura
```

A única mudança em relação ao plano de módulos foi a criação de
`CounterexampleInstance.lean`, que **não** altera assinatura alguma e
serve para que a contagem derivada corresponda à classificação
congelada.
