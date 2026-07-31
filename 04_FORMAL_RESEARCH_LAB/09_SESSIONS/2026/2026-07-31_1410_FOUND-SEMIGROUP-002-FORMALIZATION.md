---
session_id: 2026-07-31_1410_FOUND-SEMIGROUP-002-FORMALIZATION
started_at: 2026-07-31T13:10:00-03:00
ended_at: 2026-07-31T14:10:00-03:00
agent: claude-opus-5
git_commit_before: 2b86a8809776774e4caf3a54d1469d240ecdaf1d
git_commit_after: null
active_work_item: FOUND-SEMIGROUP-002
authorized_action: FOUND_SEMIGROUP_002_FORMALIZATION_AUTHORIZED
result_status: FOUND_SEMIGROUP_002_FORMALIZATION_VERIFIED
files_created:
  - "05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics/Reachability.lean"
  - "05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics/Invariants.lean"
  - "05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics/EventualPeriodicity.lean"
  - "05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics/MonoidIteration.lean"
  - "05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics/Counterexamples.lean"
  - "05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics/Audit.lean"
  - "05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics.lean"
  - "05_FORMAL/lean/TamesisLab/Tests/FoundSemigroup002.lean"
  - "05_FORMAL/lean/TamesisLab/Tests/FoundSemigroup002Counterexamples.lean"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/THEOREM_MAP.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/PROOF_AUDIT.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/COUNTEREXAMPLE_AUDIT.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/RESULT_BOUNDARY.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/C3_BOUNDARY.md"
  - "found-semigroup-002-formalization-result.json"
  - "09_SESSIONS/2026/2026-07-31_1410_FOUND-SEMIGROUP-002-FORMALIZATION.md"
files_modified:
  - "05_FORMAL/lean/TamesisLab/Foundations.lean"
  - "05_FORMAL/lean/TamesisLab.lean"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/DEFINITIONS.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/KNOWN_RESULTS_MATRIX.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/STATUS.yaml"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/GAP_REGISTER.yaml"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "00_GOVERNANCE/CLAIM_LEDGER.yaml"
  - "10_TOOLS/labctl.py"
  - "LAB_STATE.md"
  - "CHANGELOG.md"
tests_executed:
  - "lake build: PASS, 8717 jobs, 117 s"
  - "Tests/FoundSemigroup002.lean: exit 0, 16 s"
  - "Tests/FoundSemigroup002Counterexamples.lean: exit 0, 4 s"
  - "tokens proibidos: sorry=0 admit=0 axiom=0 unsafe=0"
  - "#print axioms (8 objetos): 4 sem axioma algum, 4 dentro do permitido"
  - "native_decide: 0 usos"
  - "pytest: 9 passed"
  - "labctl validate: PASS, canonical_commit_check PASS"
claims_changed:
  - "FINITE-DYNAMICS-FORMAL-001 adicionada (F, VERIFIED, novelty NONE)"
gaps_closed:
  - "FSG2-GAP-004c: DecidableEq X confirmada ociosa e omitida"
  - "FSG2-GAP-005: propagacao formalizada"
gaps_partially_resolved:
  - "FSG2-GAP-007: estrategia de codificacao decidida; negativa sobre o periodo continua sem exemplo"
next_single_action: "Revisar o resultado formal, os limites de escopo e o potencial de reutilização antes de autorizar qualquer extensão."
---

## Preflight

`HEAD = 2b86a880…`, árvore limpa. `canonical_commit` atualizado de
`39e3d95` para `2b86a880` **antes** de qualquer formalização;
`cat-file` exit 0, `merge-base --is-ancestor` exit 0 (igualdade com HEAD,
aceita).

## As duas correções obrigatórias

### 5.1 — invariância sob um elemento

A especificação afirmava que `IsInvariantUnder a` seria "estritamente mais
fraca" que `IsInvariant`. **Como afirmação universal, era falsa**: se `a`
gera `M`, as duas noções coincidem.

Formalizei **apenas a implicação**:

```lean
theorem IsInvariant.under (hI : IsInvariant I) (a : M) : IsInvariantUnder a I
```

A recíproca não é enunciada nem negada em geral. A correção está em
`DEFINITIONS.md`, `KNOWN_RESULTS_MATRIX.md`, `RESULT_BOUNDARY.md`,
`CHANGELOG.md` e no próprio docstring do módulo Lean.

### 5.2 — contraexemplo de alcançabilidade

`Reachable` é definida pela **ação completa**. O grafo de uma função
isolada refutaria apenas a alcançabilidade por iterações daquele gerador —
não a simetria de `Reachable`.

`CE-001` foi reconstruído como ação genuína de monoide,
`Tr = {idT, collapse}` sobre `St = {zero, one}`, com associatividade,
identidade bilateral e compatibilidade da ação provadas **antes** de
qualquer instância. A negativa `not_reachable_one_zero` quantifica sobre
**todo** o monoide: `act_one` mostra que nenhuma das duas transformações
move `one`.

## As três camadas, na prática

```text
CAMADA A   Reachability.lean, Invariants.lean     acao completa
CAMADA C   EventualPeriodicity.lean               SEM monoide
CAMADA B   MonoidIteration.lean                   corolario DERIVADO
```

`EventualPeriodicity.lean` **não importa** nada de teoria de monoides —
só `Fintype`, `iterate` e `PeriodicPts`. Foi possível manter a Camada C
literalmente livre de estrutura algébrica.

## Casa dos pombos: uma vez só

`Fintype.exists_ne_map_eq_of_card_lt` aparece **uma única vez**, em
`exists_bounded_iterate_collision`. Os índices vêm de
`g : Fin (card X + 1) → X`, `g k = f^[k] x`. O split `i < j` / `j < i` sai
de `lt_or_gt_of_ne`, e **ambos os ramos usam o mesmo auxiliar**
`eventual_period_of_lt`, com `hEq.symm` no segundo — sem duplicar o
argumento.

Os três limitantes saem por `omega` de `i < j` e `j ≤ card X`.

## O ponto periódico é a cauda

```lean
periodic_tail_of_collision :
  f^[mu + lam] x = f^[mu] x → Function.IsPeriodicPt f lam (f^[mu] x)
```

O argumento é `f^[mu] x`, **não** `x`. `Function.minimalPeriod` não é usado
em lugar algum — `CE-003` mostra por quê: ali `s0` não é periódico para
período positivo algum (provei a forma **forte**, `s0_not_periodic`, via
`iterate_ge_two`), logo `minimalPeriod f s0 = 0`, o que contradiria
`0 < λ`.

## Hipóteses ociosas: confirmadas e removidas

As assinaturas impressas pelo build:

```text
@exists_eventual_period :
  ∀ {X} [inst : Fintype X] (f : X → X) (x : X), ...

@monoid_element_eventually_periodic :
  ∀ {M} {X} [Monoid M] [Fintype X] [MulAction M X] (a : M) (x : X), ...
```

**Sem `DecidableEq X`, sem `Fintype M`, sem `Group M`.** `FSG2-GAP-004c`
fecha: a hipótese sugerida era de fato ociosa.

## Falhas

Quatro, nenhuma resolvida com token proibido:

1. **`import Mathlib.Tactic.Omega` não existe** nesta revisão — `omega` é
   tática do core. Removido, junto de `Mathlib.Tactic.Linarith`, também
   desnecessário. O diretório inteiro compila sem o umbrella
   `Mathlib.Tactic`.
2. **`IsRefl` está depreciada** em favor de `Std.Refl` (com `α`
   implícito). Troquei o enunciado; `IsTrans` não está depreciada, daí a
   assimetria entre os dois — registrada no `THEOREM_MAP.md`.
3. **`collision_propagates`**: dois `rw [Function.iterate_add_apply]` sem
   argumentos reescreveram duas vezes o **mesmo** lado, produzindo
   `f^[k] (f^[mu] (f^[lam] x))`. Corrigido instanciando explicitamente os
   dois lados.
4. **Teste isolado**: um `rw` tentou operar sobre `IsPeriodicPt` sem
   desdobrá-lo. Reescrevi o exemplo usando `exists_bounded_iterate_collision`,
   que já tem a forma desejada.

Além disso, seis avisos de linter foram corrigidos. **O build final não
emite aviso algum.**

Houve também uma queda do WSL durante a primeira tentativa de deploy — sem
consequência: os arquivos não haviam sido copiados, e o passo foi refeito
com cópia e build separados.

## Axiomas

Quatro dos oito objetos auditados **não dependem de axioma algum**:
`reachable_refl`, `reachable_trans`, `IsInvariant.of_reachable`,
`periodic_tail_of_collision`. Os demais usam `propext`,
`Classical.choice`, `Quot.sound`, que entram pela cadeia do pigeonhole.
Sem `sorryAx`.

## A leitura que precisa ficar travada

`RESULT_BOUNDARY.md` e `C3_BOUNDARY.md` registram, como vinculante:

```text
CORRETO:
Para CADA UMA das quatro propriedades especiais de C3 existe uma acao
finita na qual ela falha.

ERRADO:
As quatro falham SIMULTANEAMENTE em toda acao finita.
```

A segunda leitura seria falsa — em `C3` as quatro valem ao mesmo tempo.
Nenhum teorema de `FOUND-SEMIGROUP-001` foi alterado.

## Pendência que permanece

A negativa *"o período pode depender do estado inicial"* continua **sem
contraexemplo** (`FSG2-GAP-007`) e **não é afirmada** em documento algum.

## Novidade

**Zero.** Periodicidade eventual em conjunto finito é a casa dos pombos.
A claim `FINITE-DYNAMICS-FORMAL-001` registra `mathematical_novelty: NONE`
e proíbe explicitamente as leituras físicas, TRI, TDTR e de teoria do
tempo.
