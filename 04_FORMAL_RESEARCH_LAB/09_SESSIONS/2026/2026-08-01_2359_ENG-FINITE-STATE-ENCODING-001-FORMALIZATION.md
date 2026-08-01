---
session_id: 2026-08-01-ENG-FINITE-STATE-ENCODING-001-FORMALIZATION
date: 2026-08-01
gate: ENG_FINITE_STATE_ENCODING_001_FORMALIZATION
authorized_action: ENG_FINITE_STATE_ENCODING_001_FORMALIZATION_AUTHORIZED
agent: claude-opus-5
commit_before: bdc67fb9481743a7463ae4b61faa9bc7dca9e5dd
decision: ENG_FINITE_STATE_ENCODING_001_FORMALIZATION_VERIFIED
lean_files_created: 9
---

# Sessão — formalização da codificação certificada

## Preflight

```text
HEAD                  bdc67fb9481743a7463ae4b61faa9bc7dca9e5dd
commits desde 2066edc 2
arvore                limpa
processos             nenhum
canonical_commit      2066edc -> bdc67fb
ENC-VAL-001           encerrado, dois probes com exit 0
```

## O que passou a existir

```text
sistema deterministico tipado S
    |  codificacao FORNECIDA
Fin n
    |  Array.ofFn
ValidatedTransitionTable
    |  runtime adapter, sem copia
CycleWitness
    |  interpretacao
stepS^[b + p] start = stepS^[b] start,  em S
```

```text
1 estrutura, 4 definicoes, 11 teoremas (1 privado), 0 instancias
450 linhas na frente, 298 nos testes
5 modulos + agregador + Audit
lake build PASS, 8757 jobs, 120 s
```

A frente anterior custou `869` linhas. Esta, `450`. A diferença inteira é
reutilização: nem o detector nem a execução bruta foram reescritos.

## Os quatro módulos compilaram na primeira tentativa

A revisão já havia demonstrado a cadeia em probe descartável; a
formalização apenas a tornou permanente. Houve **um** ajuste, e vale
registrar por que:

```text
especificacao:  simpa using (tableIndex stepS start).isLt
linter:         "try 'simp' instead of 'simpa'"
adotado:        rw [buildTransitionTable_size]; exact (encode start).isLt
```

Com `buildTransitionTable_size` e `tableIndex_val` ambos `@[simp]`, o
`using` virou supérfluo. A rota explícita não depende do conjunto `simp`
e não emite aviso.

## Onde o auxiliar privado teve de morar

`buildTransitionTable_getElem` é `private`, e `private` em Lean 4 é
escopo de **módulo**. Seu único consumidor é `tableIndex_semiconj`. Se
ficasse em `TableConstruction.lean`, seria inacessível de
`Commutation.lean` — e torná-lo público contrariaria a revisão.

Resolução: ele vive em `Commutation.lean`. É a única disposição que
satisfaz simultaneamente "privado" e "utilizável".

## O termo de uma linha

```lean
theorem CertifiedFiniteEncoding.table_iterate_commutes (encoding) (stepS) (k) (s) :
    ((buildTransitionTable encoding stepS).step)^[k] (encoding.tableIndex stepS s)
      = encoding.tableIndex stepS (stepS^[k] s) :=
  ((encoding.tableIndex_semiconj stepS).iterate_right k s).symm
```

Na frente anterior, o resultado análogo custou indução manual com
quantificador no enunciado, dois `show` obrigatórios e a escolha delicada
entre `iterate_succ_apply` e sua variante. Aqui, `Function.Semiconj` já
encapsula tudo.

## A soundness termina em `S`

```lean
  have hrun := (analyzeTransitionTable_sound h).2.2
  rw [run?_corresponds_to_typed_iterate ..., run?_corresponds_to_typed_iterate ...] at hrun
  exact encoding.encode_injective (Fin.ext (Option.some.inj hrun))
```

Quatro linhas, e as três últimas setas do DAG — `Option.some.inj`,
`Fin.ext`, `encode_injective` — **não dependem de axioma nenhum**.

Zero `cast`, zero `Eq.ndrec`, zero transporte dependente: a expressão do
enunciado é sintaticamente a expressão da prova.

## O teste que justifica a frente

```text
codificacao identidade   tabela #[1, 2, 3, 2]
codificacao i ↦ 3 - i    tabela #[1, 0, 1, 2]
```

E os dois derivam, pela soundness, **a mesma igualdade no tipo
original**:

```lean
tailStep^[2 + 2] ⟨0, _⟩ = tailStep^[2] ⟨0, _⟩
```

Os witnesses concretos coincidiram em `⟨2,2⟩`. Isso é **observação de
teste**, não teorema — provar a invariância exigiria provar que a ordem
de busca do detector não importa. `ENC-GAP-020`, `STOP-ENC-019`.

## O tipo vazio

A tabela é construída e é `#[]`. `analyzeEncodedSystem` exige
`start : Empty`, que não existe: a ausência de chamada é garantida pelo
**sistema de tipos**.

Na frente anterior, a tabela vazia era válida e a consulta era rejeitada
**com erro**, porque o índice chegava como `Nat`. As duas respostas são
coerentes, e a diferença é onde a informação de domínio mora.

## O que foi medido

```text
sorryAx                     0
axiomas locais              0
tokens proibidos            0
correcoes silenciosas       0
Eq.ndrec, cast_heq, HEq     0
pontos de transporte        2
cycleCandidates             0
pigeonhole                  0
detector copiado            0
segunda execucao            0
lake build                  8757 jobs, baseline 8748, delta 9
```

O delta de `9` é exatamente 5 módulos + agregador + 3 testes.

## Uma correção honesta

`FINAL_PUBLIC_API.md` declarava `14` declarações públicas e listava
**quinze**. O número medido nos módulos é `15`. Erro de cabeçalho do gate
de revisão — a mesma classe de defeito que já apareceu duas vezes neste
laboratório, e pela mesma causa: contagem escrita à mão.

## Estado final

```text
work_status              VERIFIED
formalization_status     VERIFIED
authorized_action        ENG_FINITE_STATE_ENCODING_001_RESULT_REVIEW_AUTHORIZED
declaracoes publicas     15
auxiliares internos      1
lacunas                  20: 15 resolvidas, 5 abertas
claims                   22, uma promovida
```

## Próxima ação única

Revisar a API pública, os dois pontos de transporte, a semiconjugação, a
correspondência de iteradas, a soundness e completeness tipadas e os
limites de recodificação — antes de qualquer extração ou integração.
