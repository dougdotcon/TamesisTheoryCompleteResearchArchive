---
session_id: 2026-07-31_0537_RH-NOGO-001-SPECIFICATION
started_at: 2026-07-31T05:00:00-03:00
ended_at: 2026-07-31T05:37:29-03:00
agent: claude-fable-5
git_commit_before: a961eb6060d0b880c3452f179e094c94092df6b1
git_commit_after: null
active_work_item: RH-NOGO-001
authorized_action: RH_NOGO_SPECIFICATION_PREPARATION_AUTHORIZED
result_status: RH_NOGO_001_SPECIFICATION_READY
files_created:
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/OPERATOR_CLASS.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/ASYMPTOTIC_CORE.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/EXCLUSIONS.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/ESCAPE_ROUTES.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/BIBLIOGRAPHY_AUDIT.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/CLAIM_MATRIX.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/LEAN_FEASIBILITY.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/STOP_CONDITIONS.md"
  - "04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/TamesisLab/RHNogo/SignatureProbe.lean"
  - "04_FORMAL_RESEARCH_LAB/rh-nogo-001-specification-result.json"
  - "04_FORMAL_RESEARCH_LAB/09_SESSIONS/2026/2026-07-31_0537_RH-NOGO-001-SPECIFICATION.md"
files_modified:
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/README.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/STATUS.yaml"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/TARGET_RESULT.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/DEFINITIONS.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/ASSUMPTIONS.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/KNOWN_RESULTS_MATRIX.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/LEAN_MAP.md"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/DEPENDENCY_DAG.yaml"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/GAP_REGISTER.yaml"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/PROOF_SKETCH.md"
  - "04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/TamesisLab.lean"
  - "04_FORMAL_RESEARCH_LAB/01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "04_FORMAL_RESEARCH_LAB/10_TOOLS/labctl.py"
  - "04_FORMAL_RESEARCH_LAB/LAB_STATE.md"
  - "04_FORMAL_RESEARCH_LAB/CHANGELOG.md"
commands_executed:
  - "git rev-parse HEAD / git status --short"
  - "python3 10_TOOLS/labctl.py status / validate"
  - "grep na Mathlib fixada (Asymptotics, log, rpow)"
  - "WebSearch: confirmacao de listagem do preprint Hedenmalm 2026"
  - "lake env lean TamesisLab/RHNogo/SignatureProbe.lean"
  - "lake build"
  - "grep tokens proibidos"
  - "python3 -m pytest (em 06_COMPUTATION/python)"
tests_executed:
  - "SignatureProbe isolado: exit 0"
  - "lake build: exit 0, 8684 jobs"
  - "tokens proibidos: 0/0/0/0"
  - "pytest: 2 passed"
  - "labctl validate: PASS"
claims_changed: []
gaps_opened:
  - "GAP-RH-001..008 (registro novo, substituindo RH-GAP-001..003)"
gaps_closed:
  - "GAP-RH-006 (dependencia da RH): resolvido como INDEPENDENTE"
  - "GAP-RH-004 (ferramentas Mathlib): VERIFIED_AVAILABLE"
next_single_action: "Formalizar somente o lema abstrato de incompatibilidade assintotica (ASYM-NOGO-001), sem formalizar PDE, lei de Weyl ou construir operador espectral."
---

## Objetivo autorizado

Preparar especificacao rigorosa e auditoria bibliografica para RH-NOGO-001,
sem iniciar prova, sem formalizar o resultado principal e sem experimentacao
destinada a demonstra-lo.

## Estado inicial verificado

HEAD `a961eb6060d0b880c3452f179e094c94092df6b1`, working tree limpo,
`labctl validate` PASS, `active_work_item: RH-NOGO-001`,
`authorized_action: RH_NOGO_SPECIFICATION_PREPARATION_AUTHORIZED`,
`RH-NOGO-001` em `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.

Decisao de caminho canonico: a frente ja existia em
`03_MILLENNIUM/01_RIEMANN/` com 11 arquivos placeholder. Usei o caminho
existente e **nao** criei `03_MILLENNIUM/RH_NOGO/`, conforme a instrucao de
nao duplicar a frente.

## Alvo especificado

Classe W (W1-W8): operador diferencial eliptico classico, ordem inteira fixa
`m >= 1`, auto-adjunto, positivo, sobre fibrado hermitiano em variedade
riemanniana suave compacta sem bordo de dimensao `d` finita, com espectro
discreto e lei de Weyl `N_P(L) ~ C_P L^(d/m)`.

Exclusao em tres niveis: igualdade exata de multiconjuntos, discrepancia
`O(1)`, e equivalencia assintotica de densidade. O nivel mais fraco (iii) ja
contradiz o nucleo, e os outros dois o implicam.

Fundamento: `N_zeta(T)/(T log T) -> 1/(2pi)` (Riemann-von Mangoldt,
incondicional) contra `N_P(T)/T^alpha -> C_P > 0` (Weyl).

## Nucleo abstrato ASYM-NOGO-001

Sublema independente de PDE, de zeta e de pi:

> Nao existe `N : R -> R` com `N(T)/(T log T) -> c > 0` e
> `N(T)/T^alpha -> C > 0` para `alpha > 0` fixo.

Analise de casos completa (`alpha < 1`, `= 1`, `> 1`) reduzida a um unico
fato: `log T * T^(1-alpha)` diverge ou tende a zero, nunca a limite finito
positivo. Assinatura Lean registrada como `Prop` **sem corpo probatorio** em
`TamesisLab/RHNogo/SignatureProbe.lean`, que compila.

## Auditoria bibliografica

Oito fontes classificadas com `publication_type`, `peer_reviewed`,
`primary_or_secondary`, `claim_supported`, `assumptions`, `relevance`,
`inside/outside_operator_class` e `limitations`. Dois pilares ESTABLISHED
(von Mangoldt 1905 para a contagem; Hormander 1968 para Weyl), a descricao
oficial do Clay para o enunciado da RH, e quatro rotas fora da classe
(Berry-Keating, Connes, Bender-Brody-Muller, Hedenmalm).

Honestidade de verificacao: distingui `KNOWN_RECORD` (registro
bibliografico conhecido, conteudo nao rebaixado nesta sessao),
`LISTING_CONFIRMED` (existencia confirmada em listagem publica hoje) e
`TO_FETCH`. O preprint Hedenmalm 2026 teve **apenas a existencia**
confirmada; nao li o conteudo e ele nao sustenta nenhuma afirmacao aqui —
entra somente em `CLAIMS_REQUIRING_INDEPENDENT_AUDIT`.

## Auditoria de circularidade

Sem risco nesta rota: nao ha formula de traco, nao se usa GUE nem
Montgomery-Odlyzko, e nenhum operador e construido a partir dos zeros. O
enunciado e incondicional — nao depende da RH (GAP-RH-006 resolvido).

## Rotas de escape

Catorze rotas mapeadas em `ESCAPE_ROUTES.md`. Todas as propostas
espectrais vivas da literatura caem em alguma delas, o que impede a leitura
do resultado como refutacao de Hilbert-Polya.

## Novidade

`GAP-RH-007` aberto e explicito: a observacao de que a contagem `T log T`
nao e uma lei de potencia de Weyl e **folclore da area**, discutida ao menos
desde Berry-Keating 1999. O enunciado nao deve ser apresentado como novo em
matematica. O valor esta na precisao da classe, na delimitacao e na
formalizacao futura.

## Decisao

**A — SPECIFICATION_READY**, com a ressalva de que `GAP-RH-002` (transcricao
da versao exata da lei de Weyl de Hormander 1968) bloqueia a prova do
resultado completo, mas nao o nucleo abstrato, que e independente de PDE.

Nao forcei a opcao A: ela se sustenta porque o unico passo autorizado a
seguir (formalizar ASYM-NOGO-001) nao depende de nenhum gap aberto.

## Falha registrada

Primeira tentativa do probe falhou: `Real.isLittleO_log_rpow_atTop`
inexistente (`unknownIdentifier`) — o lema vive no namespace raiz. Corrigido
para `isLittleO_log_rpow_atTop`; probe passou a compilar. Registrado em
`LEAN_FEASIBILITY.md`. Este e exatamente o tipo de erro que o probe existe
para capturar antes da prova.

## Desvio do gate reportado ao mantenedor

O gate pedia `work_status: READY` para RH-NOGO-001. O `labctl` impoe
`RH-NOGO-001 must remain SCOPED` — o guardrail que mantem a frente Clay
fechada. Mantive `SCOPED` e **nao** enfraqueci esse guardrail; acrescentei
apenas a entrada literal `RH_NOGO_ASYMPTOTIC_LEMMA_FORMALIZATION_AUTHORIZED`
ao allowlist, como instruido. A substancia do estado alvo esta preservada
(`authorized_action`, `specification_status: SPECIFICATION_READY`,
`next_single_action`). A decisao de mudar ou nao o guardrail cabe ao
mantenedor.

## O que nao foi feito

- Nenhuma prova, nenhum operador construido, nenhuma experimentacao.
- `RH_NOGO_PROOF_EXECUTION` nao autorizado; nenhuma variante de
  `RH_PROOF_AUTHORIZED` acrescentada.
- Nenhuma claim cientifica criada ou promovida.
- Nenhum arquivo fora de `04_FORMAL_RESEARCH_LAB/` modificado.
- Nenhum preprint usado como autoridade.

## Handoff

> Excluimos, no maximo, uma classe convencional delimitada;
> **nao excluimos Hilbert-Polya** e nao afirmamos nada sobre a verdade ou
> falsidade da Hipotese de Riemann.

O proximo gate pode formalizar somente `ASYM-NOGO-001`.
