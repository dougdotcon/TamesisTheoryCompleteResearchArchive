---
session_id: 2026-07-31-FOUND-CYCLE-DETECTION-001-SPECIFICATION-REVIEW
date: 2026-07-31
gate: FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW
authorized_action: FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_AUTHORIZED
agent: claude-opus-5
commit_before: 03e1ec36b97233df481597980f0a5383b2decc65
decision: A_FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_APPROVED
repository_lean_files_created: 0
---

# Sessão — FOUND-CYCLE-DETECTION-001 · revisão da especificação

Revisão, correção e congelamento antes de autorizar a formalização.
**Nenhum módulo Lean permanente. Nenhuma prova permanente. Nenhum
`lake build`.**

## Preflight

```text
HEAD                  03e1ec36b97233df481597980f0a5383b2decc65
árvore                limpa
processos Lean/Lake   nenhum
cat-file -e           0
merge-base ancestor   0   (igualdade aceita)
canonical_commit      ab79032 -> 03e1ec3
```

## Correção obrigatória

```text
prefixIndex  ->  baseIndex
```

Quarenta ocorrências, oito documentos. Os registros históricos **fora** da
pasta de especificação — o JSON do gate anterior, sua sessão e o changelog
— **não** foram reescritos; a decisão está marcada como superada em
`DATA_MODEL.md` e na tabela de renomeações de
`SPECIFICATION_DECISION.md`. A governança **viva** (`LAB_STATE.md`) foi
atualizada.

`prefix` ainda podia ser lido como "o prefixo antes do ciclo", isto é,
como minimalidade. `baseIndex` é o índice-base da igualdade
`f^[baseIndex + period] x = f^[baseIndex] x`, e nada além disso.

## Probe descartável

`/tmp/CycleDetectionReviewProbe.lean`, executado com `lake env lean` em
28 s, **sem erros**, e removido ao final. Contém versões descartáveis de
`CycleWitness`, `cycleCandidates` e `detectCycleWitness?`, cinco modelos
concretos e `#eval`. Sem `axiom`, `sorry`, `admit`, `unsafe`,
`noncomputable`, `Classical.choose` ou teoremas permanentes.

## Os cinco casos obrigatórios — todos bateram

| Caso | Esperado | Medido |
|---|---|---|
| `Fin 1`, `id` | `⟨0,1⟩` | **`some ⟨0,1⟩`** |
| `Bool`, `id` | `⟨0,1⟩` | **`some ⟨0,1⟩`** nos dois estados |
| `Bool`, `not` | `⟨0,2⟩` | **`some ⟨0,2⟩`** nos dois estados |
| `Fin 3`, `0→1→2→2` | `⟨2,1⟩` | **`some ⟨2,1⟩`** |
| `Fin 4`, `0→1→2→3→2` | `⟨2,2⟩` | **`some ⟨2,2⟩`** |

Nenhuma função e nenhuma ordem foi alterada para satisfazer expectativa.

A partir dos demais estados iniciais: `Fin 3` dá `⟨1,1⟩` e `⟨0,1⟩`;
`Fin 4` dá `⟨1,2⟩`, `⟨0,2⟩` e `⟨0,2⟩`. Isso ilustra concretamente o que
`CD-TEST-005` previa: o `period` testemunhado coincide dentro do
componente; o `baseIndex` **não**.

## Enumeração medida

```text
cycleCandidates 0 = []        por rfl
cycleCandidates 1 = [<0,1>]   por rfl
comprimentos: n=3 -> 6,  n=4 -> 10,  n=5 -> 15
fronteira n=3: <0,3>, <1,2>, <2,1>
fronteira n=4: <0,4>, <1,3>, <2,2>, <3,1>
```

A observação `n(n+1)/2` agora tem três medidas concordantes — e continua
**não sendo um lema**.

## Três achados da revisão

### 1. A instância `Decidable` precisa ser declarada

`Valid` é um `def`; a resolução de instâncias **não** o desdobra. Sem

```lean
instance CycleWitness.decidableValid ... :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))
```

o `decide (Valid f x w)` não elabora e o detector nem compila. A
especificação inicial supunha que sairia sozinho. Acrescentada às
assinaturas congeladas.

### 2. Pegada axiomática não é noncomputabilidade

```text
#print axioms cycleCandidates      does not depend on any axioms
#print axioms detectCycleWitness?  [propext, Classical.choice, Quot.sound]
```

Origem localizada com um segundo probe: **`Fintype.card` e
`Finset.univ`**. `List.range`, `flatMap`, `find?` e `Nat.iterate` não
dependem de axioma algum, e uma variante `detectAt? (n : ℕ)` que recebe a
cota também não.

`Fintype.card` é computável — `#eval` devolve `3` para `Fin 3` — e mesmo
assim carrega `Classical.choice`, porque a infraestrutura de `Finset` usa
escolha dentro de **provas**, que são apagadas. O critério do gate foi
reformulado: não `noncomputable`, `#eval` funciona, nenhum
`Classical.choose` produzindo dado. Os três confirmados.

Consequência: `ValidAt` **não** resolve nada — o detector precisa calcular
`Fintype.card X` de qualquer modo. Permanece `DEFERRED`.

### 3. `propagates` alinhada ao teorema existente

`collision_propagates` tem a forma `(h) (k)`. A assinatura pública foi
alinhada a ela: hipótese primeiro, `k` depois. Nenhuma chamada extra a
`Nat.add_comm`, e `Function.iterate_add_apply` não será reprovado.

## Totalização

```yaml
total_wrapper:
  status: DEFERRED
  classification: OPTIONAL_CORE_PENDING_EXECUTION_TEST
```

Seis dos sete critérios confirmados, incluindo a avaliação do mecanismo:

```lean
def probeTotal ... (h : (detectCycleWitness? f x).isSome = true) : CycleWitness :=
  (detectCycleWitness? f x).get h
```

avaliou para `⟨0,2⟩`, `⟨2,2⟩` e `⟨2,1⟩` com `h` fornecido por `decide`. O
critério restante — `#eval` com a prova vinda da completude — exigiria
provar um teorema central no probe, o que o gate proíbe. A API garantida
da v1 permanece `Option CycleWitness`.

`Option.getD` com certificado padrão falso está **proibido**: devolveria
um certificado inválido em um caso que nunca ocorre, e
`detectCycleWitness_valid` se tornaria improvável.

## Gaps

Dezenove, reclassificados: **6** resolvidos, **5** prontos para
formalização, **1** pronto para auditoria de viabilidade, **6** diferidos,
**1** bibliográfico. **Nenhum fechado por expectativa.**

## Validação

```text
pytest                       PASS
labctl validate              PASS
canonical_commit_check       PASS
probe                        PASS, removido
arquivos Lean no repositorio 0
provas no repositorio        0
implementacao permanente     NAO
lake build                   NAO
claims promovidas            0   (ledger em 19)
legado modificado            0
whitespace                   PASS, antes do git add
```

## Estado final

```text
active_work_item      FOUND-CYCLE-DETECTION-001
work_status           READY
specification_status  APPROVED
authorized_action     FOUND_CYCLE_DETECTION_001_FORMALIZATION_AUTHORIZED
```

Floyd, Brent, tabela visitada, extração, integração e minimalidade
permanecem **não autorizados**.

## Próxima ação única

Formalizar a enumeração finita de certificados, o detector parcial
executável, sua soundness e sua completeness por reutilização de
`exists_bounded_iterate_collision`.
