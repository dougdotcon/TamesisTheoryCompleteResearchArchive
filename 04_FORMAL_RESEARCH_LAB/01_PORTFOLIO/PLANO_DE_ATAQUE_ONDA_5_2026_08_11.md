---
document_id: PLANO-ATAQUE-ONDA-5-2026-08-11
reviewed_at: 2026-08-11
input: recon + revisao adversarial de 9 grupos (8 linhas de pesquisa + infraestrutura compartilhada) para Onda 5, ancorado nos resultados reais da Onda 4 -- ver 09_SESSIONS/2026/2026-08-11_WAVE4_EXECUTION.md (14/14 CLOSED, 0 gaps, fechamento genuino de BSD-GAP-007) e 01_PORTFOLIO/PLANO_DE_ATAQUE_PORTFOLIO_COMPLETO_2026_08_09.md, 01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md, 01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_3_2026_08_10.md, 01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_4_2026_08_10.md
conclusion: PLANO_DE_EXECUCAO_ONDA_5_PROPOSTO
---

# Plano de ataque — Onda 5 (continuacao das Ondas 1-4)

## Enquadramento honesto

Este documento e a continuacao direta de
`PLANO_DE_ATAQUE_PORTFOLIO_COMPLETO_2026_08_09.md`,
`PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md`,
`PLANO_DE_ATAQUE_ONDA_3_2026_08_10.md`,
`PLANO_DE_ATAQUE_ONDA_4_2026_08_10.md` e da sessao de execucao
`2026-08-11_WAVE4_EXECUTION.md`. A Onda 4 fechou **14 de 14** itens (10
VERIFIED, 4 VERIFIED_WITH_NOTES), com **zero** `GAP_DIAGNOSED` e **zero**
`REJECTED`, e produziu um fechamento genuino de gap nomeado --
`BSD-GAP-007` -- verificado com escrutinio extra (leitura integral do
arquivo de 389 linhas, comparacao letra por letra contra o alvo exato do
`BSD-1_GAP_NOTE.md`, recompilacao pessoal e reconstrucao de `#print
axioms` para as 12 declaracoes). A Onda 5 parte desse chao real.

```text
O que este plano E:
  - a proxima rodada de pequenos testes falsificaveis contra
    infraestrutura Mathlib genuina, construida sobre os 14 itens
    fechados na Onda 4 (e, por heranca, sobre os 15+20+25 das Ondas
    1-3)
  - uma tentativa de re-verificar, por leitura direta de arquivo (nao por
    confianca no agente de recon) -- e, em varios casos desta onda,
    com verificacao independente de citacoes Mathlib linha a linha e
    ate mao-na-massa aritmetica/combinatoria -- se os alvos propostos
    continuam abertos, ja foram satisfeitos por acaso, ou tem um
    defeito matematico real
  - honesto sobre linhas sem alvo pequeno disponivel nesta rodada, e
    sobre onde um teste proposto tinha um gap de composicao real (nao
    so cosmetico) que precisou de reescopo

O que este plano NAO E:
  - uma alegacao de que qualquer Problema do Milenio ficou mais proximo
    de ser resolvido -- nenhum item abaixo toca o nucleo central de
    nenhuma das 6 frentes Clay-oficiais
  - uma alegacao de que o fechamento de BSD-GAP-007 (Onda 4) constitui
    progresso sobre a conjectura de Birch e Swinnerton-Dyer em si --
    `IsMultiplicative` de coeficientes de Dirichlet de um produto de
    Euler formal e propriedade estrutural basica, nao toca
    LSeries/continuacao analitica/equacao funcional/posto de
    Mordell-Weil. `BSD-GAP-008` (Mordell-Weil fraco) permanece `OPEN`
    e nao relacionado
  - uma alegacao de que TOE-INTERFACE-001 ou QCU-001 tem status
    Clay-oficial
  - uma reabertura do RH-NOGO-001
  - uma promessa de que todo teste "SURVIVES" fecha sem sorry -- e uma
    aposta informada, nao uma certeza
  - uma tentativa de inflar a contagem de itens: onde a revisao
    adversarial confirmou que uma linha inteira nao rendeu alvo
    pequeno genuino (PN nesta rodada), isso e reportado como tal, nao
    contornado com um item de baixo valor so para preencher a lista
```

Diferenca notavel em relacao a Onda 4: nesta rodada a linha **P vs NP
(PN) rendeu, pela primeira vez desde a Onda 1, zero itens de execucao**.
O proprio recon concluiu que a frente construtor/cobertura-de-mecanismo
esta genuinamente esgotada (todos os 7 construtores de `Stmt` ja cobertos
nas Ondas 3-4: `push`/`pop`/`load`/`branch`/`goto`/`halt`/`peek`), e a
adversarial confirmou essa conclusao por releitura independente de cada
arquivo `PN*.lean` e checagem de `K`/`k0`/`k1` -- o unico candidato
oferecido (`PN-9`, cardinalidade de `K`>1) foi corretamente rebaixado a
"checkbox de cobertura de tipo, nao tecnica de prova nova" e excluido da
lista numerada, exatamente o tratamento que este ciclo reserva para
alvos sem valor genuino em vez de forcar a contagem. Isso e um resultado
legitimo e esperado apos quatro ondas, nao um defeito do processo.

**14** candidatos revisados ao todo nos 9 grupos (8 linhas + infraestrutura
compartilhada). Excluindo `PN-9` (linha PN sem item -- ver acima), a
lista numerada de execucao da Onda 5 tem **14 candidatos distintos**
(15 entradas numeradas na lista, porque `HG-4F` e dividido em dois
passos gated, mesma convencao usada pela Onda 4 para
`YM-CAPSTONE-FULL` e `BSD-1-STEP5-COMPOSE`). Nenhum candidato foi
`REFUTED` nesta rodada -- a adversarial encontrou, em vez disso, varios
gaps de composicao genuinos (`RH-6b`, `HG-4F`, `QF-9`, `SHARED-5A`) que
foram reescopados, nao descartados, e um caso (`NS-5A`) em que a rota de
prova proposta era mais cara do que necessario e foi simplificada.

---

## 1. Riemann Hypothesis (RH) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| RH-6a | Cota de taxa nao-assintotica explicita para a lei-limite de Weyl (`unboundedEigCount`) | SURVIVES | baixo |
| RH-6b | Corolario de consistencia cruzada: ponte de conjunto de RH-5 vs formula exata de eigCount da Onda 1 | NEEDS_NARROWING | baixo-moderado |
| RH-6c | Confirmar formalmente que `Tp` e de fato ilimitado | SURVIVES | baixo |

**Passo original vs. o que mudou.** Todos os tres continuam
inteiramente dentro do `LinearPMap` de brinquedo ja usado por RH-3/RH-4/
RH-5 (Ondas 3-4), sem nenhuma conexao com `riemannZeta`/RVM. RH-6a e
RH-6c fecham lacunas de honestidade/precisao que RH-4 e RH-5 deixaram
abertas por construcao; RH-6b tenta uma ponte de consistencia entre a
formula exata de `eigCount` (Onda 1) e o `unboundedEigCount` de brinquedo
(RH-4/RH-5).

**RH-6a — SURVIVES.** Releitura integral de
`UnboundedEigCountWeylLimitLaw.lean` (RH-4, Onda 4) confirma
`unboundedEigCount_eq_floor` exatamente como descrito. Grep direto no
Mathlib vendorizado confirma `Nat.floor_le`
(`Algebra/Order/Floor/Semiring.lean:47`) e `Nat.lt_floor_add_one`
(mesma secao, linha 63) na posicao exata. Verificacao a mao: para
`Lam>0`, `unboundedEigCount(Lam)/Lam = (⌊Lam⌋₊+1)/Lam`; como
`⌊Lam⌋₊<=Lam`, a razao `<=1+1/Lam`; como `Lam<⌊Lam⌋₊+1`, a razao `>1` --
logo `0 < razao-1 <= 1/Lam` e uma prova de tres linhas a partir dos dois
lemas citados mais aritmetica de divisao, honestamente escopada como
fato de piso de brinquedo sem conteudo zeta/RH.
**Teste revisado:** sem estreitamento necessario -- para `Lam>=1` (ou
`Lam>0`), provar `0 < (unboundedEigCount Lam : R)/Lam - 1 ∧
(unboundedEigCount Lam : R)/Lam - 1 <= 1/Lam` diretamente de
`unboundedEigCount_eq_floor` + `Nat.floor_le` + `Nat.lt_floor_add_one`;
`#print axioms` limpo.

**RH-6b — NEEDS_NARROWING.** Releitura integral de
`EigenvalueSetBridgeRestricted.lean` (RH-5, Onda 4) e de
`SpectralCountingInstance.lean`/`SpectralCounting.lean` (Onda 1)
confirma `eigenvalue_set_eq_preimage` e `eigCount_eq_floor`
(`SpectralCountingInstance.lean:346-349`) exatamente como descrito.
`Set.ncard_preimage_of_injective_subset_range` confirmado em
`Data/Set/Card.lean:832`; `inv_inj` ja usado com sucesso em `C` dentro do
proprio RH-5 (linha 266). Porem: `eigCount` (`SpectralCounting.lean:143-144`)
e definido como `ncard` de um conjunto de tipo `Set R`
(`{μ:R | lam<=|μ| ∧ HasEigenvalue T (μ:C)}`), enquanto o conjunto `S` de
RH-5 e `Set C`. `S.ncard` nao pode igualar literalmente `eigCount T
((Lam+1)⁻¹)` sem um lema intermediario identificando `S` com a imagem
`R->C` do conjunto-limiar de `eigCount`, via `Complex.ofReal_injective`
(`Data/Complex/Basic.lean:102`) + `Complex.norm_real` +
`Set.ncard_image_of_injective` -- passo que o `mathlib_support` do
candidato so gesticula, sem declara-lo no proprio enunciado do teste.
Toda peca Mathlib necessaria para o conserto foi confirmada existente;
e reescopo, nao refutacao.
**Teste revisado:** dividir em tres lemas explicitos em vez de um
enunciado combinado. (1) `{nu:C | HasEigenvalue T nu ∧ (Lam+1)⁻¹<=‖nu‖}
= (Complex.ofReal) '' {mu:R | (Lam+1)⁻¹<=|mu| ∧ HasEigenvalue T (mu:C)}`
via `Complex.norm_real` + `ext`; (2) tomar `ncard` de ambos os lados via
`Set.ncard_image_of_injective` + `Complex.ofReal_injective` para obter
`S.ncard = eigCount T ((Lam+1)⁻¹)` por `eigCount`-def; (3) compor com
`eigenvalue_set_eq_preimage` de RH-5 via
`Set.ncard_preimage_of_injective_subset_range` (precisa da injetividade
de `mu↦(mu+1)⁻¹` + contencao de imagem, ja disponiveis em RH-5) e a
definicao de `unboundedEigCount` para fechar `unboundedEigCount Lam =
eigCount T ((Lam+1)⁻¹)` para `Lam>=0` (com `Lam+1>0` suprindo a
hipotese `0<lam` de `eigCount_eq_floor`).

**RH-6c — SURVIVES (item de menor prioridade, opcional).** Grep confirma
`lp.norm_single` em `Analysis/Normed/Lp/lpSpace.lean:1099` exatamente
como citado. `e i := lp.single 2 i (1:C)`
(`SpectralCountingInstance.lean:107`) da `‖e i‖=1` diretamente.
`Tp_eDom` confere byte-identico em RH-4 (linhas 185-191) e RH-5 (linhas
205-211): `Tp (eDom i) = (i:C) • e i`. Combinado com `norm_smul` e
`Complex.norm_natCast`, da `‖Tp(eDom n)‖=n` para todo `n`, com
`‖eDom n‖` fixo em 1 -- testemunha de ilimitacao limpa via
`exists_nat_gt`. Nem RH-4 nem RH-5 de fato provam nao-limitacao em
nenhum lema (confirmado por leitura de `#print axioms`/corpo dos dois
arquivos) apesar de ambos afirmarem "ilimitado" por nome/construcao --
este item tapa um gap de honestidade real, nao inventado.
**Teste revisado:** sem estreitamento -- provar `¬ ∃ C:R, ∀ x:Tp.domain,
‖(Tp x:H2)‖ <= C * ‖(x:H2)‖` usando `Tp_eDom`, `lp.norm_single` (via
`eDom_coe = e n`), `norm_smul`, `Complex.norm_natCast` e `exists_nat_gt`
para a contradicao final; `#print axioms` limpo (3 axiomas padrao).

---

## 2. Navier-Stokes (NS) — Clay oficial (nucleo Calderon-Zygmund)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| NS-5A | Monotonicidade cruzada-compacta do funcional p.v. envelope (K1<=K2, dois compactos declarados diferentes) | SURVIVES | baixo (revisado para baixo de moderado) |

**Passo original vs. o que mudou.** Continuacao direta de
`PVFunctionalOnArbitraryCompactK.lean` (NS-4a, Onda 4), que ja prova
`pvKCLM_comp_monoCLM_eq_integral` para um compacto `K'` ARBITRARIO e
`pvKCLM_comp_monoCLM_radius_independent` fixando `K'` atraves de dois
raios -- mas nunca compara dois compactos declarados DIFERENTES `K1<=K2`
entre si.

**NS-5A — SURVIVES.** Releitura integral de
`PVFunctionalOnArbitraryCompactK.lean` (1298 linhas) confirma que a
propria secao "O que NAO e afirmado" (linhas 1149-1246) escopa
corretamente para fora o gap(iii) (montagem global
`TestFunction.mkCLM`/`limitCLM`), exatamente como o candidato reconhece.
Todas as citacoes Mathlib conferem exatas por leitura direta:
`TestFunction.mkCLM`/`limitCLM` (`TestFunction.lean:353,370`),
`ContDiffMapSupportedIn.monoCLM`/`monoCLM_apply` (linhas 807/817),
`Bornology.IsBounded.subset_closedBall`/`IsCompact.isBounded`
(`MetricSpace/Bounded.lean:101,192`). Confirmado independentemente que
`integralAgainstBilinCLM` exige `LocallyIntegrableOn`, e que o nucleo
`K(e2,e3;y)~‖y‖^-3` genuinamente NAO e localmente integravel perto de 0
em `R^3` (integral radial `s^-1 ds` diverge) -- a maquinaria `pvKCLM`
custom permanece necessaria, nao substituivel por CLM padrao do Mathlib.
`GAP_REGISTER.yaml` de `02_NAVIER_STOKES` confirmado: NS-GAP-001/002/004/005
`OPEN`, NS-GAP-003 `REFUTED`, nenhum tocado por este candidato.

Analise estrutural independente mostrou que o alvo fecha por uma rota
mais barata do que a proposta original (que refazia um case-split via
`pv_value_radius_independent` do zero): compor uma vez
`pvKCLM_comp_monoCLM_eq_integral` em `K':=K1` e em `K':=K2`, usar
`monoCLM_apply` para colapsar "K1->K2->envelope-R2" para "K1->envelope-R2
direto", depois invocar diretamente o teorema JA PROVADO
`pvKCLM_comp_monoCLM_radius_independent` em `K':=K1` -- sem re-derivar
independencia de raio do zero. Isso reduz o custo estimado de moderado
para baixo. Continua sendo um fato genuinamente novo (nenhum teorema no
arquivo compara literalmente dois compactos `K1<=K2`), honestamente
escopado (deixa intocados a funcao de escolha global `R(-)`, a definicao
intrinseca de `toFun` e a montagem final de `limitCLM`).
**Teste revisado:** provar a igualdade pela rota mais barata: (1)
`pvKCLM e2 e3 R2 hR2 (monoCLM R (monoCLM R f : ContDiffMapSupportedIn E
R 1 K2)) = pvKCLM e2 e3 R2 hR2 (monoCLM R f : ContDiffMapSupportedIn E R
1 (pvKCompact R2))`, via `monoCLM_apply` em ambos os lados (usando
`K1<=K2` e `K2<=pvKCompact R2`); (2) invocar
`pvKCLM_comp_monoCLM_radius_independent e2 e3 K1 R1 R2 hR1 hR2 hK1
(hK1.trans hK2) f` (ja provado) para a igualdade K1-direto-R1 vs
K1-direto-R2; (3) encadear (1)+(2). Se o passo (1) nao elaborar
limpo/defeq, isso E a fricção residual genuina a reportar (possivel
diamante de composicao de `monoCLM` consigo mesmo, dado o proprio aviso
de doc do Mathlib de que o `monoCLM` a nivel de `TestFunction` "nao e
mergulho topologico" -- identidades de composicao de mergulhos sao
exatamente onde tais ressalvas costumam morder).

---

## 3. P vs NP (PN) — Clay oficial

**Linha honestamente esgotada nesta rodada -- zero itens de execucao.**
Releitura independente de `PN8_PeekCoverageWitness.lean` (228 linhas) e
de cada `PN*.lean` (`PN1`, `PN2PRIME`, `PN3`, `PN5`, `PN6`, `PN7`, `PN8`)
confirma que TODOS fixam `K:=Unit`, `k0:=()`, `k1:=()` -- nenhuma
excecao. `Stmt` (`Computability/StackTuringMachine.lean:125-134`) tem
exatamente 7 construtores, todos ja cobertos: `push`
(PN1/PN2PRIME/PN3/PN5), `pop` (mesmos), `load`, `branch` (PN6), `goto`
(PN7), `halt`, `peek` (PN8, Onda 4). `GAP_REGISTER.yaml` confirma que os
unicos gaps `PNP-GAP-*` sao da linha fisica, nenhum sobre cobertura de
`Stmt`/`K`. Confirmado tambem que nem `Language.NP`/`Language.P`/
`NPComplete` existem no checkout Mathlib (zero hits), e que "oracle" so
aparece em `RecursiveIn.lean`/`TuringDegree.lean`.

Correcao factual ao proprio recon (nao muda a conclusao): existe sim uma
prova de correcao TM2-para-TM1 completa (`namespace TM2to1`, ~475
linhas), so que embutida dentro de `StackTuringMachine.lean` (linhas
333-807) em vez de arquivo separado -- e de la que vem as citacoes de
`Function.update_of_ne`/`update_self` usadas na avaliacao de `PN-9`.

O unico candidato oferecido, `PN-9` (maquina multi-pilha, `K` com
cardinalidade >1), foi avaliado como `NEEDS_NARROWING` tecnicamente, mas
a propria adversarial concluiu que sua motivacao esta inflada: as
invocacoes de `Function.update_of_ne` citadas como suporte de
plausibilidade vivem dentro de `TM2to1`, uma prova GERAL sobre indice
`k` simbolico/universalmente quantificado -- nao o caso de `PN-9`, que
propoe `K:=Bool` com indices `k0:=false`, `k1:=true` CONCRETOS e
literais, estruturalmente identicos aos literais `Bool`/`List` ja
fechados por `rfl` puro em PN1/PN2PRIME/PN3/PN5/PN8 (`DecidableEq Bool`
sobre dois literais concretos reduz totalmente no kernel, sem obstaculo
simbolico). O proprio candidato ja se autoavalia como "muito
provavelmente so replicaria o padrao `rfl` sem ensinar nada novo ao
laboratorio" -- a adversarial concordou e recomendou explicitamente NAO
executa-lo como framed (testar "um caminho de codigo genuinamente
diferente"), no maximo logar como checkbox de tipo de uma linha se
alguma vez rodado, nao como item de onda.

**Decisao para esta onda: PN-9 fica de fora da lista numerada de
execucao**, mesmo tratamento que Onda 3/4 deram a itens de
infraestrutura pura -- nao e refutado (o teste como reescopado
provavelmente compila), mas nao ensina nada novo, e forca-lo na lista so
para nao deixar a linha PN em zero seria exatamente o tipo de padding
que este ciclo se propos a nao fazer. **PN e a primeira linha, desde a
Onda 1, a nao contribuir nenhum item para uma lista de execucao.**

---

## 4. Yang-Mills (YM) — Clay oficial (modelo de brinquedo de rede-transferencia 2x2)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| YM-CAPSTONE-DET-BRACKET | `det(toEuclideanCLM M1)` via `lambdaMax*lambda2=det` (SHARED-4B) composto com os brackets de M1 | SURVIVES | baixo |
| YM-CAPSTONE-EIGVAL-DICHOTOMY | Todo autovalor de M1 cai num dos dois brackets disjuntos (`lambdaMax` ou `lambda2`) | SURVIVES | baixo |

**Passo original vs. o que mudou.** Ambos combinam resultados ja
fechados nas Ondas 3-4 (`lambdaMax_mul_lambda2_eq_det` de SHARED-4B,
`lambdaMax_M1_bracket` de YM-CAPSTONE-BRACKET,
`lambda2_M1_bracket_from_compose` e `M1_isHermitian`/
`toEuclideanCLM_M1_isSymmetric`/`finrank_E_eq_two` de YM-CAPSTONE-FULL)
que nunca foram compostos entre si desta forma -- confirmado por grep,
nenhum arquivo pre-existente contem `det(M1)` nem uma alegacao de
exaustividade de autovalor sobre M1.

**YM-CAPSTONE-DET-BRACKET — SURVIVES.** Releitura integral dos quatro
arquivos-fonte (`YMCapstoneBracket.lean` 481 linhas,
`YMCapstoneFull.lean` 731 linhas, `LambdaMaxMulLambda2EqDet.lean` 287
linhas, `TwoEigenvalueExhaustiveness.lean` 287 linhas) confirma cada
peca citada exatamente: `lambdaMax_mul_lambda2_eq_det` (linhas 266-274,
construido de `LinearMap.IsSymmetric.det_eq_prod_eigenvalues`,
`Analysis/InnerProductSpace/Spectrum.lean:391`, + `Fin.prod_univ_two`,
`Algebra/BigOperators/Fin.lean:111`); `M1_isHermitian`/
`toEuclideanCLM_M1_isSymmetric`/`finrank_E_eq_two`
(`YMCapstoneFull.lean:621-631`); `lambdaMax_M1_bracket` `[2.9,3.1]`
(`YMCapstoneBracket.lean:444-450`) e `lambda2_M1_bracket_from_compose`
`[7/10,13/10]` (`YMCapstoneFull.lean:686-692`), ambos ja fechados sem
`sorry`. Aritmetica de intervalo verificada a mao: produto minimo
`2.9*0.7=2.03`, produto maximo `3.1*1.3=4.03`, ambos os limites
inferiores positivos (sem risco de flip de sinal). `GAP_REGISTER.yaml`
de `04_YANG_MILLS` confirmado: os 7 gaps `YM-GAP-*` sao todos sobre a
teoria real/limite continuo/literatura, nenhum toca esta sub-linha de
brinquedo.
**Teste:** provar `2.03 <= det(toEuclideanCLM M1) <= 4.03` via `have
hdet := lambdaMax_mul_lambda2_eq_det (toEuclideanCLM M1)
toEuclideanCLM_M1_isSymmetric finrank_E_eq_two; constructor <;>
nlinarith [...]`. Se `nlinarith` nao fechar diretamente, fallback e um
`mul_le_mul` explicito de duas linhas (ambos os limites sao positivos)
em vez de tratar falha de `nlinarith` como invalidando o candidato.

**YM-CAPSTONE-EIGVAL-DICHOTOMY — SURVIVES.** Confirmado
`eigenvalue_eq_lambdaMax_or_lambda2` exatamente como descrito
(`TwoEigenvalueExhaustiveness.lean:265-274`), construido de
`exists_eigenvalues_eq` + os dois lemas promovidos
(`lambdaMax_eq_eigenvalues_zero`, `lambda2_eq_eigenvalues_one`) +
`fin_cases i`, sem gap nem `sorry`. Substituicao direta e de baixo risco
(mesmos pre-requisitos de M1 ja fechados de YM-CAPSTONE-FULL). Grep
confirma nenhuma alegacao previa de exaustividade sobre TODOS os
autovalores de M1 (so existencia de UM autovalor igual a `lambda2`,
fato estritamente mais fraco) -- novidade genuina, estritamente mais
forte que o ja existente. A caveat honesta do proprio candidato ("nao
tight" -- autovalores reais ~3.051/~1.049 sentam bem dentro das metades
disjuntas dos brackets) e mantida sem suavizacao.
**Teste:** para o `E` 2-dim fixo e `toEuclideanCLM M1` simetrico, provar
`(2.9<=mu<=3.1) ∨ (0.7<=mu<=1.3)` para todo autovalor `mu`, via `rcases
eigenvalue_eq_lambdaMax_or_lambda2 _ toEuclideanCLM_M1_isSymmetric
finrank_E_eq_two hmu with h | h` seguido de substituicao dos dois
brackets ja fechados. Sem estreitamento necessario -- ja e uma
composicao minima e atomica.

---

## 5. Hodge Conjecture (HG) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| HG-4E | Empacotar `IsHolomorphicTransition` como `Subgroup` genuino de `(C -> C)ˣ` | SURVIVES | moderado |
| HG-1G | Parametrizar totalmente a identidade Num/Den de HG-1F sobre `(n0,d0:Z)` arbitrarios | SURVIVES | baixo |
| HG-4F | (esticado) propriedade de subgrupo proprio via `exp(conj z)` | NEEDS_NARROWING (dividido em dois estagios) | baixo-moderado (estagio 1) / moderado, gated (estagio 2) |

**Passo original vs. o que mudou.** `HG-4E` e `HG-1G` sao continuacoes
diretas de gaps ja nomeados nos proprios arquivos da Onda 4
(`isHolomorphicTransition_mul`/`_inv` de HG-4D nunca empacotados num
`Subgroup`; identidade num/den de HG-1F nunca generalizada apos HG-1E
generalizar `principalCycle`). `HG-4F` e um esticado explicitamente
marcado como tal pelo proprio recon, e a adversarial confirmou que seu
titulo ("propriedade") excede o que seu proprio teste falsificavel
prova.

**HG-4E — SURVIVES.** Releitura integral de
`HolomorphicTransitionMulInvClosureProbe.lean` confirma
`isHolomorphicTransition_mul`/`_inv` (HG-4D, Onda 4) como dois
corolarios desconectados, nenhum objeto `Subgroup` montado ainda -- gap
real. Toda citacao Mathlib conferida no local exato: `Pi.monoid`
(`Algebra/Group/Pi/Basic.lean:72`), `Pi.commMonoid` (:80),
`Pi.divisionMonoid` (:99), `Units.instCommGroupUnits`
(`Algebra/Group/Units/Defs.lean:266`), `Units.val_inv_eq_inv_val` (:280),
`GroupWithZero.toDivisionMonoid` (`Algebra/GroupWithZero/Basic.lean:376`),
`Pi.isUnit_iff`/`IsUnit.apply` (`Algebra/Group/Pi/Units.lean:31,41`),
`structure Subgroup` (`Algebra/Group/Subgroup/Defs.lean:295`). Prova
mecanicamente solida: `mul_mem'`/`one_mem'`/`inv_mem'` via as pecas
citadas. Risco real e nao-fatal identificado independentemente: possivel
fricção de diamante de instancia entre o `Monoid` usado para formar
`(C->C)ˣ` e o `DivisionMonoid` necessario para `val_inv_eq_inv_val`
(padrao usualmente benigno para tipos `Pi` a valores em corpo, mas
justifica custo "moderado" em vez de "baixo").
**Teste:** como proposto, com fallback explicito: se
`val_inv_eq_inv_val` encontrar erro de diamante de instancia ao
descarregar `inv_mem'`, cair para provar `↑u⁻¹ = (↑u)⁻¹` diretamente e
pontualmente em vez de depender da cadeia de instancia `DivisionMonoid`
via `Pi`.

**HG-1G — SURVIVES.** Releitura integral de
`HG1EPrincipalCycleA0Probe.lean` e `HG1FPrincipalCycleNumDenProbe.lean`
confirma exatamente o gap alegado: `principalCycle_a0(a0:Z)(ha0:a0!=0)`
de HG-1E ja e genuinamente parametrizado, mas `principalCycle_f_eq_sub`
de HG-1F so e provado para o par fixo `Num.a0=3`/`Den.a0=2`, re-derivando
`hkey`/`hord` localmente em vez de reusar a construcao parametrizada de
HG-1E. Citacoes Mathlib conferidas:
`Function.locallyFinsuppWithin.ext` (`Topology/LocallyFinsupp.lean:147`,
recon citou 146-148, imprecisao cosmetica de uma linha, sem efeito),
`Function.locallyFinsuppWithin.coe_sub` (linha 352), `Scheme.ord_mul`
(`AlgebraicGeometry/OrderOfVanishing.lean:81`, incondicional em `x`).
Generalizacao direta e de baixo risco -- mesmo tipo de movimento de
reindexacao que HG-1B/HG-1D ja passaram para HG-1C/HG-1E.
**Teste:** como proposto -- generalizar sobre a base ja generalizada de
HG-1E em vez de refazer a construcao Num/Den fixa; nota cosmetica sobre
a citacao de linha de `.ext` corrigida acima.

**HG-4F — NEEDS_NARROWING.** Releitura integral de
`ConjugationNotHolomorphicProbe.lean` (HG-4b) confirma que `conj(0)=0`
torna esse arquivo invalido como testemunha de nao-anulamento -- achado
correto e nao previamente documentado. Toda peca Mathlib do argumento
esticado existe: `Complex.hasDerivAt_exp`
(`Analysis/SpecialFunctions/ExpDeriv.lean:88`), `HasFDerivAt.comp`
(`Analysis/Calculus/FDeriv/Comp.lean:105`, exige linearidade sobre o
MESMO `𝕜` -- relevante abaixo), `Complex.exp_ne_zero`
(`Analysis/Complex/Exponential.lean:162`, existe mas nao pinada por
linha no recon original -- flag honesto, confirmado real apos busca mais
ampla). O recon tambem omitiu uma peca de ponte necessaria:
`HasDerivAt.hasFDerivAt` (`Analysis/Calculus/Deriv/Basic.lean:202`),
precisa para converter a forma escalar de `Complex.hasDerivAt_exp` para
`HasFDerivAt` antes de `.restrictScalars`/`.comp` -- gap real mas
consertavel, nao refutacao. O nucleo matematico e solido (argumento de
contradicao escalado por `c=exp(conj x)!=0`, analogo a HG-4b). Mas o
NOME do candidato ("propriedade de subgrupo proprio") excede o que seu
proprio teste falsificavel prova: o teste declarado so estabelece `¬
Differentiable C (exp ∘ conj)`, sem empacotar `exp∘conj` como termo de
`(C->C)ˣ`, sem mostrar que esse termo cai fora do carrier de HG-4E, e
sem que o `Subgroup` de HG-4E sequer exista ainda para se falar em
"proprio".
**Teste revisado, dividido em dois estagios explicitos:** Estagio 1
(auto-contido, executavel agora) -- provar `¬ Differentiable C
(Complex.exp ∘ starRingEnd C)` via a cadeia de regra da cadeia
esboçada, citando `HasDerivAt.hasFDerivAt` explicitamente como o passo
de ponte que faltava. Estagio 2 (gated em `HG-4E`, so apos o `Subgroup`
existir) -- empacotar `exp∘conj` como termo `u:(C->C)ˣ` (via
`Complex.exp_ne_zero` + `Pi.isUnit_iff.mpr` + `isUnit_iff_ne_zero`),
depois provar `u ∉ HolomorphicTransitionSubgroup.carrier` usando o
resultado do Estagio 1, concluindo
`HolomorphicTransitionSubgroup != ⊤`. So o sucesso do Estagio 2, nao do
Estagio 1 isolado, justificaria chamar isso de resultado de
"propriedade".

---

## 6. Birch and Swinnerton-Dyer (BSD) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| BSD-6 | `WeierstrassCurve.LFunction` determinada por/fatoravel via valores em potencias de primo (`IsMultiplicative.eq_iff_eq_on_prime_powers`) | NEEDS_NARROWING | baixo |

**Contexto factual.** `BSD-GAP-007` fechou genuinamente na Onda 4
(`BSD1Step5Compose.lean`, verificado com escrutinio extra na sessao de
execucao). `BSD-GAP-008` (Mordell-Weil fraco, cinco lacunas formais
separadas) permanece `OPEN` e nao relacionado a este candidato.

**BSD-6 — NEEDS_NARROWING.** Releitura integral de
`BSD1Step5Compose.lean` confirma `WeierstrassCurve.LFunction_isMultiplicative`
provado incondicionalmente (linhas 370-372). `GAP_REGISTER.yaml`
confirmado: `BSD-GAP-007` `CLOSED` (2026-08-10,
`WAVE4-BSD-1-STEP5-COMPOSE`), `BSD-GAP-008` `OPEN`, nenhum tocado por
este item. Cross-check direto em
`Mathlib/NumberTheory/ArithmeticFunction/Defs.lean` confirma
`multiplicative_factorization` (linha 546) e
`eq_iff_eq_on_prime_powers` (linha 564) exatamente, dentro de `namespace
IsMultiplicative`, sob `[CommMonoidWithZero R]` -- satisfeito por
`ArithmeticFunction Z`, o codominio de `LFunction`
(`LFunction.lean:79-85`). Confirmado que nenhum dos dois lemas e
referenciado hoje em nenhum arquivo do laboratorio (fora `.lake/`).
Confirmado tambem que `ArithmeticFunction.eulerProduct` (usado por
`LFunction`) e a construcao pontual/formal sem hipotese `Summable`,
distinta do `EulerProduct.eulerProduct` com convergencia real -- ou
seja, nenhum conteudo analitico e tocado por este item, so
multiplicatividade formal. Gap real encontrado: a rationale do candidato
alega DOIS corolarios como conteudo novo
(`multiplicative_factorization` e `eq_iff_eq_on_prime_powers`), mas o
teste falsificavel so constroi e typechecka UMA declaracao
(`eq_iff_eq_on_prime_powers`) -- escopo alegado excede o que o proprio
gate verifica. Consertavel por narrowing, nao refutacao.
**Teste revisado:** (a) escopo minimo recomendado -- so
`LFunction_eq_iff_eq_on_prime_powers`, exatamente como no teste
original, descartando a alegacao de `multiplicative_factorization`; OU
(b) se ambos forem reportados, adicionar uma segunda declaracao
autonoma com seu proprio `lake env lean`/`#print axioms`:
`theorem LFunction_apply_eq_prod_prime_powers {K} [Field K]
[NumberField K] (W : WeierstrassCurve K) {n : N} (hn : n != 0) :
W.LFunction n = n.factorization.prod fun p k => W.LFunction (p ^ k) :=
(LFunction_isMultiplicative W).multiplicative_factorization _ hn` --
ambas devem sair 0/limpas antes de qualquer uma ser reportada como
fechada. Em qualquer caso, nada sobre BSD em si e tocado mesmo em pleno
sucesso -- restatement puramente formal de multiplicatividade, zero
conteudo de convergencia/continuacao analitica/equacao
funcional/conductor/Mordell-Weil.

---

## 7. Sintese TOE (extensao interna do laboratorio — NAO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| TOE-5 | Fortalecer o resultado "sem funtor reverso" para qualquer `G` com `G.obj` injetivo (nao so `hG` fixo) | SURVIVES | baixo |

**Passo original vs. o que mudou.** Continuacao direta de
`KToShiftFunctorNotFaithfulNoReverse.lean` (TOE-4, Onda 4), cujo
`no_reverse_functor_with_fixed_objects` e provado SOMENTE sob a hipotese
`hG : G.obj p = show KCat from p.back` (linhas 231-233), com a propria
secao "O que este arquivo NAO estabelece" (linhas 81-84) nomeando
explicitamente o caso irrestrito como fora de escopo -- exatamente o gap
que `TOE-5` ataca.

**TOE-5 — SURVIVES.** Releitura integral de
`KToShiftFunctorNotFaithfulNoReverse.lean`,
`MonoidKConstantActionDistinctEndomorphisms.lean`,
`HomKNotIsoActionCategoryK.lean`,
`MonoidKNonPretransitiveZigzagConnected.lean`, `ActionCategoryRegime3.lean`,
`Regime3.lean` e do Mathlib (`CategoryTheory/Action.lean`,
`Data/Fintype/Card.lean`, `CategoryTheory/Functor/Const.lean`) confirma
todas as pecas: `Kact` (`.identity r = r`, `.k _ = .alpha`, linhas
148-150) da `Hom_K(p,q)` nao-vazio sse `q=p` ou `q=alpha`;
`shiftCat_hom_nonempty` (`KToShiftFunctorNotFaithfulNoReverse.lean:170-171`)
ja provado para TODO par ordenado `p q : ShiftCat` (peca ja disponivel,
nao a re-provar); doc-comment do Mathlib citado verbatim e correto
(`Action.lean:47`); `Finite.injective_iff_bijective`
(`Data/Fintype/Card.lean:342`) e `Functor/Const.lean:36` confirmados.
Grep no laboratorio confirma nenhum uso previo de
`Injective`/`Bijective` sobre objetos estilo `ActionCategory` --
territorio genuinamente novo para TOE. Verificacao a mao do argumento
central: se `G.obj` e injetivo, `sigma := back o G.obj o coe` e injetivo
em `Regime3` (3 elementos); para qualquer `q`, escolhendo `p!=q`,
`Hom_Shift(p,q)` nao-vazio (ja provado para todo par) forca via `G.map`
que `Hom_K(sigma p,sigma q)` e nao-vazio, entao `sigma q = sigma p` ou
`sigma q = alpha`; injetividade + `p!=q` descarta a primeira opcao,
forcando `sigma q = alpha` para TODO `q` -- mas dois `q` distintos (ex.
`beta`,`gamma`) mapeando ambos para `alpha` contradiz injetividade.
Argumento correto e genuina generalizacao nao-trivial do resultado
condicional da Onda 4 (o caso `hG` e exatamente o caso especial em que
`G.obj` e a bijecao canonica, logo injetiva). Um defeito de
sobre-engenharia (nao fatal) foi encontrado: o esboco original invoca
`Finite.injective_iff_bijective` antes do case-split, mas o argumento
direto de pombos (dois elementos distintos ambos forcados a `alpha`,
contradizendo injetividade pura) fecha sem nunca precisar de
sobrejetividade/bijetividade -- dependencia Mathlib inessencial a
remover.
**Teste revisado:** mesmo enunciado
(`no_injective_reverse_functor (G : ShiftCat ⥤ KCat) (hinj :
Function.Injective G.obj) : False`), mas sem o desvio por
`Finite.injective_iff_bijective`/sobrejetividade. Em vez disso: (1)
provar `homK_nonempty_iff (x y : Regime3) : (∃ m:K, m • x = y) -> y = x
∨ y = Regime3.alpha` via `revert x y; decide` (6 casos, generalizacao
direta do padrao `homK_beta_gamma_no_witness` ja existente); (2) definir
`sigma` via `back`/coe, injetivo a partir de `hinj`; (3) para `q:=beta`,
instanciar `p:=gamma` (`gamma!=beta`) e usar `shiftCat_hom_nonempty
gamma beta` + `G.map` + `homK_nonempty_iff` para obter `sigma beta =
sigma gamma ∨ sigma beta = alpha`; injetividade + `gamma!=beta` descarta
o primeiro disjunto, dando `sigma beta = alpha`; argumento simetrico com
`p:=beta` da `sigma gamma = alpha`; concluir `sigma beta = sigma gamma =
alpha` com `beta!=gamma`, contradizendo injetividade de `sigma`
diretamente (sem bijetividade/sobrejetividade).

---

## 8. Fundamentos Quanticos / Unificacao (extensao interna — NAO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| QF-8 | Preservacao de norma/produto interno sob o fluxo de Heisenberg | SURVIVES | baixo-moderado |
| QF-9 | Lei de grupo a um parametro `exp((s+t)•H) = exp(s•H)*exp(t•H)` | NEEDS_NARROWING | baixo |

**Passo original vs. o que mudou.** Ambos continuam diretamente de
`HeisenbergFlowUnitarity.lean` (QF-7, Onda 4), que prova `exp(t•H) ∈
unitary(...)` para `t:R` e nomeia explicitamente, na propria secao
"AINDA FALTANDO", tanto preservacao de norma/produto interno (item c)
quanto a lei de grupo como passos nao tentados.

**QF-8 — SURVIVES.** Releitura integral de `HeisenbergFlowUnitarity.lean`
confirma exatamente a caracterizacao do gap. Toda citacao Mathlib
re-verificada por grep/leitura direta no snapshot vendorizado:
`Matrix.toEuclideanCLM` (`CStarAlgebra/Matrix.lean:102-107`, `≃⋆ₐ[𝕜]`
genuino, incondicional); `unitary.map_mem` (`Algebra/Star/Unitary.lean:300`,
precisa `FunLike+StarHomClass+MonoidHomClass`); `norm_map_of_mem_unitary`/
`inner_map_map_of_mem_unitary` (`InnerProductSpace/Adjoint.lean:862,868`).
Cadeia de instancia rastreada um nivel mais fundo que o recon original e
confirmada fechar: `NonUnitalAlgEquivClass` (`StarAlgHom.lean:648,704`)
estende `RingEquivClass`, que tem instancia `toRingHomClass`
(`Ring/Equiv.lean:~102`) dando `RingHomClass`, que estende
`MonoidHomClass` (`Ring/Hom/Defs.lean:326-328`) -- um salto a mais que o
recon original descreveu, mas chegando no mesmo lugar. `StarHomClass`
resolve via `StarRingEquivClass->StarHomClass`
(`StarRingHom.lean:262-264`). Nada fabricado. Risco residual genuino
(nao fatal): cadeia de typeclass de 4-5 saltos, e o proprio cabecalho de
QF-7 documenta um diamante de topologia/instancia especifico do escopo
`Matrix.Norms` que ja mordeu nesta base de codigo -- compilacao limpa de
primeira e plausivel mas nao garantida. `QCU-001` continua `UNSCOPED`
(confirmado em `SCOPE.md`); mesmo em pleno sucesso, isso prova so uma
identidade de norma para um gerador 2x2 fixo nao-fisico, sem operadores
ilimitados, sem evolucao de estado fisico, sem ponte a limite classico.
**Teste:** como proposto -- provar preservacao de norma/produto interno
sob `exp(t•heisenbergGenerator)` via `Matrix.toEuclideanCLM` +
`unitary.map_mem` + `norm_map_of_mem_unitary`/
`inner_map_map_of_mem_unitary`, reusando a prova de unitariedade de QF-7
como hipotese de entrada.

**QF-9 — NEEDS_NARROWING.** `NormedSpace.exp_add_of_commute`
(`Exponential.lean:520-521`) confirmado exato, sem condicao de
pertencer-a-bola. Mas a secao ambiente `section Rat`
(`Exponential.lean:503-624`) exige `[NormedAlgebra Q A]`, e o proprio
cabecalho de QF-7 documenta que `NormedAlgebra Q (Matrix (Fin 2)(Fin 2)
C)` deliberadamente NAO e instancia global (para evitar outro diamante),
precisando ser suprida a mao via `haveI : NormedAlgebra Q (Matrix (Fin
2)(Fin 2) C) := NormedAlgebra.restrictScalars Q C (Matrix (Fin 2)(Fin 2)
C)`. O trecho Lean colado no candidato original OMITE esse `haveI` --
como literalmente escrito, falharia na busca de instancia exatamente
como QF-7 falhou antes do conserto manual. Gap real e concreto no teste
como escrito, nao um problema fundamental da alegacao subjacente (o
conserto ja e conhecido e e uma linha). Encadeamento de `Commute`
(`.smul_right`/`.smul_left`) ja usado com sucesso em QF-5/QF-6/QF-7 para
o mesmo gerador -- baixo risco por precedente direto.
**Teste revisado:** `theorem heisenbergFlow_add (s t : R) : exp ((s + t)
• heisenbergGenerator) = exp (s • heisenbergGenerator) * exp (t •
heisenbergGenerator) := by haveI : NormedAlgebra Q (Matrix (Fin 2)(Fin
2) C) := NormedAlgebra.restrictScalars Q C (Matrix (Fin 2)(Fin 2) C);
rw [add_smul]; exact exp_add_of_commute (((Commute.refl
heisenbergGenerator).smul_right t).smul_left s)` -- o `haveI` explicito
e obrigatorio, exatamente como em QF-7. O escopo `Matrix.Norms.Operator`
(mais simples, usado por QF-4/5/6) tambem deve ser tentado primeiro,
antes do `Matrix.Norms.L2Operator` especifico de QF-7 (que tem o
diamante `ContinuousStar` documentado) -- `exp_add_of_commute` nao
precisa de `StarRing`/`ContinuousStar`, entao pode evitar essa fricção
inteiramente; reportar qual escopo de fato fechou.

---

## Infraestrutura compartilhada entre frentes (continuacao)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| SHARED-5A | Fatoracao do polinomio caracteristico simetrico em dimensao 2 | NEEDS_NARROWING | baixo (revisado para baixo de moderado) |

**Passo original vs. o que mudou.** Continuacao dos dois itens SHARED-4A/
4B (Onda 4), que ja promoveram `heq0`/`hlambda2` a teoremas nomeados
(`lambdaMax_eq_eigenvalues_zero`/`lambda2_eq_eigenvalues_one`).

**SHARED-5A — NEEDS_NARROWING.** Toda citacao Mathlib do candidato
original conferiu por grep/leitura direta: `Matrix.charpoly_fin_two`
(`LinearAlgebra/Matrix/Charpoly/Coeff.lean:229`), `LinearMap.det_toMatrix`
(`Determinant.lean:212`), `LinearMap.trace_eq_matrix_trace`
(`Trace.lean:87`), `LinearMap.charpoly_toMatrix`
(`Charpoly/ToMatrix.lean:43`, recon citou 44-46, imprecisao imaterial).
Nenhuma citacao fabricada. Porem, ao checar a vizinhanca de
`LinearMap.IsSymmetric.det_eq_prod_eigenvalues` (o lema que SHARED-4B ja
cita e usa, `Spectrum.lean:391`), foi encontrado um lema
DRAMATICAMENTE mais direto na MESMA secao `Version2` (que fixa `T : E
→ₗ[𝕜] E`, exatamente o escopo de SHARED-4A/4B):
`LinearMap.IsSymmetric.charpoly_eq` (`Spectrum.lean:357-360`), provando
para QUALQUER `n` finito -- nao so 2 -- `T.charpoly = ∏ i, (X - C
(hT.eigenvalues hn i))`. Especializado a `n=2` via `Fin.prod_univ_two`
(ja citado pelo candidato) e substituido pelos ja-fechados
`lambdaMax_eq_eigenvalues_zero`/`lambda2_eq_eigenvalues_one`, isso da
`(T:E →ₗ[R] E).charpoly = (X - C (lambdaMax T)) * (X - C (lambda2 T))`
DIRETAMENTE -- sem `Matrix.charpoly_fin_two`, sem ponte
`ToMatrix`/`det`/`trace`, sem base explicita (`EuclideanSpace.basisFun`).
O alvo NAO e trivial como o ja-corretamente-rejeitado identidade de
traco -- `charpoly_eq` e um teorema Mathlib nao-trivial baseado em
diagonalizacao, nao um `unfold` gratuito -- entao continua sendo um fato
empacotado legitimo e novo, so com custo/risco menor do que o candidato
original estimou (a rota corrigida ja compila dentro do proprio
Mathlib para exatamente essa forma T/E/hT, nao e API nova para o
laboratorio).
**Teste revisado:** para `E := EuclideanSpace R (Fin 2)`, `T : E →L[R]
E`, `hT : (T:E →ₗ[R] E).IsSymmetric`, `hn : Module.finrank R E = 2`
(reproduzindo `lambdaMax`/`lambda2`/`lambdaMax_eq_eigenvalues_zero`/
`lambda2_eq_eigenvalues_one` verbatim de SHARED-4A/4B), provar
`(T:E →ₗ[R] E).charpoly = (Polynomial.X - Polynomial.C (lambdaMax T)) *
(Polynomial.X - Polynomial.C (lambda2 T))` via (a) `hT.charpoly_eq hn`
para reescrever o LHS para `∏ i, (X - C (hT.eigenvalues hn i))`; (b)
`Fin.prod_univ_two` para desdobrar; (c) reescrever com
`lambdaMax_eq_eigenvalues_zero`/`lambda2_eq_eigenvalues_one` e fechar
por `rfl`/`rw`. Sem `Matrix.charpoly_fin_two`, sem ponte `ToMatrix`, sem
base explicita. Se o passo (a) nao typechecar (ex. descasamento de cast
`RCLike` entre a forma geral de `charpoly_eq` e a especializacao
`𝕜:=R` deste arquivo), reportar como gap especifico e estreito em vez de
recuar para a rota mais pesada mediada por base.

---

## Lista de execucao Onda 5 (despacho direto para agente de formalizacao)

Cada item abaixo traz o candidato, o teorema-alvo, e o enunciado de
teste exato (ja revisado pela adversarial), pronto para um agente de
formalizacao executar sem reinterpretacao. Ordem: por linha, mesma
sequencia das secoes acima. Todos sao independentes entre si a menos que
anotado. A linha PN nao contribui item algum (ver secao 3 acima).

```text
 1. RH / RH-6a (cota de taxa nao-assintotica da lei-limite de Weyl)
    Para Lam>=1 (ou Lam>0), provar 0 < (unboundedEigCount Lam : R)/Lam -
    1 ∧ (unboundedEigCount Lam : R)/Lam - 1 <= 1/Lam, diretamente de
    unboundedEigCount_eq_floor + Nat.floor_le + Nat.lt_floor_add_one.
    #print axioms limpo.

 2. RH / RH-6b (ponte de consistencia cruzada, revisada em 3 lemas)
    (i) {nu:C | HasEigenvalue T nu ∧ (Lam+1)⁻¹<=‖nu‖} = (Complex.ofReal)
    '' {mu:R | (Lam+1)⁻¹<=|mu| ∧ HasEigenvalue T (mu:C)}, via
    Complex.norm_real + ext; (ii) tomar ncard de ambos os lados via
    Set.ncard_image_of_injective + Complex.ofReal_injective para obter
    S.ncard = eigCount T ((Lam+1)⁻¹); (iii) compor com
    eigenvalue_set_eq_preimage (RH-5) via
    Set.ncard_preimage_of_injective_subset_range para fechar
    unboundedEigCount Lam = eigCount T ((Lam+1)⁻¹) para Lam>=0.

 3. RH / RH-6c (confirmar ilimitacao formal de Tp)
    Provar ¬ ∃ C:R, ∀ x:Tp.domain, ‖(Tp x:H2)‖ <= C * ‖(x:H2)‖ usando
    Tp_eDom, lp.norm_single, norm_smul, Complex.norm_natCast e
    exists_nat_gt. #print axioms limpo (3 axiomas padrao).

 4. NS / NS-5A (monotonicidade cruzada-compacta, rota barata)
    (1) pvKCLM e2 e3 R2 hR2 (monoCLM R (monoCLM R f : ... K2)) =
    pvKCLM e2 e3 R2 hR2 (monoCLM R f : ... (pvKCompact R2)) via
    monoCLM_apply em ambos os lados (usando K1<=K2 e K2<=pvKCompact R2);
    (2) invocar pvKCLM_comp_monoCLM_radius_independent (ja provado) em
    K':=K1; (3) encadear. Se (1) nao elaborar limpo, reportar a fricção
    exata (possivel diamante de composicao de monoCLM).

 5. YM / YM-CAPSTONE-DET-BRACKET (det(M1) via lambdaMax*lambda2)
    Provar 2.03 <= det(toEuclideanCLM M1) <= 4.03 via have hdet :=
    lambdaMax_mul_lambda2_eq_det (toEuclideanCLM M1)
    toEuclideanCLM_M1_isSymmetric finrank_E_eq_two; constructor <;>
    nlinarith [...]. Fallback: mul_le_mul explicito se nlinarith nao
    fechar.

 6. YM / YM-CAPSTONE-EIGVAL-DICHOTOMY (exaustividade de autovalor de M1)
    Provar (2.9<=mu<=3.1) ∨ (0.7<=mu<=1.3) para todo autovalor mu de
    toEuclideanCLM M1, via rcases
    eigenvalue_eq_lambdaMax_or_lambda2 _ toEuclideanCLM_M1_isSymmetric
    finrank_E_eq_two hmu with h | h, substituindo os dois brackets ja
    fechados.

 7. HG / HG-4E (Subgroup de IsHolomorphicTransition)
    Construir HolomorphicTransitionSubgroup <= (C->C)ˣ via mul_mem'/
    one_mem'/inv_mem', usando isHolomorphicTransition_mul/_inv (HG-4D) +
    Units.val_inv_eq_inv_val + Pi.isUnit_iff. Fallback se diamante de
    instancia: provar ↑u⁻¹ = (↑u)⁻¹ pontualmente em vez de via a cadeia
    DivisionMonoid.

 8. HG / HG-1G (parametrizacao total da identidade Num/Den de HG-1F)
    Generalizar principalCycle_f_eq_sub sobre a base ja parametrizada de
    HG-1E (a0:Z, ha0:a0!=0) em vez do par fixo Num.a0=3/Den.a0=2,
    reusando genf/finite_support_ord_genf parametrizados.

 9. HG / HG-4F -- Estagio 1 (nao-diferenciabilidade de exp∘conj,
    autonomo)
    Provar ¬ Differentiable C (Complex.exp ∘ starRingEnd C), via
    Complex.hasDerivAt_exp + HasDerivAt.hasFDerivAt (ponte explicita) +
    HasFDerivAt.comp + contradicao de linearidade-C escalada por
    c=exp(conj x)!=0 (Complex.exp_ne_zero).

10. HG / HG-4F -- Estagio 2 (gated em #7/HG-4E, propriedade de subgrupo
    proprio)
    Empacotar exp∘conj como u:(C->C)ˣ (via Complex.exp_ne_zero +
    Pi.isUnit_iff.mpr + isUnit_iff_ne_zero); provar u ∉
    HolomorphicTransitionSubgroup.carrier usando o resultado do Estagio
    1; concluir HolomorphicTransitionSubgroup != ⊤. So tentar apos #7
    fechar; nao alegar "propriedade" so com o Estagio 1.

11. BSD / BSD-6 (LFunction determinada por valores em potencias de
    primo)
    Escopo minimo: theorem LFunction_eq_iff_eq_on_prime_powers ... :=
    (LFunction_isMultiplicative W).eq_iff_eq_on_prime_powers ... .
    Extensao opcional (declaracao SEPARADA, seu proprio check):
    LFunction_apply_eq_prod_prime_powers via
    .multiplicative_factorization. Nao alegar ambos fechados a menos que
    ambos passem lake env lean/#print axioms individualmente.

12. TOE / TOE-5 (sem funtor reverso injetivo, generalizado)
    theorem no_injective_reverse_functor (G : ShiftCat ⥤ KCat) (hinj :
    Function.Injective G.obj) : False, via (1) homK_nonempty_iff (x y :
    Regime3) : (∃ m:K, m • x = y) -> y = x ∨ y = Regime3.alpha (revert
    x y; decide); (2) sigma injetivo via hinj; (3) para q:=beta,
    p:=gamma (e simetricamente p:=beta, q:=gamma) via
    shiftCat_hom_nonempty + G.map + homK_nonempty_iff, forcar sigma
    beta = sigma gamma = alpha com beta!=gamma, contradizendo
    injetividade de sigma diretamente (sem Finite.injective_iff_bijective).

13. QF / QF-8 (preservacao de norma/produto interno sob o fluxo de
    Heisenberg)
    Provar preservacao de norma e produto interno sob exp(t•
    heisenbergGenerator) via Matrix.toEuclideanCLM + unitary.map_mem +
    norm_map_of_mem_unitary/inner_map_map_of_mem_unitary, reusando a
    prova de unitariedade de QF-7.

14. QF / QF-9 (lei de grupo a um parametro do fluxo de Heisenberg)
    theorem heisenbergFlow_add (s t : R) : exp ((s + t) •
    heisenbergGenerator) = exp (s • heisenbergGenerator) * exp (t •
    heisenbergGenerator) := by haveI : NormedAlgebra Q (Matrix (Fin 2)
    (Fin 2) C) := NormedAlgebra.restrictScalars Q C (Matrix (Fin 2)
    (Fin 2) C); rw [add_smul]; exact exp_add_of_commute (((Commute.refl
    heisenbergGenerator).smul_right t).smul_left s). Tentar primeiro sob
    o escopo Matrix.Norms.Operator (mais simples); reportar qual escopo
    de fato fechou.

15. SHARED-INFRA / SHARED-5A (fatoracao do polinomio caracteristico
    simetrico em dim 2, rota barata via charpoly_eq)
    Para E:=EuclideanSpace R (Fin 2), T : E →L[R] E, hT :
    (T:E →ₗ[R] E).IsSymmetric, hn : Module.finrank R E = 2, provar
    (T:E →ₗ[R] E).charpoly = (X - C (lambdaMax T)) * (X - C (lambda2
    T)) via hT.charpoly_eq hn + Fin.prod_univ_two +
    lambdaMax_eq_eigenvalues_zero/lambda2_eq_eigenvalues_one. Sem
    Matrix.charpoly_fin_two, sem ponte ToMatrix, sem base explicita.
```

Total: **15 entradas numeradas**, correspondendo a **14 candidatos
distintos** (itens 9/10 formam um unico candidato `HG-4F` dividido em
dois estagios gated, mesma convencao ja usada pelas Ondas 3-4 para
`BSD-1-STEP3`/`STEP4` e `YM-CAPSTONE-FULL`/`BSD-1-STEP5-COMPOSE`).
Contando por CANDIDATO (nao por linha numerada): RH(3) + NS(1) + PN(0) +
YM(2) + HG(3) + BSD(1) + TOE(1) + QF(2) + SHARED-INFRA(1) = **14**.
Mesma contagem numerica que a Onda 4, mas por composicao diferente --
PN caiu de 1 para 0 (linha esgotada), enquanto RH subiu de 2 para 3 e HG
subiu de 3 para 3 mantido, QF subiu de 1 para 2 -- nao um platô
uniforme, um reequilibrio real entre linhas. Nenhum item derivado de
candidato `REFUTED` (nenhum foi `REFUTED` nesta rodada -- ver
observacao na abertura do documento). Notas de dependencia: item 10
(HG-4F Estagio 2) depende de item 7 (HG-4E); item 11 tem uma parte
opcional que deve ser reportada separadamente da parte minima; item 14
depende do `haveI` explicito de `NormedAlgebra Q (...)` para elaborar.

---

## Descartados/adiados nesta rodada (nao reabrir sem evidencia nova)

```text
PN     PN-9 (maquina multi-pilha, cardinalidade de K > 1)
       -- nao REFUTED (o teste como reescopado provavelmente compila),
          mas rebaixado a "checkbox de cobertura de tipo" pela propria
          adversarial: a motivacao citada (Function.update_of_ne/
          update_self de TM2to1) sustenta dificuldade so no caso de
          indice SIMBOLICO, nao no caso de indice CONCRETO que PN-9
          propoe (K:=Bool, k0:=false, k1:=true literais), que e
          estruturalmente identico aos literais ja fechados por rfl
          puro em PN1/PN2PRIME/PN3/PN5/PN8. Excluido da lista numerada
          para nao inflar a contagem com um item de baixo valor
          didatico -- mesma disciplina que a Onda 4 aplicou a
          recomendacao de infraestrutura _SHARED_INFRA/FORMAL.
```

Nenhum candidato foi `REFUTED` nesta rodada. A linha PN, no entanto,
rendeu **zero** itens de execucao -- primeiro caso desde a Onda 1 de uma
linha inteira sem contribuicao para a lista numerada, e reportado como
tal sem ajuste.

---

## Avaliacao pessoal — os 1-3 candidatos com maior chance de virar
resultado formal honesto e nao-trivial mais cedo

Nao e repeticao da autoavaliacao dos agentes de recon/adversarial -- e
julgamento proprio depois de ler as 14 verificacoes inteiras desta onda.

**1. YM-CAPSTONE-DET-BRACKET (item 5).** Composicao pura de tres pecas
JA fechadas e ja verificadas linha a linha nesta propria rodada
(`lambdaMax_mul_lambda2_eq_det`, os dois brackets de M1), com aritmetica
de intervalo conferida a mao (sem risco de flip de sinal, ambos os
limites positivos). O unico ponto de atrito possivel (`nlinarith` nao
fechar de primeira) tem fallback trivial de duas linhas ja especificado.
Risco tecnico residual: minimo.

**2. TOE-5 (item 12).** O argumento combinatorio inteiro foi verificado
a mao nesta propria revisao (pombos sobre 3 elementos de `Regime3`), a
peca mais pesada (`shiftCat_hom_nonempty` para todo par) ja esta
disponivel de graca, e a correcao proposta (remover a dependencia de
`Finite.injective_iff_bijective`) simplifica em vez de complicar o
teste. E generalizacao natural e matematicamente limpa de um resultado
ja condicional da Onda 4.

**3. HG-1G (item 8).** Puro exercicio de reindexacao sobre uma base ja
generalizada (HG-1E) que a Onda 4 ja demonstrou funcionar para o mesmo
tipo de dependencia. Nenhuma citacao Mathlib nova de risco, nenhuma
maquinaria alem do que HG-1E/HG-1F ja usam.

Nao incluo `RH-6a` no top 3 apesar de solido: e aritmetica de piso
limpa, mas monta `Tendsto.add`/`congr'` num arquivo novo do zero -- mais
passos de elaboracao que os tres itens acima. `BSD-6` fica de fora
apesar de barato e bem verificado: e o unico item desta onda cujo
proprio escopo interno (min vs. ambos os corolarios) ainda precisa ser
decidido antes da execucao, e a linha BSD carrega historico de exigir
cautela extra (STEP2-FULL refutado na Onda 2; BSD-GAP-007 so fechou
genuinamente na quarta tentativa de composicao).

## O laboratorio chegou ao ponto de pausar o ciclo de ondas?

Avaliacao honesta, atualizando a da Onda 4 (nao repetindo-a).

**O que mudou desde a Onda 4:** a contagem TOTAL de candidatos-execucao
nao caiu mais nesta rodada (14, igual a Onda 4), mas a COMPOSICAO
mudou de forma que confirma, em vez de contradizer, o diagnostico
anterior -- **uma linha inteira (PN) esgotou-se genuinamente** pela
primeira vez em cinco ondas, exatamente o tipo de sinal que a Onda 4
previu ("o padrao e consistente com exaustao progressiva"). Ao mesmo
tempo, RH e QF renderam mais candidatos que na Onda 4 (RH: 2->3, QF:
1->2), mostrando que a exaustao nao e uniforme -- algumas linhas ainda
tem corda genuina, outras nao.

**Quatro observacoes atualizadas:**

1. **A exaustao por linha, nao por portfolio agregado, e o sinal real.**
   A contagem agregada (14=14) mascara o que de fato aconteceu: PN foi
   de 1 para 0 (esgotada), enquanto RH e QF cresceram. Isso sugere que
   o modo correto ja NAO e "rodar a mesma rotina de recon em todas as 8
   linhas simultaneamente indefinidamente", mas comecar a DIFERENCIAR
   linhas por status -- algumas prontas para uma pausa/consolidacao
   (PN, e possivelmente NS e YM, que renderam so 1-2 itens modestos
   cada), outras (RH, HG, QF) ainda produtivas.

2. **BSD continua sendo a linha que mais claramente pede um projeto
   dedicado, nao mais uma onda de sondas.** `BSD-GAP-007` fechou na
   Onda 4 (real, verificado com escrutinio extra), mas `BSD-GAP-008`
   (Mordell-Weil fraco) permanece `OPEN` com CINCO lacunas formais
   separadas identificadas desde a Onda 1 -- isogenia, mapa de Kummer,
   grupo de Selmer especifico de curva eliptica, correcao de
   `AddSubMap.lean:21`, altura ingenua nao definida, lei do
   paralelogramo aproximada incompleta, propriedade Northcott parcial.
   Isso e estruturalmente maior do que qualquer cadeia ja vista em
   BSD-GAP-007 (que precisou de 4 ondas so para uma unica bijecao de
   corpo de residuo). Nenhum item de Onda-5-pequena-e-paralela toca
   `BSD-GAP-008` -- nem deveria, dado o tamanho.

3. **`TOE_INTERFACE_EXECUTION` continua sendo um gate nomeado e nunca
   disparado**, exatamente como reportado na Onda 4 -- `TOE_SCOPE.md`
   segue existindo como esqueleto (`AXIOM_CANDIDATES.yaml` com
   candidatos `UNRESOLVED`), e o ciclo de ondas continuou tratando TOE
   como mais uma linha de sondas pequenas (TOE-5 nesta rodada) em vez de
   investir na sintese completa. Isso nao mudou desde a Onda 4 -- o
   gate permanece uma decisao pendente, nao uma urgencia nova.

4. **Contra-sinal, mais forte que na Onda 4:** HG produziu 3 candidatos
   novos SURVIVES/NEEDS_NARROWING de novo (mesma contagem que a Onda 4),
   e RH cresceu. Isso significa que pelo menos duas linhas (HG, RH)
   ainda geram alvos genuinamente novos e baratos, sem sinal de
   esgotamento -- nao ha justificativa honesta para encerrar TODO o
   ciclo de ondas so porque uma linha (PN) esgotou.

**Conclusao honesta, refinada em relacao a Onda 4:** a resposta
continua HIBRIDA, mas agora com um proximo passo mais concreto do que
"considerar" -- (a) a linha PN deve ser formalmente encerrada como
sub-frente de "cobertura de construtor/mecanismo" (nao mais reavaliada
onda a onda; se reaberta, so por uma proposta genuinamente nova, nao
reindexacao de K); (b) `BSD-GAP-008` e agora o candidato mais maduro
para um PROJETO DEDICADO de escala propria fora do ciclo de ondas --
mais maduro do que estava na Onda 4, porque o proprio `BSD-GAP-007` (a
prova de conceito de que uma cadeia de composicao longa pode fechar)
acabou de ser validada como viavel neste laboratorio, e a lista de
cinco lacunas de `BSD-GAP-008` ja esta nomeada e pronta para virar plano
de projeto; (c) `TOE_INTERFACE_EXECUTION` permanece candidato adiado,
nao urgente -- nenhum evento nesta onda mudou seu status; (d) as linhas
restantes com corda (RH, HG, QF, YM, SHARED-INFRA) devem continuar no
modo onda-pequena-paralela ate que produzam, elas tambem, um sinal de
esgotamento equivalente ao de PN nesta rodada -- nao ha justificativa
para declarar a varredura de portfolio inteira encerrada enquanto pelo
menos quatro linhas seguem gerando candidatos baratos e bem definidos.

---

## O que este documento confirma sobre o processo

A disciplina de "reverificar por leitura direta de arquivo, checando
citacao Mathlib por citacao Mathlib, e fazendo a aritmetica/combinatoria
a mao quando aplicavel" continuou achando coisas reais nesta rodada: um
gap de composicao load-bearing nao coberto pelo enunciado do proprio
teste falsificavel (`RH-6b`, tipo `Set C` vs `Set R`); uma rota de prova
mais cara do que necessario que uma leitura mais profunda do arquivo-
fonte revelou ser evitavel (`NS-5A`, `SHARED-5A`, ambos com um lema
Mathlib mais direto encontrado na mesma vizinhanca do que o candidato
original citou); um `haveI` de instancia omitido que faria o teste
literal falhar exatamente como falhou uma vez antes na mesma base de
codigo (`QF-9`); e um titulo de candidato que prometia mais do que seu
proprio teste declarado entregava (`HG-4F`, "propriedade de subgrupo"
vs. so um fato de nao-diferenciabilidade autonomo). Em nenhum caso isso
refutou o alvo subjacente -- em todos, o resultado real continuou de pe,
so precisou de divisao em passos mais honestos ou de uma rota de prova
mais barata. A linha PN e o achado estrutural mais importante desta
rodada: nao um erro encontrado num candidato, mas a confirmacao de que
uma sub-frente inteira do laboratorio chegou ao fim do que "compor
resultados ja fechados" consegue produzir, e que reportar isso
honestamente (zero itens, nao um item de baixo valor para preencher a
lista) e parte do mesmo padrao de disciplina que motivou este documento
desde a Onda 1.
