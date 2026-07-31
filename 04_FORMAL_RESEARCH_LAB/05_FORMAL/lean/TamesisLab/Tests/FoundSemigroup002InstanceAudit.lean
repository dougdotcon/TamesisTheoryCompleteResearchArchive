import TamesisLab.Foundations.FiniteDynamics

set_option autoImplicit false

/-!
# Auditoria de instâncias e de superfície pública — FOUND-SEMIGROUP-002

Este arquivo **não** introduz matemática. Ele verifica, por síntese de
instância e por typecheck, três coisas:

1. o núcleo matemático (`Reachability`, `Invariants`,
   `EventualPeriodicity`, `MonoidIteration`) **não declara instância
   alguma** — toda instância da frente pertence a um contraexemplo;
2. as instâncias dos contraexemplos são sintetizadas sem ambiguidade
   depois de importar o agregador;
3. nenhuma instância de `Preorder` foi criada para alcançabilidade.

Nenhum módulo matemático foi alterado para esta auditoria.
-/

namespace TamesisLab.Tests.FoundSemigroup002InstanceAudit

open TamesisLab.Foundations.FiniteDynamics
open TamesisLab.Foundations.FiniteDynamics.Counterexamples

/-! ## 1. As onze instâncias, sintetizadas nominalmente

Quatro em `CE001`, quatro em `CE002`, uma em `CE003`, duas em `CE004`,
nenhuma em `CE005`. -/

section CE001Instances
#synth Fintype CE001.St
#synth Fintype CE001.Tr
#synth Monoid CE001.Tr
#synth MulAction CE001.Tr CE001.St
end CE001Instances

section CE002Instances
#synth Fintype CE002.St
#synth Fintype CE002.Tr
#synth Monoid CE002.Tr
#synth MulAction CE002.Tr CE002.St
end CE002Instances

section CE003Instances
#synth Fintype CE003.St
end CE003Instances

section CE004Instances
#synth Fintype CE004.St
#synth MulAction CE001.Tr CE004.St
end CE004Instances

/-! ## 2. Sem colisão entre os dois usos do monoide de `CE001`

`CE001.Tr` age sobre dois tipos de estado distintos. As duas instâncias
`MulAction` são para pares diferentes e coexistem sem ambiguidade: cada
`•` abaixo resolve para a ação correta. -/

example : (CE001.Tr.collapse : CE001.Tr) • CE001.St.zero = CE001.St.one := rfl

example : (CE001.Tr.collapse : CE001.Tr) • CE004.St.pt = CE004.St.pt := rfl

/-! ## 3. Os dois monoides distintos não se confundem

`CE001.Tr` e `CE002.Tr` são tipos diferentes, cada um com **uma** instância
`Monoid`. -/

example : (1 : CE001.Tr) = CE001.Tr.idT := rfl
example : (1 : CE002.Tr) = CE002.Tr.idT := rfl

/-! ## 4. Nenhuma instância de `Preorder` para alcançabilidade

Reflexividade e transitividade estão disponíveis apenas como **teoremas**.
As duas linhas abaixo typecheck; nenhuma instância global é envolvida. -/

example {M X : Type*} [Monoid M] [MulAction M X] :
    Std.Refl (fun a b : X => Reachable (M := M) a b) :=
  reachable_isRefl

example {M X : Type*} [Monoid M] [MulAction M X] :
    IsTrans X (fun a b : X => Reachable (M := M) a b) :=
  reachable_isTrans

/-! ## 5. O núcleo aplica-se a tipos externos sem interferência

O agregador foi importado, com todas as instâncias dos contraexemplos, e o
teorema principal continua se aplicando a um tipo alheio à frente. -/

example (f : Bool → Bool) (b : Bool) :
    ∃ mu lam : ℕ,
      mu < Fintype.card Bool ∧ 0 < lam ∧ mu + lam ≤ Fintype.card Bool ∧
        Function.IsPeriodicPt f lam (f^[mu] b) ∧
        ∀ k : ℕ, f^[mu + k + lam] b = f^[mu + k] b :=
  exists_eventual_period f b

/-! ## 6. Superfície pública mínima — typecheck de cada nome exportado -/

#check @Reachable
#check @reachable_refl
#check @reachable_trans
#check @reachable_isRefl
#check @reachable_isTrans
#check @reachable_iff_mem_orbit
#check @IsInvariant
#check @IsInvariantUnder
#check @IsInvariant.under
#check @IsInvariant.of_reachable
#check @IsInvariantUnder.pow
#check @exists_bounded_iterate_collision
#check @periodic_tail_of_collision
#check @collision_propagates
#check @exists_eventual_period
#check @monoid_element_eventually_periodic
#check @monoid_element_eventual_period_propagates

end TamesisLab.Tests.FoundSemigroup002InstanceAudit
