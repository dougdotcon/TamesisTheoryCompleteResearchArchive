---
document_id: FFG-SPECIFICATION-REVIEW
gate: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW
reviewed_commit: 90fb4e26da33cebed2ba414ee5aeb663647de149
decision: A_SPECIFICATION_REVIEW_APPROVED
lean_files_in_repo_created: 0
---

# FOUND-FUNCTIONAL-GRAPH-001 — Revisão da especificação

Revisão feita **antes** da formalização, precisamente para que uma
definição inadequada não fosse congelada em Lean.

## As duas correções obrigatórias

### 1. Semântica de `MutuallyReachable`

A redação anterior — *"identifica o ciclo, não o componente"* — era
imprecisa como afirmação sobre todo o domínio. **Corrigida** em
`FINAL_DEFINITIONS.md` para a formulação por classes, com o argumento de
isolamento dos transitórios escrito.

Acrescentei um refinamento que o próprio enunciado do gate não continha: a
frase "classe não trivial" só vale para ciclos de comprimento maior que um.
**Um ponto fixo é periódico e sua classe também é unitária.** Portanto
"classe unitária" **não** distingue transitório de ponto fixo — o que
distingue é a pertinência a `Function.periodicPts f`.

### 2. `IsRecurrent` retirado

Não será publicado. "Recorrência" tem significados mais amplos em dinâmica.
Decisão e justificativa em `API_NAMING_DECISION.md`.

Adotei a **Estratégia A com a cláusula condicional resolvida
negativamente**: os teoremas públicos usam `x ∈ Function.periodicPts f`
diretamente, e `IsCyclePoint`/`IsTransientPoint` **não** são criados,
porque a lista `CORE` congelada não os usa. Nessa resolução, A coincide com
B — registro a coincidência para que não se suponha uma terceira via.

## A correção que a auditoria de API acrescentou

O gate pediu para **auditar a orientação real de
`Function.iterate_add_apply`**. O probe devolveu:

```lean
Function.iterate_add_apply (f : α → α) (m n : ℕ) (x : α) :
  f^[m + n] x = f^[m] (f^[n] x)
```

A contagem **externa** é `m` e aparece à **esquerda** da soma. Consequência
direta sobre as testemunhas da transitividade:

| Caso | Especificação do gate | **Forma natural** |
|---|---|---|
| `ny ≤ my` | `x: mx + d` | **`x: d + mx`** |
| `my ≤ ny` | `z: nz + d` | **`z: d + nz`** |

Mesmo valor, forma sintática diferente. Escrever `mx + d` obrigaria
`Nat.add_comm` para casar com `rw`. As formas naturais estão congeladas em
`FINAL_SIGNATURES.md`, com o mapa de índices completo.

Isto vale também para `iterReachable_trans`, cuja testemunha natural é
`b + a`, não `a + b`.

## Confirmações da API — probe descartável

Executado em `/tmp/FFGSpecificationReviewProbe.lean`, apenas `import` e
`#check`, exit **0**, arquivo **removido**. Zero ocorrências de `theorem`,
`example`, `axiom`, `sorry`, `admit`. Nenhum arquivo `.lean` criado no
repositório. Nenhum `lake build`.

```text
periodicPts (f : α → α) : Set α
mem_periodicPts : x ∈ periodicPts f ↔ ∃ n > 0, IsPeriodicPt f n x
mk_mem_periodicPts (hn : 0 < n) (hx : IsPeriodicPt f n x) : x ∈ periodicPts f
periodicOrbit (f : α → α) (x : α) : Cycle α
periodicOrbit_apply_iterate_eq (hx) (n) :
  periodicOrbit f (f^[n] x) = periodicOrbit f x
mem_periodicOrbit_iff (hx) : y ∈ periodicOrbit f x ↔ ∃ n, f^[n] x = y
self_mem_periodicOrbit (hx) : x ∈ periodicOrbit f x
periodicOrbit_eq_nil_iff_not_periodic_pt :
  periodicOrbit f x = Cycle.nil ↔ x ∉ periodicPts f
iterate_add_apply (f) (m n) (x) : f^[m + n] x = f^[m] (f^[n] x)
IsPeriodicPt (f : α → α) (n : ℕ) (x : α) : Prop
```

Três pontos confirmados:

1. **`periodicPts` exige período positivo**; `IsPeriodicPt f 0 x` é sempre
   verdadeiro e não pode definir pertinência ao ciclo sozinha.
2. **`periodicOrbit : Cycle X`**, sem `DecidableEq`, e **noncomputável** —
   não impede provas proposicionais, impede `decide` sobre igualdade de
   órbitas.
3. **`periodicOrbit_apply_iterate_eq`** tem `f^[n] x` à esquerda; a rota de
   `FFG-CYCLE-001` usa `.symm` no primeiro passo.

## Verificação item a item

| Critério de aprovação | Estado |
|---|---|
| `EventuallyMeets` correta | sim |
| transitividade com testemunhas coerentes | sim — **corrigidas** para a forma natural |
| `MutuallyReachable` descrita precisamente | sim — **corrigida**, com refinamento sobre ponto fixo |
| recorrência sem alias enganoso | sim — `IsRecurrent` retirado |
| `periodicOrbit` adequada | sim — `Cycle X`, sem `DecidableEq` |
| principal sem `∃!` sobre pontos | sim |
| `Fintype` apenas onde necessário | sim — só na existência e no principal |
| `DecidableEq` ausente do núcleo | sim |
| `SimpleGraph` diferido | sim |
| contraexemplos distintos | sim — seis alvos distintos |
| nenhuma prova executada | sim — 0 arquivos no repositório |

## Alteração no teorema principal

O nome e a forma mudaram em relação à especificação:

```text
antes:  functional_component_has_unique_cycle  (∃ p : X, ...)
agora:  exists_component_cycle_with_entry_bound (∃ mu : ℕ, ...)
```

A forma com `∃ mu : ℕ` e `f^[mu] x` é preferível: elimina o `p` existencial
redundante — `p` era sempre `f^[mu] x` — e torna o limite de entrada parte
do enunciado principal em vez de uma segunda versão. As duas variantes
`FFG-MAIN-001`/`002` colapsam em **uma**.

A orientação da conclusão foi ajustada para
`periodicOrbit f (f^[mu] x) = periodicOrbit f q`, e ela **continua
obedecendo** à regra congelada: o primeiro argumento de `EventuallyMeets`
na aplicação de `FFG-CYCLE-001` é `f^[mu] x`.

## Decisão

```text
A. FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW_APPROVED
```

Nenhum defeito material. As duas correções pedidas foram aplicadas, mais
uma terceira que a auditoria de orientação revelou.
