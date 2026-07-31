---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T07:13:16-03:00
canonical_commit: "16427b420aa6e5e89c39d169172ff1c2c3add142"
canonical_commit_policy: "aponta para o commit finalizado do gate; a atualização deste campo ocorre no commit de fechamento seguinte"
repository_clean: true
active_track: "millennium"
active_work_item: "RH-NOGO-001"
work_status: "SCOPED"
evidence_level: "F"
last_verified_artifact: "rh-nogo-additional-source-result.json"
current_blocker: "A ponte documental está preparada, mas sua aplicação formal ao no-go espectral ainda não foi autorizada."
next_single_action: "Especificar a ponte formal entre W-ELLIPTIC, W-POWER e ASYM-NOGO-001 sem iniciar a prova completa do no-go espectral."
authorized_action: "RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_AUTHORIZED"
prohibited_actions:
  - "Não executar a prova do no-go completo (RH_NOGO_PROOF_EXECUTION não autorizado)"
  - "Não aplicar ASYM-NOGO-001 a nenhum operador"
  - "Não formalizar PDE, lei de Weyl ou teoria espectral em Lean"
  - "Não construir operador espectral algum"
  - "Não citar Hörmander 1968 pela lei de Weyl global — apenas pelo resultado local"
  - "Não citar monografias não obtidas (Safarov–Vassiliev, Shubin, Ivrii) como fonte de enunciado"
  - "Não usar a fórmula escalar da constante para sistemas ou fibrados"
  - "Não declarar que Hilbert–Pólya foi refutado"
  - "Não declarar progresso sobre a verdade ou falsidade da Hipótese de Riemann"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/W_POWER_CLASS.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/W_ELLIPTIC_CLASS.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/HORMANDER_LOCAL_TO_GLOBAL_BRIDGE.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/CLASS_W_V2_DECISION.md"
  - "03_MILLENNIUM/01_RIEMANN/STOP_CONDITIONS.md"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

A arquitetura da frente foi separada em duas classes, e a ponte
local → global está **documentada etapa a etapa**. `RH-NOGO-001` permanece
`SCOPED`: nenhuma prova foi executada, nenhum operador construído,
`ASYM-NOGO-001` não foi aplicado.

## Arquitetura

```text
        ASYM-NOGO-001      VERIFIED em Lean
              ↑
          W-POWER          classe abstrata; nenhuma EDP
              ↑
     GLOBAL-WEYL-BRIDGE    documentada, NÃO formalizada
              ↑
        W-ELLIPTIC v2      pseudodiferencial clássico, positivo,
                           auto-adjunto, ordem m > 0, M compacta
```

A interface `W-POWER` isola o núcleo formal já verificado: qualquer
estreitamento futuro da classe geométrica **não** afeta `ASYM-NOGO-001`.

## Fontes desta rodada

Obtidas por acesso público (arXiv): **Ivrii 2016** (*100 years of Weyl's
law*, 90 pp.) e **Coriasco–Doll 2020** (*Weyl Law on Asymptotically
Euclidean Manifolds*, 26 pp.).

Não obtidas: **Safarov–Vassiliev**, **Shubin** e a **monografia de Ivrii** —
monografias comerciais; nenhuma tentativa de burlar acesso. As **provas** da
lei global permanecem em textos não lidos.

## Achado bibliográfico

Coriasco–Doll atribuem a lei de Weyl **global** a *"Hörmander [15]"*, com
`[15] = Acta Math. 121 (1968), 193–218` — o artigo que a auditoria anterior
mostrou conter apenas a lei **local**. A atribuição é matematicamente
defensável e bibliograficamente imprecisa.

**Regra de citação adotada:** Hörmander 1968 é citado pelo resultado
**local** (eq. 5.3); a lei **global** é citada por Coriasco–Doll ou Ivrii,
ou derivada pela ponte explícita.

## Decisões registradas

| Questão | Decisão |
|---|---|
| Classe | `REFORMULATE_AS_CLASSICAL_PSEUDODIFFERENTIAL` |
| Ordem | `PSEUDODIFFERENTIAL_POSITIVE_ORDER` (`m > 0` real; paridade eliminada) |
| Auto-adjunção | `positive_self_adjoint_operator` (uma realização, não essencial auto-adjunção) |

`GAP-RH-010` e `GAP-RH-011` fechados **por reformulação**, não por prova.

## O que permanece aberto

- `GAP-RH-009` — fibrados/sistemas: `W-ELLIPTIC` v2 é escalar por omissão.
- `GAP-RH-012` — discretude: sustentada por analogia com o argumento SG de
  Coriasco–Doll, não por fonte para variedades compactas.
- `GAP-RH-014` — positividade de `C_P`: corolário elementar registrado, não
  citado.
- Bordo: nenhuma fonte diz literalmente "closed manifold" para a forma
  pseudodiferencial.

## Work items

| Item | Estado |
|---|---|
| LAB-ARCH-001 | VERIFIED |
| LAB-BENCH-001 | VERIFIED |
| FOUND-SEMIGROUP-001 | VERIFIED |
| RH-NOGO-001 | SCOPED; `ASYM-NOGO-001` VERIFIED; ponte DOCUMENTADA |

## Próxima ação única

Especificar a ponte formal entre W-ELLIPTIC, W-POWER e ASYM-NOGO-001 sem
iniciar a prova completa do no-go espectral.

## Ações proibidas

- executar a prova do no-go ou aplicar `ASYM-NOGO-001`;
- formalizar PDE, lei de Weyl ou teoria espectral;
- construir operador espectral;
- citar Hörmander 1968 pela lei global;
- citar monografias não obtidas como fonte de enunciado;
- usar a fórmula escalar da constante para sistemas;
- declarar refutação de Hilbert–Pólya ou progresso sobre a RH;
- alterar arquivos fora de `04_FORMAL_RESEARCH_LAB/`.

## Histórico recente

- 2026-07-31: migração para WSL2; LAB-BENCH-001; FOUND-SEMIGROUP-001.
- 2026-07-31: RH-NOGO-001 especificado; `ASYM-NOGO-001` verificado em Lean.
- 2026-07-31: auditoria de fontes primárias —
  `PRIMARY_SOURCES_PARTIALLY_SUFFICIENT`; descoberto que Hörmander 1968
  não enuncia a lei global.
- 2026-07-31: recuperação adicional e reformulação —
  `LOCAL_TO_GLOBAL_BRIDGE_SUFFICIENT`; classes separadas; nenhuma claim
  promovida.
