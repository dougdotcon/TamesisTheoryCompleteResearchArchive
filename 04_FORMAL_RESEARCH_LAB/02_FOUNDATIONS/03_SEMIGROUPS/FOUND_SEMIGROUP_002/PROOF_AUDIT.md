---
artifact_id: FOUND-SEMIGROUP-002
audit_status: PASS
---

# FOUND-SEMIGROUP-002 — Auditoria de prova

## Axiomas

`#print axioms` nos oito objetos exigidos:

```text
reachable_refl                     does not depend on any axioms
reachable_trans                    does not depend on any axioms
IsInvariant.of_reachable           does not depend on any axioms
periodic_tail_of_collision         does not depend on any axioms
collision_propagates               [propext, Quot.sound]
exists_bounded_iterate_collision   [propext, Classical.choice, Quot.sound]
exists_eventual_period             [propext, Classical.choice, Quot.sound]
monoid_element_eventually_periodic [propext, Classical.choice, Quot.sound]
```

Quatro dos oito **não dependem de axioma algum**. Os demais permanecem
dentro do conjunto permitido. **Sem `sorryAx`, sem axioma local.**

`Classical.choice` entra pela cadeia do pigeonhole (`Fintype`/`Finset`), não
por escolha deliberada.

## Tokens proibidos

```bash
grep -RInE '\b(sorry|admit|axiom|unsafe)\b' --include='*.lean' --exclude-dir='.lake' .
```

**Zero** ocorrências na árvore Lean inteira do laboratório.

`native_decide`: **1** ocorrência, exclusivamente no docstring do teste de
contraexemplos, na frase que declara que ele **não** é usado. Nenhuma
invocação real.

## Uso único da casa dos pombos

`Fintype.exists_ne_map_eq_of_card_lt` aparece **uma única vez** em todo o
diretório, em `exists_bounded_iterate_collision`. Todos os demais
resultados são composição:

```text
exists_eventual_period          = collision + tail + propagation
monoid_element_eventually_*     = collision + smul_iterate_apply
CE-003 aplicado ao teorema      = instanciacao
```

## `minimalPeriod` não é usado

Nenhuma ocorrência de `Function.minimalPeriod` ou `MulAction.period` nos
arquivos da frente. A ligação com a API oficial de dinâmica passa por
`Function.IsPeriodicPt` aplicado ao ponto **da cauda** `f^[μ] x`.

`CE-003` demonstra por que isso importa: ali o ponto inicial não é
periódico para período positivo algum (`s0_not_periodic`), de modo que
`minimalPeriod f s0 = 0` — o que contradiria `0 < λ`.

## Nenhuma instância global perigosa

Nenhuma `instance : Preorder X`. As onze `instance` do diretório são todas
locais aos namespaces dos contraexemplos (`Fintype`, `Monoid`,
`MulAction` dos modelos `CE00x`), e nenhum par
`(monoide, tipo de estados)` recebe duas instâncias.

## Falhas durante a execução

Quatro, todas corrigidas sem token proibido:

1. **`import Mathlib.Tactic.Omega` não existe** nesta revisão. O `omega` é
   tática do core Lean; o import foi removido, junto de
   `Mathlib.Tactic.Linarith`, que também não era necessário.
2. **`IsRefl` está depreciada** em favor de `Std.Refl`, com `α` implícito.
   Enunciado trocado; `IsTrans` permanece, pois não está depreciada.
3. **`collision_propagates`**: dois `rw [Function.iterate_add_apply]` sem
   argumentos reescreveram duas vezes o **mesmo** lado, deixando
   `f^[k] (f^[mu] (f^[lam] x))`. Corrigido instanciando explicitamente
   `Function.iterate_add_apply f k (mu + lam) x` e
   `Function.iterate_add_apply f k mu x`.
4. **Teste isolado**: um `rw` tentou operar sobre `IsPeriodicPt` sem
   desdobrá-lo. O exemplo foi reescrito para usar diretamente
   `exists_bounded_iterate_collision`, que já tem a forma desejada.

Além disso, cinco avisos de linter (`tac1 <;> tac2` onde `tac1; tac2`
bastava, em tipos de um construtor) foram corrigidos, e um aviso
`simpa`→`simp`. O build final é **limpo, sem avisos**.

## Imports

Diretório inteiro:

```text
Mathlib.Algebra.Group.Action.Defs
Mathlib.Data.Finset.Insert
Mathlib.Data.Fintype.Card
Mathlib.Data.Fintype.Defs
Mathlib.Data.Fintype.Pigeonhole
Mathlib.Dynamics.PeriodicPts.Defs
Mathlib.GroupTheory.GroupAction.Defs
Mathlib.Logic.Function.Iterate
Mathlib.Order.Defs.Unbundled
```

Nenhum import de análise real, topologia, teoria da medida, PDE, geometria,
`RH-NOGO` ou arquivo legado. `Mathlib.Tactic` (umbrella) **não** foi
necessário.

## Vocabulário proibido

Busca por `TRI`, `TDTR`, `entropia`, `physics` nos arquivos da frente:
**zero** ocorrências.

## Build

```text
lake build TamesisLab.Foundations.FiniteDynamics   PASS, 765 jobs
lake build (completo)                              PASS, 8717 jobs, 117 s
Tests/FoundSemigroup002.lean                       exit 0, 16 s
Tests/FoundSemigroup002Counterexamples.lean        exit 0, 4 s
```

Nenhum erro foi ocultado pela remoção de teste: os dois testes isolados
permanecem no repositório e são importados por `TamesisLab.lean`.

## O que **não** foi provado

```text
unicidade da cauda mu;
minimalidade do periodo lam;
decomposicao canonica completa em cauda e ciclo;
classificacao de todas as acoes finitas;
qualquer resultado sobre sistemas infinitos.
```

`FSG2-GAP-004b` permanece deferido, como planejado.
