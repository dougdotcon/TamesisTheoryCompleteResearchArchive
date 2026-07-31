---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T08:20:30-03:00
canonical_commit: "0d52d375fc72741ea60c8e4c2a4cb9d14c90e5a6"
canonical_commit_policy: "aponta para o commit finalizado do gate; a atualização deste campo ocorre no commit de fechamento seguinte"
repository_clean: true
active_track: "millennium"
active_work_item: "RH-NOGO-001"
work_status: "SCOPED"
evidence_level: "F"
last_verified_artifact: "rh-nogo-source-bridge-specification-result.json"
current_blocker: "Somente o segmento abstrato (W-POWER + TLOG + E2) está ao alcance de formalização; os ramos geométrico e aritmético permanecem documentais."
next_single_action: "Formalizar somente as interfaces W-POWER/TLOG e o COUNTING-LAW-BRIDGE para discrepâncias o(T log T), sem formalizar operadores, lei de Weyl ou Riemann–von Mangoldt."
authorized_action: "RH_NOGO_COUNTING_BRIDGE_FORMALIZATION_AUTHORIZED"
prohibited_actions:
  - "Não executar a prova do no-go completo (RH_NOGO_PROOF_EXECUTION não autorizado)"
  - "Não aplicar ASYM-NOGO-001 a nenhum operador"
  - "Não formalizar operadores pseudodiferenciais, lei de Weyl ou Riemann–von Mangoldt"
  - "Não quantificar sobre todas as realizações auto-adjuntas de uma expressão formal"
  - "Não estender do caso escalar para sistemas ou fibrados"
  - "Não estender do caso sem bordo para problemas de bordo"
  - "Não citar Hörmander 1968 pela lei de Weyl global — apenas pelo resultado local"
  - "Não usar a fórmula escalar da constante para sistemas"
  - "Não declarar que Hilbert–Pólya foi refutado"
  - "Não declarar progresso sobre a verdade ou falsidade da Hipótese de Riemann"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "03_MILLENNIUM/01_RIEMANN/SOURCE_BRIDGE_SPECIFICATION.md"
  - "03_MILLENNIUM/01_RIEMANN/W_ELLIPTIC_SCALAR_V2.md"
  - "03_MILLENNIUM/01_RIEMANN/COUNTING_LAW_BRIDGE_SPEC.md"
  - "03_MILLENNIUM/01_RIEMANN/SOURCE_BRIDGE_DEPENDENCY_DAG.yaml"
  - "03_MILLENNIUM/01_RIEMANN/STOP_CONDITIONS.md"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

A ponte lógica está **especificada**. Nenhuma obrigação foi provada,
`ASYM-NOGO-001` não foi aplicado e nenhum operador foi construído.

## Arquitetura

```text
W-ELLIPTIC-SCALAR                     classe geométrica estreita
        ↓ GLOBAL-WEYL-BRIDGE-SCALAR   9 obrigações GWB-001..009
W-POWER                               interface assintótica abstrata
        ↓ COUNTING-LAW-BRIDGE         o(T log T) ⟹ mesma lei T log T
ASYM-NOGO-001                         VERIFIED em Lean
```

`W-POWER` não menciona operadores. Qualquer estreitamento futuro de
`W-ELLIPTIC-SCALAR` deixa o núcleo verificado intacto.

## Mudança central

O alvo **deixou de ser** igualdade espectral exata. A relação central é

```text
N_P(T) − N_ζ(T) = o(T log T)          (nível E2)
```

que cobre igualdade exata, igualdade eventual, discrepância `O(1)` e
equivalência por razão. Alvo estreito **e** mais robusto.

## Estreitamentos deliberados desta v2

| Exclusão | Motivo |
|---|---|
| **bordo** | evitar importar problemas elípticos de bordo não auditados; nenhuma fonte diz literalmente "closed manifold" para a forma pseudodiferencial |
| **sistemas e fibrados** | a constante de Ivrii usa `n(x,ξ)` com multiplicidades e a identidade de traço fibrada não foi auditada; `GAP-RH-009` **não foi fechado**, foi contornado |

## Regra de quantificação

Correta: *"para todo operador **realizado** `P` que satisfaça
**individualmente** as hipóteses de `W-ELLIPTIC-SCALAR`"*.

Proibida: *"para todas as realizações auto-adjuntas de uma expressão
formal"* — incluiria realizações fora da classe pseudodiferencial auditada.

## Estado da formalização

| Objeto | Estado |
|---|---|
| `ASYM-NOGO-001` | **VERIFIED** |
| `Bridge/SignatureProbe.lean` | assinaturas elaboradas, **sem provas** |
| `COUNTING-LAW-BRIDGE` | especificado; formalização autorizada no próximo gate |
| `GLOBAL-WEYL-BRIDGE-SCALAR` | documental; não formalizável agora |
| `RVM-LIMIT` | documental; exigiria formalizar `ζ` |

`lake build` PASS com 8.692 jobs; tokens proibidos zero.

## Lacunas bloqueantes

- `SB-GAP-001` / `GAP-RH-014`: **`C_P > 0` não é afirmado por nenhuma fonte
  obtida**. Sem ele a pertinência a `W-POWER` falha.
- `SB-GAP-002` / `GAP-RH-012`: discretude é hipótese **incorporada**, não
  derivada.
- `SB-GAP-003`: convenções de fronteira (`<` versus `≤`) não reconciliadas
  por escrito.

## Evidência canônica

A identidade local→global de Ivrii, eq. (3.1.11), não pôde ser verificada
independentemente por fontes públicas externas. A cópia preservada em
`08_REVIEWS/SOURCES/RH_NOGO/pdf/ivrii_2016_100years_weyl.pdf`
(`sha256 9ca07737…`) é a evidência canônica.

## Próxima ação única

Formalizar somente as interfaces W-POWER/TLOG e o COUNTING-LAW-BRIDGE para
discrepâncias `o(T log T)`, sem formalizar operadores, lei de Weyl ou
Riemann–von Mangoldt.

## Histórico recente

- 2026-07-31: migração WSL2; LAB-BENCH-001; FOUND-SEMIGROUP-001.
- 2026-07-31: RH-NOGO-001 especificado; `ASYM-NOGO-001` verificado.
- 2026-07-31: auditoria de fontes primárias — descoberto que Hörmander 1968
  não enuncia a lei global.
- 2026-07-31: recuperação adicional — classes separadas; ponte documentada.
- 2026-07-31: ponte **especificada** (`SOURCE_BRIDGE_SPECIFICATION_READY`);
  alvo migrado de igualdade exata para `o(T log T)`; bordo e sistemas
  excluídos; nenhuma claim promovida.
