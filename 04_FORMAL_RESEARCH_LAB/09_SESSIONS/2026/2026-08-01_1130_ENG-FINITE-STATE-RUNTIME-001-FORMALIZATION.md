---
session_id: 2026-08-01-ENG-FINITE-STATE-RUNTIME-001-FORMALIZATION
date: 2026-08-01
gate: ENG_FINITE_STATE_RUNTIME_001_FORMALIZATION
authorized_action: ENG_FINITE_STATE_RUNTIME_001_FORMALIZATION_AUTHORIZED
agent: claude-opus-5
commit_before: 6c3b83794cfd315543ea579546941c9e17c9a943
decision: ENG_FINITE_STATE_RUNTIME_001_FORMALIZATION_VERIFIED
theorems_formalized: 18
---

# Sessão — ENG-FINITE-STATE-RUNTIME-001 · formalização

O laboratório passou a ter **a primeira API que aceita diretamente uma
estrutura de dados dinâmica e preserva uma cadeia formal completa até o
certificado**.

```text
Array Nat  ->  validacao  ->  Fin n -> Fin n  ->  detector  ->  witness
                                                                  |
                              repeticao provada sobre o Array original
```

## Preflight

```text
HEAD                  6c3b83794cfd315543ea579546941c9e17c9a943
árvore                limpa
processos Lean/Lake   nenhum
cat-file -e           0
merge-base ancestor   0   (igualdade aceita)
canonical_commit      4d9e248 -> 6c3b837
```

## As duas obrigações sem evidência — resolvidas

`analyzeTransitionTable_sound` e `_complete` eram as únicas obrigações
centrais que a revisão da especificação não conseguira demonstrar.
**Ambas compilaram na primeira tentativa**, junto com os outros cinco
módulos.

Isso não foi sorte. A revisão já havia demonstrado
`run?_eq_iterate_step`, `step?_eq_some_step`, `detectCycle?_raw_repeat` e
os dois teoremas de erro em ambiente descartável, e registrado tanto os
padrões que funcionam quanto **as três abordagens que falham** ao tentar
reduzir o `do` sobre `Except`.

### O auxiliar que fez a diferença

```lean
private theorem analyze_reduce (hRaw : raw.Valid) (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start =
      (match detectCycle? ⟨raw.next, hRaw⟩ ⟨start, hStart⟩ with
        | some witness => .ok witness
        | none => .error .internalDetectorFailure)
```

Ele isola, de uma vez, as duas reduções que a notação `do` esconde.
Soundness ficou com sete linhas; completeness, com quatro.

**Nenhum transporte dependente foi necessário.** A tabela concreta
`⟨raw.next, hRaw⟩` tem `next` *sintaticamente* igual a `raw.next`, e seu
`toRaw` é definicionalmente `raw` por eta de estruturas. Zero `cast`,
zero `Eq.ndrec`.

## O que foi construído

```text
TamesisLab/Engineering/FiniteStateRuntime/
  RawTable.lean         Raw, Valid, decidableValid, Validated, toRaw
  Validation.lean       RuntimeCycleError e as duas validacoes
  Execution.lean        step, step?, run? e as duas pontes
  DetectorAdapter.lean  reutilizacao do detector
  DynamicAnalysis.lean  analyzeTransitionTable e cinco teoremas
  Audit.lean            somente #check

2 estruturas, 1 indutivo, 9 definicoes, 1 instancia, 18 teoremas,
869 linhas.
```

## Camadas de hipótese

```text
camada 0   Raw, Valid, step?, run?          nenhuma typeclass
camada 1   validacoes                       nenhuma typeclass
camada 2   step e pontes                    nenhuma typeclass
camada 3   detectCycle?                     Fintype/DecidableEq INFERIDAS
camada 4   analyzeTransitionTable           nenhuma do chamador
```

**O consumidor fornece `Array Nat` e `Nat`.** Nada mais.

## Pegada axiomática — o achado mais nítido

```text
step? e run?                    does not depend on any axioms
toda a camada de validacao      [propext, Quot.sound]
run?_eq_iterate_step            [propext, Quot.sound]
detectCycle? e herdeiros        [propext, Classical.choice, Quot.sound]
sorryAx                         0
```

As **duas definições de execução bruta não dependem de axioma nenhum**, e
toda a validação dispensa `Classical.choice`. A pegada entra exatamente
onde o detector entra, por `Fintype.card` — e não é marca de
não-computabilidade: a função foi avaliada em dezenove casos.

## A proibição que governa a arquitetura

```text
destinos invalidos sao REJEITADOS, nunca corrigidos.
```

Dois teoremas tornam isso impossível de esconder:
`validateTransitionTable_sound` força a tabela devolvida a ser **a
mesma**, e `validateStart_sound` — o teorema **anti-clamp** — força o
índice devolvido a ter **o valor pedido**. Qualquer `%`, `clamp` ou
`getD` futuro quebraria uma das duas provas.

A busca por correções silenciosas casou três linhas, **todas de
documentação**: as próprias proibições e o nome "anti-clamp". Zero no
código.

## Precedência dos erros — provada e medida

```text
analyzeTransitionTable ⟨#[1]⟩ 100  ->  transitionDestinationOutOfBounds
```

Tabela inválida **e** início inválido; o erro de **tabela** vence. Os
dois teoremas de erro fixam qual sai em cada caso, e é isso que impede
`internalDetectorFailure` de mascarar falha de validação.

## O ramo defensivo

`analyzeTransitionTable_ne_internalFailure` prova que ele é inalcançável
sob as pré-condições. **O construtor permanece na função executável.**
`FOUND-CYCLE-DETECTION-001` **não** foi totalizado.

## Validação

```text
DynamicAnalysis.lean (isolado)   exit 0    29 s
tres testes                      exit 0    2 / 4 / 2 s, zero erros
lake build                       PASS    8748 jobs (era 8737), 100 s
tokens proibidos                 0
correcoes silenciosas no codigo  0
internos do detector             0
imports proibidos                0
pytest                           PASS
labctl validate                  PASS
whitespace                       PASS, antes do git add
commit --amend                   NAO usado
```

O contador do build subiu **+11**: seis módulos, o `Audit`, os dois
agregadores e os três testes. A raiz alcança `TamesisLab.Engineering`.

## Desvio de ordem, registrado

Os dois teoremas de erro foram declarados **antes** de
`analyzeTransitionTable_sound`, invertendo a ordem sugerida no item 5 do
gate — porque a soundness os usa nos ramos negativos do `by_cases`.
Escolha deliberada, não desvio silencioso.

## Claim

Uma, a vigésima primeira: `FINITE-STATE-RUNTIME-ADAPTER-FORMAL-001`,
`VERIFIED`, `evidence_level: F`, novidade matemática e algorítmica
**NONE**.

## Estado final

```text
work_status            VERIFIED
specification_status   APPROVED
formalization_status   VERIFIED
authorized_action      ENG_FINITE_STATE_RUNTIME_001_RESULT_REVIEW_AUTHORIZED
```

Extração, CLI, JSON, CSV, rede, integração, diagnóstico detalhado,
totalização do detector e Floyd permanecem **não autorizados**.

## Próxima ação única

Revisar a API dinâmica, a precedência dos erros, a correspondência entre
execução bruta e iteração tipada, a reutilização do detector e os limites
de integração antes de autorizar qualquer extração, CLI ou parser.
