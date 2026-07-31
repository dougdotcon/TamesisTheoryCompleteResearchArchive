---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T06:15:28-03:00
canonical_commit: "f2d50029db08608f04822f580c9e2d22c20be4b9"
canonical_commit_policy: "aponta para o commit finalizado do gate; a atualização deste campo ocorre no commit de fechamento seguinte"
repository_clean: true
active_track: "millennium"
active_work_item: "RH-NOGO-001"
work_status: "SCOPED"
evidence_level: "F"
last_verified_artifact: "asym-nogo-001-result.json"
current_blocker: "A ponte entre o lema abstrato, Riemann–von Mangoldt e a lei de Weyl ainda depende da leitura e auditoria das fontes primárias."
next_single_action: "Obter e auditar integralmente as fontes primárias necessárias para Riemann–von Mangoldt e para a versão exata da lei de Weyl, sem iniciar a prova do no-go espectral."
authorized_action: "RH_NOGO_PRIMARY_SOURCE_AUDIT_AUTHORIZED"
prohibited_actions:
  - "Não executar a prova do no-go completo (RH_NOGO_PROOF_EXECUTION não autorizado)"
  - "Não construir operador espectral algum"
  - "Não conectar o lema abstrato a Hörmander, von Mangoldt ou à Classe W antes da leitura primária"
  - "Não declarar que Hilbert–Pólya foi refutado"
  - "Não declarar progresso sobre a verdade ou falsidade da Hipótese de Riemann"
  - "Não usar GUE, zeros ou dados definidos pelos próprios zeros como premissa"
  - "Não citar preprints não auditados como resultado estabelecido"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "03_MILLENNIUM/01_RIEMANN/README.md"
  - "03_MILLENNIUM/01_RIEMANN/EPISTEMIC_CORRECTIONS.md"
  - "03_MILLENNIUM/01_RIEMANN/BIBLIOGRAPHY_AUDIT.md"
  - "03_MILLENNIUM/01_RIEMANN/STOP_CONDITIONS.md"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

O núcleo abstrato `ASYM-NOGO-001` está **formalizado e verificado em Lean**.
`RH-NOGO-001` permanece `SCOPED`: o no-go espectral completo não foi provado,
nenhum operador foi construído e nada foi afirmado sobre a verdade ou
falsidade da Hipótese de Riemann.

## O que foi provado

```text
Não existe N : ℝ → ℝ com N(T)/(T log T) → c > 0 e, simultaneamente,
N(T)/T^α → C > 0 para algum α > 0.
```

Análise real elementar, sem zeta, sem operadores, sem PDE, sem π. Doze
teoremas rastreáveis em `05_FORMAL/lean/TamesisLab/RHNogo/AsymptoticCore/`;
mapa em `03_MILLENNIUM/01_RIEMANN/ASYM_NOGO_001_THEOREM_MAP.md`; auditoria
adversarial e de axiomas em `ASYM_NOGO_001_PROOF_AUDIT.md`.

## O que NÃO foi provado

- a fórmula de Riemann–von Mangoldt;
- a lei de Weyl;
- a aplicação dessas fórmulas a uma classe de operadores;
- `RH-NOGO-001` completo (exclusão da Classe W);
- inexistência de operador de Hilbert–Pólya;
- verdade ou falsidade da Hipótese de Riemann.

## Work items

| Item | Estado | Evidência |
|---|---|---|
| LAB-ARCH-001 | VERIFIED | governança e labctl |
| LAB-BENCH-001 | VERIFIED | lab-bench-001-result.json |
| FOUND-SEMIGROUP-001 | VERIFIED | found-semigroup-001-result.json |
| RH-NOGO-001 | SCOPED | especificação pronta; subartefato `ASYM-NOGO-001` VERIFIED |

## Frente ativa

`RH-NOGO-001` — `SCOPED`, `NOT_AUTHORIZED`, `NO_EXECUTION`. A única
autorização vigente é a **auditoria das fontes primárias**
(`RH_NOGO_PRIMARY_SOURCE_AUDIT_AUTHORIZED`).

Motivo do bloqueio: nenhuma das oito referências catalogadas está
`CONTENT_AUDITED` — ver `03_MILLENNIUM/01_RIEMANN/EPISTEMIC_CORRECTIONS.md`,
que separa `source_retrieval_status` de `mathematical_claim_status`. O lema
abstrato não depende de nenhuma delas, mas a **ponte** para as duas leis de
contagem depende (GAP-RH-002, GAP-RH-003).

## Runtime

Ubuntu 24.04/WSL2; Lean `v4.33.0-rc1`; Mathlib
`79d0395a1825a6264ad5d269e35e60537518955e`. Detalhes em
`05_FORMAL/LEAN_ENVIRONMENT.md`.

## Próxima ação única

Obter e auditar integralmente as fontes primárias necessárias para
Riemann–von Mangoldt e para a versão exata da lei de Weyl, sem iniciar a
prova do no-go espectral.

## Ações proibidas

- executar a prova do no-go completo ou qualquer frente Clay;
- construir operador espectral;
- conectar o lema abstrato às leis de contagem antes da leitura primária;
- declarar refutação de Hilbert–Pólya ou progresso sobre a RH;
- usar GUE, zeros ou dados definidos pelos próprios zeros como premissa;
- citar preprints não auditados como resultados estabelecidos;
- alterar arquivos fora de `04_FORMAL_RESEARCH_LAB/`;
- usar sorry, admit, axioma local ou unsafe.

## Histórico recente

- 2026-07-31: LAB-WSL-MIGRATION migrou o runtime canônico para WSL2.
- 2026-07-31: LAB-BENCH-001 verificado.
- 2026-07-31: FOUND-SEMIGROUP-001 verificado (modelo C3).
- 2026-07-31: RH-NOGO-001 especificado e catalogado
  (`RH_NOGO_001_SPECIFICATION_READY`).
- 2026-07-31: ASYM-NOGO-001 formalizado e verificado
  (`ASYM_NOGO_001_VERIFIED`); duas correções epistemológicas aplicadas aos
  artefatos do gate anterior, sem reescrever o relatório de sessão.
