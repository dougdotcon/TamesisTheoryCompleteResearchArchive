# FOUND-SEMIGROUP-001 — Mapa Lean

Raiz: `05_FORMAL/lean/`. Namespace: `TamesisLab.Foundations.Semigroups`.

| Módulo | Conteúdo | Imports Mathlib |
|---|---|---|
| `TamesisLab/Foundations/Semigroups/Basic.lean` | decisão de reuso da interface oficial (`SemigroupAction`/`MulAction`) e mapeamento terminológico | `Mathlib.Algebra.Group.Action.Defs` |
| `TamesisLab/Foundations/Semigroups/Regime3.lean` | `Regime3`, `Shift3`, `Shift3.apply`, `Shift3.comp`, instâncias `Fintype` manuais | `Mathlib.Data.Finset.Insert`, `Mathlib.Data.Fintype.Defs` |
| `TamesisLab/Foundations/Semigroups/Theorems.lean` | FOUND-SG-002 a FOUND-SG-013 | `Mathlib.Data.Fintype.Card` |
| `TamesisLab/Foundations/Semigroups/Action.lean` | instâncias `Monoid Shift3` e `MulAction Shift3 Regime3` (após as leis) | via `Basic` |
| `TamesisLab/Foundations/Semigroups/Audit.lean` | verificações de coincidência notacional (`*`, `1`, `•`) e das projeções `Semigroup`/`SemigroupAction` | — |
| `TamesisLab/Foundations/Semigroups.lean` | agregador da frente | — |
| `TamesisLab/Tests/FoundSemigroup001.lean` | um `example` por teorema + instâncias | — |

Grafo de build: `TamesisLab.lean` → `TamesisLab.Foundations` →
`TamesisLab.Foundations.Semigroups` e `TamesisLab.lean` →
`TamesisLab.Tests.FoundSemigroup001`. Nenhum módulo órfão.

Nota de implementação: o derive handler `Fintype` da revisão fixada
(`79d0395a…`) falha sob imports mínimos (mismatch `↑enumList`/`Nodup` na
construção derivada); as instâncias `Fintype` foram escritas manualmente com
`elems` explícito e `complete` por análise de casos.
