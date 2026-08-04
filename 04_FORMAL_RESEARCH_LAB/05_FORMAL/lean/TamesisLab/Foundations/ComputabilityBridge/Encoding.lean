import TamesisLab.Engineering.FiniteStateEncoding
import Mathlib.Computability.Primrec.List

set_option autoImplicit false

/-!
# FOUND-COMPUTABILITY-BRIDGE-001 — a ponte

`CertifiedFiniteEncoding` tem exatamente os quatro campos de uma
equivalência: dois dados e duas leis. Ela **é** um `S ≃ Fin n`, e
`Primcodable.ofEquiv` se aplica direto.

```text
encode, decode                dados
decode_encode, encode_decode  as duas leis
                              = toFun, invFun, left_inv, right_inv
```

Esta é a primeira vez que o laboratório toca `Mathlib.Computability`.

## O que a ponte NÃO é

A instância induzida **não é canônica**. `Primcodable Bool`, por
exemplo, já existe no Mathlib e é diferente de
`encodingPrimcodable boolEncoding`. Enunciados sob uma não são,
sintaticamente, enunciados sob a outra — ver `CB-GAP-010`.
-/

namespace TamesisLab.Foundations.ComputabilityBridge

open TamesisLab.Engineering.FiniteStateEncoding

variable {S : Type*} {n : Nat}

/-- A codificação certificada, lida como equivalência.

Nenhum campo é acrescentado e nenhum é descartado: os quatro campos da
estrutura são os quatro campos de `Equiv`, na ordem. -/
def encodingEquiv (e : CertifiedFiniteEncoding S n) : S ≃ Fin n where
  toFun := e.encode
  invFun := e.decode
  left_inv := e.decode_encode
  right_inv := e.encode_decode

/-- **A ponte.** Toda codificação certificada coloca seu tipo dentro da
hierarquia de computabilidade do Mathlib.

Não é `instance`: toma um argumento explícito, e registrá-la globalmente
poria a resolução de instâncias a procurar codificações. -/
@[instance_reducible]
def encodingPrimcodable (e : CertifiedFiniteEncoding S n) : Primcodable S :=
  Primcodable.ofEquiv (Fin n) (encodingEquiv e)

/-- O tipo codificado é finito.

É esta finitude — e **só** ela — que faz todo o trabalho em
`Classification.lean`. -/
theorem finite_of_encoding (e : CertifiedFiniteEncoding S n) : Finite S :=
  Finite.of_equiv _ (encodingEquiv e).symm

/-- **A armadilha de vacuidade, nomeada.**

Em `n = 0` o tipo é vazio, e tudo que se diga sobre ele é vácuo. O mesmo
defeito derrubou `FOUND-MONOVARIANT-DESCENT-001`; aqui ele está escrito
como teorema antes que alguém caia nele. -/
theorem isEmpty_of_encoding_zero (e : CertifiedFiniteEncoding S 0) : IsEmpty S :=
  ⟨fun s => (e.encode s).elim0⟩

end TamesisLab.Foundations.ComputabilityBridge
