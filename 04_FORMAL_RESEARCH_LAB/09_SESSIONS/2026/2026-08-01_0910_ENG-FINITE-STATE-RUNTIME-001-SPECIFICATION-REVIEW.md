---
session_id: 2026-08-01-ENG-FINITE-STATE-RUNTIME-001-SPECIFICATION-REVIEW
date: 2026-08-01
gate: ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_REVIEW
authorized_action: ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_REVIEW_AUTHORIZED
agent: claude-opus-5
commit_before: 4d9e2488accc8d6a952e46b1d995c5e47c498a4f
decision: A_ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_REVIEW_APPROVED
repository_lean_files_created: 0
---

# Sessão — ENG-FINITE-STATE-RUNTIME-001 · revisão da especificação

**O teorema central fecha.** Era essa a condição de aprovação, e ela foi
cumprida em ambiente descartável, com zero erros.

## Preflight

```text
HEAD                  4d9e2488accc8d6a952e46b1d995c5e47c498a4f
árvore                limpa
processos Lean/Lake   nenhum
cat-file -e           0
merge-base ancestor   0   (igualdade aceita)
canonical_commit      23fdf95 -> 4d9e248
```

## `run?_eq_iterate_step` — demonstrado

```lean
theorem run?_eq_iterate_step (t : ValidT) (k : Nat) :
    ∀ start : Fin t.next.size,
      t.toRaw.run? k (start : Nat) =
        some (((t.step)^[k] start : Fin t.next.size) : Nat) := by
  induction k with
  | zero => intro start; rfl
  | succ k ih =>
      intro start
      show (t.toRaw.step? (start : Nat)).bind (t.toRaw.run? k) = _
      rw [t.step?_eq_some_step start]
      show t.toRaw.run? k ((t.step start : Fin t.next.size) : Nat) = _
      rw [ih (t.step start), Function.iterate_succ_apply]
```

Pegada: **`[propext, Quot.sound]`** — sem `Classical.choice`.

### Três detalhes congelados

1. **A generalização vem do enunciado, não da tática.** `∀ start` depois
   de `k`, dentro do tipo; `generalizing` não é usado.
2. **Dois `show` são obrigatórios** — o primeiro expõe o `bind` que a
   notação `do` esconde, o segundo força a redução de
   `Option.bind (some a) f`. Sem eles, nem `rw` nem `simp` acham o padrão.
3. **A orientação auditada na especificação estava certa**:
   `Function.iterate_succ_apply`, não a variante linha.

Também compilaram: `step?_eq_some_step` (via `getElem?_pos`),
`detectCycle?_raw_repeat`, e os dois teoremas de precedência de erro.

## Precedência dos erros — congelada e medida

```text
1. tabela invalida
2. estado inicial invalido
3. falha interna impossivel
4. sucesso
```

Teste decisivo exigido pelo gate:

```text
analyzeT ⟨#[1]⟩ 100  ->  transitionDestinationOutOfBounds
```

Tabela inválida **e** início inválido; o erro de **tabela** vence.

## Achado técnico: as provas de precedência exigem `show`

Três abordagens falham e ficam registradas para não serem repetidas:

```text
simp [..., Except.bind]          ->  unsolved goals
split                             ->  "Could not split"
simp only [...]; simp [hStart]    ->  "made no progress"
```

Motivo: depois de `dif_pos hRaw`, a condição interna usa `validated`
ainda **ligado pelo `do`**; `(⟨raw.next, hRaw⟩).next.size` é *defeq* a
`raw.next.size` mas não sintaticamente igual, e `rw` opera
sintaticamente. O `show` resolve por operar a menos de definicional.

## Correção à auditoria de API

```text
Array.getElem?              nao existe como CONSTANTE   (confirmado)
Array.getElem?_eq_getElem   EXISTE como lema            (novo)
getElem?_pos                EXISTE, e foi o usado       (novo)
```

## Computabilidade

```text
validateT                  [propext, Quot.sound]
validateStartT             [propext, Quot.sound]
run?_eq_iterate_step       [propext, Quot.sound]
analyzeT                   [propext, Classical.choice, Quot.sound]
detectCycle?_raw_repeat    [propext, Classical.choice, Quot.sound]
```

As duas camadas de validação **e** o teorema central de correspondência
**não** dependem de `Classical.choice`. A pegada só entra onde o detector
entra. Isso confirma a arquitetura em camadas: a ponte `Array → Fin` é
axiomaticamente mais leve que o detector que ela alimenta.

## Semântica bruta — não corrigida

```text
run? 0 999 = some 999      inclusive para tabela vazia
run? 1 999 = none
```

A semântica de zero passos permanece. `run?` é parcial e fiel ao array;
`validateStart` é a barreira de segurança.

## O que ainda não tem evidência executável

```text
analyzeTransitionTable_sound e _complete foram PLANEJADAS, nao
demonstradas no probe.
```

São as duas únicas obrigações centrais sem evidência, e o que a
formalização deve atacar primeiro. A mitigação registrada: trabalhar com
`⟨raw.next, hRaw⟩`, cujo `next` é sintaticamente `raw.next`, evitando
transporte dependente entre `Fin validated.next.size` e
`Fin raw.next.size`.

## Validação

```text
probe                          0 erros, removido
pytest                         PASS
labctl validate                PASS
canonical_commit_check         PASS
arquivos Lean no repositorio   0
provas no repositorio          0
implementacao permanente       NAO
lake build                     NAO executado
claims promovidas              0   (ledger em 20)
legado modificado              0
whitespace                     PASS, antes do git add
commit --amend                 NAO usado
```

## Estado final

```text
work_status            READY
specification_status   APPROVED
authorized_action      ENG_FINITE_STATE_RUNTIME_001_FORMALIZATION_AUTHORIZED
```

Extração, CLI, JSON, integração, diagnóstico detalhado, totalização do
detector anterior e Floyd permanecem **não autorizados**.

## Próxima ação única

Formalizar a validação da tabela e do estado inicial, a função total sobre
`Fin n`, a correspondência de iterações, a aplicação do detector e a API
dinâmica baseada em `Except`.
