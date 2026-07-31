---
session_id: 2026-07-31_1240_FOUND-SEMIGROUP-002-SPECIFICATION
started_at: 2026-07-31T12:00:00-03:00
ended_at: 2026-07-31T12:40:00-03:00
agent: claude-opus-5
git_commit_before: 39e3d95925a7038da307017216dd4cb8e49c572a
git_commit_after: null
active_work_item: FOUND-SEMIGROUP-002
authorized_action: FOUND_SEMIGROUP_002_SPECIFICATION_PREPARATION_AUTHORIZED
result_status: FOUND_SEMIGROUP_002_SPECIFICATION_READY
files_created:
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/README.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/STATUS.yaml"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/TARGET_RESULT.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/DEFINITIONS.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/ASSUMPTIONS.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/THEOREM_CANDIDATES.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/LEAN_FEASIBILITY.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/COUNTEREXAMPLE_PLAN.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/KNOWN_RESULTS_MATRIX.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/DEPENDENCY_DAG.yaml"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/GAP_REGISTER.yaml"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/STOP_CONDITIONS.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/NOVELTY_BOUNDARY.md"
  - "06_COMPUTATION/python/tests/test_canonical_commit.py"
  - "found-semigroup-002-specification-result.json"
  - "09_SESSIONS/2026/2026-07-31_1240_FOUND-SEMIGROUP-002-SPECIFICATION.md"
files_modified:
  - "10_TOOLS/labctl.py"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "LAB_STATE.md"
  - "CHANGELOG.md"
tests_executed:
  - "pytest: 9 passed (2 anteriores + 7 novos de canonical_commit)"
  - "labctl validate: PASS, canonical_commit_check PASS"
  - "lean files created: 0"
  - "lean proofs created: 0"
  - "lake build: NAO executado"
  - "python experiments created: 0"
  - "scientific claims promoted: 0"
  - "legacy files modified: 0"
claims_changed: []
gaps_opened:
  - "FSG2-GAP-001..009 (registro inicial da frente)"
gaps_closed: []
decision: A_FOUND_SEMIGROUP_002_SPECIFICATION_READY
next_single_action: "Formalizar o núcleo aprovado de alcançabilidade, invariantes e periodicidade eventual para funções em tipos finitos, sem executar extensões físicas ou alegações Tamesis."
---

## Preflight

`HEAD = 39e3d95925a7038da307017216dd4cb8e49c572a`, árvore limpa, três
commits de retomada confirmados. `canonical_commit` foi atualizado de
`c186ab59` para `39e3d95` **antes** de qualquer trabalho de especificação,
e a política textual foi substituída pela definição correta.

## Validação de `canonical_commit`

Implementada em `labctl.py` como função pura com `runner` injetável, o que
permitiu testar a tabela de decisão **sem criar branch nem reescrever
histórico**:

```text
cat-file != 0        -> CANONICAL_COMMIT_UNAVAILABLE  (recomenda --unshallow)
is-ancestor exit 0   -> PASS, inclusive canonical_commit == HEAD
is-ancestor exit 1   -> CANONICAL_COMMIT_NOT_ANCESTOR
is-ancestor outro    -> CANONICAL_COMMIT_GIT_ERROR
```

Sete testes cobrem os cinco casos pedidos mais dois. O teste de igualdade
verifica a lista exata de comandos emitidos e afirma que **não há
`rev-parse` extra** — isto é, que a implementação delega a reflexividade ao
próprio git e não acrescenta uma comparação `canonical_commit != HEAD`.
Se alguém endurecer isso no futuro, o teste quebra.

## A separação que motiva a frente

```text
CAMADA A   acao completa de M          exists m, m . x = y
CAMADA B   um gerador a fixo           a^n . x
CAMADA C   funcao finita (X, f)        f^[n] x
```

Regra adotada: **todo teorema vai para a camada mais fraca em que ainda faz
sentido.** Consequência direta: periodicidade eventual é teorema da Camada
C. Não menciona monoide e não precisa de um. Enunciá-la na Camada A seria
importar hipótese ociosa — o mesmo erro que o gate `COUNTING-LAW-BRIDGE` já
corrigiu ao remover `0 < c`.

## Três achados da auditoria da Mathlib

**1. `smul_iterate_apply` já existe.** A especificação previa que a
identidade `f^[n] x = a^n • x` pudesse faltar. Ela está em
`Algebra/Group/Action/Defs.lean:437`. `FSG2-GAP-003` resolvido por leitura
da fonte, não por prova.

**2. `mem_orbit_iff` é `Iff.rfl`.** Logo `Reachable x y ↔ y ∈ orbit M x`
custa zero. Decidido usar `MulAction.orbit` com `Set X`; `Finset` exigiria
`DecidableEq X` e `Fintype M`, ambas desnecessárias.

**3. Periodicidade eventual está ausente do Mathlib.** Busca por
`preperiodic`, `eventuallyPeriodic` e `eventually_periodic`: **zero
ocorrências**. A ausência não significa novidade — significa que o
enunciado é curto demais para ter virado API compartilhada.

## A armadilha que quase passou

`Function.minimalPeriod` e `MulAction.period` devolvem **0** quando o ponto
não é periódico:

```lean
def minimalPeriod (f : α → α) (x : α) :=
  if h : x ∈ periodicPts f then Nat.find h else 0
```

E `IsPeriodicPt f n x := f^[n] x = x` exige retorno ao ponto **inicial**.
Em `CE-003` (`0 → 1 → 2 → 2`) o estado `0` é eventualmente periódico mas
não é periódico, logo `minimalPeriod f 0 = 0` — o que contradiria
`0 < λ`. Quem tratasse `minimalPeriod` como "período eventual" escreveria
um enunciado falso.

Registrado como `FSG2-GAP-002b`, com `STOP-009` e o contraexemplo `CE-003`
para torná-lo detectável. `FSG2-PER-004` é o antídoto: o ponto periódico é
`f^[μ] x`, **não** `x`.

## Escolha da meta: C, com os limitantes verificados antes de prometer

Antes de escolher, verifiquei se os três limitantes eram simultaneamente
alcançáveis:

```text
g : Fin (card X + 1) -> X,  g i = f^[i] x
pigeonhole da  i != j  com  i, j <= card X
ordenando:     i < j <= card X
mu = i         ==>  mu < card X                OK
lam = j - i    ==>  lam > 0                    OK
mu + lam = j   ==>  mu + lam <= card X         OK
```

São. Por isso `BOUNDS` sai de graça e a meta é **C**, não B.
`PROPAGATION` é corolário de três linhas via `iterate_add_apply`.

**`DECOMPOSITION` fica fora**, com custo analisado: cinco obrigações novas
(minimalidade de `μ`, minimalidade de `λ`, unicidade do par, injetividade
no segmento inicial, estrutura cíclica), e a parte de divisibilidade
depende de lemas de `Dynamics/PeriodicPts` não auditados.

## Uma hipótese que provavelmente é ociosa

A assinatura sugerida pelo gate inclui `[DecidableEq X]`. A prova esboçada
**não a usa**. Decidi omiti-la, salvo necessidade demonstrada na execução —
mesma política de não manter hipótese matematicamente ociosa. Registrado em
`FSG2-GAP-004c` para que a execução confirme ou refute.

## Preorder: nenhuma instância global

Alcançabilidade é reflexiva e transitiva, logo um preorder. Mas
`instance Preorder X` seria keyed em `X`, e a relação depende de `M`, que
não aparece no tipo. Duas ações sobre o mesmo `X` dariam instâncias
incompatíveis, e `X` frequentemente já tem ordem própria. Decisão:
teoremas mais um `def reachablePreorder` **não** marcado como `instance`,
para uso explícito com `letI`. `STOP-010` guarda isso.

## O que `C3` não cobre

Quatro propriedades valem no modelo de `FOUND-SEMIGROUP-001` e falham em
geral:

| Propriedade | `C3` | Geral |
|---|---|---|
| ação fiel | sim | não — `CE-004` |
| ação transitiva | sim | não — `CE-002` |
| alcançabilidade simétrica | sim | não — `CE-001` |
| órbita sem cauda | sim | não — `CE-003` |

`C3` é **bom demais** para servir de caso de teste do alvo. Os cinco
contraexemplos existem exatamente para cobrir o que ele não cobre.

## Uma negativa sem exemplo — registrada, não afirmada

`ASSUMPTIONS.md` lista "o período pode depender do estado inicial" como
**sem modelo planejado** (`FSG2-GAP-007`). O modelo é trivial de
construir, mas o gate pediu cinco contraexemplos específicos e nenhum
deles cobre essa negativa. Preferi registrar a pendência a afirmar uma
negativa sem exemplo — que é justamente o que o gate proíbe.

## O que não foi feito

```text
0 arquivos Lean criados
0 provas Lean
0 lake build
0 experimentos Python
0 claims cientificas promovidas
0 arquivos de legado modificados
0 arquivos de RH-NOGO-001 tocados
```

## Novidade

Zero. Periodicidade eventual em conjunto finito é o princípio da casa dos
pombos, material introdutório padrão. `NOVELTY_BOUNDARY.md` é vinculante e
traz a tabela de "não escrever / escrever". E como
`FSG2-GAP-009` registra bibliografia primária `NOT_AUDITED`, **nenhuma
afirmação de prioridade histórica ou atribuição a autor é permitida**.

## Handoff

Especificação `READY`. Onze teoremas candidatos com assinaturas, cinco
contraexemplos planejados, API auditada por leitura de fonte, doze gaps
registrados, fronteira de novidade vinculante. A formalização está
autorizada para o gate seguinte — e só ela.
