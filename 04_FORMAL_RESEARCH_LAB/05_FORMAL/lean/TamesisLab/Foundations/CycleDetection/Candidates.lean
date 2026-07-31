import TamesisLab.Foundations.CycleDetection.Witness
import Mathlib.Data.List.Range

set_option autoImplicit false

/-!
# FOUND-CYCLE-DETECTION-001 — Enumeração dos candidatos

A lista finita sobre a qual o detector busca. **Sem hipótese alguma sobre
o tipo de estados** — esta camada nem menciona `X`.

Ordem vinculante:

```text
baseIndex crescente;
para cada baseIndex, period crescente.
```

A ordem sustenta os testes de regressão. Ela **não** é promovida a
afirmação de minimalidade: que o primeiro candidato aceito seja
frequentemente o de menor `baseIndex` é consequência da ordem, não um
teorema.

Ausência de duplicatas **não** é provada: não afeta a correção nem a
completude, já que `List.find?` devolve o primeiro elemento aceito.
-/

namespace TamesisLab.Foundations.CycleDetection

/-- Todos os pares `⟨m, p⟩` com `m < n`, `0 < p` e `m + p ≤ n`.

`List.range n` dá `m < n`; `List.range (n - m)` dá `k < n - m`, e com
`p = k + 1` obtém-se `1 ≤ p ≤ n - m`. O caso de fronteira `m + p = n`
está incluído. -/
def cycleCandidates (n : ℕ) : List CycleWitness :=
  (List.range n).flatMap fun m =>
    (List.range (n - m)).map fun k =>
      ⟨m, k + 1⟩

@[simp] theorem cycleCandidates_zero : cycleCandidates 0 = [] := rfl

@[simp] theorem cycleCandidates_one : cycleCandidates 1 = [⟨0, 1⟩] := rfl

/-- Caracterização da enumeração: **completa** e **correta** sobre as três
cotas estruturais.

Sem `Fintype`, sem `DecidableEq`, sem `Classical`, sem `f` e sem `x`. -/
theorem mem_cycleCandidates_iff {n : ℕ} {w : CycleWitness} :
    w ∈ cycleCandidates n ↔
      w.baseIndex < n ∧ 0 < w.period ∧ w.baseIndex + w.period ≤ n := by
  rcases w with ⟨m, p⟩
  simp only [cycleCandidates, List.mem_flatMap, List.mem_map, List.mem_range,
    CycleWitness.mk.injEq]
  constructor
  · rintro ⟨a, ha, k, hk, rfl, rfl⟩
    omega
  · rintro ⟨h₁, h₂, h₃⟩
    exact ⟨m, h₁, p - 1, by omega, rfl, by omega⟩

end TamesisLab.Foundations.CycleDetection
