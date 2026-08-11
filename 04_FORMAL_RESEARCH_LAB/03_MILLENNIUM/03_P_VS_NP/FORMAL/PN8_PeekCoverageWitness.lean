/-
PN-8 — rascunho autocontido, NÃO integrado (não importado por
`TamesisLab.lean`; verificado isoladamente via `lake env lean` sobre este
arquivo, contra o cache já compilado da Mathlib).

Escopo (teste falsificável do item PN-8, conforme proposto e confirmado
pelo revisor adversarial na etapa de planejamento da Onda 4): esta sessão
NÃO ataca P vs NP. É uma sonda de mecanismo puro sobre o modelo
`Turing.TM2`: construir uma `FinTM2` que usa `Turing.TM2.Stmt.peek` (o
construtor de `Stmt` que faltava cobrir — ver auditoria abaixo) e
verificar que a prova de `TM2ComputableInPolyTime.outputsFun` fecha. NÃO
decide, aproxima ou sugere resposta a P vs NP clássico. NÃO reclama
novidade matemática.

Auditoria de cobertura prévia (grep literal desta sessão, motivando a
frase "construtor que faltava cobrir" acima): `grep -rn
"Stmt.peek\|Turing.TM2.Stmt.peek" --include=*.lean` em todo
`04_FORMAL_RESEARCH_LAB` (excluindo o próprio pacote `Mathlib` importado)
não retornou NENHUMA ocorrência antes desta sessão. O arquivo-irmão
`PN7_BranchCoverageWitness.lean` (Onda 3) já havia documentado
explicitamente essa lacuna na sua própria seção "O que continua
faltando": "`peek` continua sem cobertura no laboratório — este arquivo
fecha apenas `branch`, não os dois construtores citados no item
(branch/peek) ... deixando `peek` como uma lacuna DIFERENTE e ainda
aberta". Este arquivo fecha especificamente essa lacuna remanescente.

Motivação (citações conferidas por leitura direta nesta sessão,
`Mathlib/Computability/TuringMachine/StackTuringMachine.lean` e
`Mathlib/Computability/TuringMachine/Computable.lean`):
  * `inductive Stmt ... | peek : ∀ k, (σ → Option (Γ k) → σ) → Stmt →
    Stmt` — StackTuringMachine.lean, linha ~129, docstring do módulo
    (linha ~89): "`peek k (f : σ → Option (Γ k) → σ) q` changes the
    state to `f a (S k).head`, where `S k` is the value of the `k`-th
    stack, then does `q`." — mesma assinatura de `pop`
    (`σ → Option (Γ k) → σ`), mas SEM remover o elemento da pilha (ao
    contrário de `pop`, cuja docstring, linha ~87-88, termina em "...and
    removes this element from the stack, then does `q`."). A docstring
    do próprio tipo indutivo (linha ~125-126) resume a diferença:
    "`peek` modifies the internal state but does not remove an
    element."
  * `Turing.TM2.stepAux`, caso `peek` — linha ~163:
    `stepAux (peek k f q) v S = stepAux q (f v (S k).head?) S`. Comparar
    com o caso `pop`, linha ~164:
    `stepAux (pop k f q) v S = stepAux q (f v (S k).head?) (update S k
    (S k).tail)` — a ÚNICA diferença estrutural é que `peek` propaga a
    MESMA pilha `S` inalterada para a continuação, enquanto `pop` propaga
    `update S k (S k).tail` (a pilha com a cabeça removida). Esta é a
    forma concreta, no código-fonte da Mathlib, da "leitura não-consumidora
    do topo da pilha" citada no teste do item PN-8: `f v (S k).head?` é
    calculado exatamente como em `pop`, mas a pilha em si não é tocada.
    Como em `PN3`/`PN5`/`PN7`, a recursão de `stepAux` continua DENTRO da
    mesma chamada (nenhum dos casos `push`/`peek`/`pop`/`load` devolve o
    controle a `Turing.TM2.step` — só `goto`/`halt` o fazem), então uma
    cadeia `pop`/`push`/`peek`/`load`/`halt` inteira, apesar de ter 4
    instruções reais antes do `halt`, ainda conta como `steps := 1`.
  * `def haltList` — Computable.lean, linha ~118: a config de saída
    esperada por `TM2Outputs`/`EvalsTo` tem `var := tm.initialState`
    FIXO — a mesma armadilha já documentada em `PN3`/`PN5`/`PN7`; a mesma
    correção (`load` final antes do `halt`) é reaproveitada aqui.
  * `TM2Outputs`/`haltList` (Computable.lean, linhas ~118-132): o valor
    de saída comparado por `outputsFun` é a pilha final `stk k₁` da
    configuração alcançada, NÃO o estado interno `var` (que só precisa
    coincidir com `tm.initialState`, resolvido pelo `load` final). Por
    isso a leitura feita pelo `peek` abaixo — que só grava em `σ`, nunca
    na pilha — só pode influenciar o resultado da prova através do valor
    JÁ presente na pilha de saída (herdado do `push` anterior), nunca por
    um caminho paralelo isolado em `σ` sem checagem: qualquer prova de
    `outputsFun` que fechasse teria de coincidir estruturalmente com a
    pilha `[v]` deixada pelo `push`, que é exatamente o mesmo valor que o
    `peek` relê — não um valor "guardado em `σ` sem uso" à parte.

A máquina, em termos concretos: pilha única (`K := Unit`, `Γ _ := Bool`,
como em `PN1`/`PN3`/`PN5`/`PN7`), um único rótulo (`Λ := Unit`, sem
`goto`, como em `PN1`/`PN3`/`PN5`/`PN7` — o mecanismo sob teste aqui é
`peek`, não a fronteira de `step`), `σ := Bool`. Reaproveitando
literalmente o padrão testemunha-identidade já fechado em
`PN1_LanguagePNP.lean`/`PN3_NegationWitness.lean`/
`PN5_XorCertificateWitness.lean`/`PN7_BranchCoverageWitness.lean`: `pop`
lê o bit de entrada em `σ` (`fun _ ob => ob.getD false`); `push (fun v =>
v)` empurra esse MESMO bit de volta para a pilha (agora a pilha de SAÍDA
já contém `[v]`, igual à pilha de entrada); em seguida — o mecanismo
NOVO deste arquivo, ainda sem cobertura no laboratório antes desta
sessão — `peek (fun _ ob => ob.getD false)` relê o TOPO dessa mesma
pilha (que agora é a pilha de saída) de volta para `σ`, SEM consumi-la
(ao contrário de um `pop`, que a removeria); um `load (fun _ => false)`
final reseta o estado interno para `tm.initialState` (mesma correção
estrutural de `PN3`/`PN5`/`PN7`, necessária porque `σ := Bool` não é
subsingleton) antes de `halt`. Como o `peek` não altera a pilha, a pilha
final permanece `[v]` — o valor lido pelo `peek` é literalmente o mesmo
valor que a prova de `outputsFun` precisa verificar na pilha de SAÍDA
(não um valor paralelo em `σ` nunca comparado), atendendo à preferência
explícita do item de reler o valor "na pilha de SAÍDA, não só armazená-lo
em `σ` sem uso". A função `Bool → Bool` efetivamente testemunhada continua
sendo a identidade — o alvo do teste é cobertura do construtor `peek` em
si, não uma nova função aritmética.

Achado técnico (ao contrário de `PN7`, onde o construtor sob teste era
`branch`, cuja equação de `stepAux` passa por `cond (f v) ...` e por isso
FICAVA preso em `v` simbólico exigindo o fallback `by cases b <;> rfl`):
aqui `evals_in_steps := rfl` fecha DIRETAMENTE, sem `cases`, para entrada
simbólica — como em `PN3`/`PN5`/`PN2PRIME` (e ao contrário de `PN7`).
Motivo: a equação de `stepAux` para `peek` (`stepAux q (f v (S k).head?)
S`, linha ~163 citada acima) NÃO passa por `Bool.cond`/casamento de
padrão sobre um `Bool` simbólico em nenhum ponto — apenas aplica `f`
(aqui `fun _ ob => ob.getD false`, que por sua vez casa sobre `Option
Bool`, não sobre `Bool`) e propaga `S` inalterada. Cada operação de lista
(`head?`, `tail` do `pop` anterior, `::` do `push` anterior) casa
estruturalmente sobre listas literais (`[b]`/`[]`) independentemente do
valor concreto do bit `b`, exatamente como documentado em `PN3`/`PN5`; o
`peek` não introduz nenhum casamento de padrão adicional sobre `b` em si
(diferente de `branch`, cuja condição É o próprio bit). Por isso a
tentativa `evals_in_steps := rfl` (pedida pelo item como primeira
tentativa) TEVE ÊXITO aqui, sem precisar do fallback `by cases b <;>
rfl` previsto como plano B — achado documentado com honestidade, como
pedido pelo item, mesmo sendo o resultado "fácil" (`rfl` bastou).

O que continua faltando (mesmo em caso de sucesso total desta sessão,
declarado com honestidade, como pedido): (1) como em `PN1`/`PN3`/`PN5`/
`PN7`, isto é um fato de complexidade sobre uma única função de tamanho
fixo (`Bool → Bool`), não uma família assintótica sobre entrada de
tamanho crescente, e não diz nada sobre `Language.NP`, escalabilidade,
ou qualquer separação de classes de complexidade. (2) O `peek` aqui relê
um valor que o `push` imediatamente anterior já havia colocado na pilha
— a prova NÃO exercita um cenário em que o `peek` lê um valor colocado
por uma via independente do `push` que o precede (p.ex., um valor que
já estava na pilha de ENTRADA original, nunca passando por um `push`
intermediário); esse caso mais fraco/diferente (peek diretamente sobre a
pilha de entrada, sem pop/push antes) fica em aberto para uma sessão
futura, se desejado. (3) Com `Stmt.branch` já coberto por
`PN7_BranchCoverageWitness.lean` e `Stmt.peek` coberto por este arquivo,
todos os sete construtores de `Turing.TM2.Stmt`
(`push`/`peek`/`pop`/`load`/`branch`/`goto`/`halt`) têm agora pelo menos
uma cobertura de mecanismo isolada em algum arquivo deste laboratório
(`push`/`pop`/`load`/`halt`: `PN1`/`PN3`/`PN5`/`PN7`/este arquivo;
`goto`: `PN2PRIME`; `branch`: `PN7`; `peek`: este arquivo) — um fato de
cobertura de sintaxe do modelo `TM2`, não uma afirmação sobre nenhuma
propriedade semântica adicional além do que cada arquivo individualmente
prova.
-/

import Mathlib.Computability.TuringMachine.Computable

namespace TamesisLab.PeekCoverageWitness

open Turing Computability

/-! ### A máquina -/

/-- Máquina de pilha única (`K := Unit`, `Γ _ := Bool`, como em
`idComputer`/`constTrueMachine`/`negationMachine`/`xorMachine`/
`branchMachine`), um único rótulo (`Λ := Unit`, sem `goto`), que exercita
`Turing.TM2.Stmt.peek`: `pop` lê o bit de entrada em `σ`
(`fun _ ob => ob.getD false`); `push (fun v => v)` empurra o MESMO bit de
volta para a pilha (padrão testemunha-identidade de `PN1`/`PN3`/`PN5`/
`PN7`); `peek (fun _ ob => ob.getD false)` relê o TOPO dessa mesma pilha
de volta para `σ`, SEM removê-lo (ao contrário de `pop`); `load
(fun _ => false)` reseta o estado interno (mesma correção estrutural de
`PN3`/`PN5`/`PN7`, exigida porque `σ := Bool` não é subsingleton) antes
de `halt`. -/
def peekMachine : FinTM2 where
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
      (Turing.TM2.Stmt.push () (fun v => v)
        (Turing.TM2.Stmt.peek () (fun _ ob => ob.getD false)
          (Turing.TM2.Stmt.load (fun _ => false)
            Turing.TM2.Stmt.halt)))

noncomputable section

/-- `peekMachine` computa, em tempo polinomial (constante `1` — como em
`PN3_NegationWitness.lean`/`PN5_XorCertificateWitness.lean`/
`PN7_BranchCoverageWitness.lean`, porque a cadeia `pop`/`push`/`peek`/
`load`/`halt` INTEIRA ocorre dentro de UMA única chamada de
`Turing.TM2.step`, ver nota de cabeçalho: só `goto`/`halt` devolvem o
controle a `step`), a função identidade `fun b => b : Bool → Bool`, a
partir da codificação `Computability.encodeBool` tanto na entrada quanto
na saída. Prova completa, sem táticas de completude vazia nem premissas
locais não justificadas (nenhum token proibido pelo scanner de
governança): ao contrário de `PN7` (onde `branch`/`cond` exigia o
fallback `by cases b <;> rfl`), aqui `rfl` DIRETO basta, mesmo para
entrada simbólica — ver "Achado técnico" no cabeçalho do arquivo: a
equação de `stepAux` para `peek` não passa por casamento de padrão sobre
o `Bool` simbólico em si, apenas propaga a pilha inalterada. -/
def peekComputableInPolyTime :
    @TM2ComputableInPolyTime Bool Bool Bool Bool encodeBool encodeBool (fun b => b) where
  tm := peekMachine
  inputAlphabet := Equiv.cast rfl
  outputAlphabet := Equiv.cast rfl
  time := 1
  outputsFun _ :=
    { steps := 1
      evals_in_steps := rfl
      steps_le_m := by simp }

/-- Testemunha de que `peekComputableInPolyTime` não é vazia — mesmo
papel que `inhabitedTM2ComputableInPolyTime` (Mathlib) e
`inhabitedNegationTM2ComputableInPolyTime`/`inhabitedXorTM2ComputableInPolyTime`/
`inhabitedChainedGotoTM2ComputableInPolyTime`/
`inhabitedBranchTM2ComputableInPolyTime` (`PN3`/`PN5`/`PN2PRIME`/`PN7`)
desempenham para seus respectivos witnesses, aqui para a identidade
`Bool → Bool` computada via `pop`/`push`/`peek` sobre a mesma pilha. -/
instance inhabitedPeekTM2ComputableInPolyTime :
    Inhabited (TM2ComputableInPolyTime encodeBool encodeBool (fun b : Bool => b)) :=
  ⟨peekComputableInPolyTime⟩

end

/-! ### Auditoria de dependência lógica

Verificação obrigatória do protocolo de governança do laboratório: para
cada declaração acima, confirmar que nada além de `[propext,
Classical.choice, Quot.sound]` aparece (i.e. nenhum axioma local, nenhuma
falha silenciosa de síntese de instância introduzindo `sorryAx`). -/

#print axioms TamesisLab.PeekCoverageWitness.peekMachine
#print axioms TamesisLab.PeekCoverageWitness.peekComputableInPolyTime
#print axioms TamesisLab.PeekCoverageWitness.inhabitedPeekTM2ComputableInPolyTime

end TamesisLab.PeekCoverageWitness
