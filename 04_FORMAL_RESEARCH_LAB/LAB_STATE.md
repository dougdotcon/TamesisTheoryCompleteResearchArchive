---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T16:30:00-03:00
canonical_commit: "f8ccc0203e27dcb7870fa4f7f63a999038236235"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-FUNCTIONAL-GRAPH-001"
work_status: "VERIFIED"
formalization_status: "VERIFIED"
specification_status: "APPROVED"
evidence_level: "F"
last_verified_artifact: "found-functional-graph-001-formalization-result.json"
current_blocker: null
next_single_action: >
  Revisar a API formal, as instâncias, os contraexemplos e os
  limites do resultado antes de autorizar qualquer extensão.
authorized_action: "FOUND_FUNCTIONAL_GRAPH_001_RESULT_REVIEW_AUTHORIZED"
closed_work_items:
  FOUND-SEMIGROUP-002:
    work_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
frozen_work_items:
  RH-NOGO-001:
    work_status: FROZEN_PARTIAL_RESULT
    authorization_state: NOT_AUTHORIZED
    execution_state: NO_EXECUTION
    concrete_layer_status: DEFERRED
governance_lock_renamed:
  from: NO_ACTION_AUTHORIZED
  to: PORTFOLIO_REVIEW_REQUIRED
  reason: "o sufixo _AUTHORIZED convidava a ler a trava como autorização"
  satisfied_by: PORTFOLIO_REVIEW
prohibited_actions:
  - "Não publicar IsRecurrent — usar x ∈ Function.periodicPts f"
  - "Não publicar SameFunctionalComponent nem componentSet sem uso na API pública"
  - "Não usar ∃! p : X no teorema principal"
  - "Não usar decide sobre igualdade de periodicOrbit (noncomputável)"
  - "Não desviar das assinaturas congeladas em FINAL_SIGNATURES.md sem gate próprio"
  - "Não afirmar unicidade de ponto periódico, de representante, de μ ou de período"
  - "Não afirmar ponte com SimpleGraph, árvores ou distância mínima"
  - "Não definir componente funcional como MutuallyReachable (FFG-CE-004 refuta)"
  - "Não formular unicidade como existência de um único ponto periódico (FFG-CE-005 refuta)"
  - "Não importar SimpleGraph no núcleo (FFG-GAP-012 diferido)"
  - "Não acrescentar DecidableEq X sem necessidade verificada — a auditoria mostrou que não é necessária"
  - "Não criar instância global de Setoid, Preorder ou equivalência para EventuallyMeets"
  - "Não criar arquivos Lean sob a autorização atual"
  - "Não afirmar unicidade do ciclo por componente antes de FFG-GAP-002 e FFG-GAP-004"
  - "Não tratar FOUND-FUNCTIONAL-GRAPH-001 como extensão de FOUND-SEMIGROUP-002"
  - "Não estender FOUND-SEMIGROUP-002 nem abrir FOUND-SEMIGROUP-003 sem gate próprio"
  - "Não reabrir RH-NOGO-001 sem que uma condição de RH_NOGO_REACTIVATION_CRITERIA.md ocorra e seja verificada"
  - "Não conectar a nova frente a TRI, TDTR, teoria de tudo, tempo físico, entropia, mecânica quântica ou cosmologia"
  - "Não conectar a nova frente à Hipótese de Riemann, Hilbert–Pólya ou qualquer conjectura Clay"
  - "Não afirmar nova lei universal, nova teoria de dinâmica, descoberta matemática ou descoberta física"
  - "Não apresentar decomposição de grafo funcional como novidade — é material padrão"
  - "Não tratar reutilização em software como descoberta científica"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "01_PORTFOLIO/NEXT_WORK_ITEM_DECISION.md"
  - "01_PORTFOLIO/PORTFOLIO_REVIEW_2026_07_31.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/PUBLIC_API.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/RESULT_BOUNDARY.md"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

```text
FOUND-FUNCTIONAL-GRAPH-001   VERIFIED   formalizacao concluida
FOUND-SEMIGROUP-002          VERIFIED / APPROVED / sem extensao
RH-NOGO-001                  FROZEN_PARTIAL_RESULT
```

## O que foi provado

```text
alcance por iteracao: reflexivo e transitivo;
encontro eventual: reflexivo, simetrico e transitivo;
alcance implica encontro;
pontos periodicos que se encontram determinam a MESMA orbita periodica;
toda trajetoria em tipo finito alcanca um ponto periodico antes de card X;
todos os pontos periodicos do componente determinam a mesma orbita;
seis contraexemplos finitos.
```

## Interpretação vinculante

```text
A unicidade eh da ORBITA PERIODICA, nao do ponto, nao do representante,
nao de mu, nao do periodo. E nao eh decomposicao por SimpleGraph.
```

## Disciplina verificada

```text
Fintype X apenas em ComponentCycle.lean;
DecidableEq X ausente de TODOS os teoremas;
zero instancias no nucleo matematico;
zero Setoid, zero SimpleGraph, zero Quotient;
pigeonhole NAO reaplicado — consumido em FOUND-SEMIGROUP-002;
decide NAO usado sobre igualdade de periodicOrbit;
zero native_decide.
```

`iterReachable_trans` não depende de axioma algum.

## Sem rebaixamento

O gate permitia adiar a igualdade dos períodos mínimos em `FFG-CE-006`.
**Não foi necessário**: `minimalPeriod f a0 = minimalPeriod f b0 = 2` está
provado, via `IsPeriodicPt.minimalPeriod_dvd` e
`minimalPeriod_eq_one_iff_isFixedPt`.

## Novidade

```yaml
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

## Próxima ação

Revisar o resultado. **Nenhuma extensão autorizada.**
