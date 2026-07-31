---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T05:37:29-03:00
canonical_commit: "a961eb6060d0b880c3452f179e094c94092df6b1"
canonical_commit_policy: "aponta para o commit finalizado do gate; a atualização deste campo ocorre no commit de fechamento seguinte"
repository_clean: true
active_track: "millennium"
active_work_item: "RH-NOGO-001"
work_status: "SCOPED"
evidence_level: "F"
last_verified_artifact: "rh-nogo-001-specification-result.json"
current_blocker: null
next_single_action: "Formalizar somente o lema abstrato de incompatibilidade assintótica (ASYM-NOGO-001), sem formalizar PDE, lei de Weyl ou construir operador espectral."
authorized_action: "RH_NOGO_ASYMPTOTIC_LEMMA_FORMALIZATION_AUTHORIZED"
prohibited_actions:
  - "Não executar a prova do no-go completo (RH_NOGO_PROOF_EXECUTION não autorizado)"
  - "Não construir operador espectral algum"
  - "Não declarar que Hilbert–Pólya foi refutado"
  - "Não declarar progresso sobre a verdade ou falsidade da Hipótese de Riemann"
  - "Não usar GUE, zeros ou dados definidos pelos próprios zeros como premissa"
  - "Não citar preprints não auditados como resultado estabelecido"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "03_MILLENNIUM/01_RIEMANN/README.md"
  - "03_MILLENNIUM/01_RIEMANN/ASYMPTOTIC_CORE.md"
  - "03_MILLENNIUM/01_RIEMANN/STOP_CONDITIONS.md"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

A especificação de `RH-NOGO-001` está pronta (`SPECIFICATION_READY`) e
bibliograficamente auditada. Nenhuma prova foi executada, nenhum operador
foi construído e nada foi afirmado sobre a verdade ou falsidade da
Hipótese de Riemann.

O alvo especificado exclui **uma classe convencional delimitada** (Classe W:
operadores diferenciais elípticos auto-adjuntos positivos de ordem fixa em
variedades compactas fechadas), pela incompatibilidade entre a contagem
`T log T` de Riemann–von Mangoldt e a lei de potência de Weyl. Ele **não**
exclui Hilbert–Pólya: 14 rotas de escape estão mapeadas em
`03_MILLENNIUM/01_RIEMANN/ESCAPE_ROUTES.md`.

## Work items

| Item | Estado | Evidência |
|---|---|---|
| LAB-ARCH-001 | VERIFIED | governança e labctl |
| LAB-BENCH-001 | VERIFIED | lab-bench-001-result.json |
| FOUND-SEMIGROUP-001 | VERIFIED | found-semigroup-001-result.json |
| RH-NOGO-001 | SCOPED, especificação pronta | rh-nogo-001-specification-result.json |

## Frente ativa

`RH-NOGO-001` permanece `SCOPED`, `NOT_AUTHORIZED`, `NO_EXECUTION`. A única
autorização vigente é a formalização do **núcleo abstrato**
`ASYM-NOGO-001` — um lema de análise real sem zeta, sem PDE e sem π:

```text
Não existe N : ℝ → ℝ com N(T)/(T log T) → c > 0 e N(T)/T^α → C > 0, α > 0.
```

Assinatura registrada e compilando em
`05_FORMAL/lean/TamesisLab/RHNogo/SignatureProbe.lean` (sem corpo
probatório). Viabilidade Mathlib verificada em `LEAN_FEASIBILITY.md`.

## Runtime

Ubuntu 24.04/WSL2; Lean `v4.33.0-rc1`; Mathlib
`79d0395a1825a6264ad5d269e35e60537518955e`. Detalhes em
`05_FORMAL/LEAN_ENVIRONMENT.md`.

## Próxima ação única

Formalizar somente o lema abstrato de incompatibilidade assintótica
(ASYM-NOGO-001), sem formalizar PDE, lei de Weyl ou construir operador
espectral.

## Ações proibidas

- executar a prova do no-go completo ou qualquer frente Clay;
- construir operador espectral;
- declarar refutação de Hilbert–Pólya ou progresso sobre a RH;
- usar GUE, zeros ou dados definidos pelos próprios zeros como premissa;
- citar preprints não auditados como resultados estabelecidos;
- alterar arquivos fora de `04_FORMAL_RESEARCH_LAB/`;
- usar sorry, admit, axioma local ou unsafe.

## Histórico recente

- 2026-07-31: LAB-WSL-MIGRATION migrou o runtime canônico para WSL2.
- 2026-07-31: LAB-BENCH-001 verificado.
- 2026-07-31: FOUND-SEMIGROUP-001 verificado (modelo C3).
- 2026-07-31: RH-NOGO-001 especificado e auditado
  (`RH_NOGO_001_SPECIFICATION_READY`); prova não autorizada.
