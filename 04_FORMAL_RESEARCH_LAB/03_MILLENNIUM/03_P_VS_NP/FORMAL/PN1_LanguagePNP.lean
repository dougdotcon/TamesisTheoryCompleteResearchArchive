/-
PN-1 — rascunho autocontido, NÃO integrado.

Escopo (idêntico ao teste falsificável do item PN-1, versão revisada pelo
revisor adversarial): formaliza `Language.P` e `Language.NP` como predicados
sobre problemas de decisão, montados diretamente em cima do andaime já
existente em Mathlib para máquinas de Turing multi-fita limitadas em tempo
(`Turing.FinTM2` / `Turing.TM2ComputableInPolyTime`,
`Mathlib/Computability/TuringMachine/Computable.lean`). NÃO define uma nova
máquina de Turing "do zero" no sentido de teoria de complexidade original,
NÃO tenta nenhuma redução, NÃO tenta NP-completude, e absolutamente NÃO
decide, aproxima ou sugere resposta a P vs NP clássico. Ver
`GAP_REGISTER.yaml`/`PROOF_SKETCH.md` deste diretório para o item aberto
`PNP-GAP-001`, que é o que ficaria — mesmo em caso de sucesso total desta
sessão — permanentemente fora do escopo daqui.

Motivação de citação Mathlib (conferida por leitura direta nesta sessão,
`Mathlib/Computability/TuringMachine/Computable.lean`):
  * `structure FinTM2`                    — linha 46
  * `structure TM2ComputableInPolyTime`   — linhas 179-188 (`time : Polynomial ℕ`)
  * `def idComputer` / `def idComputableInPolyTime` — linhas ~204-230
    (único exemplo não-trivial pré-existente em toda a Mathlib desta revisão)
  * `proof_wanted TM2ComputableInPolyTime.comp` — linhas 284-288: a própria
    Mathlib ainda NÃO provou composição de duas máquinas
    `TM2ComputableInPolyTime` distintas; é um `proof_wanted`, i.e., um gap
    reconhecido oficialmente. Isso é usado abaixo para explicar exatamente
    até onde esta sessão consegue ir sem reconstruir essa peça de
    infraestrutura.

Correção do revisor adversarial em relação à proposta original: `∃ βΓ (eb :
Bool → List βΓ), TM2ComputableInPolyTime ea eb f` NÃO elabora, porque
`TM2ComputableInPolyTime` é uma `structure` (dado, em `Type`), não uma
`Prop`, e `Exists`/`∃` exige motivo em `Prop`. A correção usada aqui segue a
sugestão do revisor: envolver em `Nonempty`, e fixar o alfabeto de saída
`Bool` como `Computability.encodeBool` (dispensando o `∃ βΓ, ∃ eb`
desnecessário).

Passo 1 (fechado nesta sessão): `Language.P` definido via `Nonempty
(TM2ComputableInPolyTime ea Computability.encodeBool f)`, com witness
concreto (máquina construída à mão, no estilo de `idComputer`/
`idComputableInPolyTime`) para a linguagem trivial `Set.univ` sobre `Bool`.

Passo 2 (parcialmente fechado nesta sessão): `Language.NP` definido com
domínio de verificador `α × γ` e uma hipótese auxiliar explícita e SEPARADA
limitando o comprimento do certificado por um polinômio em `|ea x|`
(distinto do polinômio de tempo de execução, que é avaliado no comprimento
do par codificado inteiro `e (x, y)`) — exatamente a distinção
Cook–Karp que o revisor apontou como não trivial na proposta original. A
implicação `Language.P → Language.NP` com certificado trivial (`γ = Unit`,
certificado sempre codificado como lista vazia) FOI provada, reaproveitando
a MESMA máquina do witness de `Language.P` e reescrevendo com
`List.append_nil` — este caso particular não precisa do
`TM2ComputableInPolyTime.comp` ainda não provado em Mathlib, porque não há
duas máquinas distintas para compor: apenas um preenchimento (padding) do
input codificado com a lista vazia do certificado trivial.

O que NÃO foi tentado (fora de escopo desta sessão, não uma omissão
acidental): o caso GERAL de compor a máquina de `Language.P` com uma
segunda máquina arbitrária de leitura de certificado (necessário, por
exemplo, para uma prova genuína de NP-completude de um problema concreto)
precisaria exatamente do lema `TM2ComputableInPolyTime.comp`, que a própria
Mathlib marca como `proof_wanted` nesta revisão — não uma lacuna desta
sessão, mas uma lacuna já documentada rio acima, na própria biblioteca.
-/

import Mathlib.Computability.TuringMachine.Computable

namespace TamesisLab.LanguagePNP

open Turing Computability

/-! ### Passo 1 : `Language.P` -/

/-- `Language.P ea L` : existe uma máquina TM2 (multi-fita, limitada por um
polinômio no comprimento do input codificado por `ea`) que decide a
pertinência a `L`, com saída codificada por `Computability.encodeBool`.
Ver nota de cabeçalho sobre a correção `Nonempty` em relação à proposta
original (`∃ ... , TM2ComputableInPolyTime ...` não elabora, pois a
estrutura vive em `Type`, não em `Prop`). -/
def Language.P {α αΓ : Type} (ea : α → List αΓ) (L : Set α)
    [DecidablePred (· ∈ L)] : Prop :=
  Nonempty (TM2ComputableInPolyTime ea encodeBool (fun a => decide (a ∈ L)))

/-- Máquina auxiliar: ignora (via `pop`) o único símbolo do input codificado
por `encodeBool` (que tem sempre comprimento exatamente 1, pois
`encodeBool = pure`) e empilha (`push`) `true` na mesma pilha, que também é
a pilha de saída. Serve apenas de testemunha de que `Language.P` não é
vazia por acidente — mesmo papel que `idComputer` desempenha para a
identidade em Mathlib. -/
def constTrueMachine : FinTM2 where
  K := Unit
  k₀ := ()
  k₁ := ()
  Γ _ := Bool
  Λ := Unit
  main := ()
  σ := Unit
  initialState := ()
  m _ := Turing.TM2.Stmt.pop () (fun _ _ => ()) (Turing.TM2.Stmt.push () (fun _ => true) Turing.TM2.Stmt.halt)

noncomputable section

/-- `constTrueMachine` computa, em tempo polinomial (constante `1`), a
função constante `true : Bool → Bool` a partir da codificação
`Computability.encodeBool`. -/
def constTrueComputableInPolyTime :
    @TM2ComputableInPolyTime Bool Bool Bool Bool encodeBool encodeBool (fun _ => true) where
  tm := constTrueMachine
  inputAlphabet := Equiv.cast rfl
  outputAlphabet := Equiv.cast rfl
  time := 1
  outputsFun _ :=
    { steps := 1
      evals_in_steps := rfl
      steps_le_m := by simp }

/-- Witness concreto de que `Language.P` não é vácua: a linguagem trivial
`Set.univ` (sobre `Bool`, com a codificação `encodeBool`) está em `P`.
Prova completa, sem nenhuma premissa não justificada nem tática de
placeholder. -/
theorem languageP_univ_bool :
    Language.P (α := Bool) (αΓ := Bool) encodeBool (Set.univ : Set Bool) := by
  have hfun : (fun a : Bool => decide (a ∈ (Set.univ : Set Bool))) = fun _ : Bool => true := by
    funext a; rfl
  unfold Language.P
  rw [hfun]
  exact ⟨constTrueComputableInPolyTime⟩

end

/-! ### Passo 2 : `Language.NP` -/

/-- `Language.NP ea ey e L` : existe uma máquina TM2 verificadora, de
domínio `α × γ` codificado por `e`, decidindo `verify`, tal que (a) o
comprimento do certificado `ey y` é limitado por ALGUM polinômio no
comprimento do input original `ea x` — hipótese SEPARADA do polinômio de
tempo de execução, que (via `TM2ComputableInPolyTime.time`) é avaliado no
comprimento do PAR codificado inteiro `e (x, y)`, não em `ea x` isoladamente
— e (b) `a ∈ L` sse existe um certificado `c` aceito por `verify`. Esta é
exatamente a distinção Cook–Karp que o revisor adversarial apontou como
ausente na proposta original (que colapsava `|x|` e `|y|` em uma única
lista concatenada sem rastrear os dois comprimentos separadamente). -/
def Language.NP {α γ αΓ γΓ εΓ : Type} (ea : α → List αΓ) (ey : γ → List γΓ)
    (e : α × γ → List εΓ) (L : Set α) [DecidablePred (· ∈ L)] : Prop :=
  ∃ verify : α × γ → Bool,
    Nonempty (TM2ComputableInPolyTime e encodeBool verify) ∧
      (∃ p : Polynomial ℕ, ∀ x : α, ∀ y : γ, (ey y).length ≤ p.eval (ea x).length) ∧
      (∀ a : α, decide (a ∈ L) = true ↔ ∃ c : γ, verify (a, c) = true)

/-- Certificado trivial: `Unit`, sempre codificado como a lista vazia. -/
def trivialCertEnc {αΓ : Type} : Unit → List αΓ := fun _ => []

/-- Codificação do par `(x, certificado trivial)` : apenas `ea x`, "colada"
com a lista vazia. -/
def pairEncTrivial {α αΓ : Type} (ea : α → List αΓ) : α × Unit → List αΓ :=
  fun p => ea p.1 ++ trivialCertEnc p.2

/-- `Language.P ea L → Language.NP ea trivialCertEnc (pairEncTrivial ea) L`,
com certificado trivial `Unit`. Reaproveita a MESMA máquina do witness de
`Language.P` — não precisa de `TM2ComputableInPolyTime.comp` (ainda
`proof_wanted` em Mathlib nesta revisão, ver cabeçalho do arquivo), pois o
certificado trivial só acrescenta a lista vazia ao input codificado, e
`List.append_nil` identifica os dois inputs codificados. Prova completa,
sem nenhuma premissa não justificada nem tática de placeholder. -/
theorem languageP_to_NP {α αΓ : Type} (ea : α → List αΓ) (L : Set α)
    [DecidablePred (· ∈ L)] (h : Language.P ea L) :
    Language.NP ea (trivialCertEnc (αΓ := αΓ)) (pairEncTrivial ea) L := by
  obtain ⟨M⟩ := h
  refine ⟨fun p => decide (p.1 ∈ L), ?_, ⟨0, fun _ _ => by simp [trivialCertEnc]⟩, ?_⟩
  · refine ⟨{ tm := M.tm
              inputAlphabet := M.inputAlphabet
              outputAlphabet := M.outputAlphabet
              time := M.time
              outputsFun := ?_ }⟩
    intro p
    have hlen : pairEncTrivial ea p = ea p.1 := by
      simp [pairEncTrivial, trivialCertEnc]
    simp only [hlen]
    exact M.outputsFun p.1
  · intro a
    constructor
    · intro ha; exact ⟨(), ha⟩
    · rintro ⟨_, hc⟩; exact hc

end TamesisLab.LanguagePNP
