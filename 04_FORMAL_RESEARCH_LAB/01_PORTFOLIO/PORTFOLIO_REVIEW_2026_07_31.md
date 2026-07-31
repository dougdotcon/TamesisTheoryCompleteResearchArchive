---
document_id: PORTFOLIO-REVIEW-2026-07-31
gate: PORTFOLIO_REVIEW
authorized_action: PORTFOLIO_REVIEW_AUTHORIZED
reviewed_commit: 3f72ad0cf19e523f5b714d2d078cd71f3e44c46f
decision: A_PORTFOLIO_REVIEW_APPROVED_FUNCTIONAL_GRAPH_SELECTED
---

# Revisão de portfólio — 2026-07-31

## Situação de partida

```text
LAB-ARCH-001          VERIFIED
LAB-BENCH-001         VERIFIED
FOUND-SEMIGROUP-001   VERIFIED
FOUND-SEMIGROUP-002   VERIFIED / result_review APPROVED / extension NOT_AUTHORIZED
RH-NOGO-001           FROZEN_PARTIAL_RESULT
```

Nenhuma frente ativa. Seis itens `SCOPED` na fila, todos herdados do
planejamento original de 2026-07-28.

## Auditoria dos itens existentes

Nenhuma pesquisa matemática foi executada sobre estes itens. A avaliação é
de **portfólio**: custo, prontidão de infraestrutura e risco.

```yaml
- work_item: NS-PRESSURE-001
  title: "Auditoria do lema de pressão–alinhamento"
  scientific_value: MODERATE
  formalization_cost: HIGH
  mathlib_readiness: LOW
  dependency_risk: HIGH
  counterexample_access: MEDIUM
  poc_30_day_feasibility: NO
  reason_not_selected: >
    Análise de EDP e fluidos. A Mathlib não oferece infraestrutura pronta
    para o argumento; seria o mesmo tipo de compromisso de longo prazo que
    levou ao congelamento de RH-NOGO-001.

- work_item: PVSNP-PHYS-001
  title: "Separação entre complexidade física e clássica"
  scientific_value: MODERATE
  formalization_cost: MEDIUM
  mathlib_readiness: MEDIUM
  dependency_risk: HIGH
  counterexample_access: HIGH
  poc_30_day_feasibility: PARTIAL
  reason_not_selected: >
    É o mais viável dos seis, e o custo de formalização é apenas médio.
    Foi descartado por dois motivos: o risco de dependência é alto
    (definir P_phys/NP_phys exige um modelo de computação física cuja
    escolha é ela própria a parte contenciosa), e a frente vizinha a uma
    conjectura Clay logo após congelar outra seria um erro de portfólio.

- work_item: YM-LIMIT-001
  title: "Preservação ou perda do gap em limites"
  scientific_value: MODERATE
  formalization_cost: VERY_HIGH
  mathlib_readiness: NONE
  dependency_risk: VERY_HIGH
  counterexample_access: MEDIUM
  poc_30_day_feasibility: NO
  reason_not_selected: >
    Teoria quântica de campos construtiva. Custo de formalização e custo
    bibliográfico ambos `very_high` na própria fila.

- work_item: HODGE-CDK-001
  title: "Auditoria da inferência entre loci e ciclos"
  scientific_value: MODERATE
  formalization_cost: HIGH
  mathlib_readiness: LOW
  dependency_risk: HIGH
  counterexample_access: MEDIUM
  poc_30_day_feasibility: NO
  reason_not_selected: >
    Geometria algébrica com custo bibliográfico `very_high`. O laboratório
    não possui as fontes primárias auditadas.

- work_item: BSD-HYP-MATRIX-001
  title: "Matriz formal de hipóteses e casos cobertos"
  scientific_value: MODERATE
  formalization_cost: HIGH
  mathlib_readiness: LOW
  dependency_risk: HIGH
  counterexample_access: MEDIUM
  poc_30_day_feasibility: NO
  reason_not_selected: >
    O produto seria sobretudo bibliográfico, e o custo bibliográfico é
    `very_high`. A experiência de RH-NOGO-001 mostrou que auditoria de
    fontes sem acesso às provas produz registro, não resultado.

- work_item: TOE-INTERFACE-001
  title: "Teoria formal de interfaces entre regimes"
  scientific_value: LOW
  formalization_cost: VERY_HIGH
  mathlib_readiness: NONE
  dependency_risk: BLOCKING
  counterexample_access: MEDIUM
  poc_30_day_feasibility: NO
  reason_not_selected: >
    Depende formalmente de RH-NOGO-001, que está congelado — a dependência
    é bloqueante, não apenas custosa. Além disso é a frente de síntese
    TOE, cujo vocabulário este laboratório restringiu repetidamente.
```

### Constatação

Nenhum dos seis satisfaz simultaneamente **infraestrutura Mathlib pronta**,
**acesso alto a contraexemplos** e **PoC em 30 dias** — que são exatamente
os critérios que fizeram `FOUND-SEMIGROUP-002` funcionar. É a mesma
constatação da revisão anterior, agora com um item novo já selecionado em
vez de improvisado.

## Alvo selecionado

```yaml
work_item_id: FOUND-FUNCTIONAL-GRAPH-001
title: "Finite Functional Graph Decomposition"
track: foundations
status: SCOPED
duplicate_found: false
```

Busca por `functional graph` / `grafo funcional` / `FUNCTIONAL_GRAPH` em
todos os `.yaml` e `.md` do laboratório: **zero ocorrências**. Nenhuma
duplicata; item genuinamente novo.

## Justificativa

Reutiliza **diretamente** o que já está verificado:

```text
Reachable                              (FOUND-SEMIGROUP-002)
exists_eventual_period                 (FOUND-SEMIGROUP-002)
exists_bounded_iterate_collision       (FOUND-SEMIGROUP-002)
collision_propagates                   (FOUND-SEMIGROUP-002)
periodic_tail_of_collision             (FOUND-SEMIGROUP-002)
CE-001..CE-005                         (FOUND-SEMIGROUP-002)
Fintype, DecidableEq, decide           (Mathlib, ja exercitados)
Function.iterate                       (Mathlib, ja exercitado)
```

```yaml
expected_scientific_novelty: NONE
expected_formal_value: HIGH
expected_software_reuse: HIGH
expected_cost: LOW_TO_MODERATE
counterexample_access: HIGH
```

Vantagens:

```text
dominio finito;
propriedades decidiveis;
contraexemplos computaveis;
infraestrutura Lean ja existente;
alto potencial de reutilizacao em software;
baixo risco bibliografico;
nenhuma dependencia de fisica;
nenhuma dependencia de PDE;
nenhuma dependencia de analise espectral;
nenhuma dependencia de problema Clay.
```

## Observação honesta sobre a continuidade

`FOUND-FUNCTIONAL-GRAPH-001` é vizinho de `FOUND-SEMIGROUP-002`, e isso é
deliberado. Mas **não é uma extensão dele**: `extension_status` de
`FOUND-SEMIGROUP-002` permanece `NOT_AUTHORIZED`, e a nova frente é um
work item próprio, com identificador próprio, gaps próprios e ciclo
completo de gates. A reutilização é de **API verificada**, não de escopo.

A `REUSE_MATRIX.md` da frente anterior já apontava que os domínios em
`REQUIRES_ADAPTER` precisavam de estrutura sobre o grafo da função. Esta
frente é exatamente essa estrutura — o adaptador que faltava, formalizado
como matemática padrão em vez de como integração ad hoc.

## Decisão

```text
A. PORTFOLIO_REVIEW_APPROVED_FUNCTIONAL_GRAPH_SELECTED
```

Rejeições verificadas antes de aprovar:

| Condição de rejeição | Encontrada? |
|---|---|
| item equivalente já concluído | não |
| dependência formal material não registrada | não |
| conflito estrutural com a organização canônica | não |
| resultado-alvo falso | não — ver abaixo |

### Sobre "resultado-alvo falso"

O resultado estrutural candidato — *cada componente contém um ciclo, e todo
estado do componente o alcança em tempo finito* — é **verdadeiro** e
decorre de `exists_eventual_period`, já verificado. O resultado **mais
forte** (unicidade do ciclo por componente conexa) também é verdadeiro para
grafos funcionais, mas depende de qual noção de "componente" for adotada, e
por isso **não é autorizado** antes da especificação. Ver `FFG-GAP-002` e
`FFG-GAP-004`.
