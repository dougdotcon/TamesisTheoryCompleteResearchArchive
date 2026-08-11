---
document_id: PLANO-ATAQUE-ONDA-6-2026-08-11
reviewed_at: 2026-08-11
input: recon + revisao adversarial de 8 grupos (7 linhas de pesquisa + infraestrutura compartilhada) para Onda 6, ancorado nos resultados reais da Onda 5 -- ver 09_SESSIONS/2026/2026-08-11_WAVE5_EXECUTION.md (14/14 CLOSED, 0 GAP_DIAGNOSED, 0 REJECTED -- primeira onda totalmente limpa do ciclo) e 01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_4_2026_08_10.md, 01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_5_2026_08_11.md. Linha PN retirada formalmente da rotacao de reconhecimento por DEC-100.
conclusion: PLANO_DE_EXECUCAO_ONDA_6_PROPOSTO
---

# Plano de ataque — Onda 6 (continuação das Ondas 1-5)

## Enquadramento honesto

Este documento é a continuação direta de
`PLANO_DE_ATAQUE_PORTFOLIO_COMPLETO_2026_08_09.md`,
`PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md`,
`PLANO_DE_ATAQUE_ONDA_3_2026_08_10.md`,
`PLANO_DE_ATAQUE_ONDA_4_2026_08_10.md`,
`PLANO_DE_ATAQUE_ONDA_5_2026_08_11.md` e da sessão de execução
`2026-08-11_WAVE5_EXECUTION.md`. A Onda 5 fechou **14 de 14** itens (10
VERIFIED, 4 VERIFIED_WITH_NOTES), com **zero** `GAP_DIAGNOSED` e **zero**
`REJECTED` — a **primeira onda inteiramente limpa** do ciclo (Ondas 1-4
tiveram cada uma pelo menos um `GAP_DIAGNOSED` ou `REJECTED`). A Onda 6
parte desse chão real.

```text
O que este plano E:
  - a próxima rodada de pequenos testes falsificáveis contra
    infraestrutura Mathlib genuína, construída sobre os 14 itens
    fechados na Onda 5 (e, por herança, sobre os 15+20+25+14 das Ondas
    1-4)
  - uma tentativa de re-verificar, por leitura direta de arquivo (não
    por confiança no agente de recon), com verificação independente de
    citações Mathlib linha a linha e conferência aritmética/algébrica à
    mão onde aplicável, se os alvos propostos continuam abertos, já
    foram satisfeitos por acaso, ou têm um defeito real
  - honesto sobre linhas sem alvo pequeno disponível nesta rodada
    (nenhuma linha ficou em zero nesta rodada -- ver abaixo), e sobre
    onde um teste proposto tinha um gap real (de composição, de
    citação ausente, ou de escopo alegado excedendo o que o teste de
    fato prova) que precisou de reescopo

O que este plano NAO E:
  - uma alegação de que qualquer Problema do Milênio ficou mais
    próximo de ser resolvido -- nenhum item abaixo toca o núcleo
    central de nenhuma das 6 frentes Clay-oficiais
  - uma reabertura da linha P vs NP (PN): PN foi formalmente RETIRADA
    da rotação de reconhecimento a partir desta onda por DEC-100, a
    pedido explícito do usuário, após produzir 0 candidatos na Onda 5
    (depois de já ter caído para 1 candidato na Onda 4). Isso é
    retirada OPERACIONAL e REVERSÍVEL de uma sub-frente de
    "cobertura de construtor/mecanismo" esgotada -- NÃO um fechamento
    do problema P vs NP, nem uma declaração de que a linha está
    permanentemente encerrada. `PNP-GAP-001..004` permanecem `OPEN`.
    Se um ângulo pequeno genuinamente novo surgir, a linha pode ser
    reativada por decisão de portfólio futura
  - uma alegação de que o fechamento de `BSD-GAP-007` (Onda 4) ou de
    qualquer corolário `IsMultiplicative` adicional (Onda 5, Onda 6)
    constitui progresso sobre a conjectura de Birch e Swinnerton-Dyer
    em si. `BSD-GAP-007` permanece `CLOSED` (2026-08-10,
    `WAVE4-BSD-1-STEP5-COMPOSE`); `BSD-GAP-008` (Mordell-Weil fraco,
    cinco lacunas formais separadas) permanece `OPEN` e continua fora
    do escopo do ciclo de ondas
  - uma alegação de que `TOE-INTERFACE-001` ou `QCU-001` têm status
    Clay-oficial
  - uma reabertura do `RH-NOGO-001`
  - uma promessa de que todo teste "SURVIVES" fecha sem `sorry` -- é
    uma aposta informada, não uma certeza
  - uma tentativa de inflar a contagem de itens: onde a revisão
    adversarial encontrou um candidato de valor genuinamente baixo ou
    fora de escopo para esta rodada (o caso BSD abaixo), isso é
    reportado com a ressalva explícita, não maquiado como um item de
    confiança plena
```

**14** candidatos revisados ao todo nos 8 grupos (7 linhas +
infraestrutura compartilhada — PN não faz mais parte do reconhecimento
padrão). A lista numerada de execução da Onda 6 tem **13 candidatos
distintos**, todos com pelo menos um teste falsificável concreto
sobrevivendo à adversarial (nenhum `REFUTED` nesta rodada — ver
observação abaixo). O motivo do descompasso 14→13 no total de
candidatos revisados: um dos 14 "candidatos" da lista de entrada é, na
verdade, o próprio veredito de confirmação de que a sub-linha
`IsMultiplicative` de BSD está genuinamente esgotada (nenhum corolário
`IsMultiplicative` barato adicional vale a pena) — não é ele mesmo um
alvo de execução, é contexto que justifica por que BSD contribui apenas
**um** item nesta onda, e um item de natureza exploratória distinta dos
demais (ver seção 5).

**Nenhum candidato foi `REFUTED` nesta rodada.** A adversarial encontrou,
de novo, vários gaps de composição/citação/escopo genuínos (`RH-7A`
cruzando namespaces distintas, `HG-4g` citando uma rota mais pesada do
que a necessária, `QF-11` com um passo de continuidade sem citação
firme, `BSD` com uma linha de pesquisa inteira — `HasseCoefficientRecursionBound.lean`
— ignorada pelo recon original) — em todos os casos o alvo subjacente
sobreviveu, apenas precisou de reescopo ou de uma citação mais direta.
**Nenhuma segunda linha atingiu zero candidatos nesta rodada** (ver
seção "O laboratório chegou..." abaixo para uma leitura mais fina desse
sinal, porque a densidade de candidatos por linha não é uniforme: NS,
BSD e SHARED-INFRA renderam apenas 1 item cada, um afinamento notável em
relação às Ondas anteriores).

---

## 1. Riemann Hypothesis (RH) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| RH-7A | Cota de taxa quantitativa de `eigCount` (compor `RH-6A` + `RH-6B` da Onda 5) | NEEDS_NARROWING | baixo-moderado |
| RH-7B | `Tp` é formalmente auto-adjunto (simétrico) no seu domínio de suporte finito | SURVIVES | baixo |

**Passo original vs. o que mudou.** Ambos continuam inteiramente dentro
do `LinearPMap` de brinquedo já usado por RH-3..RH-6C (Ondas 3-5), sem
nenhuma conexão com `riemannZeta`/RVM. `RH-7A` tenta compor pela
primeira vez a cota de taxa (`RH-6A`, Onda 5) com a ponte exata de
`eigCount` (`RH-6B`, Onda 5). `RH-7B` fecha um gap de honestidade que
`DiagonalSelfAdjointOperatorProbe.lean` deixou aberto por construção
(prova auto-adjunção só para um operador DIFERENTE do `Tp` de
brinquedo usado em RH-3..RH-6C).

**RH-7A — NEEDS_NARROWING.** Releitura integral de
`UnboundedEigCountRateBound.lean` (296 linhas) e
`UnboundedEigCountEigCountBridge.lean` (429 linhas) confirma
`unboundedEigCount_rate_bound` (linhas 274-283) e
`unboundedEigCount_eq_eigCount` (linhas 405-411) exatamente como
descritos, e todos os lemas Mathlib citados (`Nat.floor_le`,
`Nat.lt_floor_add_one`, `div_sub_one`, `div_pos`,
`div_le_div_of_nonneg_right`, `Set.ncard_image_of_injective`,
`Set.ncard_preimage_of_injective_subset_range`,
`Complex.ofReal_injective`) genuinamente usados. Grep por
`eigCount.*rate` no diretório FORMAL de RH retorna zero — essa
composição nunca foi feita. Porém: os dois teoremas vivem em namespaces
DIFERENTES, declaradas independentemente (`RH6A.UnboundedEigCountRateBound`
vs. `RH6B.UnboundedEigCountEigCountBridge`), cada uma com seu próprio
`Tp`/`finiteSupport`/`unboundedEigCount` declarado à parte (confirmado
por grep: `noncomputable def Tp` aparece uma vez por arquivo, em 6
namespaces diferentes no diretório FORMAL de RH). Não são a mesma
constante Lean — a tática de cabeçalho do teste original (`rw [<-
unboundedEigCount_eq_eigCount hLam.le]; exact unboundedEigCount_rate_bound
hLam`) NÃO faria type-check como composição literal cross-file dos dois
nomes de lema pré-existentes, já que `rw` exige casamento sintático/de
constante. O reescopo segue a convenção já estabelecida por todo arquivo
RH-3..RH-6C: reproduzir os dois blocos byte-a-byte sob um namespace
compartilhado num arquivo novo, ponto em que o `rw` encadeado passa a
valer contra as cópias LOCAIS reproduzidas.
**Teste revisado:** em um arquivo novo (namespace único, ex.
`RH7A.UnboundedEigCountRateBoundEigCountBridge`), reproduzir
byte-a-byte (a) o bloco completo de `UnboundedEigCountEigCountBridge.lean`
até `unboundedEigCount_eq_eigCount` e (b) a derivação de piso-sanduíche
de `unboundedEigCount_rate_bound` (RH-6A da Onda 5), ambos operando
sobre o MESMO `Tp`/`unboundedEigCount` declarado localmente. Então
fechar, para `Lam>0`: `0 < (eigCount T ((Lam+1)⁻¹):R)/Lam-1 ∧
(eigCount T ((Lam+1)⁻¹):R)/Lam-1 <= 1/Lam` via `rw [<-
unboundedEigCount_eq_eigCount hLam.le]; exact unboundedEigCount_rate_bound
hLam`, usando os nomes de lema LOCAIS do próprio arquivo. `#print axioms`
limpo (3 axiomas padrão).

**RH-7B — SURVIVES.** Releitura integral de
`DiagonalSelfAdjointOperatorProbe.lean` (272 linhas) confirma que seu
`T` é um operador genuinamente DIFERENTE do `Tp` de brinquedo usado em
RH-3..RH-6C: vive em `H := lp (fun _:N => R) 2` (escalares reais, não
`H2` complexo) com domínio MAXIMAL `Dom = {x in l^2 | (n -> n*x_n) in
l^2}`, não o submódulo de suporte finito `finiteSupport` usado por todo
arquivo RH-3..RH-6C. O arquivo já prova `T_isFormalAdjoint` (linha 190)
e `T_isSelfAdjoint` (linha 264) para ESSE operador — mas nunca para o
`Tp` complexo de suporte finito. Toda citação Mathlib conferida no local
exato: `LinearPMap.IsFormalAdjoint`
(`Analysis/InnerProductSpace/LinearPMap.lean:74-75`, `forall x y, <T
x,y> = <x,S y>`); `lp.hasSum_inner`
(`Analysis/InnerProductSpace/l2Space.lean:150`); `Complex.conj_natCast`
(`Data/Complex/Basic.lean:481`); `HasSum.unique` (via `HasProd.unique`,
`Topology/Algebra/InfiniteSum/Defs.lean:327`, `to_additive`'d,
confirmado em uso direto noutro lugar). A convenção de produto interno
linear-conjugado-à-esquerda citada (`RCLike/Inner.lean:11-14`) é real,
embora documente diretamente um produto interno ponderado sobre tipo
`Pi` finito em vez da instância `lp` — referência indiretamente correta,
não fabricada. O ponto honesto de escopo já declarado pelo candidato: o
alvo prova apenas SIMETRIA (`IsFormalAdjoint`), não auto-adjunção plena
— como `finiteSupport` é subespaço próprio não-maximal, o domínio de
`Tp.adjoint` seria estritamente maior, exatamente a mesma distinção que
`DiagonalSelfAdjointOperatorProbe.lean` já traça para seu próprio
operador.
**Teste revisado:** reproduzir o bloco mínimo
`finiteSupport`/`TpFun`/`Tp`/`Tp_apply` (como
`TpUnboundedNormProbe.lean` linhas 94-184 já faz), então provar
`Tp_isFormalAdjoint : Tp.IsFormalAdjoint Tp`, i.e. `forall x y :
Tp.domain, inner (Tp x : H2) (y:H2) = inner (x:H2) (Tp y:H2)`, via
`lp.hasSum_inner` aplicado a ambos os lados mais igualdade termo-a-termo
via `funext` + `Complex.conj_natCast` + `ring`, fechado por
`HasSum.unique`. Explicitamente NÃO tentar `IsSelfAdjoint`/`T.adjoint =
T` neste mesmo item — declarar no cabeçalho, como
`DiagonalSelfAdjointOperatorProbe.lean` faz para seu próprio operador,
que `finiteSupport` sendo subespaço denso próprio torna auto-adjunção
genuína uma alegação separada, mais difícil, NÃO tentada. `#print
axioms` limpo (3 axiomas padrão).

---

## 2. Navier-Stokes (NS) — Clay oficial (núcleo Calderón-Zygmund)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| NS-6A | Generalização auto-raio (função de escolha) da monotonicidade cruzada-compacta, parando antes da montagem de `limitCLM` | SURVIVES | baixo |

**Passo original vs. o que mudou.** Continuação direta de
`PVEnvelopeCrossCompactMonotonicity.lean` (NS-5A, Onda 5), que fixa
`K1<=K2` e usa raios EXPLÍCITOS `R1,R2` fornecidos externamente. NS-6A
propõe substituir esses raios explícitos por um raio derivado
automaticamente de cada compacto via uma função de escolha
(`Classical.choose`/`Bornology.IsBounded.subset_closedBall_lt`), sem
ainda tentar a montagem global `TestFunction.mkCLM`/`limitCLM`.

**NS-6A — SURVIVES.** Releitura integral de
`PVEnvelopeCrossCompactMonotonicity.lean` (NS-5A, 213 linhas) confirma
`pvKCLM_cross_compact_monotone` exatamente como descrito, com sua
própria seção "O que NAO é afirmado" deixando corretamente de fora o
gap(iii) (montagem global `TestFunction.mkCLM`/`limitCLM`) — o mesmo gap
que NS-6A continua a deixar de fora. Toda citação Mathlib conferida por
leitura direta: `Bornology.IsBounded.subset_closedBall_lt`
(`MetricSpace/Bounded.lean:117-120`, `(h:IsBounded s)(a:R)(c:alpha):
exists r, a<r and s subset closedBall c r`, dá positividade estrita e
contenção num único passo com `a:=0`); `IsCompact.isBounded`
(`Bounded.lean:192`); `Compacts`' `PartialOrder := .ofSetLike`
(`Topology/Sets/Compacts.lean:49`), rastreado até
`Data/SetLike/Basic.lean:226-240` confirmando que `K1 <= pvKCompact R1`
desdobra via `IsConcreteLE`'s `coe_subset_coe'` com termo de prova
literalmente `Iff.rfl` — a ordem `SetLike` e `Set.Subset` são
definicionalmente iguais, não só propositionalmente, então um termo
derivado de `choose_spec` deveria encaixar na hipótese `K1 <=
pvKCompact R1` com no máximo um invólucro trivial de
`SetLike.coe_subset_coe.mpr` (exatamente o idioma que a própria prova de
NS-4a já usa, linhas 1123-1124). Confirmado também
`ContDiffMapSupportedIn.of_support_subset` (linha 281) e seu uso real
dentro da prova de `limitCLM` de `TestFunction.lean` (`toFun_add`/
`toFun_smul`, linhas ~376-391), e que o parâmetro `T` de `limitCLM` tem
tipo `Pi (K:Compacts E), (K:Set E) subset Omega -> 𝓓^n_K(E,F) ->L[k] V`
(`TestFunction.lean:370-372`) — a consistência cruzada-compacta que
NS-6A visa é genuinamente a forma da compatibilidade que
`toFun_eq_T` precisa, não um desvio arbitrário. `GAP_REGISTER.yaml` de
`02_NAVIER_STOKES` confirmado: NS-GAP-001/002/004/005 `OPEN`,
NS-GAP-003 `REFUTED`, nenhum tocado. O único risco real sinalizado
(fricção de unificação entre a ordem `SetLike` e `Set.Subset`) é, pela
análise acima, muito provável de resolver limpo (defeq via `Iff.rfl`) em
vez de ser um obstáculo genuíno — o custo estimado "moderado" do
candidato original é, portanto, uma superestimativa; mais perto de
"baixo", quase uma especialização gratuita de um teorema já provado.
**Teste revisado:** sem estreitamento no conteúdo matemático; uma
única correção de execução — usar o idioma explícito de conversão que a
própria NS-4a já usa
(`SetLike.coe_subset_coe.mpr (K1.isCompact.isBounded.subset_closedBall_lt
0 0).choose_spec.2`) para `hK1R1`/`hK2R2`, em vez de assumir que a defeq
bruta é resolvida silenciosamente — isso remove a única incerteza real
sinalizada (unificação de ordem `SetLike`) usando o idioma já
estabelecido do laboratório, em vez de confiar em o elaborador de Lean
desdobrar automaticamente as definições `reducible` de `.ofSetLike`.
Restante do teste falsificável (raios `R1`/`R2` derivados de
`Classical.choose`, sem nenhuma hipótese de raio/envelope livre no
enunciado final, instanciação direta de `pvKCLM_cross_compact_monotone`
de NS-5A) permanece inalterado.

---

## 3. Yang-Mills (YM) — Clay oficial (modelo de brinquedo de rede-transferência 2x2)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| YM-CAPSTONE-TRACE-M1-EXACT | `trace(toEuclideanCLM M1) = 4.1` exato, seguido de estreitamento do bracket de `lambda2` | SURVIVES | baixo |
| YM-CAPSTONE-DET-BRACKET-TIGHTENED | Estreitar `det(toEuclideanCLM M1) ∈ [2.03,4.03]` para `[2.9,3.72]` usando o `lambda2` estreitado | SURVIVES (gated no item anterior) | baixo |

**Passo original vs. o que mudou.** Continuação direta de
`YMCapstoneDetBracket.lean` (Onda 5), que já prova `det(toEuclideanCLM
M1) ∈ [2.03,4.03]` via `lambdaMax*lambda2=det` combinado com o bracket
de `lambdaMax` de `[2.9,3.1]` (via aritmética de piso/traço) e o bracket
de `lambda2` de `[0.7,1.3]` (via a rota de Lipschitz 3x, NÃO via
identidade de traço). O par desta onda explora exatamente esse gap:
provar o traço EXATO de `M1` para estreitar `lambda2`, e então propagar
o estreitamento para `det`.

**YM-CAPSTONE-TRACE-M1-EXACT — SURVIVES.** Confirmado `M1 := !![2, 1; 1,
2.1]` em `YMCapstoneDetBracket.lean:413`, logo `trace(M1) = 2+2.1 = 4.1`
por aritmética elementar. Confirmado que o bracket de `lambda2` existente
`[7/10,13/10] = [0.7,1.3]` (linhas 546-552,
`lambda2_M1_bracket_from_compose`) é genuinamente derivado pela rota de
Lipschitz 3x (`stability_compose_lambda2`), NÃO por nenhuma identidade
de traço para `M1` — confirmado pela leitura da cadeia completa
(`trace_lipschitz -> lambda2_lipschitz -> stability_compose_lambda2 ->
lambda2_M1_bracket_from_compose`). `lambda2` é definido nas linhas
465-466 como `(T).trace R E - lambdaMax T`; uma vez provado
`trace(M1)=4.1` exatamente, combinando com o já-provado
`lambdaMax_M1_bracket` (`[2.9,3.1]`, linhas 447-453), obtém-se `lambda2
∈ [4.1-3.1, 4.1-2.9] = [1.0, 1.2]` por `linarith` puro — subconjunto
estrito de `[0.7,1.3]` (1.0>0.7, 1.2<1.3), estreitamento real, não
ilusório. Verificação cruzada contra os autovalores verdadeiros (traço
4.1, det 3.2, autovalores `(4.1±sqrt(4.01))/2 ≈ 3.051` e `≈1.049`) —
ambos os brackets, antigo e novo, contêm corretamente `1.049`, com o
novo muito mais apertado, então a alegação é sólida, não vazia. Toda
citação Mathlib conferida por grep direto no checkout Mathlib local:
`LinearMap.trace_eq_sum_inner` (`Analysis/InnerProductSpace/Trace.lean:27`),
`Matrix.inner_toEuclideanCLM` (`Analysis/CStarAlgebra/Matrix.lean:122`),
`EuclideanSpace.finrank_euclideanSpace_fin`
(`Analysis/InnerProductSpace/PiL2.lean:207`). Grep no diretório FORMAL
inteiro por `trace_toEuclideanCLM_M1`, `4.1` como valor de traço e
`lambda2_M1_bracket_tight` — todos ausentes, confirmando novidade
genuína, sem duplicação. O padrão de prova é estruturalmente idêntico à
já-bem-sucedida prova de traço de `M2` e a outras chamadas `norm_num`
já funcionando no mesmo arquivo para `M1` (`M1_isHermitian`,
`diff_eq_diagonal`, `sonda2_numeric_norm` já resolvem `norm_num` com o
`2.1` decimal de `M1` com sucesso) — risco baixo de `norm_num` engasgar
no decimal.
**Teste:** provar `trace_toEuclideanCLM_M1_eq_four_point_one` seguindo o
padrão de `trace_toEuclideanCLM_M2_eq_four` (via
`LinearMap.trace_eq_sum_inner` + `Matrix.inner_toEuclideanCLM` +
`Fin.sum_univ_two` + `norm_num`) com as entradas de `M1`; então derivar
o bracket `[1.0,1.2]` via `unfold lambda2; rw [trace_toEuclideanCLM_M1_eq_four_point_one,
lambdaMax_M1_bracket-derived-bounds]; constructor <;> linarith`.
`#print axioms` limpo.

**YM-CAPSTONE-DET-BRACKET-TIGHTENED — SURVIVES (gated no item
anterior).** Confirmado `det_M1_bracket` (linhas 642-649) provando
`2.03 <= det <= 4.03` via `lambdaMax_mul_lambda2_eq_det` +
`lambdaMax_M1_bracket` + `lambda2_M1_bracket_from_compose`, fechado por
`constructor <;> nlinarith [...]`. Grep confirma nenhum fato de `det`
pré-existente exato ou mais apertado (só um comentário de sanidade
notando `det M1 = 3.2`, linha 186, nunca provado como teorema). A
aritmética de bracket proposta é correta: para `x ∈ [2.9,3.1]`, `y ∈
[1.0,1.2]` (ambos positivos), `min(x*y)` está em `(2.9,1.0)=2.9` e
`max(x*y)` em `(3.1,1.2)=3.72` (produto de dois intervalos positivos é
monótono em cada argumento), e o novo bracket `[2.9,3.72]` continua
contendo o valor real `3.2`. Estreitamento real e corretamente
calculado de `[2.03,4.03]` para `[2.9,3.72]`. Plausibilidade de
`nlinarith` fechar suportada por analogia direta: o próprio cabeçalho do
arquivo (linhas 131-148) documenta que o pré-processamento automático de
produto-de-hipóteses do `nlinarith` já fecha a mesma forma algébrica
(produto de duas quantidades com bracket positivo) para o caso atual
`[2.9,3.1]x[0.7,1.3]` sem precisar do fallback `mul_le_mul` — os termos
cruzados necessários para o caso mais apertado `[2.9,3.1]x[1.0,1.2]` têm
a mesma forma algébrica, sem razão estrutural para `nlinarith` falhar
aqui onde teve sucesso lá.
**Teste:** como proposto, com uma condição explícita: só tentar este
item DEPOIS que o lema do item anterior de fato compilar (`constructor
<;> linarith`) e seu bracket `[1.0,1.2]` estiver confirmado como
teorema real, não assumido — alvo estritamente sequencial de dois
passos, não dois itens independentemente executáveis em paralelo.

---

## 4. Hodge Conjecture (HG) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| HG-1h | `principalCycle_a0` é multiplicativo sob produtos de inteiros (`a0*b0 -> soma de ciclos`) | SURVIVES | baixo |
| HG-4g | `(C->C)ˣ / HolomorphicTransitionSubgroup` é `Nontrivial` | SURVIVES | baixo |

**Passo original vs. o que mudou.** Ambos continuam diretamente de
gaps já nomeados nos próprios arquivos da Onda 5. `HG-1h` é o espelho
multiplicativo do caso de divisão já fechado por `HG-1g`
(`f_ab`/`principalCycle_f_ab_eq_sub`). `HG-4g` depende de
`holomorphicTransitionSubgroup_ne_top`, fechado pelo Estágio 2 de
`HG-4F` na Onda 5.

**HG-1h — SURVIVES.** Releitura integral de
`HG1GPrincipalCycleNumDenParamProbe.lean` (HG-1g) confirma `genf`,
`algebraMap_eq_genf` (linhas 186-189), `genf_ne_zero` (191-195),
`finite_support_ord_genf` (275-289) e `principalCycle_a0` (303-309),
todos totalmente parametrizados sobre `a0 : Z` não-nulo arbitrário, e o
bloco `f_ab`/`principalCycle_f_ab_eq_sub` (325-389) do mesmo arquivo é o
espelho exato, do lado da divisão, do que HG-1h propõe para a
multiplicação. Toda citação Mathlib conferida no local exato:
`Scheme.ord_mul` (`AlgebraicGeometry/OrderOfVanishing.lean:80-81`,
`{x}{f g}(hf:f≠0)(hg:g≠0): ord(f*g) x = ord f x + ord g x`);
`RingHom.map_mul` (`Algebra/Ring/Hom/Defs.lean:469`); e adicionalmente
`Function.locallyFinsuppWithin.coe_add`
(`Topology/LocallyFinsupp.lean:348`, espelhando `coe_sub` já usado na
linha 352), com `AlgebraicCycle X R` definicionalmente
`Function.locallyFinsupp X R`
(`AlgebraicGeometry/AlgebraicCycle/Basic.lean:44-45`) — o padrão
`ext`/`coe_add`/`Pi.add_apply`/`omega` é substituto direto legítimo do
padrão `coe_sub` já bem-sucedido em HG-1g. A matemática subjacente
(`genf(a0*b0) = genf(a0)*genf(b0)` via `algebraMap_eq_genf` +
`map_mul`, depois aditividade de `ord` via `ord_mul`) é correta e, de
forma notável, MAIS SIMPLES que o caso de divisão de HG-1g: o LHS
`principalCycle_a0 (a0*b0) hab` não precisa de nenhuma definição de
empacotamento nova (diferente de `f_ab`/`principalCycle_f_ab`, que
HG-1g precisou definir do zero porque um quociente de dois valores de
`genf` não é ele mesmo um valor de `genf` de algum inteiro) — é
literalmente a função `principalCycle_a0` já existente avaliada em
`a0*b0`. Passo genuíno, de baixo risco, mecânico.
**Teste:** provar `theorem principalCycle_a0_mul (a0 b0 : Z) (ha0 : a0
≠ 0) (hb0 : b0 ≠ 0) (hab : a0*b0 ≠ 0) : principalCycle_a0 (a0*b0) hab =
principalCycle_a0 a0 ha0 + principalCycle_a0 b0 hb0`, via `ext` +
`Function.locallyFinsuppWithin.coe_add` (colapsando o RHS) +
`algebraMap_eq_genf` + `RingHom.map_mul` + `Scheme.ord_mul` (mostrando
`ord` do produto de `genf`-valores é a soma pontual) + `Pi.add_apply` +
`omega`/`ring` para fechar a igualdade pontual em cada ponto do suporte.
`#print axioms` limpo.

**HG-4g — SURVIVES.** Releitura integral de
`HolomorphicTransitionSubgroupProbe.lean` (HG-4e) e
`HG4FExpConjNotHolomorphicSubgroupProbe.lean` (HG-4f) confirma
exatamente a dependência alegada: o Estágio 2 de HG-4f genuinamente
prova `holomorphicTransitionSubgroup_ne_top : HolomorphicTransitionSubgroup
≠ (⊤ : Subgroup (C→C)ˣ)` (linhas 357-364), a hipótese exata que HG-4g
precisa. Todas as cinco citações Mathlib da rota ORIGINALMENTE proposta
foram conferidas e existem exatamente como citadas
(`normal_of_isMulCommutative`, `Algebra/Group/Subgroup/Defs.lean:631-632`;
`instCommGroupUnits`, `Algebra/Group/Units/Defs.lean:266`;
`Pi.commMonoid`, `Algebra/Group/Pi/Basic.lean:80`;
`subgroup_eq_top_of_subsingleton`, `GroupTheory/QuotientGroup/Basic.lean:393`,
confirmado sem exigir hipótese `[H.Normal]`;
`subsingleton_or_nontrivial`, `Logic/Nontrivial/Defs.lean:111`) — mas
essa rota é DESNECESSARIAMENTE pesada. Leitura direta de
`Mathlib/GroupTheory/QuotientGroup/Defs.lean:53-54` encontrou um lema
Mathlib muito mais direto: `QuotientGroup.nontrivial_iff : Nontrivial (G
⧸ N) ↔ N ≠ ⊤`, provado SEM hipótese `[N.Normal]` alguma (aparece antes
da linha `variable (N) [nN : N.Normal]` do arquivo) — confirmado
adicionalmente que `instHasQuotientSubgroup`
(`GroupTheory/Coset/Defs.lean:94`) também não exige instância `Normal`;
o TIPO do quociente e seus fatos de cardinalidade nunca precisam de
normalidade, só a estrutura de GRUPO no quociente precisa. O alvo
continua válido e todo o suporte citado originalmente é verdadeiro, mas
a justificativa original superengenheira (empacota maquinaria de
instância `Normal` que a prova de fato não usa) e perde um lema Mathlib
estritamente mais simples, já existente, que prova a mesma afirmação
diretamente com menos dependências.
**Teste revisado:** `theorem holomorphicTransitionQuotient_nontrivial :
Nontrivial ((C -> C)ˣ ⧸ HolomorphicTransitionSubgroup) :=
QuotientGroup.nontrivial_iff.mpr holomorphicTransitionSubgroup_ne_top` —
uma linha, usa `Mathlib/GroupTheory/QuotientGroup/Defs.lean:53-54`
diretamente, sem precisar de raciocínio sobre `Normal`/`IsMulCommutative`,
já que `Nontrivial (G ⧸ N)` é definido e provável sem hipótese de
normalidade sobre `N`. `#print axioms` limpo.

---

## 5. Birch and Swinnerton-Dyer (BSD) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| BSD-7 (exploratório/triagem) | Identidade-ponte de coeficiente entre `PowerSeries.coeff` da série local e a recursão abstrata `cSeq` (`HasseCoefficientRecursionBound.lean`, Onda 3) | NEEDS_NARROWING | baixo-moderado, incerto |

**Contexto factual.** `BSD-GAP-007` permanece `CLOSED` (fechado na Onda
4, `WAVE4-BSD-1-STEP5-COMPOSE`, verificado com escrutínio extra).
`BSD-GAP-008` (Mordell-Weil fraco, cinco lacunas formais separadas)
permanece `OPEN` e continua fora do escopo do ciclo de ondas.

**Confirmação de que a sub-linha `IsMultiplicative` está genuinamente
esgotada.** Releitura integral de `BSD6LFunctionEqOnPrimePowers.lean`
(Onda 5, 378 linhas) e do `GAP_REGISTER.yaml` confirma linha a linha:
`BSD-GAP-007` `CLOSED`, `BSD-GAP-008` `OPEN` e intocado por esse
arquivo. O único conteúdo novo além da cadeia reproduzida das Ondas
2-4 é exatamente as duas declarações já fechadas nas linhas 345-359
(`LFunction_eq_iff_eq_on_prime_powers`,
`LFunction_apply_eq_prod_prime_powers`), ambas especializações de uma
linha de lemas Mathlib. Independentemente conferida toda a vizinhança
de `Mathlib/NumberTheory/ArithmeticFunction/Defs.lean:400-644`: os
demais corolários `IsMultiplicative` disponíveis
(`map_gcd`/`map_lcm`/`map_div_of_coprime`, linhas 471/602/607) exigem
`[GroupWithZero R]`, corretamente inaplicável a `Z` (não é
`GroupWithZero`); `lcm_apply_mul_gcd_apply` (575) e
`eq_zero_of_squarefree_of_dvd_eq_zero` (612) são tecnicamente aplicáveis
mas estruturalmente ociosos (reparametrizações triviais do mesmo fato
único já fechado, sem consumidor em lugar nenhum do laboratório); e as
famílias `pmul`/`pdiv`/`ppow` de `Zeta.lean` (200-221) e o rearranjo de
`prodPrimeFactors` de `Misc.lean` (69-97) exigem genuinamente uma
segunda função aritmética não-motivada para emparelhar. **Nenhum
corolário `IsMultiplicative` barato adicional resta a propor nesta
sub-linha.** Isso não é, por si só, um item de execução — é o contexto
que explica por que BSD contribui apenas o item exploratório abaixo
nesta onda.

**BSD-7 — NEEDS_NARROWING (natureza exploratória, distinta dos demais
itens desta onda).** O recon original concluiu que BSD renderia ZERO
candidatos nesta rodada, escopando sua busca apenas à API
`ArithmeticFunction.IsMultiplicative` e a arquivos grepados pela string
literal "IsMultiplicative". Essa conclusão foi corretamente marcada
`NEEDS_NARROWING` porque a busca nunca leu nem mencionou
`03_MILLENNIUM/06_BSD/FORMAL/HasseCoefficientRecursionBound.lean`
(rotulado BSD-3, 299 linhas), que fica no MESMO diretório FORMAL do
arquivo que o recon de fato leu. Releitura integral confirma que esse
arquivo já prova, incondicionalmente e com trabalho real (um argumento
de polinômio de Chebyshev de segunda espécie construído do zero, já que
nenhuma cota empacotada existia no Mathlib), que uma recursão real de
dois termos satisfazendo uma hipótese explícita de forma Hasse (`|a| ≤
2√q`) tem coeficientes limitados por `(n+1) q^(n/2)`. O próprio
docstring do arquivo nomeia explicitamente o próximo passo NÃO tentado:
"transformar esta cota local de coeficiente numa cota global de
coeficiente de série de Dirichlet via multiplicatividade... mais um
argumento de soma-sobre-primos genuíno — nenhum dos dois tentado aqui",
visando eventualmente invocar
`LSeriesSummable_of_le_const_mul_rpow`
(`NumberTheory/LSeries/Basic.lean:341`, citado pelo texto do próprio
arquivo, não regrepado de forma independente nesta rodada). O passo-ponte
natural — relacionar `coeff n (W.localPowerSeries R)` (via a fórmula
recursiva de `PowerSeries.invOfUnit`, soma sobre antidiagonal,
`RingTheory/PowerSeries/Inverse.lean:87-93`) com a recursão abstrata
`cSeq` para um único primo de boa redução — é, por si só, não-trivial
(a recursão de `invOfUnit` é uma soma sobre antidiagonal, não
literalmente a forma de dois termos que `cSeq` usa; casá-las exige
manipulação algébrica real), e mesmo se fechado produziria apenas mais
um lema gated por hipótese (cota de Hasse ASSUMIDA, não provada, como
`BSD-3` já faz), ainda longe de somabilidade, continuação analítica, ou
qualquer alegação relevante a BSD. Tamanho comparável ao que já
descartou `BSD-GAP-008` do ciclo de ondas nas rodadas anteriores — este
item deve ser tratado como uma TRIAGEM estreita e bounded, não como um
alvo de confiança plena equivalente aos demais desta onda.
**Teste revisado (triagem, bounded):** para uma curva de Weierstrass `W`
sobre um corpo de números `K` e um lugar `p : HeightOneSpectrum (𝓞 K)`
com `W.HasGoodReduction (p.adicCompletionIntegers K)`, expressar
`PowerSeries.coeff n (W.localPowerSeries (p.adicCompletionIntegers K))`
como `TamesisLab.BSD3.cSeq a q n`, onde `a`/`q` são lidos do ramo de boa
redução de `W.localPolynomial`, com `q := Nat.card (corpo de resíduo)` e
`a` como definido no docstring de `localPolynomial` — como identidade de
coeficiente NUA, sem hipótese de Hasse para este passo. Reportar
pass/fail SÓ nessa identidade isolada (não empacotar a aplicação da cota
de Hasse nem nenhuma alegação de somabilidade); se exigir mais do que
uma prova pequena e autocontida (referência aproximada: comparável ou
menor que os ~30 linhas de conteúdo genuinamente novo de
`BSD6LFunctionEqOnPrimePowers.lean`, não os ~230 de maquinaria nova de
`BSD-3`), reportar como item por si só grande demais e fora de escopo de
onda, mesmo tratamento dado a `BSD-GAP-008`.

---

## 6. Síntese TOE (extensão interna do laboratório — NÃO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| TOE-6a | `no_surjective_reverse_functor` (dual sobrejetivo de `TOE-5`) | SURVIVES | baixo |
| TOE-6b | `F` (o funtor canônico `KCat ⥤ ShiftCat`) não é `Full` | SURVIVES | baixo |

**Passo original vs. o que mudou.** `TOE-6a` é o dual sobrejetivo direto
de `no_injective_reverse_functor` (`TOE-5`, Onda 5). `TOE-6b` continua
de `KToShiftFunctorNotFaithfulNoReverse.lean` (`TOE-4`, Onda 4), que já
prova que `F` não é `Faithful`, mas nunca examina `Full`.

**TOE-6a — SURVIVES.** Releitura integral de
`NoInjectiveReverseFunctorShiftCatKCat.lean` (`TOE-5`, Onda 5) confirma
`no_injective_reverse_functor (G : ShiftCat ⥤ KCat) (hinj :
Function.Injective G.obj) : False` exatamente como descrito, provado por
pombos direto (sem `Finite.injective_iff_bijective`). Toda citação
Mathlib conferida verbatim: `Action.lean:86`, `def objEquiv : X ≃
ActionCategory M X` (com `left_inv := coe_back`, `right_inv :=
back_coe`, linhas 77/81); `Data/Fintype/Card.lean:348`, `theorem
Finite.injective_iff_surjective_of_equiv {f : α → β} (e : α ≃ β) :
Injective f ↔ Surjective f` sob `[Finite α]`; `Data/Finite/Defs.lean:110`,
`theorem Finite.of_equiv (α : Sort*) [h : Finite α] (f : α ≃ β) : Finite
β`. Confirmado `instance : Fintype Regime3`
(`Foundations/Semigroups/Regime3.lean:33`) fornece `Finite Regime3` de
graça, e `KCat = ActionCategory K Regime3`
(`MonoidKConstantActionDistinctEndomorphisms.lean:172`), então `objEquiv
K Regime3 : Regime3 ≃ KCat` também typechecka, tornando `e : ShiftCat ≃
KCat` sólido. Grep no diretório TOE inteiro confirma ausência prévia de
instância `Fintype`/`Finite` sobre `ShiftCat`/`KCat` e de qualquer
resultado sobre funtor reverso sobrejetivo — território genuinamente
novo. A matemática (`mpr` do iff `Injective G.obj ↔ Surjective G.obj`
transforma `hsurj` em `hinj`, depois reusa o teorema de `TOE-5`
verbatim) é trivialmente correta.
**Teste:** `theorem no_surjective_reverse_functor (G : ShiftCat ⥤ KCat)
(hsurj : Function.Surjective G.obj) : False := by haveI : Finite
ShiftCat := Finite.of_equiv Regime3 (objEquiv Shift3 Regime3); exact
no_injective_reverse_functor G
(Finite.injective_iff_surjective_of_equiv (objEquiv K Regime3) |>.mpr
hsurj |> ...)` — na prática, invocar
`(Finite.injective_iff_surjective_of_equiv e).mpr hsurj` (com `e :
ShiftCat ≃ KCat` via `objEquiv`) para obter `Function.Injective G.obj`,
fechando via `no_injective_reverse_functor` (`TOE-5`, já provado). Sem
estreitamento adicional necessário — apenas conferir em edição que a
resolução de instância `Finite`/`Fintype` não colide de namespace.
`#print axioms` limpo.

**TOE-6b — SURVIVES.** Releitura integral de
`KToShiftFunctorNotFaithfulNoReverse.lean` (`TOE-4`, Onda 4) confirma
ambos os fatos citados byte-a-byte: `homK_beta_gamma_isEmpty : IsEmpty
((show KCat from Regime3.beta) ⟶ (show KCat from Regime3.gamma))`
(linhas 123-125) e `instance shiftCat_hom_nonempty (p q : ShiftCat) :
Nonempty (p ⟶ q)` (linhas 170-171), provado para TODO par ordenado.
Confirmado `F : KCat ⥤ ShiftCat` (linhas 189-193) com `obj p := show
ShiftCat from p.back`, então `F.obj (show KCat from Regime3.beta)`
reduz (via `coe_back`, `rfl`) a `show ShiftCat from Regime3.beta` —
tornando `shiftCat_hom_nonempty` aplicável exatamente no par necessário.
Confirmado `class Full (F : C ⥤ D) : Prop where map_surjective {X Y :
C} : Function.Surjective (F.map (X := X) (Y := Y))`
(`CategoryTheory/Functor/FullyFaithful.lean:45-46`) e o padrão de
notação-ponto legítimo (`hF.map_surjective f`, uso próprio do Mathlib em
`FullyFaithful.lean:74-76`). O argumento — uma função saindo de domínio
vazio (`Hom_K(beta,gamma)`) não pode sobrejetar num codomínio não-vazio
(`Hom_Shift(F.obj beta, F.obj gamma)`) — é elementar e correto. Grep no
diretório TOE inteiro confirma nenhum trabalho prévio sobre
`Full`/`not_full` — genuinamente novo.
**Teste:** `theorem F_not_full (hF : F.Full) : False := by obtain ⟨g⟩ :=
shiftCat_hom_nonempty (F.obj (show KCat from Regime3.beta)) (F.obj (show
KCat from Regime3.gamma)); obtain ⟨f, _⟩ := hF.map_surjective g; exact
homK_beta_gamma_isEmpty.false f` (ou equivalente com `.elim`/`.false'`
caso o `motive` explícito seja necessário — puramente detalhe de
engenharia de tática, não risco à alegação falsificável). `#print
axioms` limpo.

---

## 7. Fundamentos Quânticos / Unificação (extensão interna — NÃO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| QF-10 | Empacotar o fluxo de Heisenberg em `MonoidHom (Multiplicative R) -> unitary(Matrix 2x2 C)` | SURVIVES | baixo |
| QF-11 (esticado, sonda isolada primeiro) | Elevar a `ContinuousMonoidHom` | NEEDS_NARROWING | baixo (sonda) / incerto (empacotamento completo) |

**Passo original vs. o que mudou.** Ambos continuam de
`HeisenbergFlowUnitarity.lean` (QF-7), `heisenbergFlow_add` (QF-9, Onda
5) e da preservação de norma/produto interno (QF-8, Onda 5). `QF-10`
empacota os três fatos pontuais já fechados num objeto algébrico único
que preserva estrutura. `QF-11` tenta ir além, elevando esse
empacotamento a contínuo.

**QF-10 — SURVIVES.** Toda citação Mathlib re-verificada por
grep/leitura direta contra o snapshot vendorizado: `MonoidHom.mk'`
(`Algebra/Group/Hom/Defs.lean:589`, precisa `[Group G] [MulOneClass
M]`, `map_one'` derivado via `mul_right_cancel_iff`); `unitary R`'s
instância `Group` (`Algebra/Star/Unitary.lean:96`, `inv := star,
inv_mul_cancel := star_mul_self`), independente de qual instância de
norma/topologia escopada esteja aberta (sem risco de diamante ali);
`Multiplicative.group` (`Algebra/Group/TypeTags/Basic.lean:467`) com
`ofAdd_add`/`toAdd_mul` ambos `rfl` (linhas 160/163); `StarRing (Matrix
n n a)` (`LinearAlgebra/Matrix/ConjTranspose.lean:431`, instância
global, não escopada). Grep em todo o Mathlib por
`OneParameterGroup`/`OneParamGroup` retorna zero — confirma não existir
atalho de empacotamento pronto. Nenhuma infraestrutura de teorema de
Stone/operador ilimitado/CCR existe (grep por "Stone" só retorna
`StoneWeierstrass`/`StoneCech`/`Stonean`, sem relação). Releitura da
prova de `heisenbergFlow_add` (QF-9) confirma seus próprios
`Commute.smul_right`/`smul_left` corretos. O único risco real
sinalizado pelo próprio candidato — re-derivar a lei de adição de QF-9
sob `Matrix.Norms.L2Operator` em vez de `Matrix.Norms.Operator` —
verificado independentemente: a seção `'Rat'` de `Exponential.lean`
precisa só `[NormedRing][NormedAlgebra Q][CompleteSpace]`, e
`Matrix.instL2OpNormedRing`/`instL2OpNormedAlgebra`
(`CStarAlgebra/Matrix.lean:264,268,280,283`) fornecem exatamente isso
sob o escopo `L2Operator`, sem nenhuma dependência de `star` na cadeia
de adição (os fatos `Commute` vêm de `Matrix.instAlgebra`,
independente de escopo de norma) — troca de escopo muito provável de
funcionar sem novo diamante, diferente do diamante específico de `star`
que QF-7 já teve. Passo genuíno de qualidade (objeto algébrico
empacotado vs. três fatos pontuais desconectados), teste estreito e
concreto, custo baixo bem fundamentado.
**Teste:** construir `heisenbergFlowHom : Multiplicative R →*
unitary (Matrix (Fin 2) (Fin 2) C)` via `MonoidHom.mk'` com `toFun := fun
t => ⟨exp (t.toAdd • heisenbergGenerator), (prova de unitariedade de
QF-7)⟩` e `map_mul' := fun s t => by rw [toAdd_mul];
exact Subtype.ext (heisenbergFlow_add s.toAdd t.toAdd)` (reusando QF-9);
um único typecheck de arquivo novo. `#print axioms` limpo.

**QF-11 — NEEDS_NARROWING.** As citações estruturais conferem
precisamente: `ContinuousMonoidHom`
(`Topology/Algebra/ContinuousMonoidHom.lean:57`, `structure ...
extends A ->* B, C(A, B)`); `NormedSpace.exp_continuous`
(`Analysis/Normed/Algebra/Exponential.lean:507`, precisa só as mesmas
instâncias `[NormedRing][NormedAlgebra Q][CompleteSpace]` que QF-9 já
estabelece); `continuous_induced_rng` (`Topology/Order.lean:788`); e
adicionalmente confirmado (não citado pelo candidato original) que
`unitary R` herda a topologia induzida/de subtipo via
`instTopologicalSpaceSubtype` (`Topology/Defs/Induced.lean:76`), e que
`Matrix.instL2OpMetricSpace`'s `replaceTopology` de fato casa com a
topologia `Pi` ambiente padrão (`CStarAlgebra/Matrix.lean:157-171`).
PORÉM: a continuidade de `t ↦ t.toAdd • heisenbergGenerator` em si exige
uma instância `ContinuousSMul R (Matrix (Fin 2)(Fin 2) C)` (ou
equivalente) que resolva sob a pilha de instância específica,
`L2Operator`-escopada, modificada por `replaceTopology`. Busca em
`Analysis/Normed/Module/Basic.lean` e `Analysis/Normed/Group/Basic.lean`
por `instance.*ContinuousSMul` não encontrou nada citável de forma
limpa e direta como as outras três citações — quase certamente verdade
de forma genérica (sustenta a própria prova de `exp_continuous`), mas o
candidato nunca nomeia a cadeia de instância/lema que de fato descarrega
esse passo. Dado o histórico desta linha de exatamente este tipo de
fricção específica de escopo (o diamante `ContinuousStar` documentado de
QF-7), e a própria autoavaliação apenas "média" do candidato, o teste
deve ser estreitado para isolar esse único passo genuinamente não
verificado ANTES de tentar o empacotamento completo.
**Teste revisado (sonda isolada primeiro):** verificar, isoladamente,
antes de tentar o empacotamento `ContinuousMonoidHom`, se `Continuous
(fun t : R => t • heisenbergGenerator : R -> Matrix (Fin 2)(Fin 2) C)`
typechecka via `lake env lean` sob `open scoped
Matrix.Norms.L2Operator` (via `Continuous.smul`/`continuous_smul` ou o
próprio padrão de prova de `exp_continuous`). Se a síntese de instância
para `ContinuousSMul R (Matrix (Fin 2)(Fin 2) C)` falhar ou não
terminar sob o escopo `L2Operator` modificado por `replaceTopology`,
`QF-11` fica refutado como proposto e precisaria de uma instância
`ContinuousSMul` fornecida à mão (espelhando o conserto manual de
`NormedAlgebra Q` já feito para QF-7) antes de qualquer tentativa
adicional na cadeia.

---

## Infraestrutura compartilhada entre frentes (continuação)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| SHARED-6A | Identidade de discriminante/fórmula quadrática em dimensão 2 | SURVIVES | baixo |

**Passo original vs. o que mudou.** Continuação de `SHARED-5A` (Onda
5), que já fecha a fatoração do polinômio característico simétrico em
dimensão 2 (`charpoly = (X-C lambdaMax)*(X-C lambda2)`) via
`LinearMap.IsSymmetric.charpoly_eq`. SHARED-6A tenta extrair dessa
fatoração (mais os já-fechados `lambdaMax_mul_lambda2_eq_det` e traço =
soma dos dois autovalores) a identidade de discriminante
`(lambdaMax-lambda2)^2 = trace^2 - 4*det` e o corolário de fórmula
quadrática `lambdaMax = (trace+sqrt(trace^2-4det))/2`.

**SHARED-6A — SURVIVES.** Proveniência de Onda 5 re-verificada por
leitura integral (não confiada a resumo):
`CharpolyFactorizationDim2.lean` (288 linhas),
`LambdaMaxMulLambda2EqDet.lean` (287 linhas),
`TwoEigenvalueExhaustiveness.lean` (287 linhas) todas confirmadas
provando o que alegam. Confirmados os 7 arquivos de
`_SHARED_INFRA/FORMAL`; `lakefile.toml` confirmado com exatamente um
`[[lean_lib]] name='TamesisLab'`, sem alvo `SHARED_INFRA`. Suporte
Mathlib re-verificado a partir do código-fonte: `Real.sqrt_sq (h :
0<=x) : sqrt(x^2)=x` em `Analysis/Real/Sqrt.lean:181`;
`LinearMap.IsSymmetric.eigenvalues_antitone : Antitone (hT.eigenvalues
hn)` confirmado em `Spectrum.lean:312-318`, que por definição de
`Antitone` dá `lambda2 T <= lambdaMax T` a partir de `0<=1`, após
substituir as duas identificações já fechadas (não é lema literalmente
reusável verbatim — precisa de 2-3 linhas de derivação, correção a um
pequeno exagero retórico do candidato original, que alegava a ordem já
"provada inline"); `trace_eq_sum_eigenvalues` confirmado em
`InnerProductSpace/Trace.lean:39`. Álgebra conferida à mão: `(a-b)^2 =
a^2-2ab+b^2 = (a+b)^2-4ab`, então `(lambdaMax-lambda2)^2 =
trace^2-4*det` segue por substituição das identidades já fechadas
(`trace=lambdaMax+lambda2`, gratuito por definição; `det=lambdaMax*lambda2`,
`SHARED-4B`) fechado por `ring` — genuinamente trivial. O corolário de
fórmula quadrática também confere: `sqrt((lambdaMax-lambda2)^2) =
lambdaMax-lambda2` via `Real.sqrt_sq` uma vez a não-negatividade em
mãos, então `trace + (lambdaMax-lambda2) = 2*lambdaMax` algebricamente.
Nenhuma duplicação encontrada: grep na árvore `03_MILLENNIUM` inteira
por `discriminant`/`quadratic_formula`/`sqrt_sq`/`lambdaMax_sub_lambda2`
— zero hits, território genuinamente livre. Correção factual ao
brief da própria tarefa confirmada verdadeira: grep em `06_BSD` por
`eigenvalue`/`IsSymmetric`/`rayleighQuotient` — zero hits; os arquivos de
BSD são genuinamente conteúdo de curva elíptica/função-L sem
sobreposição de operador espectral. Escopo do candidato correto e
honesto: sem relevância a Problema do Milênio, não atualmente
load-bearing para nenhum arquivo consumidor (grep confirma nenhum
consumidor já precisando desta forma), com gatilho de falsificação
próprio (descartar se `ring`/`nlinarith`/`Real.sqrt_sq` não fecharem).
**Teste revisado:** mesmo teste falsificável proposto, com uma correção
de precisão — declarar explicitamente, como `have` intermediário,
`lambda2 T <= lambdaMax T` derivado via `lambdaMax_eq_eigenvalues_zero`,
`lambda2_eq_eigenvalues_one` e `hT.eigenvalues_antitone hn (by decide :
(0:Fin 2) <= 1)` (derivação de ~2-3 linhas, não lema verbatim
reusável) antes de invocar `Real.sqrt_sq` — fora isso, idêntico. Se
`ring`/`nlinarith` não fechar a identidade de discriminante a partir dos
fatos de traço/det reproduzidos, ou a derivação de ordem precisar de
mais que `eigenvalues_antitone` mais as duas identificações, descartar o
candidato como proposto.

---

## Lista de execução Onda 6 (despacho direto para agente de formalização)

Cada item abaixo traz o candidato, o teorema-alvo, e o enunciado de
teste exato (já revisado pela adversarial), pronto para um agente de
formalização executar sem reinterpretação. Ordem: por linha, mesma
sequência das seções acima. Todos são independentes entre si, exceto
onde anotado (item 5 depende do item 4; item 8, marcado exploratório,
pode terminar em "fora de escopo" sem invalidar os demais 12). A linha
PN não participa (retirada por DEC-100 — ver Enquadramento honesto).

```text
 1. RH / RH-7A (composição cota de taxa + eigCount, namespace único)
    Em arquivo novo (namespace único), reproduzir byte-a-byte o bloco
    UnboundedEigCountEigCountBridge ate unboundedEigCount_eq_eigCount e
    a derivacao de piso-sanduiche de unboundedEigCount_rate_bound,
    ambos sobre o MESMO Tp/unboundedEigCount local. Fechar, para
    Lam>0: 0 < (eigCount T ((Lam+1)^-1):R)/Lam-1 ∧
    (eigCount T ((Lam+1)^-1):R)/Lam-1 <= 1/Lam via rw [<-
    unboundedEigCount_eq_eigCount hLam.le]; exact
    unboundedEigCount_rate_bound hLam, usando os nomes locais do
    proprio arquivo. #print axioms limpo.

 2. RH / RH-7B (Tp e formalmente autoadjunto no suporte finito)
    Reproduzir o bloco minimo finiteSupport/TpFun/Tp/Tp_apply, entao
    provar Tp_isFormalAdjoint : Tp.IsFormalAdjoint Tp via lp.hasSum_inner
    em ambos os lados + funext + Complex.conj_natCast + ring, fechado
    por HasSum.unique. NAO tentar IsSelfAdjoint/T.adjoint=T neste item
    -- declarar no cabecalho que e alegacao separada nao tentada.
    #print axioms limpo.

 3. NS / NS-6A (monotonicidade cruzada-compacta com raio auto-derivado)
    Derivar R1/R2 via Classical.choose de
    Bornology.IsBounded.subset_closedBall_lt; converter hK1R1/hK2R2 via
    SetLike.coe_subset_coe.mpr (K.isCompact.isBounded.subset_closedBall_lt
    0 0).choose_spec.2; instanciar diretamente
    pvKCLM_cross_compact_monotone (NS-5A, Onda 5) com esses raios.
    Nenhuma hipotese de raio/envelope livre no enunciado final.

 4. YM / YM-CAPSTONE-TRACE-M1-EXACT (traco exato de M1, bracket
    estreitado de lambda2)
    Provar trace_toEuclideanCLM_M1_eq_four_point_one seguindo o padrao
    de trace_toEuclideanCLM_M2_eq_four (LinearMap.trace_eq_sum_inner +
    Matrix.inner_toEuclideanCLM + Fin.sum_univ_two + norm_num); derivar
    lambda2 (toEuclideanCLM M1) ∈ [1.0,1.2] via unfold lambda2; rw
    [...]; constructor <;> linarith.

 5. YM / YM-CAPSTONE-DET-BRACKET-TIGHTENED (gated no item 4)
    So apos o item 4 fechar: provar 2.9 <= det(toEuclideanCLM M1) <=
    3.72 via lambdaMax_mul_lambda2_eq_det + lambdaMax_M1_bracket +
    o novo bracket [1.0,1.2] de lambda2; constructor <;> nlinarith
    [...].

 6. HG / HG-1h (principalCycle_a0 multiplicativo)
    theorem principalCycle_a0_mul (a0 b0 : Z) (ha0 : a0≠0) (hb0 : b0≠0)
    (hab : a0*b0≠0) : principalCycle_a0 (a0*b0) hab = principalCycle_a0
    a0 ha0 + principalCycle_a0 b0 hb0, via ext +
    Function.locallyFinsuppWithin.coe_add + algebraMap_eq_genf +
    RingHom.map_mul + Scheme.ord_mul + Pi.add_apply + omega/ring.

 7. HG / HG-4g (quociente por HolomorphicTransitionSubgroup e
    Nontrivial)
    theorem holomorphicTransitionQuotient_nontrivial : Nontrivial
    ((C -> C)ˣ ⧸ HolomorphicTransitionSubgroup) :=
    QuotientGroup.nontrivial_iff.mpr
    holomorphicTransitionSubgroup_ne_top. Uma linha.

 8. BSD / BSD-7 (exploratorio/triagem -- identidade-ponte de
    coeficiente, escopo bounded)
    Para W sobre K, p com boa reducao, expressar PowerSeries.coeff n
    (W.localPowerSeries (p.adicCompletionIntegers K)) como
    TamesisLab.BSD3.cSeq a q n (a/q lidos de localPolynomial, q :=
    Nat.card do corpo de residuo) -- identidade NUA, sem hipotese de
    Hasse, sem aplicacao de cota, sem alegacao de somabilidade. Se
    exigir mais que uma prova pequena e autocontida (referencia: <=
    ordem de grandeza dos ~30 linhas novas de BSD6), reportar como fora
    de escopo de onda, mesmo tratamento de BSD-GAP-008.

 9. TOE / TOE-6a (funtor reverso sobrejetivo tambem impossivel)
    theorem no_surjective_reverse_functor (G : ShiftCat ⥤ KCat) (hsurj
    : Function.Surjective G.obj) : False, via haveI : Finite ShiftCat
    (Finite.of_equiv Regime3 objEquiv); converter hsurj em
    Function.Injective G.obj via
    Finite.injective_iff_surjective_of_equiv (e : ShiftCat ≃ KCat);
    fechar via no_injective_reverse_functor (TOE-5, ja provado).

10. TOE / TOE-6b (F : KCat ⥤ ShiftCat nao e Full)
    theorem F_not_full (hF : F.Full) : False := by obtain ⟨g⟩ :=
    shiftCat_hom_nonempty (F.obj (show KCat from Regime3.beta)) (F.obj
    (show KCat from Regime3.gamma)); obtain ⟨f,_⟩ := hF.map_surjective
    g; exact homK_beta_gamma_isEmpty.false f.

11. QF / QF-10 (fluxo de Heisenberg empacotado como MonoidHom para
    unitary)
    Construir heisenbergFlowHom : Multiplicative R →* unitary (Matrix
    (Fin 2)(Fin 2) C) via MonoidHom.mk' com toFun := fun t =>
    ⟨exp (t.toAdd • heisenbergGenerator), (unitariedade de QF-7)⟩ e
    map_mul' via toAdd_mul + heisenbergFlow_add (QF-9). Reportar sob
    qual escopo (Operator ou L2Operator) de fato fechou.

12. QF / QF-11 -- sonda isolada (pre-requisito antes do empacotamento
    ContinuousMonoidHom completo)
    Verificar isoladamente se Continuous (fun t : R => t •
    heisenbergGenerator) typechecka sob open scoped
    Matrix.Norms.L2Operator via Continuous.smul/continuous_smul ou o
    padrao de NormedSpace.exp_continuous. Se a sintese de
    ContinuousSMul R (Matrix (Fin 2)(Fin 2) C) falhar sob esse escopo,
    reportar como bloqueado e nao tentar o empacotamento
    ContinuousMonoidHom completo ate suprir a instancia a mao.

13. SHARED-INFRA / SHARED-6A (discriminante/formula quadratica em
    dim 2)
    Para E:=EuclideanSpace R (Fin 2), T : E →L[R] E, hT :
    (T:E →ₗ[R] E).IsSymmetric, hn : Module.finrank R E = 2 (reproduzindo
    lambdaMax/lambda2/as identificacoes de SHARED-4A/4B/5A verbatim),
    provar have hord : lambda2 T <= lambdaMax T via
    lambdaMax_eq_eigenvalues_zero/lambda2_eq_eigenvalues_one +
    hT.eigenvalues_antitone hn (by decide); entao (lambdaMax T - lambda2
    T)^2 = (trace T)^2 - 4*det T via ring a partir de trace=soma e
    det=produto ja fechados; entao o corolario de formula quadratica
    lambdaMax T = (trace T + Real.sqrt ((trace T)^2-4*det T))/2 via
    Real.sqrt_sq hord-derivada + algebra.
```

Total: **13 itens numerados**, correspondendo a **13 candidatos
distintos** (nenhum item desta onda precisou de divisão em
estágios-gated internos como `HG-4F` nas Ondas 4-5 — a única
dependência sequencial entre CANDIDATOS diferentes é item 5 sobre item
4, mesma convenção de dependência já usada pela Onda 5 para o item 10
sobre o item 7). Contando por linha: RH(2) + NS(1) + YM(2) + HG(2) +
BSD(1, exploratório) + TOE(2) + QF(2) + SHARED-INFRA(1) = **13**. Isso é
**menor** que os 14 da Onda 5 — queda honesta, não forçada: NS, BSD e
SHARED-INFRA cada uma rendeu apenas 1 item (afinamento notável frente a
Ondas anteriores), e o item de BSD tem natureza explicitamente
exploratória/bounded, distinta de confiança plena. Nenhum item derivado
de candidato `REFUTED` (nenhum foi `REFUTED` nesta rodada).

---

## Avaliação pessoal — os candidatos com maior chance de virar
resultado formal honesto e não-trivial mais cedo

Não é repetição da autoavaliação dos agentes de recon/adversarial — é
julgamento próprio depois de sintetizar as 13 verificações desta onda.

**1. YM-CAPSTONE-TRACE-M1-EXACT (item 4).** Aritmética `norm_num` pura
sobre um decimal (`2.1`) que o MESMO arquivo já resolve com sucesso em
três outras chamadas (`M1_isHermitian`, `diff_eq_diagonal`,
`sonda2_numeric_norm`) — precedente direto, sem risco novo. O bracket
resultante é conferido à mão contra os autovalores reais. Risco técnico
residual: mínimo.

**2. TOE-6a (item 9).** Puro dual do teorema já provado e verificado à
mão na Onda 5 (`TOE-5`); a única peça nova (`Finite.injective_iff_surjective_of_equiv`
+ `Finite ShiftCat` via `Finite.of_equiv`) é uma composição de instância
padrão sem maquinaria de risco. Generalização limpa e natural.

**3. HG-1h (item 6).** Exercício de reindexação puro sobre uma base já
generalizada (`HG-1g`) que a própria Onda 5 já demonstrou funcionar para
o mesmo tipo de dependência, e de fato mais simples que o caso de
divisão já fechado (não precisa de definição de empacotamento nova).
Nenhuma citação Mathlib nova de risco.

**4. HG-4g (item 7).** Uma linha genuína, `QuotientGroup.nontrivial_iff.mpr`,
sem maquinaria de instância `Normal`/`DivisionMonoid` alguma — mais
simples ainda que os itens acima em termos de superfície de risco.

Não incluo `RH-7A` no topo apesar de sólido: exige montar um arquivo
novo reproduzindo dois blocos byte-a-byte sob namespace compartilhado
antes do `rw` final valer — mais passos de elaboração que os itens
acima. `QF-11` (item 12) fica de fora por natureza: é uma sonda
desenhada para PODER falhar informativamente, não uma aposta de
fechamento. `BSD-7` (item 8) fica de fora pela mesma razão, com
probabilidade adicional de terminar em "fora de escopo" antes mesmo de
uma tentativa de prova completa — resultado válido e esperado, não uma
falha do item.

## O laboratório chegou ao ponto de pausar o ciclo de ondas?

Avaliação honesta, atualizando a da Onda 5 (não repetindo-a).

**O que mudou desde a Onda 5:** a retirada operacional da linha PN
(DEC-100) já aconteceu e está refletida neste documento (PN não faz
mais parte do reconhecimento padrão). A pergunta em aberto que a Onda 5
levantou — "alguma OUTRA linha vai mostrar o mesmo sinal de exaustão"
— tem agora uma resposta parcial: **nenhuma segunda linha caiu a
zero**, mas **BSD chegou perto**. A sub-linha `IsMultiplicative` de BSD
(a única fonte de candidatos baratos de BSD desde a Onda 4) está
confirmada genuinamente esgotada nesta rodada — todos os corolários
`IsMultiplicative` remanescentes no Mathlib são estruturalmente
inaplicáveis ou ociosos. O único item que BSD rendeu nesta onda não veio
dessa sub-linha: veio de uma linha de pesquisa ADJACENTE
(`HasseCoefficientRecursionBound.lean`, BSD-3) que o próprio recon
inicial não tinha nem mencionado, e mesmo esse item é explicitamente
exploratório, com risco real de terminar em "fora de escopo de onda".
NS e SHARED-INFRA também afinaram para 1 item cada — sinal mais fraco
que o de BSD (nenhum dos dois teve uma sub-linha inteira declarada
esgotada), mas na mesma direção.

**Quatro observações atualizadas:**

1. **BSD é agora o segundo candidato mais claro, depois de PN, para uma
   mudança de modo — mas o próximo passo é diferente do de PN.** Para
   PN, a resposta certa foi retirada operacional da rotação (nada mais
   a compor). Para BSD, a Onda 5 já tinha identificado `BSD-GAP-008`
   (Mordell-Weil fraco, cinco lacunas formais nomeadas) como candidato
   maduro para um PROJETO DEDICADO fora do ciclo de ondas — esta onda
   fortalece esse diagnóstico com um segundo sinal concreto: a
   sub-linha de sondas pequenas de BSD (`IsMultiplicative`) secou de
   vez, e a única fonte alternativa de item pequeno (BSD-3) é ela
   mesma uma ponte para as mesmas cinco lacunas maiores, não uma nova
   veia de sondagem barata. Recomendação concreta para a próxima
   revisão de portfólio: abrir o projeto dedicado `BSD-GAP-008` em vez
   de continuar tentando espremer itens de onda pequenos e cada vez
   mais indiretos da linha BSD.

2. **`TOE_INTERFACE_EXECUTION` continua sendo um gate nomeado e nunca
   disparado**, sem mudança de status desde a Onda 4/5 — `TOE_SCOPE.md`
   segue existindo como esqueleto, e o ciclo de ondas continuou tratando
   TOE como mais uma linha de sondas pequenas (`TOE-6a`/`TOE-6b` nesta
   rodada) em vez de investir na síntese completa. Nenhum evento desta
   onda muda essa avaliação.

3. **RH, HG, QF e YM continuam gerando alvos baratos e genuinamente
   novos, sem sinal de esgotamento equivalente ao de PN ou BSD.** RH
   manteve 2 itens (um deles, `RH-7B`, fechando outro gap de honestidade
   genuíno, no mesmo padrão de `RH-6c` na Onda 5); HG manteve 2 itens
   igualmente baratos e mecânicos; QF manteve 2, um deles (QF-10) um
   passo de qualidade real (empacotamento algébrico, não só mais um
   fato pontual); YM produziu um par sequencial limpo. Não há
   justificativa honesta para encerrar TODO o ciclo de ondas enquanto
   quatro linhas seguem produzindo candidatos bem definidos.

4. **A contagem total (13, abaixo de 14) confirma a trajetória de
   afinamento gradual que a Onda 5 já vinha sinalizando, mas de forma
   NÃO-uniforme.** Como na Onda 5, a contagem agregada mascara o que de
   fato mudou: PN saiu do reconhecimento por completo, BSD ficou reduzido
   a um item de natureza distinta (exploratório/bounded), enquanto RH,
   HG, QF e YM mantiveram-se estáveis ou melhoraram a qualidade dos
   seus alvos (QF-10, HG-4g).

**Conclusão honesta, refinada em relação à Onda 5:** a resposta continua
HÍBRIDA, com o quadro ficando mais nítido a cada onda. (a) a linha PN
permanece formalmente retirada da rotação (DEC-100), sem mudança nesta
rodada; (b) `BSD-GAP-008` deve ser promovido, na próxima decisão de
portfólio, de "candidato maduro para projeto dedicado" (linguagem da
Onda 5) para "recomendação ativa" — a sub-linha de sondas pequenas de
BSD chegou ao mesmo tipo de fim de corda que PN atingiu na Onda 5, só
que um pouco mais devagar e com uma ressalva a menos de certeza (um
item exploratório ainda pode render algo pequeno, ao contrário de PN);
(c) `TOE_INTERFACE_EXECUTION` permanece candidato adiado, não urgente —
nenhum evento desta onda muda seu status; (d) as linhas restantes com
corda genuína (RH, HG, QF, YM, SHARED-INFRA) devem continuar no modo
onda-pequena-paralela até que produzam, elas também, um sinal de
esgotamento equivalente ao de PN/BSD — não há ainda justificativa para
declarar a varredura de portfólio inteira encerrada.

---

## O que este documento confirma sobre o processo

A disciplina de "reverificar por leitura direta de arquivo, checando
citação Mathlib por citação Mathlib, e fazendo a aritmética/álgebra à
mão quando aplicável" continuou achando coisas reais nesta rodada: uma
composição cross-file que não type-checkaria literalmente como escrita
por viver em namespaces distintas (`RH-7A`); uma citação de suporte
tecnicamente correta mas desnecessariamente pesada, com um lema Mathlib
estritamente mais simples encontrado na mesma vizinhança
(`HG-4g`, espelhando o padrão já visto em `NS-5A`/`SHARED-5A` na Onda
5); um passo de continuidade sem citação firme, isolado como sonda
separada antes do empacotamento completo em vez de assumido
silenciosamente (`QF-11`); e, o achado mais importante desta rodada, uma
linha de pesquisa adjacente inteira (`HasseCoefficientRecursionBound.lean`,
BSD-3) que o recon original simplesmente não mencionou ao concluir que
BSD não tinha candidato algum — achado que não inverteu a conclusão
prática (BSD continua rendendo só um item, de natureza exploratória),
mas expôs que "zero candidatos" precisa ser verificado por leitura de
diretório inteiro, não só de grep por um termo. Em nenhum caso isso
refutou um alvo subjacente — em todos, o resultado real continuou de
pé, só precisou de reescopo, de uma citação mais direta, ou de uma
divisão mais honesta entre "sonda" e "resultado de confiança". A
composição por linha desta onda (PN fora da rotação; BSD reduzido a um
item exploratório; RH, HG, QF, YM, SHARED-INFRA seguindo estáveis) é o
sinal estrutural mais importante — não um erro encontrado num
candidato, mas a confirmação gradual, onda a onda, de que "compor
resultados já fechados" tem um teto por linha, e que esse teto está
começando a aparecer numa segunda linha (BSD) exatamente como a Onda 5
previu que aconteceria eventualmente com outras.
