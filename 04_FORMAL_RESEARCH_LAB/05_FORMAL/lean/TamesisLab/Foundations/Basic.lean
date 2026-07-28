namespace TamesisLab.Foundations

inductive Regime where
  | finite
  | continuous
deriving DecidableEq

inductive Transition (α : Type) where
  | edge : α → α → Transition α

theorem regime_smoke : True := by
  trivial

end TamesisLab.Foundations
