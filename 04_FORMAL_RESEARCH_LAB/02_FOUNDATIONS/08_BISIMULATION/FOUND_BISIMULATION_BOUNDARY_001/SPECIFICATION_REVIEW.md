---
document_id: FOUND-BISIMULATION-BOUNDARY-001-SPECIFICATION-REVIEW
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
review_start_head: a51fc14b5e6e30d03de135ad0eb9100905df413e
decision: FOUND_BISIMULATION_BOUNDARY_001_SPECIFICATION_REVIEW_APPROVED
review_probe_exit: 0
stop_conditions_triggered: 0
---

# Revisão da especificação

## Preflight

```text
REVIEW_START_HEAD   a51fc14b5e6e30d03de135ad0eb9100905df413e
mensagem            lab: specify deterministic bisimulation boundary
arvore de trabalho  limpa
processos ativos    nenhum
```

## Probe de revisão

```text
arquivo   /tmp/BisimulationReviewProbe.lean
error_lines        0
REAL_EXIT_CODE     0
removido           SIM
declaracoes destinadas a falhar   0
```

## A verificação decisiva — `STOP-BIS-002`

O risco central da frente é `Reflects` ter sido escrito já resolvido, o
que tornaria o colapso uma tautologia. A revisão testou isso
diretamente:

```lean
example (abstract) (stepC) (stepA) :
    Reflects abstract stepC stepA
      ↔ ∀ c, ∃ c', stepC c = c' ∧ abstract c' = stepA (abstract c) :=
  Iff.rfl
```

`Iff.rfl` — a existencial **está lá**, por definição.

E o contraste é o que fecha o argumento:

| Teorema | Prova | Leitura |
|---|---|---|
| `simulates_iff_semiconj` | `Iff.rfl` | zig **é** semiconjugação |
| `reflects_iff_simulates` | duas direções | zag **não é** trivial |

Se `Reflects` tivesse sido trivializado, `reflects_iff_simulates` também
seria `Iff.rfl`. Não é.

```text
STOP-BIS-002 disparada   NAO
```

## Os dez itens revisados

| # | Item | Verdito |
|---|---|---|
| 1 | definições separadas em zig e zag | APROVADO |
| 2 | `Reflects` não trivializado | APROVADO |
| 3 | teorema de colapso | APROVADO |
| 4 | contraexemplo já é bissimulação | APROVADO |
| 5 | sobrejetividade não resgata | APROVADO |
| 6 | as duas negações compilam | APROVADO |
| 7 | fronteira do recorte documentada | APROVADO |
| 8 | nenhuma typeclass | APROVADO |
| 9 | pegada axiomática nula | APROVADO |
| 10 | frentes encerradas intocadas | APROVADO |

## Pegada medida

```text
simulates_iff_semiconj                             NENHUM
reflects_iff_simulates                             NENHUM
bisimulation_iff_semiconj                          NENHUM
boolToUnit_bisimulation                            NENHUM
forgetBool_surjective                              NENHUM
bisimulation_does_not_reflect_cycles               NENHUM
surjective_bisimulation_does_not_reflect_cycles    NENHUM
```

**Sete de sete sem pegada.** A frente não atravessa
`analyzeEncodedSystem`, então `propext`, `Classical.choice` e
`Quot.sound` não entram — ao contrário da frente anterior.

## Fronteira de escopo

[`SCOPE_BOUNDARY.md`](SCOPE_BOUNDARY.md) foi revisado item a item. Ele
identifica corretamente a **origem** do colapso — a ausência de escolha
na testemunha do zag, consequência de `stepC` ser função total — e
enumera os cinco relaxamentos que a destroem.

A wording proibida está registrada, incluindo a forma mais provável de
erro: escrever "bissimulação é semiconjugação" sem qualificador.

```text
STOP-BIS-001 disparada   NAO
```

## Correções aplicadas

Uma, menor: o probe de especificação emitia
`warning: Variable name stepA is not explicitly referenced` em
`injective_bisimulation_reflects`. A declaração é `DEFERRED_OPTIONAL` e
não entra na API; o aviso está registrado em
[`PROBE_RESULT.md`](PROBE_RESULT.md) para que a ausência dela na
formalização não pareça mudança silenciosa.

## Ressalva de independência

Especificação e revisão foram executadas pelo mesmo agente em sessões
consecutivas. A revisão vale pelo que **mediu** — `Iff.rfl` contra prova
em duas direções, `#print axioms`, `REAL_EXIT_CODE` capturado por
arquivo de script — e não por independência de autoria.

## Decisão

```text
FOUND_BISIMULATION_BOUNDARY_001_SPECIFICATION_REVIEW_APPROVED
```
