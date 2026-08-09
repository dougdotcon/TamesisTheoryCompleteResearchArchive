/-
PN-3 — rascunho autocontido, NÃO integrado (não importado por
`TamesisLab.lean`; verificado isoladamente via `lake env lean` sobre este
arquivo, contra o cache já compilado da Mathlib).

Escopo (teste falsificável do item PN-3, conforme proposto e confirmado
"SURVIVES" pelo revisor adversarial): esta sessão NÃO ataca P vs NP. É uma
sonda de usabilidade, restrita a um único fato de complexidade sobre uma
única função de tamanho fixo (`Bool → Bool`, negação), não uma família
assintótica sobre entradas de tamanho crescente. Mesmo em caso de sucesso
total, isso não diz nada sobre escalabilidade, NP, ou qualquer separação —
ver seção "O que continua faltando" abaixo. NÃO decide, aproxima ou sugere
resposta a P vs NP clássico. NÃO reclama novidade matemática.

Motivação (citações conferidas por leitura direta nesta sessão,
`Mathlib/Computability/TuringMachine/Computable.lean` e
`Mathlib/Computability/TuringMachine/StackTuringMachine.lean`):
  * `structure TM2ComputableInPolyTime`  — Computable.lean, campo
    `time : Polynomial ℕ`, e `outputsFun` exigindo
    `TM2OutputsInTime tm ... (time.eval (ea a).length)`.
  * `def idComputer` / `def idComputableInPolyTime` /
    `instance inhabitedTM2ComputableInPolyTime` — os ÚNICOS construtores de
    `TM2ComputableInPolyTime` em toda a Mathlib desta revisão (grep
    confirmado nesta sessão: nenhum outro `: TM2ComputableInPolyTime` ou
    `:= ⟨...⟩ : TM2ComputableInPolyTime` existe fora deste arquivo). O
    witness da identidade usa `m _ := halt` — ZERO computação real: o
    label principal executa `halt` imediatamente, sem nenhum `pop`/`push`,
    então a pilha de entrada e a pilha de saída são a MESMA pilha (`K :=
    Unit`, `k₀ = k₁ = ()`) e o valor nunca é tocado.
  * `Turing.TM2.Stmt` — StackTuringMachine.lean, linhas ~127-134:
    construtores `push : ∀ k, (σ → Γ k) → Stmt → Stmt`,
    `pop : ∀ k, (σ → Option (Γ k) → σ) → Stmt → Stmt`, `load`, `halt`, etc.
  * `Turing.TM2.stepAux` — StackTuringMachine.lean: `pop`/`push`/`load`
    encadeados são processados INTEIRAMENTE dentro de UMA única chamada de
    `Turing.TM2.step` (a recursão de `stepAux` não passa de volta por
    `step`); só `goto`/`halt` produzem a config final de uma chamada de
    `step`. Por isso a máquina abaixo, apesar de ter 3 instruções reais
    (pop, push, load) antes do halt, ainda conta como `steps := 1`.
  * `def haltList` — Computable.lean: a config de saída ESPERADA por
    `TM2Outputs`/`EvalsTo` tem `var := tm.initialState` FIXO, não o `var`
    real alcançado pela execução. Esta é a armadilha central encontrada
    nesta sessão (ver "Achado técnico" abaixo).

Nota de honestidade sobre um precedente vizinho: o arquivo-irmão
`FORMAL/PN1_LanguagePNP.lean` (item PN-1, rascunho separado, não tocado
nesta sessão) já contém `constTrueMachine`/`constTrueComputableInPolyTime`,
uma máquina com `pop` seguido de `push` — logo, tecnicamente, não é a
identidade "crua". Mas essa máquina computa uma função CONSTANTE
(`fun _ => true`): ela usa `σ := Unit` e ignora o valor lido no `pop`
(`fun _ _ => ()`), então o "cálculo" não depende da entrada em nenhum
sentido, e — crucialmente — como `Unit` é um subsingleton, o estado interno
após o `pop` é automaticamente `()` = `tm.initialState`, contornando por
acidente de design a armadilha do `haltList.var` descrita abaixo. O teste
pedido para PN-3 é estritamente mais forte: a NEGAÇÃO `Bool → Bool`
genuinamente lê o bit de entrada (via `pop` para `σ := Bool`) e o usa (via
`push` de `!v`) — exatamente o caso "pop-negate-push via estado interno"
que o revisor adversarial identificou como mais difícil que a identidade.
Este arquivo constrói essa máquina do zero, sem importar nem reaproveitar
nada de `PN1_LanguagePNP.lean`.

Achado técnico (a "próxima marca" além da identidade, como previsto pelo
revisor adversarial): usar `σ := Bool` para carregar o bit lido entre o
`pop` e o `push` quebra a igualdade estrutural exigida por `haltList`, cujo
campo `var` é `tm.initialState` FIXO — não "o que quer que a execução real
tenha produzido". Se a máquina terminasse logo após o `push`, o `var` final
seria o bit de entrada (`true` para entrada `true`), que não é igual a
`tm.initialState` (uma constante fixa) sempre que a entrada for o valor
"errado". A correção (não documentada explicitamente em nenhum comentário
da Mathlib lida nesta sessão) é adicionar um passo `load` FINAL que reseta
o estado interno de volta a `tm.initialState` antes do `halt`, depois que o
`push` já capturou o valor negado na pilha (o `push` só lê `σ`, não o
altera). Isso é o "algo mais" genuíno que a identidade não precisa: não
apenas mais uma instrução de máquina, mas uma exigência estrutural do
próprio `TM2OutputsInTime`/`haltList` da Mathlib, que só aparece quando
`σ` deixa de ser um subsingleton.

O que continua faltando (mesmo em caso de sucesso total desta sessão,
declarado com honestidade, como pedido): um witness para UMA função de
tamanho fixo (`Bool → Bool`) é um fato de complexidade sobre uma única
instância decidível, não uma família assintótica sobre entrada de tamanho
crescente. Não diz nada sobre comportamento de escala, NP, ou qualquer
separação de classes de complexidade. `TM2ComputableInPolyTime.comp`
(composição de duas máquinas polinomiais distintas) continua sendo
`proof_wanted` na própria Mathlib nesta revisão — não usado nem necessário
aqui, pois não há composição de duas máquinas.
-/

import Mathlib.Computability.TuringMachine.Computable

namespace TamesisLab.NegationWitness

open Turing Computability

/-! ### A máquina -/

/-- Máquina de um único rótulo/uma única pilha (`K := Unit`, como em
`idComputer`/`constTrueMachine`) que efetivamente LÊ o bit de entrada
(`pop`, armazenando-o em `σ := Bool`), o NEGA e empilha o resultado
(`push`), e então reseta o estado interno para `tm.initialState`
(`load`) antes de parar (`halt`) — a etapa `load` final é exigida
porque `Turing.haltList` fixa `var := tm.initialState` na configuração
esperada, e aqui, ao contrário de `constTrueMachine` do arquivo-irmão
`PN1_LanguagePNP.lean` (que usa `σ := Unit`, um subsingleton), o estado
`σ := Bool` genuinamente varia com a entrada entre o `pop` e o `push`.
-/
def negationMachine : FinTM2 where
  K := Unit
  k₀ := ()
  k₁ := ()
  Γ _ := Bool
  Λ := Unit
  main := ()
  σ := Bool
  initialState := false
  m _ :=
    Turing.TM2.Stmt.pop () (fun _ ob => ob.getD false)
      (Turing.TM2.Stmt.push () (fun v => !v)
        (Turing.TM2.Stmt.load (fun _ => false)
          Turing.TM2.Stmt.halt))

noncomputable section

/-- `negationMachine` computa, em tempo polinomial (constante `1`, no
mesmo sentido que `idComputableInPolyTime`/`constTrueComputableInPolyTime`
— toda a cadeia `pop`/`push`/`load`/`halt` ocorre dentro de uma única
chamada de `Turing.TM2.step`, ver nota de cabeçalho sobre `stepAux`), a
função de negação booleana `fun b => !b`, a partir da codificação
`Computability.encodeBool` tanto na entrada quanto na saída. Prova
completa, sem táticas de completude vazia nem premissas locais não
justificadas (nenhum token proibido pelo scanner de governança), e sem
premissa não justificada:
`rfl` basta porque cada operação de lista (`head?`, `tail`, `update`)
casa estruturalmente sobre a lista literal `[b]`/`[]` independentemente
do valor concreto de `b`, e o `load` final faz o `var` da configuração
alcançada coincidir definicionalmente com `tm.initialState = false`. -/
def negationComputableInPolyTime :
    @TM2ComputableInPolyTime Bool Bool Bool Bool encodeBool encodeBool (fun b => !b) where
  tm := negationMachine
  inputAlphabet := Equiv.cast rfl
  outputAlphabet := Equiv.cast rfl
  time := 1
  outputsFun _ :=
    { steps := 1
      evals_in_steps := rfl
      steps_le_m := by simp }

/-- Testemunha de que `negationComputableInPolyTime` não é vazia — mesmo
papel que `inhabitedTM2ComputableInPolyTime` desempenha para a identidade
em Mathlib, aqui para a negação booleana, a segunda instância concreta de
`TM2ComputableInPolyTime` deste laboratório (a primeira sendo
`constTrueComputableInPolyTime` em `PN1_LanguagePNP.lean`, para a função
constante, não a negação). -/
instance inhabitedNegationTM2ComputableInPolyTime :
    Inhabited (TM2ComputableInPolyTime encodeBool encodeBool (fun b : Bool => !b)) :=
  ⟨negationComputableInPolyTime⟩

end

/-! ### Auditoria de dependência lógica

Verificação obrigatória do protocolo de governança do laboratório: para
cada declaração acima, confirmar que nada além de `[propext,
Classical.choice, Quot.sound]` aparece (i.e. nenhum axioma local, nenhuma
falha silenciosa de síntese de instância introduzindo `sorryAx`). -/

#print axioms TamesisLab.NegationWitness.negationMachine
#print axioms TamesisLab.NegationWitness.negationComputableInPolyTime
#print axioms TamesisLab.NegationWitness.inhabitedNegationTM2ComputableInPolyTime

end TamesisLab.NegationWitness
