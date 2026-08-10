/-
PN-7 — rascunho autocontido, NÃO integrado (não importado por
`TamesisLab.lean`; verificado isoladamente via `lake env lean` sobre este
arquivo, contra o cache já compilado da Mathlib).

Escopo (teste falsificável do item PN-7, conforme proposto e confirmado
pelo revisor adversarial na etapa de planejamento da Onda 3): esta sessão
NÃO ataca P vs NP. É uma sonda de mecanismo puro sobre o modelo
`Turing.TM2`: construir uma `FinTM2` que usa `Turing.TM2.Stmt.branch`
(a forma concreta de "`cond(f v, ...)` com `f v` simbólico dentro de
`stepAux`" citada no item) — o único construtor de `Stmt` (entre
`branch`/`peek`) ainda sem cobertura neste laboratório antes desta sessão
(ver auditoria abaixo) — e verificar que a prova de
`TM2ComputableInPolyTime.outputsFun` ainda fecha, com o MESMO fallback
já previsto no item ("mesmo fallback by cases <;> rfl") em vez de `rfl`
direto. NÃO decide, aproxima ou sugere resposta a P vs NP clássico. NÃO
reclama novidade matemática.

Nota de dependência (item WAVE3-PN-7 depende de WAVE3-PN-6 no registro do
laboratório): no início desta sessão, procurou-se por um arquivo de saída
de PN-6 em todo `04_FORMAL_RESEARCH_LAB` (`find`/`grep` por "PN-6"/"PN6"
em nomes de arquivo e no diretório
`03_MILLENNIUM/03_P_VS_NP/FORMAL/`) — nenhum arquivo de saída de PN-6
existe ainda nesta sessão (apenas a entrada `WAVE3-PN-6` em
`RESEARCH_QUEUE.yaml`, com `status: SCOPED`, sem produto). Conforme a
nota de dependência do item, este arquivo segue o caminho (a) permitido
explicitamente: uma versão autocontida que reconstrói localmente o que é
necessário, reaproveitando apenas o PADRÃO estrutural já fechado e
disponível em `PN2PRIME_ChainedGotoWitness.lean`/
`PN5_XorCertificateWitness.lean` (ambos deste mesmo diretório, Onda 2,
já com build verificado), NÃO qualquer resultado específico de PN-6 (que
não existe para reaproveitar). A dependência declarada em
`RESEARCH_QUEUE.yaml` é sobre SEQUENCIAMENTO ("sequenciar após PN-6",
"mesmo mecanismo") — os testes falsificáveis de PN-6 (`goto` com alvo
dependente de bit simbólico) e PN-7 (`branch`/`cond` com condição
simbólica) exercitam dois construtores de `Stmt` DIFERENTES
(`goto` vs. `branch`) e não compartilham nenhuma definição Lean entre si
além do padrão comum já documentado nos arquivos de Onda 2 citados acima;
nada neste arquivo assume ou importa um resultado específico de PN-6.

Auditoria de cobertura prévia (grep literal desta sessão, motivando a
frase "único construtor ainda sem cobertura" do item): `grep -rn
"Stmt.peek\|Stmt.branch" --include=*.lean` em todo `04_FORMAL_RESEARCH_LAB`
(excluindo o próprio pacote `Mathlib` importado) não retornou NENHUMA
ocorrência antes desta sessão — nem `peek` nem `branch` tinham sido
exercitados em nenhum arquivo do laboratório (`PN1_LanguagePNP.lean` usa
`pop`/`push`; `PN3_NegationWitness.lean` usa `pop`/`push`/`load`/`halt`;
`PN5_XorCertificateWitness.lean` usa `pop`/`pop`/`push`/`load`/`halt`;
`PN2PRIME_ChainedGotoWitness.lean` usa `pop`/`push`/`goto`/`load`/`halt`).
Este arquivo fecha a lacuna de `branch` especificamente (não `peek`,
deixado em aberto — ver "O que continua faltando" abaixo).

Motivação (citações conferidas por leitura direta nesta sessão,
`Mathlib/Computability/TuringMachine/StackTuringMachine.lean`):
  * `inductive Stmt ... | branch : (σ → Bool) → Stmt → Stmt → Stmt` —
    linha ~132, docstring do módulo (linha ~91): "`branch (f : σ → Bool)
    qtrue qfalse` does `qtrue` or `qfalse` according to `f a`."
  * `Turing.TM2.stepAux`, caso `branch` — linha ~166: `stepAux (branch f
    q₁ q₂) v S = cond (f v) (stepAux q₁ v S) (stepAux q₂ v S)`. Esta é a
    forma concreta, no código-fonte da Mathlib, do "`cond(f v, ...)` com
    `f v` simbólico dentro de `stepAux`" citado no teste do item PN-7. A
    recursão de `stepAux` continua DENTRO da mesma chamada em ambos os
    ramos (`stepAux q₁ v S`/`stepAux q₂ v S`), exatamente como já
    documentado para `pop`/`push`/`load` em `PN3`/`PN5`/`PN2PRIME` — só
    `goto`/`halt` devolvem o controle a `Turing.TM2.step` — logo um
    `branch` cujos DOIS ramos terminam em `halt` (sem `goto`
    intermediário) ainda conta como `steps := 1`, igual a `PN3`/`PN5`.
  * `Bool.cond` (`core`/`Init.Prelude`, reexportado, usado aqui apenas
    por referência — não reimportado à parte, já vem junto de
    `Mathlib.Computability.TuringMachine.Computable`): definido por
    casamento de padrão sobre o argumento booleano (`cond true x y = x`,
    `cond false x y = y`). Para um argumento booleano CONCRETO (`true`/
    `false` literal) isso reduz por `rfl`; para um argumento SIMBÓLICO
    (uma variável `b : Bool` não reduzida a um construtor), `cond b x y`
    fica PRESO (`stuck`), independentemente de `x`/`y` serem iguais ou
    não entre si — o mesmo obstáculo, na mesma família (casamento de
    padrão sobre um `Bool` não constante), já isolado e documentado em
    `PN2PRIME_ChainedGotoWitness.lean` (seção "Achado técnico" do
    cabeçalho, para `Bool.not` iterado) — por isso o item já previa de
    antemão o MESMO fallback `by cases <;> rfl` em vez de `rfl` direto.
  * `def haltList` — `Computable.lean`, linha ~118: a config de saída
    esperada por `TM2Outputs`/`EvalsTo` tem `var := tm.initialState`
    FIXO — a mesma armadilha já documentada em `PN3`/`PN5`/`PN2PRIME`; a
    mesma correção (`load` final antes do `halt`, em CADA ramo do
    `branch`) é reaproveitada aqui.

A máquina, em termos concretos: pilha única (`K := Unit`, `Γ _ := Bool`,
como em `PN1`/`PN3`/`PN5`), um único rótulo (`Λ := Unit`, como em `PN1`/
`PN3`/`PN5` — SEM `goto`, ao contrário de `PN2PRIME`, porque o mecanismo
sob teste aqui é `branch`, não a fronteira de `step`), `σ := Bool`.
`pop` lê o bit de entrada em `σ` (`v`); `branch (fun v => v) qTrue
qFalse` decide, com base nesse MESMO bit `v` (condição genuinamente
simbólica, não uma constante `fun _ => true`/`fun _ => false`), qual dos
dois ramos seguir; CADA ramo (`qTrue`/`qFalse`) executa `push (fun v =>
v)` (empilha o mesmo bit de volta) seguido de `load (fun _ => false)`
(reset do estado interno, mesma correção estrutural de `PN3`/`PN5`/
`PN2PRIME`) e `halt`. Os dois ramos são STATEMENTS distintos (duas
subárvores `push`/`load`/`halt` construídas separadamente na definição
de `m`, não uma referência compartilhada a um único termo), então o
`cond` sobre a condição simbólica genuinamente precisa ser resolvido pelo
kernel (não apenas "os dois ramos são o mesmo termo, então qualquer coisa
reduz") — mas como ambos os ramos computam a MESMA função (empilhar o bit
de volta sem alterá-lo), a função `Bool → Bool` efetivamente testemunhada
é a identidade, por uma rota que passa genuinamente por `branch`/`cond`
em vez de por leitura/escrita linear (`PN1`) ou por `goto` (`PN2PRIME`).

Achado técnico (confirmando, para `branch`, a mesma observação já
registrada para `goto`/`Bool.not` iterado em
`PN2PRIME_ChainedGotoWitness.lean`): uma primeira tentativa de fechar
`evals_in_steps := rfl` diretamente (sem `cases`), como em `PN3`/`PN5`
(onde `rfl` fecha para uma entrada simbólica), FALHA aqui, porque a
config final atingida por `stepAux` passa por `cond (f v) (stepAux q₁ v
S) (stepAux q₂ v S)` com `f v = v` um `Bool` simbólico (o bit de entrada,
ainda não reduzido a um construtor concreto) — ao contrário de `PN3`/
`PN5`/`PN2PRIME` (versão final, sem dupla negação), onde cada operação
(`head?`, `tail`, `update`) casa estruturalmente sobre a LISTA literal
independentemente do VALOR dos bits, aqui o casamento de padrão do
`cond` é sobre o próprio VALOR do bit, que é exatamente o tipo de
obstáculo (`stuck` em variável simbólica de tipo `Bool`) já isolado por
`PN2PRIME_ChainedGotoWitness.lean` para `Bool.not` iterado. A correção —
já prevista no texto do próprio item PN-7 ("mesmo fallback by cases <;>
rfl", reaproveitado literalmente de `PN2PRIME_ChainedGotoWitness.lean`,
que por sua vez cita esse padrão como a lição herdada de sua PRIMEIRA
tentativa malsucedida com dupla negação) — é substituir `evals_in_steps
:= rfl` por `evals_in_steps := by cases b <;> rfl` em `outputsFun`,
fazendo o case-split no bit de entrada ANTES de deixar `rfl` fechar cada
um dos dois casos concretos (`true`/`false`) separadamente, onde `cond`
já reduz por casamento de padrão direto. Confirmado abaixo: com esse
único ajuste em relação ao padrão `rfl` direto de `PN3`/`PN5`/`PN2PRIME`,
a prova fecha sem táticas de completude vazia nem premissas locais não
justificadas (nenhum token proibido pelo scanner de governança).

O que continua faltando (mesmo em caso de sucesso total desta sessão,
declarado com honestidade, como pedido): (1) `peek` continua sem
cobertura no laboratório — este arquivo fecha apenas `branch`, não os
dois construtores citados no item ("branch/peek"); a leitura do item
("o único construtor... ainda sem cobertura", singular) e o teste
falsificável explicitamente pedido ("`cond(f v, ...)`") apontam para
`branch`, não `peek` (que não usa `cond` em sua equação de `stepAux`),
então este arquivo trata `branch` como o alvo do item, deixando `peek`
como uma lacuna DIFERENTE e ainda aberta, fora do escopo estreito deste
teste. (2) Como em `PN1`/`PN3`/`PN5`/`PN2PRIME`, isto é um fato de
complexidade sobre uma única função de tamanho fixo (`Bool → Bool`), não
uma família assintótica sobre entrada de tamanho crescente, e não diz
nada sobre `Language.NP`, escalabilidade, ou qualquer separação de
classes de complexidade. (3) Os dois ramos do `branch` aqui computam a
MESMA função (identidade) por desenho — o teste pedido é sobre o
MECANISMO `branch`/`cond` em si (cobertura de construtor), não sobre uma
propriedade aritmética adicional que distinguisse os dois ramos; uma
função efetivamente RAMIFICADA (ramos com saídas diferentes) fica em
aberto para uma sessão futura, se desejado.
-/

import Mathlib.Computability.TuringMachine.Computable

namespace TamesisLab.BranchCoverageWitness

open Turing Computability

/-! ### A máquina -/

/-- Máquina de pilha única (`K := Unit`, `Γ _ := Bool`, como em
`idComputer`/`constTrueMachine`/`negationMachine`/`xorMachine`), um único
rótulo (`Λ := Unit`, sem `goto`), que exercita `Turing.TM2.Stmt.branch`
com uma condição GENUINAMENTE simbólica: `pop` lê o bit de entrada em
`σ` (`v`); `branch (fun v => v) qTrue qFalse` decide o ramo com base
nesse MESMO `v` (não uma constante `fun _ => true`); cada ramo
(construído como uma subárvore SEPARADA, não uma referência
compartilhada) empilha o bit de volta via `push (fun v => v)` e reseta
o estado interno via `load (fun _ => false)` (mesma correção estrutural
de `PN3_NegationWitness.lean`/`PN5_XorCertificateWitness.lean`/
`PN2PRIME_ChainedGotoWitness.lean`, exigida porque `σ := Bool` não é
subsingleton) antes de `halt`. -/
def branchMachine : FinTM2 where
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
      (Turing.TM2.Stmt.branch (fun v => v)
        (Turing.TM2.Stmt.push () (fun v => v)
          (Turing.TM2.Stmt.load (fun _ => false)
            Turing.TM2.Stmt.halt))
        (Turing.TM2.Stmt.push () (fun v => v)
          (Turing.TM2.Stmt.load (fun _ => false)
            Turing.TM2.Stmt.halt)))

noncomputable section

/-- `branchMachine` computa, em tempo polinomial (constante `1` — como em
`PN3_NegationWitness.lean`/`PN5_XorCertificateWitness.lean`, porque a
cadeia `pop`/`branch`/(`push`/`load`/`halt` em cada ramo) INTEIRA ocorre
dentro de UMA única chamada de `Turing.TM2.step`, ver nota de cabeçalho:
só `goto`/`halt` devolvem o controle a `step`, e nenhum dos dois ramos
usa `goto`), a função identidade `fun b => b : Bool → Bool`, a partir da
codificação `Computability.encodeBool` tanto na entrada quanto na saída.
Prova completa, sem táticas de completude vazia nem premissas locais não
justificadas (nenhum token proibido pelo scanner de governança): ao
contrário de `PN3`/`PN5`/`PN2PRIME` (onde `rfl` direto basta mesmo para
entrada simbólica), aqui `cond (f v) ...` fica preso em `v` simbólico
(ver "Achado técnico" no cabeçalho do arquivo), então usa-se o fallback
já previsto pelo próprio item PN-7 ("mesmo fallback by cases <;> rfl"):
`cases b` primeiro reduz a entrada a `true`/`false` concretos, e SÓ
ENTÃO `rfl` fecha cada um dos dois casos, onde `cond` já casa
estruturalmente. -/
def branchComputableInPolyTime :
    @TM2ComputableInPolyTime Bool Bool Bool Bool encodeBool encodeBool (fun b => b) where
  tm := branchMachine
  inputAlphabet := Equiv.cast rfl
  outputAlphabet := Equiv.cast rfl
  time := 1
  outputsFun b :=
    { steps := 1
      evals_in_steps := by cases b <;> rfl
      steps_le_m := by simp }

/-- Testemunha de que `branchComputableInPolyTime` não é vazia — mesmo
papel que `inhabitedTM2ComputableInPolyTime` (Mathlib) e
`inhabitedNegationTM2ComputableInPolyTime`/`inhabitedXorTM2ComputableInPolyTime`/
`inhabitedChainedGotoTM2ComputableInPolyTime` (`PN3`/`PN5`/`PN2PRIME`)
desempenham para seus respectivos witnesses, aqui para a identidade
`Bool → Bool` computada via `branch`/`cond` sobre uma condição
genuinamente simbólica. -/
instance inhabitedBranchTM2ComputableInPolyTime :
    Inhabited (TM2ComputableInPolyTime encodeBool encodeBool (fun b : Bool => b)) :=
  ⟨branchComputableInPolyTime⟩

end

/-! ### Auditoria de dependência lógica

Verificação obrigatória do protocolo de governança do laboratório: para
cada declaração acima, confirmar que nada além de `[propext,
Classical.choice, Quot.sound]` aparece (i.e. nenhum axioma local, nenhuma
falha silenciosa de síntese de instância introduzindo `sorryAx`). -/

#print axioms TamesisLab.BranchCoverageWitness.branchMachine
#print axioms TamesisLab.BranchCoverageWitness.branchComputableInPolyTime
#print axioms TamesisLab.BranchCoverageWitness.inhabitedBranchTM2ComputableInPolyTime

end TamesisLab.BranchCoverageWitness
