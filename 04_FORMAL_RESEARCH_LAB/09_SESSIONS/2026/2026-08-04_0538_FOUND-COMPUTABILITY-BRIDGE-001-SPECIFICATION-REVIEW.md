---
session_id: 2026-08-04_0538_FOUND-COMPUTABILITY-BRIDGE-001-SPECIFICATION-REVIEW
started_at: 2026-08-04T05:38:00-03:00
ended_at: 2026-08-04T05:38:00-03:00
agent: claude-opus-5
git_commit_before: 4c7c11dbf655edc61d75d1eb99f690dea9750a84
git_commit_after: PENDING
active_work_item: FOUND-COMPUTABILITY-BRIDGE-001
authorized_action: FOUND_COMPUTABILITY_BRIDGE_001_SPECIFICATION_REVIEW_AUTHORIZED
result_status: SPECIFICATION_APPROVED
claims_changed: []
gaps_opened: 1
gaps_closed: 0
---

## Objetivo autorizado

Revisar a especificação congelada em `4c7c11d`.

## Os cinco defeitos

| # | tipo | onde morreu |
|---|---|---|
| 1 | afirmação de primazia FALSA sobre instâncias | revisão |
| 2 | campo impreciso de typeclasses | revisão |
| 3 | teste decidível por avaliação | revisão |
| 4 | canonicidade da instância não declarada | revisão |
| 5 | chave YAML duplicada | `labctl validate`, pré-commit |

Nenhuma das **19** assinaturas públicas mudou.

### O defeito 1 é o que importa para a governança

```text
declarado    "primeira frente com instance_declarations != 0"
derivado     22 instancias, 6 arquivos, script
```

É o **terceiro defeito de contagem agregada em três frentes
consecutivas**, e o primeiro que não é aritmético. A regra
`aggregate_counts` fala em contagens; esta era uma contagem disfarçada de
adjetivo — *primeira* é um numeral. A proibição nova fecha essa brecha.

### O defeito 3 é o que importa para a evidência

`boolEncoding_bound_concrete` enunciava `0 + 2 ≤ 2`. Passaria com o
teorema da cota **apagado do arquivo**. Um teste que sobrevive à remoção
do que testa não é teste.

Substituído por `boolEncoding_bound_applies`, quantificado sobre `w`.

### O defeito 4 rendeu resultado, não só correção

`Primcodable Bool` já existe no Mathlib e difere da instância induzida.
Em vez de apenas avisar, a revisão acrescentou:

```lean
theorem boolEncoding_primrec_canonical :
    Primrec (analyzeEncodedSystem boolEncoding not) :=
  Primrec.dom_finite _
```

Sob a instância canônica, mesma conclusão, mesma linha de prova. É o
resultado central de outro ângulo: **a codificação não importa porque
quem faz o trabalho é a finitude.**

Um caso não é uma invariância. `CB-GAP-010` e `STOP-CB-013` guardam a
diferença.

## Verificações

```text
probe reexecutado no gate       exit 0, 0 error:, 0 warning:
declaracoes                     29  derivadas por script, PARTITION_OK
pegada                          29/29, cobertura FULL
labctl validate                 PASS, 0 erros            (pos-correcao)
pytest                          34 passed
frentes encerradas modificadas  0
arquivos Lean permanentes       0
```

## Estado final

```text
specification_status   APPROVED
specification_review   APPROVED
authorized_action      FOUND_COMPUTABILITY_BRIDGE_001_FORMALIZATION_AUTHORIZED
lacunas                10
condicoes de parada    13
```
