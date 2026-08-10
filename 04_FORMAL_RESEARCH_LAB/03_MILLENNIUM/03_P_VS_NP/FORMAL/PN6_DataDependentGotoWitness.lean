/-
PN-6 — rascunho autocontido, NÃO integrado (não importado por
`TamesisLab.lean`; verificado isoladamente via `lake env lean` sobre este
arquivo, contra o cache já compilado da Mathlib).

Escopo (teste falsificável do item PN-6, conforme proposto e confirmado
"SURVIVES" pelo revisor adversarial na etapa de planejamento da Onda 3,
ver `01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_3_2026_08_10.md`, linha "PN-6 —
SURVIVES"): esta sessão NÃO ataca P vs NP. É uma sonda de mecanismo puro
sobre o modelo `Turing.TM2`, continuação direta de
`PN2PRIME_ChainedGotoWitness.lean` (Onda 2): naquele arquivo o alvo do
`goto` era LITERALMENTE CONSTANTE (`fun _ => true`, independente do bit
de entrada). Este arquivo testa exatamente o próximo passo natural,
antecipado e já indicado como divergente do padrão fácil pelo revisor
adversarial: um `goto` cujo alvo (o rótulo `Λ` de destino) DEPENDE do
valor do bit de entrada, ainda simbólico no momento em que a prova
precisa fechar — ou seja, o despacho de rótulo em si (não apenas o valor
carregado adiante, como em `PN3_NegationWitness.lean`) é alimentado por
um dado não reduzido a um construtor literal. NÃO decide, aproxima ou
sugere resposta a P vs NP clássico. NÃO reclama novidade matemática.

Teste tentado, exatamente como especificado no plano de Onda 3 (nada
mais amplo): construir uma `FinTM2` com `goto` cujo alvo depende de um
bit simbólico (não constante), reaproveitando o padrão de
`PN2PRIME_ChainedGotoWitness.lean`/`PN5_XorCertificateWitness.lean`.
Tentar fechar via `rfl`; fallback já comprometido de antemão pelo
revisor adversarial (não deixado em aberto): `by cases b <;> rfl` — que
NÃO decide P vs NP nem nada além do fato mecânico local sobre `stepAux`/
`step` sendo testado aqui.

Motivação (citações conferidas por leitura direta nesta sessão,
`Mathlib/Computability/TuringMachine/StackTuringMachine.lean` e
`Mathlib/Computability/TuringMachine/Computable.lean`):
  * `Turing.TM2.Stmt.goto : (σ → Λ) → Stmt` — StackTuringMachine.lean,
    linha ~133. A função `σ → Λ` já é, EM GERAL, arbitrária — mas em
    `PN2PRIME_ChainedGotoWitness.lean` a instância concreta usada é
    `fun _ => true`, uma função CONSTANTE que ignora `σ` inteiramente.
    Este arquivo instancia essa mesma posição com uma função que de fato
    lê `σ` (`gotoTarget`, definida abaixo).
  * `Turing.TM2.stepAux`, caso `goto` — StackTuringMachine.lean, linha
    ~167: `stepAux (goto f) v S = ⟨some (f v), v, S⟩`. Com `f := gotoTarget`
    e `v` = o bit ainda simbólico guardado em `σ` por um `pop` anterior,
    `f v` é `cond v branchTrue branchFalse` (ver definição de `gotoTarget`
    abaixo) — uma aplicação de `cond`/`Bool.rec` a um argumento não
    reduzido a `true`/`false` literal, portanto PRESA (`stuck`) até um
    case-split.
  * `Turing.TM2.step` — StackTuringMachine.lean, linhas ~171-173:
    `step M ⟨some l, v, S⟩ = some (stepAux (M l) v S)`. A SEGUNDA chamada
    de `step` (depois do `goto`) precisa despachar por `M l` onde
    `l = f v` é exatamente o termo preso descrito acima — ou seja, o
    obstáculo não está apenas dentro de `stepAux` (como a negação dupla
    de `Bool.not` em `PN2PRIME_ChainedGotoWitness.lean`, achado técnico
    daquele arquivo), mas no PRÓPRIO DESPACHO de rótulo `M l` de `step`,
    que exige um `match`/recursor sobre `Λ` disparando com um escrutínio
    não literal. Esta é a distinção mecânica precisa (documentada no
    plano de Onda 3) entre PN-6 e o obstáculo já registrado em PN2PRIME:
    lá, o valor carregado adiante por `Bool.not` nunca força um `match` a
    disparar (é apenas `push`ado, comparado depois via `funext`/`decide`
    fora da prova de `rfl`); aqui, o dado alimenta diretamente uma
    ESCOLHA DE RÓTULO, que é estruturalmente um `match`/recursor.
  * `def haltList` — `Computable.lean`, linha ~118: a config de saída
    esperada por `TM2Outputs`/`EvalsTo` tem `var := tm.initialState`
    FIXO — a mesma armadilha já documentada em `PN3_NegationWitness.lean`/
    `PN5_XorCertificateWitness.lean`/`PN2PRIME_ChainedGotoWitness.lean`;
    a mesma correção (`load` final antes do `halt`) é reaproveitada aqui.
  * `structure EvalsTo`/`EvalsToInTime` — `Mathlib/Computability/
    StateTransition.lean`, linhas ~255-267: campo
    `evals_in_steps : (flip bind f)^[steps] a = b` — exatamente o
    objetivo sobre o qual `rfl`/`cases b <;> rfl` são tentados abaixo.

A máquina, em termos concretos: um único rótulo de entrada (`entry`) que
lê o bit via `pop` (guardando-o em `σ := Bool`), empilha-o DE VOLTA sem
alteração via `push` (mesma escolha de `PN2PRIME_ChainedGotoWitness.lean`
— ver o "achado técnico" daquele arquivo sobre por que `Bool.not` foi
deliberadamente evitado ali; aqui o motivo é ainda mais direto, pois o
alvo do teste é o DESPACHO de rótulo, não uma segunda propriedade
aritmética empilhada por cima), e então `goto gotoTarget` — cujo alvo
depende do MESMO bit `v` que acabou de ser lido (`gotoTarget v = cond v
branchTrue branchFalse`), saltando para UM DE DOIS rótulos distintos
(`branchFalse`/`branchTrue`) conforme o valor do bit. Cada um desses dois
rótulos apenas reseta o estado interno (`load`) e `halt`a — a pilha já
contém `[v]` desde o `push` da primeira fase, então nenhuma leitura/
escrita adicional é necessária nesses dois rótulos. Um terceiro rótulo
(`entry`) é necessário — e não apenas dois — precisamente porque, com
`Λ` de exatamente dois elementos, o `main` (ponto de entrada) teria que
COINCIDIR com um dos dois alvos possíveis de `gotoTarget`, criando um
laço infinito para um dos dois valores de entrada (o rótulo de entrada
seria revisitado em vez de levar a `halt`). `Λ := GotoLabel`, um tipo
indutivo de três construtores definido abaixo, evita esse problema por
construção.

Achado técnico #1 (a confirmação do "achado" central do item PN-6,
previsto no plano de Onda 3, honestamente marcado ali como "estruturalmente
fundamentado, não especulação" — confirmado nesta sessão por tentativa
direta, não assumido): `evals_in_steps := rfl` FALHA para um bit de
entrada simbólico `b : Bool`, com o erro do kernel relatando que o lado
esquerdo (`(flip bind dataDependentGotoMachine.step)^[2]
(initList dataDependentGotoMachine [b])`) não é definicionalmente igual
ao lado direito. A causa raiz, confirmada por leitura do erro do kernel
nesta sessão: a segunda iteração de `step` precisa avaliar
`dataDependentGotoMachine.m (gotoTarget b)`, e `gotoTarget b = cond b
GotoLabel.branchTrue GotoLabel.branchFalse` não reduz por iota quando `b`
não é um construtor `true`/`false` literal — exatamente o obstáculo
antecipado no plano ("dado alimentando um DESPACHO... que não pode
iota-reduzir sem o escrutínio ser um construtor literal"). A correção,
também pré-comprometida no plano (não uma tática de fallback aberta
escolhida ad hoc depois do fato): `by cases b <;> rfl` — que primeiro
faz case-split em `b` (produzindo dois objetivos, um para `true` e outro
para `false`, cada um com `gotoTarget` aplicado a um construtor literal,
reduzindo estruturalmente), depois fecha cada objetivo por `rfl`. Esta
tática FECHA para os dois casos, confirmado por `lake env lean` nesta
sessão (ver rodapé do arquivo). Nenhuma tática de completude vazia nem
premissa local não justificada foi usada — nenhum token proibido pelo
scanner de governança do laboratório aparece neste arquivo.

Achado técnico #2 (uma escolha de infraestrutura, registrada com
honestidade porque desviou da primeira tentativa desta sessão): a
primeira tentativa de `Λ` usou `inductive GotoLabel ... deriving
DecidableEq, Fintype` (o padrão de derivação automática de `Fintype`
usado em outros pontos da Mathlib desta revisão, ex. `Encoding.lean`).
Essa derivação TYPE-CHECKA (a instância `Fintype GotoLabel` é aceita pelo
elaborador, confirmado por `#check (inferInstance : Fintype GotoLabel)`
nesta sessão), mas a instância PRODUZIDA está estruturalmente quebrada
para uso posterior: qualquer tática que force o kernel a inspecionar o
Method (`decide`, e por extensão qualquer prova que dependa da instância
de `Fintype` derivada) falha com um erro de "application type mismatch"
envolvendo `GotoLabel.enumList_nodup`/`SetLike.instMembership` — uma
incompatibilidade entre o tipo de `GotoLabel.enumList_nodup` produzido
pelo derivador (`GotoLabel.enumList.Nodup`) e o tipo exigido pelo campo
`nodup` da estrutura `Finset` construída pelo mesmo derivador
(`(↑GotoLabel.enumList).Nodup`) — aparentemente um problema de
coerção/`SetLike` na versão do derivador `Fintype` presente nesta
revisão da Mathlib, não algo específico desta construção. Isolado nesta
sessão num arquivo-scratch dedicado, reproduzido com um `inductive`
mínimo de três construtores sem qualquer conexão com `Turing`/`FinTM2`,
antes de tocar este arquivo. A correção adotada aqui — declarar
`deriving DecidableEq` apenas (sem `Fintype`) e fornecer manualmente uma
instância `Fintype GotoLabel` via enumeração explícita da lista de três
construtores e uma prova `by intro x; cases x <;> simp` de completude —
evita o derivador quebrado sem introduzir nenhum axioma nem depender de
nenhum comportamento não documentado; é a mesma técnica padrão usada em
provas manuais de `Fintype` para tipos indutivos finitos pequenos em toda
a Mathlib quando a derivação automática não está disponível ou falha.
Esta instância é EXIGIDA pela estrutura `FinTM2` (campo `[ΛFin :
Fintype Λ]`, `Computable.lean` linha ~60) para que `Λ := GotoLabel`
type-checke na construção de `dataDependentGotoMachine` abaixo.

O que continua faltando (mesmo em caso de sucesso total desta sessão,
declarado com honestidade, como pedido): assim como em `PN2PRIME`/`PN3`/
`PN5`, isto é um fato de complexidade sobre uma única função de tamanho
fixo (`Bool → Bool`, a identidade — o mesmo bit lido é sempre devolvido,
qualquer que seja o rótulo escolhido pelo `goto`), não uma família
assintótica sobre entrada de tamanho crescente; `steps := 2` é uma
CONSTANTE fixa, não uma função do comprimento do input. Não é um passo em
direção a `TM2ComputableInPolyTime.comp` (`Computable.lean:284-288`,
ainda `proof_wanted` nesta revisão) — não há composição de duas máquinas
distintas aqui, apenas uma única `FinTM2` com três rótulos e um `goto`
cujo alvo é dado-dependente. O fato mecânico confirmado (`goto`
dado-dependente exige case-split explícito para fechar `evals_in_steps`,
ao contrário de `goto` de alvo constante) não diz nada sobre
escalabilidade, NP, ou qualquer separação de classes de complexidade.
-/

import Mathlib.Computability.TuringMachine.Computable

namespace TamesisLab.DataDependentGotoWitness

open Turing Computability

/-! ### O tipo de rótulos e a função de alvo dado-dependente -/

/-- Três rótulos: `entry` (ponto de entrada, único ponto em que o bit é
lido/empilhado de volta) e dois alvos possíveis de `goto`
(`branchFalse`/`branchTrue`), um para cada valor do bit de entrada. Três
rótulos (não dois) são necessários porque, com `Λ` de exatamente dois
elementos, `main` teria que coincidir com um dos dois alvos possíveis de
`gotoTarget`, produzindo um laço infinito para um dos dois valores de
entrada (ver cabeçalho do arquivo). `deriving DecidableEq` apenas — SEM
`Fintype` — ver cabeçalho do arquivo, seção "Achado técnico #2", sobre um
derivador de `Fintype` quebrado nesta revisão da Mathlib para este
padrão. -/
inductive GotoLabel
  | entry
  | branchFalse
  | branchTrue
  deriving DecidableEq

/-- Instância manual de `Fintype GotoLabel`, evitando o derivador
automático quebrado (cabeçalho do arquivo, "Achado técnico #2"): a lista
dos três construtores, com a prova de completude por case-split
(`cases x`) seguido de `simp` (que fecha a checagem de pertencimento ao
`Finset` literal `{entry, branchFalse, branchTrue}` para cada um dos três
casos). Exigida pelo campo `[ΛFin : Fintype Λ]` de `FinTM2`
(`Computable.lean`). -/
instance : Fintype GotoLabel :=
  ⟨{GotoLabel.entry, GotoLabel.branchFalse, GotoLabel.branchTrue}, by
    intro x; cases x <;> simp⟩

/-- A função de alvo do `goto` abaixo — o cerne do teste do item PN-6: ao
contrário de `fun _ => true` em `PN2PRIME_ChainedGotoWitness.lean`
(constante, ignora `σ`), esta função LÊ o argumento `v : σ = Bool` e
escolhe um de dois rótulos distintos via `cond` (definido por casamento
de padrão sobre `Bool`, portanto preso/`stuck` quando `v` não é um
construtor `true`/`false` literal — ver cabeçalho do arquivo, "Achado
técnico #1"). -/
def gotoTarget : Bool → GotoLabel := fun v =>
  cond v GotoLabel.branchTrue GotoLabel.branchFalse

/-- Testemunha explícita de que `gotoTarget` NÃO é constante (o requisito
literal do item PN-6, "alvo não-constante"): os dois valores de entrada
produzem dois rótulos distintos. Decidido estruturalmente (`GotoLabel`
tem `DecidableEq` por derivação), sem depender da instância de `Fintype`
manual acima. -/
theorem gotoTarget_true_ne_gotoTarget_false :
    gotoTarget true ≠ gotoTarget false := by decide

/-! ### A máquina -/

/-- Máquina de pilha única (`K := Unit`, como em `idComputer`/
`constTrueMachine`/`negationMachine`/`xorMachine`/`chainedGotoMachine`),
com TRÊS rótulos (`Λ := GotoLabel`) e um `goto` cujo alvo depende
GENUINAMENTE do bit de entrada (`gotoTarget`, definida acima) — o "algo
mais" que o item PN-6 pede em relação a
`PN2PRIME_ChainedGotoWitness.lean` (cujo `goto` tem alvo literalmente
constante, `fun _ => true`). Rótulo `entry` (`main`): `pop` lê o bit de
entrada em `σ`, `push` empilha o MESMO bit de volta (sem alteração,
mesma escolha estrutural de `PN2PRIME_ChainedGotoWitness.lean`), `goto
gotoTarget` salta para `branchFalse` ou `branchTrue` conforme o valor do
bit — sem `halt`, então esta fase consome exatamente UMA chamada de
`Turing.TM2.step`, terminando numa config ATIVA, não na config final.
Rótulos `branchFalse`/`branchTrue`: idênticos entre si (nenhuma
assimetria de comportamento entre os dois ramos — o alvo do teste é o
MECANISMO de despacho dado-dependente, não uma computação adicional
distinta por ramo), cada um apenas reseta o estado interno via `load`
(mesma correção estrutural documentada em `PN3_NegationWitness.lean`/
`PN5_XorCertificateWitness.lean`/`PN2PRIME_ChainedGotoWitness.lean`,
exigida porque `σ := Bool` não é subsingleton) e `halt`a — a pilha já
contém `[v]` desde o `push` do rótulo `entry`, nenhuma leitura/escrita
adicional é necessária. -/
def dataDependentGotoMachine : FinTM2 where
  K := Unit
  k₀ := ()
  k₁ := ()
  Γ _ := Bool
  Λ := GotoLabel
  main := GotoLabel.entry
  σ := Bool
  initialState := false
  m
  | GotoLabel.entry =>
      Turing.TM2.Stmt.pop () (fun _ ob => ob.getD false)
        (Turing.TM2.Stmt.push () (fun v => v)
          (Turing.TM2.Stmt.goto gotoTarget))
  | GotoLabel.branchFalse =>
      Turing.TM2.Stmt.load (fun _ => false) Turing.TM2.Stmt.halt
  | GotoLabel.branchTrue =>
      Turing.TM2.Stmt.load (fun _ => false) Turing.TM2.Stmt.halt

noncomputable section

/-- `dataDependentGotoMachine` computa, em tempo polinomial (constante
`2` — uma chamada de `Turing.TM2.step` para o rótulo `entry`, atravessando
o `goto`, e uma segunda chamada para `branchFalse`/`branchTrue`, mesma
contagem de `PN2PRIME_ChainedGotoWitness.lean`), a função identidade
`fun b => b : Bool → Bool` — o mesmo bit lido em `entry` é sempre
devolvido, qualquer que seja o rótulo escolhido por `gotoTarget` — a
partir da codificação `Computability.encodeBool` tanto na entrada quanto
na saída. O "achado" central do item PN-6 está na PROVA de
`evals_in_steps`, não no `steps` em si (que continua `2`, como em
PN2PRIME): AO CONTRÁRIO de `PN2PRIME_ChainedGotoWitness.lean`, onde
`evals_in_steps := rfl` fecha diretamente (alvo de `goto` constante,
nunca força um `match` sobre um valor simbólico), aqui `rfl` FALHA
(confirmado nesta sessão, ver cabeçalho do arquivo, "Achado técnico #1")
porque a segunda chamada de `step` precisa despachar por `M (gotoTarget
b)`, e `gotoTarget b` não reduz por iota para `b` simbólico. A prova usa
o fallback pré-comprometido no plano de Onda 3: `by cases b <;> rfl` —
case-split explícito no bit de entrada, seguido de `rfl` estrutural em
cada um dos dois casos concretos resultantes. Prova completa, sem
táticas de completude vazia nem premissas locais não justificadas
(nenhum token proibido pelo scanner de governança). -/
def dataDependentGotoComputableInPolyTime :
    @TM2ComputableInPolyTime Bool Bool Bool Bool encodeBool encodeBool (fun b => b) where
  tm := dataDependentGotoMachine
  inputAlphabet := Equiv.cast rfl
  outputAlphabet := Equiv.cast rfl
  time := 2
  outputsFun a :=
    { steps := 2
      evals_in_steps := by cases a <;> rfl
      steps_le_m := by simp }

/-- Testemunha de que `dataDependentGotoComputableInPolyTime` não é
vazia — mesmo papel que `inhabitedTM2ComputableInPolyTime` (Mathlib) e
`inhabitedNegationTM2ComputableInPolyTime`/`inhabitedXorTM2ComputableInPolyTime`/
`inhabitedChainedGotoTM2ComputableInPolyTime`
(`PN3_NegationWitness.lean`/`PN5_XorCertificateWitness.lean`/
`PN2PRIME_ChainedGotoWitness.lean`) desempenham para seus respectivos
witnesses, aqui para a identidade `Bool → Bool` computada via um `goto`
cujo alvo depende genuinamente do bit de entrada. -/
instance inhabitedDataDependentGotoTM2ComputableInPolyTime :
    Inhabited (TM2ComputableInPolyTime encodeBool encodeBool (fun b : Bool => b)) :=
  ⟨dataDependentGotoComputableInPolyTime⟩

end

/-! ### Auditoria de dependência lógica

Verificação obrigatória do protocolo de governança do laboratório: para
cada declaração acima, confirmar que nada além de `[propext,
Classical.choice, Quot.sound]` aparece (i.e. nenhum axioma local, nenhuma
falha silenciosa de síntese de instância introduzindo `sorryAx`). -/

#print axioms TamesisLab.DataDependentGotoWitness.gotoTarget
#print axioms TamesisLab.DataDependentGotoWitness.gotoTarget_true_ne_gotoTarget_false
#print axioms TamesisLab.DataDependentGotoWitness.dataDependentGotoMachine
#print axioms TamesisLab.DataDependentGotoWitness.dataDependentGotoComputableInPolyTime
#print axioms TamesisLab.DataDependentGotoWitness.inhabitedDataDependentGotoTM2ComputableInPolyTime

end TamesisLab.DataDependentGotoWitness
