---
document_id: PLANO-ATAQUE-ONDA-2-2026-08-09
reviewed_at: 2026-08-09
input: recon + revisao adversarial de 9 grupos (8 linhas de pesquisa + infraestrutura compartilhada) para Onda 2, ancorado nos resultados reais da Onda 1 -- ver 09_SESSIONS/2026/2026-08-09_WAVE1_EXECUTION.md (25/27 fechados, 2 gaps honestos) e 01_PORTFOLIO/PLANO_DE_ATAQUE_PORTFOLIO_COMPLETO_2026_08_09.md
conclusion: PLANO_DE_EXECUCAO_ONDA_2_PROPOSTO
---

# Plano de ataque — Onda 2 (continuacao da Onda 1)

## Enquadramento honesto

Este documento e a continuacao direta de
`PLANO_DE_ATAQUE_PORTFOLIO_COMPLETO_2026_08_09.md` e da sessao de execucao
`2026-08-09_WAVE1_EXECUTION.md`. A Onda 1 fechou 25 de 27 itens (18
VERIFIED, 7 VERIFIED_WITH_NOTES) com recompilacao independente confirmada
(27/27 exit 0, zero `sorryAx`, zero token proibido, `lake build` central
sem regressao), e diagnosticou honestamente 2 gaps (BSD-1, BSD-4) em vez
de forcar fechamento. A Onda 2 parte desse chao real, nao de aspiracao.

```text
O que este plano E:
  - a proxima rodada de pequenos testes falsificaveis contra
    infraestrutura Mathlib genuina, construida sobre os 25 itens
    fechados e os 2 gaps diagnosticados na Onda 1
  - uma tentativa de re-verificar, por leitura direta de arquivo (nao por
    confianca no agente de recon), se os passos originalmente previstos
    para "depois da Onda 1" continuam abertos, ja foram satisfeitos por
    acaso, ou ficaram obsoletos por descoberta nova
  - honesto sobre candidatos REFUTED e sobre onde um teste proposto
    tinha um defeito de tipagem ou matematico real, nao so cosmetico

O que este plano NAO E:
  - uma alegacao de que qualquer Problema do Milenio ficou mais proximo
    de ser resolvido -- nenhum item abaixo toca o nucleo central de
    nenhuma das 6 frentes Clay-oficiais
  - uma alegacao de que TOE-INTERFACE-001 ou QCU-001 tem status
    Clay-oficial
  - uma reabertura do RH-NOGO-001: o item RH desta onda vive
    explicitamente na camada abstrata "reutilizavel fora desta frente"
    do freeze, nao na camada concreta congelada -- ver secao RH abaixo
  - uma promessa de que todo teste "SURVIVES" fecha sem sorry -- e uma
    aposta informada, nao uma certeza
```

Cada candidato abaixo passou por reverificacao independente de citacao
Mathlib (leitura direta de arquivo no checkout vendorizado, nao
grep-e-confia) e, em varios casos, por compilacao real de sonda em
scratch file contra o cache Mathlib fixado do laboratorio. Veredito:
`SURVIVES` (teste proposto se sustenta como esta), `NEEDS_NARROWING`
(angulo real, mas o teste proposto precisou ser reescrito para ser
genuinamente pequeno/correto), ou `REFUTED` (nao vale investir).

23 candidatos revisados ao todo nos 9 grupos: 20 `SURVIVES`/
`NEEDS_NARROWING`, 3 `REFUTED`.

---

## 1. Riemann Hypothesis (RH) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| RVM-LIMIT-ERROR | Composicao abstrata de termo de erro O(log T) para RVM-LIMIT | SURVIVES | baixo |
| NZeta-STRUCTURE | Monotonicidade e trivialidade de fronteira da funcao de contagem de zeros restrita a faixa | SURVIVES | baixo |

**Passo original vs. o que mudou.** O passo previsto (fechar o termo de
erro O(log T) do RVM-LIMIT) continua genuinamente aberto -- `RVMLimit.lean`
linhas 18-22 e `RVM_LIMIT_BRIDGE.md` ainda listam esse passo como nao
provado. Mas a busca de citacao revelou que `StrongAsymptoticCorollary.lean`
(ja importado transitivamente por `RVMLimit.lean`) contem
`tendsto_tLog_of_eq_main_add_littleO` -- exatamente SB-GAP-010A, ja fechado
(`SOURCE_BRIDGE_GAP_REGISTER.yaml:155`, `status: CLOSED_BY_FORMALIZATION`)
e **estritamente mais geral** do que o candidato propunha construir. Ou
seja: a "nova maquinaria de composicao" prevista e obsoleta -- o trabalho
real e menor, um corolario fino desse teorema ja fechado, nao uma
re-derivacao do zero.

**RVM-LIMIT-ERROR — SURVIVES.** `IsBigO.trans_isLittleO`
(`Analysis/Asymptotics/Defs.lean:516`) e
`IsLittleO.tendsto_div_nhds_zero` (`Analysis/Asymptotics/Lemmas.lean:372`)
conferem exatos. Governanca: a restricao de recursos do
`RH_NOGO_FREEZE_RECORD.md` ("nenhum recurso do laboratorio sera gasto
nela") aplica-se textualmente so a `concrete_layer` (global_weyl_bridge,
rvm_concrete, operator_exclusion), nao a `abstract_layer`, marcada
COMPLETE e "reutilizavel fora desta frente" -- ja ha precedente direto:
WAVE1-RH-1 (`RESEARCH_QUEUE.yaml:2033`) foi autorizado e fechado como item
independente dentro de `TamesisLab/RHNogo/Bridge/` sem tocar o status
congelado de RH-NOGO-001, via gate DEC-086 separado.
**Teste revisado:** construir a mesma afirmacao falsificavel do candidato
original, mas como corolario direto de `tendsto_tLog_of_eq_main_add_littleO`
(SB-GAP-010A) em vez de re-derivar a composicao do zero: (a) mostrar
`e =O[atTop] log T` e `log T =o[atTop] (T*log T)`, logo
`e =o[atTop] (T*log T)` via `IsBigO.trans_isLittleO`; (b) mostrar que
`rvmFormula - c*(T*log T)` e o(T log T), extraivel de
`tendsto_rvmLimitFormula_div_tLogScale` ja provado; (c) somar os dois
termos o(T log T) e invocar `tendsto_tLog_of_eq_main_add_littleO`
diretamente. Registrar como item novo com gate/DEC proprio (seguindo o
precedente WAVE1-RH-1/WAVE1-RH-2 de itens separados), nao como edicao
silenciosa do escopo ja fechado de WAVE1-RH-1 em `RVMLimit.lean`.
Verificar `#print axioms` mostrando so `propext`/`Classical.choice`/
`Quot.sound`.

**NZeta-STRUCTURE — SURVIVES.** `ZetaZerosCountingFiniteness.lean`
confirmado por leitura integral: `NZeta_region_finite` ja prova finitude
para todo `T : R`; o header do arquivo (linhas 38-41) confirma
desconexao deliberada de `TamesisLab.RHNogo`. `IsCompact.inter_
riemannZetaZeros_finite` (`Mathlib/NumberTheory/LSeries/ZetaZeros.lean:64-67`),
`Set.ncard_le_ncard` (`Data/Set/Card.lean:656`) e `Set.Ioc_subset_Ioc_right`
(gerado por `to_dual` a partir de `Ioc_subset_Ioc_left`, com dois
call-sites reais confirmados em `Chebyshev.lean:184` e
`Topology/Order/OrderClosed.lean:371`) conferem e resolvem exatamente como
precisa. `still_missing_if_success` e honesto: nenhum crescimento
assintotico, nenhum termo de erro, nada em direcao a REACT-002/003, nenhum
conteudo de RH.
**Teste revisado:** provar `Monotone NZeta` (via `zetaZerosInStrip_subset`
composto com `Set.ncard_le_ncard` contra `NZeta_region_finite T2` como
testemunha de finitude) e `NZeta T = 0` para `T <= 0`, mostrando
diretamente `zetaZerosInStrip T = (empty : Set C)` via `Set.Ioc_eq_empty`
sobre o limite `0 < T` falho, em vez de rotear por `Set.ncard_eq_zero`
(mantem a prova independente de peculiaridades do `toFinite_tac`).

---

## 2. Navier-Stokes (NS) — Clay oficial (nucleo Calderon-Zygmund)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| NS-2a | Generalizar `hasLocalPV_K_mul_phi` para funcao-teste Lipschitz arbitraria | NEEDS_NARROWING | baixo (apos correcao) |
| NS-2b | Construir termo de distribuicao D'(Omega,F) genuino para o nucleo p.v. via `TestFunction.mkCLM`/`limitCLM` | NEEDS_NARROWING | moderado, depende de NS-2a |

**Passos originais vs. o que mudou.** Ambos os passos previstos (NS-2a,
NS-2b) continuam genuinamente abertos. Mas dois defeitos concretos
apareceram: (1) o mecanismo especifico que NS-2a alega usar
(`phi_lipschitz` conduzindo o bound em `hdecay`) esta errado --
`phi_lipschitz` so aparece uma vez, para mensurabilidade, e o bound real
vem de uma **igualdade algebrica exata** especifica do phi radial
concreto (`hphidiff`), nao de uma desigualdade Lipschitz; a generalizacao
e igualmente barata, mas o ponto de mudanca no arquivo e outro. (2) o
dominio que NS-2b originalmente mirava (`Omega \ {0}`) torna a propria
maquinaria de p.v. **obsoleta**: todo compacto K contido em `Omega \ {0}`
ja fica longe da origem, entao K*f ja e suave e compacto-suportado sem
singularidade nenhuma -- `integralAgainstBilinCLM` padrao ja bastaria, sem
`mkCLM`/`limitCLM`. O dominio que genuinamente precisa da maquinaria de
p.v. (onde `LocallyIntegrableOn K Omega volume` falha de verdade, porque
`0 in Omega`) e o espaco **completo**, nao `Omega` menos a origem.

**NS-2a — NEEDS_NARROWING.** `K_shell_integral_eq_zero` (:528),
`K_diff_integrableOn_closedBall` (:748),
`tendsto_setIntegral_annulus_of_integrableOn_closedBall` (:832),
`hasLocalPV_K_mul_phi` (:887) conferem exatos e sao genericos/reutilizaveis
como alegado. `LipschitzWith.dist_le_mul`
(`Topology/MetricSpace/Lipschitz.lean:50`) confirmado, capaz de substituir
`hphidiff`.
**Teste revisado:** declarar `hasLocalPV_K_mul_lipschitz (g : E -> R)
(hg : LipschitzWith L.toNNReal g)`; na prova, substituir a igualdade exata
de `hphidiff` pelo bound `|g y - g 0| <= L * ‖y‖` obtido de
`hg.dist_le_mul y 0` (reescrito via `dist_eq_norm`), e reescrever
`hnormeq` e o calc final de `hdecay` como cadeia `<=` terminando em
`C*L*‖y‖^(-2)` em vez da cadeia de igualdade exata atual terminando em
`C*‖y‖^(-2)`; manter o papel de `phi_lipschitz` so para
mensurabilidade/continuidade de g, nao como fonte do bound numerico.
Falsificado se a substituicao nao fechar no passo `hnormeq`/calc final
(nao em `hrpow`, que e identidade algebrica independente de phi).

**NS-2b — NEEDS_NARROWING.** `TestFunction.mkCLM` (:353-363),
`limitCLM` (:370-393), `abbrev Distribution := 𝓓^{n}(Ω,ℝ) →L_c[ℝ] F`
(`Distribution.lean:160`), `ContDiffMapSupportedIn.seminorm` (:625),
`Function.HasTemperateGrowth.toTemperedDistribution` (`TemperedDistribution.lean:98`)
conferem exatos; grep amplo por "principal value"/"principalValue"/
"CauchyPrincipal"/"PrincipalValue" em todo o Mathlib retorna zero hits,
confirmando ausencia genuina de construtor de p.v. `integralAgainstBilinCLM`
(`TestFunction.lean:704-711`) nao e "inaplicavel" a K -- degenera
silenciosamente na distribuicao nula quando `LocallyIntegrableOn` falha
(um `if`-decidivel, nao um argumento ausente). O alvo `n = infinito`
(𝓓' completo) tambem sobre-especifica: o bound Lipschitz de NS-2a so
controla ordem 0 e 1, nao derivadas de ordem superior.
**Teste revisado:** tentar `pvK (e2 e3 : EuclideanSpace R (Fin 3)) :
𝓓'^{1}(EuclideanSpace R (Fin 3), R)` (distribuicao de **ordem 1**,
compativel com o controle que NS-2a de fato produz) no espaco **completo**
`Omega = EuclideanSpace R (Fin 3)` (nao `Omega \ {0}`), primeiro
restrito a um unico compacto `K = closedBall 0 R` (agora consistente, ja
que `K subseteq Omega`), usando `TestFunction.mkCLM` com `cont` descarregado
via o bound Lipschitz generalizado de NS-2a contra as seminormas
`N[K,1,i]` (sup de f e sup de Df sobre K). Falsificado/reportado como gap
se o framework de seminorma de ordem 1 exigir controle que esta construcao
nao pode fornecer, ou se estender de um unico K para a familia completa
exigida por `limitCLM` (todos os compactos de `Omega`) nao fechar
uniformemente.

---

## 3. P vs NP (PN) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| PN-5 | Testemunha `Language.NP` com certificado nao-trivial (maquina unica auto-contida, sem `.comp`) | SURVIVES | baixo |
| PN-2' | Sanidade de composicao goto-encadeada na mesma pilha (explicitamente NAO progresso no `proof_wanted`) | NEEDS_NARROWING | baixo |
| — | `TM2ComputableInPolyTime.comp` geral, tentado inteiro | REFUTED | very_high |

**Passo original vs. o que mudou.** O PN-2 originalmente previsto ("a fase
de copia de fita entre tipos Gamma diferentes sequer type-checka?") esta
**confirmado obsoleto (stale)**: `PN1_LanguagePNP.lean` e
`PN3_NegationWitness.lean` usam ambos `K:=Unit`, `Gamma _:=Bool`,
`encodeBool/encodeBool` -- nao ha copia de fita entre tipos diferentes
para sequer testar. Eu re-executei `lake env lean` em ambos os arquivos
standalone contra o cache Mathlib fixado: ambos compilam limpos, so com
`[propext, Classical.choice, Quot.sound]`. Dois candidatos sucessores
substituem o PN-2 original.

**PN-5 — SURVIVES.** `Stmt` (`StackTuringMachine.lean:127-134`),
regiao `TM2ComputableInPolyTime`/`TM2OutputsInTime`/`haltList`
(`Computable.lean:118-188`), `encodeBool := pure`
(`Encoding.lean:163`) conferem exatos. Fui alem da leitura: construi a
maquina exata proposta (K:=Unit, sigma:=Bool, pop x, pop c com funcao de
atualizacao `decide (ob.getD false = !v)`, push, load-reset, halt,
verificando Bool x Bool -> Bool) num scratch file e rodei `lake env lean`
contra o cache pinado real (v4.33.0-rc1): compilou com zero erros,
`#print axioms` so com os 3 axiomas padrao. Isso confirma diretamente a
aposta tecnica central -- uma unica FinTM2 pode genuinamente ler e usar um
certificado extraido da mesma pilha, na escala do PN-3 (steps:=1), sem
precisar de `TM2ComputableInPolyTime.comp`.
**Teste revisado:** manter a construcao exatamente como proposta (ja
confirmada compilar standalone). Unica correcao: a citacao de "testemunha
verificadora genuina de leitura de certificado" entre aspas nao e citacao
literal do header do PN-1 (grep confirma ausencia dessa frase exata) --
substituir por citacao direta de `PN1_LanguagePNP.lean:57-63`.

**PN-2' — NEEDS_NARROWING.** Diagnostico de obsolescencia confirmado
(ver acima). `EvalsTo.trans`/`EvalsToInTime.trans`
(`StateTransition.lean:274-288`) tem assinatura `(f) (h1) (h2)` com `f`
fixo entre h1 e h2 -- so aplica-se apos ja se ter construido UMA FinTM2
mesclada (o que o candidato propoe: "encadear duas maquinas numa so
FinTM2 de dois labels"). Construi e compilei exatamente essa maquina
mesclada (Lambda:=Bool, main:=false, fase-false pop/push/goto-para-true,
fase-true pop/push/load/halt, computando dupla negacao = identidade sobre
Bool): a construcao **direta** (steps:=2, `evals_in_steps := rfl`)
compilou limpa. A rota literal proposta no teste original (colar dois
episodios `EvalsToInTime` via `.trans` com configs intermediarias
digitadas a mao) tropecou num mismatch de defeq no meu proprio scratch
-- mais fragil e desnecessaria, sem relacao com a pergunta real
("goto atravessa fronteira de step?").
**Teste revisado:** construir UMA nova FinTM2 (Lambda := Bool ou
2-elementos, reusando K:=Unit/Gamma:=Bool ja que ambas testemunhas
coincidem ali) com um goto cruzando duas fases, e tentar `outputsFun` com
`steps := 2` e `evals_in_steps := rfl` diretamente (mesmo padrao ja
estabelecido por PN-1/PN-3, so com steps:=2 em vez de 1) -- ja confirmado
funcionar. So recorrer a `EvalsToInTime.trans` explicito se a rota direta
falhar para um caso complexo o bastante que um `rfl` unico nao feche
(ex.: steps dependente do comprimento do input). Manter a divulgacao
`still_missing_if_success` em destaque: e um caso maximamente degenerado
de `.comp` (K1=K2, sem copia de fita real).

**`TM2ComputableInPolyTime.comp` geral — REFUTED (refutacao de escopo, nao
factual).** `proof_wanted TM2ComputableInPolyTime.comp` confirmado ainda
nao provado (`Computable.lean:284-288`); grep em toda a arvore
`Mathlib/Computability` nao encontrou nenhum outro construtor
`: TM2ComputableInPolyTime` alem de `idComputer`/`idComputableInPolyTime`
e o proprio `proof_wanted`. Mas o proprio candidato declara
`falsifiable_test: N/A / deferred`, nao propoe teste acionavel de escala
Onda 2, e se autoavalia `cost_estimate: very_high`, `plausibility: low`,
"nao recomendado para Onda 2". Autoexcluido corretamente -- concordo que
deve continuar excluido. O motivo e estrutural: uma tentativa real
precisaria de fusao de pilha em soma de tipos K1+K2 mais uma subrotina de
copia de fita genuina cujo numero de passos depende do comprimento da
saida da primeira maquina em tempo de execucao -- quebra o truque
"unica chamada `stepAux` decidida por `rfl`" que tornou todo outro item
PN da Onda 1/2 barato.
**Nenhum teste de continuacao proposto por design.** Se uma onda futura
quiser atacar isso, o primeiro sub-passo falsificavel seria muito mais
estreito que `.comp` completo: provar o numero de passos de uma subrotina
de copia-de-tamanho-fixo-conhecido via uma lista concreta curta (ex.:
copiar uma lista de 2 elementos entre duas pilhas de mesmo tipo) antes de
tocar fusao de tipo K1/K2 ou o `proof_wanted` geral.

---

## 4. Yang-Mills (YM) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| YM-1-Connect | `IsHermitian.eigenvalues` abstrato para a matriz M do YM-1, via `spectrum_real_eq_range_eigenvalues` | SURVIVES | baixo |
| YM-2-Simple | Multiplicidade do autovalor dominante da matriz primitiva A do YM-2, via `Polynomial.funext` + `rootMultiplicity` | SURVIVES | baixo-moderado |
| YM-1+YM-3 | Bound de norma de operador ligando familia de matriz 2x2 explicita ao `lambdaMax_lipschitz` do YM-3 | NEEDS_NARROWING | moderado |

**Passo original vs. o que mudou.** O teste original YM-1 (adiado na
Onda 1 como "pointwise eigenvalues_eq/charpoly_eq desajeitado") nunca foi
refutado, so adiado -- YM-1-Connect e sucessor genuino, nao forcando um
plano obsoleto. A composicao YM-1+YM-3 continua genuinamente aberta
(`FixedDimEigenvalueStability.lean` nunca aplica `lambdaMax_lipschitz` a
uma matriz concreta, so a operadores abstratos).

**YM-1-Connect — SURVIVES.** `FiniteLatticeTransferGap.lean:26-47`
confirma que o teste original foi adiado, nao refutado.
`PerronFrobeniusInstance.lean:165-194` (`A_charpoly_eval`,
`A_spectrum_real`) confirma o padrao `eval_charpoly` + `det_fin_n` +
`mem_spectrum_iff_isRoot_charpoly` ja funciona para 3x3, estritamente
mais dificil que a matriz 2x2 M do YM-1. `spectrum_real_eq_range_
eigenvalues` (`Analysis/Matrix/Spectrum.lean:211-213`),
`Real.instRCLike` (`RCLike/Basic.lean:788`), `Matrix.det_fin_two`
(`Determinant/Basic.lean:807`) conferem. Toda peca do plano ja esta
provada no laboratorio ou e reinstanciacao direta de um padrao ja
type-checado em tamanho menor -- risco genuinamente baixo.
**Teste revisado:** como proposto, sem alteracao: provar
`spectrum R YM1.TransferGap.M = {1, 3}` via `Matrix.eval_charpoly` +
`Matrix.det_fin_two` + `Matrix.mem_spectrum_iff_isRoot_charpoly`
(espelhando `A_spectrum_real`), depois
`rw [M_isHermitian.spectrum_real_eq_range_eigenvalues]` para concluir
`Set.range M_isHermitian.eigenvalues = {1, 3}`.

**YM-2-Simple — SURVIVES.** `Polynomial.funext [Infinite R]`
(`Algebra/Polynomial/Roots.lean:459`) confirmado, com `Infinite R`
descarregado genericamente via `CharZero.infinite`
(`Algebra/CharZero/Infinite.lean:21`). `rootMultiplicity_mul`
(`RingDivision.lean:291`), `rootMultiplicity_X_sub_C_pow`
(`RingDivision.lean:162`) conferem exatos. `A_charpoly_eval` ja provado
(`PerronFrobeniusInstance.lean:165-178`), mas a fatoracao polinomial em
si nao esta feita em lugar nenhum -- trabalho genuinamente incremental.
Peca faltante na lista de citacoes do candidato: `Polynomial.
rootMultiplicity_eq_zero` (`Div.lean:636`), necessaria para zerar a
multiplicidade do fator nao-correspondente.
**Teste revisado:** apos `Polynomial.funext`, usar `rootMultiplicity_mul`
+ `rootMultiplicity_X_sub_C_pow`/`rootMultiplicity_X_sub_C_self` para o
fator correspondente E `Polynomial.rootMultiplicity_eq_zero`
(`Div.lean:636`) para o fator nao-correspondente (ex.: multiplicidade de
4 em `(X-C 1)^2` = 0, ja que 4 nao e raiz), para chegar em
`rootMultiplicity 4 A.charpoly = 1` e `rootMultiplicity 1 A.charpoly = 2`.

**YM-1+YM-3 — NEEDS_NARROWING.** A alegacao central de "ponte ausente"
esta errada: `Mathlib/Analysis/CStarAlgebra/Matrix.lean` existe
especificamente para isso -- `Matrix.toEuclideanCLM`
(`≃⋆ₐ[𝕜] (EuclideanSpace 𝕜 n →L[𝕜] EuclideanSpace 𝕜 n)`, linha 102) e
`Matrix.l2_opNorm_toEuclideanCLM` (`‖toEuclideanCLM A‖ = ‖A‖`, linha 228,
`rfl`) sao a ponte, ja provada, para o tipo exato `E →L[R] E` que o YM-3
usa (n=Fin 2, k=R) -- torna a tarefa mais facil do que o candidato
esperava, nao mais dificil. O que **nao** esta resolvido: essa igualdade
so vale sob a instancia `NormedAddCommGroup` opcional
`Matrix.Norms.L2Operator`, distinta das instancias `linftyOp`/Frobenius
padrao (essas sim confirmadas ausentes de ponte); nenhuma lema de
comparacao entrywise/Frobenius-vs-L2Operator foi encontrada -- obter um
bound numerico concreto (ex.: `‖M1-M2‖ <= 0.1`) ainda exige achar essa
comparacao ou um argumento manual estilo Cauchy-Schwarz, uma camada acima
da que o candidato assumia, mas partindo do equiv correto em vez de
`toEuclideanLin` cru.
**Teste revisado:** antes da composicao completa, isolar o gargalo
correto: `open scoped Matrix.Norms.L2Operator` e verificar que
`Matrix.toEuclideanCLM (!![2,1;1,2.1] - !![2,1;1,2] : Matrix (Fin 2)
(Fin 2) R)` unifica com `(E →L[R] E)` e que `Matrix.l2_opNorm_
toEuclideanCLM` reescreve `‖toEuclideanCLM (M1 - M2)‖` para
`‖M1 - M2‖` (a norma L2Operator escopada) via `map_sub` no star-algebra
equiv. Separadamente -- a pergunta genuinamente aberta -- tentar achar ou
provar um bound numerico nessa norma L2Operator para a matriz de
diferenca concreta (via `ContinuousLinearMap.opNorm_le_bound` aplicado
diretamente a `toEuclideanCLM (M1-M2)`) OU achar lema de comparacao
op-norm-vs-entrywise/Frobenius existente. Se nenhum dos dois fechar numa
sessao, arquivar a composicao completa e reportar qual dos dois
sub-passos (a ponte, agora confirmada existir; ou o bound numerico
concreto, ainda nao confirmado) e o obstaculo real.

---

## 5. Hodge Conjecture (HG) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| HG-1b | Estender a ponte de divisor-principal de f = germe(secao global) para f = a/b geral | SURVIVES | moderado |
| HG-4b | Provar que o predicado de funcao-de-transicao-holomorfa rejeita conjugacao complexa | SURVIVES | baixo |

**Passo original vs. o que mudou.** Ambos continuam genuinamente abertos
(nenhuma alegacao de Pic/ClassGroup->cohomologia mudou, e a ausencia de
"conj nao e holomorfa" em Mathlib foi reconfirmada). Mas em HG-1b a
citacao especifica do candidato para o passo de compatibilidade
(`algebraMap_germ_eq_germToFunctionField`) nao e a peca que realmente
fecha o gap -- rastreando mais fundo, o passo real fecha por `rfl`/unfold
puro via `Scheme.ΓSpecIso_inv` + `StructureSheaf.toStalk`, tornando a
extensao **mais rotineira** do que o proprio candidato ou o HG-1 original
previam.

**HG-1b — SURVIVES.** `ord_mul` (`OrderOfVanishing.lean:81-86`) da
`ord (f*g) x = ord f x + ord g x` para f,g != 0, conferido exato.
`IsFractionRing.div_surjective` (`Localization/FractionRing.lean:260`) e
`functionField_isFractionRing_of_affine` (`FunctionField.lean:115-123`)
conferem, aplicando-se diretamente a X = Spec Z. Grep confirma ausencia
de `Scheme.Pic` e de qualquer lema ligando `AlgebraicCycle` a
`ClassGroup`/`FractionalIdeal`, como alegado. Correcao: `Scheme.ΓSpecIso_
inv` (`Scheme.lean:642`, provado por `rfl`) + desdobrar `StructureSheaf.
toStalk` (`StructureSheaf.lean:557`) e a cadeia realmente decisiva, nao o
lema originalmente citado.
**Teste revisado:** provar `algebraMap Z testScheme.functionField x =
testScheme.germToFunctionField ⊤ ((Scheme.ΓSpecIso testRing).inv x)` para
x : Z nao-nulo via `Scheme.ΓSpecIso_inv` + desdobramento de
`StructureSheaf.toStalk`. Decompor f = 3/2 via
`IsFractionRing.div_surjective (A := Z)`, aplicar essa identidade a
numerador e denominador, invocar `ord_mul` (precisa f_num != 0,
f_denom != 0, ambos de `IsFractionRing.to_map_ne_zero_of_mem_
nonZeroDivisors`/injetividade), e reduzir a duas aplicacoes do argumento
`finite_support_ord_f` ja provado por HG-1 (uma para a0=3, uma para
a0=2). Criterio de sucesso inalterado (`#print axioms`).

**HG-4b — SURVIVES.** `HolomorphicTransitionProbe.lean` confirmado por
leitura integral, incluindo o gap residual honestamente marcado no
proprio comentario de fechamento ("nao verifica que o predicado rejeita
mapas real-suaves nao-holomorfos como conjugacao complexa").
`Complex.conjCLE` (`Analysis/Complex/Basic.lean:256`, `conjCLE_apply`
:275), `HasFDerivAt.unique` (`FDeriv/Basic.lean:174`),
`HasFDerivAt.restrictScalars` (`FDeriv/RestrictScalars.lean:56-58`)
conferem exatos; busca por fato pronto "conj nao e holomorfa" nao
encontrou nada (`Deriv/Star.lean:106-125` so tem fatos sobre conjugar um
f ja diferenciavel, nao sobre conj em si; `Complex/Conformal.lean` tem
maquinaria de Cauchy-Riemann adjacente mas nenhuma declaracao direta).
`ContinuousLinearEquiv.hasFDerivAt` (usado em
`Geometry/Manifold/Instances/Sphere.lean:509` e
`Analysis/Fourier/FourierTransformDeriv.lean:118`) fornece diretamente
`HasFDerivAt conjCLE conjCLE x` -- a metade que o esboco do candidato
precisa mas nao cita explicitamente.
**Teste revisado:** mesmo teste proposto, adicionando
`ContinuousLinearEquiv.hasFDerivAt` (para `Complex.conjCLE : C ≃L[R] C`)
como quarto primitivo explicito, fornecendo `HasFDerivAt (starRingEnd C)
(Complex.conjCLE : C →L[R] C) x` -- os tres primitivos originalmente
citados nao produzem esse fato por si so.

---

## 6. Birch and Swinnerton-Dyer (BSD) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| BSD-1-STEP1-COMPOSE | Ponte localizacao-corpo-de-residuo via dois lemas Mathlib ja provados | SURVIVES | baixo |
| BSD-1-STEP2-CORE | Nucleo de sobrejetividade do lema de corpo-de-residuo-de-completacao | NEEDS_NARROWING | moderado |
| BSD-1-STEP2-FULL | Lema completo e incondicional de invariancia-por-completacao do corpo de residuo, tentado inteiro | REFUTED | — |

**Passo original vs. o que mudou.** O passo original (BSD-1, gap
diagnosticado na Onda 1: "corpo de residuo da completacao adica e
potencia de primo") continua genuinamente aberto e sem lema-ponte no
Mathlib. Tres angulos foram testados: um (STEP1-COMPOSE) fecha limpo, um
(STEP2-CORE) precisa de reescopo e esta emaranhado com o primeiro, e um
(STEP2-FULL, tentar tudo de uma vez) e refutado por um **muro de tipagem
estrutural**, nao por dificuldade de prova -- `O_K` nunca e anel local
para um corpo de numeros, entao o mapa composto que STEP2-FULL declara
como alvo nao pode ser sequer **enunciado** com `O_K` como origem.

**BSD-1-STEP1-COMPOSE — SURVIVES.** `IsLocalization.AtPrime.
equivQuotMaximalIdeal` (`Localization/AtPrime/Basic.lean:559`) e
`valuationSubringAtPrime_eq_valuationSubring`
(`DedekindDomain/AdicValuation.lean:504-506`) conferem exatos, ambos com
prova completa (sem sorry). Pre-requisitos confirmados: `Rp :=
valuationSubringAtPrime K v` e local (linha ~460) e carrega
`IsLocalization (v.asIdeal.primeCompl) Rp` (linha 497) -- exatamente o
que `equivQuotMaximalIdeal` precisa. O "risco de reconciliacao" que o
proprio candidato levantou (se `IsLocalRing.ResidueField` desdobra
compativel com o quociente cru usado por `equivQuotMaximalIdeal`) nao e
risco real: `IsLocalRing.ResidueField R := R ⧸ maximalIdeal R`
literalmente, por definicao (`ResidueField/Defs.lean:30-31`) -- mesmo
objeto ate definicionalmente. Este candidato evita corretamente as
armadilhas de tipo dos outros dois (nao exige `IsLocalRing` em `O_K`
inteiro, so `p.IsMaximal` no ideal de origem).
**Teste revisado:** nenhuma alteracao necessaria; teste como proposto
esta bem tipado e bem escopado.

**BSD-1-STEP2-CORE — NEEDS_NARROWING.** `denseRange_algebraMap`
(`DedekindDomain/AdicValuation.lean:883`), `Valued.isOpen_ball`/
`isClosed_ball`/`isClopen_ball` (`Valued/ValuationTopology.lean:233/245/253`,
confirmado `Valued (adicCompletion K v) Zm0` existe em :708),
`Valuation.mem_maximalIdeal_iff` (`ValuationSubring.lean:882-884`)
conferem exatos. Mas o teste como escrito tem defeito de tipo real
(subtrai dois elementos apos coercao ao corpo de completacao ambiente,
depois alega que a diferenca pertence ao ideal maximal da SUBALGEBRA --
nao elabora como escrito) e emaranha-se silenciosamente com
STEP1-COMPOSE: densidade de K so produz um aproximante k : K, nao um
elemento literal y : O_K -- ir de k ate y exige exatamente a
sobrejetividade de `equivQuotMaximalIdeal` do STEP1, nao citada pelo
STEP2-CORE. Alem disso, `IsLocalRing.ResidueField.map` exige
`[IsLocalRing R]` na origem, e `O_K` nunca e local (`RingOfIntegers.
not_isField`, `NumberField/Basic.lean:305`, mais infinitos ideais
maximais) -- a origem correta para qualquer passo `ResidueField.map` e
`Rp = valuationSubringAtPrime K v` (confirmado local,
`ValuationSubring.lean:148`), nao `O_K`.
**Teste revisado:** restringir exatamente a peca que so precisa dos tres
ingredientes proprios deste candidato: para K corpo de numeros, v um
lugar `HeightOneSpectrum`, x um elemento de `v.adicCompletionIntegers K`,
provar que existe um elemento de localizacao k de
`valuationSubringAtPrime K v` com `Valued.v` aplicado a (coercao de x em
`v.adicCompletion K` menos coercao de k) estritamente menor que 1 --
produzindo um elemento de localizacao, nao um elemento literal de `O_K`,
como testemunha, fraseando proximidade diretamente via a valuacao em vez
de pertencimento a ideal em subtipo. So depois desse fechar deve o passo
seguinte (elemento de localizacao -> elemento real de `O_K`, tarefa do
STEP1-COMPOSE) ser tentado como composicao separada.

**BSD-1-STEP2-FULL — REFUTED.** O teorema-alvo exato nomeado pelo
candidato -- `Function.Bijective` de `IsLocalRing.ResidueField.map`
aplicado a `algebraMap` de `O_K` para `v.adicCompletionIntegers K` -- nao
pode ser sequer **declarado** em Lean. `IsLocalRing.ResidueField.map`
(`ResidueField/Basic.lean:96`) vive sob `variable [CommRing R]
[IsLocalRing R] [CommRing S] [IsLocalRing S]` (linha 27): a origem R
precisa carregar `IsLocalRing`, e `O_K` nunca carrega (confirmado por
`RingOfIntegers.not_isField` mais o fato padrao de que `O_K` e dominio de
Dedekind 1-dimensional com infinitos ideais maximais, para todo corpo de
numeros, incluindo K=Q onde `O_K`=Z). E um muro de tipagem, nao um
problema de orcamento de esforco -- a propria moldura de risco do
candidato ("se nao fechar numa sessao, adiar para Onda 3") descreve mal o
modo de falha. A rota correta deve fatorar pelo anel LOCAL
`Rp = valuationSubringAtPrime K v`: encadear `O_K/v.asIdeal ≃
ResidueField(Rp)` (STEP2-CORE/STEP1-COMPOSE) com `ResidueField(Rp) ≃
ResidueField(adicCompletionIntegers K v)` via `ResidueField.map` de
`algebraMap Rp (adicCompletionIntegers K v)` -- ambos `Rp` e
`adicCompletionIntegers K v` sao confirmados locais
(`ValuationSubring.lean:148`), entao essa versao e enunciavel. Mesmo essa
versao corrigida ainda precisa de uma instancia `IsLocalHom` para
`algebraMap Rp (adicCompletionIntegers K v)` que **nao foi encontrada em
lugar nenhum do Mathlib** (grep em torno de `adicCompletionIntegers`,
`HeightOneSpectrum`, `valuationSubringAtPrime` -- zero hits); existe
instancia generica estruturalmente similar
(`instIsLocalHomValuationInteger`, `Valuation/Extension.lean:196`), mas
depende de `Valuation.HasExtension`, nunca conectada a `v.adicCompletion K`
em lugar nenhum (zero usos fora do proprio arquivo `Extension.lean`) --
entao tambem nao e instancia gratuita, e trabalho real por si.
**Teste revisado:** substituir o alvo pelo composto corretamente tipado.
Primeira sonda (antes de tentar bijetividade): existe, ou e barato provar,
uma instancia `IsLocalHom` para `algebraMap` de
`IsDedekindDomain.HeightOneSpectrum.valuationSubringAtPrime K v` para
`v.adicCompletionIntegers K` -- ex. via `Valuation.HasExtension`,
exigindo primeiro provar `(v.valuation K).HasExtension (Valued.v :
Valuation (v.adicCompletion K) Zm0)`. So se essa sonda de existencia de
instancia for bem-sucedida deve o composto completo de bijetividade
(originado em Rp, nao em `O_K`) ser tentado, encadeado com a equivalencia
do STEP1-COMPOSE para o transporte de cardinalidade.

---

## 7. Sintese TOE (extensao interna do laboratorio — NAO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| TOE-3a | Promover `Monoid Shift3` para `Group Shift3`, desbloquear `Groupoid (ActionCategory G X)` | SURVIVES | baixo |
| TOE-3b | Instanciar `MulAction.IsPretransitive Shift3 Regime3` a partir de FOUND-SG-013, desbloquear `IsConnected RegimeCat` | SURVIVES | minimo |
| TOE-3c | Segunda acao de brinquedo genuinamente nao-livre (monoide idempotente de 2 elementos K) como testemunha nao-Faithful | SURVIVES | moderado |

**Passo original vs. o que mudou.** O TOE-3 originalmente previsto
(functor entre `ActionCategory` e uma categoria derivada de grafo
funcional) esta confirmado **morto na largada como escopado**: computei
a mao `Shift3.apply` para os tres pontos-base (alpha/beta/gamma) e cada
orbita e uma bijecao Shift3->Regime3 -- Shift3 age livre e simplesmente
transitivamente sobre Regime3, logo por `hom_as_subtype`
(`Action.lean:92`, `rfl`) todo Hom-set de `RegimeCat` e um singleton. O
teste "testemunha nao-Faithful" originalmente planejado nao tem chance de
achar dois morfismos distintos com mesma imagem, porque nao ha dois
morfismos distintos em nenhum Hom-set para comecar. Tres candidatos
sucessores substituem o TOE-3 original, cada um desbloqueando uma
consequencia estrutural diferente dessa mesma descoberta de torsor.

**TOE-3a — SURVIVES.** `Regime3.lean:63-70` (`Shift3.comp`) confirma a
tabela de inversos por leitura direta dos `match arms` (nao so alegacao):
`comp forward forward2 = identity`, `comp forward2 forward = identity`,
`comp identity identity = identity`. Mathlib `Action.lean:139-140`
(`instance : Groupoid (ActionCategory G X) := CategoryTheory.
groupoidOfElements _` sob `section Group`, `variable [Group G]
[MulAction G X]` linha 137) confere verbatim; `MulAction Shift3 Regime3`
ja e instancia (`Semigroups/Action.lean:31-34`), entao so falta `Group
Shift3` (grep confirma zero `Group Shift3`/`Inv Shift3` em toda a arvore
do laboratorio). `Group` em `Algebra/Group/Defs.lean:1219-1220` confere.
O idioma de prova proposto (`revert a; decide`) e o mesmo ja usado com
sucesso em `Theorems.lean:20-22,35` -- risco tecnico baixo. Correcao de
citacao: a observacao "so Monoid nao Group" foi mal-atribuida a
`ActionCategoryRegime3.lean:33-39` (que trata do problema nao-relacionado
de `Fintype.ofEquiv`/`objEquiv`); o fato em si continua verdadeiro.
**Teste revisado:** mesmo teste, corrigindo so a citacao para apontar a
`instance : Monoid Shift3` (Action.lean/Theorems.lean) mais a ausencia de
qualquer instancia `Group`, em vez de `ActionCategoryRegime3.lean:33-39`.

**TOE-3b — SURVIVES.** Sem defeitos encontrados em nenhuma citacao,
laboratorio ou Mathlib. `Theorems.lean:66-68` (`apply_transitive`)
confirmado verbatim, defeq a `MulAction.IsPretransitive.exists_smul_eq`
ja que `smul := Shift3.apply` por definicao. `Algebra/Group/Action/
Pretransitive.lean:60-62` e `CategoryTheory/Action.lean:130-133`
(`instance [IsPretransitive M X] [Nonempty X] : IsConnected
(ActionCategory M X)`) conferem exatos. `Nonempty Regime3` trivial
(`⟨.alpha⟩`). O aviso do proprio candidato (que `IsConnected` e nocao
categorica de zigzag-alcancabilidade, nao alegacao fisica apesar da
sobreposicao de vocabulario "regime/interface conectado") e adicao
apropriadamente cautelosa, nao exagero.
**Teste revisado:** nenhuma alteracao necessaria; prosseguir como
especificado.

**TOE-3c — SURVIVES.** A alegacao central de torsor por tras de todo o
diagnostico de obsolescencia foi verificada independentemente a mao (nao
so confiada): para cada ponto-base, `{id•x, forward•x, forward2•x}` e
`Regime3` completo, bijetivo. `hom_as_subtype`
(`CategoryTheory/Action.lean:92`, `rfl`) confirmado verbatim. Ausencia de
instancia `Decidable` para `Faithful` confirmada por grep e leitura de
`FullyFaithful.lean:52`. Ausencia de qualquer lema Mathlib ligando
cardinalidade de Hom-set a liberdade de acao confirmada por leitura
integral das 211 linhas de `Action.lean` -- entao o flag de "conteudo
original nao-formalizado do laboratorio" do candidato e honesto, nao
citacao disfarcada. O monoide K de 2 elementos (um idempotente
nao-identidade, acao constante mapeando tudo para alpha) e construcao
finita padrao, provavel pelo mesmo idioma `decide`-apos-`revert` ja
funcionando em outro lugar do laboratorio, e o `Hom(alpha,alpha)`
resultante genuinamente tem dois elementos distintos
(`⟨id,rfl⟩`/`⟨k,rfl⟩`). Este e o maior e menos precedentado dos tres
(novo monoide + nova acao + novo functor, vs. a promocao quase-mecanica
de typeclass de 3a/3b sobre lemas ja provados) -- sequenciar depois de 3a
e 3b, nao em paralelo.
**Teste revisado:** como especificado; se cortar escopo, a versao minima
e so construir K e sua instancia `MulAction` e exibir diretamente os dois
elementos distintos de `Hom(alpha,alpha)` via `decide`, adiando o passo
completo de colapso-por-functor (que so re-demonstra nao-injetividade ja
visivel no Hom-set de dois elementos) como follow-on opcional.

---

## 8. Fundamentos Quanticos / Unificacao (extensao interna — NAO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| QF-5 | Identidade operatorial de fluxo-comutador de Heisenberg | SURVIVES | baixo |
| QF-6 | Fundacao de quantizacao por deformacao / geometrica / Wigner-Weyl-Moyal | REFUTED | very_high |

**Passo original vs. o que mudou.** QF-5 (continuacao natural do QF-4 da
Onda 1, que isolou `hasFDerivAt_exp_smul_const_of_mem_ball`) continua
genuinamente aberto e e o alvo real desta rodada. QF-6 e um angulo
inteiramente novo, nao continuacao de item fechado -- e corretamente
autoexcluido pelo proprio candidato como infraestrutura greenfield.

**QF-5 — SURVIVES.** `HasFDerivAt.mul'` (`Analysis/Calculus/FDeriv/
Mul.lean:198-202`, confirmado sem hipotese de comutatividade em 𝔸 --
formula assimetrica segura para nao-comutativo `a x • b' + a' <• b x`),
`Commute.exp_right` (`Exponential.lean:228-229`), `HasFDerivAt.neg`
(`FDeriv/Add.lean:525`) conferem exatos; grep amplo por "ehrenfest"/
"heisenberg" em todo o Mathlib retorna zero hits -- montagem genuina, nao
atalho de citacao. Re-derivei a identidade-alvo a mao: diferenciar
`t -> exp(-t*H)` via `hasFDerivAt_exp_smul_const_of_mem_ball`
instanciado em `x := -H` (rota mais simples que a composicao neg-depois-
comp do candidato, embora a rota do candidato tambem funcione via
`HasFDerivAt.comp`, `FDeriv/Comp.lean:105`, curiosamente omitido da
lista de citacoes), depois aplicar `mul'` duas vezes e usar
`Commute H (exp(tH))` para deslizar H atraves do segundo fator -- a
algebra fecha exatamente em `A(t)*H - H*A(t)`. `still_missing_if_success`
honesto: so dimensao finita/limitado, sem produto interno, sem hbar->0,
QCU-001 continua UNSCOPED.
**Teste revisado:** mesmo teste, com uma simplificacao a tentar primeiro:
instanciar `hasFDerivAt_exp_smul_const_of_mem_ball` diretamente em
`x := -heisenbergGenerator` (em vez de `HasFDerivAt.neg` composto com a
instanciacao em `x:=H`), reduzindo o numero de lemas necessarios de 5
para 4 antes de recorrer a `noncomm_ring` para o reagrupamento final.

**QF-6 — REFUTED.** Buscas re-executadas independentemente em todo o
Mathlib vendorizado: "Moyal", "star.?product", "Kontsevich", "Wigner",
"Weyl.*quant", "geometric.?quantization", "deformation.?quantization",
"prequantization", "PoissonBracket" -- todas 0 hits, exatamente como
alegado. Busca "symplectic" retorna exatamente os 4 arquivos citados
(`Lie/Classical.lean`, `InnerProductSpace/StandardSubspace.lean`,
`Hofer.lean`, `SymplecticGroup.lean`), nenhum constituindo estrutura de
variedade simpletica ou colchete de Poisson usavel para quantizacao.
QCU-001 UNSCOPED confirmado (`SCOPE.md:4`). Todas as alegacoes factuais
conferem -- e exatamente por isso que o veredito e REFUTED como alvo de
Onda 2: `plausibility=low`, `cost_estimate=very_high`, e condicao de
falsificacao ("quase certo de disparar imediatamente") do proprio
candidato equivalem a autodesqualificacao. Construcao de infraestrutura
matematica greenfield do zero -- exatamente a categoria que o proprio
gate adversarial do QF-4 da Onda 1 ja rejeitou ("se exige construir
infraestrutura do zero, desprioriza").
**Nao agendar como alvo de Onda 2.** As buscas ja executadas (e
reproduzidas independentemente aqui) bastam como documentacao de
diligencia; nenhum arquivo Lean deve ser tentado, ja que mesmo o
"fragmento mais barato" (uma forma bilinear antissimetrica nua) nao
constituiria passo reconhecivel em direcao a Moyal/Kontsevich/quantizacao
geometrica, so inflaria a contagem de claims com uma definicao
desconectada de qualquer teorema.

---

## Infraestrutura compartilhada entre frentes (continuacao)

Tres candidatos desta onda estendem diretamente as pecas de infraestrutura
compartilhada ja identificadas na Onda 1 (toolkit de espectro/traco em
dimensao finita: RH-3/RH-4, YM-1/YM-2/YM-3, QF-2).

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| SHARED-INFRA-2B | Gap de realidade-do-espectro-complexo do YM-2 | SURVIVES | baixo |
| SHARED-INFRA-2A | Estabilidade Lipschitz do segundo autovalor do YM-3 (2D fixo) | NEEDS_NARROWING | baixo-moderado |
| SHARED-INFRA-2C | Sonda de ponte de inversao espectral do RH-4 | NEEDS_NARROWING | baixo |

**SHARED-INFRA-2B — SURVIVES.** Citacao do YM-2 confirmada exata
(`PerronFrobeniusInstance.lean:74-85`: "nao verifica separadamente que A
... nao tem autovalor complexo nao-real"). `Matrix.IsHermitian.
spectrum_eq_image_range` (`Analysis/Matrix/Spectrum.lean:204`) confirmado
exato, sem carga extra de `DecidableEq`/`Fintype` alem do que ja esta em
escopo. Achado mais direto que o alegado: `isHermitian_iff_isSymm`
(`LinearAlgebra/Matrix/Hermitian.lean:69`) e `IsHermitian.map`
(linha 73) transformam a simetria real de A ja provada pelo YM-2
diretamente em `(A.map (algebraMap R C)).IsHermitian` em essencialmente
uma linha, antes mesmo de invocar `spectrum_eq_image_range`. Fecha um gap
que o proprio laboratorio ja nomeou, com escopo honesto
(`still_missing_if_success` fica corretamente calado sobre Perron-
Frobenius geral, Yang-Mills fisico, ou o problema Clay).
**Teste revisado:** teste como proposto e bem formado; adicionar citacao
explicita de `isHermitian_iff_isSymm` + `IsHermitian.map` como o passo de
ponte concreto de duas linhas.

**SHARED-INFRA-2A — NEEDS_NARROWING.** Citacao do YM-3 exata
(`FixedDimEigenvalueStability.lean:81-92`); `Spectrum.lean:87/312/320` e
`Symmetric.lean:137` conferem verbatim; grep amplo confirma ausencia de
Weyl/Courant-Fischer/min-max fora de teoria de Lie. Mas o teste proposto
tem um buraco matematico real: restringir A ao complemento ortogonal do
proprio autovetor-topo de A e B ao proprio autovetor-topo de B produz
dois subespacos 1-dimensionais DIFERENTES (a menos que A,B compartilhem
autovetor) -- repetir o argumento de Rayleigh de operador unico
separadamente para cada um nao produz por si so o bound cruzado
`|lambda2 A - lambda2 B| <= ‖A-B‖`; a prova classica de perturbacao de
Weyl precisa do min de Courant-Fischer sobre TODOS os subespacos
1-dimensionais (mesmo subespaco limitando ambos operadores ao mesmo
tempo) -- exatamente a maquinaria ja confirmada ausente. Achado nao
citado pelo candidato: `LinearMap.IsSymmetric.trace_eq_sum_eigenvalues`
(`InnerProductSpace/Trace.lean:39`) da, na dimensao fixa n=2, `lambda2 =
trace(T) - lambda1(T)` **exatamente** (so 2 autovalores existem),
contornando completamente o problema de Courant-Fischer.
**Teste revisado:** abandonar a rota `restrict_invariant`/
`invariant_orthogonalComplement_eigenspace`. Em vez disso, em
`E := EuclideanSpace R (Fin 2)`, para A,B simetricos, usando
`hT.eigenvalues hn : Fin 2 -> R` junto com `IsSymmetric.trace_eq_sum_
eigenvalues`, definir `lambda2 T := (LinearMap.trace R E T) -
lambdaMax T`, provar `|trace A - trace B| <= 2*‖A-B‖` via `trace_eq_sum_
inner` sobre base ortonormal fixa (espelhando a tecnica de bound
pontual ja existente do YM-3), depois combinar linearmente com o
`lambdaMax_lipschitz` ja provado do YM-3 para obter
`|lambda2 A - lambda2 B| <= 3*‖A-B‖`.

**SHARED-INFRA-2C — NEEDS_NARROWING.** Citacao do RH-4 confirmada exata
(`SpectralCountingLimit.lean:50-57`: "exige uma inversao espectral ...
que nao esta formalizada aqui"); `spectrum.inv_mem_iff`
(`Algebra/Algebra/Spectrum/Basic.lean:206`) confere exato; ausencia de
`LinearPMap`+spectro/resolvente confirmada (zero hits em 8 arquivos
verificados). Mas o teste proposto e quase vazio como sonda de
viabilidade: `inv_mem_iff` e verdade puramente algebrica incondicional
para QUALQUER unidade em QUALQUER algebra com unidades -- instancia-lo
num operador diagonal limitado trivialmente invertivel, escolhido a
dedo, esta garantido a compilar por construcao, entao um resultado
"passa" carregaria quase nenhuma informacao sobre se a ponte real e
tratavel. A analogia tambem e mais fraca do que apresentada: a obrigacao
real do GWB nao e "um elemento e seu proprio inverso algebrico numa
algebra fixa", e sim o espectro de um operador parcial nao-limitado
Lambda versus o espectro de um operador LIMITADO DIFERENTE R =
(Lambda-z)^-1 construido via resolvente -- um teorema de mapeamento
espectral/resolvente, nao a forma de `inv_mem_iff`.
**Teste revisado:** pular `spectrum.inv_mem_iff` (vai passar trivialmente
e nao provar nada). Tentar em vez disso o passo genuinamente informativo:
caracterizar `mu : R` como "autovalor de um `LinearPMap` T" via
`exists v in T.domain, v != 0, T v = mu * v` (contornando espectro/
resolvente inteiramente, ja que nenhum existe para `LinearPMap`), e
conectar isso a mao (nenhum lema Mathlib de inversao espectral se aplica)
a `Module.End.HasEigenvalue` de um R limitado construido como mapa
inverso explicito num `LinearPMap` diagonal nao-limitado de brinquedo
(dominio = sequencias de suporte finito, T x_n = n*x_n, R = o operador
diagonal limitado 1/(n+1) ja disponivel em `SpectralCounting.InfDim.T`).
Se mesmo esse passo definicional ad hoc exigir infraestrutura nova
substancial, esse e o bound de custo honesto e informativo que o teste
original nao produziu.

---

## Lista de execucao Onda 2 (despacho direto para agente de formalizacao)

Cada item abaixo traz o candidato, o teorema-alvo, e o enunciado de teste
exato (ja revisado pela adversarial), pronto para um agente de
formalizacao executar sem reinterpretacao. Ordem: por linha, na mesma
sequencia das secoes acima. Todos sao independentes entre si a menos que
anotado.

```text
 1. RH / RVM-LIMIT-ERROR
    Provar, como corolario de tendsto_tLog_of_eq_main_add_littleO
    (SB-GAP-010A, ja fechado): (a) e =o[atTop] (T*log T) via
    IsBigO.trans_isLittleO a partir de e =O[atTop] log T e
    log T =o[atTop] (T*log T); (b) rvmFormula - c*(T*log T) =o(T log T),
    extraido de tendsto_rvmLimitFormula_div_tLogScale; (c) somar os dois
    termos o(T log T) e invocar tendsto_tLog_of_eq_main_add_littleO.
    Registrar como item novo com gate/DEC proprio. #print axioms so com
    os 3 axiomas padrao.

 2. RH / NZeta-STRUCTURE
    Provar Monotone NZeta (via zetaZerosInStrip_subset composto com
    Set.ncard_le_ncard contra NZeta_region_finite T2 como testemunha de
    finitude) e NZeta T = 0 para T <= 0 (via zetaZerosInStrip T =
    (empty : Set C) por Set.Ioc_eq_empty).

 3. NS / NS-2a (hasLocalPV_K_mul_lipschitz)
    Declarar hasLocalPV_K_mul_lipschitz (g : E -> R)
    (hg : LipschitzWith L.toNNReal g). Substituir a igualdade exata
    hphidiff por |g y - g 0| <= L * ‖y‖ via hg.dist_le_mul y 0 (reescrito
    por dist_eq_norm); reescrever hnormeq e o calc final de hdecay como
    cadeia <= terminando em C*L*‖y‖^(-2). Manter phi_lipschitz so para
    mensurabilidade/continuidade.

 4. NS / NS-2b (pvK, depende de NS-2a fechar)
    Tentar pvK (e2 e3 : EuclideanSpace R (Fin 3)) :
    𝓓'^{1}(EuclideanSpace R (Fin 3), R) (ordem 1) no espaco COMPLETO
    (nao Omega \ {0}), restrito primeiro a um unico compacto
    K = closedBall 0 R, via TestFunction.mkCLM com cont descarregado
    pelo bound Lipschitz de NS-2a contra as seminormas N[K,1,i].

 5. PN / PN-5 (testemunha certificado nao-trivial)
    Construir FinTM2 com K:=Unit, sigma:=Bool: pop x, pop c com funcao de
    atualizacao decide (ob.getD false = !v), push, load-reset, halt,
    verificando Bool x Bool -> Bool. Provar TM2ComputableInPolyTime via
    steps:=1 / rfl. Ja confirmado compilar standalone.

 6. PN / PN-2' (goto-encadeado, mesma pilha)
    Construir uma FinTM2 (Lambda := Bool ou 2 elementos, K:=Unit,
    Gamma:=Bool) com goto cruzando duas fases; outputsFun com steps := 2,
    evals_in_steps := rfl. So recorrer a EvalsToInTime.trans explicito se
    a rota direta falhar para caso onde steps depende do comprimento do
    input.

 7. YM / YM-1-Connect
    Provar spectrum R YM1.TransferGap.M = {1, 3} via Matrix.eval_charpoly
    + Matrix.det_fin_two + Matrix.mem_spectrum_iff_isRoot_charpoly
    (espelhando A_spectrum_real), depois rw
    [M_isHermitian.spectrum_real_eq_range_eigenvalues] para concluir
    Set.range M_isHermitian.eigenvalues = {1, 3}.

 8. YM / YM-2-Simple
    Via Polynomial.funext, decompor A.charpoly usando rootMultiplicity_mul
    + rootMultiplicity_X_sub_C_pow/X_sub_C_self para o fator
    correspondente e Polynomial.rootMultiplicity_eq_zero para o fator
    nao-correspondente. Concluir rootMultiplicity 4 A.charpoly = 1 e
    rootMultiplicity 1 A.charpoly = 2.

 9. YM / YM-1+YM-3 composicao (bound de norma de operador)
    Sonda 1: open scoped Matrix.Norms.L2Operator; verificar que
    Matrix.toEuclideanCLM (!![2,1;1,2.1] - !![2,1;1,2]) unifica com
    (E →L[R] E) e que Matrix.l2_opNorm_toEuclideanCLM reescreve
    ‖toEuclideanCLM (M1-M2)‖ para ‖M1-M2‖ via map_sub. Sonda 2 (a
    pergunta real): achar/provar bound numerico nessa norma L2Operator
    via ContinuousLinearMap.opNorm_le_bound, OU achar lema de comparacao
    op-norm-vs-entrywise/Frobenius. Reportar qual sub-passo e o
    obstaculo se nenhum fechar numa sessao.

10. HG / HG-1b
    Provar algebraMap Z testScheme.functionField x =
    testScheme.germToFunctionField ⊤ ((Scheme.ΓSpecIso testRing).inv x)
    via Scheme.ΓSpecIso_inv + desdobramento de StructureSheaf.toStalk.
    Decompor f = 3/2 via IsFractionRing.div_surjective (A := Z), aplicar
    a numerador/denominador, invocar ord_mul, reduzir a duas aplicacoes
    de finite_support_ord_f (a0=3, a0=2).

11. HG / HG-4b
    Provar ¬ Differentiable C (starRingEnd C), usando
    ContinuousLinearEquiv.hasFDerivAt para obter HasFDerivAt
    (starRingEnd C) (Complex.conjCLE : C →L[R] C) x, mais
    HasFDerivAt.unique / HasFDerivAt.restrictScalars para a contradicao
    (mapa C-linear generico c*z nao pode igualar conj em z=1 e z=i
    simultaneamente).

12. BSD / BSD-1-STEP1-COMPOSE
    Compor IsLocalization.AtPrime.equivQuotMaximalIdeal (instanciado com
    Rp := valuationSubringAtPrime K v) com
    valuationSubringAtPrime_eq_valuationSubring para obter O_K/v.asIdeal
    ≃ IsLocalRing.ResidueField Rp.

13. BSD / BSD-1-STEP2-CORE (depende parcialmente de #12)
    Para K corpo de numeros, v : HeightOneSpectrum, x : v.
    adicCompletionIntegers K, provar existe k : valuationSubringAtPrime K
    v com Valued.v (coercao x - coercao k em v.adicCompletion K) < 1,
    via denseRange_algebraMap + Valued.isOpen_ball/mem_maximalIdeal_iff.
    Nao tentar produzir y : O_K diretamente nesta etapa.

14. TOE / TOE-3a
    Construir instance : Group Shift3 (idioma revert a; decide sobre a
    tabela de comp ja confirmada em Regime3.lean:63-70), desbloqueando
    instance : Groupoid (ActionCategory Shift3 Regime3) via
    CategoryTheory.groupoidOfElements.

15. TOE / TOE-3b
    Instanciar MulAction.IsPretransitive Shift3 Regime3 a partir de
    apply_transitive (Theorems.lean:66-68, defeq a exists_smul_eq),
    desbloqueando instance : IsConnected (ActionCategory Shift3 Regime3)
    via Nonempty Regime3 := ⟨.alpha⟩.

16. TOE / TOE-3c
    Construir monoide K de 2 elementos (identidade + k idempotente
    nao-identidade) com MulAction K Regime3 constante (tudo -> alpha).
    Exibir os dois elementos distintos de Hom(alpha,alpha) em
    ActionCategory K Regime3: ⟨id,rfl⟩ e ⟨k,rfl⟩, via decide.

17. QF / QF-5
    Instanciar hasFDerivAt_exp_smul_const_of_mem_ball em
    x := -heisenbergGenerator para obter a derivada de exp(-t*H) em um
    passo. Aplicar HasFDerivAt.mul' duas vezes, Commute.exp_right para
    deslizar H atraves do segundo fator, fechar a algebra final com
    noncomm_ring, concluindo d/dt[exp(-tH) A exp(tH)] = exp(-tH)(AH-HA)
    exp(tH) (identidade de fluxo-comutador de Heisenberg).

18. SHARED-INFRA / 2B (gap de realidade do YM-2)
    Provar (A.map (algebraMap R C)).IsHermitian via isHermitian_iff_isSymm
    + IsHermitian.map (semiconjugacao trivial de algebraMap R C com
    star), depois aplicar Matrix.IsHermitian.spectrum_eq_image_range para
    concluir spectrum C (A.map (algebraMap R C)) subseteq range(R).

19. SHARED-INFRA / 2A (segundo autovalor Lipschitz, YM-3, 2D fixo)
    Em E := EuclideanSpace R (Fin 2), definir lambda2 T := (LinearMap.
    trace R E T) - lambdaMax T usando IsSymmetric.trace_eq_sum_eigenvalues.
    Provar |trace A - trace B| <= 2*‖A-B‖ via trace_eq_sum_inner sobre
    base ortonormal fixa. Combinar linearmente com lambdaMax_lipschitz
    (ja provado no YM-3) para |lambda2 A - lambda2 B| <= 3*‖A-B‖.

20. SHARED-INFRA / 2C (sonda de ponte espectral, RH-4)
    Caracterizar mu : R como autovalor de um LinearPMap T via
    exists v in T.domain, v != 0, T v = mu * v. Conectar a mao a
    Module.End.HasEigenvalue de um operador limitado R construido como
    mapa inverso explicito num LinearPMap diagonal nao-limitado de
    brinquedo (dominio = sequencias de suporte finito, T x_n = n*x_n,
    R = operador diagonal 1/(n+1) de SpectralCounting.InfDim.T).
```

Total: **20 itens** na lista de execucao Onda 2 -- um para cada candidato
`SURVIVES`/`NEEDS_NARROWING` desta rodada (nenhum item derivado de
candidato `REFUTED` entra aqui; o follow-on de BSD-1-STEP2-FULL fica so
como nota no log de descartados abaixo, nao como item numerado). Nota de
dependencia: item 3 e 4 sao sequenciais entre si -- NS-2b depende de
NS-2a; item 13 depende parcialmente de 12 (BSD-1-STEP2-CORE reusa a
sobrejetividade de BSD-1-STEP1-COMPOSE para o ultimo passo, nao testado
isoladamente no item 13).

---

## Descartados nesta rodada (nao reabrir sem evidencia nova)

```text
PN  TM2ComputableInPolyTime.comp geral, tentado inteiro
      -- proprio candidato declara falsifiable_test N/A, cost very_high,
         plausibility low, "nao recomendado"; autoexclusao correta.
         Precisaria de fusao K1+K2 em soma de tipos mais subrotina de
         copia de fita cujo numero de passos depende do comprimento da
         saida em tempo de execucao -- quebra o truque de rfl unico que
         tornou todo outro item PN barato

BSD BSD-1-STEP2-FULL: lema completo de invariancia-por-completacao do
      corpo de residuo, tentado inteiro
      -- muro de tipagem estrutural, nao dificuldade de prova:
         IsLocalRing.ResidueField.map exige IsLocalRing na origem, e O_K
         nunca e anel local para nenhum corpo de numeros (infinitos ideais
         maximais). O alvo nomeado nao pode ser sequer declarado com O_K
         como origem. Versao corrigida (originada em Rp local) e
         enunciavel mas exige uma instancia IsLocalHom ainda nao
         encontrada em lugar nenhum do Mathlib. NAO entra na lista de
         execucao numerada (candidato REFUTED); se uma onda futura quiser
         retomar, o primeiro passo seria so a sonda de existencia dessa
         instancia IsLocalHom (via Valuation.HasExtension), separada de
         qualquer tentativa de bijetividade completa

QF  QF-6: fundacao de quantizacao por deformacao/geometrica/Wigner-Weyl-
      Moyal
      -- zero scaffold reaproveitavel (Moyal/Kontsevich/Wigner/Poisson
         bracket: 0 hits em todo o Mathlib); custo very_high e
         plausibilidade low admitidos pelo proprio candidato; exatamente
         a categoria "infraestrutura do zero" que o gate adversarial do
         QF-4 da Onda 1 ja rejeitou
```

---

## Avaliacao pessoal — os 2-3 candidatos com maior chance de virar
resultado formal honesto e nao-trivial mais cedo

Nao e repeticao da autoavaliacao dos agentes de recon/adversarial -- e
julgamento proprio depois de ler as 23 verificacoes inteiras desta onda.

**1. SHARED-INFRA-2B (gap de realidade-do-espectro-complexo do YM-2).**
E o candidato mais limpo do lote inteiro desta onda: toda citacao Mathlib
conferida por leitura integral e exata; a revisao adversarial encontrou
uma rota **ainda mais curta** do que a proposta original (`isHermitian_
iff_isSymm` + `IsHermitian.map` em duas linhas, antes mesmo de precisar
de `spectrum_eq_image_range`); fecha um gap que o proprio laboratorio ja
nomeou explicitamente em `PerronFrobeniusInstance.lean`; nao depende de
nenhum outro item desta onda; e o escopo permanece honesto (nada sobre
Perron-Frobenius geral, Yang-Mills fisico, ou o problema Clay). Risco
tecnico residual e o mais baixo de toda a lista.

**2. YM-1-Connect (espectro abstrato via `spectrum_real_eq_range_
eigenvalues`).** Cada peca do plano ja esta provada no laboratorio
(`M_isHermitian`) ou e reinstanciacao direta de um padrao ja
type-checado a uma escala maior (`A_charpoly_eval`/`A_spectrum_real` do
YM-2, para uma matriz 3x3, aplicado aqui a uma matriz 2x2 mais simples).
Nao ha ambiguidade de tipagem, direcao ou escala como em varios outros
candidatos "NEEDS_NARROWING" desta rodada -- e o teste original foi
mantido sem alteracao apos reverificacao, sinal de que o recon original
ja tinha acertado o alvo.

**3. TOE-3b (`IsPretransitive` -> `IsConnected RegimeCat`).** Nenhum
defeito de nenhum tipo foi encontrado em nenhuma citacao -- laboratorio
ou Mathlib -- durante a revisao adversarial inteira; `apply_transitive`
ja provado e literalmente defeq ao que `IsPretransitive.exists_smul_eq`
precisa, entao o "trabalho" real e quase so escrever a instancia. Coloco
na terceira posicao (nao na primeira) so porque o payoff e puramente
categorico/estrutural sobre um modelo de brinquedo, sem nenhum conteudo
fisico ou avanco em direcao a `TOE_CONVERGENCE_CRITERIA` -- mas como
aposta de "fecha limpo, sem sorpresa", e tao forte quanto SHARED-INFRA-2B
e YM-1-Connect.

Nao incluo nenhum candidato BSD ou RH-abstrato-superior no top 3: BSD-1-
STEP1-COMPOSE e genuinamente solido, mas BSD como frente carrega a
mesma advertencia da Onda 1 -- qualquer resultado "completo" ali depende
de uma ponte HeightOneSpectrum-completacao que segue sem instancia
`IsLocalHom` confirmada existir (item 14 e sonda, nao fechamento);
RVM-LIMIT-ERROR do RH e mais barato do que parecia, mas carrega risco de
governanca-processual (precisa de gate/DEC proprio antes de tocar codigo)
que os tres do top 3 nao carregam.
