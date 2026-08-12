---
document_id: PLANO-ATAQUE-ONDA-7-2026-08-11
reviewed_at: 2026-08-11
input: recon + revisao adversarial de 8 grupos (7 linhas de pesquisa + infraestrutura compartilhada) para Onda 7, ancorado nos resultados reais da Onda 6 -- ver 09_SESSIONS/2026/2026-08-11_WAVE6_EXECUTION.md (13/13 CLOSED, 0 GAP_DIAGNOSED, 0 REJECTED -- segundo fechamento total consecutivo do ciclo, mas com um achado explicito de disciplina de escopo em BSD-7, ~6,4x acima do proprio teto declarado) e 01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_5_2026_08_11.md, 01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_6_2026_08_11.md. Linha PN retirada formalmente da rotacao de reconhecimento por DEC-100 (nao reavaliada nesta onda).
conclusion: PLANO_DE_EXECUCAO_ONDA_7_PROPOSTO
---

# Plano de ataque — Onda 7 (continuação das Ondas 1-6)

## Enquadramento honesto

Este documento é a continuação direta de
`PLANO_DE_ATAQUE_PORTFOLIO_COMPLETO_2026_08_09.md`,
`PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md`,
`PLANO_DE_ATAQUE_ONDA_3_2026_08_10.md`,
`PLANO_DE_ATAQUE_ONDA_4_2026_08_10.md`,
`PLANO_DE_ATAQUE_ONDA_5_2026_08_11.md`,
`PLANO_DE_ATAQUE_ONDA_6_2026_08_11.md` e da sessão de execução
`2026-08-11_WAVE6_EXECUTION.md`. A Onda 6 fechou **13 de 13** itens (11
VERIFIED, 2 VERIFIED_WITH_NOTES), com **zero** `GAP_DIAGNOSED` e **zero**
`REJECTED` — o **segundo fechamento total consecutivo** do ciclo de
ondas (depois da Onda 5, que fechou 14/14). A Onda 7 parte desse chão
real.

```text
O que este plano E:
  - a próxima rodada de pequenos testes falsificáveis contra
    infraestrutura Mathlib genuína, construída sobre os 13 itens
    fechados na Onda 6 (e, por herança, sobre os 15+20+25+14+13 das
    Ondas 1-5)
  - uma tentativa de re-verificar, por leitura direta de arquivo (não
    por confiança no agente de recon), com verificação independente de
    citações Mathlib linha a linha, grep próprio contra o checkout
    Mathlib vendorizado, e conferência aritmética/algébrica à mão onde
    aplicável, se os alvos propostos continuam abertos, já foram
    satisfeitos por acaso, ou têm um defeito real
  - um teste explícito da lição de disciplina de escopo registrada em
    DEC-103 (o excesso de ~6,4x de BSD-7 na Onda 6): todo candidato
    desta onda que fica em território naturalmente propenso a
    scope-creep (BSD-8, o mais óbvio, mas também um candidato de YM que
    a própria adversarial pegou tentando a mesma manobra de contagem
    ambígua que inflou BSD-7) recebeu um teto de tamanho numérico,
    específico, checável, com instrução explícita de medir -- não
    estimar -- antes de declarar `CLOSED`
  - honesto sobre linhas sem alvo pequeno disponível nesta rodada (não
    houve nenhuma nesta onda -- todas as 7 linhas mais infraestrutura
    compartilhada renderam pelo menos um item, ver abaixo) e sobre onde
    um teste proposto tinha um defeito real (citação fabricada,
    manobra de composição que não type-checka como escrita, ou
    ambiguidade de contagem de linhas) que precisou de reescopo

O que este plano NAO E:
  - uma alegação de que qualquer Problema do Milênio ficou mais
    próximo de ser resolvido -- nenhum item abaixo toca o núcleo
    central de nenhuma das 6 frentes Clay-oficiais
  - uma reabertura da linha P vs NP (PN): PN permanece formalmente
    RETIRADA da rotação de reconhecimento desde a Onda 6 por DEC-100.
    Esta onda NÃO reavalia essa decisão -- PN simplesmente não faz
    parte do reconhecimento padrão de 8 grupos abaixo, exatamente como
    na Onda 6. `PNP-GAP-001..004` permanecem `OPEN`. Retirada
    OPERACIONAL e REVERSÍVEL, não um fechamento do problema P vs NP
  - uma alegação de que o fechamento de `BSD-GAP-007` (Onda 4) ou de
    qualquer identidade-ponte de coeficiente adicional (Onda 6, Onda 7)
    constitui progresso sobre a conjectura de Birch e Swinnerton-Dyer
    em si. `BSD-GAP-007` permanece `CLOSED`; `BSD-GAP-008`
    (Mordell-Weil fraco, cinco lacunas formais separadas) permanece
    `OPEN` e continua fora do escopo do ciclo de ondas
  - uma alegação de que `TOE-INTERFACE-001` ou `QCU-001` têm status
    Clay-oficial
  - uma reabertura do `RH-NOGO-001`
  - uma promessa de que todo teste "SURVIVES" fecha sem `sorry` -- é
    uma aposta informada, não uma certeza
  - uma tentativa de inflar a contagem de itens: onde a revisão
    adversarial encontrou um candidato genuinamente ausente do recon
    original (o terceiro item de YM abaixo) ou uma sub-linha
    corretamente deixada de fora da execução (`NS-7B`, ver seção 2),
    isso é reportado com a proveniência exata, não maquiado como se
    tivesse sido previsto desde o início
```

**14** candidatos revisados ao todo nos 8 grupos (7 linhas +
infraestrutura compartilhada — PN não faz parte do reconhecimento
padrão): RH(2) + NS(2, sendo 1 explicitamente não-proposto para
execução) + YM(2 do recon original + 1 achado pela adversarial) + HG(2)
+ BSD(1) + TOE(1) + QF(2) + SHARED-INFRA(1). A lista numerada de
execução da Onda 7 tem **13 candidatos distintos** — a mesma contagem
da Onda 6, mas por uma composição diferente e instrutiva: NS caiu para
1 item de execução (como na Onda 6), enquanto YM subiu para 3 porque a
adversarial encontrou um terceiro candidato — `YM-CAPSTONE-EIGVAL-
DICHOTOMY-TIGHTENED` — que o recon original tinha deixado passar por
completo, mesmo tipo de achado que `BSD-3`/`HasseCoefficientRecursion-
Bound.lean` foi na Onda 6. As duas quedas (NS) e o ganho (YM) se
cancelam na contagem agregada — sinal de que a estabilidade numérica
13→13 não deve ser lida como "nada mudou", ver seção de fechamento.

**Nenhum candidato foi `REFUTED` nesta rodada**, mas a adversarial
encontrou, de novo, defeitos reais e específicos que precisaram de
reescopo genuíno, não cosmético: `NS-7A` tinha uma alegação central
diretamente contradita pelo próprio teorema citado (a "independência de
raio" que a integral, na verdade, não tem); `HG-1i` citava corretamente
dois lemas Mathlib mas os emparelhava errado (`pow_succ'` com
`succ_nsmul`, quando o par correto documentado no próprio Mathlib é
`pow_succ'`/`succ_nsmul'`); `QF-13` citava uma "classe"
`StarAlgEquivClass` que na verdade é um namespace, não uma `class`, e
seu termo de prova proposto (`.toStarMonoidHom`) não se aplica ao tipo
em questão; e um candidato de YM (`LAMBDAMAX-M1-QUADRATIC-EXACT`)
repetiu, em miniatura, exatamente a manobra de contagem que inflou
`BSD-7` na Onda 6 (usar "preciso reproduzir mais coisa" como
justificativa para alargar, em vez de excluir, o teto de linhas novas).
Em todos os casos o alvo subjacente sobreviveu — a matemática está
correta e a infraestrutura Mathlib necessária existe — mas o teste
precisou de correção antes de autorização.

---

## 1. Riemann Hypothesis (RH) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| RH-7C | `Tp ≤ Tp.adjoint` via densidade + `le_adjoint` | SURVIVES | baixo |
| RH-7D | Forma quadrática `⟨Tp x, x⟩` real e `≥ 0` (positividade formal) | SURVIVES | moderado |

**Passo original vs. o que mudou.** Ambos continuam inteiramente dentro
do `LinearPMap` de brinquedo já usado por RH-3..RH-7B (Ondas 3-6), sem
nenhuma conexão com `riemannZeta`/RVM — confirmado de novo por releitura
de `ZetaZeros.lean` (74 linhas, só fatos de conjunto-nível sobre
`riemannZetaZeros`). `RH-7C` retoma o gap deixado por `RH-7B` (Onda 6):
provou apenas `IsFormalAdjoint`, não a desigualdade de operadores.
`RH-7D` tenta, pela primeira vez nesta linha, um argumento de
positividade formal do operador de suporte finito.

**RH-7C — SURVIVES.** Releitura integral de
`TpFormalAdjointProbe.lean` (210 linhas) e de
`DiagonalSelfAdjointOperatorProbe.lean` (273 linhas, Onda 1) confirma
todas as três alegações de sustentação: `LinearPMap.IsFormalAdjoint.
le_adjoint` (`LinearPMap.lean:195`, hipótese de seção `Dense`
confirmada presente), a instância `LE` de `LinearPMap`
(`LinearAlgebra/LinearPMap.lean:211`), e o padrão de prova idêntico
(lema de adjunto formal + lema de densidade → `le_adjoint`) já
compilando neste laboratório no próprio arquivo Wave-1
(`DiagonalSelfAdjointOperatorProbe.lean:266`, `dom_dense` nas linhas
149-154). A seção "ainda faltando" é precisa: não alcança
`IsSelfAdjoint Tp`, já que `finiteSupport` é subespaço próprio do
domínio maximal (testemunha `x_n = 1/(n+1)^2` conferida à mão:
quadrado-somável, `n*x_n` também quadrado-somável, mas `x` tem suporte
infinito) — logo `Tp ≤ Tp.adjoint` é estrita, exatamente como alegado.
Teto de 50 linhas novas não-comentário é hard, específico, e
confortavelmente folgado: `finiteSupport`, diferente do `Dom` do
arquivo Wave-1, contém trivialmente todo `lp.single`, sem o cômputo
tipo-`mulSeq` que o modelo precisou, então o lema de densidade análogo
aqui deve rodar notavelmente mais curto que seu modelo Onda-1 — baixo
risco de estouro estilo BSD-7. Nenhum overclaim RH/Millennium em lugar
algum do texto do candidato.
**Teste:** provar `Tp_le_adjoint : Tp ≤ Tp.adjoint` reproduzindo o
bloco mínimo `finiteSupport`/`TpFun`/`Tp` (mesmo padrão de
`Tp_isFormalAdjoint`, RH-7B/Onda 6), então uma prova de densidade de
`finiteSupport` em `H2` (trivial via `lp.single`, sem o cômputo
`mulSeq` do modelo Onda-1), fechando via
`LinearPMap.IsFormalAdjoint.le_adjoint` aplicado a
`Tp_isFormalAdjoint` mais a densidade. Teto: **50 linhas novas
não-comentário**. `#print axioms` limpo.

**RH-7D — SURVIVES.** Todas as cinco citações Mathlib conferidas no
local exato: `RCLike.inner_apply'` (`Basic.lean:915`),
`Complex.conj_natCast` (`Basic.lean:481`), `lp.hasSum_inner`
(`l2Space.lean:150`), `Complex.normSq_eq_conj_mul_self`
(`Basic.lean:544`), `Complex.normSq_nonneg` (`Basic.lean:554`). A
citação mais fraca autoassinalada pelo próprio candidato,
`hasSum_sum_of_ne_finset_zero`, é confirmada como declaração genuína
`to_additive`-gerada (dual de `hasProd_prod_of_ne_finset_one`,
`InfiniteSum/Defs.lean:296`, nomenclatura padrão `prod→sum`) com uso
real e compilável nos três pontos de chamada citados — a bandeira de
honestidade do candidato era justificada, mas a alegação subjacente se
sustenta. Ausência de `LinearMap.IsPositive` para `LinearPMap`
reconfirmada por grep fresco em todo o Mathlib. A redução `⟨Tp x,x⟩ =
Σ i·normSq(x_i)` é algebricamente correta dada a convenção de produto
interno do Mathlib (conjugado-linear no primeiro argumento) e `i:N`
convertido para valor não-negativo fixo por conjugação. Teto de 60
linhas (maior que o de RH-7C, com racional declarado: passo extra de
redução de soma finita) é hard e específico; a autoavaliação do próprio
candidato (custo moderado, plausibilidade média) é consistente com o
que foi encontrado. Nenhum overclaim RH/Millennium.
**Teste:** reproduzir o bloco mínimo `finiteSupport`/`TpFun`/`Tp`, então
provar `Tp_inner_self_real_nonneg : ∀ x ∈ Tp.domain, (inner (Tp x : H2)
(x:H2) : C).im = 0 ∧ 0 ≤ (inner (Tp x : H2) (x:H2) : C).re`, via
`RCLike.inner_apply'` + `lp.hasSum_inner` + `funext` +
`Complex.conj_natCast` reduzindo a `Σ i·normSq(x_i)`, fechado por
`Complex.normSq_nonneg`/`Complex.normSq_eq_conj_mul_self`. Teto: **60
linhas novas não-comentário**. `#print axioms` limpo.

---

## 2. Navier-Stokes (NS) — Clay oficial (núcleo Calderón-Zygmund)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| NS-7A | Corolário de independência de compacto/raio do funcional p.v. composto | NEEDS_NARROWING | moderado (revisado para cima) |

**Contexto factual — `NS-7B` corretamente NÃO proposto para execução
da Onda 7.** Releitura confirma por grep que apenas 2 dos 11 arquivos
FORMAL de NS importam `Mathlib.Analysis.Distribution.TestFunction`
(`PVDistributionOnCompactK.lean:78`,
`PVFunctionalOnArbitraryCompactK.lean:103`), e que todo hit de
`𝓓^{n}|TestFunction\.` nesses dois arquivos vive dentro de blocos de
comentário de prosa descrevendo o que NÃO está feito ainda
(`PVFunctionalOnArbitraryCompactK.lean:1153-1157`) — zero uso a nível
de termo do tipo empacotado `TestFunction`, `mkCLM`, ou `limitCLM` em
todo o corpus FORMAL de NS. `GAP_REGISTER.yaml` de `02_NAVIER_STOKES`
confirmado contendo apenas `NS-GAP-001..005`, nenhum correspondendo ao
"gap(iii)" informal citado na prosa NS-4A/5A/6A. Isso é contexto
correto para justificar por que NS contribui só um item de execução
nesta onda, não é ele mesmo um alvo.

**NS-7A — NEEDS_NARROWING.** Releitura integral de
`PVCrossCompactMonotonicityAutoRadius.lean` (NS-6A, Onda 6, 229 linhas)
e das seções 9-10 de `PVFunctionalOnArbitraryCompactK.lean` (NS-4A,
linhas 1040-1200) confirma todas as citações Mathlib e de arquivo do
laboratório citadas — nada fabricado. Mas a alegação central de
racional do candidato ("depende SÓ de f, não do... raio R") é
diretamente contradita pelo próprio teorema citado:
`pvKCLM_comp_monoCLM_eq_integral`'s RHS é uma integral sobre
`closedBall 0 R \ {0}`, i.e. depende explicitamente de R. Como
`autoEnvelopeRadius K1` e `autoEnvelopeRadius K2` são saídas
independentes de `Classical.choose` para compactos diferentes e
genericamente DIFEREM, o "rw de 2 linhas" proposto não fecha o
objetivo — deixa duas integrais sobre domínios diferentes, exigindo
exatamente a maquinaria não-trivial de wlog/case-split/`hsupp`-a-partir-
de-`zero_on_compl` da seção 10 de NS-4A (adaptada para dois K's
diferentes, estritamente mais difícil que o caso de único K' da seção
10). Medição independente por contagem direta de linhas: a Parte 10
sozinha (o caso mais fácil, de único K'-fixo, deste mesmo problema)
tem **43 linhas não-comentário** — já acima do teto de 40 linhas
proposto pelo candidato original, para um sub-problema estritamente
mais simples que o alvo de dois compactos diferentes de NS-7A. O
enunciado-alvo continua plausível e provavelmente verdadeiro, e o
`falsifiable_test` do próprio candidato já antecipa a reescrita ingênua
falhando e pede para reportar uma obstrução em vez de forçar (bom
desenho), mas o teto numérico anexado não corresponde ao tamanho de
conteúdo esperado e precisa de revisão para evitar um drift estilo
BSD-7.
**Teste revisado:** mesmo teorema-alvo, mas: (1) teto hard elevado para
**90 linhas novas não-comentário totais** (~2x a soma Parte9+Parte10 de
55 linhas, cobrindo o overhead de contabilidade dos dois compactos),
como número específico e checável, não "pequeno"; (2) protocolo de duas
fases explícito no cabeçalho do arquivo antes de escrever qualquer
prova: primeiro tentar o `rw [eq_integral, eq_integral, hfun]` literal e
ESPERAR que deixe um objetivo residual `∫_{ball R1} = ∫_{ball R2}` (este
é o resultado previsto, não excepcional); segundo, fechar esse residual
adaptando o método wlog/`hsupp` da Parte 10 (escolhendo o fato de
contenção de `K1` ou `K2` conforme qual `autoEnvelopeRadius Ki` é o
mínimo) estritamente dentro do teto de 90 linhas; (3) se o teto de 90
linhas for atingido sem o objetivo fechar, PARAR e autorreportar "fora
de escopo de onda" em vez de acrescentar mais lemas auxiliares ad hoc —
o implementador deve de fato contar linhas não-comentário contra este
número antes de declarar `CLOSED`, não apenas afirmar boa-fé.

---

## 3. Yang-Mills (YM) — Clay oficial (modelo de brinquedo de rede-transferência 2x2)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| YM-CAPSTONE-DET-M1-EXACT | `det(toEuclideanCLM M1) = 3.2` exato | SURVIVES | baixo |
| YM-CAPSTONE-LAMBDAMAX-M1-QUADRATIC-EXACT | forma fechada exata de `lambdaMax`/`lambda2` via fórmula quadrática de SHARED-6A (gated no item anterior) | NEEDS_NARROWING | baixo-moderado |
| YM-CAPSTONE-EIGVAL-DICHOTOMY-TIGHTENED (achado pela adversarial, não estava no recon) | dicotomia de autovalor com o bracket `[1.0,1.2]` de `lambda2` (já fechado na Onda 6) | SURVIVES | baixo |

**Passo original vs. o que mudou.** Continuação direta de
`YMCapstoneDetBracketTightened.lean` e `YMCapstoneTraceM1Exact.lean`
(Onda 6), que já fixam `trace(M1)=4.1` exato e o bracket estreitado
`lambda2 ∈ [1.0,1.2]`, e do `SHARED-6A` (`QuadraticFormulaDim2.lean`,
Onda 6), que já dá a fórmula quadrática genérica em dimensão 2. Os dois
candidatos do recon exploram esse chão diretamente. O terceiro item foi
encontrado só pela adversarial (ver abaixo).

**YM-CAPSTONE-DET-M1-EXACT — SURVIVES.** Todas as quatro citações
Mathlib conferidas por leitura direta: `coe_toEuclideanCLM_eq_
toEuclideanLin` (`Matrix.lean:109-111`), `toEuclideanLin_eq_toLin_
orthonormal` (`PiL2.lean:1276-1278`, confirmado NÃO depreciado,
diferente da vizinha `toEuclideanLin_eq_toLin` da linha 1270, que é),
`Matrix.det_toLin` (`Determinant.lean:223-225`, mesma base dos dois
lados, exatamente o que a instanciação de matriz quadrada precisa), e
`Matrix.det_fin_two` (`Determinant/Basic.lean:807`). `.det` sobre um
termo `E →ₗ[R] E` já é o idioma estabelecido usado no próprio arquivo
alvo (`lambdaMax_mul_lambda2_eq_det`), sem risco de API nova. Grep
próprio confirma `'3.2'` só nas duas linhas de comentário de prosa
(`YMCapstoneDetBracketTightened.lean:183`,
`YMCapstoneDetBracket.lean:186`), `det_M1` como identificador não
aparece em lugar nenhum — o gap é real. Verificação aritmética à mão:
`2*2.1 - 1*1 = 3.2`, correto. Teto de 20 linhas não-comentário é hard e
específico. Risco baixo, plausibilidade alta.
**Teste:** provar `det_toEuclideanCLM_M1_eq_three_point_two : det
(toEuclideanCLM M1 : E →ₗ[R] E) = 3.2` via `coe_toEuclideanCLM_eq_
toEuclideanLin` → `toEuclideanLin_eq_toLin_orthonormal` → `Matrix.
det_toLin` → `Matrix.det_fin_two` + `norm_num`. Teto: **20 linhas
novas não-comentário**. `#print axioms` limpo.

**YM-CAPSTONE-LAMBDAMAX-M1-QUADRATIC-EXACT — NEEDS_NARROWING.**
Matemática e suporte Mathlib conferem: `lambda2_le_lambdaMax`
(`QuadraticFormulaDim2.lean:258-266`), `discriminant_eq` (:276-284), e
`lambdaMax_eq_quadratic_formula` (:297-312) todos confirmados com as
hipóteses e provas alegadas. `toEuclideanCLM_M1_isSymmetric`/
`finrank_E_eq_two` confirmados em
`YMCapstoneDetBracketTightened.lean:457-463`. `Real.sqrt_sq`
confirmado em `Analysis/Real/Sqrt.lean:181`. Discriminante verificado à
mão: `4.1^2 - 4*3.2 = 4.01`, e `401` não é quadrado perfeito
(`400 < 401 < 441`), então `Real.sqrt 4.01` é genuinamente irracional —
a ressalva do próprio candidato ("forma fechada, não decimal") está
correta e sinalizada, não escondida. PORÉM: o teto de tamanho declarado
é internamente contraditório — diz que o orçamento é "40 linhas novas
além do boilerplate reproduzido byte-a-byte", mas justifica o número
ser maior que o teto de 20 do item 1 dizendo "também reproduz os três
teoremas de SHARED-6A" — sob a convenção já estabelecida pelo próprio
laboratório (usada em todo arquivo de onda anterior, incluindo os dois
que este próprio candidato cita), conteúdo reproduzido verbatim de onda
anterior/infra-compartilhada explicitamente NÃO conta como conteúdo
novo. Usar "tenho que reproduzir mais coisa" como base para ALARGAR em
vez de EXCLUIR o teto é exatamente o tipo de contabilidade frouxa que
deixou o item BSD-7 da Onda 6 rodar 6,4x acima do próprio teto
enquanto ainda acreditava estar dentro do escopo. O conteúdo
genuinamente novo aqui é pequeno: uma aplicação de
`lambdaMax_eq_quadratic_formula` a `toEuclideanCLM M1` com o traço
exato (4.1) e o det exato (3.2, condicionado ao item anterior) mais um
passo de `ring`/`linarith` para `lambda2` — bem abaixo de 20 linhas
pela mesma contabilidade que o item 1 usa.
**Teste revisado:** manter o teste falsificável exatamente como
proposto (`lambdaMax (toEuclideanCLM M1) = (4.1 + Real.sqrt 4.01)/2` e
a igualdade correspondente para `lambda2`), mas substituir o teto por:
(a) tudo reproduzido verbatim de `QuadraticFormulaDim2.lean` e de
arquivos YM anteriores é boilerplate explicitamente excluído da
contagem, exatamente como a própria convenção do item 1 já trata tal
reprodução; (b) o conteúdo genuinamente novo — o(s) teorema(s) que
aplicam a fórmula quadrática a M1 e derivam a forma fechada de
`lambda2` — tem teto hard de **15 linhas novas não-comentário**; (c) o
implementador deve declarar a contagem REAL medida de linhas novas no
cabeçalho do arquivo (não apenas afirmar que o teto foi cumprido) e
autorreportar fora de escopo se exceder 15 linhas, mesmo tratamento se
precisar de cola extra para unificar os namespaces `E`/`lambdaMax`/
`lambda2` dos dois arquivos. **Gated no item anterior** (só tentar após
`det_toEuclideanCLM_M1_eq_three_point_two` de fato compilar).

**YM-CAPSTONE-EIGVAL-DICHOTOMY-TIGHTENED — SURVIVES (achado pela
adversarial, ausente do recon original).** A alegação do recon de que
"nenhum terceiro candidato é proposto... genuinamente saturado" não se
sustenta sob releitura independente. `YMCapstoneEigvalDichotomy.lean`
(Onda 5, lido integralmente) prova
`eigenvalue_dichotomy_toEuclideanCLM_M1 : (2.9 ≤ mu ∧ mu ≤ 3.1) ∨ (0.7
≤ mu ∧ mu ≤ 1.3)` (linhas 584-596) usando o bracket ANTIGO,
Lipschitz-derivado, `[0.7,1.3]` (`lambda2_M1_bracket_from_compose`) —
nunca atualizado para o bracket estreitado `[1.0,1.2]` da Onda 6 que
`YMCapstoneDetBracketTightened.lean` já usou para o cálculo do bracket
de det. Grep no diretório YM inteiro e no arquivo por `'Dichotomy'` +
`'Tightened'` ou por qualquer dicotomia usando `1.0`/`1.2` — nenhum
arquivo existe. Este é um terceiro candidato legítimo, pequeno,
mecanicamente idêntico em forma ao próprio item 1 do recon (uma
substituição de bracket, não matemática nova), e deve ser adicionado à
onda.
**Teste:** gated no `lambda2_toEuclideanCLM_M1_bracket` de
`YMCapstoneTraceM1Exact.lean` (`[1.0,1.2]`, já verificado na Onda 6 —
mesma dependência de gate que os itens 4/5 da Onda 6 já usam). Provar
`eigenvalue_dichotomy_toEuclideanCLM_M1_tightened : (2.9 ≤ mu ∧ mu ≤
3.1) ∨ (1.0 ≤ mu ∧ mu ≤ 1.2)` para todo autovalor `mu` de
`toEuclideanCLM M1`, pelo mesmo padrão `rcases
eigenvalue_eq_lambdaMax_or_lambda2 ... with h | h; left; rw[h]; exact
lambdaMax_M1_bracket; right; rw[h]; obtain hlo,hhi :=
lambda2_toEuclideanCLM_M1_bracket; constructor <;> linarith` já usado
no arquivo não-estreitado. Teto: **15 linhas novas não-comentário**
além do boilerplate reproduzido byte-a-byte (o único teorema mais sua
prova) — autorreportar fora de escopo se excedido. Não gated nos outros
dois itens desta seção (usa só o bracket já fechado na Onda 6).

---

## 4. Hodge Conjecture (HG) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| HG-4h | classe de `expConjUnit` no quociente `≠` identidade | SURVIVES | baixo |
| HG-1i | lei de potência para `principalCycle_a0` | NEEDS_NARROWING | baixo-moderado |

**Passo original vs. o que mudou.** `HG-4h` continua diretamente de
`HG1HPrincipalCycleA0MulProbe.lean` e
`HG4GHolomorphicTransitionQuotientNontrivialProbe.lean` (Onda 6).
`HG-1i` estende `principalCycle_a0_mul` (Onda 6) para uma lei de
potência por indução.

**HG-4h — SURVIVES.** Releitura integral dos dois arquivos Wave-6
citados (383 e 327 linhas) confirma que o resumo repassado bate com o
que os arquivos realmente provam — nenhum overclaim detectado. Todas as
quatro citações Mathlib reconferidas: `QuotientGroup.eq_one_iff`
(`GroupTheory/QuotientGroup/Defs.lean:120`, `(x:G) = 1 ↔ x ∈ N`);
`Subgroup.normal_of_isMulCommutative`
(`Algebra/Group/Subgroup/Defs.lean:631`); `CommMagma.to_
isCommutative` (`Algebra/Group/Defs.lean:263`) — cadeia de typeclass
completa rastreada à mão: `CommGroup → CommMonoid → CommSemigroup →
CommMagma → CommMagma.to_isCommutative` resolve via projeção-de-pai
comum mesmo com o comentário em `Defs.lean:1300` avisando que não há
atalho DIRETO de `CommGroup` para `IsMulCommutative` — a cadeia
indireta continua válida; `instCommGroupUnits`
(`Algebra/Group/Units/Defs.lean:265-267`, já load-bearing na prova
já-`CLOSED` de HG-4g). `expConjUnit_not_mem` relocalizado em
linhas 274-278 do arquivo Wave-6 exatamente como citado. Teto hard de
40 linhas não-comentário é número específico e checável. Uma ressalva
menor, não fatal: `rw [Ne, QuotientGroup.eq_one_iff]` pode precisar de
`rw [ne_eq, ...]` ou de reescrita como implicação direta, já que `Ne`
é `def`, não lema-de-igualdade utilizável por `rw` diretamente — ajuste
trivial de script, bem dentro da margem de 40 linhas.
**Teste revisado:** `theorem expConjUnit_coset_ne_one : (expConjUnit :
(C → C)ˣ ⧸ HolomorphicTransitionSubgroup) ≠ 1 := fun h =>
expConjUnit_not_mem ((QuotientGroup.eq_one_iff _).mp h)`, evitando a
ressalva de desdobramento de `Ne`. Teto: **40 linhas novas
não-comentário**. `#print axioms` limpo.

**HG-1i — NEEDS_NARROWING.** Releitura integral confirma
`principalCycle_a0_mul` (Onda 6) como lei de soma de dois fatores
genuína — a base para indução é real. `pow_ne_zero`
(`Algebra/GroupWithZero/Basic.lean:258`) e `pow_succ'`
(`Algebra/Group/Defs.lean:702`, forma `a * a^n`) reconfirmados exatos.
PORÉM: o candidato afirma que `succ_nsmul`/`one_nsmul` são "duais
`to_additive`-gerados de `pow_succ`/`pow_one`" (verdade literal:
`pow_succ` na linha 695 gera `succ_nsmul` por `to_additive`) — mas o
`falsifiable_test` então empalma `succ_nsmul` numa indução construída
sobre `pow_succ'` (a OUTRA forma, de multiplicação à esquerda, `a^(n+1)
= a * a^n`). Esses não são o mesmo par: o dual verdadeiro de `pow_succ'`
é `succ_nsmul'` (append à esquerda, `(n+1)•a = a + n•a`), confirmado
por grep direto — `succ_nsmul'` é nome Mathlib real, ativamente usado
(7+ call sites), e `Mathlib/Algebra/GradedMonoid.lean:566` contém o
emparelhamento análogo exato `rw [pow_succ', succ_nsmul']` para
essencialmente este mesmo padrão de indução, confirmando que
`succ_nsmul'` (não `succ_nsmul`) é o par correto de `pow_succ'`. A
receita de prova como escrita, portanto, não type-checkaria/fecharia
conforme roteirizada. Corrigível de duas formas (trocar para
`succ_nsmul'`, ou trocar `pow_succ'` pelo `pow_succ` sem-linha via a
estrutura `AddCommGroup` de `AlgebraicCycle` — confirmada presente via
`Topology/LocallyFinsupp.lean:396` — para fazer ponte com `add_comm`
entre qualquer par de convenção) — mas a confiança do candidato na
receita exata estava superestimada.
**Teste revisado:** mesmo teorema-alvo e mesmo teto de 80 linhas, mas
corrigir a receita de prova: `induction n with | zero => simpa using
(one_nsmul _).symm ▸ ... | succ n ih => rw [pow_succ',
principalCycle_a0_mul a0 (a0^(n+1)) ha0 (pow_ne_zero (n+1) ha0), ih, ←
succ_nsmul']` — i.e. emparelhar `pow_succ'` com `succ_nsmul'` (não
`succ_nsmul`), conforme o precedente exato em
`Mathlib/Algebra/GradedMonoid.lean:566`. O implementador deve verificar
que esta cadeia `rw` exata compila (ou recorrer ao bridging via
`add_comm` com o par não-primado `pow_succ`/`succ_nsmul`) antes de
declarar sucesso. Teto: **80 linhas novas não-comentário**
(inalterado). `#print axioms` limpo.

---

## 5. Birch and Swinnerton-Dyer (BSD) — Clay oficial

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| BSD-8 | identidades de coeficiente do fator de Euler local para os três ramos de não-boa-redução de `WeierstrassCurve.localPolynomial` | SURVIVES | moderado |

**Contexto factual e endereçamento explícito de DEC-103.** Este é
literalmente o próximo item da MESMA veia (`localPolynomial`/
`localPowerSeries`/`localEulerFactor`) que produziu `BSD-7` na Onda 6 e
estourou seu próprio teto em ~6,4x (148 linhas medidas vs. 23 de
referência). Por isso o teto e a instrução de medir-antes-de-declarar-
`CLOSED` deste item são tratados como carga estrutural, não decoração —
o candidato já vem desenhado com essa disciplina embutida, e esta
revisão a reforça explicitamente abaixo.

**BSD-8 — SURVIVES.** Releitura integral de
`BSD7CoeffCSeqBridge.lean` (351 linhas, Onda 6), de
`Mathlib/AlgebraicGeometry/EllipticCurve/LFunction.lean` na íntegra, e
das seções relevantes de `Reduction.lean` confirma: o if/else de 4
ramos de `LFunction.lean` (linhas 43-50, docstring 38-42); `WellKnown.
lean:77` `mk_one_mul_one_sub_eq_one` (só precisa `CommRing S`);
`Basic.lean`'s `rescale` (543), `coeff_rescale` (567), `rescale_mk`
(585), `rescale_neg_one_X` (706); `Inverse.lean`'s `constantCoeff_
invOfUnit` (97) e `mul_invOfUnit` (102) — mesma API que `BSD-7` já usou
com sucesso. As quatro classes de redução (`HasGoodReduction` 281,
`HasMultiplicativeReduction` 303, `HasSplitMultiplicativeReduction`
322-326, trilogia 330-334) confirmadas, mais — além do que o candidato
citou — os lemas de exclusão cruzada exatos que os três alvos vão
precisar: `HasMultiplicativeReduction.not_hasGoodReduction` (344-346),
`HasAdditiveReduction.not_hasGoodReduction` (348-350), e
`HasAdditiveReduction.not_hasMultiplicativeReduction` (356-358), todos
presentes — tornando cada uma das três cadeias de desdobramento
`if_pos`/`if_neg` mecanicamente disponível sem lema faltante. Grep
próprio no Mathlib inteiro confirma zero uso downstream de
`localPolynomial`/`localPowerSeries`/`localEulerFactor` fora do
arquivo que os define, e zero ocorrência dos três nomes de tipo de
redução em `06_BSD/FORMAL` — ambas as alegações de ausência se
sustentam. Álgebra da derivação não-split-multiplicativa rederivada à
mão: `rescale(-1)` aplicado a `mk_one_mul_one_sub_eq_one` de fato
produz a identidade `(-1)^n` alternante para `1+X`, matematicamente
correta. A seção "ainda faltando se sucesso" corretamente descarta
`BSD-GAP-008`, conteúdo de cota de Hasse, somabilidade, e o teorema de
colagem de 4 ramos — sem overclaim de novidade. O teto (**90 linhas
novas não-comentário totais**, medido pelo mesmo método sed/grep que
pegou o estouro de BSD-7) é hard e específico, com instrução explícita
de MEDIR — não estimar — antes de declarar `CLOSED`.
**Teste revisado (mecânico, com checkpoint por ramo):** (1)
split-multiplicativa: `PowerSeries.coeff n (W.localPowerSeries R) = 1`,
via `if_pos` (usando `HasMultiplicativeReduction.not_
hasGoodReduction`) desdobrando para `invOfUnit (1-X) 1` igualado a
`PowerSeries.mk 1` via `mk_one_mul_one_sub_eq_one` mais um argumento de
unicidade de inverso de 3-4 linhas; (2) não-split-multiplicativa:
`coeff n = (-1)^n`, mesmo desdobramento igualando `invOfUnit (1+X) 1` a
`rescale (-1) (mk 1)` via `rescale_neg_one_X` empurrado por
`mk_one_mul_one_sub_eq_one`; (3) aditiva: `W.localPowerSeries R = 1`
(`invOfUnit 1 1 = 1`), usando `HasAdditiveReduction.not_
hasGoodReduction` e `HasAdditiveReduction.not_hasMultiplicativeReduction`
para eliminar os três primeiros ramos do if. O implementador deve
rodar a contagem exata de linhas (mesmo comando sed/grep que pegou o
estouro de BSD-7) **após cada um dos três lemas**, não só ao final, e
autorreportar "fora de escopo de onda" imediatamente se o total
corrente ultrapassar 90 em vez de prosseguir para o próximo ramo
primeiro. Teto: **90 linhas novas não-comentário totais**. `#print
axioms` limpo em todos os três.

---

## 6. Síntese TOE (extensão interna do laboratório — NÃO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| TOE-7 | `F.obj` é `Bijective` (`KCat → ShiftCat`) | SURVIVES | baixo |

**Passo original vs. o que mudou.** Continuação de `TOE-6a`/`TOE-6b`
(Onda 6) e de `TOE-4` (Onda 4, `KToShiftFunctorNotFaithfulNoReverse.
lean`). `TOE-7` tenta a alegação de bijetividade completa de `F.obj`.

**TOE-7 — SURVIVES.** `NoSurjectiveReverseFunctorShiftCatKCat.lean`
(TOE-6a) confirma `e : ShiftCat ≃ KCat := (ActionCategory.objEquiv
Shift3 Regime3).symm.trans (ActionCategory.objEquiv K Regime3)`
exatamente nas linhas 112-114. `KToShiftFunctorNotFaithfulNoReverse.
lean` (TOE-4) confirma `F.obj p := show ShiftCat from p.back` nas
linhas 189-193. Citações Mathlib conferidas por leitura direta contra o
checkout vendorizado: `Equiv.bijective` (`Logic/Equiv/Defs.lean:184`),
`Equiv.symm` (:147), `Equiv.trans` (:163-164), `ActionCategory.objEquiv`
(`CategoryTheory/Action.lean:86-90`) — todas exatas, incluindo os
números de linha citados. `symm_symm_apply`/`symm_trans_apply`
(Defs.lean:280/274) também confirmados, sustentando o fallback do
próprio candidato ("ou um simp de uma linha"). A defeq alegada foi
rastreada à mão passo a passo (desdobrando `ActionCategory M X` como
`.Elements` de um functor-de-ação, e `objEquiv`'s `toFun`/`invFun`
como literalmente o wrap-CoeTC e a projeção `.back`) e é matematicamente
real, não hand-waved. Grep no diretório TOE inteiro (13 arquivos)
confirma nenhuma alegação prévia de `Function.Bijective F.obj`
existente, e `THEORY_RECOVERY_MATRIX.md` confirma as três linhas (QM,
GR, Yang-Mills) ainda `UNRESOLVED` — a seção "ainda faltando" é precisa
e não-overclaiming (bookkeeping interno do laboratório, não passo rumo
a nenhum Problema do Milênio). Teto de 35 linhas é hard, específico, e
fundamentado num precedente medido (`TOE-6b` recontado em ~20 linhas,
Onda 6). Uma ressalva genuína, não uma refutação: a alegação de que
`F.obj` é "literalmente a coerção de um `Equiv`" é verdadeira mas quase
tautológica — `KCat` e `ShiftCat` são ambos wrappers-em-disfarce
bijetivos sobre o mesmo `Regime3` — conteúdo científico mais baixo até
que `TOE-6a`/`TOE-6b`, mas consistente com o padrão já estabelecido da
linha (`FOUNDATIONAL_FORMALIZATION_ONLY`), não uma degradação.
**Teste:** provar `F_obj_bijective : Function.Bijective (F.obj :
KCat → ShiftCat)` mostrando `F.obj = ⇑e.symm` (via `funext fun c => by
simp [e, ActionCategory.objEquiv]`, ou uma cadeia explícita
`Equiv.symm_trans_apply` + `Equiv.symm_symm` se `simp` não fechar de
primeira) e então `Equiv.bijective e.symm`. Teto: **35 linhas novas
não-comentário**. `#print axioms` limpo.

---

## 7. Fundamentos Quânticos / Unificação (extensão interna — NÃO Clay-oficial)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| QF-12 | empacotamento `ContinuousMonoidHom` completo do fluxo de Heisenberg | SURVIVES | moderado (bem de-riscado) |
| QF-13 | representar o fluxo via `Matrix.toEuclideanCLM` para `unitary(EuclideanSpace CLM)` | NEEDS_NARROWING | baixo-moderado |

**Passo original vs. o que mudou.** `QF-12` continua de
`HeisenbergFlowMonoidHom.lean` (QF-10, Onda 6) e
`HeisenbergFlowContinuitySmulProbe.lean` (QF-11, Onda 6), fechando o
gap de continuidade que QF-10 tinha explicitamente deixado para QF-11.
`QF-13` tenta uma representação alternativa via matrizes euclidianas.

**QF-12 — SURVIVES.** Releitura integral dos dois arquivos Onda-6
citados (305/265 linhas, 54/27 não-comentário, ambos reconferidos por
script de remoção de comentário próprio, batendo exato com o
dimensionamento do recon). `heisenbergFlowHom` (QF-10, linhas 275-285)
confirmado como `MonoidHom.mk'` real; sua própria seção de honestidade
(item a, linhas 163-167) nomeia explicitamente `ContinuousMonoidHom`/
continuidade como o único item NÃO tentado, deferido a QF-11.
`continuous_exp_smul_heisenbergGenerator` (QF-11, linhas 254-258) prova
exatamente a continuidade ambiente necessária, sob o mesmo escopo
`Matrix.Norms.L2Operator` que QF-10 usa (sem descompasso de escopo).
Toda citação Mathlib reconferida contra o snapshot vendorizado:
`structure ContinuousMonoidHom extends A →* B, C(A,B)`
(`ContinuousMonoidHom.lean:57`, só precisa `[Monoid A][Monoid B]
[TopologicalSpace A][TopologicalSpace B]`); `TopologicalSpace
(Multiplicative X)` + `continuous_toAdd`/`continuous_ofAdd`
(`Constructions.lean:86/109/111`); `instTopologicalSpaceSubtype`
(`Defs/Induced.lean:76-77`); `Continuous.subtype_mk`
(`Constructions.lean:413`, forma exata coincide termo-a-termo com o
`toFun` de `heisenbergFlowHom`); `unitary.instGroup`
(`Unitary.lean:96`); padrão de empacotamento idiomático
(`toContinuousMonoidHom`, linha 113/114). Nenhuma citação fabricada
encontrada — candidato bem de-riscado. Teto de 100 linhas
não-comentário é hard, específico, checável (mesmo método de medição
que dimensionou QF-10 em 54 e QF-11 em 27, ambos reproduzidos
independentemente), e com folga razoável (~2x) sobre QF-10 sozinho para
cobrir a re-derivação de continuidade mais o passo de empacotamento —
não um teto vago tipo "pequeno". Seção "ainda faltando" corretamente
não alega nada sobre teorema de Stone, geradores ilimitados, dimensões
infinitas, Ehrenfest/`hbar→0`, ou relevância Clay-Millennium. Risco
residual não totalmente de-riscável de fora da compilação real: se a
sintaxe de extensão de construtor anônimo (`{ heisenbergFlowHom with
continuous_toFun := ... }`) resolve limpo contra a estrutura exata de
campos de `ContinuousMonoidHom` — mas o candidato já embute um fallback
explícito de BLOCKED-e-parar para essa classe de risco, resposta
correta a uma incerteza irredutível que só a compilação resolve.
**Teste:** construir `heisenbergFlowContinuousHom : ContinuousMonoidHom
(Multiplicative R) (unitary (Matrix (Fin 2)(Fin 2) C))` via
`{ heisenbergFlowHom with continuous_toFun := continuous_exp_smul_
heisenbergGenerator (adaptada) }` (ou equivalente com massagem explícita
de campo se a sintaxe de extensão anônima não resolver). Reportar a
contagem real de linhas não-comentário atingida contra o teto no
relatório de fechamento. Teto: **100 linhas novas não-comentário**.
`#print axioms` limpo.

**QF-13 — NEEDS_NARROWING.** `unitary.map_mem`
(`Unitary.lean:300`) e `Matrix.toEuclideanCLM : Matrix n n K ≃⋆ₐ[K]
(EuclideanSpace K n →L[K] EuclideanSpace K n)` (`Matrix.lean:102`)
reconfirmados exatos. PORÉM a citação central de suporte do candidato
está errada: alega "a classe existe (`StarAlgEquivClass`,
`StarAlgHom.lean:666`)" — a linha 666 é `namespace StarAlgEquivClass`,
NÃO uma declaração `class`; esse namespace só contém um helper de
coerção (`toStarAlgEquiv`), não uma cadeia de instância de typeclass
por si só — citação de fato errada (um namespace rotulado como
classe). Rastreando a cadeia REAL à mão: `StarAlgEquiv` ganha
`EquivLike`, `NonUnitalAlgEquivClass` (linha 704), e
`StarRingEquivClass` (linha 709) como instâncias diretas; `StarRing
EquivClass` produz `StarHomClass` (via instância de prioridade 50 em
`StarRingHom.lean`); `NonUnitalAlgEquivClass` estende `RingEquivClass`,
que produz `RingHomClass` (`Ring/Equiv.lean:101-102`), que estende
`MonoidHomClass` (`Ring/Hom/Defs.lean:326-328`). Então os requisitos
`[StarHomClass F R S][MonoidHomClass F R S]` de `unitary.map_mem`
sintetizam DE FATO para o tipo de `toEuclideanCLM` — a alegação de
viabilidade subjacente é correta, e até mais sólida do que o próprio
candidato acreditava (autoavaliado "menos de-riscado" — a cadeia real
fecha, só não pelo nome citado). Mas o termo de prova proposto no
`falsifiable_test`, `unitary.map toEuclideanCLM.toStarMonoidHom ∘
heisenbergFlowHom`, muito provavelmente está quebrado como escrito:
`.toStarMonoidHom` (`MonoidHom.lean:318`) é definido para `A ≃⋆* B`
(`StarMulEquiv`, star + multiplicativo, sem estrutura de linearidade
escalar), não para `A ≃⋆ₐ[K] B` (`StarAlgEquiv`, o que `toEuclideanCLM`
realmente é) — nenhuma projeção `.toStarMonoidHom` direta entre esses
tipos empacotados diferentes foi encontrada. A rota mais simples e
robusta — aplicar `unitary.map_mem` diretamente e pontualmente
(espelhando exatamente como QF-10 construiu `heisenbergFlowHom` via
`MonoidHom.mk'` com prova de pertencimento fornecida pontualmente) em
vez de tentar compor dois homs já empacotados via `unitary.map` —
evita esse problema por completo.
**Teste revisado:** substituir o termo proposto por uma construção
pontual direta espelhando o próprio padrão `MonoidHom.mk'` de QF-10:
`heisenbergFlowEuclideanHom := MonoidHom.mk' (fun t => ⟨toEuclideanCLM
(heisenbergFlowHom t : Matrix (Fin 2)(Fin 2) C), unitary.map_mem
toEuclideanCLM (heisenbergFlowHom t).2⟩) (by ...)`, ou equivalentemente
aplicar `unitary.map_mem` uma vez por valor do fluxo usando o fato
pontual já existente `exp_heisenbergFlow_mem_unitary` (QF-7/QF-10)
diretamente (não via composição empacotada `→⋆*` de `unitary.map`, que
exige um tipo que o `toEuclideanCLM` de QF-8 não tem). Corrigir a
citação de "classe `StarAlgEquivClass` existe em
`StarAlgHom.lean:666`" para a cadeia real de instância:
`NonUnitalAlgEquivClass (A ≃⋆ₐ[R] B) R A B` (`StarAlgHom.lean:704`) e
`StarRingEquivClass (A ≃⋆ₐ[R] B) A B` (`StarAlgHom.lean:709`). Reportar
BLOCKED imediatamente se a rota pontual também falhar em type-checkar,
em vez de tentar construções de composição empacotada alternativas.
Teto: **60 linhas novas não-comentário** (mantido, já específico e
checável) — reportar a contagem real no fechamento.

---

## Infraestrutura compartilhada entre frentes (continuação)

| # | Candidato | Veredito | Custo~ |
|---|---|---|---|
| SHARED-7A | corolário explícito de fórmula quadrática para `lambda2` (ramo negativo) | SURVIVES | baixo |

**Passo original vs. o que mudou.** Continuação direta de
`QuadraticFormulaDim2.lean` (SHARED-6A, Onda 6), que já dá o ramo
positivo (`lambdaMax`) da fórmula quadrática em dimensão 2. SHARED-7A
propõe o corolário de sinal trocado para `lambda2`.

**SHARED-7A — SURVIVES.** Releitura integral dos 328 linhas de
`QuadraticFormulaDim2.lean` confirma: `lambda2 T` definido nas linhas
184-186 exatamente como `trace T - lambdaMax T`;
`lambdaMax_eq_quadratic_formula` (297-312) prova o ramo positivo para
`T` simétrico no `E` fixo `EuclideanSpace(R,Fin 2)`; a derivação
`lambda2 T = trace T - lambdaMax T = trace T - (trace T + sqrt(disc))/2
= (trace T - sqrt(disc))/2` é álgebra correta e fecha por
`unfold`+`rw`+`ring`, já que `sqrt(disc)` é subtermo atômico idêntico
em ambos os lados. `Real.sqrt_sq` reconfirmado em
`Analysis/Real/Sqrt.lean:181` (dependência já usada, não nova). Grep em
toda a árvore `_SHARED_INFRA` e Millennium confirma ausência prévia de
qualquer alegação do ramo negativo de `lambda2` — sem colisão de nome.
Teto de 20 linhas novas (excluindo o bloco de dependência reproduzido
verbatim) é realista — o teorema novo em si tem ~6-8 linhas — e a
convenção de exclusão bate com o que Ondas 4-6 já estabeleceram para
seus próprios blocos reproduzidos. A própria admissão do candidato de
que o conteúdo matemático marginal é "perto de zero" é honesta e
precisa (é um corolário de sinal trocado de um fato já provado), e
"ainda faltando se sucesso" corretamente não alega nada sobre nenhum
Problema do Milênio, com `dim(E)=2` permanecendo fixo. Uma cautela de
implementação: como o teto exclui explicitamente o bloco reproduzido, o
implementador deve reproduzir só o que `lambdaMax_eq_quadratic_formula`
estritamente exige (espelhando a própria cadeia de dependência de
SHARED-6A), não usar o bloco reproduzido como forma de lavar escopo.
**Teste:** sem estreitamento necessário; teto hard já específico e
checável. Provar `lambda2_eq_quadratic_formula` a partir de
`lambdaMax_eq_quadratic_formula` + `unfold lambda2` + `ring`. Teto:
**20 linhas novas não-comentário além do bloco reproduzido verbatim**
— reportar via contagem linha-a-linha contra o bloco reproduzido de
SHARED-6A para tornar a exclusão auditável, não apenas autoafirmada.
`#print axioms` limpo.

---

## Lista de execução Onda 7 (despacho direto para agente de formalização)

Cada item abaixo traz o candidato, o teorema-alvo, e o enunciado de
teste exato (já revisado pela adversarial), pronto para um agente de
formalização executar sem reinterpretação. Ordem: por linha, mesma
sequência das seções acima. Todos são independentes entre si, exceto
onde anotado (item 5 depende do item 4; item 6 é independente de ambos
— usa só o bracket já fechado na Onda 6). A linha PN não participa
(retirada por DEC-100 — ver Enquadramento honesto, não reavaliada nesta
onda).

```text
 1. RH / RH-7C (Tp <= Tp.adjoint via densidade + le_adjoint)
    Reproduzir o bloco minimo finiteSupport/TpFun/Tp; provar
    densidade de finiteSupport em H2 (via lp.single, trivial); fechar
    Tp <= Tp.adjoint via LinearPMap.IsFormalAdjoint.le_adjoint aplicado
    a Tp_isFormalAdjoint (RH-7B, Onda 6) mais a densidade. NAO tentar
    IsSelfAdjoint. Teto: 50 linhas novas nao-comentario. #print axioms
    limpo.

 2. RH / RH-7D (forma quadratica <Tp x,x> real e >=0)
    Reproduzir o bloco minimo finiteSupport/TpFun/Tp; provar
    Tp_inner_self_real_nonneg: forall x em Tp.domain, (inner (Tp x) x
    : C).im = 0 e 0 <= (inner (Tp x) x : C).re, via RCLike.inner_apply'
    + lp.hasSum_inner + funext + Complex.conj_natCast reduzindo a
    Sum i*normSq(x_i), fechado por Complex.normSq_nonneg. Teto: 60
    linhas novas nao-comentario. #print axioms limpo.

 3. NS / NS-7A (independencia de compacto/raio do funcional p.v.
    composto, ESTREITADO)
    Protocolo de duas fases OBRIGATORIO: (a) tentar rw [eq_integral,
    eq_integral, hfun] e esperar objetivo residual integral sobre
    bolas de raios diferentes (nao um fechamento de 2 linhas); (b)
    fechar o residual adaptando o metodo wlog/hsupp da Parte 10 de
    NS-4A (escolhendo a contencao de K1 ou K2 conforme qual
    autoEnvelopeRadius e o minimo). Se o teto for atingido sem fechar,
    PARAR e reportar fora de escopo. Teto: 90 linhas novas
    nao-comentario, medidas -- nao estimadas -- antes de declarar
    CLOSED.

 4. YM / YM-CAPSTONE-DET-M1-EXACT (det(M1)=3.2 exato)
    Provar det_toEuclideanCLM_M1_eq_three_point_two via
    coe_toEuclideanCLM_eq_toEuclideanLin -> toEuclideanLin_eq_toLin_
    orthonormal -> Matrix.det_toLin -> Matrix.det_fin_two + norm_num.
    Teto: 20 linhas novas nao-comentario. #print axioms limpo.

 5. YM / YM-CAPSTONE-LAMBDAMAX-M1-QUADRATIC-EXACT (gated no item 4)
    So apos o item 4 fechar: aplicar lambdaMax_eq_quadratic_formula
    (SHARED-6A) a toEuclideanCLM M1 usando o traco exato (4.1, Onda 6)
    e o det exato (3.2, item 4); derivar lambda2 por ring/linarith.
    Boilerplate reproduzido de SHARED-6A e de arquivos YM anteriores
    EXCLUIDO da contagem. Teto: 15 linhas novas nao-comentario
    (conteudo genuinamente novo apenas), declaradas no cabecalho do
    arquivo.

 6. YM / YM-CAPSTONE-EIGVAL-DICHOTOMY-TIGHTENED (independente, gated
    so no bracket [1.0,1.2] ja fechado na Onda 6)
    Provar eigenvalue_dichotomy_toEuclideanCLM_M1_tightened: para todo
    autovalor mu de toEuclideanCLM M1, (2.9<=mu<=3.1) ou
    (1.0<=mu<=1.2), pelo padrao rcases
    eigenvalue_eq_lambdaMax_or_lambda2 + lambdaMax_M1_bracket +
    lambda2_toEuclideanCLM_M1_bracket (Onda 6) + linarith. Teto: 15
    linhas novas nao-comentario alem do boilerplate reproduzido.

 7. HG / HG-4h (classe de expConjUnit no quociente != identidade)
    theorem expConjUnit_coset_ne_one : (expConjUnit : (C -> C)ˣ ⧸
    HolomorphicTransitionSubgroup) != 1 := fun h => expConjUnit_not_mem
    ((QuotientGroup.eq_one_iff _).mp h). Teto: 40 linhas novas
    nao-comentario. #print axioms limpo.

 8. HG / HG-1i (lei de potencia para principalCycle_a0, RECEITA
    CORRIGIDA)
    Provar principalCycle_a0 (a0^(n+1)) = (n+1) • principalCycle_a0
    a0, por inducao: caso succ via rw [pow_succ',
    principalCycle_a0_mul a0 (a0^(n+1)) ha0 (pow_ne_zero (n+1) ha0),
    ih, <- succ_nsmul'] -- emparelhar pow_succ' com succ_nsmul' (nao
    succ_nsmul), conforme o precedente em
    Mathlib/Algebra/GradedMonoid.lean:566. Teto: 80 linhas novas
    nao-comentario. #print axioms limpo.

 9. BSD / BSD-8 (identidades de coeficiente do fator de Euler local,
    tres ramos de nao-boa-reducao, escopo bounded -- CONTINUACAO
    DIRETA DA VEIA QUE ESTOUROU EM BSD-7)
    Tres lemas sequenciais, medindo linhas apos CADA um: (1)
    split-multiplicativa: coeff n (localPowerSeries) = 1 via if_pos +
    invOfUnit (1-X) 1 = mk 1 (mk_one_mul_one_sub_eq_one); (2)
    nao-split-multiplicativa: coeff n = (-1)^n via invOfUnit (1+X) 1 =
    rescale (-1) (mk 1) (rescale_neg_one_X); (3) aditiva:
    localPowerSeries = 1 via HasAdditiveReduction.not_hasGoodReduction
    + not_hasMultiplicativeReduction eliminando os 3 primeiros ramos
    do if. Teto: 90 linhas novas nao-comentario TOTAIS, medidas apos
    cada lema (nao so ao final) -- parar e reportar fora de escopo
    imediatamente se o total corrente ultrapassar 90 antes do terceiro
    lema. #print axioms limpo nos tres.

10. TOE / TOE-7 (F.obj e Bijective, KCat -> ShiftCat)
    theorem F_obj_bijective : Function.Bijective (F.obj : KCat ->
    ShiftCat), mostrando F.obj = coe e.symm (funext fun c => by simp
    [e, ActionCategory.objEquiv], ou cadeia explicita Equiv.symm_
    trans_apply + Equiv.symm_symm se simp nao fechar), entao
    Equiv.bijective e.symm. Teto: 35 linhas novas nao-comentario.
    #print axioms limpo.

11. QF / QF-12 (empacotamento ContinuousMonoidHom completo do fluxo
    de Heisenberg)
    Construir heisenbergFlowContinuousHom : ContinuousMonoidHom
    (Multiplicative R) (unitary (Matrix (Fin 2)(Fin 2) C)) via
    { heisenbergFlowHom with continuous_toFun := continuous_exp_smul_
    heisenbergGenerator (adaptada) } (ou massagem explicita de campo
    se a extensao anonima nao resolver). Reportar sob qual escopo
    (Operator ou L2Operator) de fato fechou e a contagem real de
    linhas. Teto: 100 linhas novas nao-comentario. #print axioms
    limpo.

12. QF / QF-13 (representacao via Matrix.toEuclideanCLM, RECEITA
    CORRIGIDA)
    Construir heisenbergFlowEuclideanHom via MonoidHom.mk' (fun t =>
    <toEuclideanCLM (heisenbergFlowHom t), unitary.map_mem
    toEuclideanCLM (heisenbergFlowHom t).2>) (...) -- rota PONTUAL, NAO
    a composicao unitary.map toEuclideanCLM.toStarMonoidHom (essa
    projecao nao existe para StarAlgEquiv). Se a rota pontual tambem
    falhar, reportar BLOCKED imediatamente, sem tentar construcoes de
    composicao empacotada alternativas. Teto: 60 linhas novas
    nao-comentario. #print axioms limpo.

13. SHARED-INFRA / SHARED-7A (corolario de formula quadratica, ramo
    negativo de lambda2)
    Provar lambda2_eq_quadratic_formula a partir de lambdaMax_eq_
    quadratic_formula (SHARED-6A) + unfold lambda2 + ring. Reportar
    contagem linha-a-linha contra o bloco reproduzido de SHARED-6A
    para tornar a exclusao auditavel. Teto: 20 linhas novas
    nao-comentario alem do bloco reproduzido. #print axioms limpo.
```

Total: **13 itens numerados**, correspondendo a **13 candidatos
distintos**. Contando por linha: RH(2) + NS(1) + YM(3) + HG(2) +
BSD(1, com teto reforçado) + TOE(1) + QF(2) + SHARED-INFRA(1) = **13**.
Isso é a MESMA contagem agregada da Onda 6, mas por uma composição
diferente e não-uniforme, o que importa mais que o número bruto: NS
continua em 1 item (como na Onda 6); YM subiu de 2 para 3 porque a
adversarial encontrou um terceiro candidato
(`YM-CAPSTONE-EIGVAL-DICHOTOMY-TIGHTENED`) que o recon original tinha
deixado passar por completo — o mesmo tipo de achado que
`HasseCoefficientRecursionBound.lean` (BSD-3) foi na Onda 6, desta vez
numa linha diferente. Dois itens (`RH-7C`+`RH-7D` gated
implicitamente na mesma máquina base, e `YM-CAPSTONE-LAMBDAMAX-M1-
QUADRATIC-EXACT` explicitamente) têm dependência sequencial dentro da
mesma seção, mesma convenção já usada nas Ondas 5-6. Nenhum item
derivado de candidato `REFUTED` (nenhum foi `REFUTED` nesta rodada —
todos os defeitos encontrados foram de composição, citação, ou
contagem de escopo, corrigíveis sem descartar o alvo subjacente).

---

## Avaliação pessoal — os candidatos com maior chance de virar
resultado formal honesto e não-trivial mais cedo

Não é repetição da autoavaliação dos agentes de recon/adversarial — é
julgamento próprio depois de sintetizar as 13 verificações desta onda.

**1. YM-CAPSTONE-DET-M1-EXACT (item 4).** `norm_num` puro sobre um
decimal (`2.1`) que o MESMO arquivo já resolve com sucesso em três
outras chamadas — precedente direto, sem risco novo. Bracket
resultante conferido à mão contra os autovalores reais. Risco técnico
residual: mínimo.

**2. HG-4h (item 7).** Uma linha genuína depois da correção de receita
(`fun h => expConjUnit_not_mem ((QuotientGroup.eq_one_iff _).mp h)`),
sem maquinaria de instância de risco além do que a Onda 6 já exercitou
com sucesso para HG-4g. Superfície de risco mínima.

**3. TOE-7 (item 10).** A defeq foi rastreada à mão, passo a passo,
neste próprio ciclo de revisão, não apenas assumida — `simp [e,
ActionCategory.objEquiv]` tem alta chance de fechar de primeira, e
mesmo o fallback (`Equiv.symm_trans_apply`+`Equiv.symm_symm`) já está
verificado como existente. Conteúdo científico baixo (quase tautológico,
ver seção 6), mas risco técnico também baixo.

**4. SHARED-7A (item 13).** Corolário de sinal trocado de uma
identidade já fechada — `ring` puro depois de `unfold`. Conteúdo
matemático marginal declaradamente perto de zero, mas exatamente por
isso o risco de falha também é próximo de zero.

Não incluo `RH-7D` no topo apesar de sólido: é o item de maior
complexidade algébrica desta onda (redução de soma via
`hasSum_sum_of_ne_finset_zero`, autoassinalada como citação "menos
firme" mesmo após confirmação). `QF-12` fica de fora do topo apesar de
muito bem de-riscado: a sintaxe de extensão de construtor anônimo
contra `ContinuousMonoidHom` é o único elo da cadeia que só a
compilação real resolve. `BSD-8` (item 9) fica de fora por desenho —
é, por natureza, um item de checkpoint-por-ramo com probabilidade não
desprezível de parar em "fora de escopo" antes do terceiro lema,
exatamente a disciplina que DEC-103 pediu, não uma falha do item se
isso acontecer. `NS-7A` (item 3) fica de fora pela mesma razão de
desenho — o protocolo de duas fases foi construído para permitir uma
parada informativa no meio.

## O laboratório chegou ao ponto de pausar o ciclo de ondas?

Avaliação honesta, atualizando a da Onda 6 (não repetindo-a).

**O que mudou desde a Onda 6:** nenhuma linha nova caiu a zero
candidatos nesta rodada — todas as 7 linhas mais infraestrutura
compartilhada renderam pelo menos um item de execução, o mesmo padrão
observado na Onda 6 (onde BSD chegou perto de zerar, mas não zerou). O
sinal mais importante desta rodada não é de quantidade, mas de
DISCIPLINA: a lição de escopo de `BSD-7` (DEC-103) não ficou confinada
a BSD — a mesma adversarial pegou, de forma independente, um candidato
de YM (`LAMBDAMAX-M1-QUADRATIC-EXACT`) tentando exatamente a mesma
manobra retórica que inflou BSD-7 ("preciso reproduzir mais coisa,
logo o teto deve ser maior" em vez de "conteúdo reproduzido é
excluído da contagem"), e corrigiu antes da execução. Isso é evidência
de que o mecanismo de revisão está generalizando a lição, não só
memorizando o caso específico de BSD.

**Quatro observações atualizadas:**

1. **`BSD-GAP-008` continua sendo a recomendação ativa correta, sem
   mudança de urgência nesta onda.** `BSD-8` (item 9) é, por desenho,
   mais um item de checkpoint-bounded da mesma veia estreita que
   produziu `BSD-7` — não uma nova fonte de itens baratos. Se `BSD-8`
   fechar dentro do teto (o resultado mais provável, dado o
   de-risco desta revisão), isso ainda não altera a avaliação de que a
   veia de `localPolynomial`/`localPowerSeries` está perto do próprio
   teto por linha. Nenhum evento desta onda enfraquece a recomendação
   de projeto dedicado já registrada na Onda 6; nenhum evento a torna
   mais urgente também — BSD ainda produziu um item nesta rodada, ao
   contrário de PN na Onda 5.

2. **TOE ganhou um sinal novo e mais fraco de afinamento de qualidade,
   não de quantidade.** `TOE-7` é honestamente avaliado nesta revisão
   como "quase tautológico" — conteúdo científico mais baixo até que
   `TOE-6a`/`TOE-6b` (Onda 6), que por sua vez já eram
   `FOUNDATIONAL_FORMALIZATION_ONLY`. Isso não é motivo para retirar
   TOE da rotação (o item ainda é um resultado formal genuíno e
   novo), mas é um sinal a observar: se a próxima onda também só
   conseguir extrair alvos quase-tautológicos desta linha, isso
   se aproximaria do mesmo tipo de esgotamento qualitativo que
   precedeu a retirada de PN.

3. **`TOE_INTERFACE_EXECUTION` continua sendo um gate nomeado e nunca
   disparado**, sem mudança de status desde a Onda 4. Nenhum evento
   desta onda muda essa avaliação — o ciclo de ondas segue tratando TOE
   como mais uma linha de sondas pequenas, não como investimento na
   síntese completa.

4. **RH, HG, NS, YM e QF continuam gerando alvos baratos e
   genuinamente novos, sem sinal de esgotamento equivalente ao de PN
   ou BSD.** YM, em particular, produziu o achado mais notável desta
   onda (um terceiro candidato inteiro que o recon original perdeu),
   sinal de que a linha ainda tem território não mapeado, não
   esgotado. NS manteve exatamente 1 item, como na Onda 6 — estável,
   não em declínio adicional.

**Conclusão honesta, refinada em relação à Onda 6:** a resposta
continua HÍBRIDA. (a) a linha PN permanece formalmente retirada da
rotação (DEC-100), sem reavaliação nesta rodada; (b) `BSD-GAP-008`
permanece "recomendação ativa" (linguagem da Onda 6), sem mudança de
urgência — `BSD-8` é tratado, corretamente, como continuação
bounded da mesma veia estreita, não como evidência de reabertura da
sub-linha; (c) `TOE_INTERFACE_EXECUTION` permanece candidato adiado,
não urgente, mas TOE como linha de sondas pequenas mostrou nesta onda
um primeiro sinal de afinamento QUALITATIVO (item quase-tautológico)
que vale observar nas próximas 1-2 ondas, não agir sobre ainda; (d) as
demais linhas (RH, NS, HG, YM, QF, SHARED-INFRA) devem continuar no
modo onda-pequena-paralela — nenhuma delas produziu, nesta rodada, um
sinal de esgotamento equivalente ao de PN. Não há ainda justificativa
honesta para declarar a varredura de portfólio inteira encerrada ou
para migrar o laboratório inteiro para o modo `TOE_INTERFACE_EXECUTION`
neste momento.

---

## O que este documento confirma sobre o processo

A disciplina de "reverificar por leitura direta de arquivo, checando
citação Mathlib por citação Mathlib, grepando o checkout Mathlib
vendorizado por conta própria, e fazendo a aritmética/álgebra à mão
quando aplicável" continuou achando coisas reais nesta rodada: uma
alegação central de racional diretamente contradita pelo próprio
teorema citado, não apenas mal-argumentada (`NS-7A` — a integral
depende sim do raio, ao contrário do que o candidato afirmava);
um emparelhamento de lema Mathlib tecnicamente-existente-mas-errado
(`HG-1i` — `pow_succ'` precisa de `succ_nsmul'`, não `succ_nsmul`,
confirmado por precedente exato em `GradedMonoid.lean:566`); uma
citação de "classe" que na verdade é um namespace, com termo de prova
proposto que não se aplica ao tipo em questão, mas cuja alegação de
viabilidade subjacente se revelou correta por uma cadeia de instância
diferente e mais indireta (`QF-13`); e, o achado estruturalmente mais
importante desta rodada, a mesma manobra retórica de contagem de
linhas que inflou `BSD-7` em 6,4x na Onda 6 reaparecendo, em miniatura,
num candidato de YM completamente não relacionado — pegada e corrigida
antes da execução, evidência de que a lição de DEC-103 está
generalizando através de linhas, não ficando confinada ao caso que a
gerou. Em nenhum caso isso refutou um alvo subjacente — em todos, o
resultado real continuou de pé, só precisou de reescopo, de uma
citação corrigida, ou de um teto de tamanho mais rigoroso e auditável.
A composição por linha desta onda (PN fora da rotação, sem
reavaliação; BSD com um item bounded reforçado; TOE com um primeiro
sinal qualitativo de afinamento; RH, NS, HG, YM, QF, SHARED-INFRA
seguindo estáveis ou até rendendo mais que o esperado) é o sinal
estrutural mais importante desta rodada — a confirmação de que a
disciplina de escopo aprendida com um único incidente (`BSD-7`) já
está sendo aplicada de forma preventiva, antes de um segundo incidente
acontecer, em vez de apenas reagindo depois do fato.
