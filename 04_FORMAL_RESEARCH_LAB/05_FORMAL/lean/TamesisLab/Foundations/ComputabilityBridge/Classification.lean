import TamesisLab.Foundations.ComputabilityBridge.ResultCodes
import Mathlib.Computability.Halting

set_option autoImplicit false

/-!
# FOUND-COMPUTABILITY-BRIDGE-001 — a classificação, e o seu limite

**O resultado central desta frente é NEGATIVO.**

`primrec_of_encoding` prova que toda função que sai de um tipo com
codificação certificada é primitiva recursiva. Seu corpo é
`Primrec.dom_finite f`, e **nunca consulta a definição de `f`**.

```text
o detector e Primrec              SIM
porque a busca e limitada         NAO
porque o dominio e finito         SIM
a classificacao distingue o
detector de uma tabela de
consulta                          NAO
```

Quem quisesse usar "o detector do laboratório é `Primrec`" como degrau
para classe de complexidade **não pode**: a afirmação é verdadeira e
vazia de conteúdo algorítmico.

## Onde a pergunta deixa de ser vácua

No nível **uniforme**, sobre `RawTransitionTable × Nat`, o domínio é
infinito, `dom_finite` não se aplica, e a classificação passa a depender
do algoritmo. `UniformPrimrecStatement` existe para provar que o
enunciado **elabora**; a prova não é tentada — `CB-GAP-001`.
-/

namespace TamesisLab.Foundations.ComputabilityBridge

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection

variable {S : Type*} {n : Nat}

/-- **A declaração central, e é negativa.**

Toda função que sai de um tipo com codificação certificada é primitiva
recursiva. A prova não olha a função: quem decide é a finitude do
domínio. -/
theorem primrec_of_encoding (e : CertifiedFiniteEncoding S n) {σ : Type*}
    [Primcodable σ] (f : S → σ) :
    haveI := encodingPrimcodable e
    Primrec f :=
  letI := encodingPrimcodable e
  haveI := finite_of_encoding e
  Primrec.dom_finite f

/-- A análise executável do laboratório é `Primrec`.

Corolário de **uma linha**, e é exatamente esse o ponto: a conclusão não
depende de nada que a análise faça. -/
theorem primrec_analyzeEncodedSystem (e : CertifiedFiniteEncoding S n)
    (stepS : S → S) :
    haveI := encodingPrimcodable e
    Primrec (analyzeEncodedSystem e stepS) :=
  primrec_of_encoding e _

/-- E, a fortiori, `Computable`. -/
theorem computable_analyzeEncodedSystem (e : CertifiedFiniteEncoding S n)
    (stepS : S → S) :
    haveI := encodingPrimcodable e
    Computable (analyzeEncodedSystem e stepS) :=
  letI := encodingPrimcodable e
  (primrec_analyzeEncodedSystem e stepS).to_comp

/-- Todo predicado sobre um tipo codificado é `ComputablePred`.

Inclusive predicados para os quais ninguém escreveu algoritmo: a
decidibilidade vem de `Classical.propDecidable` e a computabilidade da
finitude. É a mesma vacuidade, vista no lado dos predicados. -/
theorem computablePred_of_encoding (e : CertifiedFiniteEncoding S n)
    (p : S → Prop) :
    haveI := encodingPrimcodable e
    ComputablePred p := by
  letI := encodingPrimcodable e
  haveI := finite_of_encoding e
  classical
  exact ⟨fun s => Classical.propDecidable (p s),
    (Primrec.dom_finite (fun s => decide (p s))).to_comp⟩

/-- **O enunciado uniforme.**

`def : Prop`, **não** teorema. Ela demonstra que o enunciado elabora e
nada mais. Provar `Primrec₂ analyzeTransitionTable` exigiria mostrar que
a busca limitada é primitiva recursiva sobre um domínio **infinito** —
trabalho real, de gate próprio.

A alternativa rejeitada, e o porquê, estão em `STOP_CONDITIONS.md`:
mantê-los aqui faria a auditoria de tokens encontrar a própria
documentação, defeito já registrado em `FOUND-CYCLE-DETECTION-001`. -/
def UniformPrimrecStatement : Prop :=
  Primrec₂ analyzeTransitionTable

end TamesisLab.Foundations.ComputabilityBridge
