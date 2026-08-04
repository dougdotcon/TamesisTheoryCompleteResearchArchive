import TamesisLab.Foundations.BisimulationBoundary.Collapse

set_option autoImplicit false

/-!
# FOUND-BISIMULATION-BOUNDARY-001 — o contraexemplo, instanciado

Material de **instanciação**, não API pública. Ele vive na biblioteca, e
não nos testes, porque as duas negações públicas de
`CycleReflection.lean` o consomem.

A frente anterior separou `Counterexample.lean` do núcleo pelo mesmo
motivo, e pela mesma razão estas declarações ficam fora da contagem
pública.

```text
BOOL_TO_UNIT sempre foi uma bissimulacao — ninguem tinha olhado.
```

Nada do contraexemplo original é alterado: o colapso é apenas aplicado à
semiconjugação que já estava provada.
-/

namespace TamesisLab.Foundations.BisimulationBoundary

open TamesisLab.Foundations.FiniteStateAbstraction.Counterexample

/-- O contraexemplo da frente anterior **já era** uma bissimulação. -/
theorem boolToUnit_bisimulation : Bisimulation forgetBool concreteStep abstractStep :=
  (bisimulation_iff_semiconj forgetBool concreteStep abstractStep).mpr boolToUnit_semiconj

/-- E a abstração é sobrejetiva: `Unit` tem um único habitante, e
`forgetBool false = ()`.

A sobrejetividade é a hipótese que costuma acompanhar bissimulação
funcional. Ela está disponível aqui, e ainda assim não resgata a
reflexão. -/
theorem forgetBool_surjective : Function.Surjective forgetBool :=
  fun u => ⟨false, by cases u; rfl⟩

end TamesisLab.Foundations.BisimulationBoundary
