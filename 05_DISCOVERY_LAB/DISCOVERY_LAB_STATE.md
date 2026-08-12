# Estado da Trilha de Descoberta Computacional

**Última atualização:** 2026-08-12
**Trilha paralela a:** `04_FORMAL_RESEARCH_LAB` (ciclo de ondas Lean, não afetado por esta trilha)

## Status atual

| Campo | Valor |
|---|---|
| Teste ativo | nenhum — `DISC-COSMOLOGY-MOND-SPARC-001` fechado |
| Fase | Piloto concluído (CLOSED_INCONCLUSIVE); trilha aguardando próximo teste |
| Próxima ação obrigatória | Nenhuma pendente. Escolher e pré-registrar o próximo teste (domínio aberto — ver `README.md`) quando houver decisão do usuário sobre onde apontar a trilha em seguida |
| Decisões de governança | `DISC-DEC-001` (criação da trilha), `DISC-DEC-002` (fechamento do piloto) |
| Claims fechados | 1 (`DISC-CLAIM-001`, evidence_level: `preregistered_inconclusive`) |
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

## O que ainda não foi feito

- Relatório de sessão em `09_SESSIONS/2026/`.
- Commit final de todo o ciclo (análise + governança + relatório) e push.
- Escolher o próximo teste da trilha (domínio ainda aberto/multi-domínio,
  conforme decisão original do usuário — nenhum compromisso além do piloto
  de cosmologia foi feito).

## Como continuar (para o próximo agente/sessão)

O piloto está fechado. Para um novo teste, seguir `00_GOVERNANCE/AGENTS.md`
desde o passo 1 (ler este arquivo, formular hipótese nova, localizar fonte
de dado real, escrever e commitar um NOVO `PREREGISTRATION.md` antes de
tocar em qualquer dado). Não reabrir nem editar
`02_TESTS/COSMOLOGY_MOND_SPARC/PREREGISTRATION.md` — está fechado e travado;
uma extensão dessa linha de investigação (ex. amostra maior, correção de
leverage, ou o desenho de campo externo de Chae et al. 2020) é um novo teste
com seu próprio pré-registro, não uma reabertura deste.
