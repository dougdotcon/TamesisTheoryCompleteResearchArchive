---
document_id: PR-BISIMULATION-BOUNDARY-CANDIDATE
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
status: SCOPED
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SEMANTIC_FOUNDATION
---

# Candidato selecionado — bissimulação determinística e o limite da reflexão

## A pergunta

A frente anterior provou que a semiconjugação dá recorrência
**observacional** e não dá recorrência concreta. Ficou a suspeita
natural, registrada como `ABS-GAP-015`:

```text
bissimulacao e mais forte que semiconjugacao;
talvez ela reflita ciclos.
```

## A resposta, já compilada em probe

**Não.** E o motivo é mais forte do que "não vale": em sistemas
determinísticos totais, bissimulação **não é mais forte coisa alguma**.

### As duas metades

```lean
def Simulates (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  ∀ c : C, abstract (stepC c) = stepA (abstract c)

def Reflects (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  ∀ c : C, ∃ c' : C, stepC c = c' ∧ abstract c' = stepA (abstract c)

def Bisimulation (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  Simulates abstract stepC stepA ∧ Reflects abstract stepC stepA
```

### O colapso

```lean
theorem bisimulation_iff_semiconj (abstract) (stepC) (stepA) :
    Bisimulation abstract stepC stepA
      ↔ Function.Semiconj abstract stepC stepA
```

**Compilado, sem depender de nenhum axioma.**

O zag é gratuito: dado `c`, a testemunha é `stepC c`, e a obrigação que
sobra é exatamente o zig. Determinismo e totalidade fazem as duas
metades coincidirem.

### A consequência imediata

`BOOL_TO_UNIT` — o contraexemplo da frente anterior — **já é uma
bissimulação**:

```lean
theorem boolToUnit_bisimulation :
    Bisimulation forgetBool concreteStep abstractStep
```

E `forgetBool` é **sobrejetiva**. Nenhuma das duas coisas ajuda:

```lean
theorem bisimulation_does_not_reflect_cycles : ¬ (…)
theorem surjective_bisimulation_does_not_reflect_cycles : ¬ (…)
```

Ambos compilados, ambos sem axiomas.

## Por que isso vale uma frente

O laboratório já proibia, por escrito:

```text
"Nao assumir bissimulacao onde so ha semiconjugacao"
```

A proibição sugeria que **obter** bissimulação resolveria o problema.
Este resultado mostra que, no recorte determinístico total, não há nada
a obter: a bissimulação já está lá, e o ciclo continua espúrio.

O que separa não é bissimulação. É **injetividade sobre a órbita** — a
`OrbitSeparating` da frente anterior.

## Escopo congelado como proposta

```text
Simulates
Reflects
Bisimulation
bisimulation_iff_semiconj
boolToUnit_bisimulation
bisimulation_does_not_reflect_cycles
surjective_bisimulation_does_not_reflect_cycles
```

## O que NÃO entra

```text
sistemas nao deterministicos
relacoes de transicao gerais
bissimulacao RELACIONAL (R ⊆ C × A) em vez de funcional
bissimulacao de rotulos ou acoes
coinducao
quocientes
extracao, CLI, parser, integracao
```

O resultado vale para **bissimulação funcional entre sistemas
determinísticos totais**. Fora desse recorte, zig e zag não colapsam, e
nada aqui se aplica. Essa fronteira é a parte mais importante da frente.

## Pegada medida

```text
bisimulation_iff_semiconj                          NENHUM
reflects_iff_simulates                             NENHUM
boolToUnit_bisimulation                            NENHUM
bisimulation_does_not_reflect_cycles               NENHUM
surjective_bisimulation_does_not_reflect_cycles    NENHUM
```

A frente inteira é livre de pegada axiomática.

## Custo

```text
3 definicoes
5 teoremas
0 fontes primarias
0 dependencias novas
reutilizacao integral do contraexemplo ja formalizado
```

Todas as peças já compilaram em probe descartável, `exit 0`.

## Novidade

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
```

Que bissimulação funcional entre sistemas determinísticos coincida com
homomorfismo é clássico em semântica de concorrência. O que a frente
acrescenta é a conexão explícita com a fronteira de reflexão de ciclos
já formalizada neste repositório.
