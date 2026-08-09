/-
PN-4 — rascunho autocontido, NÃO integrado (não importado por
`TamesisLab.lean`; verificado isoladamente via `lake env lean` sobre este
arquivo, contra o cache já compilado da Mathlib).

Escopo (teste falsificável do item PN-4, conforme proposto e confirmado
"SURVIVES" pelo revisor adversarial): esta sessão NÃO ataca P vs NP, e
sequer toca em relativização no sentido de Baker–Gill–Solovay (BGS 1975,
oráculos A,B com P^A = NP^A e P^B ≠ NP^B, já citado em
`REVIEWS/AUDIT_REPORT.md` item 1 deste diretório). O que existe hoje na
Mathlib (`Mathlib/Computability/RecursiveIn.lean`, 2025, Tanner Duve/Elan
Roth) é computabilidade relativa a oráculo NO SENTIDO DA TEORIA CLÁSSICA
DA RECURSÃO — recursivo/parcial-recursivo SEM limite de tempo — não o
modelo de máquina de Turing com LIMITE POLINOMIAL DE TEMPO e acesso a
oráculo que BGS exige. Confirmado nesta sessão por busca em todo
`Mathlib/Computability/*.lean` e `Mathlib/Computability/TuringMachine/*.lean`
fora de `RecursiveIn.lean`/`TuringDegree.lean`: zero ocorrências da palavra
"oracle" — ou seja, não existe em nenhum lugar da Mathlib desta revisão uma
máquina de Turing multi-fita limitada em tempo com acesso a oráculo (nada
análogo a um `TM2ComputableInPolyTime` "com oráculo"). Por isso, mesmo em
caso de sucesso TOTAL desta sessão, o resultado abaixo é teoria da recursão
lida com o nome "relativização" — não dá NENHUM passo em direção à barreira
BGS propriamente dita, que é sobre tempo limitado. Este arquivo declara
isso explicitamente e não reivindica o contrário em nenhum comentário.
NÃO decide, aproxima ou sugere resposta a P vs NP clássico. NÃO reclama
novidade matemática.

Motivação (citações conferidas por leitura direta nesta sessão):
  * `protected inductive Nat.RecursiveIn (O : Set (ℕ →. ℕ)) : (ℕ →. ℕ) → Prop`
    — `RecursiveIn.lean:61-79`, construtores `zero`/`succ`/`left`/`right`/
    `oracle`/`pair`/`comp`/`prec`/`rfind`. O construtor usado abaixo é
    `oracle : ∀ g ∈ O, Nat.RecursiveIn O g` (linha 66).
  * `theorem Partrec.nat_iff {f : ℕ →. ℕ} : Partrec f ↔ Nat.Partrec f` —
    `Mathlib/Computability/Partrec.lean:432`, usada para transportar a
    hipótese de refutação `Nat.Partrec haltingIndicator` para
    `Computable haltingIndicatorTotal` (via `Computable f := Partrec
    (f : α →. σ)`, `Partrec.lean:244`).
  * `theorem ComputablePred.halting_problem (n) :
    ¬ComputablePred fun c => (eval c n).Dom` — `Halting.lean:65`, o fato de
    indecidibilidade já formalizado que esta sessão reaproveita (via
    Teorema de Rice, já provado na própria Mathlib) para refutar
    `Nat.Partrec haltingIndicator`.
  * `theorem ComputablePred.computable_iff {p : α → Prop} :
    ComputablePred p ↔ ∃ f : α → Bool, Computable f ∧ p = fun a => (f a : Prop)`
    — `RE.lean:172-174`, usada para converter o testemunho de
    computabilidade construído aqui num elemento de `ComputablePred`.
  * `Nat.Partrec.Code`, `Nat.Partrec.Code.eval : Code → ℕ →. ℕ`,
    `instance instDenumerable : Denumerable Code` — `PartrecCode.lean:176`
    (o "índice de programas" que permite falar de "o programa número m",
    usado abaixo via `Denumerable.ofNat Code m` / `Encodable.encode`).

Achado técnico de encaixe (a única parte não totalmente mecânica desta
sessão): o predicado de parada de Mathlib, `halting_problem`, está
formulado sobre `Code` (o tipo dos índices de programa), não sobre `ℕ`
diretamente — enquanto `Nat.RecursiveIn` exige um oráculo literalmente em
`ℕ →. ℕ`. A ponte entre os dois usa exclusivamente peças já provadas na
Mathlib (`Primrec.encode`, `Primrec.ofNat`, `Denumerable.ofNat_encode`),
sem nenhuma premissa nova além dessas. Isso NÃO é o "encoding gap" que a
proposta original cogitava como resultado negativo possível — a ponte
existiu e fechou nesta sessão, e é registrada abaixo com as citações
exatas usadas.

O teste, em termos concretos: `haltingIndicator : ℕ →. ℕ` é a função
(construída via `Classical.propDecidable`, portanto NÃO computável em
nenhum sentido construtivo — esse é justamente o ponto) que, no índice `m`
de um programa (`Nat.Partrec.Code`), devolve `1` se esse programa PARA ao
rodar sobre a entrada `0`, e `0` caso contrário. `O := {haltingIndicator}`
é o oráculo singleto. Prova-se (a) `Nat.RecursiveIn O haltingIndicator`
diretamente pelo construtor `.oracle` (porque `haltingIndicator` pertence
trivialmente a `O`, um fato de pertencimento a singleto, sem nenhum
cálculo), e (b) `¬ Nat.Partrec haltingIndicator` (a MESMA função, agora
SEM acesso a si mesma como oráculo, deixa de ser parcial-recursiva) —
reduzindo isso à indecidibilidade do problema da parada já formalizada em
`ComputablePred.halting_problem`. As duas provas juntas confirmam a
composição limpa entre `RecursiveIn.lean` (2025) e a infraestrutura mais
antiga do problema da parada em `Halting.lean`/`RE.lean`, exatamente o que
a proposta original pedia como teste falsificável.

O que continua faltando (mesmo em caso de sucesso total desta sessão,
declarado com honestidade, como pedido): nada aqui envolve LIMITE DE
TEMPO. `Nat.RecursiveIn` e `Nat.Partrec` são noções de computabilidade
IRRESTRITA (o programa pode rodar por tempo arbitrário, até parar ou
nunca parar). A distinção P vs NP relativizada de BGS é inteiramente sobre
o que uma máquina consegue decidir DENTRO de um polinômio de passos, com
consultas ao oráculo contadas nesse mesmo orçamento de tempo — um universo
matemático diferente, que a teoria clássica da recursão (à qual este
arquivo pertence) não modela nem aproxima. Formalizar BGS de verdade
exigiria construir do zero um modelo de máquina de Turing multi-fita COM
acesso a oráculo E limitada em tempo polinomial (nada disso existe hoje na
Mathlib, confirmado por busca nesta sessão) — uma peça de infraestrutura
comparável em esforço a `Turing.FinTM2`/`TM2ComputableInPolyTime`
(`Computable.lean`, já citado nos arquivos-irmãos `PN1_LanguagePNP.lean`/
`PN3_NegationWitness.lean` deste mesmo diretório) mas com um oráculo a
mais — não tentada aqui, fora de escopo desta sessão.
-/

import Mathlib.Computability.RecursiveIn
import Mathlib.Computability.Halting

namespace TamesisLab.OracleHaltingProbe

open Classical

/-! ### O oráculo: um indicador de parada construído classicamente

`haltingIndicatorTotal m` decide (via `Classical.propDecidable`, não de
forma construtiva) se o programa de índice `m` (decodificado como
`Nat.Partrec.Code` por `Denumerable.ofNat`) pára ao ser executado sobre a
entrada `0`. Esta seção é `noncomputable` porque essa decisão NÃO é
computável em sentido construtivo — é exatamente essa não-computabilidade
que o segundo teorema abaixo (`haltingIndicator_not_partrec`) explora. -/
noncomputable section

/-- Versão total (`ℕ → ℕ`) do indicador de parada: `1` se o programa de
índice `m` pára sobre a entrada `0`, `0` caso contrário. -/
def haltingIndicatorTotal (m : ℕ) : ℕ :=
  if (Nat.Partrec.Code.eval (Denumerable.ofNat Nat.Partrec.Code m) 0).Dom then 1 else 0

/-- O oráculo propriamente dito, como função parcial `ℕ →. ℕ` (levantada de
`haltingIndicatorTotal` via `Part.some`, sempre definida). -/
def haltingIndicator : ℕ →. ℕ := fun m => Part.some (haltingIndicatorTotal m)

/-- O oráculo singleto `O = {haltingIndicator}` pedido pelo teste
falsificável original. -/
def oracleSet : Set (ℕ →. ℕ) := {haltingIndicator}

end

/-! ### Parte (a) : `Nat.RecursiveIn oracleSet haltingIndicator` via `.oracle`

Fato trivial de pertencimento a um conjunto singleto — sem nenhum cálculo
de computabilidade real, exatamente como o construtor `oracle` prevê
(`Nat.RecursiveIn O g` para qualquer `g ∈ O`, independentemente de `g` ser
ou não parcial-recursiva por si só). -/
theorem haltingIndicator_recursiveIn_singleton :
    Nat.RecursiveIn oracleSet haltingIndicator :=
  Nat.RecursiveIn.oracle haltingIndicator rfl

/-! ### Parte (b) : `¬ Nat.Partrec haltingIndicator`

A mesma função, agora sem se ter a si mesma como oráculo disponível,
deixa de ser parcial-recursiva. A prova reduz isso à indecidibilidade do
problema da parada já formalizada em `ComputablePred.halting_problem`
(via o Teorema de Rice, ambos já provados na Mathlib, não reprovados
aqui). -/

/-- Ponte auxiliar: `haltingIndicatorTotal` no índice de um programa `c`
concreto (via `Encodable.encode`) coincide com a pergunta "esse programa
`c` pára sobre a entrada `0`?", codificada como `1`/`0`. Usa apenas
`Denumerable.ofNat_encode` (a identidade de ida-e-volta índice ↔ programa)
e análise de casos sobre a condição de parada. -/
theorem halts_iff_indicator_eq_one (c : Nat.Partrec.Code) :
    (Nat.Partrec.Code.eval c 0).Dom ↔ haltingIndicatorTotal (Encodable.encode c) = 1 := by
  unfold haltingIndicatorTotal
  rw [Denumerable.ofNat_encode]
  by_cases h : (Nat.Partrec.Code.eval c 0).Dom
  · simp [h]
  · simp [h]

theorem haltingIndicator_not_partrec : ¬ Nat.Partrec haltingIndicator := by
  intro hP
  -- `Nat.Partrec haltingIndicator` transportado para `Computable
  -- haltingIndicatorTotal` via `Partrec.nat_iff` (definicionalmente, pois
  -- `haltingIndicator` é o levantamento `PFun.lift haltingIndicatorTotal`).
  have hComp : Computable haltingIndicatorTotal := Partrec.nat_iff.2 hP
  -- Igualdade a `1` é decidível de forma genuinamente construtiva em `ℕ`
  -- (via `Primrec.eq`, não via `Classical.propDecidable`).
  have hEqOneNat : Primrec (fun n : ℕ => decide (n = 1)) :=
    Primrec.eq.decide.comp Primrec.id (Primrec.const 1)
  have hCompDecide : Computable (fun n : ℕ => decide (haltingIndicatorTotal n = 1)) :=
    hEqOneNat.to_comp.comp hComp
  have hg : Computable
      (fun c : Nat.Partrec.Code => decide (haltingIndicatorTotal (Encodable.encode c) = 1)) :=
    hCompDecide.comp Primrec.encode.to_comp
  have hCP : ComputablePred (fun c : Nat.Partrec.Code => (Nat.Partrec.Code.eval c 0).Dom) := by
    rw [ComputablePred.computable_iff]
    refine ⟨fun c => decide (haltingIndicatorTotal (Encodable.encode c) = 1), hg, ?_⟩
    funext c
    apply propext
    rw [show (decide (haltingIndicatorTotal (Encodable.encode c) = 1) : Prop)
          ↔ haltingIndicatorTotal (Encodable.encode c) = 1 from decide_eq_true_iff]
    exact halts_iff_indicator_eq_one c
  exact ComputablePred.halting_problem 0 hCP

/-! ### Auditoria de dependência lógica

Verificação obrigatória do protocolo de governança do laboratório: para
cada declaração acima, confirmar que nada além de `[propext,
Classical.choice, Quot.sound]` aparece (i.e. nenhuma premissa local extra
não justificada, nenhuma falha silenciosa de síntese de instância
introduzindo `sorryAx`). O uso de `Classical.choice` é ESPERADO aqui —
`haltingIndicatorTotal` é construído via `Classical.propDecidable`, que
depende de `Classical.choice` — e não é um enfraquecimento indevido do
enunciado: é exatamente o que torna `haltingIndicator` um oráculo bem
definido, porém não computável. -/

#print axioms TamesisLab.OracleHaltingProbe.haltingIndicatorTotal
#print axioms TamesisLab.OracleHaltingProbe.haltingIndicator
#print axioms TamesisLab.OracleHaltingProbe.haltingIndicator_recursiveIn_singleton
#print axioms TamesisLab.OracleHaltingProbe.halts_iff_indicator_eq_one
#print axioms TamesisLab.OracleHaltingProbe.haltingIndicator_not_partrec

end TamesisLab.OracleHaltingProbe
