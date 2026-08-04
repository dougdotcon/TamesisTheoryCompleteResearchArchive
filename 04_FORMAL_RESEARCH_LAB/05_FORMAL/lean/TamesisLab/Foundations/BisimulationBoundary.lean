import TamesisLab.Foundations.BisimulationBoundary.Definitions
import TamesisLab.Foundations.BisimulationBoundary.Collapse
import TamesisLab.Foundations.BisimulationBoundary.CounterexampleInstance
import TamesisLab.Foundations.BisimulationBoundary.CycleReflection

/-!
# FOUND-BISIMULATION-BOUNDARY-001 — agregador

O limite da relação de simulação.

```text
Definitions.lean      Simulates, Reflects, Bisimulation
Collapse.lean         bissimulacao funcional = semiconjugacao
CounterexampleInstance.lean   BOOL_TO_UNIT ja e bissimulacao
CycleReflection.lean  e mesmo assim nao reflete ciclos
```

## O resultado

```text
Para sistemas deterministicos TOTAIS e bissimulacao FUNCIONAL,
o zag e consequencia do zig: a testemunha esta imposta por
stepC ser funcao total.

Logo BOOL_TO_UNIT ja e uma bissimulacao, e sobrejetiva, e o
ciclo abstrato continua espurio.
```

## O quadro

```text
semiconjugacao             NAO reflete
bissimulacao funcional     NAO reflete
bissimulacao sobrejetiva   NAO reflete
OrbitSeparating            REFLETE
```

Reforçar a relação de simulação não atravessa a fronteira entre observar
e refletir. O que atravessa é separação de estados.

## O recorte, que é parte do resultado

Fora de sistemas determinísticos totais e bissimulação funcional — em
sistemas não determinísticos, relações de transição gerais, bissimulação
relacional `R ⊆ C × A`, ações rotuladas, funções parciais — zig e zag
**não** colapsam, e nada aqui se aplica.

Escrever "bissimulação é semiconjugação" sem esse qualificador é falso.

scientific_value: FORMAL_SEMANTIC_FOUNDATION
mathematical_novelty: NONE
algorithmic_novelty: NONE
-/
