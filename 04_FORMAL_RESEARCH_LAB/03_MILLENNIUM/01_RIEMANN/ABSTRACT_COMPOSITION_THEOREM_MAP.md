---
artifact_id: ABSTRACT-NOGO-001
status: VERIFIED
lean_root: "05_FORMAL/lean/TamesisLab/RHNogo/Composition/"
depends_on:
  - ASYM-NOGO-001
  - COUNTING-LAW-BRIDGE
---

# ABSTRACT-NOGO-001 — mapa de teoremas

## Identificadores

```text
ABSTRACT-NOGO-001
  PowerCountingLaw NTarget
+ TLogCountingLaw NBase
+ SubdominantTLog NTarget NBase
-> False

ABSTRACT-NOGO-E0-001
  o mesmo resultado sob igualdade eventual.

ABSTRACT-NOGO-E1-001
  o mesmo resultado sob diferença limitada.
```

## Inventário

| ID | Lean | Arquivo | Tipo |
|---|---|---|---|
| `ABSTRACT-NOGO-001` | `abstract_power_tlog_incompatibility` | `AbstractNogo.lean` | `theorem` |
| — | `AbstractCountingNogoData` | `AbstractNogo.lean` | `structure` |
| — | `AbstractCountingNogoData.false` | `AbstractNogo.lean` | `theorem` |
| — | `AbstractNogoStatement` | `AbstractNogo.lean` | `def` (`Prop`) |
| — | `abstractNogoStatement_holds` | `AbstractNogo.lean` | `theorem` |
| `ABSTRACT-NOGO-E0-001` | `abstract_nogo_of_eventuallyEq` | `Corollaries.lean` | `theorem` |
| `ABSTRACT-NOGO-E1-001` | `abstract_nogo_of_boundedDifference` | `Corollaries.lean` | `theorem` |

Cinco teoremas, uma estrutura, uma definição.

## Assinatura principal

```lean
theorem abstract_power_tlog_incompatibility
    {NTarget NBase : ℝ → ℝ}
    (hPower : PowerCountingLaw NTarget)
    (hTLog : TLogCountingLaw NBase)
    (hSubdominant : SubdominantTLog NTarget NBase) :
    False
```

## Convenção da diferença — opção C, documentar a existente

`SubdominantTLog` está definida em `Bridge/Definitions.lean` como

```lean
def SubdominantDifference (NTarget NBase scale : ℝ → ℝ) : Prop :=
  (fun T => NTarget T - NBase T) =o[atTop] scale

def SubdominantTLog (NTarget NBase : ℝ → ℝ) : Prop :=
  SubdominantDifference NTarget NBase (fun T => T * Real.log T)
```

isto é, literalmente `NTarget(T) − NBase(T) = o(T log T)` — a orientação
pedida. **Nenhuma inversão de sinal foi necessária e nenhuma foi feita.**
A convenção é confirmada por typecheck no teste isolado:

```lean
example (NTarget NBase : ℝ → ℝ) :
    SubdominantTLog NTarget NBase ↔
      (fun T => NTarget T - NBase T)
        =o[atTop] (fun T : ℝ => T * Real.log T) :=
  Iff.rfl
```

Como a orientação já era a correta, não foi criado lema de simetria de
little-o. Se um gate futuro precisar da ordem inversa, o lema terá de ser
provado ou reutilizado — não presumido.

## Cadeia da prova

```text
hTLog : TLogCountingLaw NBase
hSubdominant : SubdominantTLog NTarget NBase
        |
        |  COUNTING-LAW-BRIDGE  (TLogCountingLaw.transfer)
        v
hTarget : TLogCountingLaw NTarget     -- MESMA constante, por rfl
        |
        |  + hPower : PowerCountingLaw NTarget
        v
ASYM-NOGO-001  (asym_nogo_001)
   N        := NTarget
   α        := hPower.exponent        (> 0 por exponent_pos)
   c        := hTarget.constant       (> 0 por constant_pos)
   C        := hPower.constant        (> 0 por constant_pos)
   T log T  := hTarget.tendsto_normalized
   T ^ α    := hPower.tendsto_normalized
        v
      False
```

Duas linhas de prova: uma `have` e um `exact`. **Composição de API.**
Nenhum caso `α < 1`, `α = 1` ou `α > 1` é reprovado; nenhum limite é
manipulado; nenhum lema auxiliar novo foi criado.

## Corolários

```lean
theorem abstract_nogo_of_eventuallyEq
    (hPower : PowerCountingLaw NTarget) (hTLog : TLogCountingLaw NBase)
    (hEq : NTarget =ᶠ[atTop] NBase) : False

theorem abstract_nogo_of_boundedDifference
    (hPower : PowerCountingLaw NTarget) (hTLog : TLogCountingLaw NBase)
    (hBounded : BoundedDifference NTarget NBase) : False
```

Ambos reutilizam conversões já verificadas
(`subdominantTLog_of_eventualEquality`,
`subdominantTLog_of_boundedDifference`). O crescimento de `T log T` **não**
foi reprovado: `tendsto_norm_tLogScale_atTop` já existia.

**E3 (`RatioEquivalence`) não foi formalizado**, conforme o gate.
`SB-GAP-011` permanece aberto.

## Imports

```text
TamesisLab.RHNogo.AsymptoticCore
TamesisLab.RHNogo.Bridge
```

Somente esses dois. **`TamesisLab.RHNogo.Geometry` não é importado.**

## Separação da geometria — registro explícito

```text
W-ELLIPTIC-SCALAR-BRIDGE nao eh premissa Lean deste teorema.

O gate geometrico anterior produziu uma INTERFACE DOCUMENTAL, nao uma
instancia de PowerCountingLaw.

Nenhum resultado deste gate transforma um operador em PowerCountingLaw.

Nao existe em Lean nenhum termo do tipo PowerCountingLaw N para um N
proveniente de operador, porque nao existe tal N.
```
