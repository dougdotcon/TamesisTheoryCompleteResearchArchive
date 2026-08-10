/-
PN-5 — rascunho autocontido, NÃO integrado (não importado por
`TamesisLab.lean`; verificado isoladamente via `lake env lean` sobre este
arquivo, contra o cache já compilado da Mathlib).

Escopo (teste falsificável do item PN-5, conforme proposto e confirmado
"SURVIVES" pelo revisor adversarial na etapa de planejamento da Onda 2):
esta sessão NÃO ataca P vs NP. É uma sonda de usabilidade, restrita a um
único fato de complexidade sobre uma única função de tamanho fixo
(`Bool × Bool → Bool`), não uma família assintótica sobre entradas de
tamanho crescente, e não um "certificado" no sentido de verificador NP
(`Language.NP` de `PN1_LanguagePNP.lean` não é tocado aqui). O nome do
item ("testemunha de certificado não trivial") refere-se apenas ao fato
de a máquina abaixo consumir DOIS símbolos de entrada da pilha (em vez de
um só, como em `PN3_NegationWitness.lean`) e combiná-los via uma segunda
função de atualização de `pop` que lê o estado interno já preenchido pelo
primeiro `pop` — não a uma prova de `Language.NP`. Mesmo em caso de
sucesso total, isso não diz nada sobre escalabilidade, NP, ou qualquer
separação de classes de complexidade. NÃO decide, aproxima ou sugere
resposta a P vs NP clássico. NÃO reclama novidade matemática.

Motivação (citações conferidas por leitura direta nesta sessão,
`Mathlib/Computability/TuringMachine/Computable.lean` e
`Mathlib/Computability/TuringMachine/StackTuringMachine.lean`, e por
leitura dos arquivos-irmãos `PN1_LanguagePNP.lean`/
`PN3_NegationWitness.lean` deste mesmo diretório):
  * `structure TM2ComputableInPolyTime` — Computable.lean, campo
    `time : Polynomial ℕ`, e `outputsFun` exigindo
    `TM2OutputsInTime tm ... (time.eval (ea a).length)`.
  * `Turing.TM2.Stmt.pop : ∀ k, (σ → Option (Γ k) → σ) → Stmt → Stmt` —
    StackTuringMachine.lean, linha ~127. A função de atualização recebe
    TANTO o estado interno atual `v : σ` QUANTO o valor lido `ob : Option
    (Γ k)` — é essa dependência conjunta (`v` e `ob` juntos) que permite
    ao segundo `pop` abaixo combinar o valor já lido pelo primeiro `pop`
    (guardado em `σ`) com o segundo valor lido da pilha, sem precisar de
    `branch`/`goto`.
  * `Turing.TM2.stepAux` — StackTuringMachine.lean: `pop`/`pop`/`push`/
    `load` encadeados são processados INTEIRAMENTE dentro de UMA única
    chamada de `Turing.TM2.step` (a recursão de `stepAux` só devolve o
    controle a `step` em `goto`/`halt`). Por isso a máquina abaixo, apesar
    de ter 4 instruções reais (pop, pop, push, load) antes do halt, ainda
    conta como `steps := 1` — exatamente a mesma observação já registrada
    em `PN3_NegationWitness.lean` para sua cadeia de 3 instruções.
  * `def haltList` — Computable.lean: a config de saída ESPERADA por
    `TM2Outputs`/`EvalsTo` tem `var := tm.initialState` FIXO. A mesma
    armadilha documentada em `PN3_NegationWitness.lean` se aplica aqui
    (ver "Achado técnico" abaixo), e a mesma correção (`load` final) é
    reaproveitada.
  * `Turing.TM2.stepAux`, caso `pop`: `stepAux (pop k f q) v S = stepAux q
    (f v (S k).head?) (update S k (S k).tail)` — confirma que o `pop`
    lê da CABEÇA da lista (`head?`) e a lista de entrada é literalmente a
    lista codificada `s` (via `initList`, `stk k₀ := s`), sem inversão.
    Logo, para a codificação `encodeBoolPair p := [p.1, p.2]` usada
    abaixo, o primeiro `pop` lê `p.1` e o segundo `pop` (sobre a cauda
    `[p.2]`) lê `p.2`.

Nota de honestidade sobre os precedentes vizinhos: `PN1_LanguagePNP.lean`
(`constTrueMachine`) usa UM `pop` seguido de UM `push`, mas com `σ :=
Unit` (um subsingleton, então o `pop` não carrega informação real).
`PN3_NegationWitness.lean` (`negationMachine`) usa UM `pop` genuíno sobre
`σ := Bool`, seguido de `push`/`load`/`halt`. O teste pedido para PN-5 é
estritamente mais forte que os dois: DOIS `pop`s genuínos sobre `σ :=
Bool`, onde a função de atualização do SEGUNDO `pop` lê tanto o valor já
armazenado pelo PRIMEIRO `pop` (o parâmetro `v` da assinatura de `pop`)
quanto o novo valor lido da pilha (o parâmetro `ob`) — combinando os dois
bits de entrada numa única função de dois argumentos, antes de qualquer
`push`. Este arquivo constrói essa máquina do zero, sem importar nem
reaproveitar nada de `PN1_LanguagePNP.lean`/`PN3_NegationWitness.lean`
além do padrão estrutural já documentado neles.

Achado técnico (o mesmo "próximo degrau" identificado em
`PN3_NegationWitness.lean`, agora combinado com um segundo `pop`): usar
`σ := Bool` para carregar o primeiro bit lido entre os dois `pop`s quebra
a igualdade estrutural exigida por `haltList`, cujo campo `var` é
`tm.initialState` FIXO. A correção é idêntica à de PN-3: um `load` final
que reseta o estado interno de volta a `tm.initialState` DEPOIS que o
`push` já capturou o resultado combinado na pilha (o `push` só lê `σ`,
não o altera). Nenhuma infraestrutura adicional além da já usada em PN-3
foi necessária — o segundo `pop` não introduziu nenhuma armadilha nova,
apenas reaproveitou a mesma exatamente como o primeiro.

A função concretamente computada, para deixar o "achado" auditável sem
precisar reconstruir a prova: com `v` = bit já lido pelo primeiro `pop`
(`p.1`) e `ob.getD false` = bit lido pelo segundo `pop` (`p.2`), a função
de atualização do segundo `pop` é `fun v ob => decide (ob.getD false =
!v)`, ou seja, o novo estado é `(p.2 = !p.1)` como proposição decidida —
que coincide, ponto a ponto (verificado abaixo por `funext`/`decide`),
com `xor p.1 p.2` (OU-exclusivo booleano), a função `Bool × Bool → Bool`
efetivamente testemunhada em tempo polinomial (constante `1`) por este
arquivo.

O que continua faltando (mesmo em caso de sucesso total desta sessão,
declarado com honestidade, como pedido): um witness para UMA função de
tamanho fixo (`Bool × Bool → Bool`) é um fato de complexidade sobre uma
única instância decidível de aridade 2, não uma família assintótica sobre
entrada de tamanho crescente, nem um verificador de certificado NP no
sentido de `Language.NP` (`PN1_LanguagePNP.lean`). Não diz nada sobre
comportamento de escala, NP, ou qualquer separação de classes de
complexidade. `TM2ComputableInPolyTime.comp` continua sendo
`proof_wanted` na própria Mathlib nesta revisão — não usado nem
necessário aqui, pois não há composição de duas máquinas.
-/

import Mathlib.Computability.TuringMachine.Computable

namespace TamesisLab.XorCertificateWitness

open Turing Computability

/-! ### A codificação de entrada -/

/-- Codificação de um par de bits como lista de comprimento 2, na ordem
`[primeiro, segundo]` — a ordem em que `Turing.TM2.stepAux` consome a
pilha via `head?`/`tail` em cada `pop` sucessivo (ver nota de cabeçalho).
-/
def encodeBoolPair : Bool × Bool → List Bool := fun p => [p.1, p.2]

/-- A função efetivamente computada pela máquina abaixo: `p.2 = !p.1`,
decidida como `Bool`. Coincide ponto a ponto com `xor p.1 p.2` (ver
`xorFun_eq_xor` abaixo), registrado apenas para tornar o "achado técnico"
do cabeçalho auditável sem precisar reler a prova de `outputsFun`. -/
def xorFun : Bool × Bool → Bool := fun p => decide (p.2 = !p.1)

/-- Verificação ponto a ponto (as 4 entradas de `Bool × Bool`) de que
`xorFun` é exatamente o OU-exclusivo booleano. Não é usada pela prova de
`xorComputableInPolyTime` abaixo (que não depende de `xor`), apenas serve
de documentação executável do "achado técnico" do cabeçalho. -/
theorem xorFun_eq_xor (p : Bool × Bool) : xorFun p = xor p.1 p.2 := by
  obtain ⟨x, c⟩ := p
  cases x <;> cases c <;> decide

/-! ### A máquina -/

/-- Máquina de um único rótulo/uma única pilha (`K := Unit`, como em
`idComputer`/`constTrueMachine`/`negationMachine`) que LÊ dois bits de
entrada em sequência: o primeiro `pop` guarda o primeiro bit em
`σ := Bool` (ignorando o estado anterior, `fun _ ob => ob.getD false`,
igual ao primeiro `pop` que seria necessário em `negationMachine`); o
segundo `pop` lê o segundo bit e o COMBINA com o primeiro (agora
disponível como o parâmetro `v` da função de atualização), calculando
`decide (ob.getD false = !v)` — o "algo mais" genuíno pedido pelo item
PN-5 em relação a `PN3_NegationWitness.lean`: uma função de atualização
de `pop` que depende de dois bits de entrada distintos, não apenas um.
Em seguida `push` empilha o resultado combinado, e um `load` final
reseta o estado interno para `tm.initialState` (mesma razão estrutural
documentada em `PN3_NegationWitness.lean`: `Turing.haltList` fixa
`var := tm.initialState` na configuração esperada) antes de `halt`. -/
def xorMachine : FinTM2 where
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
      (Turing.TM2.Stmt.pop () (fun v ob => decide (ob.getD false = !v))
        (Turing.TM2.Stmt.push () (fun v => v)
          (Turing.TM2.Stmt.load (fun _ => false)
            Turing.TM2.Stmt.halt)))

noncomputable section

/-- `xorMachine` computa, em tempo polinomial (constante `1`, no mesmo
sentido que `idComputableInPolyTime`/`negationComputableInPolyTime` — toda
a cadeia `pop`/`pop`/`push`/`load`/`halt` ocorre dentro de UMA única
chamada de `Turing.TM2.step`, ver nota de cabeçalho sobre `stepAux`), a
função `xorFun : Bool × Bool → Bool` definida acima, a partir da
codificação `encodeBoolPair` na entrada e `Computability.encodeBool` na
saída. Prova completa, sem táticas de completude vazia nem premissas
locais não justificadas (nenhum token proibido pelo scanner de
governança): `rfl` basta pela mesma razão documentada em
`PN3_NegationWitness.lean` — cada operação de lista (`head?`, `tail`,
`update`) casa estruturalmente sobre a lista literal
`[p.1, p.2]`/`[p.2]`/`[]` independentemente dos valores concretos de
`p.1`/`p.2`, e o `load` final faz o `var` da configuração alcançada
coincidir definicionalmente com `tm.initialState = false`. -/
def xorComputableInPolyTime :
    @TM2ComputableInPolyTime (Bool × Bool) Bool Bool Bool encodeBoolPair encodeBool xorFun where
  tm := xorMachine
  inputAlphabet := Equiv.cast rfl
  outputAlphabet := Equiv.cast rfl
  time := 1
  outputsFun _ :=
    { steps := 1
      evals_in_steps := rfl
      steps_le_m := by simp }

/-- Testemunha de que `xorComputableInPolyTime` não é vazia — mesmo papel
que `inhabitedTM2ComputableInPolyTime`/`inhabitedNegationTM2ComputableInPolyTime`
desempenham para a identidade/negação em Mathlib/`PN3_NegationWitness.lean`,
aqui para a função `xorFun : Bool × Bool → Bool` de aridade 2. -/
instance inhabitedXorTM2ComputableInPolyTime :
    Inhabited (TM2ComputableInPolyTime encodeBoolPair encodeBool xorFun) :=
  ⟨xorComputableInPolyTime⟩

end

/-! ### Auditoria de dependência lógica

Verificação obrigatória do protocolo de governança do laboratório: para
cada declaração acima, confirmar que nada além de `[propext,
Classical.choice, Quot.sound]` aparece (i.e. nenhum axioma local, nenhuma
falha silenciosa de síntese de instância introduzindo `sorryAx`). -/

#print axioms TamesisLab.XorCertificateWitness.encodeBoolPair
#print axioms TamesisLab.XorCertificateWitness.xorFun
#print axioms TamesisLab.XorCertificateWitness.xorFun_eq_xor
#print axioms TamesisLab.XorCertificateWitness.xorMachine
#print axioms TamesisLab.XorCertificateWitness.xorComputableInPolyTime
#print axioms TamesisLab.XorCertificateWitness.inhabitedXorTM2ComputableInPolyTime

end TamesisLab.XorCertificateWitness
