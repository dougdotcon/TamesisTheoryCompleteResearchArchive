---
session_id: 2026-08-01-ENG-FINITE-STATE-RUNTIME-001-RESULT-REVIEW
date: 2026-08-01
gate: ENG_FINITE_STATE_RUNTIME_001_RESULT_REVIEW
authorized_action: ENG_FINITE_STATE_RUNTIME_001_RESULT_REVIEW_AUTHORIZED
agent: claude-opus-5
commit_before: 746102fa458fe7ccda6d8939bb3f8834a8ac0dc4
decision: A_ENG_FINITE_STATE_RUNTIME_001_RESULT_REVIEW_APPROVED
new_theorems: 0
math_modules_modified: 0
---

# Sessão — ENG-FINITE-STATE-RUNTIME-001 · revisão de resultado

Fechamento da **primeira cadeia completa do laboratório que começa em um
dado de runtime potencialmente inválido e termina em um certificado
formal de repetição sobre esse mesmo dado.**

## Preflight

```text
HEAD                  746102fa458fe7ccda6d8939bb3f8834a8ac0dc4
árvore                limpa
processos Lean/Lake   nenhum
cat-file -e           0
merge-base ancestor   0   (igualdade aceita)
canonical_commit      6c3b837 -> 746102f
```

## A correção documental

```text
GAP_REGISTER.yaml, cabecalho:
  resolved_formally  10 -> 11
  open_deferred       8 ->  7
  total                     22   (inalterado)
```

Estritamente documental: nenhum status individual, nenhum módulo Lean,
nenhuma claim, nenhuma força de resultado. Registrada em
`METADATA_CORRECTION_RECORD.md`, e **verificada por script** — o
cabeçalho agora é comparado contra um `Counter` das entradas, e a
verificação passou.

Causa raiz: o cabeçalho foi escrito à mão em vez de derivado. É a mesma
lição que já apareceu duas vezes nesta sessão sob outra forma —
**contagem escrita à mão diverge; contagem derivada não.** A regra entrou
nas proibições vivas do `LAB_STATE.md`.

## `RTR-001` a `RTR-007` — todos confirmados

Conferidos contra o fonte. Os pontos que mais importam:

- `raw.next.size` é o **único** nome público do número de estados;
  nenhum accessor `stateCount` existe.
- A validade estrutural **não** exige estado inicial nem tabela não
  vazia, e **não** afirma alcançabilidade, componente único ou ciclo
  único.
- A tabela vazia é válida; a consulta é rejeitada. Nenhum erro
  `emptyTable` existe.
- Erro de **tabela** e erro de **consulta** não colapsados.

## A garantia central, auditada

```text
destinos invalidos sao REJEITADOS, nunca corrigidos.
```

A busca por `%`, `mod`, `clamp`, `min`, `max`, `getD` e `fallback`
retornou **zero no código**; as duas ocorrências textuais são as próprias
proibições e o nome "anti-clamp", em documentação.

Dois teoremas tornam isso impossível de esconder:
`validateTransitionTable_sound` força a tabela devolvida a ser **a
mesma**, e `validateStart_sound` — o **anti-clamp** — força o índice a
ter **o valor pedido**. Não é convenção; é obrigação verificada pelo
kernel.

## A ponte de iterações — auditada linha por linha

Indução em `k` com o quantificador **no enunciado**, hipótese válida para
todo `start`, passo externo consumido primeiro,
`Function.iterate_succ_apply`, **nenhuma orientação inversa**, coerções
`Fin`/`Nat` explícitas. Axiomas `[propext, Quot.sound]`.

Os dois `show` não são cosméticos: o primeiro expõe o `bind` que o `do`
esconde, o segundo força a redução de `Option.bind (some a) f`.

**Nenhuma segunda semântica paralela de execução existe.**

## Soundness e completeness da análise

`analyzeTransitionTable_sound`: **zero** `cast`, **zero** `Eq.ndrec`,
**zero** transporte dependente manual, **zero** hipóteses extras do
consumidor, e a terceira conjunção enunciada sobre `raw` — não sobre uma
tabela intermediária.

O motivo de não haver transporte é de desenho: a tabela concreta
`⟨raw.next, hRaw⟩` tem `next` **sintaticamente** igual a `raw.next`, e
seu `toRaw` é definicionalmente `raw` por eta. O problema que a
especificação temia não ocorre porque o desenho o evitou.

`analyzeTransitionTable_complete`: o witness vem de
`detectCycle?_complete` por `obtain`, **dentro da prova**, em nível
`Prop`. Sem `Classical.choose`, sem `Option.get`, sem projeção
computacional.

O auxiliar `analyze_reduce` foi classificado `INTERNAL_HELPER` e
auditado: **não adiciona hipótese matemática** — seu enunciado é uma
igualdade de definições.

## Precedência dos erros

```text
analyzeTransitionTable ⟨#[1]⟩ 100  ->  transitionDestinationOutOfBounds
```

Tabela inválida **e** início inválido; o erro de **tabela** vence. E a
razão é visível na assinatura: `analyzeTransitionTable_invalid_table` tem
como hipótese **apenas** `¬raw.Valid` — nada é dito sobre `start`.

`internalDetectorFailure` permanece na função, com sua impossibilidade
provada. O detector anterior **não** foi totalizado.

## Cobertura dos agregadores

Criado `EngFiniteStateRuntime001UmbrellaAudit.lean`, que importa **apenas**
`TamesisLab` e referencia as vinte e nove declarações por nome totalmente
qualificado, mais o caso decisivo `⟨#[1]⟩` com `start = 100`. **Exit 0**,
87 s. Ele não é registrado na raiz — importa-a, e registrá-lo criaria
ciclo (`RT-GAP-018`).

## Validação

```text
cinco testes                exit 0, zero erros
lake build                  PASS
tokens proibidos            0
imports proibidos           0
correcoes silenciosas       0 no codigo
internos do detector        0
pytest                      PASS
labctl validate             PASS
whitespace                  PASS, antes do git add
commit --amend              NAO usado
```

## Matriz de reutilização

**Três** aplicações passaram de `REQUIRES_ADAPTER` — a classificação da
frente anterior — para `DIRECT_WITH_ARRAY`: configurações finitas,
autômatos e máquinas de estado. As outras seis não melhoraram, e a razão
é honesta: o obstáculo delas nunca foi a interface, e sim o fato de o
espaço de estados real não ser finito nem conhecido.

```text
o adaptador prova que A TABELA FORNECIDA eh analisada corretamente;
ele NAO prova que ela representa um sistema externo real.
```

## Estado final

```text
work_status                        VERIFIED
result_review                      APPROVED
extension_status                   NOT_AUTHORIZED
extraction_status                  NOT_AUTHORIZED
cli_status                         NOT_AUTHORIZED
external_format_status             NOT_AUTHORIZED
integration_status                 NOT_AUTHORIZED
detailed_diagnostics_status        NOT_AUTHORIZED
external_abstraction_correctness   DEFERRED
authorized_action                  PORTFOLIO_REVIEW_REQUIRED
```

`PORTFOLIO_REVIEW_REQUIRED` é **trava**, não autorização. Nenhuma entrada
nova no allowlist; `NO_ACTION_AUTHORIZED` não foi usado.

## Próxima ação única

Aguardar um gate explícito de revisão de portfólio. Nenhuma extração,
CLI, parser, integração ou ampliação está autorizada.
