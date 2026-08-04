import TamesisLab.Foundations.ComputabilityBridge.Encoding

set_option autoImplicit false

/-!
# FOUND-COMPUTABILITY-BRIDGE-001 — a cota do certificado

```text
w.baseIndex + w.period <= n     o TESTEMUNHO cabe em n     PROVADO
a computacao custa n passos     AFIRMACAO DE CUSTO         PROIBIDA
```

A primeira é teorema. A segunda exigiria um modelo de máquina que o
laboratório não tem — ver `CB-GAP-002`.

## A duplicação, declarada

`analyze_reduce_cb` é a **terceira** ocorrência da mesma redução do bloco
`do`: a original é privada em `FiniteStateRuntime/DynamicAnalysis.lean`,
a segunda é privada em `Monovariants/WitnessBounds.lean`.

Reproduzir uma redução curta a partir de API exclusivamente pública é
permitido; reimplementar o detector não é, e não é feito aqui. A correção
própria — alargar `analyzeTransitionTable_sound` para devolver o contrato
`Valid` inteiro — toca frente encerrada e exige gate próprio:
`CB-GAP-004`.
-/

namespace TamesisLab.Foundations.ComputabilityBridge

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection

variable {S : Type*} {n : Nat}

/-- Redução do bloco `do` quando as duas validações passam.

Auxiliar **privado**, reproduzido com API exclusivamente pública. -/
private theorem analyze_reduce_cb {raw : RawTransitionTable} (hRaw : raw.Valid)
    {start : Nat} (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start =
      (match ValidatedTransitionTable.detectCycle?
          (⟨raw.next, hRaw⟩ : ValidatedTransitionTable) ⟨start, hStart⟩ with
        | some witness => .ok witness
        | none => .error .internalDetectorFailure) := by
  unfold analyzeTransitionTable
  rw [show validateTransitionTable raw = .ok ⟨raw.next, hRaw⟩ from dif_pos hRaw]
  show (validateStart ⟨raw.next, hRaw⟩ start).bind _ = _
  rw [show validateStart ⟨raw.next, hRaw⟩ start = .ok ⟨start, hStart⟩
      from dif_pos hStart]
  rfl

/-- **A cota, no nível da tabela.**

O certificado cabe no tamanho da tabela. Recuperada da terceira cláusula
de `CycleWitness.Valid`, que `analyzeTransitionTable_sound` perde. -/
theorem analyzeTransitionTable_bound {raw : RawTransitionTable} {start : Nat}
    {w : CycleWitness} (h : analyzeTransitionTable raw start = .ok w) :
    w.baseIndex + w.period ≤ raw.next.size := by
  obtain ⟨hRaw, hStart, -⟩ := analyzeTransitionTable_sound h
  rw [analyze_reduce_cb hRaw hStart] at h
  cases hd : ValidatedTransitionTable.detectCycle?
      (⟨raw.next, hRaw⟩ : ValidatedTransitionTable) ⟨start, hStart⟩ with
  | none => rw [hd] at h; exact absurd h (by simp)
  | some w' =>
      rw [hd] at h
      have hww : w' = w := Except.ok.inj h
      subst hww
      have hv := (ValidatedTransitionTable.detectCycle?_sound hd).2.2.1
      simpa using hv

/-- **A cota tipada**: o certificado cabe em `n`.

Cota do **certificado**, não de recursos. -/
theorem analyzeEncodedSystem_bound {e : CertifiedFiniteEncoding S n}
    {stepS : S → S} {start : S} {w : CycleWitness}
    (h : analyzeEncodedSystem e stepS start = .ok w) :
    w.baseIndex + w.period ≤ n := by
  have hb : w.baseIndex + w.period ≤ (buildTransitionTable e stepS).next.size :=
    analyzeTransitionTable_bound h
  simpa using hb

end TamesisLab.Foundations.ComputabilityBridge
