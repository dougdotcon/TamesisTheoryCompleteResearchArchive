---
session_id: 2026-07-31-FOUND-CYCLE-DETECTION-001-SPECIFICATION
date: 2026-07-31
gate: FOUND_CYCLE_DETECTION_001_SPECIFICATION
authorized_action: FOUND_CYCLE_DETECTION_001_SPECIFICATION_PREPARATION_AUTHORIZED
agent: claude-opus-5
commit_before: ab79032062cddf195671208058820993cfaabe76
decision: A_FOUND_CYCLE_DETECTION_001_SPECIFICATION_READY
lean_files_created: 0
---

# Sessão — FOUND-CYCLE-DETECTION-001 · especificação

Especificação de um detector executável e formalmente verificável de
ciclos em trajetórias determinísticas finitas. **Nenhum módulo Lean
permanente. Nenhum algoritmo implementado. Nenhum `lake build`.**

## Preflight

```text
HEAD                  ab79032062cddf195671208058820993cfaabe76
árvore                limpa
processos Lean/Lake   nenhum
cat-file -e           0
merge-base ancestor   0   (igualdade aceita)
canonical_commit      49924c3 -> ab79032
```

Governança na entrada: `active_work_item FOUND-CYCLE-DETECTION-001`,
`work_status SCOPED`,
`authorized_action FOUND_CYCLE_DETECTION_001_SPECIFICATION_PREPARATION_AUTHORIZED`.

## A decisão algorítmica

A primeira implementação **não** será Floyd.

```yaml
primary_algorithm: BOUNDED_CERTIFICATE_SEARCH
future_optimization: FLOYD
reference_alternative: VISITED_TABLE
deferred_algorithm: BRENT
```

O argumento decisivo é a coincidência literal entre o contrato do
certificado e a conclusão de um teorema já verificado. Lida do fonte:

```lean
theorem exists_bounded_iterate_collision {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧ 0 < lam ∧ mu + lam ≤ Fintype.card X ∧
        f^[mu + lam] x = f^[mu] x
```

O predicado `CycleWitness.Valid` é **a mesma conjunção, na mesma ordem**.
A completude deixa de ser prova nova e passa a ser transporte.

Registrado explicitamente que isso **não** é uma afirmação de
superioridade assintótica — provavelmente não é. A escolha otimiza risco
formal.

## Modelo de dados

```lean
structure CycleWitness where
  prefixIndex : ℕ
  period : ℕ
```

Dois naturais, **não parametrizada por `X`**. `entryPoint` foi rejeitado:
é derivável por `f^[w.prefixIndex] x₀`.

Semântica vinculante: `prefixIndex` é **índice-base de uma colisão
certificada**, não o menor índice de entrada — o nome `entryIndex` fica
proibido. `period` é **período positivo testemunhado**, não
`minimalPeriod`.

## Auditoria de API

Sonda temporária em `/tmp`, executada com `lake env lean` em 27 s, sem
erros na segunda passagem. Trinta e uma APIs confirmadas com assinatura
impressa pelo próprio Lean. **Dois nomes do gate divergiam do checkout** e
foram corrigidos:

```text
List.find?_eq_some  ->  List.find?_eq_some_iff_append
Function.iterate    ->  Nat.iterate
```

`List.get?` e `List.getElem?` **não existem** como constantes nesta
revisão — `NOT_FOUND`, sem consequência: não são necessárias.

A fronteira `μ + λ = n` foi verificada **por avaliação**:

```text
n = 3  ->  [(0,1), (0,2), (0,3), (1,1), (1,2), (2,1)]
n = 1  ->  [(0,1)]
```

Os pares de soma `3` estão lá. A sonda foi removida ao final.

## Predicado executável

Decidido pela **Opção A**, `decide (Valid f x w)`, porque a sonda mostrou
que `inferInstance` monta a instância `Decidable` da conjunção completa:

```lean
example (f : Bool → Bool) (m l : ℕ) :
    Decidable (m < Fintype.card Bool ∧ 0 < l ∧ m + l ≤ Fintype.card Bool ∧
      f^[m + l] true = f^[m] true) :=
  inferInstance
```

`Bool` e `Prop` **não** ficam congelados simultaneamente: existe uma
definição só, e `decide_eq_true_eq` é a única ponte.

## Três desvios registrados

1. **`mem_cycleCandidates_iff` não é dependência da soundness.** As três
   cotas vivem dentro de `Valid`, então a soundness sai de
   `List.find?_some` mais `decide_eq_true_eq`. É fortificação: sobrevive a
   uma troca de algoritmo. O DAG do gate foi corrigido nesse ramo.
2. **Totalização `DEFERRED`.** Quatro das cinco condições têm argumento
   favorável; a quinta — `#eval` funcionar — só é verificável
   implementando, o que este gate proíbe. A API v1 permanece baseada em
   `Option`.
3. **Dois nomes de API corrigidos** contra o Lean real.

## Fronteira de computabilidade

```text
DecidableEq X  eh sobre ESTADOS.
periodicOrbit  vive em Cycle X.
```

Nenhuma decidibilidade sobre `Cycle X` é assumida, requerida ou
construída. `DecidableEq` aparece **somente** na camada do detector; as
três pontes proposicionais — `isPeriodicPt`, `mem_periodicPts`,
`propagates` — não a recebem.

Isso não contradiz as frentes anteriores: lá as camadas eram puramente
proposicionais, e afirmar igualdade não exige decidi-la.

## Reutilização

Três dos dez teoremas `CORE` **não exigem matemática nova alguma**:

| Candidato | Reutiliza | Prova nova |
|---|---|---|
| `CycleWitness.isPeriodicPt` | `periodic_tail_of_collision` | nenhuma |
| `CycleWitness.mem_periodicPts` | `Function.mk_mem_periodicPts` | nenhuma |
| `CycleWitness.propagates` | `collision_propagates` | nenhuma — assinatura idêntica |

A casa dos pombos permanece consumida **uma única vez**, em
`FOUND-SEMIGROUP-002`. `Fintype.exists_ne_map_eq_of_card_lt` não aparecerá
nesta frente.

## Terminação

Estrutural. `cycleCandidates (card X)` é lista finita, `List.find?` termina
sobre ela. **Sem `fuel`, sem recursão bem fundada, sem `Classical.choice`.**
É exatamente aqui que a busca certificada se separa de Floyd, cuja
terminação depende de um argumento matemático que teria de virar invariante.

## Limites

```yaml
complexity_status: NOT_FORMALIZED
asymptotic_optimality: NOT_CLAIMED
minimal_prefix_index: NOT_AUTHORIZED
minimal_period: NOT_AUTHORIZED
mathematical_novelty: NONE
algorithmic_novelty: NONE
```

Limitação prática registrada em `CD-GAP-019`: a busca recomputa
`f^[μ] x` e `f^[μ+λ] x` para cada par candidato, sem memoização. É a
principal desvantagem em relação a Floyd — registrada como limitação
conhecida, não como claim de complexidade.

## Artefatos

Vinte e um documentos em
`02_FOUNDATIONS/05_CYCLE_DETECTION/FOUND_CYCLE_DETECTION_001/`.
Dezenove lacunas: sete resolvidas por design ou auditoria, cinco por
plano, uma por fronteira, seis abertas e uma pronta para auditoria de
viabilidade. **Nenhuma fechada por expectativa.**

## Validação

```text
pytest                   PASS
labctl validate          PASS
canonical_commit_check   PASS
sonda temporaria         REMOVIDA
arquivos Lean criados    0
provas criadas           0
algoritmo implementado   NAO
lake build               NAO
claims promovidas        0   (ledger em 19)
legado modificado        0
whitespace               PASS, antes do git add
```

## Estado final

```text
active_work_item      FOUND-CYCLE-DETECTION-001
work_status           READY
specification_status  READY_FOR_REVIEW
authorized_action     FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_AUTHORIZED
```

Formalização, Floyd, Brent, extração e integração permanecem **não
autorizados**.

## Próxima ação única

Revisar a enumeração de certificados, a executabilidade do detector
parcial, a completude por reutilização da colisão limitada e a viabilidade
de totalização sem escolha clássica.
