---
document_id: PLANO-ATAQUE-ONDA-3-2026-08-10
reviewed_at: 2026-08-10
input: recon + revisao adversarial de 9 grupos (8 linhas de pesquisa + infraestrutura compartilhada) para Onda 3, ancorado nos resultados reais da Onda 2 -- ver 09_SESSIONS/2026/2026-08-10_WAVE2_EXECUTION.md (20/20 fechados, 0 gaps, 0 rejeitados) e 01_PORTFOLIO/PLANO_DE_ATAQUE_PORTFOLIO_COMPLETO_2026_08_09.md e 01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md
conclusion: PLANO_DE_EXECUCAO_ONDA_3_PROPOSTO
---

# Plano de ataque — Onda 3 (continuacao das Ondas 1-2)

## Enquadramento honesto

Este documento e a continuacao direta de
`PLANO_DE_ATAQUE_PORTFOLIO_COMPLETO_2026_08_09.md`,
`PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md` e da sessao de execucao
`2026-08-10_WAVE2_EXECUTION.md`. A Onda 2 fechou **20 de 20** itens (18
VERIFIED, 2 VERIFIED_WITH_NOTES), com **zero** gap diagnosticado e
**zero** item rejeitado -- melhor taxa de fechamento que a Onda 1
(25/27), com recompilacao independente confirmada (20/20 exit 0, zero
`sorryAx`, zero token proibido, `lake build` central sem regressao,
8825 jobs identicos a antes). A Onda 3 parte desse chao real, nao de
aspiracao.

```text
O que este plano E:
  - a proxima rodada de pequenos testes falsificaveis contra
    infraestrutura Mathlib genuina, construida sobre os 20 itens
    fechados na Onda 2 (e, por heranca, sobre os 25 da Onda 1)
  - uma tentativa de re-verificar, por leitura direta de arquivo (nao por
    confianca no agente de recon), se os passos originalmente previstos
    para "depois da Onda 2" continuam abertos, ja foram satisfeitos por
    acaso, ou ficaram obsoletos por descoberta nova
  - honesto sobre candidatos REFUTED, sobre linhas/sub-frentes sem alvo
    pequeno disponivel nesta rodada, e sobre onde um teste proposto tinha
    um defeito de tipagem ou matematico real, nao so cosmetico

O que este plano NAO E:
  - uma alegacao de que qualquer Problema do Milenio ficou mais proximo
    de ser resolvido -- nenhum item abaixo toca o nucleo central de
    nenhuma das 6 frentes Clay-oficiais
  - uma alegacao de que TOE-INTERFACE-001 ou QCU-001 tem status
    Clay-oficial
  - uma reabertura do RH-NOGO-001: o item RH desta onda continua vivendo
    na camada abstrata "reutilizavel fora desta frente" do freeze, nao na
    camada concreta congelada
  - uma promessa de que todo teste "SURVIVES" fecha sem sorry -- e uma
    aposta informada, nao uma certeza
  - uma tentativa de inflar a contagem de itens: onde a revisao
    adversarial confirmou que uma sub-frente nao tem alvo pequeno
    disponivel (ex.: RH/RVM-NZeta, NS-3b, HG-1b/HG-2), isso e reportado
    como resultado honesto, nao contornado com busywork
```

Cada candidato abaixo passou por reverificacao independente de citacao
Mathlib (leitura direta de arquivo no checkout vendorizado, nao
grep-e-confia) e, em varios casos, por releitura integral dos proprios
arquivos-fonte da Onda 1/Onda 2 citados como base. Veredito: `SURVIVES`
(teste proposto se sustenta como esta), `NEEDS_NARROWING` (angulo real,
mas o teste proposto precisou ser reescrito para ser genuinamente
pequeno/correto), ou `REFUTED` (nao vale investir).

18 candidatos revisados ao todo nos 9 grupos: **15** `SURVIVES`/
`NEEDS_NARROWING` que rendem item de execucao, **1** `REFUTED`, e
**2** candidatos honestamente auto-excluidos (0 candidatos genuinos
encontrados, ou escopo grande demais para esta rodada) que nao entram na
lista numerada. A contagem final de itens de execucao (15) e menor que
os 20 da Onda 2 -- resultado esperado e reportado sem ajuste: varias
sub-frentes (RH/RVM-NZeta, NS full-distribution, HG Pic/ClassGroup)
estao genuinamente exauridas de pequenos passos nesta rodada.

---

## 1. Riemann Hypothesis (RH) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| RH-3 | Lei de contagem `unboundedEigCount(Lam) = floor(Lam)+1` para `Tp` de brinquedo, via `eigenvalue_bridge` + `eigCount_eq_floor` | SURVIVES | baixo-moderado |
| — | Composicao NZeta (WAVE2-RH-2) com formula-limite RVM (WAVE2-RH-1) | 0 candidatos (confirmado) | — |

**Passo original vs. o que mudou.** O candidato 1 e continuacao direta e
genuina da dupla `eigenvalue_bridge`/`eigCount_eq_floor` fechada na Onda
2 (`LinearPMapEigenvalueBridge.lean`, `SpectralCountingInstance.lean`).
O segundo item nao e um candidato proposto, e uma verificacao
independente do proprio veredito "0 candidatos" do recon para a
composicao NZeta/RVM -- confirmada correta.

**RH-3 — SURVIVES.** `eigenvalue_bridge` (`LinearPMapEigenvalueBridge.lean:279-300`,
`IsEigenvalue Tp mu <-> Module.End.HasEigenvalue (T : Module.End C H2)
(mu+1)^-1`, incondicional, auditado por `#print axioms` so com os 3
axiomas padrao) e `eigCount_eq_floor` (`SpectralCountingInstance.lean:346-349`,
`eigCount T lam = floor(1/lam)` para `0 < lam`, tambem auditado)
conferem ambos exatos. `SpectralCountingLimit.lean` (linhas 53-57)
confirma verbatim que a inversao espectral fica como "lacuna explicita
para trabalho futuro" -- exatamente o que este item fecha. Grep em
`Mathlib/LinearAlgebra/LinearPMap.lean` e
`Mathlib/Analysis/InnerProductSpace/LinearPMap.lean` confirma zero hits
para `HasEigenvalue`/`eigenvalue`: nao ha atalho Mathlib, o predicado
`IsEigenvalue` ad hoc do laboratorio e o unico veiculo. `Set.ncard_image_of_injective`
(`Data/Set/Card.lean:829`) e os lemas de `Nat.floor` necessarios
existem e ja foram usados com sucesso neste mesmo arquivo
(`eigCount_two`). Uma ressalva real, que estreita a ESTRATEGIA sem
invalidar o alvo: o proprio arquivo `SHARED-2C` (Onda 2) ja mostra
`Tp_isEigenvalue`/`Tp_eigenvalue_mem_range` caracterizando `IsEigenvalue
Tp mu` diretamente como `{mu = (n:C) : n in N}`, sem passar pela ponte ou
por `eigCount` -- entao existe uma rota MAIS SIMPLES (bijecao direta via
`Nat.cast` e `Set.ncard`) que nao precisa de nenhum dos dois lemas
citados. A rota via `eigenvalue_bridge`/`eigCount_eq_floor` tambem fecha
(verificado a mao: autovalores de `R` sao `1/(i+1)`, e `|nu| >= lam =
(Lam+1)^-1 <-> i <= Lam`, batendo com a enumeracao direta), mas exige um
passo extra de transporte de desigualdade nao mencionado como tal no
candidato original.
**Teste revisado:** manter o enunciado `unboundedEigCount Lam =
Nat.floor Lam + 1` para `0 <= Lam` exatamente como proposto, mas nao
exigir a rota `eigenvalue_bridge`/`eigCount_eq_floor` como unica valida;
uma prova direta via `Tp_isEigenvalue`+`Tp_eigenvalue_mem_range`
(bijetando o conjunto de autovalores com `{n : N | n <= Lam}` via
`Nat.cast`) e igualmente valida e mais simples -- aceitar qualquer uma.
Se a sessao escolher a rota da ponte (para genuinamente exercitar as duas
pecas da Onda 2 citadas), exigir que o passo intermediario de transporte
de desigualdade (`Complex.abs mu <= Lam <-> lam <= Complex.abs ((mu+1)^-1)`
em `lam=(Lam+1)^-1`) seja provado como lema nomeado explicito, nao
escondido. `#print axioms` deve mostrar so os 3 axiomas padrao.

**Composicao NZeta/RVM-limit — 0 candidatos, confirmado.**
`RVMLimitErrorComposition.lean` opera sobre uma funcao ABSTRATA `e : R ->
R` com `e =O(log T)` -- nao ha `riemannZeta` nem `N_zeta` no arquivo, e o
proprio header nomeia a conexao com o termo de erro real como SB-GAP-010B,
fora de escopo. `ZetaZerosCountingMonotoneVanishing.lean` prova `NZeta`
genuina sobre zeros reais de `riemannZeta`, mas so monotonicidade e
`NZeta(T<=0)=0` -- sem taxa de crescimento, e seu proprio header desconecta
explicitamente da maquinaria RVM-limit. Grep independente em
`Mathlib/NumberTheory/LSeries/ZetaZeros.lean` confirma que so oferece
fechamento/discretude/finitude-em-compactos -- nenhum teorema de
assintotica de contagem que permitisse uma ponte pequena sem formalizar o
argumento classico de Riemann-von Mangoldt (o nucleo matematico duro que
SB-GAP-010B ja nomeia). Nenhuma ponte pequena alternativa foi encontrada.
**Nenhum teste proposto.** Confirma-se o proprio veredito do recon: forcar
um alvo aqui exigiria reprovar a formula classica de contagem de zeros do
zero (nao pequeno, fora da estrategia do laboratorio) ou fabricar
busywork sem conteudo. Se um passo genuinamente pequeno aparecer no
futuro, a unica forma defensavel seria um corolario CONDICIONAL
explicitamente rotulado -- mas mesmo esse atalho exigiria primeiro provar
que `NZeta` e igual a `symbolicFormula + erro` com erro `O(log T)`, que e
exatamente a lacuna ja disparada (SB-GAP-010B). Veredito de 0 candidatos
mantido.

---

## 2. Navier-Stokes (NS) — Clay oficial (nucleo Calderon-Zygmund)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| NS-3a | Consistencia de raio (R-independencia) do valor p.v. local contra funcao-teste Lipschitz/suporte compacto | NEEDS_NARROWING | baixo-moderado |
| NS-3b | Distribuicao p.v. global `pvK` em `D'^1(E,R)` via `TestFunction.mkCLM`/`limitCLM` sobre TODOS os compactos | SURVIVES (nao proposta -- corretamente adiada) | very_high |

**Passo original vs. o que mudou.** NS-3a e continuacao direta e
correta do gap (i) explicitamente nomeado por `PVDistributionOnCompactK.lean`
(NS-2b da Onda 2). NS-3b nao e um candidato proposto para esta onda, e
uma analise honesta de "por que nao tentar isso na Onda 3" -- confirmada
correta apos reverificacao independente.

**NS-3a — NEEDS_NARROWING.** Releitura integral de
`K_LipschitzDifference_HasLocalPV.lean` (1111 linhas) e
`PVDistributionOnCompactK.lean` (1266 linhas) confirma toda citacao do
candidato: `K_shell_integral_eq_zero` (linhas 518-702, integral de `K`
sobre `{a<||y||<=b}` e 0 para `0<a<b`), reusado verbatim em
`PVDistributionOnCompactK.lean:490-665`; `hasLocalPV_K_mul_lipschitz`
(linhas 897-968) prova `HasLocalPV (K*g) 0 R L'` para QUALQUER
`LipschitzWith g`, ja reusado por `pvKLM` (linhas 953-1027). O header de
`PVDistributionOnCompactK.lean` (linhas 29-39, 1118-1136) nomeia
literalmente o gap (i) -- R-independencia via `K_shell_integral_eq_zero`
para dois raios -- como a peca faltante, e enquadra a hipotese necessaria
como "suporte ESTRITAMENTE dentro de `closedBall 0 R`" (a funcao-teste se
ANULA fora de `R1`). `ContDiffMapSupportedIn.support_subset`/`tsupport_subset`
(linhas 265/268), `monoLM`/`monoCLM` (linhas 339-372/796-827),
`Compacts`-como-subconjunto (`Topology/Sets/Compacts.lean:45,49`) e
`MeasureTheory.setIntegral_union` (`Integral/Bochner/Set.lean:87`, ja
importado por ambos os arquivos) conferem todos exatos. Porem, a
hipotese concreta proposta no teste falsificavel esta ERRADA e torna o
teste trivial: como escrito, exige `g y = g 0` (constante) fora de
`R1`, o que zera `g y - g 0` identicamente na casca e fecha por
`integral_zero`/`integral_congr_ae` puro, SEM tocar
`K_shell_integral_eq_zero` -- contradizendo a propria justificativa do
candidato ("a casca contribui exatamente `-g(0) * integral de K sobre a
casca`"), que so vale se `g` se ANULA (nao "e igual a g(0)") fora de
`R1`, como uma funcao-teste de suporte compacto real.
**Teste revisado:** substituir a hipotese por anulamento genuino (ou uma
constante arbitraria `c` fora do suporte, generalizacao que inclui
anulamento como caso `c=0`): para `g : E -> R`, `L c : R`,
`hg : LipschitzWith L.toNNReal g`, `R1 R2 : R` com `0 < R1 < R2`,
`hsupp : forall y, R1 < ||y|| -> g y = c`, provar
`(integral sobre closedBall 0 R1 \ {0} de K*(g-g0)) = (integral sobre
closedBall 0 R2 \ {0} de K*(g-g0))`. Prova: dividir
`closedBall 0 R2 \ {0} = (closedBall 0 R1 \ {0}) union (casca R1..R2)`
via `setIntegral_union` (disjuntos, mensuraveis, integraveis via
`K_diff_integrableOn_closedBall_lipschitz.mono_set`); na casca o
integrando e `K*(c-g0)`, CONSTANTE vezes `K`, entao sua integral e
`(c-g0) * (integral de K na casca) = (c-g0)*0 = 0` por
`K_shell_integral_eq_zero` em `(R1,R2)`. Isso genuinamente forca o uso
de `K_shell_integral_eq_zero` (ao contrario da versao como proposta) e e
o degrau correto rumo ao corolario em nivel de
`ContDiffMapSupportedIn`/`monoCLM` que o gap (i) realmente precisa.

**NS-3b — nao proposta, corretamente adiada.** `TestFunction.mkCLM`
(`Distribution/TestFunction.lean:353`) e `limitCLM` (linha 370) confirmam
exatamente a hipotese `cont` exigida (continuidade para CADA compacto
`K`, nao exaustao contavel), mais as hipoteses de `toFun_eq_T` e a pilha
de typeclasses `[Algebra R k][IsScalarTower R k F][Module k V]
[IsScalarTower R k V]`. `ContDiffMapSupportedIn.monoCLM` (:796-827),
`CompactExhaustion` (`Topology/Compactness/SigmaCompact.lean:321`) e
`IsCompact.isBounded` (`MetricSpace/Bounded.lean:192`) sao ferramentas
genericas confirmadas, corretamente descritas como suporte, nao atalho.
A cadeia de dependencia (gap (i) = NS-3a, depois gap (ii) = bola para `K'`
arbitrario via `monoCLM`+`isBounded`, depois `toFun_eq_T`/typeclasses de
`limitCLM`) e materialmente maior que um unico item de onda, e nao e
decomponivel em unidade falsificavel pequena sem NS-3a primeiro.
**Nenhum teste proposto nesta onda.** Decisao correta de nao entrar na
lista de execucao; retomar apenas depois de NS-3a fechado, e ainda assim
provavelmente como item de duas ou mais sub-etapas em ondas futuras.

---

## 3. P vs NP (PN) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| PN-6 | Testemunha de fronteira de passo dependente de dado (goto com alvo nao-constante) | SURVIVES | baixo |
| PN-7 | Testemunha de cobertura de `branch`/`cond` | SURVIVES | baixo |

**Passo original vs. o que mudou.** Ambos sao continuacao direta do
padrao ja estabelecido por `PN2PRIME`/`PN5` da Onda 2 (`goto` de alvo
constante, obstaculo de dupla-negacao `Bool.not` documentado
honestamente). O terceiro candidato aventado pelo recon (extensao
mecanica de goto de 3 labels) foi corretamente excluido como busywork de
baixa informacao -- confirmado independentemente, nao entra na lista.

**PN-6 — SURVIVES.** `Stmt` (`StackTuringMachine.lean:127-134,161-173`)
e `Computable.lean` (`outputsFun`/`proof_wanted`) conferem exatos por
leitura direta, sem fabricacao encontrada. `PN2PRIME` e `PN5`
reconfirmados por leitura integral: o alvo de `goto` e literalmente
constante (`fun _ => true`), o obstaculo `Bool.not`/dupla-negacao e real
e honestamente documentado, `branch`/`peek` confirmados zero-instanciados
por grep independente. A alegacao "mesma classe de obstaculo que
`Bool.not`" foi verificada contra `PN3` (que tambem aplica `Bool.not` a
um bit simbolico mas fecha por `rfl` puro, porque o valor so e carregado
adiante, nunca forca um `match` a disparar): `PN-6`/`PN-7` sao um caso
genuinamente diferente e mais dificil -- dado alimentando um DESPACHO
(match de label `Lambda` ou `cond`) que nao pode iota-reduzir sem o
escrutinio ser um construtor literal. A previsao tecnica ("goto
data-dependente trava sob `rfl` puro para entrada simbolica") e
estruturalmente fundamentada, nao especulacao.
**Teste revisado:** mesma construcao proposta, mas comprometer-se de
antemao com a tatica de fallback `by cases b <;> rfl` (ou `rcases b`) em
vez de deixar "cases ou decide" em aberto -- `decide` dificilmente
type-checa direto contra um objetivo de igualdade `TM2OutputsInTime`/`Cfg`
sem antes desdobrar `stepAux`/`step`, entao nao e rota de fallback
independente aqui.

**PN-7 — SURVIVES.** Grep confirma que `branch` e `peek` nao sao usados
em nenhum arquivo PN fora de duas linhas de comentario (`PN2PRIME:43`,
`PN5:36`) -- alegacao de gap de cobertura precisa, nao inflada. `cond`
confirmado como primitivo do nucleo Lean4 (`Init/Prelude.lean:1164`), nao
lema Mathlib, batendo exato com a citacao. Previsao tecnica valida pelo
mesmo argumento de PN-6: `cond(f v, ...)` nao iota-reduz para `f v`
simbolico, `stepAux` genuinamente trava sem case split. Porem este e
mecanicamente O MESMO obstaculo de PN-6 (termo `Bool` bloqueando um
match, um passo antes -- dentro de `cond` de `stepAux` em vez do
despacho `M l` de `step`), entao seu valor marginal apos PN-6 e baixo:
item legitimo mas majoritariamente confirmatorio.
**Teste revisado:** manter como proposto, mas sequenciar apos PN-6 (ou
rodar so se PN-6 surpreender, ex.: fechar por `rfl` sem `cases`), e
enquadrar explicitamente no relatorio como cobertura confirmatoria do
unico construtor `Stmt` ainda nao testado, nao como segundo teste
independente do mesmo mecanismo.

---

## 4. Yang-Mills (YM) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| YM-STABILITY-COMPOSE | Encadear Lipschitz direto + norma de operador (`lambdaMax`/`lambda2` sobre `M1`,`M2` de brinquedo) | SURVIVES | baixo |
| YM-STABILITY-GROUNDED | Identificar `lambdaMax(toEuclideanCLM M2) = 3`, conectando ao espectro `{1,3}` do YM-1-Connect | SURVIVES | baixo (corrigido de moderado) |

**Passo original vs. o que mudou.** Ambos sao continuacao direta dos
tres itens fechados na Onda 2 (`L2OperatorNormProbe.lean`,
`FixedDimEigenvalueStability.lean`, `SecondEigenvalueLipschitz.lean`,
`FiniteLatticeTransferGap.lean`/`YM-1-Connect`). O segundo candidato
tinha uma alegacao de "confirmado ausente" no Mathlib que se revelou
FALSA na reverificacao -- tornando o item mais barato, nao mais caro, do
que o proprio candidato avaliou.

**YM-STABILITY-COMPOSE — SURVIVES.** Releitura integral dos tres
arquivos-fonte confirma: `lambdaMax_lipschitz` (:157-158) e
`lambda2_lipschitz` (:275-276) tomam `A B : E →L[R] E` arbitrarios, sem
hipotese extra, sobre `E := EuclideanSpace R (Fin 2)` (mesmo tipo
subjacente nas tres declaracoes independentes, `abbrev` reduzivel =
defeq genuina). `M2` em `L2OperatorNormProbe.lean:142` e byte-identico ao
`M` de `TransferGapSpectrumCharpoly.lean`/YM1. `sonda1_bridge` (:163-167)
prova `‖toEuclideanCLM M1 - toEuclideanCLM M2‖ = ‖M1-M2‖` diretamente, e
`sonda2_numeric_norm` (:198) prova `‖M1-M2‖ = 1/10` exato. `Matrix.
toEuclideanCLM` (:102), `l2_opNorm_toEuclideanCLM` (:228),
`l2_opNorm_diagonal` (:232) conferem todos na posicao citada. A cadeia
composta `(lambdaMax_lipschitz _ _).trans (by rw [sonda1_bridge]; exact
sonda2_numeric_norm.le)` e mecanicamente solida e nao exige nenhuma
citacao Mathlib nova -- e recombinacao pura de tres pecas ja
type-checadas, seguindo a convencao de reproducao verbatim ja
estabelecida no laboratorio. Mesmo argumento fecha `lambda2_lipschitz`
em `3/10`. `still_missing_if_success` honesto: continua sobre uma unica
matriz 2x2 de brinquedo com uma perturbacao fixa, nada sobre SU(N)/rede/
positividade de reflexao/limite continuo -- YM-3 e explicitamente o caso
conversor a dimensao fixa, nao generaliza.
**Teste revisado:** como proposto, sem alteracao: um arquivo novo
autonomo reproduzindo verbatim `E`, `lambdaMax`, `lambdaMax_lipschitz`,
`lambda2`, `lambda2_lipschitz` mais `M1`, `M2`, `sonda1_bridge`,
`sonda2_numeric_norm`, depois os dois corolarios compostos com bounds
`1/10` e `3/10`. Unico modo de falha plausivel: mismatch de unificacao
entre os `abbrev E` reproduzidos independentemente (improvavel dado
reducibilidade).

**YM-STABILITY-GROUNDED — SURVIVES.** Citacoes confirmadas exatas:
`StarAlgEquiv.toAlgEquiv` (`Algebra/Star/StarAlgHom.lean:829`),
instancia generica `AlgEquivClass`-de-`NonUnitalAlgEquivClass` (:662-663)
mais a instancia `NonUnitalAlgEquivClass` para `A ≃⋆ₐ[R] B` (:704),
`AlgEquiv.spectrum_eq` (`Algebra/Spectrum/Basic.lean:431`) e
`M_eigen_three` (`FiniteLatticeTransferGap.lean:161`,
`M.mulVec ![1,1] = 3 • ![1,1]`) -- todos conferem. Porem a alegacao
central "CONFIRMADO AUSENTE" (a ponte de espectro `CLM`-vs-`LinearMap`)
esta ERRADA: grep proprio por `spectrum.*ContinuousLinearMap` encontrou
`ContinuousLinearMap.spectrum_eq`
(`Analysis/Normed/Operator/Banach.lean:483-486`,
`spectrum K f = spectrum K (f : Module.End K E)` sob `[CompleteSpace E]`)
-- exatamente a ponte que faltava. `CompleteSpace (EuclideanSpace R (Fin
2))` vem de graca via `FiniteDimensional.complete`
(`Normed/Module/FiniteDimension.lean:32`). O motivo do candidato nao ter
achado: os padroes de busca usados (`toLinearMap`/`coe`) nao batem com o
nome real do lema. Isso torna o item mais barato e mais plausivel do que
a propria autoavaliacao do candidato (custo/plausibilidade deveriam ser
baixo/alto, nao moderado/medio).
**Teste revisado:** pular o passo de "tentar a ponte ausente" -- ela nao
esta ausente. Encadear diretamente: `ContinuousLinearMap.spectrum_eq`
(sob `CompleteSpace` via `FiniteDimensional.complete`) para obter
`spectrum R (toEuclideanCLM M2) = spectrum R (toEuclideanCLM M2 : E →ₗ[R] E)`;
combinar com `AlgEquiv.spectrum_eq` (via a instancia `AlgEquivClass`
derivada do `StarAlgEquiv toEuclideanCLM`) e `M_spectrum_eq` (YM-1-Connect,
`spectrum R M2 = {1,3}`) para obter
`spectrum R (toEuclideanCLM M2 : E →ₗ[R] E) = {1,3}`; depois
`Module.End.hasEigenvalue_iff_mem_spectrum` (`Eigenspace/Basic.lean:507`)
mais `M_eigen_three` para identificar `lambdaMax (toEuclideanCLM M2) = 3`.
Falsificado se houver mismatch de coercao/defeq entre `(toEuclideanCLM
M2 : E →ₗ[R] E)` via a coercao de algebra do `StarAlgEquiv` e o tipo
`Module.End R E`/`E →ₗ[R] E` esperado pelas duas pontes -- vale um
`#check` de sanidade antes de comprometer a prova completa.

---

## 5. Hodge Conjecture (HG) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| HG-1c | Finitude de ordem-de-anulamento parametrizada em `a0`, via threading explicito de instancia | SURVIVES | baixo-moderado |
| HG-1d | Empacotar o resultado de finitude f=3/2 do HG-1b como termo `AlgebraicCycle` | SURVIVES | baixo |
| HG-4c | Reconectar `not_differentiable_starRingEnd` (HG-4b) ao predicado `IsHolomorphicTransition` (HG-4) | SURVIVES | trivial |
| — | Ponte maquinaria `ord` (HG-1b) <-> `ClassGroup`/`Pic` (HG-2) | REFUTED | — |

**Passo original vs. o que mudou.** HG-1c e HG-1d sao continuacao direta
de HG-1b (Onda 2). HG-4c e uma descoberta NOVA desta rodada, nao prevista
pelo recon original: releitura integral de
`ConjugationNotHolomorphicProbe.lean` (HG-4b) mostrou que seu proprio
preambulo (linhas 20-26, 64-66, 161-164) marca explicitamente como
"trabalho conectivo futuro, fora de escopo" a reconexao de
`not_differentiable_starRingEnd` ao predicado `IsHolomorphicTransition`
de HG-4 -- e grep em todo o laboratorio confirma que essa reconexao nunca
foi feita em lugar nenhum. A ponte `ord`-`ClassGroup` continua REFUTED,
como ja havia sido diagnosticado (por um angulo ligeiramente diferente)
na Onda 2.

**HG-1c — SURVIVES.** `Scheme.germToFunctionField`
(`AlgebraicGeometry/FunctionField.lean:41-44`, binder `[h : Nonempty U]`
nomeado) e `Scheme.ord_of_isUnit` (`OrderOfVanishing.lean:88-89`, binder
`Nonempty` anonimo -- passagem por nome indisponivel ali, batendo com a
alegacao do candidato) conferem exatos.
`RingedSpace.isUnit_res_basicOpen` (`RingedSpace/Basic.lean:163-166`) nao
tem argumento `Nonempty` nenhum, tambem confere. O preambulo de HG-1b
(linhas 104-117) confirma verbatim o obstaculo documentado (`a0 != 0`
como hipotese de secao nao consegue disparar sintese de typeclass a
jusante) -- real, mas especifico a derivacao automatica em nivel
`variable`, nao obstaculo fundamental a generalizar sobre `a0`.
**Teste revisado:** mesmo teste falsificavel proposto; permitir que a
prova use `haveI : Nonempty (testScheme.basicOpen aSec) := ⟨...⟩`
construido localmente por lema a partir de `(a0 : Z)(ha0 : a0 != 0)`
explicitos, alem de (ou em vez de) threading por argumento nomeado/`@`,
ja que essa e a forma mais idiomatica de contornar o obstaculo
documentado, que e especifico a derivacao automatica em nivel
`variable`.

**HG-1d — SURVIVES.** `AlgebraicCycle` confirmado como
`abbrev AlgebraicCycle (X : Scheme.{u}) (R) [Zero R] :=
Function.locallyFinsupp X R`
(`AlgebraicCycle/Basic.lean`) e `Function.locallyFinsuppWithin`
(`Topology/LocallyFinsupp.lean`, campos `toFun`/`supportWithinDomain'`/
`supportLocallyFiniteWithinDomain'`) conferem em conteudo exato (pequena
discrepancia de ~4 linhas na numeracao citada, sem efeito substantivo).
`principalCycle` do proprio HG-1 (`principal_divisor_algebraic_cycle_bridge.lean:331-336`)
ja e instancia funcionando e ja compilada desse padrao exato, e HG-1b ja
define `f`/`finite_support_ord_f` com tipos identicos aos que
`principalCycle_f` precisaria -- risco tecnico muito baixo.
**Teste revisado:** como proposto, sem estreitamento necessario.

**HG-4c — SURVIVES (item novo, descoberto na revisao).** Ambos os
arquivos-fonte (`HolomorphicTransitionProbe.lean` = HG-4,
`ConjugationNotHolomorphicProbe.lean` = HG-4b) sao arquivos autonomos
`import Mathlib` puro, fora do pacote do lakefile -- a nova sonda precisa
inlinar as duas pecas curtas em vez de importar entre si, seguindo o
mesmo padrao ja usado pelo laboratorio.
**Teste revisado:** construir um novo arquivo autonomo provando
`¬ HG4HolomorphicTransitionProbe.IsHolomorphicTransition (starRingEnd C)`
via `isHolomorphicTransition_iff_differentiable.not.mpr
not_differentiable_starRingEnd` (ou o equivalente `.not_left`/`Iff.not`)
-- combinando mecanicamente dois resultados ja compilados. Isso entrega
exatamente a evidencia que a propria secao "O QUE ESTE ARQUIVO NAO FAZ"
de HG-4 ja nomeou como faltante (mostrar que o predicado REJEITA
corretamente um exemplo real-suave-mas-nao-holomorfo genuino). Escopo
honesto: continua 100% plumbing de diferenciabilidade real/complexa sobre
um fibrado trivial de posto 1 de brinquedo com uma unica carta -- nenhuma
API `VectorBundle`/`Bundle`, nenhuma cohomologia, nada de Hodge (1,1)
mesmo apos sucesso.

**Ponte `ord`(HG-1b) <-> `ClassGroup`/`Pic`(HG-2) — REFUTED.** Grep na
arvore Mathlib vendorizada inteira: zero hits para
`principalDivisor|PrincipalDivisor`, zero hits para `divisorOf|divMap`, e
exatamente um arquivo sob `Mathlib/AlgebraicGeometry/` mencionando
`ClassGroup` -- `EllipticCurve/Affine/Point.lean`. Leitura direta desse
arquivo (linhas 381-393, 716-754) confirma que e maquinaria bespoke de
lei-de-grupo de Weierstrass (`ClassGroup.mk`, `CoordinateRing.XYIdeal'`),
sem conexao com `Scheme.ord` ou `AlgebraicCycle` -- nao serve como ponte
generica. A identificacao classica grupo-de-classes-de-Weil <->
grupo-de-classes-de-ideais para dominios de Dedekind que conectaria
genuinamente HG-1b a HG-2 e teorema classico real, ausente, nao-trivial,
corretamente fora de escopo para um teste falsificavel pequeno.
**Nenhum teste proposto.** Corretamente excluido; nao reabrir sem
evidencia nova de que essa maquinaria classica entrou no Mathlib.

---

## 6. Birch and Swinnerton-Dyer (BSD) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| BSD-1-STEP3-HASEXTENSION | Instancia `HasExtension` para a extensao de valoracao `K -> v.adicCompletion K` | SURVIVES | baixo |
| BSD-1-STEP4-RESIDUE-BIJECTION | Bijecao de corpo de residuo induzida (depende de #STEP3) | SURVIVES | moderado |

**Passo original vs. o que mudou.** Ambos sao continuacao direta do gap
BSD-GAP-007 diagnosticado na Onda 1 e refinado na Onda 2
(`BSD-1_GAP_NOTE.md`, decomposicao em 3 passos). STEP3 ataca exatamente o
ingrediente que Onda 2/BSD-1-STEP2-FULL (REFUTED) identificou como
faltante -- a instancia `IsLocalHom` via `Valuation.HasExtension` -- e a
reverificacao confirma que essa instancia esta genuinamente disponivel
de graca para qualquer corpo-fonte.

**BSD-1-STEP3-HASEXTENSION — SURVIVES.** Releitura integral de
`BSD1Step1ComposeResidueField.lean` e `BSD1Step2CoreDensityBall.lean`
confirma exatamente o que o recon alega, incluindo a nao-composicao
declarada entre eles e o fato de STEP2-CORE ja estabelecer
`algebraMap K (v.adicCompletion K) k' = (k' : v.adicCompletion K) := rfl`
-- exatamente a coercao que este item precisa. `BSD-1_GAP_NOTE.md`
confirma a decomposicao de 3 passos e o "onde retomar" batendo
precisamente. `Mathlib/RingTheory/Valuation/Extension.lean` confirma
todo numero de linha citado: `class HasExtension` (:66),
`instIsLocalHomValuationInteger` (:154-164), secao `AlgebraInstances`
(:167-214) com `instAlgebra_valuationSubring` (:183-184),
`instance : IsLocalHom (algebraMap K₀ L₀)` (:196, verbatim),
`algebraMap_residue_eq_residue_algebraMap` (:209-212, provado por `rfl`).
`Mathlib/RingTheory/DedekindDomain/AdicValuation.lean` confirma
`valuedAdicCompletion_eq_valuation'` (igualdade pontual) e que
`adicCompletionIntegers` e literalmente `Valued.v.valuationSubring`,
batendo com `K₀`/`L₀` de `Extension.lean`. `Valuation.ext` (`Basic.lean:142`)
e `Valuation.IsEquiv`/`of_eq` (:259/705) confirmam que o passo
igualdade-pontual-para-`IsEquiv` e genuinamente curto. Achado adicional
nao citado pelo recon: `Mathlib/RingTheory/LocalRing/RingHom/Basic.lean`
tem uma instancia generica `(priority := 100)` de `IsLocalHom` para
QUALQUER `f : K →+* R` com `K` corpo de divisao -- fornecendo de graca a
hipotese-lado `[IsLocalHom (algebraMap R S)]` que
`instIsLocalHomValuationInteger` tambem exige, reforcando (nao
enfraquecendo) a alegacao de "barato". Grep de `HasExtension` em todo o
Mathlib usado pelo laboratorio: aparece so em `Extension.lean` mesmo,
zero instanciacoes a jusante -- confirmando que este e um alvo genuino,
nao ja fechado em outro lugar.
**Teste revisado:** mesmo teste como proposto; unico refinamento -- antes
de tentar a instancia `HasExtension`, fazer uma sonda de 30 segundos
(`#check`/`example`) de que `IsLocalHom (algebraMap K (v.adicCompletion K))`
resolve sozinho via `inferInstance` (exercitando a instancia generica de
corpo-de-divisao encontrada acima), ja que `instIsLocalHomValuationInteger`
precisa dela silenciosamente ao lado de `HasExtension`.

**BSD-1-STEP4-RESIDUE-BIJECTION — SURVIVES (gated em STEP3).**
Explicitamente condicionado ao sucesso do candidato 1, como o recon
declara. `Mathlib/RingTheory/LocalRing/ResidueField/Basic.lean` confirma
`map`/`map_residue` (`rfl`-provavel) e a instancia
`Algebra (ResidueField R)(ResidueField S)` (via
`Ideal.Quotient.algebraOfLiesOver`, exigindo exatamente
`[Algebra R S][IsLocalHom (algebraMap R S)]` -- ambos supridos pelo
sucesso do STEP3, sem diamante, ja que
`algebraMap_residue_eq_residue_algebraMap` de `Extension.lean` e provado
por `rfl` contra essa mesma instancia generica). `ValuationSubring.lean:882-884`
confirma `mem_maximalIdeal_iff : a in maximalIdeal(v.valuationSubring) <->
v a < 1` verbatim. Encadeando a mao: o testemunha `k` de STEP2-CORE
satisfaz `Valued.v (x - algebraMap k) < 1`, que por `mem_maximalIdeal_iff`
significa `x - algebraMap K₀ L₀ k in maximalIdeal L₀`, i.e.
`residue L₀ x = algebraMap (ResidueField K₀)(ResidueField L₀) (residue K₀ k)`
-- estabelecendo sobrejetividade diretamente de STEP2-CORE, sem argumento
separado de "ideal maximal aberto". Injetividade-a-partir-de-hom-de-corpo-
nao-nulo e `finiteQuotientOfFreeOfNeBot`
(`NumberField/Completion/FinitePlace.lean:126`) sao citacoes padrao,
corretamente marcadas como nao re-derivadas independentemente pelo
candidato. BSD-GAP-007 confirmado como gap corretamente alvejado
(`GAP_REGISTER.yaml`); BSD-GAP-008 (Mordell-Weil) corretamente excluido.
**Teste revisado:** como proposto, gated em #STEP3. Nota de guarda: antes
de compor, verificar que so existe UMA instancia
`Algebra (ResidueField K₀)(ResidueField L₀)` (confirmado por leitura --
`Extension.lean` supre os ingredientes, `ResidueField/Basic.lean` supre a
unica construcao a partir deles), documentacao para quem executar, nao
bloqueador.

---

## 7. Sintese TOE (extensao interna do laboratorio — NAO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| TOE-3d | `homK` nao e isomorfismo em `ActionCategory K Regime3` | SURVIVES | baixo |
| TOE-3e | `IsConnected (ActionCategory K Regime3)` via zigzag construido a mao apesar de nao-pretransitividade | SURVIVES | moderado |

**Passo original vs. o que mudou.** Ambos sao continuacao direta de
TOE-3c (Onda 2), que construiu o monoide de brinquedo `K = {identity, k}`
com acao constante `Kact .k _ = .alpha`. TOE-3d testa a consequencia
categorica imediata (o segundo morfismo nao e isomorfismo); TOE-3e testa
uma questao mais fina (a categoria de acao e conexa mesmo sem
pretransitividade).

**TOE-3d — SURVIVES.** Releitura confirma `K = {identity, k}`,
`Kmul .identity x = x`, `Kmul .k _ = .k` (absorvente/idempotente),
`Kact .identity r = r`, `Kact .k _ = .alpha`, `homIdentity`/`homK` como
os dois elementos literais de `Hom(alpha,alpha)` (`.val` `rfl` em ambos),
`k_ne_identity` ja provado por `decide`.
`CategoryTheory/Iso.lean:238-240` confirma `class IsIso (f : X ⟶ Y) :
Prop where out : exists inv, f ≫ inv = id X and inv ≫ f = id Y` exatamente
citado. `Action.lean:127-128` da `comp_val : (f ≫ g).val = g.val * f.val`
(ordem "invertida" ao nivel de `.val`) -- verificado que isso nao quebra
o argumento: como `K.k` e absorvente dos dois lados (`Kmul .k _ = .k` e
`Kmul x .k` reduz a `.k` em ambos os casos `x=identity`/`x=k`), para
QUALQUER candidato-inverso `g` com `g.val in {identity,k}`, tanto
`g.val * K.k` quanto `K.k * g.val` reduzem a `K.k != K.identity =
(id alpha).val` -- as duas equacoes de `IsIso.out` falham identicamente,
independente da ordem de composicao que o elaborador efetivamente
precisar. Uma ressalva real: `stabilizerIsoEnd` (`Action.lean:106-108`)
carrega `set_option backward.isDefEq.respectTransparency.types false in`,
sinal de que o proprio Mathlib achou fragil esse desdobramento
definicional -- a rota alternativa (b), construida sobre isso, carrega
risco de elaboracao nao-trivial. A rota (a) direta (case-split via
Hom-como-subtipo, `comp_val`, `k_idempotent`, `k_ne_identity`, o mesmo
idioma que ja fechou `homIdentity_ne_homK` em TOE-3c) e suficiente e
primaria.
**Teste revisado:** sem estreitamento necessario no enunciado; usar so a
rota (a) como principal e remover a rota (b) do plano inteiramente (nao
so marcar "opcional"), dado o aviso de transparencia anexado a
`stabilizerIsoEnd` no proprio Mathlib -- reduz risco de elaboracao a
quase zero sem perda de conteudo.

**TOE-3e — SURVIVES.** `MulAction.IsPretransitive`
(`Algebra/Group/Action/Pretransitive.lean:60-62`, campo
`exists_smul_eq : forall x y, exists g, g • x = y`) aplicado a
`x=alpha,y=beta`: como `Kact .identity alpha = alpha` e `Kact .k _ =
.alpha` (o segundo braco tambem dispara para entrada `alpha`), todo
`m : K` leva `alpha` a `alpha`, nunca a `beta` -- confirmando
`¬IsPretransitive K Regime3` por calculo direto, nao so plausibilidade.
`IsConnected.lean` confirma `Zag.of_hom`/`of_inv` (:307/309),
`Zigzag := ReflTransGen Zag` (:314-315), `Zigzag.trans` (:331-333),
`zigzag_isConnected [Nonempty J]` (:436) exatamente citados. Construcao
de zigzag verificada a mao: `Kact k beta = alpha` e `Kact k gamma =
alpha` valem ambos (por `Kact .k _ = .alpha` incondicional), dando
morfismos literais `beta⟶alpha` e `gamma⟶alpha`, de onde `Zag.of_hom`/
`of_inv`/`Zigzag.trans` encadeiam `beta-alpha-gamma`; os pares
`alpha-alpha`/`beta-beta`/`gamma-gamma` sao `Zigzag.refl` -- os 9 pares
ordenados de `Regime3` fecham dessa forma. `Regime3.lean` (linhas 25-28,
63-70) reconfirmado batendo com a citacao. Item genuinamente diferente e
nao-trivial de TOE-3d (sondando suficiencia vs. necessidade de
`IsPretransitive` para `IsConnected`), reusa zero construcao nova alem do
que TOE-3c ja estabeleceu. Custo "moderado" e justo: os objetos de
`ActionCategory K Regime3` nao sao defeq a `Regime3` (so equivalentes via
`objEquiv`), entao as testemunhas de zigzag precisam do mesmo estilo
`show KCat from Regime3.alpha` ja usado em TOE-3c, mais case analysis
explicito sobre os pares 3x3 (ou 6 por simetria).
**Teste revisado:** sequenciar como o proprio teste de duas partes ja
propoe: primeiro o lema negativo `¬IsPretransitive` como resultado
autonomo e imediatamente verificavel; tratar a construcao completa de
`zigzag_isConnected` como commit separado -- se a burocracia de
equivalencia de objeto se mostrar mais atritosa que o esperado, o fato
`¬IsPretransitive` autonomo ja e um resultado honesto e pequeno por si
so, nao tudo-ou-nada.

---

## 8. Fundamentos Quanticos / Unificacao (extensao interna — NAO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| QF-6 | Identidade de Ehrenfest em tempo real (parear WAVE2-QF-5 com vetor fixo via `toEuclideanLin` + `HasDerivAt.inner`) | NEEDS_NARROWING | baixo-moderado |

**Passo original vs. o que mudou.** Continuacao direta de WAVE2-QF-5
(Onda 2), que provou so a identidade operatorial pura, com o proprio
header do arquivo marcando explicitamente o passo de pareamento por
produto interno como nao tentado; QCU-001 continua UNSCOPED em
`SCOPE.md`, sem overclaiming encontrado.

**QF-6 — NEEDS_NARROWING.** Releitura integral de
`HeisenbergCommutatorFlowIdentity.lean` (259 linhas) e
`HeisenbergFlowDerivativeProbe.lean` (179 linhas) confirma o resumo do
recon sobre o que a Onda 2/QF-5 realmente provou. A arquitetura central
esta correta: `HasDerivAt.inner` (`Calculus.lean:109`, so `f g : R -> E`,
sem versao parametrizada em `C` -- confirmando que reparametrizar o tempo
para `R` e genuinamente necessario e correto), `HasFDerivAt.comp_hasDerivAt`
(`Deriv/Comp.lean:389`), `ContinuousLinearMap.hasFDerivAt`
(`FDeriv/Linear.lean:57`), `toEuclideanLin` e sua identidade `mulVec`
(`PiL2.lean:1242/1256`) e `LinearMap.applyₗ` (`End.lean:387`) conferem
todos exatos. Porem TRES citacoes especificas do recon estao erradas ou
enganosas: (1) `NormedSpace R E` para `E=EuclideanSpace C n` NAO e
"auto-suprido" por `InnerProductSpace.rclikeToReal`
(`InnerProductSpace/Basic.lean:946`) -- esse e um `abbrev` cujo docstring
diz explicitamente que NAO e registrado como instancia (risco de
diamante); a conclusao e verdadeira, mas via `NormedSpace.complexToReal`
(`Complex/Basic.lean:80`, instancia global genuina de prioridade 900).
Mesmo padrao para `NormedAlgebra R (Matrix .. C)`: a rota automatica real
e `Matrix.linftyOpNormedAlgebra` (bloco `Norms.Operator` ja aberto por
QF-5) instanciado com `NormedAlgebra R C`
(`Complex/Basic.lean:84`), nao o mecanismo vago descrito. (2)
`LinearMap.continuous_of_finiteDimensional` citado em
`Normed/Module/FiniteDimension.lean:51` e so mencao em doc-comment; o
teorema real esta em `Topology/Algebra/Module/FiniteDimension.lean:277`,
arquivo diferente. (3) `toEuclideanLin_apply` esta marcado
`@[deprecated toLpLin_apply (since := "2026-01-22")]` no snapshot
vendorizado -- ainda usavel mas nao o idioma atual; usar `toLpLin_apply`.
Nenhuma fabricacao (todo objeto citado existe e faz o que se alega), mas
um implementador seguindo as citacoes como escritas iria a arquivo/linha
errados em dois casos e a uma declaracao formalmente-nao-instancia no
terceiro. O proprio teste de 3 passos do recon tambem nao inclui um
checkpoint explicito para um ponto de atrito real: o mapa de avaliacao
`A -> (toEuclideanLin A) psi` e naturalmente C-linear, mas
`HasFDerivAt.comp_hasDerivAt` exige que a derivada de Frechet do mapa
externo viva no MESMO corpo do parametro da curva interna (`R` aqui) --
exigindo um `ContinuousLinearMap.restrictScalars R` explicito antes de
compor, tratado como automatico no esboco original. Grep no arquivo
inteiro por "Ehrenfest" confirma zero duplicacao (so os 4 arquivos QF +
docs de planejamento). `still_missing_if_success` honesto: continua
gerador de brinquedo limitado de dimensao finita fixa, nao toca
UNSCOPED de QCU-001, nenhuma constante fisica `hbar` anexada.
**Teste revisado:** mesmo teste de 3 passos, corrigido, com um 4o
checkpoint: (1) confirmar `NormedAlgebra R (Matrix (Fin 2)(Fin 2) C)` via
`Matrix.linftyOpNormedAlgebra (R:=R)` + `NormedAlgebra R C`
(`Complex/Basic.lean:84`) -- NAO depender do `abbrev` interno de
`InnerProductSpace.rclikeToReal`; (2) rerodar
`hasDerivAt_exp_smul_const_of_mem_ball` com `A=C=R`, `t0:R` -- parar se
sintese de instancia falhar; (3) construir
`A -> (Matrix.toEuclideanLin A) psi` como
`Matrix (Fin 2)(Fin 2) C →ₗ[C] EuclideanSpace C (Fin 2)` via
`LinearMap.applyₗ` composto com `toEuclideanLin.toLinearMap` (usando
`toLpLin_apply`, nome nao-deprecated), depois aplicar explicitamente
`LinearMap.restrictScalars R` antes de invocar
`LinearMap.continuous_of_finiteDimensional` (citacao correta:
`Topology/Algebra/Module/FiniteDimension.lean:277`) para obter
`Matrix (Fin 2)(Fin 2) C →L[R] EuclideanSpace C (Fin 2)` -- parar se a
cadeia `restrictScalars`/instancia-dimensao-finita-sobre-R nao descarregar
automaticamente; (4) encadear via `HasFDerivAt.comp_hasDerivAt` sobre a
curva do passo (2) e fechar com `HasDerivAt.inner` -- parar se a algebra
final `simp`/`noncomm_ring` nao fechar na forma esperada
`⟨psi,(A(t)H-HA(t))psi⟩`.

---

## Infraestrutura compartilhada entre frentes (continuacao)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| SHARED-2A-EXT | `lambda2_hasEigenvalue` -- promover "trace - lambdaMax" a segundo autovalor genuino em dim 2 | NEEDS_NARROWING | baixo-moderado |

**Passo original vs. o que mudou.** Continuacao direta de SHARED-INFRA-2A
(Onda 2), que definiu `lambda2 := trace - lambdaMax` e provou sua
Lipschitz-continuidade sem nunca mostrar que `lambda2` e de fato um
autovalor. Este item fecha exatamente essa lacuna.

**SHARED-2A-EXT — NEEDS_NARROWING.** Releitura integral de
`SecondEigenvalueLipschitz.lean` (293 linhas) e
`FixedDimEigenvalueStability.lean` (213 linhas) confirma o resumo do
recon como preciso, e os quatro lemas Mathlib citados existem com as
assinaturas alegadas: `LinearMap.IsSymmetric.trace_eq_sum_eigenvalues`
(`Trace.lean:39-42`), `exists_eigenvalues_eq` (`Spectrum.lean:283-287`),
`eigenvalues_antitone` (`Spectrum.lean:312-318`),
`hasEigenvalue_eigenvalues` (`Spectrum.lean:320-322`). `Fin.sum_univ_two`
(auto-gerado de `Fin.prod_univ_two`, `BigOperators/Fin.lean:110-112`) e
`Module.End.HasEigenvalue` (`Eigenspace/Basic.lean:425`) tambem conferem,
batendo com a sintaxe ja usada em `lambdaMax_hasEigenvalue` do proprio
YM-3. O esboco de prova e matematicamente solido: `lambdaMax T` ja
mostrado autovalor (YM-3) fixa `eigenvalues[0]` via
`exists_eigenvalues_eq`+`eigenvalues_antitone`; a desigualdade reversa
vem de um calculo de quociente de Rayleigh no autovetor via
`eigenvectorBasis`, mesmo padrao `le_ciSup`/coercao ja precedentado em
`lambdaMax_lipschitz`. Porem o teste falsificavel como proposto alega que
o arquivo novo pode reusar "a maquinaria existente de `lambdaMax`/
`lambdaMax_hasEigenvalue`/trace... reproduzida de
`SecondEigenvalueLipschitz.lean`" -- ISSO ESTA ERRADO. Grep direto em
`SecondEigenvalueLipschitz.lean` mostra que ele reproduz so `abbrev E`,
`def lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
`lambdaMax_lipschitz`. `lambdaMax_hasEigenvalue` aparece SO em comentarios
de prosa (linhas 61, 109), nunca como teorema real -- existe apenas no
arquivo YM-3 da Onda 1 (`FixedDimEigenvalueStability.lean:139-144`). O
proprio esboco de prova do candidato depende exatamente desse lema
faltante (e o que permite invocar `exists_eigenvalues_eq` sobre
`lambdaMax T`). Nao invalida a matematica -- so significa que o arquivo
novo precisa reproduzir um QUARTO bloco verbatim (`lambdaMax_hasEigenvalue`,
~6 linhas) de YM-3, seguindo a mesma convencao de reproducao byte-identica
ja estabelecida por SHARED-2A, em vez de assumir que ja esta disponivel.
Separadamente, a citacao de `finrank` (`PiL2.lean:202`) aponta para o
`finrank_euclideanSpace` generico indexado por `Fintype`, nao o mais
diretamente relevante `finrank_euclideanSpace_fin` (`PiL2.lean:207`, caso
`Fin n`) -- ambos existem e funcionam, entao e deslize de linha de
citacao inofensivo, nao gap de suporte. `still_missing_if_success`
honesto e corretamente escopado (so dim-2, sem alegacao de gap/min-max,
sem conteudo Yang-Mills).
**Teste revisado:** em arquivo novo autonomo (ex.:
`SHARED-2A-EXT/LambdaTwoHasEigenvalue.lean`, seguindo a convencao ja
estabelecida por SHARED-2A), reproduzir verbatim QUATRO blocos, nao tres:
(1) `abbrev E`; (2) `def lambdaMax` + `bddAbove_rayleighQuotient_subtype`
+ `lambdaMax_lipschitz`; (3) `theorem lambdaMax_hasEigenvalue (T :
E →L[R] E) (hT : (T : E →ₗ[R] E).IsSymmetric) : Module.End.HasEigenvalue
(T : E →ₗ[R] E) (lambdaMax T)` -- copiado byte-identico de
`FixedDimEigenvalueStability.lean:139-144`, que `SecondEigenvalueLipschitz.lean`
NAO contem; (4) `def lambda2 := trace - lambdaMax` mais
`trace_lipschitz`/`lambda2_lipschitz`. Depois tentar o alvo novo:
`theorem lambda2_hasEigenvalue (T : E →L[R] E) (hT : (T : E →ₗ[R]
E).IsSymmetric) (hn : Module.finrank R E = 2) : Module.End.HasEigenvalue
(T : E →ₗ[R] E) (lambda2 T)` via: obter `i0` com
`hT.exists_eigenvalues_eq hn` aplicado ao autovalor de `lambdaMax_hasEigenvalue`;
mostrar `i0 = 0` usando `eigenvalues_antitone` mais o bound reverso de
Rayleigh-no-autovetor (`le_ciSup` sobre o sup definidor de `lambdaMax`,
espelhando `lambdaMax_lipschitz`); concluir `lambdaMax T = hT.eigenvalues
hn 0` por antissimetria; reescrever `lambda2 T = trace - lambdaMax T =
(eigenvalues 0 + eigenvalues 1) - eigenvalues 0 = eigenvalues 1` (via
`trace_eq_sum_eigenvalues` + `Fin.sum_univ_two`); fechar com
`hasEigenvalue_eigenvalues hn 1`. Se a fronteira de coercao entre
`(T : E →L[R] E)` e `(T : E →ₗ[R] E)` bloquear algum passo alem do que a
propria prova de `lambdaMax_hasEigenvalue` do YM-3 ja teve que tratar, ou
se a identidade de quociente-de-Rayleigh-no-autovetor nao reduzir limpo
via `apply_eigenvectorBasis` + simp de produto interno, reportar essa
falha honestamente em vez de forcar contorno.

---

## Lista de execucao Onda 3 (despacho direto para agente de formalizacao)

Cada item abaixo traz o candidato, o teorema-alvo, e o enunciado de teste
exato (ja revisado pela adversarial), pronto para um agente de
formalizacao executar sem reinterpretacao. Ordem: por linha, na mesma
sequencia das secoes acima. Todos sao independentes entre si a menos que
anotado.

```text
 1. RH / RH-3 (unboundedEigCount)
    Provar unboundedEigCount Lam = Nat.floor Lam + 1 para 0 <= Lam.
    Aceitar QUALQUER prova valida: (a) direta via Tp_isEigenvalue +
    Tp_eigenvalue_mem_range, bijetando o conjunto de autovalores com
    {n : N | n <= Lam} via Nat.cast; ou (b) via eigenvalue_bridge +
    eigCount_eq_floor em lam=(Lam+1)^-1, exigindo neste caso um lema
    nomeado explicito para o transporte de desigualdade
    (Complex.abs mu <= Lam <-> lam <= Complex.abs ((mu+1)^-1)).
    #print axioms so com os 3 axiomas padrao.

 2. NS / NS-3a (revisado -- consistencia de raio)
    Para g : E -> R, L c : R, hg : LipschitzWith L.toNNReal g,
    R1 R2 : R com 0 < R1 < R2, hsupp : forall y, R1 < ||y|| -> g y = c,
    provar (integral sobre closedBall 0 R1 \ {0} de K*(g-g0)) =
    (integral sobre closedBall 0 R2 \ {0} de K*(g-g0)), via
    setIntegral_union (dividindo em bola interna + casca) e
    K_shell_integral_eq_zero na casca (integrando ai e a constante
    (c-g0) vezes K).

 3. PN / PN-6 (goto data-dependente)
    Construir FinTM2 com goto cujo alvo depende de um bit simbolico
    (nao constante), reusando o padrao de PN2PRIME/PN5. Tentar fechar
    via rfl; fallback comprometido de antemao: by cases b <;> rfl (nao
    decide).

 4. PN / PN-7 (cobertura branch/cond)
    Construir FinTM2 usando cond(f v, ...) com f v simbolico dentro de
    stepAux, testando o unico construtor Stmt (branch/peek) ainda sem
    cobertura no laboratorio. Sequenciar apos item 3; mesmo fallback
    by cases <;> rfl.

 5. YM / YM-STABILITY-COMPOSE
    Arquivo novo autonomo reproduzindo verbatim: E, lambdaMax,
    lambdaMax_lipschitz, lambda2, lambda2_lipschitz (Lipschitz files) +
    M1, M2, sonda1_bridge, sonda2_numeric_norm (L2OperatorNormProbe).
    Provar os dois corolarios compostos: |lambdaMax M1 - lambdaMax M2|
    <= 1/10 e |lambda2 M1 - lambda2 M2| <= 3/10, via
    (lambdaMax_lipschitz _ _).trans (rw [sonda1_bridge]; exact
    sonda2_numeric_norm.le), mesma rota para lambda2.

 6. YM / YM-STABILITY-GROUNDED
    Encadear ContinuousLinearMap.spectrum_eq (sob CompleteSpace via
    FiniteDimensional.complete) + AlgEquiv.spectrum_eq (via
    AlgEquivClass do StarAlgEquiv toEuclideanCLM) + M_spectrum_eq
    (YM-1-Connect, spectrum R M2 = {1,3}) para obter
    spectrum R (toEuclideanCLM M2 : E →ₗ[R] E) = {1,3}; depois
    Module.End.hasEigenvalue_iff_mem_spectrum + M_eigen_three para
    concluir lambdaMax (toEuclideanCLM M2) = 3.

 7. HG / HG-1c (finitude parametrizada em a0)
    Generalizar o resultado de finitude de HG-1b sobre (a0 : Z)
    (ha0 : a0 != 0) explicitos, usando haveI local por lema para a
    instancia Nonempty (testScheme.basicOpen aSec) construida a partir
    de a0/ha0, em vez de depender de derivacao automatica em nivel
    variable.

 8. HG / HG-1d (AlgebraicCycle a partir do f=3/2 de HG-1b)
    Construir principalCycle_f : AlgebraicCycle testScheme Z a partir
    de f e finite_support_ord_f (ja definidos em HG-1b), espelhando
    verbatim a construcao principalCycle ja provada em HG-1.

 9. HG / HG-4c (reconexao holomorfa)
    Arquivo novo autonomo inlinando as pecas curtas de
    HolomorphicTransitionProbe.lean e ConjugationNotHolomorphicProbe.lean.
    Provar ¬ HG4HolomorphicTransitionProbe.IsHolomorphicTransition
    (starRingEnd C) via isHolomorphicTransition_iff_differentiable.not.mpr
    not_differentiable_starRingEnd.

10. BSD / BSD-1-STEP3-HASEXTENSION
    Provar (v.valuation K).HasExtension (Valued.v : Valuation
    (v.adicCompletion K) Zm0), desbloqueando
    instIsLocalHomValuationInteger. Sonda previa recomendada: confirmar
    IsLocalHom (algebraMap K (v.adicCompletion K)) resolve por
    inferInstance sozinho.

11. BSD / BSD-1-STEP4-RESIDUE-BIJECTION (depende de #10)
    Usando a instancia Algebra (ResidueField K₀)(ResidueField L₀)
    (via Ideal.Quotient.algebraOfLiesOver, suprida por #10), provar
    sobrejetividade do mapa residual induzido diretamente do
    testemunha k de STEP2-CORE via mem_maximalIdeal_iff (x - algebraMap
    k in maximalIdeal L₀ -> residue L₀ x = algebraMap(residue K₀ k)).
    Fechar injetividade via hom de corpo nao-nulo padrao, cardinalidade
    via finiteQuotientOfFreeOfNeBot.

12. TOE / TOE-3d (homK nao e isomorfismo)
    Provar ¬ IsIso homK em ActionCategory K Regime3, via case-split
    direto sobre Hom-como-subtipo (rota (a) apenas): para qualquer
    candidato-inverso g com g.val in {identity,k}, usar comp_val +
    k_idempotent + k_ne_identity para mostrar que ambas as equacoes de
    IsIso.out falham (K.k absorvente dos dois lados). Nao tentar a rota
    via stabilizerIsoEnd.

13. TOE / TOE-3e (IsConnected apesar de nao-pretransitivo)
    Primeiro, como resultado autonomo: provar ¬ MulAction.IsPretransitive
    K Regime3 (Kact .identity alpha = alpha e Kact .k _ = .alpha,
    nenhum m leva alpha a beta). Depois, como commit separado: provar
    IsConnected (ActionCategory K Regime3) via zigzag_isConnected,
    construindo Zigzag para os 9 pares ordenados de Regime3 usando
    Kact k beta = alpha, Kact k gamma = alpha (Zag.of_hom/of_inv/trans).

14. QF / QF-6 (Ehrenfest, revisado)
    (1) Confirmar NormedAlgebra R (Matrix (Fin 2)(Fin 2) C) via
    Matrix.linftyOpNormedAlgebra (R:=R) + NormedAlgebra R C
    (Complex/Basic.lean:84). (2) Rerodar
    hasDerivAt_exp_smul_const_of_mem_ball com A=C=R, t0:R. (3) Construir
    A -> (Matrix.toEuclideanLin A) psi via LinearMap.applyₗ +
    toLpLin_apply, aplicar LinearMap.restrictScalars R, invocar
    LinearMap.continuous_of_finiteDimensional
    (Topology/Algebra/Module/FiniteDimension.lean:277). (4) Encadear via
    HasFDerivAt.comp_hasDerivAt + HasDerivAt.inner, fechar com
    noncomm_ring, concluindo a identidade de Ehrenfest
    d/dt⟨psi, A(t)psi⟩ = ⟨psi,(A(t)H-HA(t))psi⟩. Reportar honestamente
    em qual dos 4 passos travar, se travar.

15. SHARED-INFRA / 2A-EXT (lambda2_hasEigenvalue)
    Em arquivo novo autonomo, reproduzir verbatim QUATRO blocos: E;
    lambdaMax + bddAbove_rayleighQuotient_subtype + lambdaMax_lipschitz;
    lambdaMax_hasEigenvalue (copiado de FixedDimEigenvalueStability.lean:
    139-144, NAO presente em SecondEigenvalueLipschitz.lean); lambda2 +
    trace_lipschitz + lambda2_lipschitz. Provar lambda2_hasEigenvalue
    (T : E →L[R] E) (hT : IsSymmetric) (hn : finrank R E = 2) :
    HasEigenvalue (T : E →ₗ[R] E) (lambda2 T), via exists_eigenvalues_eq
    + eigenvalues_antitone + bound reverso de Rayleigh no autovetor
    (le_ciSup) para fixar lambdaMax T = eigenvalues 0, depois
    trace_eq_sum_eigenvalues + Fin.sum_univ_two para lambda2 T =
    eigenvalues 1, fechando com hasEigenvalue_eigenvalues.
```

Total: **15 itens** na lista de execucao Onda 3 -- um para cada
candidato `SURVIVES`/`NEEDS_NARROWING` desta rodada que rendeu teste
falsificavel concreto (nenhum item derivado de candidato `REFUTED`, e
nenhum item forcado onde a revisao confirmou "0 candidatos" ou "escopo
grande demais para esta rodada"). Contagem menor que os 20 da Onda 2 --
resultado honesto, nao ajustado: tres sub-frentes (RH/RVM-NZeta, NS
full-distribution/NS-3b, HG ord-ClassGroup) nao renderam alvo pequeno
nesta rodada, e o item PN de extensao mecanica de 3 labels foi
autoexcluido como busywork de baixa informacao. Notas de dependencia:
item 4 (PN-7) sequenciado apos item 3 (PN-6), mesmo mecanismo, marcado
confirmatorio; item 11 (BSD STEP4) depende de item 10 (BSD STEP3); item
13 (TOE-3e) tem uma parte autonoma (nao-pretransitividade) e uma parte
dependente dela (construcao completa do zigzag), tratadas como dois
commits sequenciais do mesmo item.

---

## Descartados nesta rodada (nao reabrir sem evidencia nova)

```text
RH  Composicao NZeta(WAVE2-RH-2)/formula-limite RVM(WAVE2-RH-1)
      -- 0 candidatos, confirmado independentemente. RVMLimitErrorComposition.lean
         opera sobre e : R -> R abstrato (sem riemannZeta/N_zeta,
         conexao real e SB-GAP-010B, fora de escopo por design).
         ZetaZerosCountingMonotoneVanishing.lean prova NZeta real mas so
         monotonicidade/anulamento de fronteira, desconectado da
         maquinaria RVM por header proprio. Mathlib/ZetaZeros.lean nao
         oferece assintotica de contagem. Ponte pequena exigiria
         reformalizar Riemann-von Mangoldt do zero -- fora de escopo

NS  NS-3b: distribuicao p.v. global pvK em D'^1(E,R) via
      TestFunction.mkCLM/limitCLM sobre TODOS os compactos
      -- correta e conscientemente adiada, nao REFUTED. Cadeia de
         dependencia (gap(i)=NS-3a -> gap(ii)=bola-para-K'-arbitrario via
         monoCLM+isBounded -> toFun_eq_T/typeclasses de limitCLM) e
         materialmente maior que um item de onda; retomar so apos NS-3a
         fechar, provavelmente como item multi-etapa em onda futura

PN  Extensao mecanica de goto de 3 labels
      -- deprioridade pelo proprio recon e confirmada pela adversarial
         como busywork de baixa informacao: nao testa mecanismo novo
         alem do que PN-6/PN-7 ja cobrem, so aumenta contagem de labels
         sem novo obstaculo tecnico

HG  Ponte maquinaria ord(HG-1b) <-> ClassGroup/Pic(HG-2)
      -- REFUTED. Zero hits para principalDivisor/divisorOf em todo o
         Mathlib; unico arquivo AlgebraicGeometry mencionando ClassGroup
         (EllipticCurve/Affine/Point.lean) e maquinaria bespoke de
         Weierstrass sem conexao com Scheme.ord ou AlgebraicCycle. A
         identificacao classica grupo-de-Weil <-> grupo-de-ideais para
         dominios de Dedekind e teorema real ausente, nao-trivial, fora
         de escopo para teste pequeno. NAO entra na lista de execucao;
         se retomado no futuro, so apos confirmar que essa maquinaria
         classica entrou no Mathlib
```

---

## Avaliacao pessoal — os 2-3 candidatos com maior chance de virar
resultado formal honesto e nao-trivial mais cedo

Nao e repeticao da autoavaliacao dos agentes de recon/adversarial -- e
julgamento proprio depois de ler as 18 verificacoes inteiras desta onda.

**1. HG-4c (reconexao `not_differentiable_starRingEnd` ao predicado de
transicao holomorfa).** E o candidato mais barato do lote inteiro desta
onda: os dois ingredientes ja compilam de forma independente (HG-4 e
HG-4b, ambos Onda 2), o proprio arquivo HG-4b ja nomeia essa reconexao
como o unico passo faltante em seu comentario de fechamento, e a
combinacao e literalmente uma linha (`isHolomorphicTransition_iff_differentiable.not.mpr
not_differentiable_starRingEnd`). Nenhuma citacao Mathlib nova entra em
jogo. Risco tecnico residual: quase nulo.

**2. YM-STABILITY-COMPOSE (bound de norma encadeado sobre `M1`,`M2`).**
A revisao adversarial confirmou que nenhuma citacao Mathlib nova e
necessaria -- e recombinacao pura de tres pecas ja type-checadas
(`lambdaMax_lipschitz`/`lambda2_lipschitz` do YM-3, `sonda1_bridge`/
`sonda2_numeric_norm` do YM-1+YM-3 da Onda 2), seguindo a convencao de
reproducao verbatim ja estabelecida. Nao ha ambiguidade de tipagem ou
direcao como em varios outros candidatos "NEEDS_NARROWING" desta rodada.

**3. HG-1d (empacotar o resultado de finitude f=3/2 de HG-1b como
`AlgebraicCycle`).** `principalCycle` do proprio HG-1 (Onda 1) ja e
instancia funcionando e ja compilada do mesmo padrao estrutural exato, e
HG-1b (Onda 2) ja define `f`/`finite_support_ord_f` com tipos
identicos aos que a nova construcao precisa -- e essencialmente uma copia
quase-verbatim de uma construcao ja verificada, aplicada a termos que ja
existem. A revisao adversarial nao encontrou nenhum defeito em nenhuma
citacao.

Nao incluo nenhum candidato BSD, QF ou SHARED-INFRA no top 3: BSD-1-STEP3
e genuinamente solido e a revisao adversarial ate reforcou sua alegacao
de "barato" com um achado extra (instancia `IsLocalHom` generica de
corpo-de-divisao), mas BSD como frente carrega a mesma advertencia das
Ondas 1-2 -- o item STEP4 so fecha se STEP3 fechar primeiro, e a frente
inteira ja teve um item inteiro (STEP2-FULL, Onda 2) refutado por muro de
tipagem estrutural, entao o historico pede cautela extra. QF-6 e
SHARED-2A-EXT tem matematica solida mas cada um carrega pelo menos uma
citacao Mathlib corrigida pela adversarial (arquivo/linha errados, ou
lema faltante nao percebido pelo proprio candidato) -- sinal de que a
execucao real vai precisar de mais navegacao do que o texto do teste
sozinho sugere, mesmo com o teste ja revisado.

---

## O que este documento confirma sobre o processo

A cada onda, a disciplina de "reverificar por leitura direta de arquivo,
nao por confianca no recon" continua achando erros reais e especificos
-- nesta rodada: uma citacao "confirmado ausente" que na verdade existe
(`ContinuousLinearMap.spectrum_eq`, YM-STABILITY-GROUNDED), tres
citacoes de arquivo/linha erradas em um unico candidato (QF-6), um
bloco de reproducao faltante nao percebido pelo proprio candidato
(SHARED-2A-EXT), e uma hipotese de teste falsificavel matematicamente
errada que tornaria o teste trivial em vez de informativo (NS-3a). Nenhum
desses erros invalidou o candidato subjacente -- em todos os casos o
alvo real continuou de pe, so precisou de correcao de rota. Isso e
exatamente o padrao que justifica manter a etapa adversarial obrigatoria
antes de qualquer despacho de execucao.
