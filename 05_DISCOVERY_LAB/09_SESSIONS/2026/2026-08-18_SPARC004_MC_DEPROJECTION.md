# Sessão 2026-08-18 — DISC-COSMOLOGY-MOND-SPARC-004: redesenho, análise e fechamento

## Contexto

Usuário pediu: "redesenhe o SPARC-003 com desprojeção Monte Carlo
completa". `DISC-COSMOLOGY-MOND-SPARC-003` (`02_TESTS/COSMOLOGY_WIDE_BINARIES/`)
havia sido fechado `CLOSED_INCONCLUSIVE` porque a estatística simplificada
de velocidade projetada (Chae 2023, Artigo B) tinha imagem matematicamente
restrita a `(1,+∞)`, mas as 5 medianas empíricas reais eram todas `<1` —
ajuste de `a0` estruturalmente impossível. O método primário completo de
Chae (desprojeção 3D via Monte Carlo orbital) havia sido descartado
naquele momento como "tratável demais para reproduzir".

## Pesquisa e pré-registro

Pesquisa dedicada (não memória) verificou o algoritmo exato de Chae
(2023), ApJ 952:128, arXiv:2305.04613v4, via leitura direta do
LaTeX-fonte. **Correção de citação encontrada:** o catálogo de
excentricidades individuais não é de "Hamers, Kratter & Shu" (presunção
inicial errada), e sim de Hwang, Ting & Zakamska (2022), MNRAS 512:3383,
arXiv:2111.01789 — verificado acessível (208MB, FITS, 1.817.594 linhas,
cobertura total de El-Badry+2021).

**Achado metodológico decisivo:** o método primário de Chae não ajusta
`a0` livre contra `g/g_N` bruto — usa uma estatística diferenciada,
`δ_obs-newt` = mediana real menos mediana de um ensemble Newtoniano mock
casado por sistema. Essa estatística não sofre da restrição de imagem que
matou SPARC-003.

Pré-registro escrito (`COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/PREREGISTRATION.md`),
reaproveitando H_A/H_B, catálogo, cortes de qualidade e split
discovery(30.203)/holdout(12.944 selado) de SPARC-002/003 sem modificação.
Catálogo de Hwang extraído para os 43.147 sistemas (100% de cobertura,
74,3% via excentricidade individual, resto via fallback populacional).

## Validação pré-lock: primeiro problema encontrado por desenho, não bug

A validação sintética obrigatória (`METHODOLOGY_EXTENSIONS.md` Seção 1,
lição direta de SPARC-003) rodou a pipeline sobre dado 100% Newtoniano
sintético e falhou seu critério literal: mediana recuperada de
`log10(g/g_N)=-0,204`, não próxima de 0. Diagnóstico: `g≡v²/r` não é a
aceleração radial newtoniana instantânea para órbita excêntrica — efeito
Kepleriano de médio-tempo-de-fase conhecido, batendo com a própria Eq. 16
de Chae. **Não é um bug.** Corrigido ANTES de qualquer dado real: a
estatística discriminadora passou a ser `δ_obs-newt` (Adendo 4c),
revalidada sob controle negativo (2 ensembles Newtonianos, ICs contêm 0)
e controle positivo (boost MOND injetado, sinal recuperado bate em sinal
e magnitude no bin onde é detectável acima do piso de ruído). Só então
`Status: LOCKED` (2026-08-15).

## Análise primária v1 e bug encontrado pela descoberta adversarial de nulos

Pipeline aplicada pela primeira vez ao `v_p` real observado. Resultado v1:
`δ_obs-newt=[+0,2274;+0,1723;+0,1313;+0,1027;+0,0467]`,
`a0_fit=3,634×10⁻¹⁰` (IC95% `[2,944×10⁻¹⁰;4,494×10⁻¹⁰]`), ambos `a0_A`/`a0_B`
fora → `BOTH_FALSIFIED` bruto. Reexecução adversarial bit a bit confirmou
v1 sem bug de fórmula/unidade/constante.

Mas a descoberta adversarial de nulos obrigatória (`AGENTS.md` passo 7)
achou um bug estrutural real: o ramo mock (`generate_synthetic_vp_newtonian`)
era sempre gerado sem ruído, enquanto o `v_p` real carrega ruído
astrométrico Gaia genuíno (viés de Rice/Rayleigh, magnitude de vetor 2D
ruidoso, pior em baixo SNR — justamente o bin de menor `g_N`). A subtração
`real-mock` não cancelava esse viés como a Seção 4c pretendia. **Prova
decisiva** (100% dado sintético, zero física MOND): injetar o MESMO ruído
real simetricamente nos dois ramos colapsa o efeito para consistente-com-
zero nos 5 bins; injetar só no ramo real reproduz ~33% da magnitude do
bin 0.

**Classificado como BUG DE IMPLEMENTAÇÃO** (Seção 5b do pré-registro), não
reformulação de H_A/H_B/critério/cortes — a estatística `δ_obs-newt`
continua conceitualmente correta; o mock só precisava replicar TODAS as
fontes de variância do ramo real, incluindo ruído de medição. Corrigido
(injeção de ruído Gaussiano simétrico via erros de PM reais do Gaia de
cada sistema), revalidado sob os mesmos controles do Adendo 4c antes de
reaceitar qualquer resultado real.

## Análise primária v2 (corrigida)

Reexecução completa: `δ_obs-newt=[+0,1486;+0,1482;+0,1150;+0,0949;+0,0430]`
— cerca de 5× menor que v1. `a0_fit=1,657×10⁻¹⁰` (IC95%
`[1,232×10⁻¹⁰;2,181×10⁻¹⁰]`). `a0_A=1,082288×10⁻¹⁰` cai **logo abaixo** do
limite inferior do IC (margem pequena, ≈0,057 dex); `a0_B` claramente
fora. Sanidade passa (0,14 dex do valor de referência McGaugh, bem melhor
que v1). Reexecução adversarial independente reproduziu v2 bit a bit (IC
de `a0` idêntico a 6 algarismos significativos) e encontrou uma
imprecisão de documentação menor (colunas de correlação `pmRApmDEcor1/2`
existem no catálogo bruto, ao contrário do que um comentário afirmava) —
teste de sensibilidade via Cholesky confirmou efeito desprezível
(≤0,00064 dex), não muda nenhuma conclusão.

## Checagem adversarial de multiplicidade oculta — o achado decisivo

O gatilho pré-declarado (`g/g_N` real bruto>1 no bin 0) ativou a checagem
adversarial obrigatória de multiplicidade oculta (`f_multi`, Chae Eqs.
11-13, declarada NÃO implementada por simplificação desde o pré-registro),
rodada duas vezes: sobre o sinal v1 (com bug) e refeita sobre o sinal v2
(corrigido).

**Na v1**, a inflação de massa por companheiras ocultas cobria no máximo
~25% do sinal, mesmo no limite superior de `f_multi` — conclusão:
"contribui mas não basta."

**Na v2**, com o sinal ~5× menor, o resultado se inverte: (1) a inflação
de massa sozinha (sem wobble) cobre de 23% a 146% do sinal por bin, e
79-146% no bin de menor `g_N`; (2) a diferença RUWE-alto vs. RUWE-baixo
permanece grande e significativa em todos os 5 bins, e agora EXCEDE o
sinal real total em vários deles; (3) uma simulação Monte Carlo própria de
injeção mostra que mesmo `f_multi=0,25` (limite inferior da faixa
observacional da literatura, 0,25-0,47) já produz sinal sintético (zero
física MOND) MAIOR que o sinal real inteiro nos 5 bins.

## Veredito

O critério mecânico da Seção 5, aplicado literalmente a v2, produz
`BOTH_FALSIFIED`. **Não aceito.** A própria Seção 4 do pré-registro já
pré-comprometia, antes de ver qualquer dado real, que esse gatilho exige
a checagem adversarial de multiplicidade oculta antes de aceitar o
veredito — e a checagem mostra que um confundidor mundano já nomeado e
conhecido (companheiras não resolvidas, em magnitude inteiramente
plausível pela literatura) é plausivelmente suficiente, sozinho, para
produzir o resíduo observado inteiro, sem física MOND. Registrado como
`DISC-CLAIM-006`, `evidence_level: preregistered_inconclusive`,
`adversarial_review_verdict: METHODOLOGY_FLAW_FOUND`. Teste fechado
`CLOSED_INCONCLUSIVE` em `TEST_QUEUE.yaml` — mesma disciplina já usada em
SPARC-003. Gate de Replicação não acionado. Holdout (12.944 sistemas)
permanece selado.

## Estado final

`DISC-COSMOLOGY-MOND-SPARC-004`: `CLOSED_INCONCLUSIVE` (confundidor de
multiplicidade oculta plausivelmente suficiente para explicar todo o
sinal residual). Todas as quatro linhas SPARC/MOND (001-004) estão agora
encerradas. `DISC-TRI-RG-001` segue pausada (`DISC-DEC-007`).

## Próxima decisão (não tomada nesta sessão)

Nenhuma linha ativa. Opções para o usuário: implementar a auto-calibração
completa de `f_multi` de Chae e reabrir esta linha com um pré-registro
genuinamente novo sobre o holdout selado; retomar `DISC-TRI-RG-001`
(grafo de visibilidade / RQA, únicos candidatos ainda não fechados);
investigar o achado de integridade de `gaia_real_analysis.py` (fabricação
de dado, fora do escopo do Discovery Lab); ou outra linha inteiramente
nova.
