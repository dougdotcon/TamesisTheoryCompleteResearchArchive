import TamesisLab.Foundations.Semigroups

/-!
# FOUND-SEMIGROUP-001 — teste de importação e referência

Importa a frente de semigrupos e referencia cada teorema por nome, um
`example` por resultado, com as assinaturas originais.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
-/

namespace TamesisLab.Tests.FoundSemigroup001

open TamesisLab.Foundations.Semigroups

-- FOUND-SG-002 a FOUND-SG-004 — estrutura algébrica.
example (a b c : Shift3) :
    Shift3.comp (Shift3.comp a b) c = Shift3.comp a (Shift3.comp b c) :=
  comp_assoc a b c

example (a : Shift3) : Shift3.comp .identity a = a := identity_comp a

example (a : Shift3) : Shift3.comp a .identity = a := comp_identity a

-- FOUND-SG-005 — compatibilidade da ação.
example (a b : Shift3) (r : Regime3) :
    (Shift3.comp a b).apply r = a.apply (b.apply r) := apply_comp a b r

-- FOUND-SG-006 — ciclo.
example (r : Regime3) :
    Shift3.forward.apply (Shift3.forward.apply (Shift3.forward.apply r)) = r :=
  forward_cycle r

-- FOUND-SG-007 e FOUND-SG-008 — cardinalidades.
example : Fintype.card Regime3 = 3 := card_regime3
example : Fintype.card Shift3 = 3 := card_shift3

-- FOUND-SG-009 a FOUND-SG-011 — distinção das transições.
example : Shift3.identity ≠ Shift3.forward := identity_ne_forward
example : Shift3.identity ≠ Shift3.forward2 := identity_ne_forward2
example : Shift3.forward ≠ Shift3.forward2 := forward_ne_forward2

-- FOUND-SG-012 — fidelidade.
example (a b : Shift3) (h : ∀ r, Shift3.apply a r = Shift3.apply b r) :
    a = b := apply_faithful a b h

-- FOUND-SG-013 — transitividade do modelo.
example (x y : Regime3) : ∃ s : Shift3, s.apply x = y := apply_transitive x y

-- Instâncias estruturais disponíveis.
example : Monoid Shift3 := inferInstance
example : SemigroupAction Shift3 Regime3 := inferInstance

end TamesisLab.Tests.FoundSemigroup001
