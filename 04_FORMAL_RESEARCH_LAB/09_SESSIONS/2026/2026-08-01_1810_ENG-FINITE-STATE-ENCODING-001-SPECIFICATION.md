---
session_id: 2026-08-01-ENG-FINITE-STATE-ENCODING-001-SPECIFICATION
date: 2026-08-01
gate: ENG_FINITE_STATE_ENCODING_001_SPECIFICATION
authorized_action: ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_PREPARATION_AUTHORIZED
agent: claude-opus-5
commit_before: 4c15d4aded3ba706efd24c169a2a5a137eebaf5b
decision: A_ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_READY
lean_files_created: 0
---

# Sessão — especificação da codificação certificada

## Preflight

```text
HEAD                  4c15d4aded3ba706efd24c169a2a5a137eebaf5b
historico             confere com os seis commits esperados
arvore                limpa
processos             nenhum
cat-file -e           0
merge-base ancestor   0
canonical_commit      861dc6b -> 4c15d4a
```

## O que esta frente acrescenta

A frente anterior provou algo sobre **a tabela**. Esta prova algo sobre
**a relação entre a tabela e o sistema**. A diferença aparece no
enunciado final:

```lean
stepS^[w.baseIndex + w.period] start = stepS^[w.baseIndex] start
```

Igualdade em `S`. Não sobre `Nat`, não sobre `Fin n`, não sobre o
`Array`.

## A decisão que organiza tudo

```text
a codificacao eh dado executavel FORNECIDO, nunca derivada.
```

`Fintype.equivFin` é `noncomputable`; `Fintype.truncEquivFin` devolve
`Trunc`, que não produz dado. Não há rota computável partindo de
`[Fintype S]`. A estrutura tem quatro campos nomeados, e o consumidor
não precisa de **nenhuma** typeclass.

## O ponto decisivo, como o gate previu

`tableIndex`. Duas coisas foram congeladas:

```text
existem exatamente DOIS pontos de transporte Fin n <-> Fin table.size;
tableIndex_val eh rfl — o cast nao modifica o indice natural.
```

O segundo é o análogo, nesta frente, do `validateStart_sound` da
anterior: o teorema que impede a correção silenciosa de um índice.

## O achado técnico do gate

```text
Array.size_ofFn e Array.getElem_ofFn sao aceitos EM MODO TERMO por defeq
e REJEITADOS por rw/simp, que trabalham em transparencia reduzida.
```

Quatro rotas foram testadas para o lema central de leitura:

| Variante | Tática | Resultado |
|---|---|---|
| `cv1` | `simp [buildTransitionTable]` | falhou |
| `cv2` | `show` + `rw` | quase; objetivo residual |
| `cv3` | `unfold` + `simp` | falhou |
| `cv4` | termo puro | **passou** |

O lema central ficou com **uma linha**.

## O achado que encurtou a frente

```lean
table_iterate_commutes := ((tableIndex_semiconj e stepS).iterate_right k s).symm
```

Um termo. Na frente anterior, o resultado análogo custou indução com
quantificador no enunciado, dois `show` obrigatórios e uma escolha
delicada entre `iterate_succ_apply` e sua variante. `Function.Semiconj`
já encapsula tudo isso.

Em compensação, a orientação inverte: `Semiconj f ga gb` é
`∀ x, f (ga x) = gb (f x)`, que é o `.symm` da comutação. Congelado, com
o motivo escrito.

## Os treze resultados CORE compilaram

Não foram planejados: foram **provados** em dois probes descartáveis,
ambos exit `0`, ambos removidos. Seis erros reais apareceram e foram
corrigidos — o primeiro deles, o mais banal e o mais caro: o namespace
`TamesisLab.Engineering.FiniteStateRuntime` não estava aberto, e **toda**
referência ao runtime adapter falhava.

A soundness e a completeness compilaram na primeira tentativa, como na
frente anterior, e pela mesma razão: o objeto do enunciado é
sintaticamente o objeto da prova.

## O teste que justifica a frente

```text
sistema  0 → 1 → 2 → 3 → 2

codificacao identidade   tabela #[1, 2, 3, 2]   witness ⟨2, 2⟩
codificacao i ↦ 3 - i    tabela #[1, 0, 1, 2]   witness ⟨2, 2⟩
```

Os números mudaram completamente. O witness semântico não.

## A precisão de linguagem congelada

```text
Um erro de codificacao NAO torna falso o certificado sobre a tabela.

O certificado continua correto para aquela tabela, mas pode nao
sustentar nenhuma conclusao sobre o sistema que se pretendia
representar.
```

## O que continua aberto

```yaml
relationship_to_RT_GAP_017:
  status: ADDRESSED_FOR_CERTIFIED_TYPED_SYSTEMS_ONLY
  runtime_item_modified: false
  general_external_system_case: OPEN
```

`RT-GAP-017` não foi alterado retroativamente, e nenhum arquivo da frente
anterior foi tocado. O caso externo geral segue aberto — e a pergunta de
onde vem o objeto tipado pertence a quem modela o sistema.

## Estado final

```text
work_status              READY
specification_status     READY_FOR_REVIEW
formalization_status     NOT_STARTED
authorized_action        ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW_AUTHORIZED
documentos               29
lacunas                  19, nenhuma fechada por expectativa
stop conditions          18, zero disparadas
arquivos Lean            0
provas permanentes       0
lake build               NAO executado
claims                   21, nenhuma promovida
```

## Próxima ação única

Revisar a representação, a construção, a política de casts, a comutação
das iterações e a interpretação tipada do witness. Nada de formalização.
