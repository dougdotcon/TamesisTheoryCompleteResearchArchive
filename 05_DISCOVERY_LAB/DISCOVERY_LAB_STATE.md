# Estado da Trilha de Descoberta Computacional

**Última atualização:** 2026-08-12
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
| Teste ativo | `DISC-RH-GAP-EXTREME-VALUE-SCALING-001` (`ADVERSARIALLY_REVIEWED`, `CONFIRMED` — ver abaixo). `DISC-RH-ZERO-GAP-RUNS-001` encerrado (`REPLICATION_PASSED`). `DISC-COSMOLOGY-MOND-SPARC-002` encerrado (`REPLICATION_FAILED`). `DISC-TRI-RG-001` segue `CANDIDATE_FORMULATING`, não iniciado |
| Fase | RH-REAL: dois sub-testes concluídos. (1) `DISC-RH-ZERO-GAP-RUNS-001`: `INVERSE_SIGNAL` `REPLICATION_PASSED` — gaps grandes consecutivos são menos comuns que sob reordenação aleatória, confirmado em 3 regimes de altura (~75.000, ~10¹², ~10²¹). (2) `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`: gap mínimo escala como `N^(-1/3)` (GUE), exclui `N^(-1)` (Poisson) e `N^(-1/2)` (GOE) — resultado decisivo, `β̂=-0,3395` vs. previsão `-0,3333` |
| Próxima ação obrigatória | Decisão do usuário: acionar o Gate de Replicação completo para `DISC-CLAIM-004` (exigiria baixar `zeros5.txt`, regime #10²², já reservado) ou seguir para `DISC-TRI-RG-001` |
| Decisões de governança | `DISC-DEC-001` (criação da trilha), `DISC-DEC-002` (fechamento do piloto), `DISC-DEC-003` (arquitetura de três motores + seis extensões), `DISC-DEC-004` (pivô de SPARC-002 + pré-registro do teste de derivação de a₀) |
| Claims fechados/registrados | 4 (`DISC-CLAIM-001`, `preregistered_inconclusive`; `DISC-CLAIM-002`, `preregistered_inconclusive` após Gate, `replication_status: REPLICATION_FAILED`; `DISC-CLAIM-003`, `preregistered_falsified` [direção de H, efeito real na direção oposta], `replication_status: REPLICATION_PASSED`; `DISC-CLAIM-004`, `preregistered_confirmed`, `adversarial_review_verdict: CONFIRMED`, `replication_status: NOT_SUBMITTED`) |
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

- Escolher entre `DISC-RH-REAL-001` e `DISC-TRI-RG-001` (ou uma nova
  linha) para aprofundamento real.
- Resolver o `next_action` da linha escolhida (todas exigem trabalho de
  formulação — literatura, dado real, modelo concorrente nomeado — antes
  de qualquer pré-registro).
- Fora do escopo desta trilha, mas acionável: reportar/corrigir o
  provável erro de copy-paste em
  `01_TAMESIS_CORE/03_Axiomatic_Closure/Universe_Equation/02_MOND_Emergence/index.html:282`.

## Como continuar (para o próximo agente/sessão)

Ler `00_GOVERNANCE/RESEARCH_PIPELINE.md` e `METHODOLOGY_EXTENSIONS.md`
primeiro. Para uma das 2 linhas candidatas restantes, seguir
`00_GOVERNANCE/AGENTS.md` desde o passo 1 — mas agora o passo 3 exige
declarar o discriminating observable (e holdout selado, se aplicável) no
`PREREGISTRATION.md` antes do commit de lock. Não reabrir nem editar
`02_TESTS/COSMOLOGY_MOND_SPARC/PREREGISTRATION.md` (piloto 001) nem
`02_TESTS/COSMOLOGY_A0_DERIVATION/PREREGISTRATION.md` (teste 002, ambos
fechados e travados, holdout deste último já consumido) — uma extensão
de qualquer uma dessas linhas de investigação é um novo teste com seu
próprio pré-registro, não uma reabertura.
