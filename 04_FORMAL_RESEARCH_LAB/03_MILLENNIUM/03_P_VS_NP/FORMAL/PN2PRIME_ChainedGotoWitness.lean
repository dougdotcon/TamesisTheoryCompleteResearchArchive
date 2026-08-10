/-
PN-2' — rascunho autocontido, NÃO integrado (não importado por
`TamesisLab.lean`; verificado isoladamente via `lake env lean` sobre este
arquivo, contra o cache já compilado da Mathlib).

Escopo (teste falsificável do item PN-2', conforme reformulado e
confirmado "NEEDS_NARROWING → teste revisado" pelo revisor adversarial na
etapa de planejamento da Onda 2, ver
`01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md`, itens "PN-2'" e
"6. PN / PN-2'"): esta sessão NÃO ataca P vs NP. É uma sonda de
mecanismo puro sobre o modelo `Turing.TM2`: verificar que um `goto`
efetivamente atravessa a fronteira de UMA chamada de `Turing.TM2.step`
para a próxima — ou seja, que uma `FinTM2` de DOIS rótulos (`Λ := Bool`),
com a primeira fase terminando em `goto` (não em `halt`), soma DOIS
`Turing.TM2.step` (`steps := 2` em `outputsFun`) em vez de um só, e que
`evals_in_steps` ainda fecha por `rfl`. Não é um passo em direção a
`TM2ComputableInPolyTime.comp` (composição de DUAS máquinas distintas,
`proof_wanted` em `Computable.lean:284-288`, confirmado ainda não provado
nesta revisão) — é o caso maximamente degenerado onde NÃO há duas
máquinas nem cópia de fita entre `Γ`/`K` diferentes: a MESMA pilha única
(`K := Unit`, como em `PN1_LanguagePNP.lean`/`PN3_NegationWitness.lean`)
é lida e escrita nas duas fases. Ver seção "O que continua faltando"
abaixo. NÃO decide, aproxima ou sugere resposta a P vs NP clássico. NÃO
reclama novidade matemática.

Diagnóstico de obsolescência do PN-2 original (já registrado no plano da
Onda 2, reproduzido aqui para que este arquivo seja autocontido): o PN-2
originalmente previsto — "a fase de cópia de fita entre tipos `Γ`
diferentes sequer type-checka?" — está confirmado obsoleto, porque
`PN1_LanguagePNP.lean` e `PN3_NegationWitness.lean` já usam ambos
`K := Unit`, `Γ _ := Bool`, sem nenhuma cópia de fita entre tipos
diferentes para sequer testar. O teste revisado (PN-2', este arquivo)
substitui isso por uma pergunta genuinamente diferente e ainda aberta na
etapa de planejamento: o comportamento de `goto` atravessando a fronteira
de `step`.

Motivação (citações conferidas por leitura direta nesta sessão,
`Mathlib/Computability/TuringMachine/StackTuringMachine.lean` e
`Mathlib/Computability/TuringMachine/Computable.lean`):
  * `Turing.TM2.Stmt.goto : (σ → Λ) → Stmt` — StackTuringMachine.lean,
    linha ~133.
  * `Turing.TM2.stepAux` — StackTuringMachine.lean, linhas ~161-168:
    `pop`/`push`/`load`/`branch` encadeados são processados INTEIRAMENTE
    dentro de uma única chamada de `stepAux`/`step` (a recursão de
    `stepAux` só devolve o controle a `step` em `goto`/`halt`), MAS
    `goto f, v, S => ⟨some (f v), v, S⟩` — ou seja, ao contrário de
    `halt` (que produz `l := none`, config final), um `goto` produz uma
    config com `l := some (f v)` ainda ATIVA, que exige uma NOVA chamada
    de `Turing.TM2.step` para continuar. Esta é exatamente a distinção
    que o teste abaixo verifica mecanicamente: uma cadeia
    `pop`/`push`/`goto` termina em UMA config intermediária (após 1
    `step`), não na config final; é preciso um segundo `step` (que
    processa a segunda fase, `pop`/`push`/`load`/`halt`) para chegar à
    config de `halt`.
  * `Turing.TM2.step` — StackTuringMachine.lean, linhas ~171-173:
    `step M ⟨none, _, _⟩ = none`; `step M ⟨some l, v, S⟩ = some
    (stepAux (M l) v S)` — cada chamada de `step` despacha por UM único
    rótulo `l` corrente.
  * `structure EvalsTo`/`EvalsToInTime` — `Mathlib/Computability/
    StateTransition.lean`, linhas ~255-288: `evals_in_steps :
    (flip bind f)^[steps] a = b`, isto é, `steps` iterações da função de
    transição `f` (aqui `tm.step`) aplicadas à config inicial devem
    coincidir com a config final esperada. Com duas fases separadas por
    `goto`, `(flip bind tm.step)^[2] a = tm.step (tm.step a)` — dois
    despachos de rótulo, um por fase.
  * `EvalsToInTime.trans` — `StateTransition.lean`, linhas ~284-288:
    assinatura `(f) (m₁) (m₂) (a) (b) (c) (h₁ : EvalsToInTime f a b m₁)
    (h₂ : EvalsToInTime f b c m₂) : EvalsToInTime f a c (m₂ + m₁)` — com
    `f` FIXO entre `h₁`/`h₂`; só se aplica depois de já se ter UMA
    `FinTM2` fundida com dois rótulos (exatamente o que este arquivo
    constrói), colando duas testemunhas `EvalsToInTime` PARCIAIS (config
    inicial → config intermediária pós-`goto`, e config intermediária →
    config final pós-`halt`) em vez de uma prova `rfl` direta de ponta a
    ponta. Citada aqui apenas como a rota de fallback prevista pelo teste
    original — NÃO USADA na versão final abaixo (ver "Achado técnico"
    sobre por que a rota `rfl` direta fechou, e sobre um obstáculo
    genuíno encontrado nesta sessão que uma primeira tentativa de
    desenho da máquina não superou).
  * `def haltList` — `Computable.lean`, linha ~118: a config de saída
    esperada por `TM2Outputs`/`EvalsTo` tem `var := tm.initialState`
    FIXO — a mesma armadilha já documentada em `PN3_NegationWitness.lean`/
    `PN5_XorCertificateWitness.lean`; a mesma correção (`load` final na
    ÚLTIMA fase, antes do `halt`) é reaproveitada aqui.

A máquina, em termos concretos: duas fases sobre `Λ := Bool`, `K := Unit`
(pilha única, entrada e saída coincidem, como em `PN3`/`PN5`),
`Γ _ := Bool`, `σ := Bool`. Fase `false` (`main`): lê o bit de entrada via
`pop` (guardando-o em `σ`), empilha-o DE VOLTA sem alteração via `push`
(a pilha volta a ter comprimento 1), e então `goto` para a fase `true` —
SEM `halt`, forçando a segunda fase a rodar numa segunda chamada de
`step`. Fase `true`: lê de volta o mesmo bit via `pop`, empilha-o DE
VOLTA sem alteração via `push`, reseta o estado interno para
`tm.initialState` via `load` (mesma correção estrutural de `PN3`/`PN5`,
exigida porque `σ := Bool` não é um subsingleton), e `halt`. A função
efetivamente testemunhada é, portanto, a identidade `Bool → Bool` — mas
por uma rota GENUINAMENTE diferente de `idComputer`/`idComputableInPolyTime`
(Mathlib, `Computable.lean:204-230`, que computa a identidade com UM
único rótulo e `halt` imediato, sem tocar a pilha) ou de
`PN1_LanguagePNP.lean` (`constTrueMachine`, função CONSTANTE, um único
rótulo): aqui a pilha é genuinamente lida e escrita duas vezes, em DUAS
fases separadas por um `goto` que atravessa a fronteira de `step` — o
"algo mais" que o item PN-2' revisado pede. A escolha de NÃO negar o bit
em nenhuma das duas fases (ao contrário de uma primeira tentativa desta
sessão, ver "Achado técnico" abaixo) é deliberada: o alvo do teste é o
mecanismo `goto`/fronteira-de-`step`, não uma propriedade aritmética
adicional sobre `Bool.not`.

Achado técnico (o resultado genuíno desta sessão, e uma correção
explícita em relação ao texto do plano de Onda 2 citado no cabeçalho
"6. PN / PN-2'", que previa — a partir de um scratch da ETAPA DE
PLANEJAMENTO, não reaproveitado nem re-verificado nesta sessão — que uma
máquina computando "dupla negação = identidade" (fase `false`: `pop`,
NEGAR, `push`, `goto`; fase `true`: `pop`, NEGAR DE NOVO, `push`, `load`,
`halt`) fecharia por `rfl` direto): a PRIMEIRA tentativa desta sessão
construiu exatamente essa máquina de dupla negação, e `evals_in_steps :=
rfl` FALHOU para um bit de entrada simbólico `b : Bool` (compilou apenas
para um literal concreto como `true`/`false`, onde `Bool.not` pode de
fato reduzir por casamento de padrão). A razão, isolada nesta sessão num
arquivo-scratch dedicado (dois `example`s: um com `b` literal, outro com
`b` simbólico) antes de tocar este arquivo: `!(!b) = b` — a identidade
que a dupla negação exigiria na config final — é a IGUALDADE PROPOSICIONAL
`Bool.not_not` (tipicamente provada por `cases b <;> rfl`, NÃO por `rfl`
direto), não uma igualdade DEFINICIONAL. `Bool.not` é definido por
casamento de padrão sobre os construtores `true`/`false`; aplicado a um
`b` simbólico (não reduzido a um construtor concreto), `Bool.not b` fica
PRESO (`stuck`), e uma segunda aplicação de `Bool.not` sobre esse termo
preso não reduz de volta a `b` só por unfolding — o kernel não sabe, por
definição pura, que negar duas vezes devolve o valor original; isso
exigiria case-split (`cases b`), que `rfl` não faz. Esse é exatamente o
tipo de obstáculo que o teste original antecipava ("recorrer a
`EvalsToInTime.trans`... para caso onde..."), só que a causa raiz não é
sobre COMPRIMENTO DO INPUT (como o teste original especulava), e sim
sobre uma função aritmética não-estrutural (`Bool.not` iterada) dentro do
corpo da máquina — `EvalsToInTime.trans` também NÃO resolveria isso
diretamente (ele cola duas testemunhas `EvalsTo`, mas cada uma ainda
precisaria fechar sua PRÓPRIA `evals_in_steps`, e a segunda metade ainda
enfrentaria o mesmo `!(!b) = b` não-definicional). A correção adotada
aqui — trocar a dupla negação por um simples "ler e devolver o mesmo
bit" em cada fase (`push (fun v => v)` em vez de `push (fun v => !v)`) —
isola exatamente o que o item PN-2' pede testar (a fronteira `goto`/
`step`) sem introduzir essa complicação aritmética não relacionada. Com
essa correção, `evals_in_steps := rfl` fecha tanto para um `b` literal
quanto para um `b` simbólico (confirmado no mesmo arquivo-scratch, e
reproduzido abaixo): `(flip bind tm.step)^[2] a` reduz definicionalmente
a `tm.step (tm.step a)`, e cada uma das duas chamadas de `tm.step` reduz
por sua vez inteiramente estruturalmente (despacho de rótulo via
`Bool.rec` sobre `l = false`/`l = true`, ambos casos literais; `pop`/
`push`/`load`/`goto` casam estruturalmente sobre a lista literal
`[b]`/`[]` e sobre a função identidade `fun v => v`, sem NENHUMA
aplicação de `Bool.not` a um valor simbólico). A rota `EvalsToInTime.trans`
citada acima como fallback previsto pelo teste original NÃO foi
necessária para esta versão — mas o obstáculo real encontrado (a
identidade `!(!b) = b` NÃO ser definicional) é o achado honesto desta
sessão, distinto do que o texto de planejamento da Onda 2 presumia.

O que continua faltando (mesmo em caso de sucesso total desta sessão,
declarado com honestidade, como pedido): este é o caso MAXIMAMENTE
degenerado do que seria necessário para `TM2ComputableInPolyTime.comp`
(`Computable.lean:284-288`, ainda `proof_wanted` nesta revisão) — as duas
fases aqui pertencem à MESMA `FinTM2`, com o MESMO `K`/`Γ`, sem nenhuma
cópia de fita entre codificações distintas nem composição de duas
`TM2ComputableInPolyTime` PRÉ-EXISTENTES e distintas. `.comp` precisaria
combinar duas máquinas construídas independentemente (com seus próprios
`K`/`Γ`/`σ` possivelmente distintos), preservando cada testemunha de
tempo polinomial separadamente — nada disso é tentado ou aproximado
aqui. Além disso, como em `PN3`/`PN5`, isto é um fato de complexidade
sobre uma única função de tamanho fixo (`Bool → Bool`), não uma família
assintótica sobre entrada de tamanho crescente; `steps := 2` é uma
CONSTANTE fixa aqui, não uma função do comprimento do input (o caso
"steps dependente do comprimento do input", citado no teste original
como o gatilho que exigiria `EvalsToInTime.trans`, não surge nesta
construção de aridade fixa — permanece aberto para uma eventual família
de máquinas indexada por tamanho de entrada, fora de escopo desta
sessão).
-/

import Mathlib.Computability.TuringMachine.Computable

namespace TamesisLab.ChainedGotoWitness

open Turing Computability

/-! ### A máquina -/

/-- Máquina de pilha única (`K := Unit`, como em `idComputer`/
`constTrueMachine`/`negationMachine`/`xorMachine`), mas com DOIS rótulos
(`Λ := Bool`) e uma fronteira de `goto` genuína entre eles. Fase `false`
(`main`): `pop` lê o bit de entrada em `σ`, `push` empilha o MESMO bit
de volta (sem alteração — ver cabeçalho do arquivo, seção "Achado
técnico", sobre por que uma primeira tentativa com dupla negação foi
abandonada), `goto` salta para a fase `true` — sem `halt`, então esta
fase consome exatamente UMA chamada de `Turing.TM2.step`, terminando
numa config ATIVA (`l := some true`), não na config final. Fase `true`:
`pop` lê de volta o mesmo bit, `push` empilha-o de volta mais uma vez,
`load` reseta o estado interno para `tm.initialState` (mesma correção
estrutural documentada em `PN3_NegationWitness.lean`/
`PN5_XorCertificateWitness.lean`, exigida porque `σ := Bool` não é
subsingleton), e `halt`. -/
def chainedGotoMachine : FinTM2 where
  K := Unit
  k₀ := ()
  k₁ := ()
  Γ _ := Bool
  Λ := Bool
  main := false
  σ := Bool
  initialState := false
  m
  | false =>
      Turing.TM2.Stmt.pop () (fun _ ob => ob.getD false)
        (Turing.TM2.Stmt.push () (fun v => v)
          (Turing.TM2.Stmt.goto (fun _ => true)))
  | true =>
      Turing.TM2.Stmt.pop () (fun _ ob => ob.getD false)
        (Turing.TM2.Stmt.push () (fun v => v)
          (Turing.TM2.Stmt.load (fun _ => false)
            Turing.TM2.Stmt.halt))

noncomputable section

/-- `chainedGotoMachine` computa, em tempo polinomial (constante `2` — não
`1` como em `PN3_NegationWitness.lean`/`PN5_XorCertificateWitness.lean`,
precisamente porque `steps := 2` aqui e `steps_le_m` exige
`steps ≤ time.eval (ea a).length`), a
função identidade `fun b => b : Bool → Bool` — por leitura/escrita PURA
(sem `Bool.not`) em duas fases separadas por `goto`, a partir da
codificação `Computability.encodeBool` tanto na entrada quanto na saída
(ver cabeçalho do arquivo, seção "Achado técnico", sobre por que a
identidade é testemunhada por passagem direta do bit e não por dupla
negação). O "achado" central do item PN-2' está no valor de `steps`:
`outputsFun` exige `steps := 2` (uma chamada de `Turing.TM2.step` por
fase — ver nota de cabeçalho sobre `Turing.TM2.stepAux`/`goto`), em
contraste com `steps := 1` em `PN3_NegationWitness.lean`/
`PN5_XorCertificateWitness.lean` (cadeias `pop`/`push`/.../`halt` que
nunca cruzam uma fronteira de `goto`). Prova completa, sem táticas de
completude vazia nem premissas locais não justificadas (nenhum token
proibido pelo scanner de governança): `rfl` basta porque a cadeia
inteira, nas DUAS iterações consecutivas de `tm.step`, é puramente
estrutural — cada `pop`/`push`/`load`/`goto` casa sobre a lista literal
`[b]`/`[]` e sobre a função identidade `fun v => v`, e o despacho de
rótulo via `Bool.rec` sobre `false`/`true` é literal — sem NENHUMA
aplicação de `Bool.not` a um valor simbólico (que bloquearia `rfl`, como
documentado no cabeçalho), independentemente do valor concreto de `b`. -/
def chainedGotoComputableInPolyTime :
    @TM2ComputableInPolyTime Bool Bool Bool Bool encodeBool encodeBool (fun b => b) where
  tm := chainedGotoMachine
  inputAlphabet := Equiv.cast rfl
  outputAlphabet := Equiv.cast rfl
  time := 2
  outputsFun _ :=
    { steps := 2
      evals_in_steps := rfl
      steps_le_m := by simp }

/-- Testemunha de que `chainedGotoComputableInPolyTime` não é vazia —
mesmo papel que `inhabitedTM2ComputableInPolyTime` (Mathlib) e
`inhabitedNegationTM2ComputableInPolyTime`/`inhabitedXorTM2ComputableInPolyTime`
(`PN3_NegationWitness.lean`/`PN5_XorCertificateWitness.lean`) desempenham
para seus respectivos witnesses, aqui para a identidade `Bool → Bool`
computada via duas fases encadeadas por `goto` sobre a mesma pilha. -/
instance inhabitedChainedGotoTM2ComputableInPolyTime :
    Inhabited (TM2ComputableInPolyTime encodeBool encodeBool (fun b : Bool => b)) :=
  ⟨chainedGotoComputableInPolyTime⟩

end

/-! ### Auditoria de dependência lógica

Verificação obrigatória do protocolo de governança do laboratório: para
cada declaração acima, confirmar que nada além de `[propext,
Classical.choice, Quot.sound]` aparece (i.e. nenhum axioma local, nenhuma
falha silenciosa de síntese de instância introduzindo `sorryAx`). -/

#print axioms TamesisLab.ChainedGotoWitness.chainedGotoMachine
#print axioms TamesisLab.ChainedGotoWitness.chainedGotoComputableInPolyTime
#print axioms TamesisLab.ChainedGotoWitness.inhabitedChainedGotoTM2ComputableInPolyTime

end TamesisLab.ChainedGotoWitness
