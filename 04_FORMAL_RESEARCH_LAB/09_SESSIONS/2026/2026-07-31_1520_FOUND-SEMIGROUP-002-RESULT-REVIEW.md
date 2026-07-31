---
session_id: 2026-07-31_1520_FOUND-SEMIGROUP-002-RESULT-REVIEW
started_at: 2026-07-31T14:40:00-03:00
ended_at: 2026-07-31T15:20:00-03:00
agent: claude-opus-5
git_commit_before: b4ce2551cd9f3588030fc7281d7f8c7aa624bac3
git_commit_after: null
active_work_item: FOUND-SEMIGROUP-002
authorized_action: FOUND_SEMIGROUP_002_RESULT_REVIEW_AUTHORIZED
result_status: FOUND_SEMIGROUP_002_RESULT_REVIEW_APPROVED
files_created:
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/RESULT_REVIEW.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/PUBLIC_API.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/INSTANCE_AUDIT.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/REUSE_MATRIX.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/FINAL_GAP_STATUS.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/CLOSURE_RECORD.md"
  - "05_FORMAL/lean/TamesisLab/Tests/FoundSemigroup002InstanceAudit.lean"
  - "found-semigroup-002-result-review.json"
  - "09_SESSIONS/2026/2026-07-31_1520_FOUND-SEMIGROUP-002-RESULT-REVIEW.md"
files_modified:
  - "05_FORMAL/lean/TamesisLab.lean"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/STATUS.yaml"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/GAP_REGISTER.yaml"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "00_GOVERNANCE/CLAIM_LEDGER.yaml"
  - "10_TOOLS/labctl.py"
  - "LAB_STATE.md"
  - "CHANGELOG.md"
lean_math_files_modified: 0
new_theorems: 0
new_claims: 0
tests_executed:
  - "Tests/FoundSemigroup002.lean: exit 0"
  - "Tests/FoundSemigroup002Counterexamples.lean: exit 0"
  - "Tests/FoundSemigroup002InstanceAudit.lean: exit 0"
  - "lake build: PASS"
  - "tokens proibidos: 0; sorryAx: 0"
  - "pytest: 9 passed"
  - "labctl validate: PASS, canonical_commit_check PASS"
decision: A_FOUND_SEMIGROUP_002_RESULT_REVIEW_APPROVED
next_single_action: "Aguardar um gate separado de revisão de portfólio para selecionar o próximo work item. Nenhuma extensão de FOUND-SEMIGROUP-002 está autorizada."
---

## Preflight

`HEAD = b4ce2551…`, árvore limpa. `canonical_commit` atualizado de
`2b86a880` para `b4ce2551` **antes** da revisão; `cat-file` exit 0,
`merge-base --is-ancestor` exit 0 (igualdade com HEAD).

## O que você apontou como risco principal

> *"verificar se as 11 instâncias ficaram suficientemente isoladas e se a
> API pública está separada dos auxiliares e contraexemplos"*

O resultado da auditoria é melhor do que o esperado:

```text
Reachability.lean          0 instancias
Invariants.lean            0 instancias
EventualPeriodicity.lean   0 instancias
MonoidIteration.lean       0 instancias
Audit.lean                 0 instancias
Counterexamples.lean      11 instancias
```

**O núcleo matemático não declara instância alguma.** As onze estão todas
em modelos de contraexemplo, distribuídas em cinco namespaces:
`CE001` 4, `CE002` 4, `CE003` 1, `CE004` 2, `CE005` 0.

O caso que merecia atenção era `CE004`, que reutiliza `CE001.Tr` sobre um
espaço de estados diferente — duas instâncias `MulAction` para o **mesmo**
monoide. Não há conflito: os pares `(CE001.Tr, CE001.St)` e
`(CE001.Tr, CE004.St)` são distintos. Verifiquei por `#synth` e por dois
`rfl` que resolvem o `•` para a ação correta em cada tipo.

## Separação da API

```text
17 declaracoes publicas — exatamente a lista minima esperada
 1 auxiliar, `eventual_period_of_lt`, e ele eh `private`
11 instancias, todas sob Counterexamples.CExxx
 3 arquivos de teste, fora do namespace da frente
```

Não há auxiliar público acidental. `eventual_period_of_lt` existe
precisamente para que os ramos `i < j` e `j < i` não dupliquem argumento,
e não vaza.

## Teste de auditoria criado

`Tests/FoundSemigroup002InstanceAudit.lean`, exit 0. **Não altera módulo
matemático algum.** Além dos onze `#synth`, ele verifica o que realmente
importa: com o agregador importado — portanto com todas as instâncias em
escopo — `exists_eventual_period` **continua se aplicando a `Bool`**. Ou
seja, a poluição de instâncias não existe na prática, não apenas na
inspeção.

## FRR-001 a FRR-007

Todos **CONFIRMADOS**. Dois pontos que exigiram verificação ativa:

- **FRR-003** — confirmei por inspeção que não existe declaração cuja
  conclusão seja `IsInvariant` a partir de `IsInvariantUnder`. A recíproca
  não é afirmada em lugar algum.
- **FRR-005** — `Function.minimalPeriod` aparece **quatro vezes** nos
  arquivos, todas em comentários explicando por que **não** é usado. Zero
  usos reais. `MulAction.period`: zero ocorrências. A palavra "período"
  nunca significa período mínimo.

## Caso `card X = 0`

O teorema recebe `x : X`. Logo, no ponto de aplicação, `X` é habitado e
`card X > 0`. Se `card X = 0`, a conclusão `μ < 0` seria insatisfazível em
`ℕ` — mas nenhuma instância do teorema existe ali, porque não há termo
`x : X`. **Não há contradição escondida.**

Auditei a hipótese oculta correspondente: busca por `Nonempty` e
`Inhabited` nos módulos da frente devolve **zero ocorrências**. A habitação
vem do próprio argumento, não de instância global.

## Casa dos pombos

```yaml
pigeonhole_uses_in_core: 1
reproved_in_main_theorem: false
reproved_in_monoid_corollary: false
reproved_in_propagation: false
```

Três ocorrências textuais: um uso real, um docstring, um `#check`.

## Gaps

Nove resolvidos, três abertos. **Não fechei `FSG2-GAP-007`** — a negativa
*"o período depende do estado inicial"* continua sem contraexemplo — nem
**`FSG2-GAP-009`**, por falta de auditoria bibliográfica. Ambos como o
gate exigiu.

## Reutilização

Um único domínio em `DIRECT_REUSE`: **testes de alcançabilidade** — e é o
mais abstrato justamente porque essa parte da API **não exige finitude**.
Tudo que depende de `Fintype X` precisa de adaptador, e essa é a hipótese
que costuma falhar em software real, onde estados carregam dados não
limitados.

Nenhuma integração foi criada.

## Decisão

```text
A. FOUND_SEMIGROUP_002_RESULT_REVIEW_APPROVED
```

Nenhum defeito material encontrado. Nenhum teorema criado, nenhum módulo
matemático alterado, nenhuma instância criada ou corrigida.

## Encerramento

```yaml
work_status: VERIFIED
result_review: APPROVED
extension_status: NOT_AUTHORIZED
authorized_action: NO_ACTION_AUTHORIZED
```

`NO_ACTION_AUTHORIZED` é **trava, não autorização**. Nenhum gate pode agir
sob ela. Registrei isso explicitamente nas `prohibited_actions`, porque um
nome terminado em `_AUTHORIZED` convida à leitura errada.

O laboratório fica com **nenhuma frente ativa**:

```text
FOUND-SEMIGROUP-002   VERIFIED / APPROVED     encerrado
RH-NOGO-001           FROZEN_PARTIAL_RESULT   congelado
```

A escolha do próximo trabalho exige um gate separado de revisão de
portfólio.
