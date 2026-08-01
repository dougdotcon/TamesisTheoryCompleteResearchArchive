---
session_id: 2026-08-01-PORTFOLIO-REVIEW-AFTER-CERTIFIED-ENCODING
date: 2026-08-01
gate: PORTFOLIO_REVIEW
authorized_action: PORTFOLIO_REVIEW_AUTHORIZED
agent: claude-opus-5
commit_before: e0db1dceaf8e73239d361ed17453b050716d88bc
decision: A_PORTFOLIO_REVIEW_APPROVED_FINITE_ABSTRACTION_SELECTED
selected_work_item: FOUND-FINITE-ABSTRACTION-001
lean_files_created: 0
---

# Sessão — revisão de portfólio após a codificação certificada

## Preflight

```text
HEAD                  e0db1dceaf8e73239d361ed17453b050716d88bc
arvore                limpa
processos             nenhum
canonical_commit      e9e2ce7 -> e0db1dc
duplicatas YAML       0, em 55 arquivos
claims                22
work items            15
```

## A pergunta

A cadeia existente resolve o caso **exato**: `S ≃ Fin n`, nada se perde.
Falta o caso em que **se perde** — abstração muitos-para-um.

A tentação é perguntar "abstração finita preserva ciclos?". Este gate
respondeu, e a resposta é **não**:

```lean
theorem naive_cycle_reflection_is_false : ¬ (∀ …)
```

Compilado, **sem axioma nenhum**, pelo contraexemplo `Bool → Unit` com
`stepC = not`. O abstrato repete em um passo; o concreto, não.

A pergunta certa é a outra: **o que a abstração preserva, e sob qual
hipótese o que ela destrói pode ser recuperado.**

## As duas metades, ambas compiladas

```text
preserva, sempre:
  abstract (stepC^[b+p] start) = abstract (stepC^[b] start)

recupera, sob hipotese:
  OrbitSeparating abstract stepC start →
    stepC^[b+p] start = stepC^[b] start
```

A primeira sai de `analyzeEncodedSystem_sound` mais duas aplicações de
`Semiconj.iterate_right`. A segunda é a primeira mais uma aplicação da
hipótese.

## A condição não é enfeite

`boolToUnit_not_orbitSeparating` prova que `OrbitSeparating` **falha**
exatamente no contraexemplo. Se ela fosse consequência da
semiconjugação, valeria ali — e a reflexão ingênua seria verdadeira.
Compilado, sem axiomas.

E ela não assume a conclusão: quantifica sobre **todos** os pares da
órbita, enquanto a conclusão compara **um** par.

E é satisfazível: toda abstração injetiva a cumpre, e a cadeia inteira
foi instanciada com a identidade sobre `Fin 4`.

## `OrbitSeparating` contra `Set.InjOn`

```lean
theorem orbitSeparating_iff_injOn : OrbitSeparating … ↔ Set.InjOn abstract (Set.range …)
```

Equivalentes, sem axiomas. Recomendação preliminar: a primeira como
formulação primária, por ser mais direta na prova (`hsep (b+p) b h`) e na
verificação pelo consumidor; a segunda como vista equivalente, exatamente
como `Equiv` foi tratado na frente anterior. O nome **não** está
congelado.

## A alternativa que eu quase escolhi por conveniência

`B`, invariância do witness sob recodificação, fecha uma lacuna nomeada e
é estreita. Rejeitada porque a igualdade do witness **concreto** depende
da ordem de enumeração de `cycleCandidates` — provar isso abriria o
detector, que quatro frentes trataram como caixa-preta verificada. O que
é de fato invariante, a validade semântica, já é a soundness.

## A alternativa que auditei em vez de supor

`F`, front matter YAML em Markdown. Eu mesmo registrei essa lacuna no
gate anterior, o que torna tentador promovê-la. Medi:

```text
markdown_files                    429
com_front_matter                  277
com_duplicatas                      0
bloco de LAB_STATE.md          limpo
```

A lacuna é **real** — o scanner seleciona por extensão e não vê YAML em
`.md`. Mas não está sendo explorada. Fica registrada como candidata, sem
prioridade sobre a lacuna científica.

## Doze de doze

As doze condições da regra de decisão foram verificadas, **oito por
compilação**. Nenhuma exige `C` finito nem `DecidableEq C`: os probes
usam `C : Type*` sem typeclass.

## Estado final

```text
active_work_item     FOUND-FINITE-ABSTRACTION-001
work_status          SCOPED
authorized_action    FOUND_FINITE_ABSTRACTION_001_SPECIFICATION_PREPARATION_AUTHORIZED
allowlist            uma entrada literal, sem wildcard
gaps                 20, nenhum fechado
stop conditions      16
arquivos Lean        0
claims               22, nenhuma promovida
duplicatas YAML      0
```

## Próxima ação única

Preparar a especificação. Distinguir soundness observacional de reflexão
concreta, e congelar o contraexemplo — sem iniciar a formalização.
