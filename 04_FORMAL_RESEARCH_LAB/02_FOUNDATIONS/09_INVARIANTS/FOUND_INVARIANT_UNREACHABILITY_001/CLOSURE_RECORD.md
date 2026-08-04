---
document_id: FOUND-INVARIANT-UNREACHABILITY-001-CLOSURE-RECORD
work_item_id: FOUND-INVARIANT-UNREACHABILITY-001
work_status: VERIFIED
result_review: APPROVED
extension_status: NOT_AUTHORIZED
---

# Registro de encerramento

## Estado final

```yaml
active_work_item: FOUND-INVARIANT-UNREACHABILITY-001
work_status: VERIFIED
specification_status: APPROVED
specification_review: APPROVED
formalization_status: VERIFIED
result_review: APPROVED
extension_status: NOT_AUTHORIZED

relational_invariants_status: NOT_AUTHORIZED
monovariant_status: NOT_AUTHORIZED
termination_status: NOT_AUTHORIZED
complete_invariant_status: NOT_AUTHORIZED
nondeterministic_systems_status: NOT_AUTHORIZED

authorized_action: PORTFOLIO_REVIEW_REQUIRED
```

## Os cinco gates

```text
0611e7f  lab: select invariant unreachability toolkit
b835983  lab: specify invariant unreachability toolkit
d5ddb69  lab: review invariant unreachability specification
27b1972  lab: formalize invariant unreachability toolkit
(este)   lab: review invariant unreachability result
```

## A ferramenta

```text
abstract x != abstract y  ->  y nao e alcancavel a partir de x
```

Forma geral de paridade, coloração e monovariante. `[propext]` só.
Nenhuma finitude, nenhuma typeclass, nenhuma decidibilidade.

## O limite

```text
para abstracoes invariantes,
OrbitSeparating  <->  stepC start = start
```

Invariantes certificam **impossibilidade** e nunca **recorrência**.

## Números finais, derivados

```text
modulos Lean criados             4
agregadores modificados          2  (apenas imports)
arquivos de teste                2
declaracoes publicas             8  (3 definicoes, 5 teoremas)
declaracoes TEST_ONLY            2
declaracoes sem pegada alguma    3 de 10
Classical.choice                 0 de 10
typeclasses no nucleo            0
gaps abertos                    10 de 10
stop conditions declaradas      12
stop conditions disparadas       0
defeitos achados pela revisao    1  (contagem agregada a mao)
claims promovidas                1
ledger de claims                25
lake build                       exit 0, 8782 jobs
frentes encerradas modificadas   0
```

## O defeito que a própria frente pegou

A revisão de especificação derivou `12` declarações contra `10`
declaradas. A classificação estava certa — o campo omitia os dois testes.
Corrigido **contra a derivação**, e a proibição correspondente foi
gravada: *não escrever contagem agregada sem derivá-la por script no
mesmo gate*.

## O que fica aberto

```text
INV-GAP-001  completude: existe invariante separador CALCULAVEL?
INV-GAP-009  bibliografia de argumentos de invariante
             DELIBERADAMENTE ABERTA
```

`INV-GAP-001` é a pergunta com conteúdo do assunto. A recíproca ingênua é
vacuamente verdadeira pelo invariante mais fino, e por isso não diz nada.

## Próxima ação

```text
PORTFOLIO_REVIEW_REQUIRED
```

Nenhuma frente nova está escolhida. **Nenhum problema de milênio foi
atacado**, por decisão explícita: a estratégia é acumular ferramentas
antes de abrir tabuleiro. `RH-NOGO-001` permanece `NOT_AUTHORIZED` /
`NO_EXECUTION`.
