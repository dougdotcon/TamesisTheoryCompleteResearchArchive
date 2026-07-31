---
session_id: 2026-07-31_0820_RH-NOGO-SOURCE-BRIDGE-SPECIFICATION
started_at: 2026-07-31T07:50:00-03:00
ended_at: 2026-07-31T08:20:30-03:00
agent: claude-opus-5
git_commit_before: 0d52d375fc72741ea60c8e4c2a4cb9d14c90e5a6
git_commit_after: null
active_work_item: RH-NOGO-001
authorized_action: RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_AUTHORIZED
result_status: RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_READY
files_created:
  - "03_MILLENNIUM/01_RIEMANN/SOURCE_BRIDGE_SPECIFICATION.md"
  - "03_MILLENNIUM/01_RIEMANN/W_ELLIPTIC_SCALAR_V2.md"
  - "03_MILLENNIUM/01_RIEMANN/W_ELLIPTIC_SYSTEM_DEFERRED.md"
  - "03_MILLENNIUM/01_RIEMANN/GLOBAL_WEYL_BRIDGE_OBLIGATIONS.md"
  - "03_MILLENNIUM/01_RIEMANN/RVM_LIMIT_BRIDGE.md"
  - "03_MILLENNIUM/01_RIEMANN/COUNTING_LAW_RELATIONS.md"
  - "03_MILLENNIUM/01_RIEMANN/COUNTING_LAW_BRIDGE_SPEC.md"
  - "03_MILLENNIUM/01_RIEMANN/NARROW_NOGO_STATEMENT.md"
  - "03_MILLENNIUM/01_RIEMANN/SPECTRAL_MATCH_CONVENTIONS.md"
  - "03_MILLENNIUM/01_RIEMANN/SOURCE_BRIDGE_DEPENDENCY_DAG.yaml"
  - "03_MILLENNIUM/01_RIEMANN/SOURCE_BRIDGE_GAP_REGISTER.yaml"
  - "03_MILLENNIUM/01_RIEMANN/SOURCE_BRIDGE_LEAN_FEASIBILITY.md"
  - "05_FORMAL/lean/TamesisLab/RHNogo/Bridge/SignatureProbe.lean"
  - "rh-nogo-source-bridge-specification-result.json"
  - "09_SESSIONS/2026/2026-07-31_0820_RH-NOGO-SOURCE-BRIDGE-SPECIFICATION.md"
files_modified:
  - "05_FORMAL/lean/TamesisLab.lean"
  - "03_MILLENNIUM/01_RIEMANN/STATUS.yaml"
  - "03_MILLENNIUM/01_RIEMANN/LEAN_MAP.md"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "10_TOOLS/labctl.py"
  - "LAB_STATE.md"
  - "CHANGELOG.md"
tests_executed:
  - "lake env lean Bridge/SignatureProbe.lean: exit 0"
  - "lake build: PASS, 8692 jobs"
  - "tokens proibidos: 0/0/0/0"
  - "pytest: 2 passed"
  - "labctl validate: PASS, errors []"
claims_changed: []
gaps_opened: ["SB-GAP-001 a SB-GAP-010"]
gaps_closed: []
next_single_action: "Formalizar somente as interfaces W-POWER/TLOG e o COUNTING-LAW-BRIDGE para discrepâncias o(T log T), sem formalizar operadores, lei de Weyl ou Riemann–von Mangoldt."
---

## Objetivo autorizado

Especificar, **sem provar**, a arquitetura
`W-ELLIPTIC-SCALAR → W-POWER → ASYM-NOGO-001`.

## Decisão

**A — `SOURCE_BRIDGE_SPECIFICATION_READY`.** Os oito requisitos de `READY`
estão satisfeitos: `W-POWER` definida; `W-ELLIPTIC-SCALAR` definida;
sistemas e bordo excluídos; obrigações global-Weyl enumeradas (GWB-001..009);
`RVM-LIMIT` especificada; relações E0–E3 especificadas; `COUNTING-LAW-BRIDGE`
especificada; conclusão estreita delimitada; **nenhuma prova executada**.

## Os três ajustes que você pediu

**1. Quantificação.** Distingui explicitamente quatro objetos — operador
formal, domínio, realização auto-adjunta, operador realizado `P` — e fixei
que a classe é propriedade do **quarto**. A forma
*"para todas as realizações auto-adjuntas de uma expressão formal"* está
**proibida** em `W_ELLIPTIC_SCALAR_V2.md`, porque incluiria realizações que
não satisfazem a classe pseudodiferencial auditada, e nenhuma fonte garante
que toda realização de um `p` fixo permaneça na classe.

**2. `W-ELLIPTIC-SCALAR`.** Bordo e fibrados/sistemas **excluídos**.
`GAP-RH-009` **não foi fechado** — foi contornado por estreitamento, e isso
está registrado como tal em `SB-GAP-006`. A classe adiada vive em
`W_ELLIPTIC_SYSTEM_DEFERRED.md`, inativa.

**3. Relação central `o(T log T)`.** É agora o nível E2, e o
`COUNTING-LAW-BRIDGE` é enunciado uma única vez sobre ele, cobrindo E0, E1,
E2 e E3 de uma vez. Criar um lema por nível multiplicaria a superfície de
prova sem ganho.

## Ponte central

```text
Se  N_ζ(T)/(T log T) → c > 0
e   N_P(T) − N_ζ(T) = o(T log T),
então N_P(T)/(T log T) → c.
```

Esboço registrado (não é prova): a diferença dividida por `T log T` tende a
zero por definição de `o`, e a soma dos limites dá `c`. Complexidade
estimada **baixa** — mesma forma da `eventually_normalization_identity` já
verificada, sem `ζ`, sem operadores, sem `π`.

## Obrigações GLOBAL-WEYL

Nove obrigações com fonte e estado. Apenas **GWB-005** (assíntota local
uniforme) é `SOURCE_DIRECT` — leitura direta de Hörmander (5.3). Quatro são
`SOURCE_CITED_RESULT`, duas são `ELEMENTARY_COROLLARY`, uma é hipótese
incorporada (GWB-001) e uma é **bloqueante**:

**GWB-008 (`C_P > 0`) não é afirmado por nenhuma fonte obtida.** Sem ele a
pertinência a `W-POWER` falha, pois `W-POWER` exige constante positiva.
Registrado como `SB-GAP-001`, severidade alta.

Observação que reduz o requisito: Ivrii 3.1.1(iv) diz que a assintótica de
**um termo** vale sem hipótese de não degenerescência. Como `W-POWER` só
precisa de um termo, micro-hiperbolicidade e não periodicidade **não são
necessárias**.

## Convenções espectrais

Sete obrigações em `SPECTRAL_MATCH_CONVENTIONS.md`. Duas permanecem
`UNRESOLVED_CONVENTION_MISMATCH`: `N_P` usa desigualdade **estrita**
(Coriasco–Doll eq. 1), `N_ζ` moderna usa `≤ T`, e von Mangoldt evita o
problema escolhendo `T` fora de zeros. A reconciliação é elementar mas não
está escrita.

Registrei também que deslocamentos constantes são **absorvidos por E2** —
uma das vantagens de abandonar a igualdade exata — e que a implicação
`E2 ⟹ igualdade espectral` é **falsa** e nunca deve ser usada.

## Lean

`Bridge/SignatureProbe.lean` com oito assinaturas elaboradas, `#check` das
ferramentas Mathlib previstas, `set_option autoImplicit false` e **nenhuma
prova**. `lake build` PASS com 8.692 jobs; tokens proibidos zero;
`ASYM-NOGO-001` **não** aplicado.

Nota de projeto: `PowerCountingLaw` e `TLogCountingLaw` elaboram em `Type`,
não `Prop`, porque carregam dados (`exponent`, `constant`) — corresponde à
definição de `W-POWER` como tripla mais suposições.

## Evidência canônica

Registrei que a identidade de Ivrii (3.1.11) não pôde ser verificada
independentemente por fontes públicas externas e que **a cópia preservada
neste laboratório (`sha256 9ca07737…`, 90 pp.) é a evidência canônica**.

## O que não foi feito

- Nenhuma obrigação provada; nenhuma seta do DAG demonstrada.
- `ASYM-NOGO-001` **não** aplicado.
- Operadores, lei de Weyl e Riemann–von Mangoldt **não** formalizados.
- Nenhum operador construído ou excluído.
- Nenhuma extrapolação de escalar para sistemas, nem de sem-bordo para
  bordo.
- Hilbert–Pólya **não** excluído; nenhuma afirmação sobre a RH.
- Nenhuma claim criada ou promovida; legado intocado.

## Handoff

Só o segmento abstrato está ao alcance de formalização:
`W-POWER + TLOG + E2 ⟹ contradição`. Os dois ramos que ligam esse segmento
à matemática real — `GLOBAL-WEYL-BRIDGE-SCALAR` e `RVM-LIMIT` — permanecem
documentais, e o segundo provavelmente ficará fora de alcance por muito
tempo (`SB-GAP-010`). O próximo gate formaliza a ponte de contagem e nada
mais.
