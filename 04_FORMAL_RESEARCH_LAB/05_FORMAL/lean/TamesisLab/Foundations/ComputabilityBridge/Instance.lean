import TamesisLab.Foundations.ComputabilityBridge.Encoding

set_option autoImplicit false

/-!
# FOUND-COMPUTABILITY-BRIDGE-001 — instâncias, TEST_ONLY

Duas codificações que existem para sustentar a **instância positiva**
exigida pela governança, e o seu contraste.

```text
boolEncoding    Bool,  n = 2   HABITADO    o caso positivo
emptyEncoding   Empty, n = 0   VAZIO       o caso vacuo
```

`CertifiedFiniteEncoding S 0` força `IsEmpty S`. É a mesma armadilha que
derrubou `FOUND-MONOVARIANT-DESCENT-001`, e as duas pontas estão no mesmo
arquivo de propósito.
-/

namespace TamesisLab.Foundations.ComputabilityBridge

open TamesisLab.Engineering.FiniteStateEncoding

/-- `false ↔ 0`, `true ↔ 1`. Tipo **habitado**, `n = 2 > 0`. -/
def boolEncoding : CertifiedFiniteEncoding Bool 2 where
  encode := fun b => if b then ⟨1, by decide⟩ else ⟨0, by decide⟩
  decode := fun i => decide (i.val = 1)
  decode_encode := by decide
  encode_decode := by decide

/-- `Empty ↔ Fin 0`. O caso **vácuo**, exibido em vez de escondido. -/
def emptyEncoding : CertifiedFiniteEncoding Empty 0 where
  encode := fun s => s.elim
  decode := fun i => absurd i.isLt (Nat.not_lt_zero _)
  decode_encode := fun s => s.elim
  encode_decode := fun i => absurd i.isLt (Nat.not_lt_zero _)

end TamesisLab.Foundations.ComputabilityBridge
