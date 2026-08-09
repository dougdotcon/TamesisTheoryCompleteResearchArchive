---
document_id: PLANO-ATAQUE-PORTFOLIO-COMPLETO-2026-08-09
reviewed_at: 2026-08-09
input: recon + revisao adversarial de 8 frentes (6 Millennium oficiais Clay + 2 extensoes internas do laboratorio)
conclusion: PLANO_DE_EXECUCAO_EM_ONDAS_PROPOSTO
---

# Plano de ataque de portfolio completo — 8 frentes

## Enquadramento honesto

Este documento sintetiza uma rodada de reconhecimento + revisao adversarial
(citacoes Mathlib reconferidas por leitura direta de arquivo, nao por
confianca no agente de recon) sobre candidatos de ataque **nao-convencionais**
para as 8 frentes de pesquisa do laboratorio: os 6 Problemas do Milenio
oficiais da Clay (Riemann, Navier-Stokes, P vs NP, Yang-Mills, Hodge, BSD)
mais 2 extensoes internas do laboratorio (Sintese TOE e Fundamentos
Quanticos/Unificacao) que **nao sao reconhecidas pela Clay Mathematics
Institute e nunca devem ser apresentadas como tal**.

```text
O que este plano E:
  - um mapa de pequenos testes falsificaveis, baratos, de sessao unica,
    contra infraestrutura Mathlib genuina mas hoje desconectada
  - uma tentativa de identificar onde construir peca de infraestrutura
    formal compartilhada rende mais que duplicar esforco por frente
  - honesto sobre candidatos REFUTADOS -- para que ninguem precise
    re-derivar por que foram descartados

O que este plano NAO E:
  - uma alegacao de que qualquer Problema do Milenio ficou mais proximo
    de ser resolvido
  - uma alegacao de que as extensoes TOE/Quantica tem status Clay-oficial
  - uma promessa de que todo teste "SURVIVES" vai fechar sem sorry -- e
    uma aposta informada, nao uma certeza
```

Cada candidato abaixo passou por reverificacao independente de citacao
Mathlib (leitura direta do arquivo em
`05_FORMAL/lean/.lake/packages/mathlib/Mathlib`, nao grep-e-confia) e
recebeu um veredito: `SURVIVES` (teste proposto se sustenta como esta),
`NEEDS_NARROWING` (angulo real, mas o teste proposto precisou ser reescrito
para ser genuinamente pequeno/correto), ou `REFUTED` (nao vale investir).

---

## 1. Riemann Hypothesis (RH) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| RH-2 | Conectar `riemannZetaZeros` (discretude/finitude Mathlib) a N_zeta(T) | SURVIVES | baixo |
| RH-1 | Fechar RVM-LIMIT como lema autonomo de analise real | SURVIVES | baixo |
| RH-4 | Estender `eigCount` a uma funcao de contagem N(Lambda) | NEEDS_NARROWING | baixo (apos correcao) |
| RH-3 | Instancia minima de operador auto-adjunto nao-limitado via `LinearPMap` | NEEDS_NARROWING | moderado |
| RH-5 | Rota Nevanlinna/Jensen para bound cru de contagem de zeros | NEEDS_NARROWING | baixo (apos correcao) |

**RH-2 — SURVIVES.** `riemannZetaZeros` (`Mathlib/NumberTheory/LSeries/ZetaZeros.lean:33`),
`isClosed_riemannZetaZeros` (:57), `isDiscrete_riemannZetaZeros` (:60) e
`IsCompact.inter_riemannZetaZeros_finite` (:64) existem exatamente como
citados; zero referencias previas no laboratorio. A maquinaria de
compacidade de retangulo em C que o teste precisa (`IsClosed.reProdIm`,
`Bornology.IsBounded.reProdIm`, `isCompact_iff_isClosed_bounded`,
`ProperSpace C`) foi verificada existir e encaixar. Teste proposto mantido
sem alteracao.

**RH-1 — SURVIVES.** `PowerLog.lean` existe como descrito, a prova de
`tendsto_powerLogFactor_nhds_zero_of_one_lt` genuinamente chama
`(isLittleO_log_rpow_atTop hr).tendsto_div_nhds_zero` (confirmado em
`Mathlib/Analysis/SpecialFunctions/Pow/Asymptotics.lean:364`). E a mesma
especie de "razao de assintoticas" das lemas ASYM-NOGO-001 ja verificadas.
**Teste revisado:** isolar primeiro o sub-lema
`Tendsto (fun T => log(T/(2*pi))/log T) atTop (nhds 1)` sozinho, antes de
compor no limite completo do quociente -- isso isola o passo genuinamente
novo (log(T/c)/log T -> 1) da composicao rotineira de aritmetica de
limites ao redor dele.

**RH-4 — NEEDS_NARROWING (defeito real, nao so imprecisao).** Todas as
citacoes (`eigCount` :143, `finite_eigenvalues_above` :92,
`eigCount_antitone` :180) conferem. Mas o teste falsificavel proposto pede
`Tendsto (fun L => eigCount T L) atTop atTop` -- direcao invertida, pois
`eigCount_antitone` (ja provado no laboratorio) implica que essa contagem e
**nao-crescente** em L, logo nunca tende a atTop quando o limiar cresce.
**Teste revisado:** provar
`Tendsto (fun lam => (eigCount T lam : R)) (nhdsWithin 0 (Set.Ioi 0)) atTop`
para um operador compacto auto-adjunto com espectro infinito, reutilizando
`finite_eigenvalues_above`/`eigCount_antitone`. Registrar explicitamente que
essa contagem-cauda de operador compacto **nao e** diretamente o N(Lambda)
de Weyl do GWB (que conta autovalores de um operador nao-limitado abaixo de
Lambda, crescendo com Lambda -> +infinito); a ponte entre os dois exige
inversao espectral (lambda = 1/mu), uma obrigacao separada ainda nao
nomeada em nenhum lugar.

**RH-3 — NEEDS_NARROWING.** Citacoes de `LinearPMap`/`IsFormalAdjoint`
conferem exatamente (linhas 74/152/235/242/341), e a ausencia de
espectro/resolvente/Friedrichs em todo o Mathlib foi reconfirmada por grep
(zero hits). Mas o teste proposto (multiplicacao em L^2(R) com dominio
{g : f*g in L^2}) exige stack de teoria da medida real (densidade via
funcoes simples, integrabilidade) -- nao e sessao unica.
**Teste revisado:** trocar L^2(R) por um operador diagonal em espaco de
sequencias l^2 (via `lp`/`PiLp`), dominio
`{x : l^2 | (fun n => n*x n) in l^2}`. Densidade do dominio vem de
sequencias de suporte finito serem l^2-densas -- muito mais elementar que
densidade em L^2(R) -- mantendo o mesmo teste de
`LinearPMap.adjoint`/`IsFormalAdjoint` ponta a ponta.

**RH-5 — NEEDS_NARROWING.** `logCounting_isBigO_one_iff_analyticOnNhd`
existe (`.../LogCounting/Asymptotic.lean:109`); ausencia de qualquer
`IsBigO`/bound de crescimento para `riemannZeta` em faixa vertical
reconfirmada por grep amplo. O teste original ("procurar, depois tentar
formular") ja tinha sido efetivamente executado por dois checks
independentes chegando no mesmo "muro".
**Teste revisado:** pular a busca redundante e ir direto ao bound trivial
`|riemannZeta (sigma + I*t)| = O(1)` para sigma > 1 FIXO (fora da faixa
critica, onde a serie de Dirichlet converge absolutamente), usando so a
maquinaria de produto de Euler ja existente para Re s > 1. Se nem esse
bound trivial ja estiver empacotado como `IsBigO` reutilizavel, isso
confirma que a infraestrutura de crescimento para zeta falta em todo nivel,
nao so na faixa critica -- decidindo desinvestir sem tocar a estimativa de
convexidade genuinamente dificil.

---

## 2. Navier-Stokes (NS) — Clay oficial (linha do nucleo Calderon-Zygmund)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| NS-3 | Analogo discreto/periodico via `ZMod N` DFT + cotangente | NEEDS_NARROWING | baixo (apos correcao) |
| NS-1 | Estender fato de media-zero a p.v. contra teste Lipschitz/C^1 | NEEDS_NARROWING | moderado |
| NS-2 | Reaproveitar framework `Distribution`/`TemperedDistribution`/`FourierMultiplier` | SURVIVES | moderado, **depende de NS-1** |
| NS-4 | Desigualdade maximal de Doob (Martingale) como substituto de dyadic cubes | SURVIVES (= beco sem saida confirmado) | — |

**NS-3 — NEEDS_NARROWING.** `ZMod.dft` (:88), `dft_dft` (:177),
`dft_odd_iff` (:197), `Complex.cot_series_rep` (:231) todos conferidos
exatos. Mas o teste original (N=8 via `decide`/`norm_num`) superestima:
`ZMod.dft` usa expoentes complexos genuinos de raizes 8-esimas da unidade,
que `decide` nao alcanca sem lemas de angulo especial.
**Teste revisado:** usar N=4 primeiro (raizes {1,i,-1,-i}, ja em forma
normal Mathlib), so escalando para N=8/geral depois de fechar N=4.

**NS-1 — NEEDS_NARROWING.** `K_homogeneous` (:272-282),
`contDiffAt_K` (:318), `K_mean_zero_sphereSurfaceMeasure` (:725) conferem.
Mas `integral_fun_norm_addHaar` (HaarToSphere.lean:296) so se aplica a
funcoes de `‖x‖` isoladas -- K(y)*(phi(y)-phi(0)) depende de direcao, entao
essa lema **nao serve** diretamente para a decomposicao em cascas alegada.
Encontrado (nao citado pelo recon) `integrableOn_ball_of_norm_le_rpow`
(SpecialFunctions/Pow/Integral.lean:109), rota mais barata via bound
pontual |K(y)(phi(y)-phi(0))| <= C/‖y‖^2, mas exige media-zero em **todo**
raio r, nao so r=1 -- um lema de escala ainda nao existente em lugar nenhum.
**Teste revisado:** provar `HasLocalPV` em 4 passos: (1) media-zero em raio
r via escala explicita de `sphereSurfaceMeasure` sob dilatacao (a peca
genuinamente nova); (2) bound |K| <= C*‖y‖^-3 via `contDiffAt_K` + compacidade
da esfera; (3) `integrableOn_ball_of_norm_le_rpow` (dim=3, alpha=2) para
integrabilidade absoluta na bola cheia; (4) convergencia da integral em anel
via continuidade absoluta do integral de Lebesgue quando epsilon -> 0.

**NS-2 — SURVIVES, mas logicamente a jusante de NS-1.** `Distribution`,
`TemperedDistribution` (`fourier_apply` linha exata 482),
`fourierMultiplierCLM` (linhas 50/141) todos conferidos exatos, sem
fabricacao. Remove apenas a metade "sem construtor de p.v." do bloqueio;
o teste so faz sentido depois que a integrabilidade absoluta de NS-1 estiver
estabelecida como insumo.

**NS-4 — SURVIVES, mas equivale a beco sem saida ja confirmado; nenhuma
acao de continuacao.** `maximal_ineq` (`.../OptionalStopping.lean:155`)
confirmado ser martingale de **tempo discreto** indexado por filtracao, sem
qualquer relacao com decomposicao espacial em R^3. Grep ampliado por toda a
arvore Mathlib (nao so `Probability/` e `MeasureTheory/`) confirma zero
filtracao diadica em espaco euclidiano em lugar nenhum. Aplicar
`maximal_ineq` a um problema espacial CZ exigiria construir do zero uma
filtracao diadica em R^3 -- exatamente o mesmo custo da rota classica via
cubos diadicos, nao um atalho. **Nao ha teste de continuacao a despachar
aqui** -- o proprio teste original ja e a falsificacao correta e completa.

---

## 3. P vs NP (PN) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| PN-4 | Sonda de relativizacao via `Nat.RecursiveIn`/`TuringDegree` | SURVIVES | baixo |
| PN-3 | Segunda testemunha nao-identidade (negacao booleana) de `TM2ComputableInPolyTime` | SURVIVES | baixo |
| PN-1 | Formalizar `Language.P`/`Language.NP` sobre `TM2ComputableInPolyTime` | NEEDS_NARROWING | baixo (apos correcao) |
| PN-2 | Atacar o `proof_wanted TM2ComputableInPolyTime.comp` via id-com-id | NEEDS_NARROWING | moderado, **depende de PN-3** |
| PN-5 | Teorema de Fagin / complexidade descritiva via `ModelTheory` | **REFUTED** | — |

**PN-4 — SURVIVES.** `Nat.RecursiveIn` lido por inteiro
(zero/succ/left/right/oracle/pair/comp/prec/rfind, linhas 61-79),
`RecursiveIn.mono` (:212), `recursiveIn_empty_iff` (:229) confirmados;
zero uso no laboratorio; zero maquinaria oracle-com-tempo-limitado em
qualquer lugar de Mathlib (confirmado por grep alem dos dois arquivos
citados pelo recon) -- exatamente como alegado, e alegado honestamente
como limitacao (nao ponte para relativizacao BGS com tempo). Teste
proposto mantido.

**PN-3 — SURVIVES.** `TM2.Stmt` tem push/peek/pop/load/branch/goto/halt
(`StackTuringMachine.lean:127-134`) com maquinaria suficiente para negacao
booleana genuina. Diferente da instancia identidade (que so faz alias entre
duas pilhas identicas, sem computacao real), negacao exige pop-negar-push
via estado interno -- um caso genuinamente mais dificil por um degrau, que
testa se o aparato e usavel alem do caso degenerado.

**PN-1 — NEEDS_NARROWING (defeito de tipagem real).** Citacoes exatas
(`FinTM2` :46, `TM2ComputableInPolyTime` :179-188, `idComputableInPolyTime`
:204-230). Mas `∃ βΓ (eb : ...), TM2ComputableInPolyTime ...` como escrito
**nao elabora**: `TM2ComputableInPolyTime` e uma `structure` em `Type`, e
`Exists`/`∃` exige motivo em `Prop`. Alem disso a definicao de NP e
subespecificada: o bound de tempo em `Polynomial ℕ` avalia o comprimento do
input **codificado inteiro** (x concatenado com certificado y), sem
mecanismo para limitar |y| <= p(|x|) para um polinomio p separado do que
limita o tempo -- exatamente a sutileza que torna uma definicao NP
Cook-Karp-fiel nao-trivial.
**Teste revisado:** passo 1, `Language.P := Nonempty (TM2ComputableInPolyTime ...)`
(trocar ∃ por Nonempty, fixar eb = encodeBool), verificar que compila e e
habitado para L = univ via `idComputableInPolyTime`. Passo 2 (separado, sem
prova): so **declarar** `Language.NP` com hipotese auxiliar de bound de
certificado e ver se sequer type-checka -- o travamento ali, nao no passo 1,
e o sinal informativo.

**PN-2 — NEEDS_NARROWING.** `proof_wanted TM2ComputableInPolyTime.comp`
confirmado unico no Mathlib inteiro (:284-288). Mas compor
`idComputableInPolyTime` consigo mesma e o caso degenerado id∘id=id,
provavel por `rfl`/`Function.comp.left_id` sem tocar a maquinaria real de
copia de fita entre tipos Sum -- um teste que fecharia sem dizer nada sobre
a dificuldade real da composicao geral.
**Teste revisado:** compor duas maquinas com tipos distintos (identidade +
negacao booleana de PN-3, construida como pre-requisito), e verificar so a
nivel de tipo (sem prova) se a fase de copia entre pilhas de tipos
`tm1.Γ tm1.k₁` e `tm2.Γ tm2.k₀` sequer type-checka. Depende explicitamente
de PN-3 estar construida primeiro.

**PN-5 — REFUTED.** Ausencias reconfirmadas (zero "fagin", zero
"ehrenfeucht", zero segunda-ordem/monadic em `ModelTheory`; unicos hits de
"back and forth" sao ordem densa contavel, nao relacionados). `ModelTheory`
tem apenas sintaxe FOL generica (`IsAtomic`/`IsQF`/`IsPrenex`), sem
quantificacao de segunda ordem, sem especializacao a estruturas finitas, sem
conexao a classes de complexidade. Diferente das outras frentes, aqui **nao
ha infraestrutura existente para reaproveitar** -- o proprio recon admite
"essencialmente nenhum scaffold Mathlib para construir sobre". O custo
proprio (very_high) contradiz o requisito de teste pequeno. Registrar como
ausencia confirmada; nao reabrir sem nova evidencia de infraestrutura.

---

## 4. Yang-Mills (YM) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| YM-1 | Gap espectral de matriz de transferencia finita (autovalores Hermitianos) | NEEDS_NARROWING | baixo (apos correcao) |
| YM-3 | Estabilidade do gap de autovalor sob convergencia em norma de operador | SURVIVES | baixo-moderado |
| YM-2 | Teorema de gap espectral Perron-Frobenius sobre scaffolding `Irreducible`/`Primitive` | SURVIVES | moderado |
| YM-4 | Rota de teoria de representacao de grupo de Lie compacto SU(2)->SU(N) | **REFUTED** | — |

**YM-1 — NEEDS_NARROWING.** `spectral_theorem`, `eigenvalues_eq`,
`det_eq_prod_eigenvalues`, `trace_eq_sum_eigenvalues` (Matrix/Spectrum.lean,
linhas 141/146/191/238) e `eigenvalues_antitone`
(InnerProductSpace/Spectrum.lean:312) todos existem exatamente como citado.
Mas `IsHermitian.eigenvalues` e **noncomputable**, construido via escolha
(`eigenvalues₀` + `Fintype.equivOfCardEq`) -- nao e um one-liner para
matriz numerica concreta; exige traducao real via
`eigenvalues_eq`/`charpoly_eq` de volta a numeros concretos.
**Teste revisado:** pular a API abstrata na primeira passada. Para uma
matriz 2x2 real simetrica explicita [[a,b],[b,d]], provar via
formula quadratica/discriminante (traco = a+d, det = ad-b^2) que as duas
raizes diferem por quantidade estritamente positiva, usando `nlinarith`.
Conectar a API abstrata via `eigenvalues_eq`/`charpoly_eq` so como meta
estica (wave 2), nao caminho primario.

**YM-3 — SURVIVES.** `norm_eq_iSup_rayleighQuotient` (Rayleigh.lean:120-134)
lida por inteiro e confirmada. Achado adicional relevante:
`hasEigenvalue_iSup_of_finiteDimensional` (:325-336) -- em dimensao finita o
sup COM SINAL do quociente de Rayleigh e realizado como autovalor via
argumento de valor extremo de Weierstrass na esfera, exatamente a
ferramenta que faz o argumento 1-Lipschitz em norma de operador ser
manipulacao elementar de `ciSup`. Ausencia de qualquer maquinaria tipo
Weyl/Courant-Fischer de perturbacao de autovalor reconfirmada por grep
amplo (fora de teoria de Lie/sistemas de raiz).

**YM-2 — SURVIVES.** `LinearAlgebra/Matrix/Irreducible/Defs.lean` e o
UNICO arquivo do diretorio (240 linhas): `IsIrreducible` (:82),
`IsPrimitive` (:88), `isIrreducible_iff_exists_pow_pos` (:159), e
`IsPrimitive.isIrreducible` (:182) (nome real da declaracao; a string do
recon `IsPrimitive.to_IsIrreducible` era so o docstring de prosa em :42 --
correcao de citacao menor, nao fabricacao). Tag "perron-frobenius" no
proprio arquivo confirma referencia futura deliberada. Ausencia do
resultado de dominancia de autovalor reconfirmada em toda a arvore.

**YM-4 — REFUTED.** A ausencia e ainda mais completa do que o recon
descreveu: grep case-insensitive por "peterweyl"/"peter_weyl"/"peter-weyl"
retorna **literalmente zero hits** em todo o Mathlib (nem sequer um stub,
diferente do caso Perron-Frobenius). `Matrix.specialUnitaryGroup` existe
so como Submonoid algebrico, sem topologia/metrica/compacidade em lugar
nenhum. Nenhum `UnitaryRepresentation` existe. `RepresentationTheory/` e
puramente algebrico (modulos de anel de grupo), nao a teoria analitica de
representacao de grupos de Lie compactos necessaria aqui. Perseguir esta
rota significa construir um subcampo inteiro do zero primeiro -- o proprio
recon ja classifica custo `very_high`/plausibilidade `low`. (Nota a
parte: "SU(2) e `CompactSpace`" isoladamente E pequeno e provavel via
`FiniteDimensional.proper`/Heine-Borel, mas nao contribui em nada
especificamente para Peter-Weyl/YM-GAP-005 -- nao vale investir so por
isso.)

---

## 5. Hodge Conjecture (HG) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| HG-2 | Reaproveitar `ClassGroup.equivPic` como esqueleto algebrico "classe de divisor = classe de fibrado" | SURVIVES | baixo |
| HG-1 | Ponte divisor-principal-como-ciclo-algebrico (`AlgebraicCycle.Basic` x `OrderOfVanishing`) | SURVIVES | moderado |
| HG-4 | Stub minimo de fibrado de linha holomorfo em `Geometry/Manifold/Complex.lean` | NEEDS_NARROWING | baixo (apos correcao) |
| HG-3 | Trivialidade codim-1 = top-codim para curva projetiva lisa via homologia singular | **REFUTED** | — |

**HG-2 — SURVIVES.** `ClassGroup.equivPic : ClassGroup R ≃* Pic R`
(PicardGroup.lean:878-881) confirmado; `Pic` (:431) confirmado. Unico hit
de `Pic`/`PicardGroup` em `AlgebraicGeometry/` e a condicao lateral so-em-
docstring de `EllipticCurve/Weierstrass.lean` -- confirma o lado algebrico
provado e desconectado da geometria, exatamente como alegado. Instancias
Dedekind concretas prontas (`IsDedekindDomain (𝓞 K)` em
`NumberField/Basic.lean:314`) tornam especializar `equivPic` em teste
genuinamente barato, nao aspiracional. Escopo honesto: so da Pic ≅
ClassGroup, nao a direcao de sobrejetividade sobre H^{1,1} que Lefschetz
(1,1) realmente precisa.

**HG-1 — SURVIVES.** `AlgebraicCycle` como `abbrev` de
`Function.locallyFinsupp` (:37-38) e `OrderOfVanishing.ord`/`ordHom`
(:33-56) conferidos exatos; zero referencia cruzada entre os dois arquivos.
Ideal.finite_factors (`DedekindDomain/Factorization.lean:84-89`) ja prova
finitude ideal-teorica de primos de altura 1 que dividem um ideal nao-nulo
-- entao o insumo bruto do teste nao e vazio. Mas nenhuma lema conecta
`HeightOneSpectrum R` (lado ideal-teorico) a pontos de coaltura-1 de um
Scheme (linguagem de `OrderOfVanishing.ord`) -- confirmado zero hits.
Teste bem posto: ou fecha reaproveitando finitude existente (vitoria
barata), ou revela que a identificacao HeightOneSpectrum <-> ponto-de-
coaltura-1 e ela mesma peca faltante (muro barato de descobrir). **Ver
secao de infraestrutura compartilhada -- esta mesma ponte importa tambem
para BSD.**

**HG-4 — NEEDS_NARROWING.** TODO confirmado verbatim
(`Geometry/Manifold/Complex.lean:27-34`). Grep mais cuidadoso (4 arquivos
com "holomorph"+"bundle", nao 1) mostra que os 3 hits extras sao so o
idioma "bundled as" -- a alegacao substantiva do recon se sustenta. Mas
"<=30 linhas" reutilizando a API generica `VectorBundle`/`Bundle`
subestima o risco: essa API e construida sobre `ContMDiff` real, e enfiar
uma condicao holomorfa genuina sem ela degenerar silenciosamente em fibrado
real-suave e exatamente o tipo de problema de encanamento de typeclass que
ja consumiu esforco real em PRs Mathlib comparaveis.
**Teste revisado:** testar SO se "compatibilidade de transicao holomorfa"
e sequer enunciavel via `ContMDiff (𝓘(ℂ,ℂ)) (𝓘(ℂ,ℂ)) ⊤` num total space de
brinquedo de 2 cartas (M x C sobre 1 carta fixa), sem tentar encaixar na
API geral de `VectorBundle`. Genuinamente <=30 linhas, separa "podemos
enunciar holomorficidade" de "podemos retrofit na API geral" (a parte
provavelmente dificil).

**HG-3 — REFUTED.** Nao pelas alegacoes de suporte Mathlib -- essas
conferem (4 arquivos exatos em `SingularHomology/`, `HomologyZero.lean` so
computa H_0, zero hits de "fundamental class"/"Poincare duality" em todo
Mathlib). Mas o proprio recon rotula custo `very_high`/plausibilidade
`low` E preve o resultado do teste ("bate num muro imediatamente") **antes**
de propo-lo. Um teste cujo autor ja sabe a resposta nao e teste de hipotese
viva -- e um resultado negativo pre-concedido disfarcado de candidato.
Registrar como ausencia confirmada no registro de gaps; nao reabrir como
"candidato a investir" em lotes futuros.

---

## 6. Birch and Swinnerton-Dyer (BSD) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| BSD-4 | Escopar precisamente o gap restante na cadeia de Mordell-Weil ja em progresso no Mathlib | SURVIVES | minimo (so leitura/escrita) |
| BSD-3 | Convergencia condicional (Hasse) de L(E,s) a partir de hipotese Hasse explicita | NEEDS_NARROWING | baixo (nucleo aritmetico isolado) |
| BSD-1 | `WeierstrassCurve.LFunction` e funcao aritmetica multiplicativa | NEEDS_NARROWING | moderado |
| BSD-2 | Finitude do lugar de reducao ruim de uma curva de Weierstrass | NEEDS_NARROWING | moderado |

**BSD-4 — SURVIVES.** Todas as citacoes conferem: docstring de
`GroupTheory/Descent.lean` (~20-45), `CommGroup.fg_of_descent'` (:150),
TODO de `AddSubMap.lean:21`, `instAdmissibleAbsValues`
(`Height/NumberField.lean:77`). Sem codigo Lean exigido -- risco minimo.
**Correcao ao relatorio esperado:** o lado de altura/lei do paralelogramo
esta MENOS perto de fechado do que o recon sugeriu -- o proprio TODO de
`Height/EllipticCurve.lean` admite que "definir a altura ingenua" e
"adicionar a lei do paralelogramo aproximada" seguem em aberto; o que esta
provado (:45-51) e so uma desigualdade de altura em coordenadas P^2
arbitrarias, uma camada de abstracao removida de um enunciado sobre pontos
reais P, Q em E(K). Lista de gaps honesta: (1) correcao do `AddSubMap`,
(2) altura ingenua sobre E(K) ainda nao definida, (3) lei do paralelogramo
para pontos de curva (nao so coordenadas projetivas) ainda nao enunciada,
(4) Mordell-Weil fraco inteiramente ausente e separado. Nao caracterizar
como "quase fechado".

**BSD-3 — NEEDS_NARROWING.** `LSeriesSummable_of_le_const_mul_rpow`
(:341) e `LSeriesSummable_of_isBigO_rpow` (:367) conferem exatos;
`WeierstrassCurve.LSeries` e genuinamente `LSeries (... ∘ W.LFunction) s`
(:84); ausencia total de "Hasse"/modularidade em Mathlib reconfirmada
(unicos hits sao falsos-positivos de substring). Mas o teste proposto
empilha silenciosamente a multiplicatividade nao-provada de BSD-1 sobre um
argumento indutivo real (recursao de dois termos estilo Dickson/Chebyshev
sob |a| <= 2*sqrt(q)) -- nao e "estimativa de rotina".
**Teste revisado:** desacoplar e testar so o nucleo aritmetico,
independente de curva de Weierstrass/L-function: dado a, q com
|a| <= 2*sqrt(q), c_0=1, c_1=a, c_{n+1}=a*c_n - q*c_{n-1}, tentar
`|c_n| <= (n+1)*q^(n/2)` por inducao. Isola o cerne matematico real sem
exigir BSD-1 nem maquinaria adica/HeightOneSpectrum.

**BSD-1 — NEEDS_NARROWING.** `eulerProduct`/`localEulerFactor`
(LFunction.lean:79-85, :43-58) e `isMultiplicative_ofPowerSeries_of_isPrimePow`/
`isMultiplicative_eulerProduct` (ArithmeticFunction/LFunction.lean:186, :314)
conferem exatos; o argumento algebrico central e genuinamente barato como
alegado (nao precisa de hipotese extra de "Multipliable"). Mas o passo
conectivo que o proprio recon ja sinalizava -- que o corpo de residuo da
completacao adica em `v.adicCompletionIntegers K` e uma potencia de primo
-- e um gap real e desconectado. Grep confirma zero lema ligando
`ResidueField`+`HeightOneSpectrum`+`adicCompletion`; o unico transporte
generico disponivel (`AdicCompletion.residueField_map_bijective`,
`AdicCompletion/LocalRing.lean:151-154`) e para a construcao de completacao
de MODULO (`AdicCompletion (maximalIdeal R) R`), diferente da construcao de
completacao de espaco uniforme (`Valued.v.integer`) realmente usada em
`LFunction.lean` -- nenhuma ponte encontrada entre as duas.
**Teste revisado:** isolar SO `Finite (IsLocalRing.ResidueField (v.adicCompletionIntegers K))`
como meta autonoma antes de tocar `IsMultiplicative`. Se fechar via
isomorfismo de corpo de residuo para `𝓞K ⧸ v.asIdeal` ja existente, o
candidato inteiro e barato; se exigir construir compatibilidade nova entre
os dois frameworks de completacao, esse e o achado negativo (barato de
descobrir) que decide se vale prosseguir.

**BSD-2 — NEEDS_NARROWING.** `HasGoodReduction`/`HasMultiplicativeReduction`/
`HasAdditiveReduction`/`HasSplitMultiplicativeReduction`
(Reduction.lean:281-329) conferem; TODO sobre discriminante em
caracteristica != 2 confirmado verbatim (:314); `conductor` confirmado
ausente em `AlgebraicGeometry/`. `Ideal.finite_factors` (:84) da o insumo
de finitude bruto, ate mais forte que o citado. Mas `Reduction.lean` **nao
importa** `DedekindDomain/AdicValuation.lean`, `Factorization.lean` nem
`HeightOneSpectrum` em lugar nenhum -- e um framework de DVR abstrato
totalmente generico e isolado. A ponte entre a valuacao abstrata local
(`valuation K (maximalIdeal R) W.Δ < 1`) e a fatoracao de ideal global
(`p ∣ (Δ)`) nao e cola, E o conteudo matematico -- um lema de
compatibilidade genuino entre dois frameworks de valuacao independentemente
desenvolvidos que hoje nao compartilham ponte nenhuma.
**Teste revisado:** isolar SO o lema de ponte, desacoplado de
`HasGoodReduction`/teoria de reducao inteiramente:
`valuation K (maximalIdeal (p.adicCompletionIntegers K)) (algebraMap x) < 1 ↔ x ∈ p.asIdeal`
para `x : 𝓞 K` nao-nulo, `p : HeightOneSpectrum (𝓞 K)`. **A mesma
ponte HeightOneSpectrum <-> valuacao/coaltura-1 de HG-1 -- ver
infraestrutura compartilhada abaixo.**

---

## 7. Sintese TOE (extensao interna do laboratorio — NAO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| TOE-4 | Formalizar politica de promocao de status epistemico do `TRANSITION_ATLAS` como relacao decidivel | SURVIVES | baixo |
| TOE-2 | Dividir `TOE-INTERFACE-001` em `TOE-INTERFACE-SKELETON-001` (remover dependencia de RH/NS) | SURVIVES | minimo (governanca) |
| TOE-1 | Instanciar `ActionCategory` do Mathlib sobre a acao finita de FOUND-SEMIGROUP-001 | SURVIVES | baixo |
| TOE-3 | Functor entre `ActionCategory` e uma categoria derivada de grafo funcional | NEEDS_NARROWING | moderado, **depende de TOE-1** |

**TOE-4 — SURVIVES.** `EpistemicStatus` (12 casos, `models.py:13-25`) e
`promotion_decision` (`promotion.py:6`) confirmados por leitura direta do
codigo Python. Reaproveita o padrao `Fintype`/`DecidableEq` ja funcionando
hoje em `TamesisLab/Foundations/Semigroups/Regime3.lean:29-49`. Auto-
avaliacao honesta do recon ("bookkeeping do laboratorio, nao fisica") --
teste barato como descrito, mas entrega pouco para
`TOE_CONVERGENCE_CRITERIA`.

**TOE-2 — SURVIVES.** `GLOBAL_DEPENDENCY_GRAPH.md:16` ("As setas sao
dependencias de infraestrutura... nao implicacoes matematicas") e
`RESEARCH_QUEUE.yaml:356-359` conferidos verbatim. Zero risco de conteudo
Mathlib; exercicio de papelada de sessao unica genuino.

**TOE-1 — SURVIVES.** `ActionCategory := (actionAsFunctor M X).Elements`
com `deriving Category` (`Action.lean:48-50`) generico sobre qualquer
`[Monoid M] [MulAction M X]`; `Shift3`/`Regime3` ja tem `Monoid`/`MulAction`
prontos (`Action.lean:31-34` do laboratorio). Precedente real dentro do
proprio Mathlib (`NielsenSchreier.lean:107` instancia `ActionCategory` em
dados concretos) reforca que a construcao genuinamente instancia limpo.
**Correcao ao teste:** `Fintype RegimeCat` NAO resolve automaticamente
via "instancia `Fintype Regime3` existente" como alegado -- `Functor.Elements`
e `def`, nao `abbrev`; precisa de `Fintype.ofEquiv` explicito (trivial, mas
nao gratis). Tambem os objetos de `ActionCategory` sao bijecao-com, nao
igualdade literal a, `Regime3` -- corrigir "objetos = regimes" para
"objetos em bijecao com regimes".

**TOE-3 — NEEDS_NARROWING.** `Full`/`Faithful`
(`Functor/FullyFaithful.lean:45,52`) conferem; arquivos de grafo funcional
do laboratorio existem como alegado. Mas `Faithful` e Prop sem instancia
`Decidable` generica -- "refutavel por `decide`" nao esta literalmente
disponivel, precisa de testemunha concreta manual. Mais substantivo: zero
estrutura de categoria existe hoje em `FunctionalGraphs/` -- construir a
categoria-alvo e trabalho novo nao-trivial, diferente do reuso puro de
TOE-1.
**Teste revisado:** restringir a duas instancias de `ActionCategory`
(ambas genericas, ambas ja mostradas funcionar via TOE-1): construir um
segundo `MulAction` de brinquedo (`Shift2`/`Regime2`) e um functor explicito
F entre as duas `ActionCategory`, provando nao-Faithful por testemunha
term-mode direta (duas fitas de morfismos distintos com mesma imagem sob
F.map), sem inventar categoria de grafo funcional nova.

---

## 8. Fundamentos Quanticos / Unificacao (extensao interna do laboratorio — NAO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| QF-2 | Impossibilidade em dimensao finita da CCR (argumento de traco) | SURVIVES | minimo |
| QF-3 | Dualidade de Gelfand como enunciado de correspondencia classico/quantico | SURVIVES | minimo |
| QF-1 | Tightness CHSH/Tsirelson (tupla explicita atingindo 2*sqrt(2)) | SURVIVES | baixo |
| QF-4 | Teorema de Ehrenfest para operadores auto-adjuntos limitados | NEEDS_NARROWING | baixo (teste isolado) |

**QF-2 — SURVIVES.** `trace_mul_comm` (`Trace.lean:103`), `trace_one`
(`Matrix/Trace.lean:146`), `trace_mul_comm` para `CommMagma`(:158),
`trace_smul`(:68), `trace_sub`(:132) todos conferidos com assinatura exata.
O esboco de prova (tr(XP-PX)=0 via `trace_mul_comm`; tr(c•1)=c*n via
`trace_one`+`trace_smul`; c*n=0 com n!=0 em caracteristica zero forca c=0)
mapeia limpo para essas lemas exatas -- prova Lean genuina de 4-6 linhas,
nao estimativa inflada. "Wielandt"/"Wintner"/"canonical commutation"
ausentes de Mathlib (unicos hits sao teoria de grupo nao relacionada) --
conteudo genuinamente novo. **O candidato mais forte deste lote inteiro:
pequeno, autocontido, citado corretamente, e um fato estrutural genuino
(ainda que modesto).**

**QF-3 — SURVIVES.** Linguagem do doc-comment de `VonNeumannAlgebra`
("ainda temos um projeto grande pela frente para mostrar a equivalencia
entre essas definicoes") e match exato, nao paratrase. Achado adicional:
`gelfandTransform_map_star` (`GelfandDuality.lean:137`) ja esta no arquivo
-- torna o teste proposto (auto-adjunto -> funcao invariante-por-star, i.e.
real) ainda mais trivialmente verdadeiro do que o recon previu,
essencialmente ja um corolario de uma linha. Auto-avaliacao do recon
(custo baixo, plausibilidade baixa em termos de contribuicao substantiva)
nao esta inflada.

**QF-1 — SURVIVES.** `IsCHSHTuple` (`CHSH.lean:88-100`),
`CHSH_inequality_of_comm` (:115-132), `tsirelson_inequality` (:164-199)
lidos por inteiro; secao `## Future work` (:60-67) confirma que a
construcao de tightness/matriz 4x4 explicita e genuinamente TODO em
aberto, nao gap fabricado. `instStarOrderedRing` para `CStarMatrix n n A`
confirmado (`CStarMatrix.lean:807`). Infraestrutura de autovalor/autovetor
existe para tornar "exibir autovetor explicito v com
(A0B0+A0B1+A1B0-A1B1)v = 2*sqrt(2)*v" uma tarefa limitada e genuinamente
pequena.

**QF-4 — NEEDS_NARROWING.** Ausencias (`Ehrenfest`, `Schrodinger`, `WKB`,
`StoneVonNeumann`) reconfirmadas por grep amplo -- genuinamente ausente.
Mas `MatrixExponential.lean` tem **zero** lemas de derivada especificos
para `Matrix.exp` (nenhum `HasDerivAt`/`HasFDerivAt`); a ferramenta
correta e `hasFDerivAt_exp_smul_const_of_mem_ball` (para escalar
comutativo, algebra possivelmente nao-comutativa), mas recuperar a
identidade completa de Ehrenfest no quadro de Heisenberg exige compor com
regra do produto de 3 fatores, fatos de comutacao, e derivada adicional do
valor esperado sesquilinear -- montagem de multiplos passos, nao busca de
uma lema.
**Teste revisado:** isolar SO a instanciacao de
`hasFDerivAt_exp_smul_const_of_mem_ball` para um H anti-Hermitiano 2x2 ou
3x3 fixo, confirmando que compila sem atrito na hipotese de raio de
convergencia (algebras matriciais de dimensao finita deveriam ter raio
infinito -- confirmar que isso compila em vez de assumir). So se essa
instanciacao isolada for limpa vale comprometer com a derivacao completa
de Ehrenfest de 3 fatores como tarefa maior separada.

---

## Infraestrutura compartilhada entre frentes

Tres pecas de infraestrutura aparecem como dependencia (bloqueante ou
facilitadora) de **mais de uma frente**. Construir cada uma uma vez e
reaproveitar rende mais do que resolver caso a caso.

```text
(A) Toolkit de espectro/traco em dimensao finita para operadores
    auto-adjuntos/Hermitianos compactos
    -- aparece em: RH (RH-3, RH-4), Yang-Mills (YM-1, YM-2, YM-3),
       Fundamentos Quanticos (QF-2)
    -- pecas comuns: Matrix.IsHermitian.eigenvalues / trace_mul_comm /
       norm_eq_iSup_rayleighQuotient / hasEigenvalue_iSup_of_finiteDimensional
    -- se as 6 sondas de wave 1 relacionadas fecharem limpo, vale
       consolidar um arquivo interno de lemas-ponte (numerico <-> API
       abstrata de autovalor) reusavel pelas 3 frentes, em vez de cada
       linha reinventar sua propria travessia charpoly<->eigenvalues.

(B) Ponte entre HeightOneSpectrum/valuacao-adica de dominio de Dedekind
    e pontos de coaltura-1 de um Scheme / fatoracao de ideal global
    -- aparece em: BSD (BSD-1, BSD-2), Hodge (HG-1)
    -- hoje: zero lema liga HeightOneSpectrum a coaltura-1 de Scheme;
       zero lema liga a construcao de completacao uniforme
       (Valued.v.integer/adicCompletionIntegers) a construcao de
       completacao de modulo (AdicCompletion (maximalIdeal R) R)
    -- ESTA e a peca de maior alavancagem do lote inteiro: se
       construida uma vez, desbloqueia potencialmente BSD-1, BSD-2 e HG-1
       simultaneamente. Candidata natural para wave 3.

(C) Padrao de bound de crescimento (IsBigO) -> convergencia de LSeries
    para funcoes-L aritmeticas
    -- aparece em: RH (RH-5), BSD (BSD-3)
    -- a maquinaria generica (LSeriesSummable_of_isBigO_rpow /
       _of_le_const_mul_rpow) ja existe e e reutilizavel; o trabalho
       especifico de cada linha e so provar o bound de coeficiente de
       Dirichlet do objeto especifico (zeta vs. L de curva eliptica) e
       alimentar na mesma maquinaria generica -- vale documentar o padrao
       uma vez para as duas linhas usarem.
```

---

## Ordem de execucao em ondas

Pensado para despacho paralelo entre agentes de formalizacao. Onda 1 =
testes independentes entre si, sem pre-requisito de outro teste deste
lote. Onda 2 = depende do fechamento de itens especificos da onda 1. Onda 3
= integracao e infraestrutura compartilhada, contingente aos achados das
ondas 1-2.

### Onda 1 — despachar em paralelo agora, zero dependencia cruzada

```text
RH-1  (sub-lema isolado log(T/2pi)/log T -> 1)
RH-2  (riemannZetaZeros -> finitude de N_zeta(T) num retangulo)
RH-3  (operador diagonal em l^2, versao revisada)
RH-4  (eigCount, direcao corrigida: nhdsWithin 0)
RH-5  (bound trivial |zeta(sigma+it)|=O(1) para sigma>1 fixo)

NS-1  (HasLocalPV, 4 passos revisados, com sub-lema de escala de raio)
NS-3  (ZMod 4 DFT, versao revisada barata)

PN-1  (Language.P via Nonempty; declarar Language.NP sem provar)
PN-3  (segunda testemunha: negacao booleana)
PN-4  (sonda RecursiveIn/TuringDegree)

YM-1  (gap 2x2 via discriminante, nlinarith, bypass da API abstrata)
YM-2  (instancia IsPrimitive concreta 3x3 + dominancia de autovalor)
YM-3  (estabilidade do gap 2-dim sob convergencia em norma)

HG-1  (ponte divisor-principal via Ideal.finite_factors, sonda)
HG-2  (especializar ClassGroup.equivPic a 𝓞K de corpo de numeros)
HG-4  (statability de compatibilidade holomorfa em total space de brinquedo)

BSD-1 (lema isolado: Finite (ResidueField (adicCompletionIntegers)))
BSD-2 (lema isolado: ponte valuacao-local <-> pertence-ao-ideal)
BSD-3 (nucleo aritmetico desacoplado: bound |c_n| <= (n+1)*q^(n/2))
BSD-4 (leitura/escrita: lista de gaps de Mordell-Weil, sem codigo)

TOE-1 (ActionCategory sobre Shift3/Regime3, com Fintype.ofEquiv corrigido)
TOE-2 (split TOE-INTERFACE-SKELETON-001, papelada)
TOE-4 (porte de EpistemicStatus para Fintype/DecidableEq)

QF-1  (autovetor explicito CHSH atingindo 2*sqrt(2))
QF-2  (impossibilidade CCR em dimensao finita, argumento de traco)
QF-3  (auto-adjunto -> invariante-por-star via Gelfand)
QF-4  (instanciacao isolada de hasFDerivAt_exp_smul_const_of_mem_ball)
```

### Onda 2 — dispara apos onda 1 fechar os pre-requisitos nomeados

```text
RH:   compor o limite completo do quociente de RVM-LIMIT
        (depende de RH-1 fechar)

NS-2: construir T como elemento de Distribution/TemperedDistribution
        (depende de NS-1 fechar -- integrabilidade absoluta e o insumo)

PN-2: composicao id+negacao ao nivel de tipo para TM2ComputableInPolyTime.comp
        (depende de PN-3 fechar -- reusa a testemunha de negacao construida)

YM:   tentar conectar o gap 2x2 numerico de volta a API abstrata
        IsHermitian.eigenvalues via eigenvalues_eq/charpoly_eq (meta estica,
        depende de YM-1 fechar)

BSD:  IsMultiplicative(LFunction) completo
        (depende de BSD-1 wave-1 fechar)
BSD:  finitude do lugar de reducao ruim completa
        (depende de BSD-2 wave-1 fechar)

TOE-3: functor entre duas instancias de ActionCategory (Shift3/Regime3 e
        Shift2/Regime2 de brinquedo)
        (depende de TOE-1 fechar)
```

### Onda 3 — integracao e infraestrutura compartilhada, contingente

```text
(B) Ponte HeightOneSpectrum <-> coaltura-1/fatoracao-de-ideal global
      -- construir SE HG-1 e/ou BSD-1/BSD-2 da onda 1-2 revelarem que essa
         identificacao e o gargalo real (resultado provavel, nao garantido)
      -- se construida, retestar HG-1, BSD-1, BSD-2 sobre ela

BSD-3 integracao final: cablear o nucleo aritmetico (onda 1) + resultado
      de multiplicatividade (onda 2, se BSD-1 fechar) na declaracao real
      de meio-plano de convergencia condicional de WeierstrassCurve.LSeries

NS integracao final: construir a distribuicao temperada completa do nucleo
      CZ combinando NS-1 (onda 1) + NS-2 (onda 2)

(A) Avaliar consolidar toolkit compartilhado de espectro/traco em dimensao
    finita SE as 6 sondas relacionadas (RH-3, RH-4, YM-1, YM-2, YM-3, QF-2)
    fecharem limpo nas ondas 1-2
```

---

## Descartados nesta rodada (nao reabrir sem evidencia nova)

```text
PN-5  Teorema de Fagin / complexidade descritiva via ModelTheory
        -- zero scaffold reaproveitavel; custo very_high admitido pelo
           proprio recon; nao e "angulo subvalorizado", e beco confirmado

YM-4  Teoria de representacao de grupo de Lie compacto, rota SU(2)->SU(N)
        -- Peter-Weyl tem zero presenca em todo o Mathlib (nem stub);
           perseguir exigiria construir subcampo inteiro do zero

HG-3  Trivialidade codim-1=top-codim via homologia singular
        -- resultado previsto como falha pelo proprio autor antes do teste;
           nao e hipotese viva, e ausencia pre-concedida
```

---

## Onde nenhum candidato sobreviveu

Nenhuma das 8 frentes ficou com zero candidatos `SURVIVES`/
`NEEDS_NARROWING` -- mas vale registrar explicitamente que **3 dos 21
candidatos revisados foram REFUTED** (PN-5, YM-4, HG-3), um por linha em 3
frentes diferentes (P vs NP, Yang-Mills, Hodge). Isso nao e falha do
processo: e exatamente o tipo de descarte barato que a revisao adversarial
deveria produzir, e evita que essas 3 rotas sejam re-propostas do zero em
ciclos futuros sem essa memoria.

---

## Avaliacao pessoal — os 2-3 candidatos com maior chance de virar
resultado formal honesto e nao-trivial mais cedo

Nao e uma repeticao da autoavaliacao dos agentes de recon -- e um
julgamento proprio depois de ler as 21 verificacoes adversariais inteiras.

**1. QF-2 (impossibilidade em dimensao finita da CCR, argumento de
traco).** E o candidato mais limpo do lote inteiro: toda citacao Mathlib
foi lida por inteiro e confere exatamente; o esboco de prova mapeia lema-
por-lema para ferramentas ja existentes (`trace_mul_comm`, `trace_one`,
`trace_smul`, `trace_sub`); e genuinamente 4-6 linhas; nao depende de
nenhum outro candidato deste lote; e nao ha ambiguidade de direcao,
tipagem ou escala como em varios outros candidatos "SURVIVES" desta
rodada. E tambem um fato matematico real (nao trivial de se ver a olho nu
sem o argumento de traco) que distingue representacoes limitadas/finitas
da forca infinito-dimensional imposta pela CCR -- um resultado honesto,
pequeno, e citavel por si.

**2. RH-2 (conectar `riemannZetaZeros` a finitude de N_zeta(T) num
retangulo).** Diferente da maioria dos candidatos aqui, este nao e so "um
lema pequeno" -- e a conexao de uma peca de infraestrutura Mathlib
genuinamente recente (checkout de 2026-07-16, fora do que qualquer modelo
teria memorizado em treino) a um objeto central da linha RH
(N_zeta(T)) que hoje esta comprovadamente desconectado. Toda a cadeia de
dependencia (compacidade de retangulo em C, Heine-Borel, ProperSpace)
foi verificada peca por peca, nao so a lema final. O risco tecnico
residual e baixo e o valor de infraestrutura e real: e o tipo de resultado
que abre trabalho futuro na linha, nao so fecha uma caixa isolada.

**3. QF-1 (tightness CHSH/Tsirelson, tupla explicita 2*sqrt(2)).**
Diferente de QF-2, este tem um ingrediente de risco genuino (exibir o
autovetor certo e verificar `IsCHSHTuple` para as matrizes de Pauli pode
esbarrar em atrito de `simp`/`Fin.sum_univ`), mas o alvo e um TODO
explicito e documentado dentro do proprio Mathlib (`## Future work`,
`CHSH.lean:60-67`), nao uma lacuna inventada pelo laboratorio -- fechar
esse teste teria valor fora do laboratorio tambem, nao so como marco
interno. Coloco na terceira posicao, nao na primeira, precisamente por
esse atrito residual de calculo explicito ser real e nao totalmente
eliminavel por reescopo, diferente de QF-2 e RH-2.

Nao incluo nenhum candidato BSD ou Hodge no top 3: todos os que sobrevivem
la carregam uma dependencia de ponte ainda nao verificada existir
(HeightOneSpectrum <-> coaltura-1, ou corpo-de-residuo-de-completacao-adica)
como pre-condicao real para o resultado completo, mesmo que a sub-sonda
isolada de wave 1 seja barata -- o resultado final "honesto e nao-trivial"
nessas duas frentes esta, no melhor caso, a duas ondas de distancia, nao
uma.
