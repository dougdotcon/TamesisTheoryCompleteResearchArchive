---
session_id: 2026-08-01-ENG-FINITE-STATE-RUNTIME-001-SPECIFICATION
date: 2026-08-01
gate: ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION
authorized_action: ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_PREPARATION_AUTHORIZED
agent: claude-opus-5
commit_before: 23fdf957a2ddd63e52551bf2cd071bf290eb0d25
decision: A_ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_READY
lean_files_created: 0
---

# Sessão — ENG-FINITE-STATE-RUNTIME-001 · especificação

Ponte entre `Array Nat` e `Fin n → Fin n`, para aplicar com segurança o
detector já verificado. **Nenhum módulo Lean permanente, nenhuma prova,
nenhum adaptador, nenhum binário, nenhum `lake build`.**

## Preflight

```text
HEAD                  23fdf957a2ddd63e52551bf2cd071bf290eb0d25
árvore                limpa
processos Lean/Lake   nenhum
cat-file -e           0
merge-base ancestor   0   (igualdade aceita)
canonical_commit      a4907b7 -> 23fdf95
```

Todos os códigos de saída verificados explicitamente.

## As quatro decisões congeladas

```text
entrada bruta        Array Nat
tabela vazia         estruturalmente valida
destino invalido     erro, nunca modulo/clamp/fallback
resultado dinamico   Except RuntimeCycleError CycleWitness
```

## O probe fez o trabalho pesado

Uma versão **descartável** do pipeline inteiro foi escrita, executada e
removida. Treze casos avaliados, **todos com o resultado previsto**:

```text
#[]        start 0   ->  error (initialStateOutOfBounds 0 0)
#[1]       start 0   ->  error transitionDestinationOutOfBounds
#[0]       start 1   ->  error (initialStateOutOfBounds 1 1)
#[0]       start 0   ->  ok <0,1>
#[1,0]     start 0   ->  ok <0,2>
#[1,2,2]   start 0   ->  ok <2,1>
#[1,2,3,2] start 0   ->  ok <2,2>   e de 1,2,3 -> <1,2>, <0,2>, <0,2>
#[0,2,1]   start 0,1,2 -> <0,1>, <0,2>, <0,2>
```

Os quatro que produzem certificado a partir de `#[0]`, `#[1,0]`,
`#[1,2,2]` e `#[1,2,3,2]` reproduzem **exatamente** os modelos `Fin 1`,
`Bool`, `Fin 3` e `Fin 4` já verificados no detector. Isso dá à frente um
**oráculo independente**.

Além disso: `step_val` fechou por `rfl`, a instância decidível foi
sintetizada, e `run?` devolveu `none` no acesso fora do array — sem
fallback.

## Quatro decisões que o gate deixou em aberto

1. **`stateCount` não será criado.** Duplicaria `next.size` sob um segundo
   nome público, e `next.size` já aparece nos tipos `Fin`, em `step`, em
   `validateStart` e no erro. A alternativa — adotá-lo em toda parte —
   ficou registrada.
2. **`toRaw` será público.** É a única forma de enunciar
   `run?_eq_iterate_step` e `detectCycle?_raw_repeat`, que falam da tabela
   **original**.
3. **`step?_eq_some_step` é `CORE`, não opcional.** A indução de
   `run?_eq_iterate_step` depende dele para o `bind` reduzir.
4. **A variante de iteração é `Function.iterate_succ_apply`**, não a
   linha. `run?` aplica um passo e recorre sobre o resto, logo a contagem
   externa consome o passo **interno**. Auditado no checkout, não
   presumido — precisamente o tipo de detalhe que a frente anterior errou
   uma vez com `iterate_add_apply`.

## Um achado da auditoria de API

```text
#print axioms validateT   ->   [propext, Quot.sound]
```

A camada de validação, **isolada**, não depende de `Classical.choice`. A
pegada só entra quando o detector é aplicado, por `Fintype.card`. E, como
já estabelecido, pegada axiomática não é não-computabilidade.

Três nomes de constante **não existem** nesta revisão: `Array.get`,
`Array.getElem?` e `Array.size_toArray`. A funcionalidade existe pela
notação `xs[i]` e `xs[i]?`, ambas usadas com sucesso no probe.

## A proibição que governa a arquitetura

```text
NAO corrigir destinos invalidos por modulo, clamp ou fallback.
```

Um `% n` silencioso transformaria uma tabela errada em um **sistema
diferente**, e o certificado seria correto sobre um sistema que o usuário
nunca descreveu. `validateStart_sound` — que prova preservação exata do
`start` — é o teorema anti-clamp, e existe para tornar essa falha
impossível de passar despercebida.

## O ganho central

```text
o consumidor fornece Array Nat e Nat. Nada mais.
```

Sem `Fintype`, sem `DecidableEq`, sem `Fin`, sem provas, sem funções
Lean. As estruturas finitas são construídas **internamente**.

## O risco

```text
run?_eq_iterate_step eh o unico teorema da frente cuja prova nao eh
mecanica.
```

Se a indução exigir generalização adicional ou lemas de coerção
`Fin`/`Nat` não previstos, o custo cresce. É onde a especificação está
mais exposta, e onde a revisão deve olhar primeiro.

## Localização

`03_ENGINEERING/01_FINITE_STATE_RUNTIME/ENG_FINITE_STATE_RUNTIME_001/`,
25 documentos. O prefixo `03_` repete `03_MILLENNIUM`; segui o caminho
literal do gate, e há precedente no repositório —
`02_FOUNDATIONS/` contém `04_FUNCTIONAL_GRAPHS/` e `04_MONOTONES/`.

## Validação

```text
pytest                       PASS
labctl validate              PASS
canonical_commit_check       PASS
probe                        REMOVIDO
arquivos Lean no repositorio 0
provas                       0
adaptador implementado       NAO
executavel criado            NAO
lake build                   NAO executado
claims promovidas            0   (ledger em 20)
legado modificado            0
whitespace                   PASS, antes do git add
commit --amend               NAO usado
```

## Estado final

```text
work_status            READY
specification_status   READY_FOR_REVIEW
authorized_action      ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_REVIEW_AUTHORIZED
```

Formalização, extração, CLI, JSON, integração e diagnóstico detalhado
permanecem **não autorizados**. Floyd, Brent e a totalização do detector
anterior também.

## Próxima ação única

Revisar a validade da tabela, a construção da função sobre `Fin n`, a
correspondência entre execução bruta e iteração tipada e a API dinâmica
baseada em `Except`.
