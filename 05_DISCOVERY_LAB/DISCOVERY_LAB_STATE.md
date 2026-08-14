# Estado da Trilha de Descoberta Computacional

**Última atualização:** 2026-08-14
**Arquitetura:** motor 1 de 3 — ver `00_GOVERNANCE/RESEARCH_PIPELINE.md`
(`05_DISCOVERY_LAB` → `03_REPLICATION_GATE` → `04_FORMAL_RESEARCH_LAB`,
adotada em `DISC-DEC-003`). `04_FORMAL_RESEARCH_LAB` não é mais um
laboratório paralelo desacoplado — é o destino de formalização para claims
que sobrevivem ao Gate de Replicação (ver `DEC-107` de lá, que reclassifica
as Ondas 1-7 como arquivo de calibração de capacidade formal, não pesquisa
sobre nenhum Problema do Millennium).

## Status atual

| Campo | Valor |
|---|---|
| Teste ativo | Nenhum travado. `DISC-RH-ZERO-GAP-RUNS-001` encerrado (`REPLICATION_PASSED`). `DISC-RH-GAP-EXTREME-VALUE-SCALING-001` encerrado (`REPLICATION_FAILED` — inconclusivo por falta de poder no dataset reservado, achado primário NÃO contradito, ver seção própria abaixo). `DISC-COSMOLOGY-MOND-SPARC-002` encerrado (`REPLICATION_FAILED`). `DISC-TRI-RG-001` segue `CANDIDATE_FORMULATING` — Fase 0 concluída (5 candidatos avaliados, ver seção própria abaixo), nenhum travado ainda |
| Fase | RH-REAL: dois sub-testes concluídos, ambos com Gate de Replicação completo acionado. (1) `DISC-RH-ZERO-GAP-RUNS-001`: `INVERSE_SIGNAL` `REPLICATION_PASSED` — gaps grandes consecutivos são menos comuns que sob reordenação aleatória, confirmado em 3 regimes de altura (~75.000, ~10¹², ~10²¹). (2) `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`: gap mínimo escala como `N^(-1/3)` (GUE), exclui `N^(-1)` (Poisson) e `N^(-1/2)` (GOE) — `β̂=-0,3395` vs. previsão `-0,3333`, `evidence_level: preregistered_confirmed` sobre o dataset primário; Gate no terceiro dataset reservado (`zeros5.txt`, #10²²) resultou `REPLICATION_FAILED` por amostra pequena demais para a grade travada (0 blocos possíveis em N=10.000) — inconclusivo, não contraditório. TRI-RG: Fase 0 concluída — 3/5 candidatos `viable=true` com dado real verificado, nenhum ainda pronto para pré-registro (ver seção própria) |
| Próxima ação obrigatória | Decisão do usuário sobre `DISC-TRI-RG-001`: prosseguir com `critical-slowing-down` (candidato mais forte, mas com 3 gaps concretos a fechar antes de pré-registro), buscar segundo domínio para `wavelet-multiresolution-scaling`, reformular `dfa-multiscale-entropy`, ou nova rodada de busca |
| Decisões de governança | `DISC-DEC-001` (criação da trilha), `DISC-DEC-002` (fechamento do piloto), `DISC-DEC-003` (arquitetura de três motores + seis extensões), `DISC-DEC-004` (pivô de SPARC-002 + pré-registro do teste de derivação de a₀) |
| Claims fechados/registrados | 4 (`DISC-CLAIM-001`, `preregistered_inconclusive`; `DISC-CLAIM-002`, `preregistered_inconclusive` após Gate, `replication_status: REPLICATION_FAILED`; `DISC-CLAIM-003`, `preregistered_falsified` [direção de H, efeito real na direção oposta], `replication_status: REPLICATION_PASSED`; `DISC-CLAIM-004`, `preregistered_confirmed`, `adversarial_review_verdict: CONFIRMED`, `replication_status: REPLICATION_FAILED` [inconclusivo por falta de poder no dataset reservado, não contradição]) |
| Claims em andamento | 0 |

## Resultado do piloto (DISC-COSMOLOGY-MOND-SPARC-001)

Auditoria do código legado (`AUDIT_LEGACY_MOND_EFE_SPARC.md`) confirmou que
o resultado "EFE CONFIRMED, p<0.000001" de
`01_TAMESIS_CORE/.../MOND_EFE/efe/README.md` vinha de curvas de rotação
digitadas à mão para 8 galáxias de Virgem que **não existem** no catálogo
SPARC público real — não apenas um fallback de emergência, mas o dado por
trás da manchete inteira.

Refeito com dado real (SPARC_Lelli2016c.mrt + Rotmod_LTG/*.dat, 175
galáxias, proveniência em `data/PROVENANCE.md`), pré-registro travado antes
de qualquer cálculo (`PREREGISTRATION.md`, commit `49867fa`), o teste
comparável disponível (aglomerado de Ursa Maior vs. campo, já que Virgem não
está representado na amostra real) deu p=0.049373 — cruza o limiar de 0.05
na direção prevista pelo EFE, mas cai exatamente na zona frágil (0.04–0.06)
que o próprio pré-registro já previa precisar declarar como tal.

Reexecução adversarial independente reproduziu os números exatamente (sem
bugs) e mostrou que excluir 4 galáxias de campo com ajuste de inclinação
baseado em apenas 2 pontos inverte o veredito (p sobe para 0.0635). Veredito
formal: **INCONCLUSIVE**. Registrado em `DISC-CLAIM-001`, sem nenhuma
linguagem "CONFIRMED"/"DETECTED".

Este é o resultado que a trilha foi desenhada para produzir: nem a manchete
inflada do código legado, nem uma negação categórica — um número real,
reproduzido de forma independente, e corretamente rotulado como frágil
demais para sustentar qualquer alegação de detecção.

## Resultado de DISC-COSMOLOGY-MOND-SPARC-002 (pivotado, encerrado)

`next_action` original (extrair de `01_TAMESIS_CORE` uma previsão Tamesis
distinta de MOND genérico) resolvido com achado **negativo**: essa
previsão não existe. Pivotado para testar qual das duas derivações
internas conflitantes de `a₀` sobrevive ao dado real — `a₀=cH₀/(2π)`
("Ponte Holográfica") vs. `a₀=cH₀` ("MOND Emergence", cuja própria
alegação numérica já é aritmeticamente incorreta por fator ~5,7,
independente de qualquer dado).

Na amostra de descoberta (120 galáxias), o resultado pareceu decisivo:
`H_A` sobrevive, `H_B` falsificada por fator ~2,5×, reproduzido de forma
independente com 0,004% de diferença. O Gate de Replicação (holdout de 55
galáxias, nunca antes visto, aberto por um terceiro agente independente)
**não confirmou** esse resultado — `g†` no holdout saiu 3,5× maior,
intervalo de confiança largo o suficiente para conter as duas hipóteses.
Um adversário de nulo dedicado mostrou que o achado sobrevive a
sistemáticas conhecidas do SPARC, mas seu peso evidencial específico para
Tamesis é mais fraco do que parecia (a0_A reproduz uma coincidência já
conhecida na literatura MOND padrão desde antes de Tamesis existir).
Achado lateral acionável: `MOND_Emergence/index.html:282` provavelmente
contém um erro de copy-paste, independente do veredito estatístico.

Veredito final: `DISC-CLAIM-002`, `evidence_level: preregistered_inconclusive`,
`replication_status: REPLICATION_FAILED` (inconclusivo, não contraditório).
Ver `09_SESSIONS/2026/2026-08-12_A0_DERIVATION_PIVOT.md` para o relato
completo em ordem cronológica.

## Resultado da linha RH-REAL (dois sub-testes, ambos com Gate acionado)

Motivada pela pesquisa de zeros de zeta da Anthropic, a linha `DISC-RH-REAL-001`
converteu duas afirmações de literatura não-testáveis com dado finito
(`liminf`/"infinitos") em perguntas proxy falsificáveis com modelo
concorrente nomeado, satisfazendo a exigência de discriminating observable.

**Sub-teste 1 — `DISC-RH-ZERO-GAP-RUNS-001`** (item 9, correlação sequencial
de gaps). Hipótese direcional original **errada** — previu mais runs de
gaps grandes consecutivos, achado real foi o oposto (`INVERSE_SIGNAL`,
reportado honestamente como tal, sem spin). Gate de Replicação com
`zeros4.txt` (regime #10²¹): `REPLICATION_PASSED`. Adversário de nulo
mostrou que o efeito é genérico a qualquer sequência com autocorrelação
serial negativa (confirmado via simulação sintética AR(1)) — isso não
enfraquece o achado, já que a alegação substantiva sempre foi "gaps de
zeta têm correlação serial negativa", não um mecanismo exclusivo de zeta.
Ver `09_SESSIONS/2026/` para o relato completo desta sessão.

**Sub-teste 2 — `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`** (item 7,
constante de gaps pequenos de Inoue 2026, arXiv:2604.05733). Pergunta
proxy via teoria de valores extremos: gap normalizado mínimo entre `N`
zeros escala como `N^(-1/3)` (GUE) ou `N^(-1)` (Poisson)? Resultado sobre
`zeros1.txt` (100k zeros): `β̂=-0,3395`, quase exatamente `-1/3=-0,3333`,
IC 95% bootstrap `[-0,3872;-0,2868]` — contém GUE folgadamente, exclui
Poisson e GOE (`-1/2`) com folga grande. `evidence_level:
preregistered_confirmed`, `adversarial_review_verdict: CONFIRMED`
(reprodução bit a bit por agente independente, três métodos de ajuste
concordantes). Gate de Replicação completo acionado sobre `zeros5.txt`
(regime #10²², nunca antes baixado): **`REPLICATION_FAILED` por falta de
poder estatístico**, não por contradição — o dataset reservado só tem
9.999 gaps, insuficiente para a grade travada (0 blocos possíveis em
N=10.000; só N=500/N=1.000 atingem a barra de ≥8 blocos declarada no
pré-registro, e restritos a esses dois pontos o IC vira
não-informativo). O achado primário sobre `zeros1.txt` permanece de pé,
apenas não pôde ser confirmado de forma independente numa terceira altura
com esta fonte específica. `promoted_to_formal_lab: false` — confirmação
numérica de universalidade GUE já conhecida na literatura, não descoberta
matemática nova. Lição de governança documentada em
`03_REPLICATION_GATE/PROTOCOL.md`: verificar A PRIORI que uma fonte
reservada tem amostra suficiente para a grade já travada, não apenas que
existe em regime diferente. Ver
`09_SESSIONS/2026/2026-08-12_RH_GAP_EXTREME_VALUE_SCALING.md` para o
relato completo.

Não há mais fonte adicional de Odlyzko disponível no regime #10²² para
resolver a falta de poder do sub-teste 2 sem consumir dado já usado.

## Resultado da Fase 0 de `DISC-TRI-RG-001` (2026-08-14)

5 candidatos de par `(R_lambda, I(X))` avaliados em paralelo por agentes
de pesquisa independentes, cada um obrigado a verificar dado real (baixar/
inspecionar, não só citar) antes de declarar um domínio utilizável. Relato
completo em `02_TESTS/TRI_RG/phase0/PHASE0_SURVEY.md`.

**3/5 `viable: true`**, ranqueados por uma síntese adversarial que aplicou
a mesma régua a todos: (1) **critical-slowing-down** — variância/
autocorrelação lag-1 crescentes perto de bifurcação (Scheffer 2009, Dakos
2008/2012, Lenton 2012); 3 domínios com transição REAL dentro do mesmo
sistema no tempo, dado verificado (GISP2/Younger Dryas, PhysioNet SDDB/
onset de fibrilação ventricular, NASDAQ/crash pontocom); modelo
concorrente nomeado real (B-tipping vs. R/N-tipping, Ashwin 2012); ainda
faltam regra de `lambda` cross-domain, protocolo de nulo substituto, e o
cálculo real de `Delta I` (só o acesso ao dado foi verificado). (2)
**wavelet-multiresolution-scaling** — `R_lambda` mais rigoroso
matematicamente dos 5 (`R_2λ=R_λ'∘R_λ` por construção via subespaços
aninhados), mas só 1 domínio robusto (sismologia, mainshock de Tohoku
2011, rótulo USGS/GCMT externo). (3) **dfa-multiscale-entropy** —
execução empírica mais sólida (DFA implementado do zero, validado contra
nulos teóricos, rodado sobre dado PhysioNet real decodificado E sobre os
gaps de zeta já usados em `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`), mas
os 2 domínios usados são comparações ESTÁTICAS de classe (saudável vs.
insuficiência cardíaca; continental vs. oceânico), não transições
temporais — mesmo defeito que corretamente derrubou o candidato (4)
abaixo, só detectado na síntese cross-candidato.

**2/5 `viable: false`**, corretamente rejeitados pelos próprios agentes:
(4) **box-covering-network-renorm** (Song-Havlin-Makse) — `R_lambda` mais
literal de todos, dado real de 4 redes verificado (SNAP/CAIDA), mas toda
"transição" fractal↔não-fractal na literatura vem de modelos sintéticos
com parâmetro artificial; dado real só mostra classificação estática, e
essa classificação está sob disputa ativa em 2025. (5)
**spacing-statistics-rmt-non-zeta** — dado real e computação real
executados (níveis nucleares RIPL-3, autovalores de rede SNAP), mas falha
em identificabilidade (previsão idêntica ao consenso BGS/RMT de 40 anos)
e em RG/EFT (nenhum `R_lambda` genuíno implementado).

**Nenhum candidato foi travado.** Decisão de qual (ou quais) perseguir
fica com o usuário.

## O que já foi feito nesta trilha

1. Governança criada: `00_GOVERNANCE/{AGENTS.md,DECISION_LEDGER.yaml,CLAIM_LEDGER.yaml,PREREGISTRATION_TEMPLATE.md}`.
2. Piloto escolhido (autorização explícita do usuário): auditar e refazer o
   teste EFE/SPARC de `01_TAMESIS_CORE/02_Experimental_Validation/MOND_EFE`.
3. Auditoria do código legado completa (`AUDIT_LEGACY_MOND_EFE_SPARC.md`,
   8 achados citados por arquivo:linha).
4. Dado real baixado e verificado (`data/PROVENANCE.md`).
5. Pré-registro travado (`PREREGISTRATION.md`, commit `49867fa`).
6. Análise pré-registrada executada sobre dado real
   (`analysis/run_preregistered_analysis.py`, `result_primary.json`).
7. Reexecução adversarial por agente independente
   (`analysis/adversarial_reproduction.py`, `result_adversarial.json`) —
   veredito INCONCLUSIVE.
8. Resultado registrado em `TEST_QUEUE.yaml` (status `CLOSED_INCONCLUSIVE`)
   e `CLAIM_LEDGER.yaml` (`DISC-CLAIM-001`).
9. Decisão de fechamento registrada (`DISC-DEC-002`).

## Arquitetura adotada em 2026-08-12 (`DISC-DEC-003`)

Revisão estratégica externa do usuário identificou que o laboratório
formal (Ondas 1-7, `04_FORMAL_RESEARCH_LAB`) provavelmente otimizava
probabilidade de fechamento (13/13 em três ondas seguidas) em vez de valor
científico esperado. Resposta: arquitetura de três motores
(`00_GOVERNANCE/RESEARCH_PIPELINE.md`) — descoberta de risco alto aqui,
Gate de Replicação (`03_REPLICATION_GATE/PROTOCOL.md`) de risco baixo no
meio, formalização Lean de risco baixíssimo só para quem sobrevive os dois.
Seis extensões técnicas de metodologia adotadas junto
(`00_GOVERNANCE/METHODOLOGY_EXTENSIONS.md`): identificabilidade
(discriminating observable obrigatório), RG/EFT para TRI/TDTR, MDL/
complexidade algorítmica (`ΔJ`), descoberta automática de invariantes
antes de narrativa LLM, descoberta adversarial de nulos (debunker
convencional dedicado), holdout selado obrigatório para buscas amplas.

Três linhas candidatas registradas (`01_PORTFOLIO/TEST_QUEUE.yaml`,
status `CANDIDATE_FORMULATING`, nenhuma pré-registrada):
- `DISC-COSMOLOGY-MOND-SPARC-002` — SPARC como comparação preditiva de
  modelos nomeados, não confirmação/refutação de EFE isolada.
- `DISC-RH-REAL-001` — pesquisa real sobre `riemannZeta`, distinta do
  operador de brinquedo `Tp` (agora reclassificado em
  `04_FORMAL_RESEARCH_LAB` como teste unitário de maquinário, não
  caminho até RH — ver `DEC-107` de lá).
- `DISC-TRI-RG-001` — busca de invariante cross-domain via lente de
  renormalização/coarse-graining para a Theory of Regime Interfaces.

## O que ainda não foi feito

- Decisão do usuário sobre qual candidato de `DISC-TRI-RG-001` perseguir
  (ver seção própria acima) e fechamento dos gaps concretos do candidato
  escolhido antes de qualquer `PREREGISTRATION.md`.
- Fora do escopo desta trilha, mas acionável: reportar/corrigir o
  provável erro de copy-paste em
  `01_TAMESIS_CORE/03_Axiomatic_Closure/Universe_Equation/02_MOND_Emergence/index.html:282`.

## Como continuar (para o próximo agente/sessão)

Ler `00_GOVERNANCE/RESEARCH_PIPELINE.md` e `METHODOLOGY_EXTENSIONS.md`
primeiro. Para `DISC-TRI-RG-001` ou uma nova linha, seguir
`00_GOVERNANCE/AGENTS.md` desde o passo 1 — mas o passo 3 exige declarar
o discriminating observable (e holdout selado, se aplicável) no
`PREREGISTRATION.md` antes do commit de lock, e ao reservar uma fonte de
dado adicional para o Gate, verificar A PRIORI que ela tem amostra
suficiente para a grade/estatística que será travada (lição de
`03_REPLICATION_GATE/PROTOCOL.md`, 2026-08-13). Não reabrir nem editar
`02_TESTS/COSMOLOGY_MOND_SPARC/PREREGISTRATION.md` (piloto 001),
`02_TESTS/COSMOLOGY_A0_DERIVATION/PREREGISTRATION.md` (teste 002),
`02_TESTS/RH_ZETA_ZEROS/PREREGISTRATION.md` (RH-REAL sub-teste 1) nem
`02_TESTS/RH_GAP_EXTREME_VALUE_SCALING/PREREGISTRATION.md` (RH-REAL
sub-teste 2) — todos fechados e travados, holdouts/fontes reservadas já
consumidos. Uma extensão de qualquer uma dessas linhas de investigação é
um novo teste com seu próprio pré-registro, não uma reabertura.
