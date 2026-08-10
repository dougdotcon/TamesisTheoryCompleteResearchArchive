---
document_id: PLANO-ATAQUE-ONDA-4-2026-08-10
reviewed_at: 2026-08-10
input: recon + revisao adversarial de 9 grupos (8 linhas de pesquisa + infraestrutura compartilhada) para Onda 4, ancorado nos resultados reais da Onda 3 -- ver 09_SESSIONS/2026/2026-08-10_WAVE3_EXECUTION.md (15/15 fechados, 0 gaps, 0 rejeitados) e 01_PORTFOLIO/PLANO_DE_ATAQUE_PORTFOLIO_COMPLETO_2026_08_09.md, 01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md, 01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_3_2026_08_10.md
conclusion: PLANO_DE_EXECUCAO_ONDA_4_PROPOSTO
---

# Plano de ataque — Onda 4 (continuacao das Ondas 1-3)

## Enquadramento honesto

Este documento e a continuacao direta de
`PLANO_DE_ATAQUE_PORTFOLIO_COMPLETO_2026_08_09.md`,
`PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md`,
`PLANO_DE_ATAQUE_ONDA_3_2026_08_10.md` e da sessao de execucao
`2026-08-10_WAVE3_EXECUTION.md`. A Onda 3 fechou **15 de 15** itens (12
VERIFIED, 3 VERIFIED_WITH_NOTES), com **zero** gap diagnosticado e
**zero** item rejeitado, recompilacao independente confirmada (15/15
exit 0, zero `sorryAx`, zero token proibido, `lake build` central sem
regressao, 8825 jobs identicos a antes/depois). A Onda 4 parte desse
chao real, nao de aspiracao.

```text
O que este plano E:
  - a proxima rodada de pequenos testes falsificaveis contra
    infraestrutura Mathlib genuina, construida sobre os 15 itens
    fechados na Onda 3 (e, por heranca, sobre os 20 da Onda 2 e os 25
    da Onda 1)
  - uma tentativa de re-verificar, por leitura direta de arquivo (nao por
    confianca no agente de recon) -- e, em varios casos desta onda, por
    COMPILACAO DIRETA com `lake env lean` contra o Mathlib real do
    projeto -- se os passos previstos para "depois da Onda 3" continuam
    abertos, ja foram satisfeitos por acaso, ou ficaram obsoletos
  - honesto sobre linhas/sub-frentes sem alvo pequeno disponivel nesta
    rodada e sobre onde um teste proposto tinha um defeito matematico
    real (nao so cosmetico) que o tornaria trivial ou falso

O que este plano NAO E:
  - uma alegacao de que qualquer Problema do Milenio ficou mais proximo
    de ser resolvido -- nenhum item abaixo toca o nucleo central de
    nenhuma das 6 frentes Clay-oficiais
  - uma alegacao de que TOE-INTERFACE-001 ou QCU-001 tem status
    Clay-oficial
  - uma reabertura do RH-NOGO-001
  - uma promessa de que todo teste "SURVIVES" fecha sem sorry -- e uma
    aposta informada, nao uma certeza
  - uma tentativa de inflar a contagem de itens: onde a revisao
    adversarial confirmou que um candidato precisava de reescopo
    (NEEDS_NARROWING) ou que uma peca so e recomendacao de
    infraestrutura (nao teste Lean falsificavel), isso e reportado como
    tal, nao contornado
```

Diferenca notavel em relacao as Ondas 2-3: **nenhum dos 15 candidatos
revisados nesta rodada foi REFUTED**. Isso nao significa que a barra
caiu -- a revisao adversarial desta onda efetivamente compilou dois
candidatos inteiros (`YM-STABILITY-CAPSTONE-BRACKET`,
`YM-STABILITY-CAPSTONE-FULL/Step-1`) com `lake env lean` contra o cache
Mathlib real do laboratorio, achou e corrigiu um erro matematico
substantivo (a hipotese "route (b)" do RH, incondicional sobre todo
`mu:C`, e FALSA -- contraexemplo numerico `mu=i, Lam=0.5` verificado a
mao), e narrowed dois outros candidatos (`BSD`, `QF`) por reconhecer
gaps de composicao genuinos que a self-avaliacao do candidato nao havia
isolado. O padrao "zero REFUTED" reflete um recon desta rodada
particularmente bem calibrado (nenhum grupo propos algo ja morto ou
fora de escopo), nao uma adversarial mais frouxa.

**15** candidatos revisados ao todo nos 9
grupos (8 linhas + infraestrutura compartilhada), todos
`SURVIVES`/`NEEDS_NARROWING`. Um deles (a recomendacao de registrar
`_SHARED_INFRA/FORMAL` no projeto Lake) e explicitamente uma
recomendacao de infraestrutura, nao um teste Lean falsificavel, e fica
fora da lista numerada de execucao (mesmo tratamento que `NS-3b` recebeu
na Onda 3: adiada corretamente, nao descartada por defeito). A contagem
final de itens de execucao (14, ver secao abaixo) e **menor** que os 15
da Onda 3 -- resultado esperado e reportado sem ajuste: varias linhas
renderam apenas um candidato modesto desta vez, sinal de que o
laboratorio esta se aproximando da fronteira de pequenos passos
disponiveis em varias frentes simultaneamente.

---

## 1. Riemann Hypothesis (RH) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| RH-4 | Densidade assintotica de `unboundedEigCount` -- lei-limite tipo Weyl de brinquedo | SURVIVES | baixo |
| RH-5 | Ponte de conjunto route-b: `unboundedEigCount` vs `eigCount` via `eigenvalue_bridge` (SHARED-2C) | NEEDS_NARROWING | baixo-moderado |

**Passo original vs. o que mudou.** RH-4 e continuacao direta e nova de
`UnboundedEigCountFloorLaw.lean` (RH-3, Onda 3): em vez de reprovar a
mesma identidade de contagem, testa uma proposicao logicamente diferente
(um limite, nao uma identidade) sobre o mesmo objeto de brinquedo. RH-5
tenta genuinamente exercitar a rota (b) que RH-3 documentou como
alternativa mais pesada (`eigenvalue_bridge` + `eigCount_eq_floor`), mas
a hipotese de transporte de desigualdade citada verbatim do proprio
cabecalho da Onda 3 se revelou **matematicamente falsa** como enunciado
irrestrito.

**RH-4 — SURVIVES.** Releitura integral de `UnboundedEigCountFloorLaw.lean`
(292 linhas) confirma `unboundedEigCount_eq_floor` exatamente como
`{mu | IsEigenvalue Tp mu ∧ ‖mu‖ <= Lam}.ncard = ⌊Lam⌋₊+1` para `Lam>=0`,
sobre o mesmo `LinearPMap` de brinquedo, sem nenhuma conexao com
`riemannZeta`/`N_zeta`/RVM -- e a rota (b) esta explicitamente marcada
"NOT attempted here". Grep direto no Mathlib vendorizado confirma toda
citacao na posicao exata: `tendsto_nat_floor_div_atTop`
(`Analysis/SpecificLimits/Basic.lean:739`, compoe de
`tendsto_nat_floor_mul_div_atTop` com `a=1`), `tendsto_inv_atTop_zero`
(`Topology/Algebra/Order/Field.lean:74`), `Complex.norm_natCast`
(`Analysis/Complex/Norm.lean:113`). A forma da prova e solida:
`(⌊Lam⌋₊+1)/Lam = ⌊Lam⌋₊/Lam + 1/Lam -> (1+0) = 1` via `Tendsto.add`,
`congr'`ado contra `unboundedEigCount_eq_floor` eventualmente (`Lam>=0`
eventualmente em `atTop` via `eventually_ge_atTop`). E genuinamente uma
proposicao diferente (limite, nao identidade), permanece inteiramente
dentro do fato de contagem de naturais de brinquedo sem contaminacao
zeta/GWB, e esta honestamente escopado em "ainda faltando". Custo baixo,
plausibilidade alta confirmada independentemente.
**Teste revisado:** sem estreitamento necessario; o teste como proposto
(`Tendsto (fun Lam => (unboundedEigCount Lam : R)/Lam) atTop (nhds 1)`)
esta corretamente escopado e diretamente construivel a partir de
`unboundedEigCount_eq_floor` + `tendsto_nat_floor_div_atTop` +
`tendsto_inv_atTop_zero` via um argumento `congr'`+`add`, mesma
convencao de arquivo autonomo do seu predecessor.

**RH-5 — NEEDS_NARROWING.** Releitura integral de
`LinearPMapEigenvalueBridge.lean` confirma `eigenvalue_bridge`
(linhas 279-300) exatamente como um `iff` incondicional. Ambos os lemas
Mathlib citados conferem exatos: `norm_inv`
(`Analysis/Normed/Field/Basic.lean:77`), `one_div_le_one_div`
(`Algebra/Order/Field/Basic.lean:93`). Porem a propria secao "ainda
faltando" do candidato sinalizava um risco real que se confirmou FATAL
como literalmente escrito: `Nat.floor_add_one (ha : 0<=a) :
⌊a+1⌋₊=⌊a⌋₊+1` (`Algebra/Order/Floor/Semiring.lean:311`) torna a
proposicao-alvo do teste falsificavel original --
`unboundedEigCount Lam = eigCount T (1/(Lam+1))` -- provavel em uma
linha a partir de `unboundedEigCount_eq_floor` + `eigCount_eq_floor` +
`Nat.floor_add_one`, SEM nenhuma referencia a `eigenvalue_bridge`,
`IsEigenvalue`, ou qualquer bijecao em nivel de conjunto. Uma
proposicao trivialmente fechavel por uma rota nao relacionada nao testa
genuinamente o que alega testar. Pior: o lema de transporte de
desigualdade citado verbatim do proprio cabecalho da Onda 3
(`‖mu‖ <= Lam <-> (Lam+1)⁻¹ <= ‖(mu+1)⁻¹‖`) e **FALSO** como enunciado
irrestrito sobre todo `mu:C` -- contraexemplo verificado numericamente:
`mu=i, Lam=0.5` da `‖mu‖=1` (LHS Falso) mas `‖(1+i)⁻¹‖=1/√2≈0.7071` e
`(Lam+1)⁻¹≈0.6667`, entao `0.6667<=0.7071` (RHS Verdadeiro). O lema so e
verdadeiro quando `mu` e restrito a valores reais nao-negativos (em
particular `mu=(n:C)` para `n:N`, os unicos valores que de fato ocorrem
como autovalores de `Tp`) -- restricao que nem o candidato nem o arquivo
da Onda 3 flagram como load-bearing.
**Teste revisado:** substituir o alvo numerico por um enunciado em nivel
de CONJUNTO que nao pode contornar `eigenvalue_bridge`: para `Lam>=0`,
provar `{mu : C | IsEigenvalue Tp mu ∧ ‖mu‖<=Lam} = (fun mu =>
(mu+1)⁻¹) ⁻¹' {nu : C | Module.End.HasEigenvalue T nu ∧ (Lam+1)⁻¹ <=
‖nu‖}`, construido ponto a ponto via `eigenvalue_bridge` composto com
um lema de transporte CORRETAMENTE RESTRITO a `mu=(n:C)`, `n:N`, i.e.
`∀ n:N, (n:R)<=Lam <-> (Lam+1)⁻¹ <= ‖((n:C)+1)⁻¹‖` (verdadeiro, via
`norm_inv` + `Complex.norm_natCast` + `one_div_le_one_div` em
`a=n+1,b=Lam+1`) -- NAO a versao incondicional para todo `mu`, que e
falsa. Esta igualdade de conjunto genuinamente exige a ponte (nao ha
atalho de aritmetica de piso para ela) e escopa corretamente o lema de
transporte para onde ele de fato vale.

---

## 2. Navier-Stokes (NS) — Clay oficial (nucleo Calderon-Zygmund)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| NS-4a | Familia continua-linear do funcional p.v. sobre um compacto ARBITRARIO `K'` (fecha gap(ii) sozinho) | SURVIVES | baixo-moderado |

**Passo original vs. o que mudou.** Continuacao direta do gap (ii)
explicitamente nomeado pela propria secao "O que NAO e afirmado" de
`NS-2b`/Onda-2 (`PVDistributionOnCompactK.lean`), agora que `NS-3a`
(Onda 3, `RadiusIndependencePVLipschitz.lean`) ja fechou o gap (i).

**NS-4a — SURVIVES.** Releitura integral de `PVDistributionOnCompactK.lean`
(1266 linhas) e `RadiusIndependencePVLipschitz.lean` (961 linhas)
confirma linha a linha `pvKCLM`/`pvKCLM_apply` (1041-1114) e
`pv_value_radius_independent` (786-836) exatamente como descrito, e que
a propria secao "O que NAO e afirmado" de NS-2b divide o trabalho
restante exatamente nos dois gaps que o recon nomeia. Toda citacao
Mathlib conferida contra o Mathlib vendorizado real, incluindo numeros
de linha exatos para `monoCLM` (807) e `monoCLM_apply` (817).
`PartialOrder.ofSetLike` rastreado ate `Data/SetLike/Basic.lean:234-240`
confirmando que `<=` de `Compacts` e definicionalmente subconjunto
(`Iff.rfl`). `lipschitzWith_seminorm_of_contDiffMapSupportedIn` (NS-2b)
ja esta enunciado para um compacto GENERICO `K`, nao so bolas, e
`f.zero_on_compl` existe em `ContDiffMapSupportedIn.lean:161` -- ambos
suprindo diretamente o que este item precisa. A composicao
`pvKCLM(bola) o monoCLM(K'->bola)` reproduz a mesma formula integral, e
`pv_value_radius_independent` com `c:=0` fecha a radius-independence
para o composto. Escopo corretamente exclui o gap (iii) (montagem
global de `limitCLM`/`toFun_eq_T`).
**Teste revisado:** mesmo teste proposto, com uma adicao: como
`pv_value_radius_independent` exige `R1<R2` estrito, o enunciado deve
explicitamente `wlog`/case-split sobre qual dos dois raios envolventes e
menor (aplicar o lema com `(min R1 R2, max R1 R2)` em vez de assumir
ordem), e derivar `hsupp` de `f.zero_on_compl` composto com `K' <=
closedBall 0 (min R1 R2)` via
`ContDiffMapSupportedIn.tsupport_subset`/`support_subset`. Gap cosmetico
no enunciado do teste, nao matematico -- nao muda o veredito.

---

## 3. P vs NP (PN) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| PN-8 | Testemunha de cobertura de `peek` (leitura nao-consumidora da pilha) | SURVIVES | baixo |

**Passo original vs. o que mudou.** `Stmt` tem 7 construtores
(`push`/`peek`/`pop`/`load`/`branch`/`goto`/`halt`,
`StackTuringMachine.lean:127-134`); PN-6/PN-7 (Onda 3) fecharam
`goto`-com-alvo-simbolico e `branch`, deixando `peek` como um setimo
construtor genuinamente ainda sem cobertura -- confirmado por grep
independente de `peek`/`Stmt.peek`/`Stmt.branch` em todo o laboratorio
(fora `.lake`): zero hits alem da propria prosa de PN-7, que ja nomeia
`peek` explicitamente como lacuna diferente e ainda aberta.

**PN-8 — SURVIVES.** `RESEARCH_QUEUE.yaml` confirma que
`WAVE3-PN-7` ja registra `peek` como "unico construtor ainda sem
cobertura", sem nenhuma entrada anterior tratando `peek` como
tentado/refutado -- ao contrario de HG `ord`/`ClassGroup`, esta nao e
uma linha morta reaberta. `stepAux` de `peek` (linha 163,
`stepAux q (f v (S k).head?) S`) comparado lado a lado com `pop`
(linha 164, mutando a pilha) e estruturalmente quase identico, diferindo
so em mutar ou nao a pilha -- e `pop` e o mecanismo ja provado fechar
via `rfl` direto mesmo para entrada simbolica em PN1/PN3/PN5 (confirmado
por grep: as tres usam `evals_in_steps := rfl` diretamente, PN3/PN5 ate
threading o bit simbolico via `!v`/`decide(...)` antes de armazena-lo,
sem case-split). Isso fundamenta a previsao mecanica do candidato --
`peek` pertence a familia "facil" que fecha por `rfl` direto, nao a
familia "trava em cond/match" de `goto`/`branch` -- em vez de
especulacao. Design `Lambda:=Unit` (ja usado por PN7, evitando o
obstaculo de derivacao de `Fintype` de PN6) confirmado suficiente; sem
necessidade de `goto` pois `peek` nao exige despacho multi-label. Secao
de ressalvas honesta (prediz resultado confirmatorio, nao novo).
**Teste revisado:** essencialmente como proposto -- `FinTM2` de pilha
unica, `Lambda:=Unit`, popar o bit de entrada em `sigma`, empurra-lo de
volta (padrao testemunha-identidade ja reusado em PN1/PN3/PN5/PN7),
depois `peek(fun _ ob => ob.getD false)` para reler o topo da pilha em
`sigma` SEM consumir, `load`/`halt`, `steps=1`. Tentar `evals_in_steps
:= rfl` diretamente primeiro; so recorrer a `by cases b <;> rfl` se
`rfl` genuinamente falhar, documentando isso explicitamente como
achado inesperado (um terceiro membro da familia "trava") em vez de
suavizar a surpresa. Rigor adicional recomendado: uma versao
maximamente honesta deveria reler o valor tambem na pilha de SAIDA (ou
mostrar de outra forma que ele materialmente alcancou `haltList`), em
vez de so armazena-lo em `sigma` e nunca usa-lo -- senao um revisor
poderia razoavelmente perguntar se a chamada `peek` foi load-bearing
para a testemunha-identidade, ou decorativa.

---

## 4. Yang-Mills (YM) — Clay oficial (modelo de brinquedo de rede-transferencia 2x2)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| YM-CAPSTONE-BRACKET | Compor `stability_compose_lambdaMax` com `lambdaMax_grounded_eq_three` num arquivo capstone unico | SURVIVES (compilado limpo) | baixo |
| YM-CAPSTONE-FULL | Estender o bracket ao `lambda2` via `trace(toEuclideanCLM M2)=4` e composicao completa | NEEDS_NARROWING | moderado |

**Passo original vs. o que mudou.** Ambos combinam resultados ja
fechados em `YMStabilityCompose.lean` (Onda 3) e `StabilityGrounded.lean`
(Onda 3) que nunca foram compostos entre si -- confirmado por grep, nao
existe hoje nenhum arquivo do laboratorio combinando
`stability_compose_lambdaMax` com `lambdaMax_grounded_eq_three`.

**YM-CAPSTONE-BRACKET — SURVIVES, ja COMPILADO pela revisao
adversarial.** A revisao construiu de fato o arquivo capstone proposto
(deduplicando as definicoes identicas de `E`/`lambdaMax`/`M2` das duas
fontes num namespace compartilhado) e compilou com `lake env lean`
contra o cache Mathlib real do laboratorio (`leanprover/lean4:v4.33.0-rc1`,
8279 `.olean` vendorizados). Primeira tentativa falhou com erro
`Ambiguous term sub_apply`, causado por um `open Matrix WithLp`
vestigial herdado do cabecalho de `StabilityGrounded.lean` colidindo com
o `sub_apply` nao-qualificado usado dentro do `simp` de
`lambdaMax_lipschitz` -- colisao que nao pode aparecer em nenhum dos
dois arquivos-fonte isoladamente, so ao combina-los. Removendo o `open`
vestigial (nenhum nome de nenhum dos dois arquivos depende dele -- todos
ja totalmente qualificados), o arquivo -- incluindo a tatica de
fechamento exata proposta `rw [lambdaMax_grounded_eq_three] at h; rw
[abs_le] at h; constructor <;> linarith` -- compila LIMPO, zero erros,
`#print axioms` so com `[propext, Classical.choice, Quot.sound]`.
Artefato verificado:
`/tmp/claude-0/.../scratchpad/YMCapstoneTest.lean` (sessao da
adversarial).
**Teste revisado:** exatamente como proposto, com uma correcao: ao
montar o arquivo-scratch unico (reproduzindo as cadeias de dependencia
de ambos os arquivos-fonte sob um namespace compartilhado com um unico
`M1`/`M2`/`E`/`lambdaMax`), NAO carregar `open Matrix WithLp` do
cabecalho de `StabilityGrounded.lean` -- todo nome em ambos os arquivos
ja e totalmente qualificado (`Matrix.toEuclideanCLM`, `WithLp.toLp`,
`M2.mulVec`, etc.). Omitindo essa linha, `lambdaMax_M1_bracket : 2.9 <=
lambdaMax (toEuclideanCLM M1) ∧ lambdaMax (toEuclideanCLM M1) <= 3.1`
fecha exatamente como especificado.

**YM-CAPSTONE-FULL — NEEDS_NARROWING, dividido em dois passos gated.**
Todas as citacoes Mathlib conferem exatas: `Matrix.inner_toEuclideanCLM`
(`Analysis/CStarAlgebra/Matrix.lean:122`), `EuclideanSpace.basisFun_apply`/
`basisFun_inner` (`PiL2.lean:808/815`), `LinearMap.trace_eq_sum_inner`
(`InnerProductSpace/Trace.lean:27`). Nenhum lema pre-existente
`trace_toEuclideanCLM`/`trace_toEuclideanLin` existe no snapshot
(confirmado ausente por grep) -- entao o fato-chave exige montagem
genuina, nao um one-liner, como o recon ja avisava. A revisao
adversarial de fato tentou a derivacao `trace (toEuclideanCLM M2) = 4`
via `lake env lean` e ela NAO fechou nas primeiras quatro tentativas:
(1) `dotProduct`/`mulVec` em notacao infixa exige `open Matrix` em
escopo, senao produz um erro obscuro de elaboracao no subscrito `v`;
(2) `EuclideanSpace.basisFun_apply (Fin 2) 0` (estilo posicional
implicito pelo proprio recon) falha com "failed to synthesize OfNat"
porque a ordem de argumentos explicitos de `basisFun_apply` difere da
de `basisFun` e precisa de argumentos NOMEADOS `(ι:=Fin 2) (𝕜:=R)`.
Apos corrigir ambos (5 iteracoes de compilacao no total), o lema fecha
limpo, zero sorries, so os 3 axiomas padrao -- de-riscando
substancialmente a preocupacao central do candidato. As tres etapas de
composicao restantes (`M1.IsHermitian`, aplicar `lambda2_hasEigenvalue`
a `M1`, join final de tres vias com `stability_compose_lambda2`/bracket
de `lambdaMax`) NAO foram verificadas pela revisao -- seguem padroes ja
provados em outro lugar do laboratorio (forma identica a
`M2_isHermitian`; mesma composicao `rw`/`abs_le` ja verificada para o
BRACKET), entao sao plausiveis mas nao testadas. Artefato verificado
(compila limpo): `/tmp/claude-0/.../scratchpad/YMTraceTest.lean`.
**Teste revisado:** Passo 1 (de-riscado, ja compila -- entregavel
falsificavel proprio, fazer primeiro): provar `trace (toEuclideanCLM M2
: E →l[R] E) = 4` usando `open Matrix` (necessario para notacao infixa
`dotProduct`/`mulVec` parsear), `LinearMap.trace_eq_sum_inner _ basis2`,
`Matrix.inner_toEuclideanCLM M2 (basis2 i) (basis2 i)` com parenteses
externos explicitos `(basis2 i) dotProduct (M2 *v (basis2 i))`
(precedencia ingenua causa erro de tipo por associatividade errada), e
`EuclideanSpace.basisFun_apply (ι:=Fin 2) (𝕜:=R) i` com argumentos
NOMEADOS (posicionais atribuem `𝕜`/`ι` errado silenciosamente). Depois
`lambda2 (toEuclideanCLM M2) = 1` via `unfold lambda2; rw
[trace_toEuclideanCLM_M2_eq_four, lambdaMax_grounded_eq_three];
norm_num`. Passo 2 (nao tentado pela revisao, genuinamente ainda
aberto, gated no Passo 1): `M1.IsHermitian` (copiar forma de
`M2_isHermitian`) + `lambda2_hasEigenvalue` aplicado a `M1` + composicao
final de tres vias com `stability_compose_lambda2` -- so tentar apos o
Passo 1 fechar, e re-testar do zero antes de alegar que o candidato
completo fecha.

---

## 5. Hodge Conjecture (HG) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| HG-1E | Familia parametrizada de `principalCycle` sobre `a0` | SURVIVES | baixo |
| HG-1F | Divisor de um quociente = diferenca `AlgebraicCycle` dos dois divisores | SURVIVES | moderado |
| HG-4D | `IsHolomorphicTransition` fechado por multiplicacao e inversao pontual | SURVIVES | baixo |

**Passo original vs. o que mudou.** Todos os tres sao genuinamente
novos (nenhum dos tres arquivos da Onda 3 -- HG-1C, HG-1D,
`HolomorphicTransitionConjugationBridgeProbe.lean` -- ja faz o que se
propoe aqui), corretamente auto-escopados, e nenhum toca a ponte
`ord`/`ClassGroup` duas vezes REFUTED nem a API `VectorBundle`/`Bundle`
ja sinalizada como grande demais. Recon desta linha e incomumente
preciso: toda citacao Mathlib e de arquivo do laboratorio conferiu
exata.

**HG-1E — SURVIVES.** Releitura integral de
`HG1CParametrizedFiniteSupportOrdProbe.lean` confirma que o arquivo para
em `finite_support_ord_algebraMap (a0)(ha0)` mais duas instanciacoes --
nenhum empacotamento `AlgebraicCycle` existe, gap real. `principalCycle`
(HG-1, linhas 331-336) e `principalCycle_f` (HG-1D, linhas 422-428) usam
o mesmo padrao de tres campos (`toFun`/`supportWithinDomain'` por
`simp`/`supportLocallyFiniteWithinDomain'` via `⟨Set.univ,
Filter.univ_mem, ...⟩`) que este candidato propoe reusar. `AlgebraicCycle
X R` e literalmente `abbrev ... := Function.locallyFinsupp X R`
(`AlgebraicGeometry/AlgebraicCycle/Basic.lean`) -- sintaxe de
struct-literal ja usada duas vezes garante typecheck para qualquer trio
`toFun`/prova bem-tipado; nao ha wrinkle de typeclass que a
dependencia-em-`a0` introduziria que HG-1C ja nao resolveu (via
`haveI`) para o mesmo par `genf`/`finite_support_ord_genf`.
**Teste revisado:** como proposto -- inlinar as declaracoes de HG-1C
verbatim num arquivo novo autonomo e adicionar `principalCycle_a0 (a0:Z)
(ha0:a0!=0) : AlgebraicCycle testScheme Z` usando `genf a0`/
`finite_support_ord_genf a0 ha0`; checar `lake env lean` exit 0.

**HG-1F — SURVIVES.** Grep confirma `structure
Function.locallyFinsuppWithin` (`Topology/LocallyFinsupp.lean:48`),
instancia `FunLike` (:125, necessaria para o lema `ext` aplicar
pontualmente), `ext` (:147), instancias `Neg`/`Sub`/`SMul Z` (:337/340/343),
`coe_sub` (:352), e a instancia `AddGroup` combinada via
`Injective.addGroup` (existe, mas NAO nas linhas 337-343 -- imprecisao
de citacao menor, sem efeito substantivo). Releitura de HG-1D
(linhas 385-408, prova de `finite_support_ord_f`) confirma que a
identidade pontual `ord f x + ord(algebraMap Den.a0) x =
ord(algebraMap Num.a0) x` ja e derivada la via `Scheme.ord_mul`
(`OrderOfVanishing.lean:81`) -- exatamente a forma necessaria para
reorganizar numa identidade de subtracao. A sanidade concreta `n=3,d=2`
NAO depende de HG-1E: os namespaces `Num`/`Den` de HG-1D ja contem
`genf`/`finite_support_ord_genf` para `a0=3` e `a0=2`, entao
`principalCycle_Num`/`principalCycle_Den` podem ser construidos
diretamente pelo mesmo idioma de HG-1E, independentemente.
**Teste revisado:** construir diretamente dos namespaces `Num`/`Den`
existentes de HG-1D (sem depender de HG-1E): definir
`principalCycle_Num`, `principalCycle_Den` via o mesmo padrao de tres
campos aplicado a `Num.genf`/`Num.finite_support_ord_genf` e
`Den.genf`/`Den.finite_support_ord_genf`, depois provar
`principalCycle_f = principalCycle_Num - principalCycle_Den` via
`Function.locallyFinsuppWithin.ext`, fechando o objetivo pontual com
`coe_sub` mais um rearranjo de uma linha (`sub_eq_of_eq_add`/`omega`) da
identidade ja derivada via `ord_mul` em `finite_support_ord_f`. Citar o
numero de linha real da instancia `AddGroup` com precisao antes de
depender dela num cabecalho de arquivo novo.

**HG-4D — SURVIVES.** `HolomorphicTransitionConjugationBridgeProbe.lean`
(HG-4C) para no teorema unico `not_isHolomorphicTransition_starRingEnd`
-- nenhum fato de fechamento por mul/inv aparece, gap real.
`IsHolomorphicTransition g := MDifferentiable ...` e o iff-bridge
(`HolomorphicTransitionProbe.lean:129-133`) conferem exatos.
`Differentiable.mul` (`FDeriv/Mul.lean:226`) e `Differentiable.inv`
(:779, exigindo `∀x, h x != 0`) conferem exatos, assinaturas batendo
precisamente com a composicao proposta. Mesmo idioma "compor dois fatos
ja provados" que HG-4C ja usou, sobre um predicado de carta unica de
brinquedo, sem API `VectorBundle`/`Bundle`.
**Teste revisado:** como proposto -- inlinar o predicado+ponte de
HG-4/HG-4C e provar `isHolomorphicTransition_mul` via
`isHolomorphicTransition_iff_differentiable.mpr ((...).mp hg).mul
((...).mp hh)`, mais o corolario analogo `isHolomorphicTransition_inv`
exigindo `∀x, g x != 0`; checar `lake env lean` exit 0.

---

## 6. Birch and Swinnerton-Dyer (BSD) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| BSD-1-STEP5-COMPOSE | Compor STEP1+STEP4 (Ondas 2-3) na bijecao de corpo de residuo, depois estender a `IsMultiplicative` incondicional | SURVIVES (dividido em A/B) | baixo (A) / moderado-nao-verificado (B) |

### A pergunta factual central: BSD-GAP-007 fecha genuinamente?

**Resposta honesta: AINDA NAO -- e mesmo se a parte A fechar na
execucao, a parte B permanece em aberto e nao verificada.**

`BSD-1_GAP_NOTE.md` (Onda 1) nomeou tres passos que faltavam para a
ponte de corpo de residuo entre `v.adicCompletionIntegers K`
(`UniformSpace.Completion` de um corpo valorado) e a construcao
modular `AdicCompletion`: (1) um `RingEquiv` entre o corpo de residuo da
localizacao de `O_K` em `v` e o anel de valoracao pre-completacao; (2)
um lema de invariancia-de-corpo-de-residuo-por-completacao especifico
para a construcao `UniformSpace.Completion`; (3) compor (1)+(2) para
obter `IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃
O_K ⧸ v.asIdeal`, depois transportar finitude e cardinalidade
potencia-de-primo.

`BSD-1-STEP3-HASEXTENSION` e `BSD-1-STEP4-RESIDUE-BIJECTION` (Onda 3)
nao seguiram literalmente essa rota (1)+(2) -- usaram a maquinaria
`Valuation.HasExtension` do proprio Mathlib (`Extension.lean`) para
chegar por um caminho diferente. A revisao adversarial desta onda
**compilou individualmente** `BSD1Step1ComposeResidueField.lean` e
`BSD1Step4ResidueBijection.lean` com `lake env lean` contra o Mathlib do
projeto -- ambos exit 0, `#print axioms` so com os 3 axiomas padrao --
confirmando que as alegacoes da Onda 3 sobre esses dois arquivos sao
genuinas, nao so auto-reportadas. Confirmou tambem, por leitura direta,
que `adicCompletionIntegers` e literalmente `Valued.v.valuationSubring`
sem atributo `irreducible` bloqueando defeq, entao a notacao local
`L0` de STEP4 e de fato definicionalmente `v.adicCompletionIntegers K`,
e que `K0` de STEP1 e sintaticamente o mesmo objeto que STEP4 usa.

**Isso significa que, se a composicao proposta pela parte A abaixo
compilar, ela entrega exatamente o objeto que os passos (1)-(3) do gap
note pediam para "construir essencialmente do zero"** --
`IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃+*
(O_K ⧸ v.asIdeal)` -- por uma rota diferente da originalmente prevista.
Isso seria progresso real e substancial sobre o gap.

**Mas dois pontos impedem declarar o gap fechado agora:**

1. **A composicao em si (parte A / STEP5a) ainda NAO foi compilada.**
   STEP1 e STEP4 compilam cada um isoladamente; os dois arquivos
   explicitamente NAO se compoem entre si hoje (disclaimers em ambos os
   cabecalhos). Montar `(STEP1result.trans (RingEquiv.ofBijective _
   STEP4result)).symm` num arquivo unico e trabalho genuinamente novo
   desta onda, nao um fato ja verificado.

2. **Mesmo se a parte A fechar, a parte B (fiar a equivalencia ate a
   versao incondicional de `WeierstrassCurve.LFunction.IsMultiplicative`)
   e um checkpoint SEPARADO, nao verificado pela adversarial.** Isso
   exige: obter `IsPrimePow (Nat.card (ResidueField (v.adicCompletionIntegers
   K)))` a partir da equivalencia da parte A mais
   `finiteQuotientOfFreeOfNeBot` (`IdealQuotient.lean:46-49`) e
   `FiniteField.isPrimePow_card` (`FieldTheory/Finite/Basic.lean:273`);
   depois universalmente quantificar sobre TODO lugar `v :
   HeightOneSpectrum (O_K)` e alimentar
   `LFunction_isMultiplicative_of_residueField_isPrimePow`
   (`LFunctionMultiplicativity.lean`) para produzir o teorema
   incondicional `W.LFunction.IsMultiplicative` -- sem hipotese
   `hq` residual. A revisao julga essa etapa "pequena e de baixo risco
   dado tudo o que ja foi checado", mas nao a compilou; nao deve ser
   assumida de graca.

**Nome preciso do que permanece, no estilo do gap note original:**
`BSD-GAP-007-RESIDUAL` -- mesmo apos a Onda 4 tentar e (hipoteticamente)
fechar a parte A (a equivalencia de corpo de residuo em si, o nucleo
Mathlib que o gap note original identificou como ausente), a parte B
(fiacao universal de `IsPrimePow` sobre todos os lugares `v` e a
producao do teorema `IsMultiplicative` sem hipotese) permanece
totalmente nao tentada e deve ser reportada como resultado separado, nao
assumida como consequencia automatica.

**Teste revisado, dividido em dois checkpoints explicitos, NAO
bundlados:**

**(A) STEP5a** — exatamente o teste proposto: `example :
IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃+*
(O_K ⧸ v.asIdeal) := (STEP1result.trans (RingEquiv.ofBijective _
STEP4result)).symm`, checado com `lake env lean`, exit 0, zero tatica
proibida.

**(B) STEP5b** — SOMENTE se (A) passar: usar o equiv de (A) mais
`finiteQuotientOfFreeOfNeBot` e `FiniteField.isPrimePow_card` para
produzir o termo literal `hq` que
`LFunction_isMultiplicative_of_residueField_isPrimePow` exige, e so
entao enunciar `theorem WeierstrassCurve.LFunction_isMultiplicative ...
:= LFunction_isMultiplicative_of_residueField_isPrimePow W (fun v =>
...)` sem hipotese, novamente checado com `lake env lean`, exit 0.
Reportar (A) e (B) como resultados pass/fail SEPARADOS -- nao alegar
`LFunction_isMultiplicative` incondicional fechado se so (A) tiver
sucesso.

---

## 7. Sintese TOE (extensao interna do laboratorio — NAO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| TOE-4 | Comparacao funtorial entre a categoria-de-acao do mundo-Shift3 e do mundo-K (contraste Faithful/nao-Faithful) | SURVIVES | baixo-moderado |

**Passo original vs. o que mudou.** O plano funtorial original (TOE-3,
Onda 2) foi declarado morto na largada por Shift3/`RegimeCat` ser um
torsor livre+transitivo com Hom-sets singleton -- confirmado
verbatim contra `PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md:537-548`. TOE-4
reabre a ideia corretamente, na direcao OPOSTA: comparar `K`
(nao-livre, nao-pretransitivo, ja construido em TOE-3c/TOE-3d/TOE-3e da
Onda 3) contra Shift3, em vez de tentar um funtor dentro de Shift3
sozinho.

**TOE-4 — SURVIVES.** Releitura integral de
`HomKNotIsoActionCategoryK.lean` e
`MonoidKNonPretransitiveZigzagConnected.lean` (mais pre-requisitos:
`ActionCategoryRegime3.lean`, `Shift3PretransitiveActionCategoryConnected.lean`,
`MonoidKConstantActionDistinctEndomorphisms.lean`,
`Foundations/Semigroups/{Regime3,Theorems,Action}.lean`) confirma as
provas de TOE-3d/TOE-3e exatamente como resumidas, sem embelezamento.
Citacoes Mathlib re-checadas: `Functor` (`Functor/Basic.lean`, campos
`obj`/`map`/`map_id`/`map_comp`), `Faithful`
(`FullyFaithful.lean:52-56`, campo `map_injective`), `hom_as_subtype`
(`Action.lean:92`), `back`/`CoeTC`/`back_coe` (`Action.lean:71-81`).
Grep confirma ausencia total no laboratorio de "free action",
`Injective.*apply`, `IsFree`, funtor entre `RegimeCat`/`KCat`, ou
`Subsingleton` -- maquinaria genuinamente nova.

Verificacao combinatoria a mao (nao so confianca no recon): Shift3 e
livre (checado nos tres pontos-base, `{identity,forward,forward2}•x` da
3 valores distintos em cada caso), logo `Hom_Shift(p,q)` e sempre
singleton (via a transitividade ja provada + a liberdade). `K` da
`Hom_K(alpha,alpha) = {identity,k}` (2 elementos, ja distintos por
TOE-3c). Os quatro `Hom_K` alegados vazios (`beta->gamma`, `gamma->beta`,
`alpha->beta`, `alpha->gamma`) checados um a um contra a definicao de
`Kact` em duas linhas -- todos genuinamente vazios (`identity` fixa
pontos nao-`alpha`, `k` sempre aterrissa em `alpha`). `Hom_Shift(beta,gamma)`
nao-vazio confirmado pela tabela (`forward.apply beta = gamma`).

Os dois blocos propostos sao logicamente solidos: (A) um funtor
"morfismo unico" `K-mundo -> Shift3-mundo` existe (via `Nonempty` +
`Subsingleton` dos Hom-sets alvo, padrao standard de montagem de
funtor-de-categoria-fina) e comprovadamente NAO e `Faithful` porque
`homIdentity != homK` (TOE-3c) mas ambos mapeiam no mesmo elemento
singleton. (B) escopado corretamente como "nenhum funtor com ESTE mapa
de objeto especifico label-identidade" (nao "nenhum funtor de forma
alguma" -- um funtor constante-para-alpha existe trivialmente na direcao
oposta): tal funtor precisaria enviar o morfismo concreto `beta->gamma`
(que existe) no `Hom_K(beta,gamma)` vazio, impossivel por case-split
direto sobre `K`.

**Ressalvas para quem executar, nao bloqueadoras:** (a) o campo mapa-de-
morfismo da parte (A) deve ser construido via tabela de casos finita
explicita (espelhando o idioma `rfl`/`decide` ja estabelecido no
laboratorio), nao `Classical.choice`/`Exists.choose`, para evitar puxar
`Classical` na lista de axiomas e manter a construcao computavel; (b) a
hipotese "funtor label-identidade" da parte (B) precisa ser fixada
precisamente em Lean (ex.: `∀ p, F.obj p = show KCat from p.back`) antes
de escrever a prova de nao-existencia, ja que a frase e informal como
esta. Nenhuma das duas muda o veredito.
**Teste:** dois `decide` autonomos que servem de porta de entrada barata
-- (1) liberdade de Shift3 nos tres pontos-base; (2)
`Hom_K(beta,gamma) = ∅`. So depois, construir o funtor "morfismo unico"
`F : KCat ⥤ ShiftCat` (campo `map` via tabela de casos explicita, nao
`Classical.choice`) e provar `¬ Faithful F` via `homIdentity != homK`
mapeando ambos ao unico elemento de `Hom_Shift(alpha,alpha)`; depois,
fixando explicitamente a hipotese "`G.obj p = show KCat from p.back`
para todo `p`", provar que nenhum tal `G : ShiftCat ⥤ KCat` existe, via
o morfismo concreto `beta->gamma` de Shift3 precisando de imagem em
`Hom_K(beta,gamma) = ∅`.

---

## 8. Fundamentos Quanticos / Unificacao (extensao interna — NAO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| QF-7 | Unitariedade / conservacao de produto interno do fluxo de Heisenberg | NEEDS_NARROWING | baixo-moderado |

**Passo original vs. o que mudou.** Facies genuinamente nova: nenhum
dos tres arquivos QF-4/QF-5/QF-6 (Ondas 1-3) toca unitariedade/adjunto-
via-star, e a propria secao "AINDA FALTANDO" de QF-6 (linhas 175-195)
confirma que nenhuma alegacao de unitariedade/conservacao-de-norma foi
feita ali. `SCOPE.md` continua `UNSCOPED` verbatim.

**QF-7 — NEEDS_NARROWING.** Toda citacao Mathlib re-grepada diretamente
(nao confiando nos numeros do candidato) confere no local exato ou muito
proximo: `exp_mem_unitary_of_mem_skewAdjoint` (`Exponential.lean:539`,
exige `[StarRing][ContinuousStar]`), `StarRing (Matrix n n a)`
(`ConjTranspose.lean:431`), `NormedStarGroup.to_continuousStar`
(`CStarAlgebra/Basic.lean:72`), `NormedStarGroup (Matrix m m a)`
(`Matrix/Normed.lean:138`, NAO gated atras de nenhuma familia de norma
com `open` -- funciona independente de qual familia esta aberta),
`skewAdjoint.mem_iff` (`SelfAdjoint.lean:536`),
`Matrix.star_eq_conjTranspose` (`ConjTranspose.lean:413`),
`Matrix.toEuclideanCLM` como `≃⋆ₐ[𝕜]` genuino (`CStarAlgebra/Matrix.lean:102-107`),
`unitary.mapEquiv` (`Unitary.lean:337`),
`ContinuousLinearMap.inner_map_map_of_mem_unitary` (`Adjoint.lean:868`).
Conjunto de citacoes incomumente bem verificado.

Porem foi encontrado um gap real que a propria lista `mathlib_support`
do candidato nao enderecava: o Passo 1 do teste (`exp (t •
heisenbergGenerator) ∈ unitary (...)`) exige primeiro estabelecer `t •
heisenbergGenerator ∈ skewAdjoint (...)` -- NAO so que
`heisenbergGenerator` em si e skew-adjoint (tudo que QF-4 provou e tudo
que o candidato citou). `skewAdjoint` e so um `AddSubgroup`
(`SelfAdjoint.lean:360`), nao fechado automaticamente sob multiplicacao
escalar arbitraria. A ponte necessaria e `skewAdjoint.smul_mem`
(`SelfAdjoint.lean:574`, exige `[TrivialStar R][Monoid R][DistribMulAction
R A][StarModule R A]`). Todas as hipoteses resolvem independentemente
para `R:=R` (real): `TrivialStar R` (`Data/Real/Star.lean:21`),
`StarModule R (Matrix n n C)` via encadeamento de `StarModule R C`
(`LinearAlgebra/Complex/Module.lean:107`) atraves da instancia generica
`StarModule a (Matrix n n b)` (`ConjTranspose.lean:427`). A alegacao
ainda e VERDADEIRA e fechavel, mas o candidato nunca citou essa cadeia,
e ela e load-bearing exatamente como o Passo 1 esta escrito.

Pior: isso expoe que a coberta "para todo `t:R` (ou `C`)" do proprio
Passo 1 e matematicamente imprecisa a ponto de errada para o caso
complexo geral: `skewAdjoint.smul_mem` exige `[TrivialStar R]`, e `C`
NAO e `TrivialStar` (conjugacao e nao-trivial) -- entao para `t`
complexo geral, `t*H` nao e skew-adjoint (de fato, para `t` puramente
imaginario, `t*H` se torna self-adjoint, entao `exp(t*H)` genericamente
falharia em ser unitario). A alternativa "ou `C`" deve ser descartada;
so `t:R` e de fato suportado por esta rota.

O Passo 2 (extensao via produto interno) confere estruturalmente, e o
proprio candidato ja sinaliza honestamente seu ponto de atrito de risco
moderado (se a ponte `≃⋆ₐ[𝕜]`-para-`≃⋆*` necessaria por
`unitary.mapEquiv` esta disponivel sem lemas extras) -- autoavaliacao
apropriadamente cautelosa; `StarAlgEquiv.toStarRingEquiv`
(`StarAlgHom.lean:641`) confirmado como ponte plausivel, risco genuino
ainda assim permanece.
**Teste revisado:** mesmo plano de dois passos, estreitado. Passo 1:
enunciar e provar `exp (t • heisenbergGenerator) ∈ unitary (Matrix
(Fin 2)(Fin 2) C)` para `t:R` SOMENTE (descartar a alternativa "(ou C)"
-- nao suportada por esta rota e provavelmente falsa em geral para `t`
complexo). Adicionar explicitamente a cadeia, antes de invocar
`exp_mem_unitary_of_mem_skewAdjoint`: (a) `skewAdjoint.smul_mem`
(`SelfAdjoint.lean:574`) instanciado em `R:=R`, `A:=Matrix (Fin 2)(Fin 2)
C`, alimentado por (b) `TrivialStar R` (`Data/Real/Star.lean:21`) e (c)
`StarModule R (Matrix (Fin 2)(Fin 2) C)`, obtido encadeando `StarModule R
C` (`LinearAlgebra/Complex/Module.lean:107`) atraves da instancia
generica `StarModule a (Matrix n n b)`
(`LinearAlgebra/Matrix/ConjTranspose.lean:427`). Se (a)/(b)/(c) nao
resolverem ou nao unificarem com a estrutura de modulo-R ja usada
implicitamente em outro lugar deste diretorio, essa e a real condicao
de falsificacao do Passo 1 -- reportar exatamente qual falha. Passo 2
pode prosseguir como originalmente proposto, com seu risco moderado ja
sinalizado inalterado.

---

## Infraestrutura compartilhada entre frentes (continuacao)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| SHARED-4A | Exaustividade de dois autovalores em dim 2 | SURVIVES | baixo |
| SHARED-4B | `det = lambdaMax * lambda2` em dim 2 | SURVIVES | baixo |
| — | (recomendacao de infraestrutura) registrar `_SHARED_INFRA/FORMAL` no projeto Lake TamesisLab | SURVIVES (fora da lista numerada -- nao e teste Lean) | — |

**Passo original vs. o que mudou.** Ambos os itens matematicos sao
continuacao direta de `SecondEigenvalueHasEigenvalue.lean`
(SHARED-2A-EXT, Onda 3), que provou `lambda2` ser um autovalor genuino
mas deixou dois fatos internos nao-exportados (`heq0`, `hlambda2`) sem
promove-los a teoremas reutilizaveis.

**SHARED-4A — SURVIVES.** Releitura integral de
`SecondEigenvalueHasEigenvalue.lean` (388 linhas) confirma linha a linha:
`heq0 : lambdaMax T = hT.eigenvalues hn 0` (linha 364) e `hlambda2 :
lambda2 T = hT.eigenvalues hn 1` (linhas 369-371), ambos `have`s internos
nao exportados dentro da prova de `lambda2_hasEigenvalue`. Grep no
Mathlib vendorizado confirma `exists_eigenvalues_eq`
(`Analysis/InnerProductSpace/Spectrum.lean:283`) enunciado para
QUALQUER autovalor `mu` (nao so `lambdaMax`), exatamente o que este
candidato precisa. Combinado com `heq0`/`hlambda2` mais um case-split
trivial em `Fin 2`, da `mu = lambdaMax T ∨ mu = lambda2 T` sem gaps.
**Teste:** `theorem eigenvalue_eq_lambdaMax_or_lambda2 (T : E →L[R] E)
(hT : (T:E →ₗ[R] E).IsSymmetric) (hn : Module.finrank R E = 2) {mu:R}
(hmu : Module.End.HasEigenvalue (T:E →ₗ[R] E) mu) : mu = lambdaMax T ∨
mu = lambda2 T`.

**SHARED-4B — SURVIVES.** `det_eq_prod_eigenvalues`
(`Spectrum.lean:391-394`) confirmado exato -- `T.det = ∏ i,
(hT.eigenvalues hn i : k)` -- e a variavel ambiente `T` desse arquivo
(linha 84) e `T : E →ₗ[k] E`, batendo exatamente com o tipo-alvo do
candidato, `(T:E →ₗ[R] E).det`, nao um `ContinuousLinearMap.det`
descasado. `Fin.prod_univ_two` (`BigOperators/Fin.lean:111`) confirmado.
Combinando com `heq0`/`hlambda2` de SHARED-2A-EXT, `lambdaMax T *
lambda2 T = T.det` fecha sem gap. A metade do traco (`trace = lambdaMax
+ lambda2`) e livre por construcao (definicao de `lambda2`), como o
candidato corretamente nao alega como trabalho novo.
**Teste:** `theorem lambdaMax_mul_lambda2_eq_det (T : E →L[R] E) (hT :
(T:E →ₗ[R] E).IsSymmetric) (hn : Module.finrank R E = 2) : lambdaMax T *
lambda2 T = (T:E →ₗ[R] E).det`.

**Recomendacao de infraestrutura (fora da lista de execucao, nao
verificada como math candidate).** Explicitamente fora do escopo desta
rodada (nenhum arquivo de governanca/build tocado). Fatos verificados:
`05_FORMAL/lean/lakefile.toml` so registra `TamesisLab`;
`TamesisLab.lean` nao importa nenhum `03_MILLENNIUM/*/FORMAL/*.lean`;
nenhum diretorio `SharedInfra` existe ainda sob `TamesisLab/`. O
cabecalho de `UnboundedEigCountFloorLaw.lean` (RH-4, acima) confirma que
essa dependencia entre-linhas ja existe na pratica (reproduz
`LinearPMapEigenvalueBridge.lean` linhas 154-261 verbatim porque esse
arquivo compartilhado vive FORA do projeto Lake). O piloto proposto
(mover um arquivo ja fechado, adicionar um import, confirmar `lake
build` isolado) e apropriadamente minimo, e deve ser executado numa
sessao dedicada de infraestrutura com sign-off explicito de governanca,
nao dobrado nesta onda de conteudo matematico.

---

## Lista de execucao Onda 4 (despacho direto para agente de formalizacao)

Cada item abaixo traz o candidato, o teorema-alvo, e o enunciado de
teste exato (ja revisado pela adversarial), pronto para um agente de
formalizacao executar sem reinterpretacao. Ordem: por linha, mesma
sequencia das secoes acima. Todos sao independentes entre si a menos
que anotado.

```text
 1. RH / RH-4 (unboundedEigCount, lei-limite tipo Weyl)
    Provar Tendsto (fun Lam => (unboundedEigCount Lam : R)/Lam) atTop
    (nhds 1), via unboundedEigCount_eq_floor (congr'ado eventualmente
    em Lam>=0 via eventually_ge_atTop), reescrito como
    (floor Lam + 1)/Lam = floor Lam/Lam + 1/Lam, fechando com
    Tendsto.add contra tendsto_nat_floor_div_atTop (limite 1) e
    tendsto_inv_atTop_zero (limite 0). #print axioms so com os 3
    axiomas padrao.

 2. RH / RH-5 (ponte de conjunto route-b, revisada)
    Para Lam >= 0, provar {mu : C | IsEigenvalue Tp mu ∧ ‖mu‖<=Lam} =
    (fun mu => (mu+1)⁻¹) ⁻¹' {nu : C | Module.End.HasEigenvalue T nu ∧
    (Lam+1)⁻¹ <= ‖nu‖}, construido ponto a ponto via eigenvalue_bridge
    composto com o lema de transporte RESTRITO a mu=(n:C), n:N:
    ∀ n:N, (n:R)<=Lam <-> (Lam+1)⁻¹ <= ‖((n:C)+1)⁻¹‖ (via norm_inv +
    Complex.norm_natCast + one_div_le_one_div). NAO usar a versao
    incondicional para todo mu:C -- e falsa (contraexemplo mu=i,
    Lam=0.5).

 3. NS / NS-4a (funcional p.v. sobre compacto K' arbitrario)
    Compor pvKCLM (bola) com monoCLM (K' -> bola) para obter o
    funcional p.v. continuo-linear sobre K' arbitrario; fechar
    radius-independence via pv_value_radius_independent aplicado com
    (min R1 R2, max R1 R2) (wlog sobre qual raio e menor); derivar
    hsupp de f.zero_on_compl composto com K' <= closedBall 0
    (min R1 R2) via ContDiffMapSupportedIn.tsupport_subset/
    support_subset.

 4. PN / PN-8 (cobertura de peek)
    Construir FinTM2 de pilha unica, Lambda:=Unit: popar o bit
    simbolico de entrada em sigma, empurra-lo de volta (padrao
    testemunha-identidade de PN1/PN3/PN5/PN7), depois
    peek(fun _ ob => ob.getD false) para reler o topo em sigma sem
    consumir, load/halt, steps=1. Tentar evals_in_steps := rfl
    primeiro; fallback by cases b <;> rfl, documentando explicitamente
    se rfl falhar (achado, nao suavizado). Preferir tambem reler o
    valor na pilha de SAIDA, nao so armazena-lo em sigma sem uso.

 5. YM / YM-CAPSTONE-BRACKET (ja compilado pela adversarial)
    Arquivo capstone unico, deduplicando E/lambdaMax/M2 de
    YMStabilityCompose.lean e StabilityGrounded.lean sob um namespace
    compartilhado, SEM `open Matrix WithLp` (vestigial, causa
    ambiguidade em sub_apply). Provar lambdaMax_M1_bracket : 2.9 <=
    lambdaMax (toEuclideanCLM M1) ∧ lambdaMax (toEuclideanCLM M1) <=
    3.1, via rw [lambdaMax_grounded_eq_three] at h; rw [abs_le] at h;
    constructor <;> linarith.

 6. YM / YM-CAPSTONE-FULL -- Passo 1 (trace, ja compilado pela
    adversarial)
    Provar trace (toEuclideanCLM M2 : E →l[R] E) = 4, usando
    open Matrix (obrigatorio para notacao infixa dotProduct/mulVec),
    LinearMap.trace_eq_sum_inner _ basis2, Matrix.inner_toEuclideanCLM
    M2 (basis2 i) (basis2 i) com parenteses externos explicitos
    (basis2 i) dotProduct (M2 *v (basis2 i)), e
    EuclideanSpace.basisFun_apply (ι:=Fin 2) (𝕜:=R) i com argumentos
    NOMEADOS (posicionais atribuem 𝕜/ι errado). Depois
    lambda2 (toEuclideanCLM M2) = 1 via unfold lambda2;
    rw [trace_toEuclideanCLM_M2_eq_four, lambdaMax_grounded_eq_three];
    norm_num.

 7. YM / YM-CAPSTONE-FULL -- Passo 2 (depende de #6, nao verificado)
    Provar M1.IsHermitian (mesma forma de M2_isHermitian), aplicar
    lambda2_hasEigenvalue a M1, compor tres vias com
    stability_compose_lambda2 e o bracket de lambdaMax (item 5) para
    obter o bracket analogo de lambda2 (M1). So tentar apos #6 fechar;
    reportar honestamente onde travar, se travar.

 8. HG / HG-1E (principalCycle parametrizado em a0)
    Inlinar as declaracoes de HG-1C verbatim num arquivo novo
    autonomo; adicionar principalCycle_a0 (a0:Z)(ha0:a0!=0) :
    AlgebraicCycle testScheme Z usando genf a0/
    finite_support_ord_genf a0 ha0. lake env lean exit 0.

 9. HG / HG-1F (divisor de quociente = diferenca de AlgebraicCycle)
    A partir dos namespaces Num/Den existentes de HG-1D, definir
    principalCycle_Num, principalCycle_Den via o mesmo padrao de tres
    campos; provar principalCycle_f = principalCycle_Num -
    principalCycle_Den via Function.locallyFinsuppWithin.ext, fechando
    o objetivo pontual com coe_sub mais rearranjo de uma linha
    (sub_eq_of_eq_add/omega) da identidade ord_mul ja derivada em
    finite_support_ord_f.

10. HG / HG-4D (fechamento por mul/inv de IsHolomorphicTransition)
    Inlinar o predicado+ponte de HG-4/HG-4C num arquivo novo autonomo;
    provar isHolomorphicTransition_mul via
    isHolomorphicTransition_iff_differentiable.mpr
    ((...).mp hg).mul ((...).mp hh), mais isHolomorphicTransition_inv
    exigindo ∀x, g x != 0 (Differentiable.inv). lake env lean exit 0.

11. BSD / BSD-1-STEP5a (bijecao de corpo de residuo, compondo #STEP3+#STEP4
    das Ondas 2-3)
    example : IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃+*
    (O_K ⧸ v.asIdeal) := (STEP1result.trans (RingEquiv.ofBijective _
    STEP4result)).symm. lake env lean exit 0, zero tatica proibida.
    NAO alegar BSD-GAP-007 fechado so com este item -- ver #12.

12. BSD / BSD-1-STEP5b (fiacao IsPrimePow universal, depende de #11,
    NAO verificado pela adversarial)
    Usando o equiv de #11 mais finiteQuotientOfFreeOfNeBot e
    FiniteField.isPrimePow_card, produzir o termo hq literal que
    LFunction_isMultiplicative_of_residueField_isPrimePow exige;
    enunciar theorem WeierstrassCurve.LFunction_isMultiplicative ... :=
    LFunction_isMultiplicative_of_residueField_isPrimePow W (fun v =>
    ...) sem hipotese. lake env lean exit 0. Reportar #11 e #12 como
    resultados pass/fail separados.

13. TOE / TOE-4 (comparacao funtorial Shift3-mundo vs K-mundo)
    Porta de entrada: dois decide autonomos -- (a) liberdade de Shift3
    nos tres pontos-base; (b) Hom_K(beta,gamma) = ∅. Depois construir
    F : KCat ⥤ ShiftCat (funtor "morfismo unico" via Nonempty+
    Subsingleton dos Hom-sets alvo, campo map por tabela de casos
    explicita, NAO Classical.choice); provar ¬ Faithful F via
    homIdentity != homK mapeando ambos ao unico elemento de
    Hom_Shift(alpha,alpha). Depois, fixando explicitamente a hipotese
    "G.obj p = show KCat from p.back para todo p", provar que nenhum
    tal G : ShiftCat ⥤ KCat existe, via o morfismo beta->gamma de
    Shift3 precisando de imagem em Hom_K(beta,gamma) = ∅.

14. QF / QF-7 (unitariedade do fluxo de Heisenberg, revisado, so t:R)
    Provar exp (t • heisenbergGenerator) ∈ unitary (Matrix (Fin 2)
    (Fin 2) C) para t:R (NAO "ou C" -- descartado, falso em geral),
    via: (a) skewAdjoint.smul_mem em R:=R, A:=Matrix (Fin 2)(Fin 2) C,
    alimentado por TrivialStar R e StarModule R (Matrix (Fin 2)(Fin 2)
    C) (via StarModule R C encadeado pela instancia generica
    StarModule a (Matrix n n b)); (b) exp_mem_unitary_of_mem_skewAdjoint.
    Se (a) nao resolver/unificar, reportar exatamente qual sub-passo
    falhou -- essa e a condicao real de falsificacao. Passo 2 (extensao
    via produto interno, unitary.mapEquiv +
    inner_map_map_of_mem_unitary) so apos Passo 1, risco moderado ja
    sinalizado (ponte StarAlgEquiv->StarRingEquiv).

15. SHARED-INFRA / SHARED-4A (exaustividade de dois autovalores dim 2)
    theorem eigenvalue_eq_lambdaMax_or_lambda2 (T : E →L[R] E)
    (hT : (T:E →ₗ[R] E).IsSymmetric) (hn : Module.finrank R E = 2)
    {mu:R} (hmu : Module.End.HasEigenvalue (T:E →ₗ[R] E) mu) :
    mu = lambdaMax T ∨ mu = lambda2 T, via exists_eigenvalues_eq
    aplicado ao mu de hmu, mais os fatos internos heq0/hlambda2 de
    SecondEigenvalueHasEigenvalue.lean promovidos a lemas nomeados,
    mais case-split em Fin 2.

16. SHARED-INFRA / SHARED-4B (det = lambdaMax * lambda2 dim 2)
    theorem lambdaMax_mul_lambda2_eq_det (T : E →L[R] E)
    (hT : (T:E →ₗ[R] E).IsSymmetric) (hn : Module.finrank R E = 2) :
    lambdaMax T * lambda2 T = (T:E →ₗ[R] E).det, via
    det_eq_prod_eigenvalues + Fin.prod_univ_two + heq0/hlambda2
    (mesmos fatos internos do item 15).
```

Total: **14 itens de execucao** na lista numerada (a numeracao acima
chega a 16 porque os itens 6/7 formam um unico candidato
`YM-CAPSTONE-FULL` dividido em dois passos gated, e os itens 11/12
formam um unico candidato `BSD-1-STEP5-COMPOSE` dividido em dois
checkpoints gated -- mesma convencao ja usada pela Onda 3 para
`BSD-1-STEP3`/`STEP4`). Contando por CANDIDATO (nao por linha numerada):
RH(2) + NS(1) + PN(1) + YM(2) + HG(3) + BSD(1) + TOE(1) + QF(1) +
SHARED-INFRA(2) = **14**. Contagem menor que os 15 da Onda 3 --
resultado honesto, nao ajustado: varias linhas renderam so um candidato
modesto desta vez (NS, PN, BSD, TOE, QF), sinal de aproximacao da
fronteira de pequenos passos disponiveis em multiplas frentes ao mesmo
tempo. Nenhum item derivado de candidato `REFUTED` (nenhum candidato
desta rodada foi `REFUTED` -- ver observacao na abertura do documento).
A recomendacao de infraestrutura (`_SHARED_INFRA/FORMAL` no Lake) fica
FORA da contagem -- nao e teste Lean falsificavel, e explicitamente
adiada para sessao dedicada de governanca. Notas de dependencia: item 7
(YM Passo 2) depende de item 6 (YM Passo 1); item 12 (BSD STEP5b)
depende de item 11 (BSD STEP5a) e NAO deve ser alegado fechado so por
#11 ter sucesso; item 4 (PN-8) e autonomo mas mecanicamente contiguo aos
itens PN-6/PN-7 ja fechados na Onda 3.

---

## Descartados/adiados nesta rodada (nao reabrir sem evidencia nova)

```text
SHARED-INFRA  Registrar _SHARED_INFRA/FORMAL no projeto Lake TamesisLab
      -- nao descartado, corretamente adiado (mesmo tratamento que
         NS-3b recebeu na Onda 3). E recomendacao de infraestrutura,
         nao teste Lean falsificavel; fatos verificados (lakefile.toml
         so registra TamesisLab; nenhuma importacao cross-line existe
         hoje) confirmam que a dependencia real ja existe na pratica
         (UnboundedEigCountFloorLaw.lean reproduz codigo compartilhado
         verbatim por falta dessa integracao). Piloto minimo proposto
         (mover um arquivo ja fechado + lake build isolado) deve
         acontecer em sessao dedicada com sign-off de governanca, nao
         nesta onda de conteudo matematico.
```

Nenhum candidato foi `REFUTED` nesta rodada -- primeira onda (desde a
Onda 2) em que isso acontece. Ver observacao no "Enquadramento honesto"
acima sobre por que isso reflete um recon bem calibrado, nao uma
adversarial mais frouxa (dois candidatos inteiros foram efetivamente
compilados pela revisao com `lake env lean`, e um erro matematico
substantivo -- a hipotese route-b do RH incondicional sobre `mu:C` --
foi encontrado e corrigido, nao ignorado).

---

## Avaliacao pessoal — os 1-3 candidatos com maior chance de virar
resultado formal honesto e nao-trivial mais cedo

Nao e repeticao da autoavaliacao dos agentes de recon/adversarial -- e
julgamento proprio depois de ler as 15 verificacoes inteiras desta onda.

**1. YM-CAPSTONE-BRACKET (item 5).** E o unico candidato desta onda que
a propria revisao adversarial ja compilou do inicio ao fim contra o
Mathlib real do projeto, incluindo a correcao do unico obstaculo
encontrado (`open Matrix WithLp` vestigial). Nao ha trabalho matematico
remanescente -- e recombinacao pura de duas pecas ja fechadas na Onda 3,
com o unico ponto de atrito ja identificado e resolvido. Risco tecnico
residual: praticamente zero, e o teste ja tem um artefato compilado
como evidencia.

**2. YM-CAPSTONE-FULL, Passo 1 (item 6).** Tambem ja compilado pela
revisao (`trace (toEuclideanCLM M2) = 4`), apos corrigir dois erros de
sintaxe/argumento-nomeado que um implementador cego as citacoes
originais teria enfrentado. Como item isolado (nao o candidato completo,
que ainda depende do Passo 2 nao verificado), e um resultado pequeno,
barato e ja de-riscado.

**3. HG-4D (item 10).** Composicao de uma linha de dois resultados ja
compilados independentemente (HG-4/HG-4C, Onda 3), citacoes Mathlib
conferidas exatas, sem ambiguidade de tipagem. Mesmo padrao de "menor
risco tecnico" que HG-4C teve na Onda 3.

Nao incluo RH-4 no top 3 apesar de solido: e um limite (nao identidade)
sobre naturais de brinquedo, matematicamente limpo, mas exige montar
`Tendsto.add`/`congr'` num arquivo novo do zero -- mais passos de
elaboracao do que os tres itens acima, mesmo sem citacao Mathlib
questionavel. BSD-STEP5a fica de fora do top 3 apesar de potencialmente
o resultado mais IMPORTANTE da onda (progride genuinamente sobre
BSD-GAP-007): ao contrario dos itens 5/6/10, a propria composicao nunca
foi tentada nem compilada pela revisao -- so as pecas isoladas -- e a
linha BSD ja teve um item inteiro (STEP2-FULL, Onda 2) refutado por
muro de tipagem estrutural, entao o historico pede cautela extra antes
de apostar nele como "fechamento facil".

## O laboratorio chegou ao ponto de pausar o ciclo de ondas?

Avaliacao honesta, separada da anterior. Quatro sinais apontam para
"sim, ou pelo menos para reduzir o ritmo":

1. **A contagem de candidatos por rodada esta caindo estruturalmente**,
   nao por acidente de amostragem: Onda 1 (25), Onda 2 (20), Onda 3
   (15), Onda 4 (14 -- e isso apos varias linhas renderem so um
   candidato modesto). O padrao e consistente com exaustao progressiva
   dos pequenos passos alcancaveis por composicao de resultados ja
   fechados, nao com um poco inesgotavel.
2. **BSD e a unica linha com um gap nomeado e rastreado
   (`BSD-GAP-007`) que uma onda inteira de pequenos passos ainda nao
   fechou** -- quatro rodadas (Onda 1 diagnostica, Onda 2 refuta uma
   rota, Onda 3 fecha STEP3/STEP4, Onda 4 propoe STEP5a/STEP5b) e o
   proprio gap note continua dizendo, no fundo, "isso e um projeto de
   escala propria". Isso e exatamente o tipo de alvo para o qual o modo
   "onda paralela de sondas pequenas" e estruturalmente mal adequado --
   cada passo e pequeno, mas a CADEIA de passos ate o teorema
   incondicional continua crescendo (STEP1->STEP2[refutado]->STEP3->
   STEP4->STEP5a->STEP5b), e cada elo novo continua descobrindo mais
   elos.
3. **RH e NS ja tem sub-frentes explicitamente identificadas como
   "seriam um projeto proprio"** (RVM-NZeta para RH desde a Onda 3;
   distribuicao p.v. global via `limitCLM` para NS desde a Onda 3) --
   nenhuma delas mudou de categoria nesta rodada.
4. **Contra-sinal:** varias linhas (HG, YM, TOE) continuam produzindo
   candidatos genuinamente baratos e bem-definidos onda apos onda, sem
   sinal de esgotamento -- HG em particular teve TRES candidatos novos
   e nenhum REFUTED nesta rodada, e a linha compartilhada
   (SHARED-INFRA) continua gerando follow-ons uteis (SHARED-4A/4B) que
   nenhuma onda anterior antecipou.

**Conclusao honesta:** nao ha um sinal unico e decisivo, mas a
combinacao dos quatro pontos acima sugere que o modo certo daqui para
frente e HIBRIDO, nao um corte total do ciclo de ondas: (a) continuar
ondas pequenas-paralelas para as linhas que seguem produzindo candidatos
baratos e bem-definidos (HG, YM, TOE, SHARED-INFRA parecem ter ainda
alguma corda); (b) abrir uma sessao/projeto DEDICADO e de escala propria
para `BSD-GAP-007` especificamente (seguindo o proprio "onde retomar" do
`BSD-1_GAP_NOTE.md`, agora atualizado por este documento com a rota
STEP5a/STEP5b), em vez de continuar tratando-o como um item de onda a
mais; (c) tratar RH-RVM-NZeta e NS-distribuicao-global como candidatos a
projeto dedicado semelhante, so se/quando o laboratorio decidir investir
neles deliberadamente -- nao forcar seu aparecimento em rodadas futuras
de recon so para preencher a lista.

---

## O que este documento confirma sobre o processo

A disciplina de "reverificar por leitura direta de arquivo, e nesta
rodada em varios casos por COMPILACAO DIRETA com `lake env lean`, nao
por confianca no recon" continuou achando coisas reais: uma hipotese de
teste falsificavel matematicamente FALSA como enunciado irrestrito (a
rota (b) do RH sobre todo `mu:C`, refutada por contraexemplo numerico
explicito), dois obstaculos de sintaxe/nomeacao de argumento que um
implementador cego as citacoes teria enfrentado e que so apareceram ao
efetivamente tentar compilar (YM-CAPSTONE-FULL Passo 1), uma colisao de
namespace que so surge ao combinar dois arquivos-fonte que nunca
tinham sido compostos antes (YM-CAPSTONE-BRACKET), e uma lacuna de
composicao load-bearing nao citada pelo proprio candidato (QF-7,
`skewAdjoint.smul_mem`). Em nenhum caso isso invalidou o candidato
subjacente -- em todos, o alvo real continuou de pe, so precisou de
correcao de rota ou de divisao explicita em checkpoints menores e mais
honestos. Para BSD especificamente, essa mesma disciplina produziu o
resultado mais importante deste documento: confirmar, com evidencia
concreta (dois arquivos compilados independentemente, todo lema
Mathlib citado conferido), que uma composicao promissora existe mas
AINDA NAO foi tentada -- e nomear precisamente, no mesmo estilo do
`BSD-1_GAP_NOTE.md` original, o que continua faltando mesmo se essa
composicao funcionar.
