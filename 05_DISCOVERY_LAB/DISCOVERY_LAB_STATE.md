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
| Teste ativo | `DISC-COSMOLOGY-MOND-SPARC-002` (pivotado, `ADVERSARIALLY_REVIEWED`) — as outras 2 linhas candidatas (`DISC-RH-REAL-001`, `DISC-TRI-RG-001`) seguem `CANDIDATE_FORMULATING` |
| Fase | Achado forte e robusto: uma das duas derivações internas conflitantes de `a₀` do corpo teórico Tamesis (`a₀=cH₀`, "MOND Emergence") foi falsificada contra dado real SPARC; a outra (`a₀=cH₀/2π`, "Ponte Holográfica") sobreviveu. Reproduzido de forma independente (0,004% de diferença). Holdout selado (55 galáxias) ainda não aberto |
| Próxima ação obrigatória | Decisão do usuário: acionar o Gate de Replicação completo (`03_REPLICATION_GATE/PROTOCOL.md` — terceiro agente independente, abertura do holdout, adversário de nulo dedicado) para este resultado, ou seguir para outra linha |
| Decisões de governança | `DISC-DEC-001` (criação da trilha), `DISC-DEC-002` (fechamento do piloto), `DISC-DEC-003` (arquitetura de três motores + seis extensões), `DISC-DEC-004` (pivô de SPARC-002 + pré-registro do teste de derivação de a₀) |
| Claims fechados/registrados | 2 (`DISC-CLAIM-001`, `preregistered_inconclusive`; `DISC-CLAIM-002`, `preregistered_falsified` para H_B, `adversarial_review_verdict: CONFIRMED`) |
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

- Priorização do usuário entre as 3 linhas candidatas para aprofundamento
  real nesta sessão ou na próxima.
- Resolver o `next_action` de qualquer uma delas (todas exigem trabalho de
  formulação — literatura, dado real, modelo concorrente nomeado — antes
  de qualquer pré-registro).

## Como continuar (para o próximo agente/sessão)

Ler `00_GOVERNANCE/RESEARCH_PIPELINE.md` e `METHODOLOGY_EXTENSIONS.md`
primeiro. Para uma das 3 linhas candidatas, seguir `00_GOVERNANCE/AGENTS.md`
desde o passo 1 — mas agora o passo 3 exige declarar o discriminating
observable (e holdout selado, se aplicável) no `PREREGISTRATION.md` antes
do commit de lock. Não reabrir nem editar
`02_TESTS/COSMOLOGY_MOND_SPARC/PREREGISTRATION.md` (piloto 001, fechado e
travado) — uma extensão dessa linha de investigação é um novo teste com
seu próprio pré-registro, não uma reabertura deste.
