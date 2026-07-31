---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T06:49:05-03:00
canonical_commit: "e1183da0f765189635d4d227ca4ffce313a77d18"
canonical_commit_policy: "aponta para o commit finalizado do gate; a atualização deste campo ocorre no commit de fechamento seguinte"
repository_clean: true
active_track: "millennium"
active_work_item: "RH-NOGO-001"
work_status: "SCOPED"
evidence_level: "F"
last_verified_artifact: "primary-source-audit-result.json"
current_blocker: "A lei de Weyl global (W8) e a discretude do espectro (W7) não são sustentadas pela fonte primária auditada; a cadeia da ponte está quebrada na etapa E."
next_single_action: "Obter a fonte primária ou monografia necessária para fechar as hipóteses ainda não sustentadas da Classe W, em especial a lei de Weyl global (W8) e a discretude do espectro (W7)."
authorized_action: "RH_NOGO_ADDITIONAL_SOURCE_RETRIEVAL_AUTHORIZED"
prohibited_actions:
  - "Não executar a prova do no-go completo (RH_NOGO_PROOF_EXECUTION não autorizado)"
  - "Não escrever a ponte formal entre as leis de contagem e ASYM-NOGO-001"
  - "Não formalizar Riemann–von Mangoldt nem a lei de Weyl"
  - "Não construir operador espectral algum"
  - "Não declarar que Hilbert–Pólya foi refutado"
  - "Não declarar progresso sobre a verdade ou falsidade da Hipótese de Riemann"
  - "Não citar as monografias candidatas de Q1 antes de obtê-las e lê-las"
  - "Não tratar traduções ou textos secundários como originais"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/SOURCE_MANIFEST.yaml"
  - "08_REVIEWS/SOURCES/RH_NOGO/CLASS_W_SOURCE_MAPPING.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/UNRESOLVED_SOURCE_QUESTIONS.md"
  - "03_MILLENNIUM/01_RIEMANN/STOP_CONDITIONS.md"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

A auditoria de fontes primárias de `RH-NOGO-001` foi executada. As quatro
fontes obrigatórias foram **obtidas** e preservadas com proveniência e
`sha256`. O resultado é **`PARTIALLY_SUFFICIENT`**.

## O que a auditoria estabeleceu

**Pilar A — contagem dos zeros: SUSTENTADO.** von Mangoldt 1905, p. 19,
prova incondicionalmente, com termo de erro efetivo de ordem `log T`:

```
N = (T/2π)·l(T/2π) − T/2π + 7/8 + η·(0,43200 lT + 1,91662 llT + 12,20373)
```

para `T > 28,558`, `−1 < η < 1`, contando zeros de `ξ(t)` por parte real,
**com multiplicidade**, com `T` escolhido fora de zeros.

**Pilar B — lei de Weyl: PARCIALMENTE SUSTENTADO.** Hörmander 1968 prova a
assíntota **local** da função espectral na diagonal (eq. 5.3), mas **não
enuncia** a contagem global `N_P(Λ) ~ C_P Λ^{d/m}`. Busca no texto integral
por "number of eigenvalues", "counting function", `N(λ)`: nenhuma
ocorrência.

## Classe W contra a fonte

| Estado | Hipóteses |
|---|---|
| `SUPPORTED_DIRECTLY` | W4 (elipticidade), W6 (positividade) |
| `PARTIALLY_SUPPORTED` | W1, W2 (só autovalores distintos), W3 |
| `AMBIGUOUS` | W5 (Friedrichs vs. essencial auto-adjunção) |
| `NOT_SUPPORTED` | **W7 (espectro discreto)**, **W8 (contagem global)** |

Duas de oito hipóteses diretamente sustentadas; as duas decisivas, não.

## Work items

| Item | Estado | Evidência |
|---|---|---|
| LAB-ARCH-001 | VERIFIED | governança e labctl |
| LAB-BENCH-001 | VERIFIED | lab-bench-001-result.json |
| FOUND-SEMIGROUP-001 | VERIFIED | found-semigroup-001-result.json |
| RH-NOGO-001 | SCOPED | especificação pronta; `ASYM-NOGO-001` VERIFIED; auditoria de fontes `PARTIALLY_SUFFICIENT` |

## Frente ativa

`RH-NOGO-001` — `SCOPED`, `NOT_AUTHORIZED`, `NO_EXECUTION`. A única
autorização vigente é **obter fontes adicionais**
(`RH_NOGO_ADDITIONAL_SOURCE_RETRIEVAL_AUTHORIZED`). A especificação da
ponte **não** foi autorizada, precisamente porque a etapa E da ponte está
sem fonte.

## Estados de leitura (dois eixos)

`CONTENT_AUDITED`: apenas RIEMANN-1859 (tradução Wilkins; o **original
alemão não foi obtido**).
`PARTIALLY_AUDITED`: VONMANGOLDT-1905, HORMANDER-1968, BOMBIERI-CLAY.

## Runtime

Ubuntu 24.04/WSL2; Lean `v4.33.0-rc1`; Mathlib
`79d0395a1825a6264ad5d269e35e60537518955e`.

## Próxima ação única

Obter a fonte primária ou monografia necessária para fechar as hipóteses
ainda não sustentadas da Classe W, em especial a lei de Weyl global (W8) e
a discretude do espectro (W7).

## Ações proibidas

- executar a prova do no-go completo ou qualquer frente Clay;
- escrever a ponte formal antes de fechar a etapa E;
- formalizar Riemann–von Mangoldt ou a lei de Weyl;
- construir operador espectral;
- declarar refutação de Hilbert–Pólya ou progresso sobre a RH;
- citar as monografias candidatas de Q1 antes de obtê-las e lê-las;
- alterar arquivos fora de `04_FORMAL_RESEARCH_LAB/`;
- usar sorry, admit, axioma local ou unsafe.

## Histórico recente

- 2026-07-31: LAB-WSL-MIGRATION migrou o runtime canônico para WSL2.
- 2026-07-31: LAB-BENCH-001 verificado.
- 2026-07-31: FOUND-SEMIGROUP-001 verificado (modelo C3).
- 2026-07-31: RH-NOGO-001 especificado (`SPECIFICATION_READY`).
- 2026-07-31: ASYM-NOGO-001 formalizado e verificado em Lean.
- 2026-07-31: auditoria de fontes primárias executada;
  `RH_NOGO_PRIMARY_SOURCES_PARTIALLY_SUFFICIENT`. Nenhum teorema novo,
  nenhuma claim promovida.
