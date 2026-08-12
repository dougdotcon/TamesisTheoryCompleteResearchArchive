# Arquitetura de três motores

**Decisão de origem:** `DISC-DEC-003` (`DECISION_LEDGER.yaml`), motivada por
revisão estratégica externa do usuário em 2026-08-12, após o piloto
`DISC-COSMOLOGY-MOND-SPARC-001`. Substitui o modelo anterior de dois
laboratórios paralelos e desacoplados (`04_FORMAL_RESEARCH_LAB` gerando seu
próprio ciclo de ondas; `05_DISCOVERY_LAB` operando de forma independente)
por um fluxo único com um portão explícito no meio.

```text
                SCIENTIFIC SEARCH ENGINE
                         │
                         ▼
              ┌─────────────────────┐
              │  05_DISCOVERY_LAB   │   risco ALTO
              │                     │   (ver 02_TESTS/)
              │ papers, LLM hipótese│
              │ symbolic regression │
              │ simulações          │
              │ dados públicos      │
              │ busca numérica      │
              │ contra-exemplos     │
              └─────────┬───────────┘
                        │
               candidato sobrevive
              à reexecução adversarial
             (00_GOVERNANCE/AGENTS.md
                  passo 7)?
                        │
             ┌──────────┴───────────┐
             │                      │
            NÃO                    SIM
             │                      │
      NEGATIVE LEDGER               ▼
    (CLAIM_LEDGER.yaml,   ┌─────────────────────┐
     evidence_level       │ 03_REPLICATION_GATE │   risco BAIXO
     preregistered_       │                     │   (ver PROTOCOL.md)
     falsified/null)      │ agente independente │
                          │ implementação nova   │
                          │ dado held-out        │
                          │ modelos nulos         │
                          │ auditoria de proven.  │
                          └──────────┬──────────┘
                                    │
                             sobrevive de novo?
                                    │
                    ┌───────────────┴────────────────┐
                    │                                 │
                   NÃO                                SIM
                    │                                 │
             NEGATIVE LEDGER                          ▼
                                          ┌─────────────────────┐
                                          │04_FORMAL_RESEARCH   │  risco
                                          │       _LAB          │  BAIXÍSSIMO
                                          │                     │
                                          │ Lean, prova simbólica│
                                          │ cotas de erro         │
                                          │ extração de teorema   │
                                          └─────────────────────┘
```

## O que muda e o que não muda

Isto preserva praticamente toda a disciplina já construída em ambos os
laboratórios (claim ledger, proveniência, stop conditions, `REFUTED`,
revisão adversarial, Lean, versionamento, negativos documentados, Transition
Atlas). O que muda é **onde o risco é aceito**:

- **Na descoberta (`05_DISCOVERY_LAB`):** risco alto. Hipóteses ousadas,
  buscas amplas, muita coisa deve morrer aqui — `REFUTED`, `NULL`,
  `INCONCLUSIVE`, `OUT_OF_DOMAIN` são resultados de valor, não desperdício.
  Ver `METHODOLOGY_EXTENSIONS.md` para as ferramentas que tornam essa busca
  disciplinada (identificabilidade, RG/EFT, MDL, descoberta automática de
  invariantes, adversário de nulo, holdout cego).
- **No Gate de Replicação (`03_REPLICATION_GATE`):** risco baixo. Nada passa
  sem reprodução independente, dado não visto pela análise original, e
  auditoria de proveniência. Ver `PROTOCOL.md`.
- **Na promoção de claim para o laboratório formal (`04_FORMAL_RESEARCH_LAB`):**
  risco baixíssimo. Só chega aqui o que já sobreviveu duas rodadas de
  tentativa de refutação. A partir daqui, a disciplina de verificação
  formal de quatro camadas do laboratório Lean se aplica sem alteração —
  ver `04_FORMAL_RESEARCH_LAB/AGENTS.md`.

## Ciclo de vida de um item (`TEST_QUEUE.yaml` / `RESEARCH_QUEUE.yaml`)

```text
CANDIDATE_FORMULATING        -- hipótese sendo formulada, dado sendo localizado
        │
        ▼
CANDIDATE_LOCKED             -- pré-registro travado e commitado (AGENTS.md passo 3-4)
        │
        ▼
ANALYZED                     -- análise pré-registrada rodada sobre dado real
        │
        ▼
ADVERSARIALLY_REVIEWED       -- reexecução adversarial concluída (AGENTS.md passo 7)
        │
   sobreviveu?
    ┌───┴───┐
   NÃO     SIM
    │       │
    ▼       ▼
CLOSED_*   REPLICATION_PENDING     -- entra no Gate de Replicação
(REFUTED/       │
 NULL/          ▼
 INCONCLUSIVE/  REPLICATION_PASSED / REPLICATION_FAILED
 OUT_OF_DOMAIN)      │
                sobreviveu?
                 ┌───┴───┐
                NÃO     SIM
                 │       │
                 ▼       ▼
            CLOSED_*   PROMOTED_TO_FORMAL_LAB
                              │
                              ▼
                    (vira item RESEARCH_QUEUE.yaml em
                     04_FORMAL_RESEARCH_LAB, sujeito à
                     disciplina de verificação Lean padrão)
```

`CLOSED_*` nunca é um estado envergonhado. Um laboratório que tenta coisas
difíceis deve produzir `CLOSED_REFUTED`/`CLOSED_NULL`/`CLOSED_INCONCLUSIVE`/
`CLOSED_OUT_OF_DOMAIN` com frequência — isso é informação, catalogada com o
mesmo peso que um `PROMOTED_TO_FORMAL_LAB`.

## Relação com os laboratórios existentes

- `04_FORMAL_RESEARCH_LAB` deixa de ser autogerador de seu próprio próximo
  alvo (ver `DEC-107`, que reclassifica as Ondas 1-7 como "Formal
  Capability & Method Calibration Archive"). Ele continua existindo,
  intocado em conteúdo, como o destino de formalização para claims
  replicados — e como prova de que, quando um alvo real chega, o
  maquinário de verificação Lean já está calibrado e funciona.
- `01_TAMESIS_CORE/03_TRANSITION_ATLAS` permanece a infraestrutura
  reaproveitável de registro computável (regimes, transições, evidência,
  falsificação, incerteza, proveniência) — candidato natural para hospedar
  achados da linha TRI/RG (ver `METHODOLOGY_EXTENSIONS.md` §2) depois que
  sobreviverem ao Gate de Replicação.
