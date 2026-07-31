---
session_id: 2026-07-31-FOUND-FUNCTIONAL-GRAPH-001-RESULT-REVIEW
date: 2026-07-31
gate: FOUND_FUNCTIONAL_GRAPH_001_RESULT_REVIEW
authorized_action: FOUND_FUNCTIONAL_GRAPH_001_RESULT_REVIEW_AUTHORIZED
agent: claude-opus-5
commit_before: 3f6d7e785ba8bd90a35f33f7dc889f1234a7b650
decision: A_FOUND_FUNCTIONAL_GRAPH_001_RESULT_REVIEW_APPROVED
new_theorems: 0
math_modules_modified: 0
---

# Sessão — FOUND-FUNCTIONAL-GRAPH-001 · Revisão de resultado

Revisão do que já estava verificado. **Nenhum teorema novo. Nenhum módulo
matemático alterado.**

## Preflight

```text
HEAD                  3f6d7e785ba8bd90a35f33f7dc889f1234a7b650
árvore                limpa
cat-file -e           0
merge-base ancestor   0   (igualdade aceita)
canonical_commit      f8ccc02 -> 3f6d7e7
```

Governança na entrada: `work_status: VERIFIED`,
`specification_status: APPROVED`, `formalization_status: VERIFIED`,
`authorized_action: FOUND_FUNCTIONAL_GRAPH_001_RESULT_REVIEW_AUTHORIZED`.

## O que foi revisado

`FGR-001` a `FGR-008`: **todos CONFIRMADOS**, cada um contra a assinatura
impressa pelo Lean, não contra a documentação.

A transitividade de `EventuallyMeets` foi revisada **linha a linha**, com o
mapa de índices `hxy : f^[mx] x = f^[ny] y`, `hyz : f^[my] y = f^[nz] z`,
separação por `Nat.le_total ny my` e testemunhas `(d + mx, nz)` e
`(mx, d + nz)`. A orientação de `Function.iterate_add_apply` — contagem
externa à esquerda — foi reconferida, e todas as chamadas passam `f`
explicitamente.

## A ressalva vinculante

A recíproca **exige** que ambos os pontos sejam periódicos. Se
`p ∉ periodicPts f`, então `periodicOrbit f p = Cycle.nil`; dois pontos
não periódicos têm, ambos, a órbita **vazia**, e as órbitas são iguais
**sem** que as trajetórias se encontrem. As hipóteses `hp` e `hq`
permanecem visíveis na assinatura pública e na documentação.

O fenômeno foi verificado concretamente no teste de auditoria:

```lean
example : Function.periodicOrbit CE002.f CE002.St.a = Cycle.nil :=
  Function.periodicOrbit_eq_nil_iff_not_periodic_pt.mpr CE002.a_not_periodic
```

**Não formalizado**: nenhum dos seis contraexemplos exibe dois pontos não
periódicos que **não** se encontram — em `CE-002` e `CE-004` os pontos
transitórios **se encontram**. Construir tal modelo exigiria um sétimo
contraexemplo, isto é, matemática nova, proibida neste gate. Registrado
como observação estrutural, **não** como fato formalizado.

## Auditoria de API e instâncias

```text
declarações públicas       16   (exatamente a lista mínima)
auxiliar privado            1   minimalPeriod_eq_two
instâncias                  5   CE001, CE002, CE003, CE004, CE006
instâncias no núcleo        0
conflitos                   0
Setoid                      0
imports de SimpleGraph      0
```

Os wrappers relacionais usam `Std.Refl` e `Std.Symm` — os nomes **não
depreciados** nesta revisão da Mathlib — e `IsTrans`, que também não está
depreciado. Nenhum exigiu API depreciada.

Criado `TamesisLab/Tests/FoundFunctionalGraph001InstanceAudit.lean`, que
**não altera módulo matemático algum** e verifica que, com as cinco
instâncias em escopo pelo umbrella, a API continua se aplicando a `Bool`.

## Validação

```text
FoundFunctionalGraph001.lean                 exit 0    30 s
FoundFunctionalGraph001Counterexamples.lean  exit 0     2 s
FoundFunctionalGraph001InstanceAudit.lean    exit 0     3 s
lake build                                   PASS   8727 jobs, 108 s
sorry/admit/axiom/unsafe                     0 / 0 / 0 / 0
sorryAx                                      0
pytest                                       9 passed
labctl validate                              PASS
whitespace EOF (antes do git add)            PASS
```

Axiomas: `eventuallyMeets_trans` fica em `[propext, Quot.sound]`; os outros
quatro em `[propext, Classical.choice, Quot.sound]`.

## Limites

`periodicOrbit` é **noncomputável**. O resultado formal **não** fornece
algoritmo executável de enumeração de componentes, cálculo de `mu` ou
detecção de ciclo. A matriz de reutilização separa uso proposicional de
uso computacional: **1** `DIRECT_REUSE`, **7** `REQUIRES_ADAPTER`, **2**
`CONCEPTUAL_ONLY`. Nenhuma integração criada.

Novidade matemática: **NENHUMA**. Papel: fundação formal.

## Lacunas

Quinze no total: **onze resolvidas, quatro abertas** — `FFG-GAP-006`,
`-007` e `-012` diferidas; `-014` bibliográfica. Nenhuma foi fechada sem
evidência.

## O que não foi feito

**0** teoremas novos, **0** módulos matemáticos alterados, **0** claims
novas (ledger permanece em **19**), **0** arquivos de legado tocados, **0**
arquivos de `RH-NOGO-001`, **0** arquivos matemáticos de
`FOUND-SEMIGROUP-002`.

`RH-NOGO-001` permanece `FROZEN_PARTIAL_RESULT`, não autorizada, sem
execução, camada concreta diferida.

## Estado final

```text
work_status         VERIFIED
result_review       APPROVED
extension_status    NOT_AUTHORIZED
authorized_action   PORTFOLIO_REVIEW_REQUIRED
```

`PORTFOLIO_REVIEW_REQUIRED` é **trava de governança**, não ação
autorizada. `NO_ACTION_AUTHORIZED` não foi usado, e nenhuma entrada nova
foi acrescentada ao allowlist.

## Próxima ação única

Aguardar um gate explícito de revisão de portfólio. Nenhuma extensão de
`FOUND-FUNCTIONAL-GRAPH-001` está autorizada.
