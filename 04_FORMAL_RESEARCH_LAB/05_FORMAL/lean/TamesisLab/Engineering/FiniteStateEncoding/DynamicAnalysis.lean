import TamesisLab.Engineering.FiniteStateEncoding.Commutation

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-ENCODING-001 — análise dinâmica tipada

O consumidor fornece **três coisas**: a codificação, o passo tipado e o
estado inicial. Nenhuma typeclass.

A soundness termina numa igualdade **em `S`** — não sobre `Nat`, não
sobre `Fin n`, não sobre o `Array`. Esse é o resultado que separa esta
frente da anterior.

A completeness **não exige pré-condição alguma** do consumidor: a
validade da tabela e o domínio do índice são consequências da
construção.
-/

namespace TamesisLab.Engineering.FiniteStateEncoding

open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection

variable {S : Type*} {n : Nat}

/-- Analisa um sistema determinístico tipado, através de sua codificação.

Uma linha de corpo: constrói a tabela e chama a API já verificada. O tipo
de resultado é reutilizado sem alteração — nenhum construtor de erro é
criado ou removido, nenhum certificado padrão existe, e o detector
subjacente **não** é totalizado. -/
def analyzeEncodedSystem (encoding : CertifiedFiniteEncoding S n) (stepS : S → S)
    (start : S) : Except RuntimeCycleError CycleWitness :=
  analyzeTransitionTable (buildTransitionTable encoding stepS).toRaw
    ((encoding.encode start : Fin n) : Nat)

/-- **Soundness tipada.**

Se a análise devolve um certificado, a repetição vale **entre iteradas de
`stepS`, no tipo `S`**.

```text
analyzeTransitionTable_sound
  -> igualdade entre run? sobre o Array construido
      -> run?_corresponds_to_typed_iterate, nos dois lados
          -> Option.some.inj
              -> Fin.ext
                  -> encode_injective
                      -> igualdade em S
```

Nada é afirmado sobre minimalidade, unicidade ou invariância sob
recodificação. -/
theorem analyzeEncodedSystem_sound {encoding : CertifiedFiniteEncoding S n}
    {stepS : S → S} {start : S} {witness : CycleWitness}
    (h : analyzeEncodedSystem encoding stepS start = .ok witness) :
    stepS^[witness.baseIndex + witness.period] start = stepS^[witness.baseIndex] start := by
  have hrun := (analyzeTransitionTable_sound h).2.2
  rw [encoding.run?_corresponds_to_typed_iterate stepS
        (witness.baseIndex + witness.period) start,
      encoding.run?_corresponds_to_typed_iterate stepS witness.baseIndex start] at hrun
  exact encoding.encode_injective (Fin.ext (Option.some.inj hrun))

/-- **Completeness tipada.**

Toda entrada tipada produz certificado, **sem pré-condição alguma**.

A frente anterior exigia do chamador a validade da tabela e o domínio do
índice; aqui as duas vêm da construção — `toRaw_valid` e
`buildTransitionTable_size`.

A casa dos pombos não é repetida: ela permanece onde foi provada. -/
theorem analyzeEncodedSystem_complete (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (start : S) :
    ∃ witness, analyzeEncodedSystem encoding stepS start = .ok witness := by
  have hStart : ((encoding.encode start : Fin n) : Nat)
      < (buildTransitionTable encoding stepS).next.size := by
    rw [buildTransitionTable_size]
    exact (encoding.encode start).isLt
  exact analyzeTransitionTable_complete _ _
    (buildTransitionTable encoding stepS).toRaw_valid hStart

/-- Nenhum erro é alcançável, qualquer que seja o construtor.

Um único corolário quantificado sobre `err` substitui três exclusões
individuais. Os construtores **permanecem** no tipo executável: a
impossibilidade é teorema, não motivo de remoção. -/
theorem analyzeEncodedSystem_ne_error (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (start : S) (err : RuntimeCycleError) :
    analyzeEncodedSystem encoding stepS start ≠ .error err := by
  intro hError
  obtain ⟨witness, hOk⟩ := analyzeEncodedSystem_complete encoding stepS start
  rw [hOk] at hError
  cases hError

end TamesisLab.Engineering.FiniteStateEncoding
