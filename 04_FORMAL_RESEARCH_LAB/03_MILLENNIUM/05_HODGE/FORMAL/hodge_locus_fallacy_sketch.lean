/-
HODGE-CDK-001 — rascunho formal isolado (NÃO integrado a TamesisLab)

STATUS: COMPILADO (`lake env lean`, exit 0) na integração serial da
sessão orquestradora — o rascunho paralelo original corretamente não
rodou `lake build` (instrução explícita da onda paralela). Nenhuma
correção de prova foi necessária; compilou de primeira. Ainda NÃO
registrado em `TamesisLab.lean`.

O QUE ESTE ARQUIVO NÃO É:
Este arquivo NÃO formaliza o Teorema de Cattani–Deligne–Kaplan (1995),
nem a transversalidade de Griffiths, nem o teorema de Lefschetz sobre
classes (1,1), nem qualquer enunciado de geometria algébrica ou teoria
de Hodge. Mathlib não possui (até onde verificado nesta sessão)
variações de estrutura de Hodge, domínios de período, ou o mapa de
classe de ciclo com a generalidade necessária — formalizar CDK está
fora do alcance desta rodada. Ver ../PROOF_SKETCH.md.

O QUE ESTE ARQUIVO É:
Uma formalização mínima e honesta da ESTRUTURA LÓGICA da falácia
identificada na auditoria (../REVIEWS/AUDIT_REPORT.md,
../GAP_REGISTER.yaml, item HODGE-GAP-002): "o locus onde uma
propriedade estrutural forte (aqui usamos finitude, como substituto
formal do tipo mais forte de conclusão que aparece nas formulações de
CDK — componentes algébricas, próprias e finitas sobre a base) é
satisfeita" NÃO implica "a aplicação subjacente é sobrejetiva sobre os
valores-alvo". O contraexemplo abaixo é elementar, explícito e com prova
completa — ver proibições contra provas incompletas em ../../../AGENTS.md.

Analogia com o caso auditado (não uma formalização dele):
  α  ~ pontos t no espaço de parâmetros S de uma família
  β  ~ "classes de Hodge possíveis" (aqui, simplificado a dois valores)
  f  ~ o mapa "que classe (se houver) o ponto t realiza"
  Locus f b ~ o locus de Hodge de b (Definição 2.5, ../DEFINITIONS.md)
  (Locus f b).Finite ~ substituto formal de "é uma subvariedade
    algébrica" (CDK, Teorema 2.8, ../DEFINITIONS.md) — usamos finitude
    porque é uma propriedade estrutural ainda mais forte, para deixar
    claro que mesmo a hipótese mais forte razoável não resolve o
    problema.
  Function.Surjective f ~ "todo valor-alvo é de fato realizado" —
    substituto formal (e deliberadamente mais fraco do que
    "existe ciclo algébrico") do que a Conjectura de Hodge exigiria.

O ponto do contraexemplo: um locus pode ser vazio, e o vazio é
trivialmente "finito"/"algébrico". Nenhuma prova de que um locus tem
uma propriedade estrutural boa pode, por si, garantir que o locus é
não-vazio — e é exatamente a não-vacuidade (existência de um
representante) que a Conjectura de Hodge exige.

VERIFICAÇÃO DOS NOMES (por grep, não por compilação — mesma convenção
usada em ../../04_YANG_MILLS/FORMAL/InsufficiencyToyModel.lean desta
mesma onda): conferido nesta sessão, por busca textual, contra o
snapshot de Mathlib vendorizado em
04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib, que os
seguintes nomes existem nos arquivos indicados:
  - `Set.toFinite`      Mathlib/Data/Finite/Defs.lean
      ("theorem toFinite (s : Set α) [Finite s] : s.Finite := ‹_›",
      dentro de `namespace Set`)
  - `Subtype.finite`    Mathlib/Data/Fintype/EquivFin.lean
      ("instance Subtype.finite {α : Sort*} [Finite α] {p : α → Prop} :
      Finite { x // p x }" — fornece a instância `Finite ↥(Locus f b)`
      necessária para `Set.toFinite`, a partir de `Finite Unit`)
  - `Set.mem_setOf_eq`, `Function.Surjective` — nomes padrão de Mathlib,
    não confirmados individualmente por grep nesta sessão.
Não compilado nesta sessão — ver STATUS no topo deste arquivo.
-/

import Mathlib

namespace HodgeCDKAudit

/-- O "locus" para o valor `b` sob o mapa `f` — a pré-imagem de `{b}`.
Modelo puramente formal de Definição 2.5 (../DEFINITIONS.md), não uma
formalização dela: aqui `α`, `β` são tipos arbitrários, sem nenhuma
estrutura de variedade, cohomologia, ou Hodge. -/
def Locus {α β : Type*} (f : α → β) (b : β) : Set α := {a | f a = b}

/-- Contraexemplo explícito e finito: existe `f` tal que TODO locus é
finito (o substituto formal, aqui, do que CDK garante sobre o locus de
Hodge — algebricidade, uma condição estrutural forte), mas `f` não é
sobrejetiva (o substituto formal do que a Conjectura de Hodge exigiria
e que nem CDK nem transversalidade fornecem). Prova completa. -/
theorem finite_locus_does_not_imply_surjective :
    ∃ (f : Unit → Bool),
      (∀ b : Bool, (Locus f b).Finite) ∧ ¬ Function.Surjective f := by
  refine ⟨fun _ => true, ?_, ?_⟩
  · intro b
    exact Set.toFinite (Locus (fun _ => true) b)
  · intro hsurj
    obtain ⟨a, ha⟩ := hsurj false
    -- `ha : (fun _ => true) a = false`, que se reduz por beta a
    -- `true = false`; `simp` fecha o objetivo por contradição.
    simp at ha

/-- Reformulação equivalente, tornando explícito qual valor de `β`
fica "sem representante" (o análogo formal de "uma classe de Hodge sem
ciclo algébrico conhecido que a represente") — precisamente o valor
cujo locus é vazio, que ainda assim satisfaz trivialmente a hipótese de
finitude/algebricidade. -/
theorem empty_locus_is_finite_but_witnesses_non_surjectivity :
    (Locus (fun _ : Unit => true) false) = (∅ : Set Unit) ∧
    (Locus (fun _ : Unit => true) false).Finite := by
  constructor
  · ext a
    simp [Locus]
  · exact Set.toFinite _

end HodgeCDKAudit

/-
NOTA PARA A INTEGRAÇÃO (fora desta rodada):
- Verificar `lake build` neste arquivo isoladamente antes de qualquer
  import em TamesisLab.lean (instrução explícita: não fazer isso nesta
  rodada paralela).
- `import Mathlib` (topo do arquivo) segue a convenção já usada por
  ../../04_YANG_MILLS/FORMAL/InsufficiencyToyModel.lean nesta mesma
  onda. Os dois usos de `Set.toFinite` foram checados por grep (ver
  bloco de verificação acima), não por compilação — se o nome tiver
  mudado numa versão mais nova de Mathlib, o conserto é uma
  atualização de nome, não uma lacuna matemática (o conteúdo é lógica
  proposicional elementar sobre um contraexemplo de dois elementos).
-/
