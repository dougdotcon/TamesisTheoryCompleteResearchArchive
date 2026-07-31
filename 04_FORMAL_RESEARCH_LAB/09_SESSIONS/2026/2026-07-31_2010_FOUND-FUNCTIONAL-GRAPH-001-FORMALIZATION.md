---
session_id: 2026-07-31_2010_FOUND-FUNCTIONAL-GRAPH-001-FORMALIZATION
started_at: 2026-07-31T19:20:00-03:00
ended_at: 2026-07-31T20:10:00-03:00
agent: claude-opus-5
git_commit_before: f8ccc0203e27dcb7870fa4f7f63a999038236235
git_commit_after: null
active_work_item: FOUND-FUNCTIONAL-GRAPH-001
authorized_action: FOUND_FUNCTIONAL_GRAPH_001_FORMALIZATION_AUTHORIZED
result_status: FOUND_FUNCTIONAL_GRAPH_001_FORMALIZATION_VERIFIED
files_created:
  - "05_FORMAL/lean/TamesisLab/Foundations/FunctionalGraphs/Relations.lean"
  - "05_FORMAL/lean/TamesisLab/Foundations/FunctionalGraphs/PeriodicOrbits.lean"
  - "05_FORMAL/lean/TamesisLab/Foundations/FunctionalGraphs/ComponentCycle.lean"
  - "05_FORMAL/lean/TamesisLab/Foundations/FunctionalGraphs/Counterexamples.lean"
  - "05_FORMAL/lean/TamesisLab/Foundations/FunctionalGraphs/Audit.lean"
  - "05_FORMAL/lean/TamesisLab/Foundations/FunctionalGraphs.lean"
  - "05_FORMAL/lean/TamesisLab/Tests/FoundFunctionalGraph001.lean"
  - "05_FORMAL/lean/TamesisLab/Tests/FoundFunctionalGraph001Counterexamples.lean"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/THEOREM_MAP.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/PROOF_AUDIT.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/COUNTEREXAMPLE_AUDIT.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/RESULT_BOUNDARY.md"
  - "found-functional-graph-001-formalization-result.json"
  - "09_SESSIONS/2026/2026-07-31_2010_FOUND-FUNCTIONAL-GRAPH-001-FORMALIZATION.md"
files_modified:
  - "05_FORMAL/lean/TamesisLab/Foundations.lean"
  - "05_FORMAL/lean/TamesisLab.lean"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/STATUS.yaml"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/GAP_REGISTER.yaml"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "00_GOVERNANCE/CLAIM_LEDGER.yaml"
  - "10_TOOLS/labctl.py"
  - "LAB_STATE.md"
  - "CHANGELOG.md"
commits_in_this_gate: 1
decision: FOUND_FUNCTIONAL_GRAPH_001_FORMALIZATION_VERIFIED
next_single_action: "Revisar a API formal, as instâncias, os contraexemplos e os limites do resultado antes de autorizar qualquer extensão."
---

## Preflight

`HEAD = f8ccc020…`, árvore limpa. `canonical_commit` atualizado de
`90fb4e2` para `f8ccc02` **antes** de criar qualquer arquivo Lean.

## O resultado

```lean
theorem exists_component_cycle_with_entry_bound {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ mu : ℕ,
      mu < Fintype.card X ∧
      f^[mu] x ∈ Function.periodicPts f ∧
      ∀ q : X, q ∈ Function.periodicPts f → EventuallyMeets f x q →
        Function.periodicOrbit f (f^[mu] x) = Function.periodicOrbit f q
```

Prova por composição de cinco passos. **Nenhum pigeonhole, nenhuma indução
nova, nenhum `∃!`.**

## A arquitetura por hipóteses funcionou

```text
Relations.lean        sem finitude
PeriodicOrbits.lean   sem finitude
ComponentCycle.lean   [Fintype X]  — unico arquivo
```

As assinaturas impressas confirmam: `eventuallyMeets_trans` e
`periodicOrbit_eq_of_eventuallyMeets` **não** exigem `Fintype X`, e
`DecidableEq X` está ausente de **todos** os teoremas. A previsão do gate
de portfólio, de que `DecidableEq` provavelmente seria necessária aqui,
está definitivamente refutada.

## Três falhas, todas corrigidas sem token proibido

1. **`le_total` desconhecido.** Sob imports mínimos ele não está em escopo.
   Trocado por `Nat.le_total`, do core.
2. **`Symmetric` está depreciado** em favor de `Std.Symm` — o mesmo que já
   havia acontecido com `IsRefl`/`Std.Refl` em `FOUND-SEMIGROUP-002`. E o
   construtor de `Std.Symm` tem os **dois elementos explícitos**, exigindo
   `⟨fun _ _ h => …⟩`; a primeira tentativa com `⟨fun h => …⟩` falhou com
   erro de tipo.
3. **`rw` não fechava por `rfl`** em cinco lemas de iteração dos
   contraexemplos. O `rfl` automático de `rw` usa transparência reducível e
   não desdobra funções definidas por casamento de padrão. Corrigido com
   `rfl` explícito.

Também confirmei, antes de escrever, que **`Mathlib.Tactic.Omega` não
existe** nesta revisão — `omega` é tática do core. O import sugerido pelo
gate foi omitido, e o umbrella `Mathlib.Tactic` não foi necessário em
lugar algum.

## Sem rebaixamento em CE-006

O gate permitia formalizar a versão fraca e declarar
`igualdade dos períodos mínimos: DEFERRED`. **Não foi necessário.** A
sondagem prévia mostrou que `IsPeriodicPt.minimalPeriod_dvd`,
`minimalPeriod_pos_of_mem_periodicPts` e
`minimalPeriod_eq_one_iff_isFixedPt` existem, então provei
`minimalPeriod f a0 = minimalPeriod f b0 = 2` pelo auxiliar `private
minimalPeriod_eq_two`, em seis passos.

```yaml
minimal_period_counterexample_status: FORMALIZED_NOT_DEFERRED
```

## A disciplina que o gate exigia

```text
Fintype X apenas em ComponentCycle.lean        OK
DecidableEq X ausente de todos                 OK
zero instancias no nucleo matematico           OK
zero Setoid, zero SimpleGraph, zero Quotient   OK  (so mencoes em prosa)
pigeonhole NAO reaplicado                      OK
decide NAO usado sobre periodicOrbit           OK
zero native_decide                             OK  (3 mencoes, todas negando uso)
```

`iterReachable_trans` **não depende de axioma algum**.
`eventuallyMeets_trans` usa apenas `propext` e `Quot.sound` — sem
`Classical.choice`.

## Auditoria de whitespace — antes do commit

O defeito de linha em branco final ocorreu em dois gates seguidos. Desta
vez rodei a auditoria **antes** do `git add`, conforme o gate exigiu, e
corrigi os arquivos afetados na mesma passagem. **Um único commit**,
nenhum commit corretivo posterior.

## O objeto único é a órbita

Este é o ponto do gate, e vale repetir por ser o mais fácil de ler errado:

```text
A unicidade eh da ORBITA PERIODICA.

NAO do ponto periodico     — FFG-CE-005 exibe dois, distintos
NAO do representante       — f^[mu] x eh UM, nao O
NAO de mu                  — minimalidade nao provada
NAO do periodo             — minimalidade nao provada no principal
NAO de um ciclo global     — FFG-CE-001 exibe dois
```

## O que fica bloqueado

```text
ponte com SimpleGraph, arvores de entrada, distancia minima,
tempo minimo de entrada, representante canonico, quociente formal,
classificacao completa.
```

`FFG-GAP-014` permanece `OPEN_BIBLIOGRAPHIC`: nenhuma fonte primária foi
obtida, logo nenhuma afirmação de prioridade histórica é permitida.

## Novidade

```yaml
mathematical_novelty: NONE
```

Toda a maquinaria de ciclos já existia na Mathlib. O trabalho desta frente
foi conectá-la a `EventuallyMeets` e ao resultado já verificado de
`FOUND-SEMIGROUP-002`. O valor é de API e integração.
