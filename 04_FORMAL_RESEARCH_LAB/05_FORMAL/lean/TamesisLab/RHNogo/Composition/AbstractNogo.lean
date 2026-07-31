import TamesisLab.RHNogo.AsymptoticCore
import TamesisLab.RHNogo.Bridge

set_option autoImplicit false

/-!
# ABSTRACT-NOGO-001 — composição dos dois núcleos abstratos

Combina dois resultados **já verificados**:

* `COUNTING-LAW-BRIDGE` (`TamesisLab/RHNogo/Bridge/`) — transferência da
  lei `T log T` sob diferença `o(T log T)`;
* `ASYM-NOGO-001` (`TamesisLab/RHNogo/AsymptoticCore/`) — incompatibilidade
  entre lei de potência e lei `T log T`.

A prova é **composição de API**. Nenhuma análise assintótica nova é feita
aqui: não há manipulação de limites, não há tricotomia em `α`, não há
lema auxiliar.

## Escopo, vinculante

O enunciado é sobre duas funções reais arbitrárias. Não menciona — e não
depende de — `ζ`, zeros, Riemann, operadores, espectro, lei de Weyl,
variedades, PDE, Hilbert–Pólya ou `W-ELLIPTIC-SCALAR`.

Em particular: **`W-ELLIPTIC-SCALAR-BRIDGE` não é premissa Lean deste
teorema.** O gate geométrico anterior produziu uma interface *documental*,
não uma instância de `PowerCountingLaw`. Nada aqui transforma um operador
em `PowerCountingLaw`, e o diretório `Geometry/` **não** é importado.

## Convenção da diferença

`SubdominantTLog NTarget NBase` está definida em `Bridge/Definitions.lean`
como

```text
(fun T => NTarget T - NBase T) =o[atTop] (fun T => T * Real.log T)
```

isto é, `NTarget(T) − NBase(T) = o(T log T)` — exatamente a orientação
usada abaixo. Nenhuma inversão de sinal é necessária, e nenhuma foi feita
silenciosamente.
-/

namespace TamesisLab.RHNogo.Composition

open Filter TamesisLab.RHNogo.Bridge

/-- **ABSTRACT-NOGO-001.**

Nenhum par de funções reais `NTarget`, `NBase` pode satisfazer
simultaneamente:

1. uma lei de potência positiva finita para `NTarget`
   (`PowerCountingLaw`, expoente e constante positivos);
2. uma lei positiva finita `T log T` para `NBase` (`TLogCountingLaw`);
3. `NTarget − NBase = o(T log T)` (`SubdominantTLog`).

A prova compõe `COUNTING-LAW-BRIDGE` com `ASYM-NOGO-001`; não reprova
nenhum caso `α < 1`, `α = 1` ou `α > 1`. -/
theorem abstract_power_tlog_incompatibility
    {NTarget NBase : ℝ → ℝ}
    (hPower : PowerCountingLaw NTarget)
    (hTLog : TLogCountingLaw NBase)
    (hSubdominant : SubdominantTLog NTarget NBase) :
    False := by
  -- Passo 1 — COUNTING-LAW-BRIDGE: a lei `T log T` passa de `NBase` para
  -- `NTarget`, com a MESMA constante.
  have hTarget : TLogCountingLaw NTarget :=
    TLogCountingLaw.transfer hTLog hSubdominant
  -- Passos 2–5 — ASYM-NOGO-001 aplicado diretamente aos campos das duas
  -- interfaces, agora ambas referentes a `NTarget`.
  exact TamesisLab.RHNogo.AsymptoticCore.asym_nogo_001
    NTarget hPower.exponent hTarget.constant hPower.constant
    hPower.exponent_pos hTarget.constant_pos hPower.constant_pos
    hTarget.tendsto_normalized hPower.tendsto_normalized

/-- Dados de `ABSTRACT-NOGO-001` reunidos numa única estrutura, para
rastreabilidade: uma hipótese, um identificador.

Não é `class`: não há síntese de instância nem busca automática. -/
structure AbstractCountingNogoData (NTarget NBase : ℝ → ℝ) where
  powerLaw : PowerCountingLaw NTarget
  tLogLaw : TLogCountingLaw NBase
  subdominant : SubdominantTLog NTarget NBase

/-- A estrutura `AbstractCountingNogoData` é **inabitável**. -/
theorem AbstractCountingNogoData.false {NTarget NBase : ℝ → ℝ}
    (h : AbstractCountingNogoData NTarget NBase) : False :=
  abstract_power_tlog_incompatibility h.powerLaw h.tLogLaw h.subdominant

/-- Enunciado de `ABSTRACT-NOGO-001` como `Prop` fechada, para registro. -/
def AbstractNogoStatement : Prop :=
  ∀ (NTarget NBase : ℝ → ℝ),
    PowerCountingLaw NTarget →
    TLogCountingLaw NBase →
    SubdominantTLog NTarget NBase →
    False

/-- O enunciado registrado está provado. -/
theorem abstractNogoStatement_holds : AbstractNogoStatement :=
  fun _ _ hPower hTLog hSub =>
    abstract_power_tlog_incompatibility hPower hTLog hSub

end TamesisLab.RHNogo.Composition
